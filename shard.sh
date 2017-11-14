#!/bin/bash

cd /temp/mongodb-linux-x86_64-rhel70-3.4.7/bin

echo -ne "\n Beginning sharding process \n"
./mongo --host $1 --port 27017 team10 --eval 'sh.enableSharding("team10")'
./mongo --host $1 --port 27017 team10 --eval 'sh.shardCollection("team10.warehouse_district", {w_id: 1})'
./mongo --host $1 --port 27017 team10 --eval 'sh.shardCollection("team10.customer", { c_w_id: 1, c_d_id: 1, c_id: 1 })'
./mongo --host $1 --port 27017 team10 --eval 'sh.shardCollection("team10.order", { o_w_id: 1, o_d_id: 1, o_id: 1 })'
./mongo --host $1 --port 27017 team10 --eval 'sh.shardCollection("team10.stock_item", { s_w_id: 1, s_i_id: 1})'

echo -ne "\n Starting Balancer \n"

./mongo --host $1 --port 27017 team10 --eval 'sh.startBalancer()'

echo -ne "\n Check chunks \n"

./mongo --host $1 --port 27017 team10 --eval 'sh.status()'

echo -ne "\n End of Sharding \n"
