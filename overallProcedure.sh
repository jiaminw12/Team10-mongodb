#!/bin/bash

# The following script allows user to benchmark Cassandra performance
# Enter arguments to select the data to benchmark:
# For 10 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark10.sh arg0
# For 20 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark20.sh arg0
# For 40 clients:
#	bash ~/Team10-mongodb/benchmark/benchmark40.sh arg0

# arg0 can have the following values:
#		arg0: WRITE CONCERN LEVEL
#		1 - set WRITE CONCERN = 1, READ CONCERN = LOCAL
#		majority - set WRITE CONCERN = MAJORITY, READ CONCERN = MAJORITY

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

# Load all data to all tables
bash bulkload.sh $1

# 10 clients
echo -ne "Executing 10 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1 .... \n"
bash ~/Team10-mongodb/benchmark/benchmark10.sh 1 &> benchmarkResult1001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log1001
echo -ne "Done... \n"

# 20 clients
cd ~/Team10-mongodb
bash bulkload02.sh $1
echo -ne "Executing 20 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1.... \n"
bash ~/Team10-mongodb/benchmark/benchmark20.sh 1 &> benchmarkResult2001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log2001
echo -ne "Done... \n"

# 40 clients
cd ~/Team10-mongodb
bash bulkload02.sh $1
echo -ne "Executing 40 clients for READ CONCERN - LOCAL, WRITE CONCERN - 1 .... \n"
bash ~/Team10-mongodb/benchmark/benchmark40.sh 1 &> benchmarkResult4001.log
cp -a ~/Team10-mongodb/log ~/Team10-mongodb/log4001
echo -ne "Done... \n"

