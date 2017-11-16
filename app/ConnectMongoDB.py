#!/usr/bin/env python

import pymongo

from pymongo import MongoClient
from pymongo import read_concern

class Connect(object):

	global client;
	global db;

	def __init__(self, hostname, port, writeConcernLvl):
		if writeConcernLvl == "majority":
			self.client = MongoClient(hostname, int(port), readConcernLevel=writeConcernLvl, w=writeConcernLvl)
		else:
			self.client = MongoClient(hostname, int(port), readConcernLevel=None, w=int(writeConcernLvl))

		self.db = self.client.team10 # Getting a database

	def getDBSession(self):
		return self.db;

	def close(self):
		self.client.close();

