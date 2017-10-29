use team10
db.warehouse_district.createIndex({w_id:1})
db.customer.createIndex({c_w_id:1, c_d_id:1, c_id:1})
db.order.createIndex({o_c_id:1})
db.order.createIndex({o_carrier_id:1})
db.order.createIndex({o_w_id:1, o_d_id:1, o_id:1})
db.stock_item.createIndex({s_w_id:1, s_i_id:1})
