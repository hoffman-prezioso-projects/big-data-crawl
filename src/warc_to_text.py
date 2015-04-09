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
  records_per_file = 1000
else:
  records_per_file = int(sys.argv[4])

warcStream = warctools.WarcRecord.open_archive(sys.argv[1])
outputDir = sys.argv[2]
regex = re.compile(r'\W+')

i = 0

for record in warcStream:
  if i % records_per_file == 0:
    fileObject = codecs.open('data/' + str(i / records_per_file).zfill(6) + '.txt', 'w', 'utf-8')
  if record.type == "response":
    if record.content[1][0:50].find("HTTP/1.1 2") > -1:	#if a succesful response
      startIndex = record.content[1].find("<html")
      if startIndex > -1:	#if html found

        fileObject.write(record.url + ' ')
        
        
        words = strip_html(record.content[1][startIndex:-1])
        for word in words:
          # if word is utf-8, write it to file
          try:
            utf8_word = word.decode('utf-8')
            fileObject.write(utf8_word.lower() + ' ')
          except UnicodeDecodeError:
            pass
        
        fileObject.write('\n')
        # logging
        i = i + 1
        if i % 100 == 0:
          print '%6s records processed' % (i)
        if max_records > 0 and i == max_records:
          break
  
  if i % records_per_file == 0: 
    fileObject.close()

print 'Plain Text Files Have Been Extracted'