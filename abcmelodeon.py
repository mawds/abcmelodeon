#!/usr/bin/env python

import re
import argparse

# Regexs
# The key line
rxkey = re.compile(r'^K: ?(.+)$') 
# a note
rxnote = re.compile(r'([\^_]?[a-gA-G])|(".+?")' )
rxtunestart = re.compile(r'^[XT]:')
rxblankline = re.compile(r'^$')

notemappings = {}
notemappings["gRow"]= {"F":"~2",
        "_E":"^2",
        "D":"~4",
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
        "c'":"^16",
        "d'":"~16",
        "e'":"^18",
        "g'":"~18",
        "^f'":"^20",
        "b'":"~20"
        }

notemappings["dRow"] = {"^G":"~1",
        "_B":"^1",
        "A,":"~3",
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
        "a":"~15",
        "b":"^17",
        "d'":"~17",
        "^c'":"^19",
        "^f'":"~19",
        "a'":"~21",
        "e'":"^21"
        }

#TODO finish - do automatically. Sharps and flats
notemappings["noteNames"] = {"a":"A",
        "b":"B",
        "c":"C",
        "d":"D",
        "e":"E",
        "f":"F",
        "g":"G"}

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

    try:
        key = getkey(infile)
    except ValueError as e:
        print e
        print infile
    notes = extractnotes(infile)

    newnotes = [[applykeysig(n, key=key) for n in nn] for nn in notes]

    notestrings = []
    for m in mappings:
        notestrings.append(getNoteString(newnotes, notemappings[m]))

    outabc = ''
    foundkey = False
    for line in infile:
        outabc += line
        if foundkey:
            for n in notestrings:
                if len(n) > 0:
                    outabc += ("w: " + n.pop(0) + "\n")
        if rxkey.search(line):
            foundkey = True

    return outabc


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
            linenotes = [i[0] for i in rxnote.findall(thisline)]
            # Remove blank notes - these are where a chord was 
            # extracted instead
            justnotes = filter(None, linenotes)
            notes.append( justnotes )

    return notes

def extractabc(tunebook):
    """ Extract the tunes from a tunebook """
    # TODO handle comments, formatting etc.
    tunes = []
    thistune = [] 
    intune = False
    for thisline in tunebook:
        if rxtunestart.search(thisline) and not intune:
            thistune = []
            intune = True

        if intune: 
            thistune.append(thisline)
            

        if thisline in ['\n', '\r\n']:
            if len(thistune) > 3:
                tunes.append(thistune)
            intune = False

    # If there's no blank line at the end,add the tune
    if intune:
        if len(thistune) > 3:
            tunes.append(thistune)
        

    return tunes

def applykeysig(note, key):
    """ Sharpen the appropriate notes
    Only implemented for G/D for now
    """
    # TODO Handle naturals
    # TODO handle other keys - presumably there's a clever way
    # of doing this if you know music theory
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
        # Just return the note for now 
        # THIS WILL BREAK THE ANNOTATION 
        return note



def getNoteString(notes, notemap):
    mappednotes = [[notemap.get(x,"*") for x in y] for y in notes]

    notestring = [' '.join(x)   for x in mappednotes]

    return notestring

parser = argparse.ArgumentParser(description = "Add button numbers to abc file")
parser.add_argument("infile")
parser.add_argument("outfile")
parser.add_argument("--mappings", default ="gRow,dRow")

args = parser.parse_args()
mappings = args.mappings.split(",")

abcfiles = readfile(args.infile)
abcbook = extractabc(abcfiles)
annotatedabc = []
for tune in abcbook:
    annotated = annotateabc(tune)
    annotatedabc.append(annotated)

with open(args.outfile, "w") as file:
    for abc in annotatedabc:
        file.write(abc)

