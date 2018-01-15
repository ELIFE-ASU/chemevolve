# -*- coding: utf-8 -*-
# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import unittest
from chemevolve.Parser import ParserError

class TestParserError(unittest.TestCase):
    '''
    Ensure that all is well with the `ParserError` class.
    '''
    def test_init_(self):
        err = ParserError('message', 'file.txt', 5)
        self.assertEqual('message (file.txt:5)', err.args[0])
        self.assertEqual('file.txt', err.filename)
        self.assertEqual(5, err.linenum)

        err = ParserError('message', None, 5)
        self.assertEqual('message (:5)', err.args[0])
        self.assertFalse(err.filename)
        self.assertEqual(5, err.linenum)

