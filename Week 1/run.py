#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from tokenizer import split_text
from markov import *
import json

text_source = "http://www.gutenberg.org/cache/epub/158/pg158.txt"
data = urllib2.urlopen(text_source)
content_text = data.read()
tokened_text = split_text(content_text)
transitions = generate_nth_order_transitions(tokened_text, 3)
chain = generate_markov(transitions)
print chain
