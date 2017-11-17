#!/bin/bash

# The following script allows user to benchmark Cassandra performance
# Enter arguments to select the data to benchmark:
# For 10 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark10.sh
# For 20 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark20.sh
# For 40 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark40.sh

declare -r DATA_FOLDER="data-files"
declare -r XACT_FOLDER="xact-files"

cd ~/Team10-mongodb

echo -ne "Checking whether data and xact folder exist...\n"
if [ -d $DATA_FOLDER ];
then
	echo -ne "yes \n"
else
	echo -ne "Downloading 4224-project-files...\n"
	wget http://www.comp.nus.edu.sg/~cs4224/4224-project-files.zip
	unzip 4224-project-files.zip

	cd 4224-project-files
	mv data-files ~/Team10-mongodb/
	mv xact-files ~/Team10-mongodb/
	cd ..
	rm -Rf 4224-project-files
	rm -Rf 4224-project-files.zip
	echo -ne "Done...\n"

fi

# 10 clients
cd ~/Team10-mongodb
bash bulkload03.sh $1
echo -ne "Executing 10 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1 .... \n"
bash ~/Team10-mongodb/benchmark/benchmark10.sh 1 &> benchmarkResultNoShard1001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/NoShardlog1001
echo -ne "Done... \n"

# 20 clients
cd ~/Team10-mongodb
bash bulkload03.sh $1
echo -ne "Executing 20 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1.... \n"
bash ~/Team10-mongodb/benchmark/benchmark20.sh 1 &> benchmarkResultNoShard2001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/NoShardlog2001
echo -ne "Done... \n"

# 40 clients
cd ~/Team10-mongodb
bash bulkload03.sh $1
echo -ne "Executing 40 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1 .... \n"
bash ~/Team10-mongodb/benchmark/benchmark40.sh 1 &> benchmarkResultNoShard4001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/NoShardlog4001
echo -ne "Done... \n"

