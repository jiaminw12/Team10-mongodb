#!/usr/bin/env python

import sys
import pymongo

from pymongo import MongoClient

client = MongoClient(sys.argv[1], int(sys.argv[2]))
db = client.team10 # Getting a database

warehouseCollection = db.warehouse_district
districtCollection = db.district
customerCollection = db.customer
for customer in customerCollection.find():
	db.customer.update({"c_w_id": customer["c_w_id"], "c_d_id": customer["c_d_id"], "c_id": customer["c_id"]},{"$set":{"c_address":{"c_street_1": customer["c_street_1"], "c_street_2": customer["c_street_2"], "c_city":customer["c_city"], "c_state": customer["c_state"], "c_zip":customer["c_zip"]}}})

	# Insert w_name, d_name
	warehouseName = warehouseCollection.find_one({"w_id": customer["c_w_id"]})
	warehouseDistrictRow = [{"$match": {"w_id": customer["c_w_id"]}}, {"$project": {"district": {"$filter": {"input": "$district", "as": "district", "cond": {"$eq": ["$$district.d_id", customer["c_d_id"]]}}}, "_id": 0}}]
	result = list(warehouseCollection.aggregate(warehouseDistrictRow))
	db.customer.update({"c_w_id": customer["c_w_id"], "c_d_id": customer["c_d_id"]},{"$set":{"w_name": warehouseName["w_name"], "d_name":result[0]["district"][0]["d_name"]}})

db.customer.update({}, {"$unset": {"c__street_1":1}}, multi=True)
db.customer.update({}, {"$unset": {"c__street_2":1}}, multi=True)
db.customer.update({}, {"$unset": {"c_state":1}}, multi=True)
db.customer.update({}, {"$unset": {"c__city":1}}, multi=True)
db.customer.update({}, {"$unset": {"c_zip":1}}, multi=True)


