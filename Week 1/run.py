#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from tokenizer import split_text
from markov import generate_markov_from_source

text_source = "http://www.gutenberg.org/cache/epub/158/pg158.txt"
data = urllib2.urlopen(text_source)
content_text = data.read()
tokened_text = split_text(content_text)
print generate_markov_from_source(tokened_text, 55)
