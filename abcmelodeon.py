#!/usr/bin/env python

import re
import argparse

# Regexs
# The key line
rxkey = re.compile(r'^K: ?(.+)$') 
# a note
rxnote = re.compile(r"[a-gA-G]" )

gRow = {"D":"~4",
        "^F":"^4",
        "G":"~6",
        "A":"^6",
        "B":"~8",
        "c":"^8",
        "d":"~10",
        "e":"^10",
        "^f":"^12",
        "g":"~12",
        "a":"^14",
        "b":"~14",
        "^c":"^16",
        "^d'":"~16"}

dRow = {"A,":"~3",
        "^C":"^3",
        "D":"~5",
        "E":"^5",
        "^F":"~7",
        "G":"^7",
        "A":"~9",
        "B":"^9",
        "^c":"^11",
        "d":"~11",
        "e":"^13",
        "^f":"~13",
        "g":"^15",
        "a'":"~15"}


def getkey (infile):
    """ Read an abc file and extract the key """
    key = None
    for thisline in infile:
        m = rxkey.search(thisline)
        if m:
            if key is not None:
                raise ValueError("Multiple key lines found")
            key = m.group(1).strip()

    return key


def annotateabc (infile):
    """ Annotate an abc file with button numbers """

    key = getkey(infile)

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
            notes.append(  rxnote.findall(thisline) )


    return notes

def applykeysig(note, key):
    """ Sharpen the appropriate notes
    Only implemented for G/D for now
    """
    # TODO Handle naturals
    if key == "C":
        return note
    if key == "G" or key == "Gmaj":
        if note.upper() == "F":
            return ("^" + note)
        return note
    if key == "D" or key == "Dmaj":
        if note.upper() == "F":
            return ("^" + note)
        if note.upper() == "C":
            return ("^" + note)
        return note
    else:
        print "Key not supported"




parser = argparse.ArgumentParser(description = "Add button numbers to abc file")
parser.add_argument("--infile", required=True)
parser.add_argument("--outfile", required=True)

args = parser.parse_args()

abcfile = readfile(args.infile)

annotatedabc = annotateabc(abcfile)


notes = extractnotes(abcfile)
key = getkey(abcfile)


print notes

newnotes = [[applykeysig(n, key=key) for n in nn] for nn in notes]

# TODO To a function
gRownotes = [[gRow.get(x,"*") for x in y] for y in newnotes]
dRownotes = [[dRow.get(x,"*") for x in y] for y in newnotes]

gnotestring = [' '.join(x) for x in gRownotes]
dnotestring = [' '.join(x) for x in dRownotes]

with open(args.outfile, "w") as file:
    foundkey = False
    for line in abcfile:
        file.write(line)
        if foundkey:
            if len(gnotestring) > 0:
                file.write("w: " + gnotestring.pop(0) + "\n")
            if len(dnotestring) > 0:
                file.write("w: " + dnotestring.pop(0) + "\n")
        if rxkey.search(line):
            foundkey = True
