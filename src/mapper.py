#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    
    # separate url and words
    url = words[0]
    words = words[1:]
    frequency_dict = {}

    for word in words:
        try:
            frequency_dict[word] += 1
        except:
            frequency_dict[word] = 1
    
    for word, frequency in frequency_dict.iteritems():
        print '%s\t%s\t%s' % (word, url, frequency)