#!/usr/bin/env python

import pymongo

from time import gmtime, strftime

class OrderStatusTransaction(object):

	def __init__(self, session, c_w_id, c_d_id, c_id):
		self.session = session
		self.consistencyLevel = consistencyLevel
		self.c_w_id = c_w_id
		self.c_d_id = c_d_id
		self.c_id = c_id
		self.initPreparedStmts()
	
	def initPreparedStmts(self):
		# get the customer's last order
		self.select_customer_las_order = self.session.prepare("SELECT c_first, c_middle, c_last, c_balance from payment_by_customer WHERE c_w_id = ? and c_d_id = ? and c_id = ?")
		
		# get the last order id
		self.select_last_order = self.session.prepare("select o_id, o_entry_d, o_carrier_id from Order_By_Desc where o_w_id = ? AND o_d_id = ? AND o_c_id = ? LIMIT 1 ALLOW FILTERING")
	
		self.select_order = self.session.prepare("SELECT ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_delivery_d from OrderLine where ol_w_id = ? AND ol_d_id = ? AND ol_o_id = ? ALLOW FILTERING")


	def process(self):
		
		orderid = self.session.execute(self.select_last_order, (int(self.c_w_id), int(self.c_d_id), int(self.c_id)))
		
		if orderid :
			lastorder = orderid[0]

			# execute
			customerdetails = self.session.execute(self.select_customer_las_order, (int(self.c_w_id), int(self.c_d_id), int(self.c_id)));
		
			# print output 1. customer name and balance 2. its order
			customer = customerdetails[0]
			print "Customer name: %s %s %s, Balance amount: %2f\n"%(customer.c_first, customer.c_middle, customer.c_last, customer.c_balance)

			# print order with items
			orderdetails = self.session.execute(self.select_order,(int(self.c_w_id), int(self.c_d_id), int(lastorder.o_id)))
			temp = orderdetails[0];
			print "order ID: %d\t Entry Date: %s\t Carrier ID: %s\t\n" % (lastorder.o_id, lastorder.o_entry_d, lastorder.o_carrier_id)
		
			for row in orderdetails:
				print "Item ID: %d\t Supply Warehouse ID: %d\t Quantity: %d\t Amount: %f\t Delivery Date: %s\n" % (row.ol_i_id, row.ol_supply_w_id, row.ol_quantity, row.ol_amount,row.ol_delivery_d)
