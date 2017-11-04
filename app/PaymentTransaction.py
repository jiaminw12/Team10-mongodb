#!/usr/bin/env python

import pymongo
import decimal

class PaymentTransaction(object):

        def __init__(self, session, c_w_id, c_d_id, c_id, payment):
                self.session = session
                self.c_w_id = int(c_w_id)
                self.c_d_id = int(c_d_id)
                self.c_id = int(c_id)
                self.payment = payment

        def process(self):
                warehouseCollection = self.session.warehouse_district
                customerCollection = self.session.customer
                # update warehouse District
                warehouseDistrictRow = [{"$unwind":"$district"},{"$match":{"w_id":self.c_w_id, "district.d_id":self.c_d_id}}]
                warehouseCollection.update({"w_id":self.c_w_id, "district.d_id":self.c_d_id}, {"$set":{"w_ytd": float(self.payment), "district.$.d_ytd":float(self.payment)}})
                selected_warehouse_district = list(warehouseCollection.aggregate(warehouseDistrictRow))[0]
                # update customer
                selected_customer = customerCollection.find_one({"c_w_id":self.c_w_id,"c_d_id":self.c_d_id,"c_id":self.c_id})
                c_balance_to_update = selected_customer["c_balance"] - float(self.payment)
                c_ytd_payment_to_update = selected_customer["c_ytd_payment"] + float(self.payment)
                c_payment_cnt_to_update = selected_customer["c_payment_cnt"] + 1
                customerCollection.update({"c_w_id":self.c_w_id, "c_d_id":self.c_d_id,"c_id": self.c_id},{"$set":{"c_balance":float(c_balance_to_update),"c_ytd_payment":float(c_ytd_payment_to_update),"c_payment_cnt": c_payment_cnt_to_update}})
                #retrieve output
                print ("customer identifier: %d, %d, %d name: %s, %s, %s address %s, %s, %s, %s, %s phone %s since %s credit %s credit_lim %s c_discount %s c_balance %s" % (self.c_w_id, self.c_d_id, self.c_id, selected_customer["c_first"], selected_customer["c_middle"], selected_customer["c_last"], selected_customer["c_address"]["c_street_1"],selected_customer["c_address"]["c_street_2"], selected_customer["c_address"]["c_city"], selected_customer["c_address"]["c_state"], selected_customer["c_address"]["c_zip"], selected_customer["c_phone"], selected_customer["c_since"], selected_customer["c_credit"],selected_customer["c_credit_lim"], selected_customer["c_discount"], c_balance_to_update))
                print ("warehouse address: %s, %s, %s, %s, %s" % (selected_warehouse_district["w_address"]["w_street_1"], selected_warehouse_district["w_address"]["w_street_2"], selected_warehouse_district["w_address"]["w_city"], selected_warehouse_district["w_address"]["w_state"], selected_warehouse_district["w_address"]["w_zip"]))
                print ("district address: %s, %s, %s, %s, %s" % (selected_warehouse_district["district"]["d_address"]["d_street_1"], selected_warehouse_district["district"]["d_address"]["d_street_2"], selected_warehouse_district["district"]["d_address"]["d_city"], selected_warehouse_district["district"]["d_address"]["d_state"], selected_warehouse_district["district"]["d_address"]["d_zip"]))
                print ("payment amount: %.2f\n" % float(self.payment))
