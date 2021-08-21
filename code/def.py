import numpy as np
import random

invalid_percent = 0.1 #fraction of invalid-trxns generated 
class node :
	def __init__(self,num,speed,ttx,bal,pers):
		self.id = num
		self.type= speed
		self.T_tx = ttx
		self.balance = bal
		self.t_cnt = 0
		self.peers = pers

	def create_trxn():
		#time = np.random.exponential(self.T_tx)
		vendor = random.randint(1,n)
		valid = np.random.uniform()
		pay=0
		if valid<invalid_percent:
			pay = random.randint(1,self.balance)
		else:
			pay = self.balance+10
		#trxn = str(num_trxns)+": "+str(self.id)+" pays "+str(vendor)+" "+str(pay)+" coins"
		self.t_cnt = self.t_cnt+1
		trxn_id = str(self.id)+"_"+str(self.t_cnt)
		real_trxn = trxn(trxn_id,self.id,vendor,pay)
		return real_trxn

	# def send_to_peers(trxn):
	# 	
class trxn:
	def __init__(self,txnID,F,to,coins):
		self.id = txnID
		self.payer = F
		self.payee = to
		self.money = coins

class link:
	def __init__(self,j,r_ij,c_ij):
		self.j = j
		self.r_ij = r_ij
		self.c_ij = c_ij 