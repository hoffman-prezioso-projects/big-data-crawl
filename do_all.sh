#!/bin/sh

if [ $# -lt 1 ]; then
  echo "No warc location provided"
  echo "Use: $0 <path to warc file> [<number of records to process>]"
  exit 0
fi

if [ $# -eq 2 ]; then
  NUM_RECORDS=$2
else
  NUM_RECORDS=0
fi

# run all the needed scripts
./warc_to_text.sh $1 $2
./mapreduce.sh
./load_db.sh output/part-00000

