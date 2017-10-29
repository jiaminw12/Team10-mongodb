#!/usr/bin/env python

import sys
import time
from decimal import *
from ConnectMongoDB import Connect
from NewOrderTransaction import NewOrderTransaction
from PaymentTransaction import PaymentTransaction
from DeliveryTransaction import DeliveryTransaction
from OrderStatusTransaction import OrderStatusTransaction
from StockLevelTransaction import StockLevelTransaction
from PopularItemTransaction import PopularItemTransaction
from TopBalanceTransaction import TopBalanceTransaction

# function - read file
def getdata(filename):
	with open(filename) as f:
		content = f.read()
		yield content

# New Order Transaction
def newOrder(w_id, d_id, c_id, newOrderList):
	
	print("\n-------- New Order Transaction --------")	
	num_items = len(newOrderList);
	i_id_list = [];
	supplier_w_id_list = [];
	quantity_list = [];

	for strOrder in newOrderList:
		orderArray = strOrder.split(',');
		i_id_list.append(int(orderArray[0]));
		supplier_w_id_list.append(int(orderArray[1]));
		quantity_list.append(int(orderArray[2]));

	newOrderTransaction = NewOrderTransaction(dbSession, w_id, d_id, c_id, num_items, i_id_list, supplier_w_id_list, quantity_list);
	newOrderTransaction.process();

# Payment Transaction
def payment(c_w_id, c_d_id, c_id, paymentAmt):
	print("\n-------- Payment Transaction --------")
	paymentTransaction = PaymentTransaction(dbSession, c_w_id, c_d_id, c_id, paymentAmt)
	paymentTransaction.process()

# Delivery Transaction
def delivery(w_id, carrier_id):
	print("\n-------- Delivery Transaction --------")
	deliveryTransaction = DeliveryTransaction(dbSession, w_id, carrier_id)
	deliveryTransaction.process()

# Order-Status Transaction
def orderStatus(c_w_id, c_d_id, c_id):
	print("\n-------- Order-Status Transaction --------")
	orderStatusTransaction = OrderStatusTransaction(dbSession, c_w_id, c_d_id, c_id)
	orderStatusTransaction.process()

# Stock-Level Transaction
def stockLevel( w_id, d_id, stockThreshold, numLastOrder):
	print("\n-------- Stock-Level Transaction --------")
	stockLevelTransaction = StockLevelTransaction(dbSession, w_id, d_id, stockThreshold, numLastOrder)
	stockLevelTransaction.process()

# Popular-Item
def popularItem(w_id, d_id, numLastOrder):
	print("\n-------- Popular Item Transaction --------")
	popularItemTransaction = PopularItemTransaction(dbSession, w_id, d_id, numLastOrder)
	popularItemTransaction.process()

# Top-Balance
def topBalance():
	print("\n-------- Top Balance Transaction --------")
	topBalanceTransaction = TopBalanceTransaction(dbSession)
	topBalanceTransaction.process()


numOfExceutedTransaction = 0

newOrderXact = 'N'
paymentXact = 'P'
deliveryXact = 'D'
orderStatusXact = 'O'
stockLevelXact = 'S'
popularItemXact = 'I'
topBalanceXact = 'T'

# Connect Keyspace
connect = Connect(sys.argv[2], sys.argv[3])
dbSession = connect.getDBSession()

filePath = '../xact-files/%s' % sys.argv[1];
start_time = time.time()
with open(filePath, 'r+') as myFile:
	lines = myFile.readlines()

	for i in range(0, len(lines)):
		numOfExceutedTransaction += 1
		line = lines[i]
		str = line.split(',')

		if str[0] == newOrderXact:
			c_id = int(str[1]);
			w_id = int(str[2]);
			d_id = int(str[3]);
			needToRead = int(str[4]) #Num of lines needed to read

			newOrderList = []
			for j in range(0, needToRead):
				newOrderList.append(lines[i+j+1]);

			newOrder(w_id, d_id, c_id, newOrderList);
		
		elif str[0] == paymentXact:
			c_w_id = str[1];
			c_d_id = str[2];
			c_id = str[3];
			paymentAmt = Decimal(str[4]);

			payment(c_w_id, c_d_id, c_id, paymentAmt);

		elif str[0] == deliveryXact:
			w_id = str[1];
			carrier_id = str[2];

			delivery(w_id, carrier_id);

		elif str[0] == orderStatusXact:
			c_w_id = str[1];
			c_d_id = str[2];
			c_id = str[3];

			orderStatus(c_w_id, c_d_id, c_id);

		elif str[0] == stockLevelXact:
			w_id = str[1];
			d_id = str[2];
			threshold = str[3];
			numLastOrders = str[4];

			stockLevel(w_id, d_id, threshold, numLastOrders);

		elif str[0] == popularItemXact:
			w_id = str[1];
			d_id = str[2];
			numLastOrders = str[3];
			popularItem(w_id, d_id, numLastOrders)

		elif str[0] == topBalanceXact:
			topBalance()

connect.close()
finalExecutionTime = (time.time() - start_time)
# Each client
print "\n--- %s seconds ---" % (finalExecutionTime)
print "--- Number of executed transactions: %d" % (numOfExceutedTransaction)
throughput = finalExecutionTime / numOfExceutedTransaction
print "--- Transaction Throughput: %f" % (throughput)

with open("throughput.txt", "a") as myfile:
	myfile.write("%f" % throughput)
	myfile.write('\n')
