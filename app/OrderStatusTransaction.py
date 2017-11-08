#!/usr/bin/env python

import pymongo

from time import gmtime, strftime

import pprint

class OrderStatusTransaction(object):

	def __init__(self, session, c_w_id, c_d_id, c_id):
		self.session = session
		self.c_w_id = int(c_w_id)
		self.c_d_id = int(c_d_id)
		self.c_id = int(c_id)

	def process(self):
	
		# get collection
		customerCollection = self.session.customer
		orderCollection = self.session.order

		# get the customer's info
		selected_customer = customerCollection.find_one({"c_w_id":self.c_w_id,"c_d_id":self.c_d_id,"c_id":self.c_id})
		
		# get the last order id
		select_last_order = orderCollection.find_one({"o_w_id":self.c_w_id,"o_d_id":self.c_d_id,"o_c_id":self.c_id}, sort = [("o_id",pymongo.DESCENDING)])
		
		if select_last_order:
		
			lastOrder = select_last_order["o_id"]
			
			getOrderLineList = select_last_order["o_line"]
			
			#print customer info
			print("Customer name: %s %s %s\tBalance: %f"%(selected_customer["c_first"], selected_customer["c_middle"], selected_customer["c_last"],selected_customer["c_balance"]))

			#print last order id
			print ("Last Order: %d" % (lastOrder))
			
			print ("Entry Date: %s \t Carrier ID: %d \n"%(select_last_order["o_entry_d"], select_last_order["o_carrier_id"]))
			
			#print item list
			for orderLineItem in getOrderLineList:
				print "OL_i_ID: %d \t OL_SUPPLY_ID: %d \t OL_QUANTITY: %d \t OL_AMOUNT: %f \t OL_DELIVERY_D: %s "%(orderLineItem["ol_i_id"], orderLineItem["ol_supply_w_id"], orderLineItem["ol_quantity"], orderLineItem["ol_amount"], orderLineItem["ol_delivery_d"])
