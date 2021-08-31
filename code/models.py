import numpy as np
import random

# node_list=[]

class Node:
	def __init__(self,id,speed,bal,peers,gen_blk,mining_block):
		self.id = id
		self.speed= speed
		self.bal = bal
		self.peers = peers
		self.genesis_blk = gen_blk
		self.mining_blk = mining_block # Block object
		self.trxn_cnt = 0
		self.blk_cnt = 0
		self.trxn_pool=[]

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

class Block:
	def __init__(self,blk_id,parent_id,trxn_list,level,parent_ptr):
		self.blk_id = blk_id
		self.parent_id = parent_id
		self.trxn_list = trxn_list
		self.level = level
		self.parent_ptr = parent_ptr
		self.child_ptr_list = []