import numpy as np
import simpy
from networkgen import *
from models import *

#input---------------------------------------------------------------------------------------------------------
n = int(input("Enter the number of nodes(n): "))
z = int(input("Enter the percent of slow nodes(z): "))
T_tx = int(input("Enter the mean interarrival time of transactions(T_tx): "))

# Setup--------------------------------------------------------------------------------------------------------

# Global Variables
env = simpy.Environment()
stop_time = 5
all_balance=20 # initial balance of all users
invalid_trxn_ratio = 0.1
genesis_block = Block('gen','none',[],0,'none')
B_tx = 5 # average time of block creation (change this value) 

node_list=[]
weights = []

# nodes creation
for i in range(n):
	speed = np.random.uniform()
	if speed<(z/100):
		speed = 0
	else:
		speed=1
	node = Node(i,speed,all_balance,[],genesis_block,genesis_block)
	node_list.append(node)
	weights.append(0.1+0.9*speed)

#network generation
adj = networkgen(n,2,weights)
for i in range(n):
	for j in range(i+1):
		if(adj[i][j]==1):
			r_ij = np.random.uniform(10,500);
			if(node_list[i].speed==1 and node_list[j].speed==1):
				c_ij=100
			else:
				c_ij=5
			connect_j = link(j,r_ij,c_ij)
			connect_i = link(i,r_ij,c_ij)
			node_list[i].peers.append(connect_j)
			node_list[j].peers.append(connect_i)

# for i in node_list:
# 	for l in i.peers:
# 		print('Node %d: linked to %d with r_ij=%d,c_ij=%d' % (i.id,l.j,l.r_ij,l.c_ij))

# helper functions

def route_trxn(node_id,trxn,lat,f_id):
	yield env.timeout(lat)
	print('Node %d : got packet %s at %f' % (node_id,trxn.id,env.now))
	if(trxn.coins<=node_list[trxn.payer].bal):
		present = False
		for i in node_list[node_id].trxn_pool:
			if(i.id == trxn.id):
				present=True
		if(not present):
			node_list[node_id].trxn_pool.append(trxn)
			for l in node_list[node_id].peers:
				if(l.j!=f_id):
					d_ij = np.random.exponential(96/l.c_ij)
					lat = (l.r_ij+d_ij+8/l.c_ij)*(0.001)
					print('routing trxn %s to %d with delay = %f' % (trxn.id,l.j,lat))
					env.process(route_trxn(l.j,trxn,lat,node_id))

def broadcast_trxn(node_id,trxn):
	for l in node_list[node_id].peers:
		d_ij = np.random.exponential(96/l.c_ij)
		lat = (l.r_ij+ d_ij+ 8/l.c_ij)*(0.001)
		print('broadcasting trxn %s to %d with delay = %f' % (trxn.id,l.j,lat))
		env.process(route_trxn(l.j,trxn,lat,node_id))

def create_trxn(node_id):
	while True:
		yield env.timeout(np.random.exponential(T_tx))
		vendor = random.randint(0,n-2)
		if(vendor>=node_id):
			vendor=vendor+1
		valid = np.random.uniform()
		pay=0
		if valid<invalid_trxn_ratio:
			pay = node_list[node_id].bal+10
		else:
			pay = random.randint(1,node_list[node_id].bal)

		node_list[node_id].trxn_cnt = node_list[node_id].trxn_cnt+1
		trxn_id = str(node_id)+"_"+str(node_list[node_id].trxn_cnt)
		str_trxn = str(trxn_id)+": "+str(node_id)+" pays "+str(vendor)+" "+str(pay)+" coins"
		print(str_trxn + ' at %f' % env.now)
		real_trxn = Trxn(trxn_id,node_id,vendor,pay)
		broadcast_trxn(node_id,real_trxn)
		node_list[node_id].trxn_pool.append(real_trxn)

def get_balance(itr_node): # checked 
	calc_bal = []
	for i in range(n):
		calc_bal.append(all_balance)
	while itr_node!='none':
		trxns = itr_node.trxn_list
		for t in trxns:
			if t.payer!=-1:
				calc_bal[t.payer] = calc_bal[t.payer]-t.coins
			calc_bal[t.payee] = calc_bal[t.payee]+t.coins
		itr_node = itr_node.parent_ptr
	return calc_bal

