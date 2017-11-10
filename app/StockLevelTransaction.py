#!/usr/bin/env python

import pymongo

from time import gmtime, strftime

class StockLevelTransaction(object):

        def __init__(self, session, w_id, d_id, stockThreshold, numOfLastOrder):
                self.session = session
                self.w_id = int(w_id)
                self.d_id = int(d_id)
                self.stockThreshold = int(stockThreshold)
                self.numOfLastOrder = int(numOfLastOrder)

        def process(self):

                # prepare statement
                # get the next_o_id N
                warehouseDistrictRowAggregate = [{"$match": {"w_id": self.w_id}}, {"$project": {"district": {"$filter": {"input": "$district", "as": "district", "cond":{"$eq": ["$$district.d_id", self.d_id]}}}, "_id": 0}}]
                resultDNextOId = list(self.session.warehouse_district.aggregate(warehouseDistrictRowAggregate))[0]["district"][0]["d_next_o_id"]

                # get set of items from the last L orders
                startOrderId = resultDNextOId - int(self.numOfLastOrder)
                #lastOrderListCollection = self.session.order.find({"o_w_id":self.w_id, "o_d_id": self.d_id, "o_id":{"$gte": startOrderId, "$lt": resultDNextOId}})[0]["o_line"]
                lastOrderListCollection = self.session.order.find({"o_w_id":self.w_id, "o_d_id": self.d_id, "o_id":{"$gte": startOrderId, "$lt": resultDNextOId}})
                #for every order in last order list collection, extract item id
                for item in lastOrderListCollection:
                        orderAggregate = [{"$match": {"o_w_id": int(item["o_w_id"]), "o_d_id": int(item["o_d_id"]), "o_id": int(item["o_id"])}}, {"$unwind": "$o_line"}, {"$limit":1}]
                        result = list(self.session.order.aggregate(orderAggregate))
                        item_id = result[0]["o_line"]["ol_i_id"]
                        #print (item_id)
                        resultCount = list(self.session.stock_item.aggregate([{"$match":{"$and":[{"s_w_id": {"$eq":self.w_id}}, {"s_i_id":{"$eq":int(item_id)}}, {"s_quantity":{"$lt":self.stockThreshold}}]}}]))

                        #finalResult = resultCount)
                        if (resultCount):
                                print "Items below threshold"
                                print "Item ID: %d \t   Total quantity: %d\n" % (item_id, resultCount[0]["s_quantity"])
