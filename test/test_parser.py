# -*- coding: utf-8 -*-
# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import unittest
from chemevolve.Parser import ParserError, ParserPhase, Parser

class TestParserError(unittest.TestCase):
    '''
    Ensure that all is well with the `ParserError` class.
    '''
    def test_init(self):
        err = ParserError('message', 'file.txt', 5)
        self.assertEqual('message (file.txt:5)', err.args[0])
        self.assertEqual('file.txt', err.filename)
        self.assertEqual(5, err.linenum)

        err = ParserError('message', None, 5)
        self.assertEqual('message (:5)', err.args[0])
        self.assertFalse(err.filename)
        self.assertEqual(5, err.linenum)

class TestParser(unittest.TestCase):
    '''
    Ensure that all is well with the `Parser` class.
    '''
    def test_init(self):
        '''
        Ensure that the `Parser` is correctly initialized
        '''
        p = Parser()
        self.assertFalse(p.filename)
        self.assertEqual(1, p.linenum)
        self.assertEqual(ParserPhase.START, p.phase)

        p = Parser('file.txt')
        self.assertEqual('file.txt', p.filename)
        self.assertEqual(1, p.linenum)
        self.assertEqual(ParserPhase.START, p.phase)

    def test_parse_empty(self):
        '''
        The first parse should return None if the text is empty or only contains
        spaces.
        '''
        self.assertFalse(Parser().parse(''))
        self.assertFalse(Parser().parse(' '))
        self.assertFalse(Parser().parse(' \t'))
        self.assertFalse(Parser().parse(' \n\t '))
