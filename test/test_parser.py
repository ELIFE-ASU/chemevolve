# -*- coding: utf-8 -*-
# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import unittest, os
from chemevolve.Parser import ParserError, ParserPhase, Parser
from chemevolve.CoreClasses import Reaction

class TestParserError(unittest.TestCase):
    '''
    Ensure that all is well with the `ParserError` class.
    '''
    def test_init(self):
        err = ParserError('message', 'file.txt', 5)
        self.assertEqual('message (file.txt:5)', err.args[0])
        self.assertEqual('message', err.message)
        self.assertEqual('file.txt', err.filename)
        self.assertEqual(5, err.linenum)

        err = ParserError('message', None, 5)
        self.assertEqual('message (:5)', err.args[0])
        self.assertEqual('message', err.message)
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

        p.parse('''<meta-data>
                   nrMolecules = 4
                   nrReactions = 4
                   <molecules>
                   [0] A
                   [1] AA
                   [2] B
                   [3] AB
                   <reactions>
                   [0] 2[A] -- 1.0 -> [AA] STD
                   [1] [A] + [B] -- 0.5 -> [AB] QED
                   [2] [AA] -- 1.5 -> 2[A] STD (2.3[AA])
                   [3] [AB] -- 2.5e-1 -> [A] + 1[B] STD (1e-3[A],1e-2[B])''')
        self.assertEqual(2, len(p.metadata))
        self.assertEqual(4, p.metadata['nrMolecules'])
        self.assertEqual(4, p.metadata['nrReactions'])
        self.assertEqual(['A','AA','B','AB'], p.molecule_list)
        self.assertEqual({'A':0, 'AA':1, 'B':2, 'AB': 3}, p.molecule_dict)
        self.assertEqual(4, len(p.reaction_list))

        reactions = [
                Reaction(0, [0], [2], [1], [1], 1.0, [], [], 'STD'),
                Reaction(1, [0,2], [1,1], [3], [1], 0.5, [], [], 'QED'),
                Reaction(2, [1], [1], [0], [2], 1.5, [1], [2.3], 'STD'),
                Reaction(3, [3], [1], [0,2], [1,1], 0.25, [0,2], [1e-3,1e-2], 'STD')
                ]

        for expect, got in zip(reactions, p.reaction_list):
            self.assertEqual(expect.ID, got.ID)
            self.assertEqual(expect.reactants, got.reactants)
            self.assertEqual(expect.reactant_coeff, got.reactant_coeff)
            self.assertEqual(expect.products, got.products)
            self.assertEqual(expect.product_coeff, got.product_coeff)
            self.assertEqual(expect.catalysts, got.catalysts)
            self.assertEqual(expect.catalyzed_constants, got.catalyzed_constants)
            self.assertEqual(expect.constant, got.constant)
            self.assertEqual(expect.prop, got.prop)

    def test_configs_from_string(self):
        '''
        Ensure that the configuration files in configs/parser/valid all parse
        without error while those in configs/parser/invalid do not.
        '''
        valid = 'test/configs/parser/valid'
        for filename in os.listdir(valid):
            with open(os.path.join(valid, filename), 'rb') as f:
                crs = Parser().parse(f.read())
                self.assertTrue(crs)

        invalid = 'test/configs/parser/invalid'
        for filename in os.listdir(invalid):
            with open(os.path.join(invalid, filename), 'rb') as f:
                with self.assertRaises(Exception):
                    Parser().parse(f.read())

    def test_parse_file(self):
        '''
        Ensure that the configuration files in configs/parse/valid all parse
        without error and produce the same CRS when using `parse_file` as when
        using `parse`. Ensure that files in configs/parse/invalid raise errors.
        '''
        valid = 'test/configs/parser/valid'
        for filename in os.listdir(valid):
            path = os.path.join(valid, filename)
            parser = Parser()
            with open(path, 'rb') as f:
                expected = parser.parse(f.read())

            # Parse the file from a file handle
            with open(path, 'rb') as f:
                got = parser.parse_file(f)
            self.assertEqual(expected, got)

            # Parse the file from a filename
            got = parser.parse_file(path)
            self.assertEqual(expected, got)


        invalid = 'test/configs/parser/invalid'
        for filename in os.listdir(invalid):
            path = os.path.join(invalid, filename)
            with open(path, 'rb') as f:
                with self.assertRaises(Exception):
                    Parser().parse_file(f)
            with self.assertRaises(Exception):
                Parser().parse_file(path)

