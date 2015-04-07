#!/bin/sh

if [ $# -ne 1 ]; then
  echo "No data file provided"
	echo "Use: $0 <data filename>"
	exit 0
fi

DATABASE="search.db"
TABLE="data"

echo "Importing database..."

sqlite3 $DATABASE <<EOS

DROP TABLE IF EXISTS $TABLE;
CREATE TABLE $TABLE (word TEXT, url TEXT, frequency INTEGER);

.mode csv
.separator "\t"
.import $1 $TABLE

EOS
