#!/usr/bin/python

import sys

for line in sys.stdin:

  line = line.strip()
  words = line.split()
	
  # separate url and words
  url = words[0]
  words = words[1:]

  for word in words:
    print '%s\t%s\t%s' % (word, url, 1)

