#!/usr/bin/env python

import re
import argparse

def getkey (infile):
    """ Read an abc file and extract the key """
    rxkey = re.compile(r'^K: ?(.+$)') 
    key = None
    for thisline in infile:
        m = rxkey.search(thisline)
        if m:
            if key is not None:
                raise ValueError("Multiple key lines found")
            key = m.group(1)

    return key


def annotateabc (infile):
    """ Annotate an abc file with button numbers """

    key = getkey(infile)
    print key

def readfile (infile):
    """ Read in a file """
    with open(infile) as file:
        content = file.readlines()

    return content

parser = argparse.ArgumentParser(description = "Add button numbers to abc file")
parser.add_argument("--infile", required=True)
parser.add_argument("--outfile", required=True)

args = parser.parse_args()

abcfile = readfile(args.infile)

annotatedabc = annotateabc(abcfile)



