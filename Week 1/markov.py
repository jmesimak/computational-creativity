#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from copy import copy
from collections import OrderedDict
import time
import json

# For each word/symbol, we need to find out all the possible words/symbols that can appear after it.
# We also need the counts in order to work with the probabilities.
# 'computer': {'science': 5, 'system': 4, 'repair': 3}
def generate_transitions(tokenized_source, save_source):
    begin = time.time()
    print 'generating transitions'
    wdict = {}
    for token in tokenized_source:
        if token not in wdict:
            # Find all occurrences of token, get their successors.
            wdict[token] = nth_order_occ_dict(token, tokenized_source)

    end = time.time()
    print 'it took ' + str(end - begin) + ' seconds to construct the transitions'

    if save_source:
        json.dump(wdict, open('wdictdump', 'w'))

    return wdict

def generate_transitions_fast(tokenized_source, save_source):
    begin = time.time()
    print 'generating transitions fast'
    ret = {}
    prev = ''
    for token in tokenized_source:
        if token not in ret:
            ret[token] = {}

        if prev != '':
            if token not in ret[prev]:
                ret[prev][token] = 1
            else:
                ret[prev][token] += 1

        prev = token
    end = time.time()
    print 'it took ' + str(end - begin) + ' seconds to construct the transitions'
    return ret

## This is not yet working, need to parse all the dicts together
def nth_order_occ_dict(t, tokenized_source, order=1):
    current = occurrence_dict(t, tokenized_source)
    for i in range(1, order):
        new_wdict = {}
        for token in current:
            temp = occurrence_dict(token, tokenized_source)
            for temp_t in temp:
                if temp_t not in new_wdict:
                    new_wdict[temp_t] = 1
                else:
                    new_wdict[temp_t] += 1

        current = new_wdict

    return current

def occurrence_dict(t, tokenized_source):
    ret = {}
    for i, token in enumerate(tokenized_source[:-1]):

        # Found an occurrence
        if token == t:

            # Get the succeeding token
            next_t = tokenized_source[i+1]

            # Place it in the dict or increment the counter by 1
            if next_t not in ret:
                ret[next_t] = 1
            else:
                ret[next_t] += 1


    return ret

def generate_markov(wdict, length):
    print 'generating markov'
    keys = wdict.keys()
    cur_t = keys[randint(0, len(keys) - 1)]
    while not str.istitle(str(cur_t[0])):
        cur_t = keys[randint(0, len(keys) - 1)]
    ret = cur_t

    for x in range(0, length):
        cur_t = get_next_token(wdict[cur_t])
        if cur_t != ',':
            ret += ' '
        ret += cur_t
    return ret


def get_next_token(transition_dict):
    total = 0
    ret = ""
    td_cpy = OrderedDict(sorted(copy(transition_dict).items(), key=lambda t: t[1]))
    for token in td_cpy:
        total += transition_dict[token]
        td_cpy[token] = total

    next_t_int = randint(1, total)

    for i, (t, v) in enumerate(td_cpy.items()):
        if next_t_int <= v:
            ret = t
            break

    return ret

def generate_markov_from_source(tokenized_source, length, save_source=False):
    return generate_markov(generate_transitions_fast(tokenized_source, save_source), length)
