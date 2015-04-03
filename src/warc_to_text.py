#!/usr/bin/python

from hanzo import warctools
import codecs
import re
import sys

from html_parser import strip_html

if not sys.argv[1]:
  print "Please supply warc.gz file"
  sys.exit(1)

if not sys.argv[2]:
  print "please supply an output directory"
  sys.exit(2)

warcStream = warctools.WarcRecord.open_archive(sys.argv[1])
outputDir = sys.argv[2]
regex = re.compile(r'\W+')

i = 0

for record in warcStream:
  if record.type == "response":
    if record.content[1][0:50].find("HTTP/1.1 2") > -1:	#if a succesful response
      startIndex = record.content[1].find("<html")
      if startIndex > -1:	#if html found

        # get filename
        filename = re.sub('[<>]', '', record.id)
        filename = re.sub(':', '-', filename)
        fileName = outputDir + '/' + filename
        
        fileObject = codecs.open(fileName, "w", "utf-8")
        fileObject.write(record.url + ' ')
        
        words = strip_html(record.content[1][startIndex:-1])
        for word in words:
          # if word is utf-8, write it to file
          try:
            utf8_word = word.decode('utf-8')
            fileObject.write(utf8_word + ' ')
          except UnicodeDecodeError:
            pass
        fileObject.close()
        
        # logging
        i = i + 1
        if i % 10 == 0:
          print '%6s records processed' % (i) 

print 'Plain Text Files Have Been Extracted'
