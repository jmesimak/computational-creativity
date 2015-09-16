from collections import OrderedDict
from operator import itemgetter
import re

fname = "as_x.txt"
mysterious_things = {}
with open(fname, "r") as f:
    for line in f:
        if "the" in line:
            print line
        # m = re.search('as\s[a-z]+\sas\sa\sstudent', line)
        # if m != None:
        #     print m.group(0)
