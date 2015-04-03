#!/bin/sh

if [ $# -lt 1 ]; then
	echo "No warc location provided"
	echo "Use: $0 <path to warc file> [<number of records to read>]"
	exit 0
fi

if [ $# -eq 2 ]; then
	NUM_RECORDS=$2
else
	NUM_RECORDS=0
fi

echo "Creating data directory"
DATA_FILE="data"

if [ ! -d $DATA_FILE ]; then
	mkdir $DATA_FILE
fi

echo "Converting warc records to text files"
./src/warc_to_text.py $1 $DATA_FILE $NUM_RECORDS
