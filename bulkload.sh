#!/bin/bash

# The following script allows user to retrieve data and transactions
# and load the data into the database by running the following:
# bash bulkload.sh

# Conditions:
#       Project (Team10-mongodb) is in home directory
#	   mongodb is within /temp/mongodb-linux-x86_64-rhel70-3.4.7/bin directory

echo -ne "Loading WAREHOUSE_DISTRICT, ORDER_LINE, STOCK_ITEM, CUSTOMER data\n"

# Bulk load data
cd /temp/mongodb-linux-x86_64-rhel70-3.4.7/bin

# drop database - team10
./mongo team10 --eval "printjson(db.dropDatabase())"

# create collection
./mongoimport -d team10 -c warehouse --type csv --file ~/Team10-mongodb/data-files/warehouse.csv --fields w_id,w_name,w_street_1,w_street_2,w_city,w_state,w_zip,w_tax,w_ytd

./mongoimport -d team10 -c district --type csv --file ~/Team10-mongodb/data-files/district.csv --fields d_w_id,d_id,d_name,d_street_1,d_street_2,d_city,d_state,d_zip,d_tax,d_ytd,d_next_o_id

./mongoimport -d team10 -c customer --type csv --file ~/Team10-mongodb/data-files/customer.csv --fields c_w_id,c_d_id,c_id,c_first,c_middle,c_last,c_street_1,c_street_2,c_city,c_state,c_zip,c_phone,c_since,c_credit,c_credit_lim,c_discount,c_balance,c_ytd_payment,c_payment_cnt,c_delivery_cnt,c_data

./mongoimport -d team10 -c order --type csv --file ~/Team10-mongodb/data-files/order.csv --fields o_w_id,o_d_id,o_id,o_c_id,o_carrier_id,o_ol_cnt,o_all_local,o_entry_d

./mongoimport -d team10 -c orderline --type csv --file ~/Team10-mongodb/data-files/order-line.csv --fields ol_w_id,ol_d_id,ol_o_id,ol_number,ol_i_id,ol_delivery_d,ol_amount,ol_supply_w_id,ol_quantity,ol_dist_info

./mongoimport -d team10 -c item --type csv --file ~/Team10-mongodb/data-files/item.csv --fields i_id,i_name,i_price,i_im_id,i_data

./mongoimport -d team10 -c stock --type csv --file ~/Team10-mongodb/data-files/stock.csv --fields s_w_id,s_i_id,s_quantity,s_ytd,s_order_cnt,s_remote_cnt,s_dist_01,s_dist_02,s_dist_03,s_dist_04,s_dist_05,s_dist_06,s_dist_07,s_dist_08,s_dist_09,s_dist_10,s_data

# Update Table
cd ~/Team10-mongodb/loadData
chmod +x *.py
./loadWarehouseDistrict.py localhost 27017
./loadCustomer.py localhost 27017
./loadStockItem.py localhost 27017
./loadOrder.py localhost 27017

cd /temp/mongodb-linux-x86_64-rhel70-3.4.7/bin
./mongoexport -d team10 -c warehouse_district --type json --out /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/warehouse_district.json
./mongoexport -d team10 -c customer --type json /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/customer.json
./mongoexport -d team10 -c stock_item --type json /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/stock_item.json
./mongoexport -d team10 -c order --type json ./mongoexport -d team10 -c stock_item --type json /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/order.json
