#!/usr/bin/env python

import pymongo

from time import gmtime, strftime

class OrderStatusTransaction(object):

	def __init__(self, session, c_w_id, c_d_id, c_id):
		self.session = session
#		self.consistencyLevel = consistencyLevel
		self.c_w_id = c_w_id
		self.c_d_id = c_d_id
		self.c_id = c_id
#	self.initPreparedStmts()
	
#	def initPreparedStmts(self):
		

	def process(self):
		
		# get collection
		customerCollection = self.session.customer
		orderCollection = self.session.order

		# get the customer's info
		select_customer = customerCollection.find_one({"c_w_id":self.c_w_id,"c_d_id":self.c_d_id,"c_id":self.c_id})
		
		# get the last order id
		select_last_order = orderCollection.find_one({"o_w_id":self.c_w_id,"o_d_id":self.c_d_id,"o_c_id":self.c_id}).sort("o_id",pymongo.DESCENDING)
		lastOrder = select_last_order["o_id"]
		#get list of items
		getItemList = orderCollection.find({"ol_w_id":self.c_w_id, "ol_d_id": self.c_d_id, "ol_o_id":lastOrder},{ol_i_id:1,ol_supply_w_id:1,ol_quantity:1,ol_amount:1,ol_delivery_d:1})
		#self.select_order = self.session.prepare("SELECT ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_delivery_d from OrderLine where ol_w_id = ? AND ol_d_id = ? AND ol_o_id = ? ALLOW FILTERING")


		#print customer info
		print("customer name: %s %s %s\tBalance: %f"%(selected_customer["c_first"], selected_customer["c_middle"], selected_customer["c_last"],selected_customer["c_balance"]))

		#print last order id
		print ("Last Order: %d"%(lastOrder))

		#print item list
		for item in getItemList:
			print "OL_i_ID: %d \t OL_SUPPLY_ID: %d \t OL_QUANTITY: %d \t OL_AMOUNT: %f \t OL_DELIVERY_D: %s "%(item["ol_i_id"], item["ol_supply_w_id"], item["ol_quantity"], item["ol_amount"], item["ol_delivery_d"])
