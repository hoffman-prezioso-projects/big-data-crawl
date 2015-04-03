#!/usr/bin/python

import re

def strip_html(html):
	
	# regex patterns
	body_pattern = re.compile('<body.*?>(.*?)</body>', re.DOTALL)
	script_pattern = re.compile('(<script.*?</script>)|(<noscript*?</noscript>)', re.DOTALL)
	html_pattern = re.compile('(<!--.*?-->)|(<.*?>)', re.DOTALL)
	nonword_pattern = re.compile(r'(&.+?;)|\\|\.\s|\||\"|!|:|;|,|/', re.DOTALL)

	# get the body
	body = re.search(body_pattern, html)
  
	# if body wasn't found, get out of here
	if (body == None):
		return []
	body = body.group(1);

	# get rid of html tags and other unwanted stuff
	cleaned = re.sub(script_pattern, '', body)
	cleaned = re.sub(html_pattern, ' ', cleaned)
	cleaned = re.sub(nonword_pattern, ' ', cleaned)

	# get all the words from the cleaned text and display them
	words = cleaned.split()
	
	return words

