#!/usr/bin/env python

from decimal import *
from operator import itemgetter, attrgetter, methodcaller

class TopBalanceTransaction(object):

	def __init__(self, session ):
		self.session = session

	def process(self):
		customerCollection = self.session.customer
		cbalanceCollection = list(customerCollection.find().sort([("c_balance", -1)]).limit(10))
			
		for result in cbalanceCollection:
			print "C_FIRST: %s,  C_MIDDLE: %s,  C_LAST: %s"%(result["c_first"], result["c_middle"], result["c_last"])
			print "C_BALANCE: %f"%(result["c_balance"])
			print "W_NAME: %s"%(result["w_name"])
			print "D_NAME: %s"%(result["d_name"])
			print "\n"
