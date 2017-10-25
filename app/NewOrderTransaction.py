#!/usr/bin/env python

import pymongo

from time import gmtime, strftime
from datetime import datetime

class NewOrderTransaction():

	def __init__(self, session, w_id, d_id, c_id, num_items, i_id_list, supplier_w_id_list, quantity_list):
		self.session = session
		self.w_id = w_id
		self.d_id = d_id
		self.c_id = c_id
		self.num_items = num_items
		self.i_id_list = i_id_list
		self.supplier_w_id_list = supplier_w_id_list
		self.quantity_list = quantity_list

		self.initPreparedStmts()

	def initPreparedStmts(self):

		self.update_stockitem = self.session.prepare("UPDATE stockitem set s_ytd = ?, s_order_cnt = ?, s_remote_cnt = ?, s_quantity = ?  where s_w_id = ? and s_i_id = ?");

		self.select_cnt_stockitem = self.session.prepare("SELECT s_order_cnt, s_remote_cnt from stockitem where s_w_id = ? and s_i_id = ?")

		self.select_next_oid_district = self.session.prepare("SELECT d_next_o_id FROM district where d_w_id = ? AND d_id = ?");

		self.update_next_oid_district = self.session.prepare("UPDATE district SET d_next_o_id = ? where d_w_id = ? AND d_id = ?");

		self.select_item_info = self.session.prepare("SELECT i_price, i_name, s_quantity FROM stockitem where s_w_id = ? AND s_i_id = ?");

		self.select_tax = self.session.prepare("SELECT w_tax,d_tax from item_by_warehouse_district where w_id = ? and d_id = ?");

		self.select_customer_info = self.session.prepare("SELECT c_last, c_credit, c_discount from payment_by_customer where c_w_id = ? and c_d_id = ? and c_id = ?");

		self.insert_order_desc = self.session.prepare("INSERT INTO order_by_desc (o_w_id, o_d_id, o_id, o_c_id, o_carrier_id, o_ol_cnt, o_all_local, o_entry_d) VALUES(?,?,?,?,?,?,?,?)")

		self.insert_order_asc = self.session.prepare("INSERT INTO order_by_asc (o_w_id, o_d_id, o_id, o_c_id, o_carrier_id, o_ol_cnt, o_all_local, o_entry_d) VALUES (?,?,?,?,?,?,?,?)")

		self.insert_orderline = self.session.prepare("INSERT INTO orderline (ol_w_id, ol_d_id, ol_o_id, ol_number, ol_i_id, ol_delivery_d, ol_amount, ol_supply_w_id, ol_quantity, ol_dist_info) VALUES (?,?,?,?,?,?,?,?,?,?)");

	def process(self):
		self.updateNextOrderId();
		self.getTaxInformation();
		self.getCustomerInformation();
		self.getAllItemInformation();
		self.insertNewOrderLine();
		self.printOutput();

	def printOutput(self):
		print("Customer ID(%d,%d,%d), Lastname:%s, Credit:%s, Discount:%.4f" %(self.w_id,self.d_id, self.c_id, self.c_last, self.c_credit, self.c_discount));
	
		print("Warehouse Tax:%.4f, Disctrict Tax:%.4f" %(self.w_tax, self.d_tax));

		print("Order Num: %d, Entry Date: %s" %(self.o_id, self.o_entry_d));

		print("Number of items:%d, Total amount:%.4f" %(self.num_items, self.total_amt));
		
		for i in range(0, self.num_items):
			print("Item Num:%d, Name:%s, Supplier Warehouse:%d, Quantity:%d, OL Amount: %.4f, S_Quantity:%d"%(self.i_id_list[i], self.i_name_list[i], self.supplier_w_id_list[i], self.quantity_list[i], self.itemamt_list[i], self.s_quantity_list[i]));

													 
	def getCustomerInformation(self):
		rows = self.session.execute(self.select_customer_info, (self.w_id, self.d_id, self.c_id));		
		self.c_last = rows[0].c_last;
		self.c_credit = rows[0].c_credit;
		self.c_discount = rows[0].c_discount;

													 
	# Increment d_next_o_id by 1 in table DISTRICT and ITEM_BY_WAREHOUSE_DISTRICT
	def updateNextOrderId(self):
		rows = self.session.execute(self.select_next_oid_district, (self.w_id, self.d_id));
		self.d_next_o_id = int(rows[0].d_next_o_id) + 1;
		self.session.execute(self.update_next_oid_district, (self.d_next_o_id, self.w_id, self.d_id));
	
													 
	def getTaxInformation(self):
		rows = self.session.execute(self.select_tax, (self.w_id, self.d_id));
		self.w_tax = rows[0].w_tax;
		self.d_tax = rows[0].d_tax;

	
	def getAllItemInformation(self):		
		self.i_price_list = [0] * self.num_items;
		self.i_name_list = [0] * self.num_items;
		self.s_quantity_list = [0] * self.num_items;
		self.itemamt_list = [0] * self.num_items;
		
		for i in range(0, self.num_items):
			rows = self.session.execute(self.select_item_info, (self.supplier_w_id_list[i], self.i_id_list[i]));
			self.i_price_list[i] = rows[0][0];
			self.i_name_list[i] = rows[0][1];
			self.s_quantity_list[i] = rows[0][2];

													 
	def updateStockItem(self, ytd, _remotecnt, wid, iid, s_qty):
		rows = self.session.execute(self.select_cnt_stockitem, (wid, iid));
		if rows:
			ordercnt = rows[0].s_order_cnt;
			remotecnt = rows[0].s_remote_cnt;
			self.session.execute(self.update_stockitem,(ytd, ordercnt, remotecnt+_remotecnt, s_qty, wid, iid));

													 
	def insertCustomerByDelivery(self, ol_number, ol_amount, ol_i_id, ol_quantity, ol_supply_w_id):
		self.session.execute(self.insert_delivery_by_customer, (self.w_id, self.d_id, self.o_id, ol_number, self.c_id, self.o_carrier_id, self.o_entry_d, ol_amount, None, ol_i_id, ol_quantity, ol_supply_w_id));
		
													 
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

		self.total_amt = 0;
													 
		self.session.execute(self.insert_order_desc, (self.o_w_id, self.o_d_id, self.o_id, self.o_c_id, self.o_carrier_id, self.o_ol_cnt, self.o_all_local, self.o_entry_d));
													 
		self.session.execute(self.insert_order_asc, (self.o_w_id, self.o_d_id, self.o_id, self.o_c_id, self.o_carrier_id, self.o_ol_cnt, self.o_all_local, self.o_entry_d));

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
													 
			self.session.execute(self.insert_orderline, (self.o_w_id, self.o_d_id, self.o_id, self.ol_number, self.ol_i_id, None, self.ol_amount, self.ol_supply_w_id, self.ol_quantity, self.ol_dist_info))
