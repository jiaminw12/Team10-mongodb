#!/usr/bin/env python

import pymongo

from time import gmtime, strftime

class StockLevelTransaction(object):

	def __init__(self, session, w_id, d_id, stockThreshold, numOfLastOrder):
		self.session = session
		self.w_id = w_id
		self.d_id = d_id
		self.stockThreshold = stockThreshold
		self.numOfLastOrder = numOfLastOrder
	
	def process(self):
		
		# prepare statement
		# get the next_o_id N
		warehouseDistrictRowAggregate = [{"$match": {"w_id": int(self.w_id)}}, {"$project": {"district": {"$filter": {"input": "$district", "as": "district", "cond":{"$eq": ["$$district.d_id", int(self.d_id)]}}}, "_id": 0}}]
		resultDNextOId = list(self.session.warehouse_district.aggregate(warehouseDistrictRowAggregate))[0]["district"][0]["d_next_o_id"]

		# get set of items from the last L orders
		startOrderId = resultDNextOId - int(self.numOfLastOrder)
		lastOrderListCollection = self.session.order.find({"o_w_id":int(self.w_id), "o_d_id": int(self.d_id), "o_id":{"$gte": startOrderId, "$lt": resultDNextOId}})[0]["o_line"]

		#for every order in last order list collection, extract item id
		for item in lastOrderListCollection:
			
			item_id = item["ol_i_id"]
			resultCount = self.session.stock_item.aggregate([{"$match":{"$and":[{"s_w_id": {"$eq":int(self.w_id)}}, {"s_i_id":{"$eq":int(item_id)}}, {"s_quantity":{"$lt":int(self.stockThreshold)}}]}}])
			
			finalResult = list(resultCount)
			
			if finalResult:
				print "Items below threshold\n"
				print "Item ID: %d \t 	Total quantity: %d\n" % (item_id, finalResult[0]["s_quantity"])
