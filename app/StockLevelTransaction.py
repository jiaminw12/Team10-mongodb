#!/usr/bin/env python

import pymongo

from time import gmtime, strftime

class StockLevelTransaction(object):

	def __init__(self, session, w_id, d_id, stockThreshold, numOfLastOrder):
		self.session = session
		self.consistencyLevel = consistencyLevel
		self.w_id = w_id
		self.d_id = d_id
		self.stockThreshold = stockThreshold
		self.numOfLastOrder = numOfLastOrder
		self.initPreparedStmts()
	
	def initPreparedStmts(self):
		# prepare statement
		# get the next_o_id N
		self.select_d_next_o_id = self.session.prepare("SELECT D_NEXT_O_ID FROM district WHERE d_w_id = ? AND d_id = ?")
		# get set of items from the last L orders
		self.select_last_l_order = self.session.prepare("SELECT OL_I_ID FROM orderline WHERE OL_W_ID = ? AND OL_D_ID = ? AND OL_O_ID >= ? AND OL_O_ID < ?")
		
		# get total number of items in S where its stock quantity < T
		#self.select_quantity = self.session.prepare("SELECT count(i_id)as countno FROM ITEM_BY_WAREHOUSE_DISTRICT WHERE w_id = ? AND i_id = ? AND s_quantity < ? ALLOW FILTERING")
		self.select_quantity = self.session.prepare("SELECT count(s_i_id)as countno FROM stockitem WHERE s_w_id = ? AND s_i_id = ? AND s_quantity < ? ALLOW FILTERING")

	def process(self):
		# execute
		next_oid = self.session.execute(self.select_d_next_o_id, (int(self.w_id), int(self.d_id)))
		next_o_id = next_oid[0].d_next_o_id
		
		last_l_orders = self.session.execute(self.select_last_l_order,(int(self.w_id), int(self.d_id), (int(next_o_id) - int(self.numOfLastOrder)), int(next_o_id)))
		print "Items below threshold\n"
		for row in last_l_orders:
			execute_count = self.session.execute(self.select_quantity, (int(self.w_id), int(row.ol_i_id), int(self.stockThreshold)))
			#print "Order item ID: %d\n"%(row.ol_i_id)
			if execute_count[0].countno > 0:
				print "Item ID: %d \nNumber: %d\n"%(row.ol_i_id, execute_count[0].countno)







