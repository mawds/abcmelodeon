# abcmelodeon
Add (melodeon) button numbers or note names to ABC music files

This Python script will add "lyrics" to [ABC Notation](http://abcnotation.com/) music files containing the melodeon button numbers corresponding to each note.  It uses Ed Rennie's system (i.e. outer row odd), and prefixes pull notes with a ^.

To use:

```
./abcmelodeon.py infile outfile
```

where `infile` and `outfile` are the input and output abc music files.

The program takes an optional `--mappings` argument.  This should be supplied
with one or more "mappings": dRow, gRow (which will print "Ed Rennie" style button numbers for a Hohner D/G box), or noteNames (which will print the names of each note).

By default both the D and G row notes will be printed, which helps when trying to work out how to cross rows.

For example, to annotate mytune.abc with G row and note names to the file mytune_out.abc:

```
./abcmelodeon.py --mappings gRow,noteNames mytune.abc mytune_out.abc
```
(note no space between gRow and noteNames)

