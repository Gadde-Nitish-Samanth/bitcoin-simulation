import numpy as np
import random

# node_list=[]

class Node:
	def __init__(self,id,speed,ttx,bal,peers,env):
		self.id = id
		self.speed= speed
		self.ttx = ttx
		self.bal = bal
		self.peers = peers
		self.env = env
		self.trxn_cnt = 0
		self.trxn_pool=[]
		# self.action = env.process(self.create_trxn())

	# def create_trxn(self):
	# 	#time = np.random.exponential(self.T_tx)
		
	# 	while True:
	# 		yield self.env.timeout(np.random.exponential(self.ttx))
	# 		vendor = random.randint(1,self.n-1)
	# 		if(vendor>=self.id):
	# 			vendor=vendor+1
	# 		valid = np.random.uniform()
	# 		pay=0
	# 		if valid<self.invalid_percent:
	# 			pay = self.bal+10
	# 		else:
	# 			pay = random.randint(1,self.bal)

	# 		self.trxn_cnt = self.trxn_cnt+1
	# 		trxn_id = str(self.id)+"_"+str(self.trxn_cnt)
	# 		trxn = str(trxn_id)+": "+str(self.id)+" pays "+str(vendor)+" "+str(pay)+" coins"
	# 		print(trxn + ' at %d' %self.env.now)
	# 		real_trxn = trxn(trxn_id,self.id,vendor,pay)
	# 		self.broadcast_trxn(real_trxn)
	# 	#return real_trxn

	# def broadcast_trxn(self,trxn):
	# 	for l in peers:
	# 		d_ij = np.random.exponential(96/l.c_ij)
	# 		lat = (l.r_ij+ d_ij+ 8/l.c_ij)*(0.001)
	# 		node = l.j
	# 		node.input_trxn(trxn,lat,self.id)

	# def input_trxn(self,trxn,lat,f): #f is id
	# 	yield self.env.timeout(lat)
	# 	if(trxn.coins>trxn.payer.balance):


	# 	
class Trxn:
	def __init__(self,txnID,F,to,coins): #payer and payee are id's
		self.id = txnID
		self.payer = F
		self.payee = to
		self.coins = coins

class link:
	def __init__(self,j,r_ij,c_ij): #j is id
		self.j = j
		self.r_ij = r_ij
		self.c_ij = c_ij 