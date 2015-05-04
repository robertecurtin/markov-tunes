#!/usr/bin/env python

# Written by Robert Curtin

from random import randint
from Note import Note

# This class represents a single musical phrase
# It also tracks which other phrases it relates to.
class Phrase:
    def __init__(self):
        self.notes = []
        self.tunes = []     # All tunes that contain this phrase
        self.tuneType = ''
        self._linkedPhrases = {} # All phrases that come after this one
    
    def addNote(self, note):
        self.notes.append(note)
    
    def addOriginTune(self, tuneName):
        if tuneName not in self.originTunes:
            self.originTunes.append(tuneName)
        else:
            print("Warning: Tune {} is already recorded in phrase {}".format(\
            tuneName, self.notes))
            
    def linkPhrase(self, phrase):
        if phrase not in self._linkedPhrases:
            self._linkedPhrases[phrase] = 1
        else:
            self._linkedPhrases[phrase] += 1
            
    def getLastNote(self):
        return self.notes[-1]

    def getLength(self):
        length = 0
        for note in self.notes:
            length += note.length
        return length
        
    def isLastNoteBroken(self):
        return self.getLastNote().isDotted() or self.getLastNote().isHalved()
        
    def getLastNoteLength(self):
        return self.getLastNote().getLength()
        
    def getNextPhrase(self):
        # Determine the next phrase randomly using Markov chains
        totalPhraseWeights = sum(self._linkedPhrases.values())
        selectedPhrase = randint(1, totalPhraseWeights)
        currentPhraseWeight = 0
        print("Selecting next phrase ({}) from ".format(selectedPhrase))
        for phrase in self._linkedPhrases:
            print("{} : {}".format(phrase.notes, self._linkedPhrases[phrase]))
        for phrase in self._linkedPhrases:
            currentPhraseWeight += self._linkedPhrases[phrase]
            if currentPhraseWeight > selectedPhrase:
                print("Selected: {}".format(phrase.notes))
                return phrase
                
# This class represents a chain of phrases, constructed by adding one note
# at a time.
# Be sure to set the phrase length before adding notes to properly group
# phrases.
class PhraseChain:
    def __init__(self):
        firstPhrase = Phrase()
        self._phrases = [firstPhrase]
        self.phraseLength = 1/8
        
    def getLastPhrase(self):
        return self._phrases[-1]
        
    def isLastNoteBroken(self):
        return self.getLastPhrase().isLastNoteDotted()
        
    def getLastNoteLength(self):
        return self.getLastPhrase().getLastNoteLength()
        
    def addNote(self, note):
        if self.isLastNoteBroken():
            newLength = 2 - self.getLastNoteLength
            note.setLength(newLength)
        self.getLastPhrase().addNote(note)
        if self.getLastPhrase().getLength() >= self.phraseLength:
            if self.getLastPhrase().getLength() != self.phraseLength:
                print("Error: Phrase {} too long for length {}".format(
                self.getLastPhrase().notes, self.phraseLength))
            self._phrases.append(Phrase())
        