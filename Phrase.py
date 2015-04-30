#!/usr/bin/env python

# Written by Robert Curtin

from random import randint

class Phrase:
    def __init__(self):
        self.notes = ''
        self.tunes = []     # All tunes that contain this phrase
        self.tuneType = ''
        self._linkedPhrases = {} # All phrases that come after this one
    
    def setNotes(self, notes):        
        if self.notes != '' and self.notes != notes:
            print("Warning: Phrase {} is being overwritten by {}!"\
            .format(self.notes, notes))
        # Todo: Convert individual notes to intervals
        self.notes = notes
    
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