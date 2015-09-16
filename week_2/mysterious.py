from collections import OrderedDict
from operator import itemgetter

fname = "as_x.txt"
mysterious_things = {}
with open(fname, "r") as f:
    for line in f:
        if "as mysterious as" in line:
            suchmysterious = line.split(' ')[:5][4].split('\t')[0]
            if len(suchmysterious) > 1:
                if suchmysterious not in mysterious_things:
                    mysterious_things[suchmysterious] = 1
                else:
                    mysterious_things[suchmysterious] += 1

print OrderedDict(sorted(mysterious_things.items(), key=itemgetter(1), reverse=True))
