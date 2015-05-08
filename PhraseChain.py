#!/usr/bin/env python

# Written by Robert Curtin
from Phrase import Phrase
                
# This class represents a chain of phrases, constructed by adding one note
# at a time.
# Be sure to set the phrase length before adding notes to properly group
# phrases.
class PhraseChain:
    def __init__(self, meter, noteLength):
        firstPhrase = Phrase()
        self._phrases = [firstPhrase]
        self.noteLength = noteLength
        self.meter = meter
        
    def getLastPhrase(self):
        return self._phrases[-1]
        
    def isLastNoteBroken(self):
        return self.getLastPhrase().isLastNoteBroken()
        
    def getLastNoteLength(self):
        return self.getLastPhrase().getLastNoteLength()
        
    def addNote(self, note):
        # Carry over leftover note length if the previous note was dotted or
        # halved
        if self.isLastNoteBroken():
            note.setLengthToLeftover(self.getLastNoteLength())
        self.getLastPhrase().addNote(note)
        # Check if the maximum phrase length has been met
        # Todo: Split up notes between phrases if phrase length is too long
        # or ignore phrase entirely
        if self.getLastPhrase().getLength() >= self.meter:
            if self.getLastPhrase().getLength() != self.meter:
                print("Error: Phrase {} with length {} too long for meter {}"
                .format(self.getLastPhrase().getText(), 
                        self.getLastPhrase().getLength(), 
                        self.meter))
                self.getLastPhrase().printNoteInfo()
            self._phrases.append(Phrase())
    