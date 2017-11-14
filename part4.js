use team10

print ("1. SELECT sum(W_YTD) FROM team10.warehouse_district ... ")
db.warehouse_district.aggregate([ { $group: { _id: null, total: {$sum: "$w_ytd"}}} ])

print ("2. SELECT sum(D_YTD), sum(D_NEXT_O_ID) FROM team10.warehouse_district ... ")
db.warehouse_district.aggregate([ { $group: { _id: null, total: {$sum: "$district.$d_ytd"}}} ])

print ("3. SELECT sum(C_BALANCE), sum(C_YTD_PAYMENT), sum(C_PAYMENT_CNT), sum(C_DELIVERY_CNT) FROM team10.customer ... ")
db.customer.aggregate([ { $group: { _id: null, total: {$sum: "$c_balance"}}} ])
db.customer.aggregate([ { $group: { _id: null, total: {$sum: "$c_ytd_payment"}}} ])
db.customer.aggregate([ { $group: { _id: null, total: {$sum: "$c_payment_cnt"}}} ])

print ("4. SELECT max(O_ID), sum(O_OL_CNT) FROM team10.order ... ")
db.order.aggregate([ { $group: { _id: null, total: {$sum: "$o_id"}}} ])
db.order.aggregate([ { $group: { _id: null, total: {$sum: "$o_ol_cnt"}}} ])

print ("5. SELECT sum(OL_AMOUNT), sum(OL_QUANTITY) FROM team10.order ... ")
db.order.aggregate([ { $group: { _id: null, total: {$sum: "$ol_amount"}}} ])
db.order.aggregate([ { $group: { _id: null, total: {$sum: "$ol_quantity"}}} ])

print ("6. SELECT sum(S_QUANTITY), sum(S_YTD), sum(S_ORDER_CNT), sum(S_REMOTE_CNT) FROM team10.stock_item ... ")
db.stock_item.aggregate([ { $group: { _id: null, total: {$sum: "$s_quantity"}}} ])
db.stock_item.aggregate([ { $group: { _id: null, total: {$sum: "$s_ytd"}}} ])
db.stock_item.aggregate([ { $group: { _id: null, total: {$sum: "$s_order_cnt"}}} ])
db.stock_item.aggregate([ { $group: { _id: null, total: {$sum: "$s_remote_cnt"}}} ])
