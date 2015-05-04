#!/usr/bin/env python

# Written by Robert Curtin

import string

def extractDigits(inputString):
    return ''.join([c for c in inputString.strip() if c in string.digits])
# This class represents a single note in ABC
class Note:
    def __init__(self, baseLength):
        self.text = ''
        self._overwriteLength = False
        self._length = 1
        self.baseLength = baseLength
        
    def __str__(self):
        output = 'Text: "{}\n'.format(self.text)
        output += 'Overwrite Length: {}\n'.format(self._overwriteLength)
        output += 'Length: {}\n'.format(self._length)
        output += 'Base length: {}\n'.format(self.baseLength)
        return output
    def addChar(self, char):
        # Do not mark any characters after the bar (repeat numbers, etc)
        if '|' not in self.text:
            self.text += char
        
    def isDotted(self):
        return '>' in self.text 
        
    def isHalved(self):
        return '<' in self.text
       
    def containsNote(self):
        return any(c in self.text for c in 'abcdefgABCDEFGz')

    def setLength(self, length):
        self._length = length
        self._overwriteLength = True
        
    def setLengthToLeftover(self, prevLength):
        # Sets length to the remainder from a previous dotted or halved
        # note
        self._length = 2 * self.baseLength - prevLength
        self._overwriteLength = True

    def getLength(self):
        # If the previous note was dotted, the length will be overwritten
        if not self._overwriteLength:
                
            self._length = self.baseLength
            # Handle dotted rhythms
            if self.isDotted() or self.isHalved():
                if self.isDotted() and self.isHalved():
                    print("Multiple modifiers in note {}, this may\
                    cause rhythm issues.".format(self.text))
                lengthText = (c for c in self.text if c in '><')
                dottedModifier = 1.0
                for char in lengthText:
                    dottedModifier /= 2.0
                if self.isDotted():
                    self._length *= (2 - dottedModifier)
                elif self.isHalved():
                    self._length *= dottedModifier
                else:
                    print("Error in rhythm modification! < or > was missing for\
                    note {}".format(self.text))
    
            # Handle fractional modifiers
            elif '/' in self.text:
                # Split the text on the bar before continuing
                splitNote = self.text.split('/')
                if len(splitNote) > 2:
                    print("Warning in rhythm of note {}! Multiple '/' detected."
                    .format(self.text))
                # Get all digits in the numerator
                numerator = extractDigits(splitNote[0])
                # Get all digits in the denominator
                denominator = extractDigits(splitNote[1])
                if numerator:
                    self._length *= float(numerator)
                if denominator:
                    self._length /= float(denominator)
                # / is shorthand for 1/2, // for 1/4, 3/ for 3/2, etc.
                else:
                    for slashes in range(self.text.count('/')):
                        self._length /= 2.0
            
            elif any(x in self.text for x in string.digits):
                multiplier = extractDigits(self.text)
                self._length *= float(multiplier)
        if self._length == 0:
            print("Warning: 0-length note {}!".format(self.text))
        return self._length
        