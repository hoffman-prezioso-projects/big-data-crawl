OUTPUT_DIR="output"

echo "Creating crawl directory..."
hadoop fs -mkdir crawl > /dev/null 2>&1

echo "Creating data directory..."
hadoop fs -mkdir crawl/data > /dev/null 2>&1
hadoop fs -rm crawl/data/* > /dev/null 2>&1

echo "Removing previous output..."
hadoop fs -rm -r crawl/$OUTPUT_DIR > /dev/null 2>&1

echo "Copying data..."
hadoop dfs -copyFromLocal data crawl > /dev/null 2>&1

echo "Running mapReduce..."
hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar \
-file src/mapper.py \
-mapper src/mapper.py \
-file src/reducer.py \
-reducer src/reducer.py \
-input crawl/data/* \
-output crawl/$OUTPUT_DIR

# create local output directory
if [ ! -d $OUTPUT_DIR ]; then
	mkdir $OUTPUT_DIR
else
	rm -f $OUTPUT_DIR/*
fi

echo "Creating output directory"
hadoop dfs -copyToLocal crawl/$OUTPUT_DIR ./
