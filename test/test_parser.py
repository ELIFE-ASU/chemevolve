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

    def test_parse_metadata_first(self):
        '''
        Ensure that the first thing parsed is meta-data.
        '''
        with self.assertRaises(ParserError):
            Parser().parse('=')

        with self.assertRaises(ParserError):
            Parser().parse('[0] AAA')

        with self.assertRaises(ParserError):
            Parser().parse('<molecules>')

        with self.assertRaises(ParserError):
            Parser().parse('[2] 2[A] -- 1.0 -> [AA]')

    def test_parse_metadata_fail(self):
        '''
        Ensure that invalid meta-data sections fail to parse
        '''
        with self.assertRaises(ParserError):
            # No nrMolecules, no nrReactions keys
            Parser().parse('<meta-data>')

        with self.assertRaises(ParserError):
            # No nrMolecules, no nrReactions keys
            Parser().parse('<meta-data> apple=10')

        with self.assertRaises(ParserError):
            # Invalid key type
            Parser().parse('<meta-data>\n5 = apples')

        with self.assertRaises(ParserError):
            # Invalid value type
            Parser().parse('<meta-data>\napples = [3]')

        with self.assertRaises(ParserError):
            # Invalid type for nrMolecules
            Parser().parse('<meta-data> nrMolecules = string nrReactions = 10')

    def test_parse_metadata(self):
        '''
        Ensure that the meta-data section parses and stores correctly
        '''
        p = Parser()

        p.parse('<meta-data> nrMolecules = 2 nrReactions = 10')
        self.assertEqual( 2, p.metadata['nrMolecules'])
        self.assertEqual(10, p.metadata['nrReactions'])
        self.assertEqual( 2, len(p.metadata))
        self.assertEqual( 2, len(p.molecule_list))
        self.assertEqual( 0, len(p.molecule_dict))
        self.assertEqual(10, len(p.reaction_list))

        p.parse('<meta-data> nrMolecules = 2 nrReactions = 8')
        self.assertEqual(2, p.metadata['nrMolecules'])
        self.assertEqual(8, p.metadata['nrReactions'])
        self.assertEqual(2, len(p.metadata))
        self.assertEqual(2, len(p.molecule_list))
        self.assertEqual(0, len(p.molecule_dict))
        self.assertEqual(8, len(p.reaction_list))

        p.parse('<meta-data> nrMolecules = 2 nrReactions = 100 nrMolecules = 3')
        self.assertEqual(  3, p.metadata['nrMolecules'])
        self.assertEqual(100, p.metadata['nrReactions'])
        self.assertEqual(  2, len(p.metadata))
        self.assertEqual(  3, len(p.molecule_list))
        self.assertEqual(  0, len(p.molecule_dict))
        self.assertEqual(100, len(p.reaction_list))

        p.parse('<meta-data> nrMolecules = 10 nrReactions = 100 apples = fruit')
        self.assertEqual( 10, p.metadata['nrMolecules'])
        self.assertEqual(100, p.metadata['nrReactions'])
        self.assertEqual('fruit', p.metadata['apples'])
        self.assertEqual(  3, len(p.metadata))
        self.assertEqual( 10, len(p.molecule_list))
        self.assertEqual(  0, len(p.molecule_dict))
        self.assertEqual(100, len(p.reaction_list))

    def test_parse_reset(self):
        '''
        Ensure that parse resets at the beginning of each parse.
        '''
        p = Parser()

        p.parse('<meta-data> nrMolecules = 2 nrReactions = 10 apple = 5')
        self.assertEqual( 2, p.metadata['nrMolecules'])
        self.assertEqual(10, p.metadata['nrReactions'])
        self.assertEqual( 5, p.metadata['apple'])
        self.assertEqual(3, len(p.metadata))

        p.parse('<meta-data> nrMolecules = 1 nrReactions = 8', reset=False)
        self.assertEqual(1, p.metadata['nrMolecules'])
        self.assertEqual(8, p.metadata['nrReactions'])
        self.assertEqual(5, p.metadata['apple'])
        self.assertEqual(3, len(p.metadata))

        p.parse('<meta-data> nrMolecules = 10 nrReactions = 100')
        self.assertEqual( 10, p.metadata['nrMolecules'])
        self.assertEqual(100, p.metadata['nrReactions'])
        self.assertEqual(2, len(p.metadata))
