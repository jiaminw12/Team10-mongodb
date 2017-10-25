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

	def process(self):
		customerCollection = self.session.customer
		cbalanceCollection = customerCollection.find().sort({("c_balance", -1)}).limit(10)
			
		for result in cbalanceCollection:
			print "C_FIRST: %s,  C_MIDDLE: %s,  C_LAST: %s"%(result["c_first"], result["c_middle"], result["c_last"])
			print "C_BALANCE: %f"%(result["c_balance"])
			print "W_NAME: %s"%(result["w_name"])
			print "D_NAME: %s"%(result["d_name"])
			print "\n"
