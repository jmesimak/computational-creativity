#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from tokenizer import split_text
from markov import generate_markov_from_source, generate_markov
import json

# text_source = "http://www.gutenberg.org/cache/epub/158/pg158.txt"
# data = urllib2.urlopen(text_source)
# content_text = data.read()
# tokened_text = split_text(content_text)
tokened_text = json.load(open('wdictdump'))
print generate_markov(tokened_text, 55)
# print generate_markov_from_source(tokened_text, 55, True)
