#!/usr/bin/python

import sys

def emit(word, url, count):
    print '%s\t%s\t%s' % (word, url, count)

current_word = None
current_url = None
count = 0

for line in sys.stdin:
    word, url, frequency = line.strip().split('\t', 2)
    frequency = int(frequency)

    if word != current_word or url != current_url:
        if current_word:
            emit(current_word, current_url, count)
            count = 0

        if word != current_word:
            current_word = word

        if url != current_url:
            current_url = url

    count += 1

# print the last word/url/count
emit(current_word, current_url, count)