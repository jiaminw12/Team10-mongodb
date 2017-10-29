#!/usr/bin/env python

import pymongo

from pymongo import MongoClient

class Connect(object):

	global client;
	global db;

	def __init__(self, hostname, port):
		self.client = MongoClient(hostname, int(port))
		self.db = self.client.team10 # Getting a database

	def getDBSession(self):
		return self.db;

	def close(self):
		self.client.close();

