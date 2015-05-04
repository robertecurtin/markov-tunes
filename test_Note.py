#!/usr/bin/env python

# Written by Robert Curtin

from Note import Note
import unittest


class NoteTest(unittest.TestCase):
    def test_note_length(self):
        baseNoteLength = 1.0/8.0
        testBasic = Note(baseNoteLength)
        testBasic.addChar('F')
        self.assertEqual(testBasic.getLength(), 1 * baseNoteLength)
        
        testBasic.addChar('3')
        self.assertEqual(testBasic.getLength(), 3 * baseNoteLength)
        
        testBasic.addChar('/')
        self.assertEqual(testBasic.getLength(), 3.0/2.0 * baseNoteLength)
        
        testBasic.addChar('2')
        self.assertEqual(testBasic.getLength(), 3.0/2.0 * baseNoteLength)
        
        numberlessFraction = Note(baseNoteLength)
        numberlessFraction.addChar('D')
        numberlessFraction.addChar('/')
        self.assertEqual(numberlessFraction.getLength(), 
                         1.0/2.0 * baseNoteLength)
        numberlessFraction.addChar('/')
        self.assertEqual(numberlessFraction.getLength(), 
                         1.0/4.0 * baseNoteLength)
        
        testDotted = Note(baseNoteLength)
        testDotted.addChar('=')
        testDotted.addChar('c')
        testDotted.addChar('>')
        testDotted.addChar('!')
        self.assertTrue(testDotted.isDotted())
        self.assertFalse(testDotted.isHalved())
        self.assertEqual(testDotted.getLength(),
                         1.5 * baseNoteLength)
        
        
if __name__ == '__main__':
    unittest.main()