#!/usr/bin/env python

import re
import argparse

# Regexs
# The key line
rxkey = re.compile(r'^K: ?(.+$)') 
# a note
rxnote = re.compile(r"[a-gA-G]" )

def getkey (infile):
    """ Read an abc file and extract the key """
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

def extractnotes (infile):
    """ Extract the notes from the file. 
    We read everything from the Key line until we get to an empty line.
    We don't care about note length"""
    notes = []
    foundbody = False
    for thisline in infile:
        if rxkey.search(thisline):
            foundbody = True
            continue
        if foundbody:
            notes.append( [ rxnote.findall(thisline) ])


    return notes




parser = argparse.ArgumentParser(description = "Add button numbers to abc file")
parser.add_argument("--infile", required=True)
parser.add_argument("--outfile", required=True)

args = parser.parse_args()

abcfile = readfile(args.infile)

annotatedabc = annotateabc(abcfile)


notes = extractnotes(abcfile)
print notes


