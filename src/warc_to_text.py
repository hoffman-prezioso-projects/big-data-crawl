#!/usr/bin/python

from hanzo import warctools
import codecs
import re
import sys
from multiprocessing import Process
from spell_checker import SpellChecker
from time import time
from html_parser import strip_html

start_time = time()

if len(sys.argv) < 2:
    print "Please supply warc.gz file"
    sys.exit(1)

if len(sys.argv) < 3:
    print "please supply an output directory"
    sys.exit(2)

if len(sys.argv) < 4:
    max_records = 0
else:
    max_records = int(sys.argv[3])

if len(sys.argv) < 5:
    records_per_file = 10000
else:
    records_per_file = int(sys.argv[4])


def split_array(array):
    temp1 = array[:len(array)/2]
    temp2 = array[len(array)/2:]
    a = temp1[:len(temp1)/2]
    b = temp1[len(temp1)/2:]
    c = temp2[:len(temp2)/2]
    d = temp2[len(temp2)/2:]
    return [a, b, c, d]


def split_stream(stream):
    # a, b, c, d = [], [], [], []
    a, d = [], []
    counter = 0
    for record in stream:
        if counter % 2 == 0:
            a.append(record)
        # elif counter % 4 == 1:
        #     b.append(record)
        # elif counter % 4 == 2:
        #     c.append(record)
        else:
            d.append(record)
        if counter == 22000:
            break
        counter += 1
    # return [a, b, c, d]
    return [a, d]


warc_stream = warctools.WarcRecord.open_archive(sys.argv[1])


# warc_stream_array = []
# for record in warc_stream:
#     warc_stream_array.append(record)

warc_streams = split_stream(warc_stream)


def convert_warc_to_text(warc_stream):
    output_directory = sys.argv[2]
    spell_checker = SpellChecker()
    file_name_counter = 0
    current_file = codecs.open('data/' + str(file_name_counter / records_per_file)
                               .zfill(6) + '.txt', 'w', 'utf-8')

    for record in warc_stream:
        if record.type == "response":

            # if not a robots.txt page
            if record.url[-10:] != 'robots.txt':
                # find start of <body>

                startIndex = record.content[1][5:].find("<body")

                # if body found
                if startIndex > -1:
                    # add url to beginning of line
                    record_url = record.url
                    if record_url.endswith("/"):
                        record_url = record_url[:-1]
                    current_file.write(record_url + ' ')

                    # strip out html
                    words = strip_html(record.content[1][startIndex:-1])

                    for word in words:
                        if spell_checker.check(word):  # word is spelled correctly
                            current_file.write(word + ' ')

                    current_file.write('\n')

                    # logging
                    file_name_counter += 1

                    if file_name_counter % 500 == 0:
                        time_per_100_records = ((((time() - start_time) * 1000) /
                                                file_name_counter) * 100)

                        print '%6s records processed at %d ms per 100 records' % \
                            (file_name_counter, time_per_100_records)

                        if file_name_counter % records_per_file == 0:
                            current_file.close()
                            current_file = codecs.open(
                                'data/' + str(file_name_counter / records_per_file)
                                .zfill(6) + '.txt', 'w', 'utf-8')


p = Process(target=convert_warc_to_text, args=(warc_streams[0],))
q = Process(target=convert_warc_to_text, args=(warc_streams[1],))
# r = Process(target=convert_warc_to_text, args=(warc_streams[2],))
# s = Process(target=convert_warc_to_text, args=(warc_streams[3],))
p.start()
q.start()
# r.start()
# s.start()
p.join()
q.join()
# r.join()
# s.join()

# p.map(convert_warc_to_text, warc_stream_array)

# p.close()
# p.join()
# def put_on_queue(queue, stream):
#     queue.put(convert_warc_to_text(stream))

# q = Queue.Queue()

# for stream in warc_streams:
#     t = threading.Thread(target=put_on_queue, args=(q, stream))
#     t.daemon = False
#     t.start()

# s = q.get()

# print s

print 'Plain Text Files Have Been Extracted'

minutes, seconds = divmod(time() - start_time, 60)
print "Total Time: %d minutes %d seconds" % (minutes, seconds)
