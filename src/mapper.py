#!/usr/bin/python

import sys

for line in sys.stdin:

  line = line.strip()
  words = line.split()
	
  # separate url and words
  url = words[0]
  words = words[1:]
	
  # compute word frequencies
  word_frequencies = {}
  for word in words:
    if word in word_frequencies:
      word_frequencies[word] += 1
    else:
      word_frequencies[word] = 1
  
  # emit word and its frequecy
  for word in word_frequencies:
		print '%s\t%s\t%s' % (word, url, word_frequencies[word])
