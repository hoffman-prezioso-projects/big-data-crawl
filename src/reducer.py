#!/usr/bin/python

import sys

def emit(word, url, frequency):
    print '%s\t%s\t%s' % (word, url, frequency)

last_word = None
last_url = None
last_frequency = 0

for line in sys.stdin:
    current_word, current_url, current_frequency = line.strip().split('\t', 2)
    current_frequency = int(current_frequency)

    if current_word == last_word and current_url == last_url:
        last_frequency += current_frequency
    else:
        emit(last_word, last_url, last_frequency)
        last_word = current_word
        last_url = current_url
        last_frequency = current_frequency

# print the last word/url/frequency if needed
try:
    emit(last_word, last_url, last_frequency)
except:
    pass