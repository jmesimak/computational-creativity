#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize

def split_text(text):
    return word_tokenize(text)
