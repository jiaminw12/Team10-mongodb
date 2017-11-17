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
./mongo < ~/Team10-mongodb/mongo_drop_database.js

# create collection
./mongoimport -d team10 -c warehouse_district --type json --file /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/warehouse_district.json

./mongoimport -d team10 -c customer --type json --file /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/customer.json

./mongoimport -d team10 -c stock_item --type json --file /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/stock_item.json

./mongoimport -d team10 -c order --type json --file /temp/mongodb-linux-x86_64-rhel70-3.4.7/json/order.json

./mongo < ~/Team10-mongodb/mongo_create_index_after_build.js