def get_parent(blk,check_blk): #checked
	if(check_blk.blk_id == blk.parent_id):
		return check_blk
	elif (len(check_blk.child_ptr_list)==0):
		return 0
	else:
		for child in check_blk.child_ptr_list:
			temp = get_parent(blk,child)
			if temp!=0:
				return temp
		return 0 

def is_valid(node_id,blk): #checked
	parent = get_parent(blk,node_list[node_id].genesis_blk)
	if parent!=0:
		for child in parent.child_ptr_list:
			if blk.blk_id == child.blk_id:
				return 0
		calc_bal = get_balance(parent)
		for t in blk.trxn_list:
			if t.payer!=-1:
				calc_bal[t.payer] = calc_bal[t.payer]-t.coins
			calc_bal[t.payee] = calc_bal[t.payee]+t.coins
		valid = True
		for i in calc_bal:
			if i<0:
				valid = False
		if valid:
			return parent
		else:
			return 0
	return 0

def route_blk(node_id,blk,lat,f_id): #checked
	yield env.timeout(lat)
	print('Node %d : got blk %s at %f' % (node_id,blk.blk_id,env.now))
	parent = is_valid(node_id,blk)

	if(parent!=0): 
		blk.parent_ptr = parent 
		blk.level = parent.level+1
		parent.child_ptr_list.append(blk)
		for l in node_list[node_id].peers:
			if(l.j!=f_id):
				d_ij = np.random.exponential(96/l.c_ij)
				blk_size= len(blk.trxn_list)
				lat = (l.r_ij+d_ij+8*blk_size/l.c_ij)*(0.001)
				print('routing block %s to %d with delay = %f' % (blk.blk_id,l.j,lat))
				env.process(route_blk(l.j,blk,lat,node_id))
		if blk.level > node_list[node_id].mining_blk.level:
			node_list[node_id].mining_blk = blk
			create_blk(node_id)


def broadcast_blk(node_id,blk): #checked
	yield env.timeout(np.random.exponential(B_tx))
	if node_list[node_id].mining_blk.blk_id == blk.parent_id:
		for l in node_list[node_id].peers:
			d_ij = np.random.exponential(96/l.c_ij)
			blk_size= len(blk.trxn_list)
			lat = (l.r_ij+ d_ij+ 8*blk_size/l.c_ij)*(0.001)
			print('broadcasting block %s to %d with delay = %f' % (blk.blk_id,l.j,lat))
			env.process(route_blk(l.j,blk,lat,node_id))
		create_blk(node_id)

def get_trxns(itr_node): # checked
	all_trxns = []
	while itr_node!='none':
		all_trxns.extend(itr_node.trxn_list)
		itr_node = itr_node.parent_ptr
	return all_trxns

def create_blk(node_id): # checked
		node_list[node_id].blk_cnt = node_list[node_id].blk_cnt+1
		blk_id = 'b'+str(node_id)+'_'+str(node_list[node_id].blk_cnt)
		
		parent_id = node_list[node_id].mining_blk.blk_id
		
		trxn_list = []# get the trxn list
		node_list[node_id].trxn_cnt =node_list[node_id].trxn_cnt+1
		mining_trxnid = str(node_id)+'_'+str(node_list[node_id].trxn_cnt)
		trxn_list.append(Trxn(mining_trxnid,-1,node_id,50))
		# add other trxns
		calc_bal = get_balance(node_list[node_id].mining_blk)
		done_trxns = get_trxns(node_list[node_id].mining_blk)
		useful_trxns = [ele for ele in node_list[node_id].trxn_pool if ele not in done_trxns]
		for t in useful_trxns:
			if(((calc_bal[t.payer]-t.coins)>=0) and len(trxn_list)<1000):
				trxn_list.append(t)
				calc_bal[t.payer] = calc_bal[t.payer]-t.coins
				calc_bal[t.payee] = calc_bal[t.payee]+t.coins

		level = node_list[node_id].mining_blk.level+1
		
		parent_ptr = node_list[node_id].mining_blk
		
		new_blk = Block(blk_id,parent_id,trxn_list,level,parent_ptr)

		print('Block %s is created at t = %f with num_trxns = %d' % (blk_id,env.now,len(trxn_list)))
		for i in trxn_list:
			print(i.id)
		
		env.process(broadcast_blk(node_id,new_blk))


# Simulation---------------------------------------------------------------------------------------------------

for i in node_list:
	env.process(create_trxn(i.id))
	create_blk(i.id)

env.run(until=stop_time)