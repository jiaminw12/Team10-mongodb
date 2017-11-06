#!/usr/bin/env python

import sys
import pymongo

from pymongo import MongoClient

client = MongoClient(sys.argv[1], int(sys.argv[2]))
db = client.team10 # Getting a database

itemCollection = db.item
for item in itemCollection.find():
	i_id = item["i_id"]
	db.stock.update_many({"s_i_id": i_id}, {"$set": {"i_name": item["i_name"], "i_price":item["i_price"], "i_im_id":item["i_im_id"], "i_data":item["i_data"]}})

stockCollection = db.stock
stockCollection.rename("stock_item")
db.drop_collection('item')

