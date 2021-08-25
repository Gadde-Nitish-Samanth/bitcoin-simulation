import numpy as np
import simpy
from networkgen import *
from models import *

#input---------------------------------------------------------------------------------------------------------
n = int(input("Enter the number of nodes(n): "))
z = int(input("Enter the percent of slow nodes(z): "))
T_tx = int(input("Enter the mean interarrival time of transactions(T_tx): "))

# Setup--------------------------------------------------------------------------------------------------------

# nodes creation
node_list=[]
weights = []
all_balance=20 # initial balance of all users
invalid_trxn_ratio = 0.1 # fraction of invalid trxns generated
env = simpy.Environment()

for i in range(n):
	speed = np.random.uniform()
	if speed<(z/100):
		speed = 0
	else:
		speed=1
	node = Node(i,speed,T_tx,all_balance,[],env)
	node_list.append(node)
	weights.append(0.1+0.9*speed)

#network generation
adj = networkgen(n,2,weights)
for i in range(n):
	temp=[]
	for j in range(n):
		if(adj[i][j]==1):
			r_ij = np.random.uniform(10,500);
			if(node_list[i].speed==1 and node_list[j].speed==1):
				c_ij=100
			else:
				c_ij=5
			connect = link(j,r_ij,c_ij)
			temp.append(connect)
	node_list[i].peers = temp

# helper functions

def route_trxn(node_id,trxn,lat,f_id):
	print('inside route_trxn')
	yield node_list[node_id].env.timeout(lat)
	print('node %d : got packet at %d' % (node_id,node_list[node_id].env.now))
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
					node= node_list[l.j]
					env.process(route_trxn(l.j,trxn,lat,node_id))

def broadcast_trxn(node_id,trxn):
	for l in node_list[node_id].peers:
		d_ij = np.random.exponential(96/l.c_ij)
		lat = (l.r_ij+ d_ij+ 8/l.c_ij)*(0.001)
		print('Node %d : broadcasting to %d' % (node_id,l.j))
		env.process(route_trxn(l.j,trxn,lat,node_id))
	print('Node %d : completed broadcasting' % node_id)

def create_trxn(node_id):
	while True:
		yield node_list[node_id].env.timeout(np.random.exponential(node_list[node_id].ttx))
		vendor = random.randint(1,n-1)
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
		print(str_trxn + ' at %d and bal: %d' % (node.env.now,node_list[node_id].bal))
		real_trxn = Trxn(trxn_id,node_id,vendor,pay)
		broadcast_trxn(node_id,real_trxn)


# Simulation---------------------------------------------------------------------------------------------------

for i in node_list:
	env.process(create_trxn(i.id))

stop_time = 10
env.run(until=stop_time)