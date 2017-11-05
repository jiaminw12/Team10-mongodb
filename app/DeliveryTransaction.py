#!/usr/bin/env python

import pymongo
import decimal

from datetime import datetime

class DeliveryTransaction(object):
        def __init__(self, session, w_id, carrier_id):
                self.session = session
                self.w_id = int(w_id)
                self.carrier_id = int(carrier_id)

        def process(self):
                for district_no in range(1, 11):
                        self.get_next_order_and_customer(district_no)

        def get_next_order_and_customer(self, district_no):
                customerCollection = self.session.customer
                orderCollection = self.session.order
                min_order = list(orderCollection.find({“o_w_id":self.w_id, "o_d_id":district_no, "o_carrier_id": 0}).sort([("o_id", 1)]).limit(1))
                if min_order:
                        order_id = min_order[0][“o_id"]
                        customer = min_order[0]["o_c_id"]
                        # Update carrier id
                        orderCollection.update({"o_w_id":self.w_id, "o_d_id":district_no, "o_id": order_id}, {"$set": {"o_carrier_id":self.carrier_id}})
                        ol_amount = 0.00
                        for ol_in_order in min_order[0]["o_line"]:
                                ol_amount = ol_amount + float(ol_in_order["ol_amount"])
                                orderCollection.update({"o_w_id":self.w_id, "o_d_id":district_no, "o_id": order_id, "o_line.ol_number":ol_in_order["ol_number"]}, {"$set": {"ol_delivery_d":datetime.now()}})
                        selected_customer = customerCollection.find_one({"c_w_id":self.w_id,"c_d_id":district_no,"c_id":customer})
                        c_balance_to_update = selected_customer["c_balance"] + float(ol_amount)
                        c_delivery_cnt_to_update = selected_customer["c_delivery_cnt"] + 1
                        customerCollection.update({"c_w_id":self.w_id, "c_d_id":district_no,"c_id": customer},{"$set":{"c_balance":float(c_balance_to_update), "c_delivery_cnt": c_delivery_cnt_to_update}})

