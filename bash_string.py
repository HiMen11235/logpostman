#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import codecs

# fpath = 'FromHosttoTohost,srcIP,dstIP.log'

if __name__ == "__main__":
    arg = sys.argv
    with codecs.open(arg[1],'r','utf-8') as f:
        for line in f:
            srcIP = os.path.basename(line).split(",")[1]
            dstIP = os.path.basename(line).split(",")[2].split(".", 1)[0]
            print "'" + 'logpostman ' + '--spoof ' + srcIP + ' --eps 250 ' + '--file ' + line + ' --quiet ' + dstIP + "'"