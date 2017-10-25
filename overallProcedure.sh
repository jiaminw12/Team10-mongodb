#!/bin/bash

# The following script allows user to benchmark Cassandra performance
# Enter arguments to select the data to benchmark:
# For 10 clients:
#	bash ~/Team10/benchmark/benchmark10.sh
# For 20 clients:
#	bash ~/Team10/benchmark/benchmark20.sh
# For 40 clients:
#	bash ~/Team10/benchmark/benchmark40.sh

declare -r DATA_FOLDER="data-files"
declare -r XACT_FOLDER="xact-files"

cd ~/Team10

echo -ne "Checking whether data and xact folder exist...\n"
if [ -d $DATA_FOLDER ];
then
	echo -ne "yes \n"
else
	echo -ne "Downloading 4224-project-files...\n"
	wget http://www.comp.nus.edu.sg/~cs4224/4224-project-files.zip
	unzip 4224-project-files.zip

	cd 4224-project-files
	mv data-files ~/Team10/
	mv xact-files ~/Team10/
	cd ..
	rm -Rf 4224-project-files
	rm -Rf 4224-project-files.zip
	echo -ne "Done...\n"

fi

# Load all data to all tables
bash bulkload.sh
