#!/usr/bin/env python

# Written by Robert Curtin

from Note import Note
import unittest


class NoteTest(unittest.TestCase):
    def test_note_length(self):
        a = Note()
        a.addChar('F')
        self.assertEqual(a.getLength(), 1)
        
        a.addChar('3')
        self.assertEqual(a.getLength(), 3)
        
        a.addChar('/')
        self.assertEqual(a.getLength(), 3.0/2.0)
        
        a.addChar('2')
        self.assertEqual(a.getLength(), 3.0/2.0)
        
        b = Note()
        b.addChar('D')
        b.addChar('/')
        self.assertEqual(b.getLength(), 1.0/2.0)
        
if __name__ == '__main__':
    unittest.main()