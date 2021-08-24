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
env = simpy.Environment()

for i in range(n):
	speed = np.random.uniform()
	if speed<(z/100):
		speed = 0
	else:
		speed=1
	node = Node(i+1,speed,T_tx,20,[],n,env)
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
			connect = link(node_list[j],r_ij,c_ij)
			temp.append(connect)
	node_list[i].peers = temp

# helper functions

def create_trxn(node):
		#time = np.random.exponential(self.T_tx)
		
		while True:
			yield node.env.timeout(np.random.exponential(node.ttx))
			vendor = random.randint(1,node.n-1)
			if(vendor>=node.id):
				vendor=vendor+1
			valid = np.random.uniform()
			pay=0
			if valid<node.invalid_percent:
				pay = node.bal+10
			else:
				pay = random.randint(1,node.bal)

			node.trxn_cnt = node.trxn_cnt+1
			trxn_id = str(node.id)+"_"+str(node.trxn_cnt)
			trxn = str(trxn_id)+": "+str(node.id)+" pays "+str(vendor)+" "+str(pay)+" coins"
			print(trxn + ' at %d' %node.env.now)
			# real_trxn = trxn(trxn_id,node.id,vendor,pay)

# Simulation---------------------------------------------------------------------------------------------------

for i in node_list:
	env.process(create_trxn(i))


stop_time = 15
env.run(until=stop_time)