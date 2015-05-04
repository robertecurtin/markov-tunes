#!/usr/bin/env python

# Written by Robert Curtin

import string

def extractDigits(inputString):
    return ''.join([c for c in inputString if c in string.digits])
# This class represents a single note in ABC
class Note:
    def __init__(self):
        self.text = ''
        
    def addChar(self, char):
        self.text += char
        
    def isDotted(self):
        return '>' in self.text 
        
    def isHalved(self):
        return '<' in self.text
       
    def containsNote(self):
        return any(c in self.text for c in 'abcdefgABCDEFGz')

    def getLength(self):
        length = 1
        # Handle dotted rhythms
        if self.isDotted() or self.isHalved():
            if self.isDotted() and self.isHalved():
                print("Multiple modifiers in note {}, this may\
                cause rhythm issues.".format(self.text))
            lengthText = (c for c in self.text if c in '><')
            dottedModifier = 1
            for char in lengthText:
                    dottedModifier /= 1/2
            if self.isDotted():
                length = 1 - dottedModifier
            elif self.isHalved():
                length = dottedModifier
            else:
                print("Error in rhythm modification! < or > was missing for\
                note {}".format(self.text))
            return length

        elif '/' in self.text:
            # Split the text on the bar before continuing
            splitNote = self.text.split('/')
            if len(splitNote) > 2:
                print("Error in rhythm of note {}! Multiple '/' detected."
                .format(self.text))
            # Get all digits in the numerator
            numerator = extractDigits(splitNote[0])
            # Get all digits in the denominator
            denominator = extractDigits(splitNote[1])
            if numerator:
                length *= float(numerator)
            if denominator:
                length /= float(denominator)
            return length
        
        elif any(x in self.text for x in string.digits):
            multiplier = extractDigits(self.text)
            length *= float(multiplier)
            return length
        else:
            return length
            
            