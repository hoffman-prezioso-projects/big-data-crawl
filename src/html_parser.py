#!/usr/bin/python

import re


def strip_html(html):

    # regex patterns
    script_pattern = re.compile(
        '(<script.*?</script>)|(<noscript*?</noscript>)', re.DOTALL)
    html_pattern = re.compile('(<!--.*?-->)|(<.*?>)', re.DOTALL)
    nonword_pattern = re.compile(
        r'(\w+://)?\w+\.\S+|\S*@\S|(&.+?;)|[^a-zA-Z]|[0-9]', re.DOTALL)

    # get rid of html tags and other unwanted stuff
    cleaned = re.sub(script_pattern, '', html)
    cleaned = re.sub(html_pattern, ' ', cleaned)
    cleaned = re.sub(nonword_pattern, ' ', cleaned)

    # get all the words from the cleaned text and display them
    cleaned = cleaned.lower()
    words = cleaned.split()

    return words
