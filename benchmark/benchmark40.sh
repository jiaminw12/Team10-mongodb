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

# Run app
IFS=$'\n' read -d '' -r -a lines < nodeList.txt

rm -rf log
mkdir log
cd ~/Team10-mongodb/app
chmod +x *.py
echo -ne "Running Performance Measurement now ... \n"
let "CONCERNLEVEL = $1"

echo -ne "Execute 40 clients ...\n"

for i in 5 10 15 20 25 30 35 40; do
	echo -ne "./MainApp.py $i.txt ... \n"
	./MainApp.py "$i".txt "${lines[0]}" 27017 "$CONCERNLEVEL" 1> ~/Team10-mongodb/log/output$i.log 2> ~/Team10-mongodb/log/error$i.log &
done

for i in 1 6 11 16 21 26 31 36; do
	echo -ne "./MainApp.py $i.txt ... \n"
	./MainApp.py "$i".txt "${lines[1]}" 27017 "$CONCERNLEVEL" 1> ~/Team10-mongodb/log/output$i.log 2> ~/Team10-mongodb/log/error$i.log &
done

for i in 2 7 12 17 22 27 32 37; do
	echo -ne "./MainApp.py $i.txt ... \n"
	./MainApp.py "$i".txt "${lines[2]}" 27017 "$CONCERNLEVEL" 1> ~/Team10-mongodb/log/output$i.log 2> ~/Team10-mongodb/log/error$i.log &
done

for i in 3 8 13 18 23 28 33 38; do
	echo -ne "./MainApp.py $i.txt ... \n"
	./MainApp.py "$i".txt "${lines[3]}" 27017 "$CONCERNLEVEL" 1> ~/Team10-mongodb/log/output$i.log 2> ~/Team10-mongodb/log/error$i.log &
done

for i in 4 9 14 19 24 29 34 39; do
	echo -ne "./MainApp.py $i.txt ... \n"
	./MainApp.py "$i".txt "${lines[4]}" 27017 "$CONCERNLEVEL" 1> ~/Team10-mongodb/log/output$i.log 2> ~/Team10-mongodb/log/error$i.log &
done
wait

./computeMinMaxAvgXactNCClients.py

rm ~/Team10-mongodb/app/throughput.txt

# Part 4
cd /temp/mongodb-linux-x86_64-rhel70-3.4.7/bin
./mongo < ~/Team10-mongodb/part4.js

exit
