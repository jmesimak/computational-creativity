#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

def split_text(text):
    return text.replace('\n', '').translate(string.maketrans("",""), string.punctuation).split(' ')
