#!/bin/bash

# The following script allows user to benchmark Cassandra performance
# Enter arguments to select the data to benchmark:
# For 10 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark10.sh
# For 20 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark20.sh
# For 40 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark40.sh

# 10 clients
bash bulkload02.sh $1
echo -ne "Executing 10 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1 .... \n"
bash ~/Team10-mongodb/benchmark/benchmark10.sh majority &> benchmarkResult1001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log1001
echo -ne "Done... \n"

# 20 clients
bash bulkload02.sh $1
cd ~/Team10-mongodb
echo -ne "Executing 20 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1.... \n"
bash ~/Team10-mongodb/benchmark/benchmark20.sh majority &> benchmarkResult2001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log2001
echo -ne "Done... \n"

# 40 clients
bash bulkload02.sh $1
cd ~/Team10-mongodb
echo -ne "Executing 40 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1 .... \n"
bash ~/Team10-mongodb/benchmark/benchmark40.sh majority &> benchmarkResult4001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log4001
echo -ne "Done... \n"

