#!/usr/bin/env python

import pymongo

from decimal import *

class PopularItemTransaction(object):
	
	global popular_item

	def __init__(self, session, w_id, d_id, numOfLastOrder):
		self.session = session
		self.w_id = w_id
		self.d_id = d_id
		self.numOfLastOrder = numOfLastOrder
		self.initPreparedStmts()
	
	def initPreparedStmts(self):
		self.select_d_next_o_id = self.session.prepare("SELECT d_next_o_id FROM district WHERE d_w_id = ? AND d_id = ?");

		self.select_last_order_id = self.session.prepare("SELECT o_id FROM order_by_desc WHERE o_w_id = ? AND o_d_id = ? AND o_id >= ? AND o_id < ?")

		self.select_last_order = self.session.prepare("SELECT o_c_id, o_entry_d FROM order_by_desc WHERE o_w_id = ? AND o_d_id = ? AND o_id = ?")

		self.select_customer_name = self.session.prepare("SELECT c_first, c_middle, c_last FROM payment_by_customer WHERE c_w_id = ? AND c_d_id = ? AND c_id = ?")

		self.select_max_quantity = self.session.prepare("SELECT max(ol_quantity) as max_quantity FROM orderline WHERE ol_w_id = ? AND ol_d_id = ? AND ol_o_id = ?");

		self.select_max_quantity_item  = self.session.prepare("SELECT ol_i_id, ol_quantity FROM orderline WHERE ol_w_id = ? AND ol_d_id = ? AND ol_o_id = ? AND ol_quantity = ? ALLOW FILTERING");

		self.select_item_name = self.session.prepare("SELECT i_name FROM stockitem WHERE s_w_id = ? AND s_i_id = ?");

	def process(self):
		
		popular_item = dict()
		
		print "District identifier: w_id -  %s, d_id - %s"%(self.w_id, self.d_id)
		print "Number of last orders to be examined, L: %s"%(self.numOfLastOrder)

		# 1. Find N - the next available order number
		result_d_next_o_id = self.session.execute(self.select_d_next_o_id, [int(self.w_id), int(self.d_id)])
		nextAvailableOrderNum = int(result_d_next_o_id[0].d_next_o_id)

		# 2. Find S - the set of last L orders and order lines for district
		startOrderId = nextAvailableOrderNum - int(self.numOfLastOrder)

		result_last_order_id = self.session.execute(self.select_last_order_id, [int(self.w_id), int(self.d_id), startOrderId, nextAvailableOrderNum])
		
		for row in result_last_order_id:

			o_id = int(row[0])
			
			result_last_order = self.session.execute(self.select_last_order, [int(self.w_id), int(self.d_id), o_id])
			
			if result_last_order[0].o_c_id is not None:
				o_c_id = int(result_last_order[0].o_c_id)
				o_entry_d = result_last_order[0].o_entry_d

				print "O_ID: %d, O_ENTRY_D: %s "%(o_id, o_entry_d)
			
				result_customer_name = self.session.execute(self.select_customer_name, [int(self.w_id), int(self.d_id), o_c_id])
			
				print "C_FIRST: %s,  C_MIDDLE: %s,  C_LAST: %s"%(result_customer_name[0].c_first, result_customer_name[0].c_middle, result_customer_name[0].c_last)
			
				# 3. Find max quantity
				result_max_quantity= self.session.execute(self.select_max_quantity, [int(self.w_id), int(self.d_id), o_id])
				if result_max_quantity[0].max_quantity is not None:
					max_num = int(result_max_quantity[0].max_quantity)
			
					# 4. Get the set with max quantity
					result_max_quantity_item= self.session.execute(self.select_max_quantity_item, [int(self.w_id), int(self.d_id), o_id, max_num])
			
					for rowPopular in result_max_quantity_item:
				
						# 5. Find item name
						result_item_name= self.session.execute(self.select_item_name, [int(self.w_id), rowPopular.ol_i_id])
				
						#print "I_ID: %d"%(rowPopular.ol_i_id)
						print "I_NAME: %s"%(result_item_name[0].i_name)
						print "OL_QUANTITY: %0.2f"%(rowPopular.ol_quantity)
						print "\n"
	
						if result_item_name[0].i_name in popular_item:
							popular_item[result_item_name[0].i_name] += 1
						else:
							popular_item[result_item_name[0].i_name] = 1


		# 6. Find the percentage of examined of orders that contain each popular item
		#print (popular_item)

		for key, value in popular_item.iteritems():
			print "I_NAME: %s"%(key)
			print "Percentage of orders in S: %0.2f"%(Decimal(int(value)/int(self.numOfLastOrder)*100))
			print "\n"


