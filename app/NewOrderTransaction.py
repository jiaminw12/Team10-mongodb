#! /usr/bin/env python

from decimal import *
from datetime import datetime

class NewOrderTransaction(object):

	def __init__(self, session, w_id, d_id, c_id, num_items, i_id_list, supplier_w_id_list, quantity_list):
		self.session = session;
		self.w_id = w_id;
		self.d_id = d_id;
		self.c_id = c_id;
		self.num_items = num_items;
		self.i_id_list = i_id_list;
		self.supplier_w_id_list = supplier_w_id_list;
		self.quantity_list = quantity_list;
		
		print("wid=%d, did=%d, cid=%d\n" %(w_id, d_id, c_id));
		self.getCollections();
	
	def getCollections(self):
		self.warehouse_district = self.session.warehouse_district;
		self.customer = self.session.customer;
		self.stockitem = self.session.stock_item;
		self.order = self.session.order

	def getWarehouseInformation(self):
		warehouseDistrictRowAggregate = [{"$unwind":"$district"},{"$match":{"w_id":self.w_id, "district.d_id":self.d_id}}, {"$project":{"w_tax":1, "district.d_next_o_id":1, "district.d_tax":1}}];
		result = list(self.warehouse_district.aggregate(warehouseDistrictRowAggregate))
		self.w_tax = result[0]["w_tax"];
		self.d_next_o_id = result[0]["district"]["d_next_o_id"];
		self.d_tax = result[0]["district"]["d_tax"];
		print("W_TAX = %s, D_TAX = %s, D_NEXT_O_ID = %s" %(self.w_tax, self.d_tax, self.d_next_o_id));
		

	def updateNextOID(self):
		self.d_next_o_id = self.d_next_o_id + 1;
		result = self.warehouse_district.update({"w_id":self.w_id, "district.d_id":self.d_id}, {"$set":{"district.$.d_next_o_id":self.d_next_o_id}})
		print("Updated next o id to %d" %(self.d_next_o_id));



	def getCustomerInformation(self):
		result = self.customer.find({"c_w_id":self.w_id, "c_d_id":self.d_id, "c_id":self.c_id})	
		self.c_last = result[0]["c_last"];
		self.c_credit = result[0]["c_credit"];
		self.c_discount = result[0]["c_discount"];
		print("C_LAST = %s, C_CREDIT = %s, C_DISCOUNT = %s" %(self.c_last, self.c_credit, self.c_discount));			



	def getAllItemInformation(self):		
		print("ASDSADSAD");
		self.i_price_list = [0] * self.num_items;
		self.i_name_list = [0] * self.num_items;
		self.s_quantity_list = [0] * self.num_items;
		self.itemamt_list = [0] * self.num_items;
		
		print("NUM ITEMS: %d" %(self.num_items));
		for i in range(0, self.num_items):
			print("Stockinfo for w_id:%d, i_id:%d" % (self.supplier_w_id_list[i], self.i_id_list[i]));
			rows = list(self.stockitem.find({"s_w_id":self.supplier_w_id_list[i], "s_i_id":self.i_id_list[i]}));
			self.i_price_list[i] = rows[0]["i_price"];
			self.i_name_list[i] = rows[0]["i_name"];
			self.s_quantity_list[i] = rows[0]["s_quantity"];
			print("PRICE = %d, NAME = %s, S_QTY = %d" %(self.i_price_list[i], self.i_name_list[i], self.s_quantity_list[i]));

	def updateStockItem(self, ytd, _remotecnt, wid, iid, s_qty):
		rows = list(self.stockitem.find({"s_w_id":wid, "s_i_id":iid}));
		
		if rows:
			s_ytd = rows[0]["s_ytd"] + ytd;
			ordercnt = rows[0]["s_order_cnt"] + 1;
			remotecnt = rows[0]["s_remote_cnt"] + _remotecnt;
			self.stockitem.update({"s_w_id":wid, "s_i_id":iid}, {"$set":{"s_ytd":s_ytd, "s_quantity":s_qty, "s_order_cnt":ordercnt, "s_remote_cnt":remotecnt}})

	

	def insertNewOrderLine(self):
		#Fill in Order data
		self.o_id = self.d_next_o_id;
		self.o_d_id = self.d_id;
		self.o_w_id = self.w_id;
		self.o_c_id = self.c_id;
		self.o_entry_d = int(float(datetime.now().strftime("%s.%f"))) * 1000 #strftime("%Y-%m-%d %H:%M:%S", gmtime()); #Not sure format
		self.o_carrier_id = None;
		self.o_ol_cnt = self.num_items;
		self.o_all_local = int(all(x == self.o_w_id for x in self.supplier_w_id_list));

		newOrder = {"o_w_id":self.o_w_id, "o_d_id":self.o_d_id, "o_id":self.o_id, "o_c_id":self.o_c_id, "o_carrier_id":self.o_carrier_id, "o_ol_cnt":self.o_ol_cnt, "o_all_local":self.o_all_local, "o_entry_d":self.o_entry_d, "o_line":[]};

		self.total_amt = 0;

		for i in range(0, self.num_items):
			adjusted_qty = self.s_quantity_list[i] - self.quantity_list[i];
			adjusted_qty = adjusted_qty if adjusted_qty >= 10 else (adjusted_qty+100);
			
			if self.supplier_w_id_list[i] != self.w_id:
				remotecnt = 1;
			else:
				remotecnt = 0;

			self.updateStockItem(self.quantity_list[i], remotecnt, adjusted_qty, self.supplier_w_id_list[i], self.i_id_list[i]);
			itemamt = self.quantity_list[i] * self.i_price_list[i]
			self.itemamt_list[i] = itemamt;
			self.total_amt += itemamt
			self.total_amt = self.total_amt * (1+self.d_tax + self.w_tax)* (1-self.c_discount)
			self.ol_number = i;
			self.ol_amount = itemamt 
			self.ol_dist_info = "S_DIST_" + str(self.d_id)
			self.ol_i_id = self.i_id_list[i];
			self.ol_quantity = self.quantity_list[i]
			self.ol_supply_w_id = self.supplier_w_id_list[i]
			newOrder["o_line"].append({"ol_amount":self.ol_amount, "ol_deliver_d":datetime.now(), "ol_number":self.ol_number, "ol_dist_info":self.ol_dist_info, "ol_i_id":self.ol_i_id, "ol_supply_w_id":self.ol_supply_w_id, "ol_quantity":self.ol_quantity}); 

		self.order.insert(newOrder);		



	
	def printOutput(self):
		print("Customer ID(%d,%d,%d), Lastname:%s, Credit:%s, Discount:%.4f" %(self.w_id,self.d_id, self.c_id, self.c_last, self.c_credit, self.c_discount));
	
		print("Warehouse Tax:%.4f, Disctrict Tax:%.4f" %(self.w_tax, self.d_tax));

		print("Order Num: %d, Entry Date: %s" %(self.o_id, self.o_entry_d));

		print("Number of items:%d, Total amount:%.4f" %(self.num_items, self.total_amt));
		
		for i in range(0, self.num_items):
			print("Item Num:%d, Name:%s, Supplier Warehouse:%d, Quantity:%d, OL Amount: %.4f, S_Quantity:%d"%(self.i_id_list[i], self.i_name_list[i], self.supplier_w_id_list[i], self.quantity_list[i], self.itemamt_list[i], self.s_quantity_list[i]));


	def process(self):
		self.getWarehouseInformation();
		self.updateNextOID();
		self.getCustomerInformation();
		self.getAllItemInformation();
		self.insertNewOrderLine();
		self.printOutput();


	









