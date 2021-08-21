import numpy as np

n = input("Enter the number of nodes(n): ")
z = input("Enter the percent of slow nodes(z): ")
T_tx = inuput("Enter the mean interarrival time of transactions(T_tx): ")

node_list=[]
for i in range(n):
	speed = np.random.uniform()
	if speed<(z/100):
		speed = 0
	else:
		speed=1
	real_node = node(i+1,speed,T_tx)
	node_list.append(real_node)