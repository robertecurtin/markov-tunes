#!/usr/bin/env python
# This file creates markov links from a series of ABC files in directories
# relative to this one.
# Each link is one measure in the tune.

# Written by Robert Curtin
import urllib2
import os

def ParseAbcInfo(line):
    return line.split(':')[1].strip()

def WriteMarkov(firstLink, secondLink, tuneType, tuneKey):
    # Write the specified Markov pair to the correct file
    # as determined by the tune type and key.
    if firstLink.strip() == '' or secondLink.strip() == '':
        print("Issue at {}|{}".format(firstLink, secondLink))
    folder = 'data/{}/{}'.format(tuneType, tuneKey)
    if not os.path.exists(folder):
        os.makedirs(folder)
    fileName = "{}/MarkovLinks.txt".format(folder)
    markovFile = open(fileName, 'a')
    markovFile.write('{} | {}\n'.format(firstLink, secondLink))
    markovFile.close()

def ParseAbcFile(abcFileName, tuneType, tuneKey):
    # Find markov links within the given file.
    currentMeasure = "start" # This indicates the beginning of a new tune
    tuneName = ''
    abcFile = open(abcFileName, 'r')
    for line in abcFile:
        if 'Z:' in line or 'S:' in line or 'M:' in line or 'L:' in line:
            continue
        if 'X:' in line:
	    # This marks the beginning of a new tune
            tuneNumber = ParseAbcInfo(line)
            if tuneNumber != '1':
                print("New tune {}".format(tuneNumber))
                WriteMarkov(currentMeasure, 'end', tuneType, tuneKey)
                currentMeasure = "start"

        elif 'T:' in line:
            tuneName = ParseAbcInfo(line)
        elif 'R:' in line:
            if tuneType != ParseAbcInfo(line):
                print("Tune type mismatch!")
        elif 'K:' in line:
            if tuneKey != ParseAbcInfo(line):
                print("Tune key mismatch!")            
        elif line.strip() == '':
            continue
        elif '|' in line:
            # This is a part of the tune
            editedLine = line.strip()
            editedLine = line.replace(':','')
	    # Extract measures from the tune
            for measure in editedLine.split('|'):
                editedMeasure = measure.strip()
                if(editedMeasure == ''):
                    continue
                WriteMarkov(currentMeasure, editedMeasure, tuneType, tuneKey)
                currentMeasure = editedMeasure                
        else:
            continue
    abcFile.close()
    WriteMarkov(currentMeasure, 'end', tuneType, tuneKey)
    return True

# Process all tunes of a given type and key and generate the markov pairs file
tuneType = 'reel'
tuneKey = 'Dmaj'
folder = 'data/{}/{}'.format(tuneType, tuneKey)
markovFile = "{}/MarkovLinks.txt".format(folder)
if os.path.isfile(markovFile):
    os.remove(markovFile)
for abcFileName in os.listdir(folder):
    if 'abc' in abcFileName:
        fullAbcFileName = "{}/{}".format(folder, abcFileName)
        print("Processing {}".format(fullAbcFileName))
        ParseAbcFile(fullAbcFileName, tuneType, tuneKey) 
