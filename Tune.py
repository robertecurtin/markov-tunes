#!/usr/bin/env python
# Written by Robert Curtin
# This class encapsulates information about a single tune.
import os # Temporary for testing
from Phrase import Phrase
from PhraseChain import PhraseChain
from Note import Note
from fractions import Fraction

def ParseAbcInfo(line):
    return line.split(':')[1].strip()
        
def ParseAbcFraction(line):
    info = ParseAbcInfo(line)
    fraction = Fraction(info.strip())
    return float(fraction)
    
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
    return char in "',/123456789><)}.~HKkMOPSTuv|"
    
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
    # J should not be used, this may have some other meaning
    # \ denotes a continuations, which is not relevant as we remove bars
    # + was used in previous abc standards, but is outdated
    return char.strip() in ': #*;?@m-J\\+[]'

class Tune:
    def __init__(self):
        self.title = ''
        self.meter = 6.0/8.0
        self.rhythm = 'Jig'
        self.noteLength = 1.0/8.0
        self.key = ''
        self.origin = ''
        self.currentNote = Note(self.noteLength)
        self.phraseChain = PhraseChain(self.meter, self.noteLength)
        
    def setMeter(self, meter):
        self.meter = meter
        self.phraseChain.meter = meter
        
    def setNoteLength(self, noteLength):
        self.noteLength = noteLength
        self.phraseChain.noteLength = noteLength
    
    def GetLengthModifier(self, note):
        return self.noteLength
        
    def extractPhrasesFromLine(self, line):
        # Detect notes
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
                    self.phraseChain.addNote(self.currentNote)
                    self.currentNote = Note(self.noteLength)
                self.currentNote.addChar(char)
                
            # If a chord is in progress, continue recording that chord until
            # the chord is closed
            elif inChord:
                self.currentNote.addChar(char)
                
            # If the character comes before a note and a note has been
            # recorded in the previous sequence, begin a new note
            # Otherwise, just add the character
            elif IsPreNote(char):
                if self.currentNote.containsNote():
                    self.phraseChain.addNote(self.currentNote)
                    self.currentNote = Note(self.noteLength)
                self.currentNote.addChar(char)
                
            # If the character is a note, do the same as PreNote above
            elif IsNote(char):
                if self.currentNote.containsNote():
                    self.phraseChain.addNote(self.currentNote)
                    self.currentNote = Note(self.noteLength)
                self.currentNote.addChar(char)
                
            # If the character comes after a note, it will only be added
            # if a note has been recorded. This may lose some information.
            elif IsPostNote(char):
                if self.currentNote.containsNote():
                    self.currentNote.addChar(char)
                
            elif char == '%':
                # Rest of the line is commented out
                break
            
            elif IsIgnored(char):
                continue
            else:
                print(ord(char))
                print("Warning: Unrecognized char [{}] from line [{}]"
                .format(char, line))

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
                self.setMeter(ParseAbcFraction(line))
            elif 'L' in line:
                self.setNoteLength(ParseAbcFraction(line))
            elif line.strip() == '':
                continue
            else:
                self.extractPhrasesFromLine(line)

tuneType = 'jig'
tuneKey = 'Dmaj'
folder = 'data/{}/{}'.format(tuneType, tuneKey)
for abcFileName in os.listdir(folder):      
    if 'abc' in abcFileName:
        print("Parsing {}...".format(abcFileName))
        fullAbcFileName = "{}/{}".format(folder, abcFileName)   
        t = Tune()
        t.parseFile(fullAbcFileName)