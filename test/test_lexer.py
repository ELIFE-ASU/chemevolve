# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import unittest
from chemevolve.Lexer import TokenType

class TestTokenType(unittest.TestCase):
    '''
    Ensure that all is well with the `TokenType`
    '''
    def test_str(self):
        '''
        Check the string representations of the various token types
        '''
        self.assertEqual('NL',       str(TokenType.NL))
        self.assertEqual('LT',       str(TokenType.LT))
        self.assertEqual('GT',       str(TokenType.GT))
        self.assertEqual('EQ',       str(TokenType.EQ))
        self.assertEqual('PLUS',     str(TokenType.PLUS))
        self.assertEqual('MINUS',    str(TokenType.MINUS))
        self.assertEqual('DASH',     str(TokenType.DASH))
        self.assertEqual('ARROW',    str(TokenType.ARROW))
        self.assertEqual('OBRACKET', str(TokenType.OBRACKET))
        self.assertEqual('CBRACKET', str(TokenType.CBRACKET))
        self.assertEqual('OPAREN',   str(TokenType.OPAREN))
        self.assertEqual('CPAREN',   str(TokenType.CPAREN))
        self.assertEqual('COMMA',    str(TokenType.COMMA))
        self.assertEqual('INTEGER',  str(TokenType.INTEGER))
        self.assertEqual('FLOAT',    str(TokenType.FLOAT))
        self.assertEqual('STRING',   str(TokenType.STRING))

    def test_repr(self):
        '''
        Check the representations of the various token types
        '''
        self.assertEqual('TokenType.NL',       repr(TokenType.NL))
        self.assertEqual('TokenType.LT',       repr(TokenType.LT))
        self.assertEqual('TokenType.GT',       repr(TokenType.GT))
        self.assertEqual('TokenType.EQ',       repr(TokenType.EQ))
        self.assertEqual('TokenType.PLUS',     repr(TokenType.PLUS))
        self.assertEqual('TokenType.MINUS',    repr(TokenType.MINUS))
        self.assertEqual('TokenType.DASH',     repr(TokenType.DASH))
        self.assertEqual('TokenType.ARROW',    repr(TokenType.ARROW))
        self.assertEqual('TokenType.OBRACKET', repr(TokenType.OBRACKET))
        self.assertEqual('TokenType.CBRACKET', repr(TokenType.CBRACKET))
        self.assertEqual('TokenType.OPAREN',   repr(TokenType.OPAREN))
        self.assertEqual('TokenType.CPAREN',   repr(TokenType.CPAREN))
        self.assertEqual('TokenType.COMMA',    repr(TokenType.COMMA))
        self.assertEqual('TokenType.INTEGER',  repr(TokenType.INTEGER))
        self.assertEqual('TokenType.FLOAT',    repr(TokenType.FLOAT))
        self.assertEqual('TokenType.STRING',   repr(TokenType.STRING))

