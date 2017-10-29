#!/usr/bin/env python

from decimal import *

import pprint

class PopularItemTransaction(object):

	global popular_item

	def __init__(self, session, w_id, d_id, numOfLastOrder):
		self.session = session
		self.w_id = w_id
		self.d_id = d_id
		self.numOfLastOrder = numOfLastOrder

	def process(self):

		popular_item = dict()

		print "District identifier: w_id -  %s, d_id - %s"%(self.w_id, self.d_id)
		print "Number of last orders to be examined, L: %s"%(self.numOfLastOrder)

		# Get d_next_o_id
		warehouseDistrictRowAggregate = [{"$match": {"w_id": int(self.w_id)}}, {"$project": {"district": {"$filter": {"input": "$district", "as": "district", "cond":{"$eq": ["$$district.d_id", int(self.d_id)]}}}, "_id": 0}}]

		resultDNextOId = list(self.session.warehouse_district.aggregate(warehouseDistrictRowAggregate))[0]["district"][0]["d_next_o_id"]

		# Get set of last L orders with orderline
		startOrderId = resultDNextOId - int(self.numOfLastOrder)

		lastOrderListCollection = self.session.order.find({"o_w_id":int(self.w_id), "o_d_id": int(self.d_id), "o_id":{"$gte": startOrderId, "$lt": resultDNextOId}})

		for orderItem in lastOrderListCollection:
			print "O_ID: %d, O_ENTRY_D: %s "%(orderItem["o_id"], orderItem["o_entry_d"])

			customerCollection = self.session.customer.find_one({"c_w_id":int(self.w_id), "c_d_id":int(self.d_id), "c_id": int(orderItem["o_c_id"])})
			print "C_FIRST: %s,  C_MIDDLE: %s,  C_LAST: %s"%(customerCollection["c_first"], customerCollection["c_middle"], customerCollection["c_last"])

			orderAggregate = [{"$match": {"o_w_id": int(orderItem["o_w_id"]), "o_d_id": int(orderItem["o_d_id"]), "o_id": int(orderItem["o_id"])}}, {"$unwind": "$o_line"}, {"$sort":{"o_line.ol_quantity":-1}}, {"$limit":1}]
			resultMaxQuantity = list(self.session.order.aggregate(orderAggregate))

			resultItemName = self.session.stock_item.find({"s_w_id":int(self.w_id), "s_i_id": int(resultMaxQuantity[0]["o_line"]["ol_i_id"])})
			
			if "i_name" in resultItemName[0]:
				print "I_NAME: %s"%(resultItemName[0]["i_name"])
				print "OL_QUANTITY: %0.2f"%(resultMaxQuantity[0]["o_line"]["ol_quantity"])

				if resultItemName[0]["i_name"] in popular_item:
					resultItemName[0]["i_name"] += 1
				else:
					resultItemName[0]["i_name"] = 1
			print "\n"
							
		for key, value in popular_item.iteritems():
			print "I_NAME: %s"%(key)
			print "Percentage of orders in S: %0.2f"%(Decimal(int(value) /int(self.numOfLastOrder)*100))
			print "\n"


																									 
