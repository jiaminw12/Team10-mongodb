#!/usr/bin/env python

import pymongo

from decimal import *
from operator import itemgetter, attrgetter, methodcaller

class Customer(object):
    def __init__(self, c_w_id, c_d_id, c_first, c_middle, c_last, c_balance):
		self.c_w_id = c_w_id
		self.c_d_id = c_d_id
		self.c_first = c_first
		self.c_middle = c_middle
		self.c_last = c_last
		self.c_balance = c_balance

class TopBalanceTransaction(object):

	def __init__(self, session ):
		self.session = session
		self.initPreparedStmts()
	
	def initPreparedStmts(self):
		self.select_stmt = self.session.prepare("SELECT c_w_id, c_d_id, c_first, c_middle, c_last, c_balance FROM top_balance LIMIT 10");
		self.select_w_name = self.session.prepare("SELECT w_name FROM warehouse WHERE w_id = ?");
		self.select_d_name = self.session.prepare("SELECT d_name FROM district WHERE d_w_id = ? AND d_id = ?");

	def process(self):
		# (TOPBALANCE) SELECT C_FIRST, C_MIDDLE, C_LAST, C_BALANCE, W_NAME, D_NAME FROM TOP_BALANCE LIMIT 10
		
		result_count = self.session.execute(self.select_stmt)
		
		result_list = []
		for row in result_count:
			c = Customer(row[0], row[1], row[2], row[3], row[4], row[5])
			result_list.append(c)
		
		result_list.sort(key=lambda x: x.c_balance, reverse=True)
		
		for row in result_list:
			
			result_w_name = self.session.execute(self.select_w_name, [row.c_w_id])
			result_d_name = self.session.execute(self.select_d_name, [row.c_w_id, row.c_d_id])

			print "C_FIRST: %s,  C_MIDDLE: %s,  C_LAST: %s"%(row.c_first, row.c_middle, row.c_last)
			print "C_BALANCE: %f"%(row.c_balance)
			print "W_NAME: %s"%(result_w_name[0])
			print "D_NAME: %s"%(result_d_name[0])
			print "\n"
