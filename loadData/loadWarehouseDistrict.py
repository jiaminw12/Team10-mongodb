#!/usr/bin/env python

import sys
import pymongo

from pymongo import MongoClient

client = MongoClient(sys.argv[1], int(sys.argv[2]))
db = client.team10 # Getting a database

# Getting a collection, create indexes
collection = db.warehouse.create_index([('w_id', pymongo.ASCENDING)])

warehouseCollection = db.warehouse
for warehouse in warehouseCollection.find():
	w_id = warehouse["w_id"]
	db.warehouse.update({"w_id": w_id},{"$set":{"w_address":{"w_street_1": warehouse["w_street_1"], "w_street_2": warehouse["w_street_2"], "w_city":warehouse["w_city"], "w_state": warehouse["w_state"], "w_zip":warehouse["w_zip"]}}})

db.warehouse.update({}, {"$unset": {"w_street_1":1}}, multi=True)
db.warehouse.update({}, {"$unset": {"w_street_2":1}}, multi=True)
db.warehouse.update({}, {"$unset": {"w_state":1}}, multi=True)
db.warehouse.update({}, {"$unset": {"w_city":1}}, multi=True)
db.warehouse.update({}, {"$unset": {"w_zip":1}}, multi=True)

# district
districtCollection = db.district
for district in districtCollection.find():
	d_w_id = district["d_w_id"]
	districtObj = {"d_id": district["d_id"], "d_name": district["d_name"], "d_address": {"d_street_1": district["d_street_1"], "d_street_2": district["d_street_2"], "d_city": district["d_city"], "d_state": district["d_state"], "d_zip": district["d_zip"]}, "d_tax": district["d_tax"], "d_ytd": district["d_ytd"], "d_next_o_id": district["d_next_o_id"]}
	
	db.warehouse.update({"w_id": d_w_id}, {"$addToSet":{"district":districtObj}})

warehouseCollection.rename("warehouse_district")
db.drop_collection('district')
