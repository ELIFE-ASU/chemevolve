# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import unittest
from chemevolve.Lexer import TokenType, Token

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

class TestToken(unittest.TestCase):
    '''
    Ensure that all is well with the `Token` class.
    '''
    def test_invalid_args(self):
        '''
        Token should be constructed from a TokenType and a string.
        '''
        with self.assertRaises(TypeError):
            Token(0, '\n')
        with self.assertRaises(TypeError):
            Token(TokenType.NL, 5)

        Token(TokenType.NL, '\n')

    def test_convert_integer(self):
        '''
        Ensure that tokens with integer type can be properly converted to python
        integers.
        '''
        with self.assertRaises(ValueError):
            Token(TokenType.INTEGER, '').convert()

        with self.assertRaises(ValueError):
            Token(TokenType.INTEGER, '1.0').convert()

        with self.assertRaises(ValueError):
            Token(TokenType.INTEGER, 'a').convert()

        self.assertEqual(1, Token(TokenType.INTEGER, '1').convert())
        self.assertEqual(1, Token(TokenType.INTEGER, '+1').convert())
        self.assertEqual(-1, Token(TokenType.INTEGER, '-1').convert())

    def test_convert_float(self):
        '''
        Ensure that tokens with float type can be properly converted to python
        floats.
        '''
        with self.assertRaises(ValueError):
            Token(TokenType.FLOAT, '').convert()

        with self.assertRaises(ValueError):
            Token(TokenType.FLOAT, 'a').convert()

        self.assertEqual(1.0, Token(TokenType.FLOAT, '1').convert())
        self.assertEqual(1.0, Token(TokenType.FLOAT, '+1').convert())
        self.assertEqual(-1.0, Token(TokenType.FLOAT, '-1').convert())

        self.assertEqual(100.0, Token(TokenType.FLOAT, '1e2').convert())
        self.assertEqual(100.0, Token(TokenType.FLOAT, '+1e2').convert())
        self.assertEqual(-100.0, Token(TokenType.FLOAT, '-1e2').convert())

        self.assertEqual(100.0, Token(TokenType.FLOAT, '1e+2').convert())
        self.assertEqual(100.0, Token(TokenType.FLOAT, '+1e+2').convert())
        self.assertEqual(-100.0, Token(TokenType.FLOAT, '-1e+2').convert())

        self.assertEqual(0.01, Token(TokenType.FLOAT, '1e-2').convert())
        self.assertEqual(0.01, Token(TokenType.FLOAT, '+1e-2').convert())
        self.assertEqual(-0.01, Token(TokenType.FLOAT, '-1e-2').convert())

    def test_convert_others(self):
        '''
        Ensure that all stringy token types can be converted to strings.
        '''
        self.assertEqual('\n', Token(TokenType.NL, '\n').convert())
        self.assertEqual('<',  Token(TokenType.LT, '<').convert())
        self.assertEqual('>',  Token(TokenType.GT, '>').convert())
        self.assertEqual('=',  Token(TokenType.EQ, '=').convert())
        self.assertEqual('+',  Token(TokenType.PLUS, '+').convert())
        self.assertEqual('-',  Token(TokenType.MINUS, '-').convert())
        self.assertEqual('--', Token(TokenType.DASH, '--').convert())
        self.assertEqual('->', Token(TokenType.ARROW, '->').convert())
        self.assertEqual('[',  Token(TokenType.OBRACKET, '[').convert())
        self.assertEqual(']',  Token(TokenType.CBRACKET, ']').convert())
        self.assertEqual('(',  Token(TokenType.OPAREN, '(').convert())
        self.assertEqual(')',  Token(TokenType.CPAREN, ')').convert())
        self.assertEqual(',',  Token(TokenType.COMMA, ',').convert())

        self.assertEqual('', Token(TokenType.STRING, '').convert())
        self.assertEqual('apple', Token(TokenType.STRING, 'apple').convert())
        self.assertEqual('+', Token(TokenType.STRING, '+').convert())

    def test_validate_fails(self):
        '''
        Ensure that validate raises a `ValueError` when the token's data has
        an invalid value.
        '''
        with self.assertRaises(ValueError):
            Token(TokenType.NL, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.LT, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.GT, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.EQ, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.PLUS, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.MINUS, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.DASH, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.ARROW, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.OBRACKET, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.CBRACKET, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.OPAREN, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.CPAREN, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.COMMA, '').validate()

        with self.assertRaises(ValueError):
            Token(TokenType.INTEGER, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.INTEGER, '1.0').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.INTEGER, 'a').validate()

        with self.assertRaises(ValueError):
            Token(TokenType.FLOAT, '').validate()
        with self.assertRaises(ValueError):
            Token(TokenType.FLOAT, 'a').validate()

    def test_validate(self):
        '''
        Ensure that validate does not raise a `ValueError` when the token's
        data is valid.
        '''
        Token(TokenType.NL, '\n').validate()
        Token(TokenType.LT, '<').validate()
        Token(TokenType.GT, '>').validate()
        Token(TokenType.EQ, '=').validate()
        Token(TokenType.PLUS, '+').validate()
        Token(TokenType.MINUS, '-').validate()
        Token(TokenType.DASH, '--').validate()
        Token(TokenType.ARROW, '->').validate()
        Token(TokenType.OBRACKET, '[').validate()
        Token(TokenType.CBRACKET, ']').validate()
        Token(TokenType.OPAREN, '(').validate()
        Token(TokenType.CPAREN, ')').validate()
        Token(TokenType.COMMA, ',').validate()

        Token(TokenType.INTEGER, '1').validate()
        Token(TokenType.INTEGER, '+1').validate()
        Token(TokenType.INTEGER, '-1').validate()

        Token(TokenType.FLOAT, '1').validate()
        Token(TokenType.FLOAT, '+1').validate()
        Token(TokenType.FLOAT, '-1').validate()

        Token(TokenType.FLOAT, '1e2').validate()
        Token(TokenType.FLOAT, '+1e2').validate()
        Token(TokenType.FLOAT, '-1e2').validate()

        Token(TokenType.FLOAT, '1e+2').validate()
        Token(TokenType.FLOAT, '+1e+2').validate()
        Token(TokenType.FLOAT, '-1e+2').validate()

        Token(TokenType.FLOAT, '1e-2').validate()
        Token(TokenType.FLOAT, '+1e-2').validate()
        Token(TokenType.FLOAT, '-1e-2').validate()

        Token(TokenType.STRING, '').validate()
        Token(TokenType.STRING, '1').validate()
        Token(TokenType.STRING, 'a').validate()
        Token(TokenType.STRING, 'apple').validate()
        Token(TokenType.STRING, '-1.0e-3').validate()

    def test_str(self):
        '''
        Ensure that the __str__ method returns a properly formatted,
        human-readable string.
        '''
        self.assertEqual('(NL, \'\\n\')', str(Token(TokenType.NL, '\n')))
        self.assertEqual('(LT, \'<\')', str(Token(TokenType.LT, '<')))
        self.assertEqual('(GT, \'>\')', str(Token(TokenType.GT, '>')))
        self.assertEqual('(EQ, \'=\')', str(Token(TokenType.EQ, '=')))
        self.assertEqual('(PLUS, \'+\')', str(Token(TokenType.PLUS, '+')))
        self.assertEqual('(MINUS, \'-\')', str(Token(TokenType.MINUS, '-')))
        self.assertEqual('(DASH, \'--\')', str(Token(TokenType.DASH, '--')))
        self.assertEqual('(ARROW, \'->\')', str(Token(TokenType.ARROW, '->')))
        self.assertEqual('(OBRACKET, \'[\')', str(Token(TokenType.OBRACKET, '[')))
        self.assertEqual('(CBRACKET, \']\')', str(Token(TokenType.CBRACKET, ']')))
        self.assertEqual('(OPAREN, \'(\')', str(Token(TokenType.OPAREN, '(')))
        self.assertEqual('(CPAREN, \')\')', str(Token(TokenType.CPAREN, ')')))
        self.assertEqual('(COMMA, \',\')', str(Token(TokenType.COMMA, ',')))

        self.assertEqual('(INTEGER, \'1\')', str(Token(TokenType.INTEGER, '1')))
        self.assertEqual('(INTEGER, \'+1\')', str(Token(TokenType.INTEGER, '+1')))
        self.assertEqual('(INTEGER, \'-1\')', str(Token(TokenType.INTEGER, '-1')))

        self.assertEqual('(FLOAT, \'1e2\')', str(Token(TokenType.FLOAT, '1e2')))
        self.assertEqual('(FLOAT, \'+1e2\')', str(Token(TokenType.FLOAT, '+1e2')))
        self.assertEqual('(FLOAT, \'-1e2\')', str(Token(TokenType.FLOAT, '-1e2')))

        self.assertEqual('(STRING, \'\')', str(Token(TokenType.STRING, '')))
        self.assertEqual('(STRING, \'+\')', str(Token(TokenType.STRING, '+')))
        self.assertEqual('(STRING, \'apple\')', str(Token(TokenType.STRING, 'apple')))

    def test_repr(self):
        '''
        Ensure that the __repr__ method returns a python-evaluable string.
        '''
        def check_repr(token):
            got = eval(repr(token))
            self.assertEqual(token.type, got.type)
            self.assertEqual(token.data, got.data)

        check_repr(Token(TokenType.NL, '\n'))
        check_repr(Token(TokenType.LT, '<'))
        check_repr(Token(TokenType.GT, '>'))
        check_repr(Token(TokenType.EQ, '='))
        check_repr(Token(TokenType.PLUS, '+'))
        check_repr(Token(TokenType.MINUS, '-'))
        check_repr(Token(TokenType.DASH, '--'))
        check_repr(Token(TokenType.ARROW, '->'))
        check_repr(Token(TokenType.OBRACKET, '['))
        check_repr(Token(TokenType.CBRACKET, ']'))
        check_repr(Token(TokenType.OPAREN, '('))
        check_repr(Token(TokenType.CPAREN, ')'))
        check_repr(Token(TokenType.COMMA, ','))

        check_repr(Token(TokenType.INTEGER, '1'))
        check_repr(Token(TokenType.INTEGER, '+1'))
        check_repr(Token(TokenType.INTEGER, '-1'))

        check_repr(Token(TokenType.FLOAT, '1e2'))
        check_repr(Token(TokenType.FLOAT, '+1e2'))
        check_repr(Token(TokenType.FLOAT, '-1e2'))

        check_repr(Token(TokenType.STRING, ''))
        check_repr(Token(TokenType.STRING, '+'))
        check_repr(Token(TokenType.STRING, 'apple'))
