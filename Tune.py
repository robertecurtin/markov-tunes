#!/usr/bin/env python

# Written by Robert Curtin
import os # Temporary for testing
from Phrase import Phrase
from Note import Note

def ParseAbcInfo(line):
    return line.split(':')[1].strip()
        
def IsPreNote(char):
    # ^ _ and = change a note to sharp, flat, or natural respectively
    # ( begins a slur, { begins a grace note
    return char in '^=_({'
    
def IsPostNote(char):
    # ' and , change the octave of the note
    # Combining / and numbers change the length of the note
    # Using > and < change the length of the notes on each side of it
    # ) ends a slur, } ends a grace note
    # . ~ H K k M O P S T u v are various accents
    return char in "',/123456789><)}.~HKkMOPSTuv"
    
def IsNote(char):
    # Note: z is a rest
    return char in 'abcdefgABCDEFGz'
    
def IsChord(char):
    return char in '"!'    

def ContainsNote(string):
    for char in string:
        if IsNote(char):
            return True
    return False

def IsIgnored(char):
    # m is used for chords
    # | denotes a bar separating phrases
    # : is used for repeats
    # # * ; ? @ are ignored per the abc standard v2.1
    # [] denote temporary changes, which I am ignoring 
    # - denotes a tie, which I am ignoring
    # Stripping the char ensures whitespace characters are ignored
    return char.strip() in '|: #*;?@[]m-'

class Tune:
    def __init__(self):
        self.title = ''
        self.meter = 6/8
        self.rhythm = 'Jig'
        self.noteLength = 1/8
        self.key = ''
        self.origin = ''
        self.phrases = {}
        self.startPhrase = Phrase()
        self.currentPhrase = self.startPhrase
    
    def GetLengthModifier(self, note):
        return self.noteLength
        
    def extractPhrasesFromLine(self, line):
        # Detect notes
        firstNote = Note()
        notes = [firstNote]
        inChord = False
        for char in line.strip():
            # Record everything between " as a single note, as it is a chord
            if IsChord(char):
                if inChord:
                    # Close the chord
                    inChord = False
                else:
                    # Begin a new chord
                    inChord = True
                    notes.append(Note())
                notes[-1].addChar(char)
                
            # If a chord is in progress, continue recording that chord until
            # the chord is closed
            elif inChord:
                notes[-1].addChar(char)
                
            # If the character comes before a note and a note has been
            # recorded in the previous sequence, begin a new note
            # Otherwise, just add the character
            elif IsPreNote(char):
                if notes[-1].containsNote():
                    notes.append(Note())
                notes[-1].addChar(char)
                
            # If the character is a note, do the same as PreNote above
            elif IsNote(char):
                if notes[-1].containsNote():
                    notes.append(Note())
                notes[-1].addChar(char)
                
            # If the character comes after a note, it will always be added
            elif IsPostNote(char):
                notes[-1].addChar(char)
                
            elif char == '%':
                # Rest of the line is commented out
                break
            
            elif IsIgnored(char):
                continue
            else:
                print(ord(char))
                print("Warning: Unrecognized char [{}] from line [{}]"
                .format(char, line))
            
        # Combine notes until phrase length is met
        for note in notes:
            length = note.getLength()
            if length != 1:
                print("{} has length {}".format(note.text, length))
            
     # Carry over remainder to next phrase
        
    def parseFile(self, fileName):
        if '.abc' not in fileName:
            print("Warning: The selected file is not a .abc file.")
        abcFile = open(fileName, 'r')
        for line in abcFile:
            if any(x in line for x in [ 'A:', 'B:', 'C:', 'D:', 'E:', 'F:', 
                                        'G:', 'H:', 'I:', 'N:', 'O:', 'P:', 
                                        'Q:', 'S:', 'W:', 'Z']):
                continue
            if 'X:' in line:
                tuneNumber = ParseAbcInfo(line)
                if tuneNumber != '1':
                    # Begin parsing the new tune
                    print("New tune {}".format(tuneNumber))
                    
    
            elif 'T:' in line:
                self.title = ParseAbcInfo(line)
            elif 'R:' in line:
                self.rhythm = ParseAbcInfo(line)
            elif 'K:' in line:
                self.key = ParseAbcInfo(line)
            elif 'M:' in line:
                self.meter = ParseAbcInfo(line)
            elif 'L' in line:
                self.noteLength = ParseAbcInfo(line)
            elif line.strip() == '':
                continue
            else:
                self.extractPhrasesFromLine(line)

tuneType = 'reel'
tuneKey = 'Dmaj'
folder = 'data/{}/{}'.format(tuneType, tuneKey)
for abcFileName in os.listdir(folder):      
    if 'abc' in abcFileName:
        print("Parsing {}...".format(abcFileName))
        fullAbcFileName = "{}/{}".format(folder, abcFileName)   
        t = Tune()
        t.parseFile(fullAbcFileName)