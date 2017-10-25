#!/usr/bin/env python

import sys
import pymongo

from pymongo import MongoClient

client = MongoClient(sys.argv[1], int(sys.argv[2]))
db = client.team10 # Getting a database

# Getting a collection, create indexes
collection = db.order.create_index([('o_w_id', pymongo.ASCENDING), ('o_d_id', pymongo.ASCENDING), ('o_id', pymongo.ASCENDING)])

#find all orderline
orderlineCollection = db.orderline
for orderline in orderlineCollection.find():
	ol_w_id = orderline["ol_w_id"]
	ol_d_id = orderline["ol_d_id"]
	ol_o_id = orderline["ol_o_id"]
	
	orderlineObj = {"ol_number": orderline["ol_number"], "ol_i_id": orderline["ol_i_id"], "ol_delivery_d": orderline["ol_delivery_d"], "ol_amount": orderline["ol_amount"], "ol_supply_w_id": orderline["ol_supply_w_id"], "ol_quantity": orderline["ol_quantity"], "ol_dist_info": orderline["ol_dist_info"]}
	
	db.order.update({"o_w_id": ol_w_id, "o_d_id": ol_d_id, "o_id":ol_o_id}, {"$addToSet":{"o_line":orderlineObj}})

db.drop_collection('orderline')

