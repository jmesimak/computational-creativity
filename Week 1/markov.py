#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from copy import copy
from collections import OrderedDict

def generate_nth_order_transitions(tokenized_source, order=1):
    ret = OrderedDict()
    for idx, token in enumerate(tokenized_source):
        pre_tuple_list = []
        for i in range(0, order):
            if (idx+i) < len(tokenized_source):
                pre_tuple_list.append(tokenized_source[idx+i])
            else:
                pre_tuple_list.append("")

        follower_idx = idx + order

        follower = ""
        if follower_idx <= len(tokenized_source)-1:
            follower = tokenized_source[idx+order]

        key = tuple(pre_tuple_list)
        if key not in ret:
            ret[key] = {}
            ret[key][follower] = 1
        else:
            if follower not in ret[key]:
                ret[key][follower] = 1
            else:
                ret[key][follower] += 1

    return ret

def generate_markov(transitions):
    cur = transitions.keys()[0]
    cur_str = get_next_token(transitions[cur])
    ret = ""
    while cur_str is not "":
        try:
            t = get_next_token(transitions[cur])
        except KeyError:
            break
        cur_str = t
        newkey = []
        for idx, item in enumerate(cur):
            if idx > 0:
                newkey.append(item)
        newkey.append(t)
        cur = tuple(newkey)
        ret += " " + cur_str
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
