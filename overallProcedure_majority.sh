#!/bin/bash

# The following script allows user to benchmark Cassandra performance
# Enter arguments to select the data to benchmark:
# For 10 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark10.sh
# For 20 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark20.sh
# For 40 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark40.sh

cd /temp/mongodb-linux-x86_64-rhel70-3.4.7/bin

# 10 clients
cd ~/Team10-mongodb
bash bulkload02.sh $1
echo -ne "Executing 10 clients for READ CONCERN - MAJORITY, WRITE CONCERN - MAJORITY .... \n"
bash ~/Team10-mongodb/benchmark/benchmark10.sh majority &> benchmarkResult1002.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log1002
echo -ne "Done... \n"

# 20 clients
cd ~/Team10-mongodb
bash bulkload02.sh $1
echo -ne "Executing 20 clients for READ CONCERN - MAJORITY, WRITE CONCERN - MAJORITY.... \n"
bash ~/Team10-mongodb/benchmark/benchmark20.sh majority &> benchmarkResult2002.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log2002
echo -ne "Done... \n"

# 40 clients
cd ~/Team10-mongodb
bash bulkload02.sh $1
echo -ne "Executing 40 clients for READ CONCERN - MAJORITY, WRITE CONCERN - MAJORITY .... \n"
bash ~/Team10-mongodb/benchmark/benchmark40.sh majority &> benchmarkResult4002.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log4002
echo -ne "Done... \n"

