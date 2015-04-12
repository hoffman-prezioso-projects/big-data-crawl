#!/usr/bin/python

from hanzo import warctools
import codecs
import re
import sys
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

warc_stream = warctools.WarcRecord.open_archive(sys.argv[1])
output_directory = sys.argv[2]
spell_checker = SpellChecker()
file_name_counter = 0
current_file = codecs.open('data/' + str(file_name_counter / records_per_file)
                           .zfill(6) + '.txt', 'w', 'utf-8')
for record in warc_stream:

    if record.type == "response":

        # if not a robots.txt page
        if record.url.rfind('robots.txt') == -1:
            # find start of <body>
            startIndex = record.content[1][5:].find("<body")

            # if body found
            if startIndex > -1:
                # add url to beginning of line
                current_file.write(record.url + ' ')

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

print 'Plain Text Files Have Been Extracted'

minutes, seconds = divmod(time() - start_time, 60)
print "Total Time: %d minutes %d seconds" % (minutes, seconds)
