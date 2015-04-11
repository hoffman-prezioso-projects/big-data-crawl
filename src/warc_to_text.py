#!/usr/bin/python

from hanzo import warctools
import codecs
import re
import sys

from html_parser import strip_html

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
regex = re.compile(r'\W+')

file_name_counter = 0

for record in warc_stream:
    if file_name_counter % records_per_file == 0:
        current_file = codecs.open('data/' + str(file_name_counter / records_per_file).zfill(6) + '.txt', 'w', 'utf-8')
    if record.type == "response":
        if record.content[1][0:50].find("HTTP/1.1 2") > -1: #if a succesful response
            startIndex = record.content[1].find("<html")
            if startIndex > -1: #if html found

                current_file.write(record.url + ' ')
                
                
                words = strip_html(record.content[1][startIndex:-1])
                for word in words:
                    # if word is utf-8, write it to file
                    try:
                        utf8_word = word.decode('utf-8')
                        current_file.write(utf8_word.lower() + ' ')
                    except UnicodeDecodeError:
                        pass
                
                current_file.write('\n')
                # logging
                file_name_counter = file_name_counter + 1
                if file_name_counter % 500 == 0:
                    print '%6s records processed' % (file_name_counter)
                if max_records > 0 and file_name_counter == max_records:
                    break
    
    if file_name_counter % records_per_file == 0: 
        current_file.close()

print 'Plain Text Files Have Been Extracted'