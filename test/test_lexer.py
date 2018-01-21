# -*- coding: utf-8 -*-
# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
import os, unittest
from chemevolve.Lexer import TokenType, Token, LexerError, Lexer

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

    def test_isnewline(self):
        '''
        Ensure that isnewline performs as expected.
        '''
        self.assertTrue(Token(TokenType.NL, '\n').isnewline())
        self.assertFalse(Token(TokenType.LT, '<').isnewline())

    def test_islessthan(self):
        '''
        Ensure that islessthan performs as expected.
        '''
        self.assertTrue(Token(TokenType.LT, '<').islessthan())
        self.assertFalse(Token(TokenType.NL, '\n').islessthan())

    def test_isgreaterthan(self):
        '''
        Ensure that isgreaterthan performs as expected.
        '''
        self.assertTrue(Token(TokenType.GT, '>').isgreaterthan())
        self.assertFalse(Token(TokenType.LT, '<').isgreaterthan())

    def test_isequalto(self):
        '''
        Ensure that isequalto performs as expected.
        '''
        self.assertTrue(Token(TokenType.EQ, '=').isequalto())
        self.assertFalse(Token(TokenType.LT, '<').isequalto())

    def test_isplus(self):
        '''
        Ensure that isplus performs as expected.
        '''
        self.assertTrue(Token(TokenType.PLUS, '+').isplus())
        self.assertFalse(Token(TokenType.EQ, '=').isplus())

    def test_isminus(self):
        '''
        Ensure that isminus performs as expected.
        '''
        self.assertTrue(Token(TokenType.MINUS, '-').isminus())
        self.assertFalse(Token(TokenType.EQ, '=').isminus())

    def test_isdash(self):
        '''
        Ensure that isdash performs as expected.
        '''
        self.assertTrue(Token(TokenType.DASH, '--').isdash())
        self.assertFalse(Token(TokenType.EQ, '=').isdash())

    def test_isarrow(self):
        '''
        Ensure that isarrow performs as expected.
        '''
        self.assertTrue(Token(TokenType.ARROW, '->').isarrow())
        self.assertFalse(Token(TokenType.PLUS, '+').isarrow())

    def test_isobracket(self):
        '''
        Ensure that isobracket performs as expected.
        '''
        self.assertTrue(Token(TokenType.OBRACKET, '[').isobracket())
        self.assertFalse(Token(TokenType.ARROW, '->').isobracket())

    def test_iscbracket(self):
        '''
        Ensure that iscbracket performs as expected.
        '''
        self.assertTrue(Token(TokenType.CBRACKET, ']').iscbracket())
        self.assertFalse(Token(TokenType.OBRACKET, '[').iscbracket())

    def test_isoparen(self):
        '''
        Ensure that isoparen performs as expected.
        '''
        self.assertTrue(Token(TokenType.OPAREN, '(').isoparen())
        self.assertFalse(Token(TokenType.ARROW, '->').isoparen())

    def test_iscparen(self):
        '''
        Ensure that iscparen performs as expected.
        '''
        self.assertTrue(Token(TokenType.CPAREN, ')').iscparen())
        self.assertFalse(Token(TokenType.OPAREN, '(').iscparen())

    def test_iscomma(self):
        '''
        Ensure that iscomma performs as expected.
        '''
        self.assertTrue(Token(TokenType.COMMA, ',').iscomma())
        self.assertFalse(Token(TokenType.CPAREN, ')').iscomma())

    def test_isinteger(self):
        '''
        Ensure that isinteger performs as expected.
        '''
        self.assertTrue(Token(TokenType.INTEGER, '2').isinteger())
        self.assertFalse(Token(TokenType.FLOAT, '2.3').isinteger())

    def test_isfloat(self):
        '''
        Ensure that isfloat performs as expected.
        '''
        self.assertTrue(Token(TokenType.FLOAT, '2.3').isfloat())
        self.assertFalse(Token(TokenType.INTEGER, '2').isfloat())

    def test_isstring(self):
        '''
        Ensure that isstring performs as expected.
        '''
        self.assertTrue(Token(TokenType.STRING, 'apples').isstring())
        self.assertFalse(Token(TokenType.FLOAT, '2.3').isstring())
        self.assertFalse(Token(TokenType.INTEGER, '2').isstring())

class TestLexerError(unittest.TestCase):
    '''
    Ensure that all is well with the `LexerError` class.
    '''
    def test_init(self):
        err = LexerError('message', 'file.txt', 5, 3)
        self.assertEqual('message (file.txt:5:3)', err.args[0])
        self.assertEqual('file.txt', err.filename)
        self.assertEqual(5, err.linenum)
        self.assertEqual(3, err.charnum)

        err = LexerError('message', None, 5, 3)
        self.assertEqual('message (:5:3)', err.args[0])
        self.assertFalse(err.filename)
        self.assertEqual(5, err.linenum)
        self.assertEqual(3, err.charnum)

class TestLexer(unittest.TestCase):
    '''
    Ensure that all is well with the `Lexer` class
    '''
    def assertLexed(self, tokens, s):
        '''
        Create a method for asserting that a string is correctly lexed
        '''
        lexer = Lexer()
        got = lexer.lex(s)
        if isinstance(tokens, list):
            self.assertEqual(tokens, got)
        else:
            self.assertEqual(tokens, got[0])

    def test_init(self):
        '''
        Ensure that the internal state of the `Lexer` is correctly initialized
        '''
        lexer = Lexer()
        self.assertFalse(lexer.filename)
        self.assertEqual(1, lexer.linenum)
        self.assertEqual(0, lexer.charnum)
        self.assertEqual([], lexer.tokens)
        self.assertEqual(None, lexer.token_type)
        self.assertEqual('', lexer.data)

        lexer = Lexer('file.txt')
        self.assertEqual('file.txt', lexer.filename)
        self.assertEqual(1, lexer.linenum)
        self.assertEqual(0, lexer.charnum)
        self.assertEqual([], lexer.tokens)
        self.assertEqual(None, lexer.token_type)
        self.assertEqual('', lexer.data)

    def test_empty(self):
        '''
        Ensure that (most) whitespace is lexed as nothing.
        '''
        self.assertLexed([], '')
        self.assertLexed([], ' ')
        self.assertLexed([], '  ')
        self.assertLexed([], '\r')
        self.assertLexed([], '    ')

    def test_basic_tokens(self):
        '''
        Ensure that we can lex the basic tokens.
        '''
        self.assertLexed(Token(TokenType.NL, '\n'), '\n')
        self.assertLexed(Token(TokenType.LT, '<'), '<')
        self.assertLexed(Token(TokenType.GT, '>'), '>')
        self.assertLexed(Token(TokenType.EQ, '='), '=')
        self.assertLexed(Token(TokenType.PLUS, '+'), '+')
        self.assertLexed(Token(TokenType.MINUS, '-'), '-')
        self.assertLexed(Token(TokenType.DASH, '--'), '--')
        self.assertLexed(Token(TokenType.ARROW, '->'), '->')
        self.assertLexed(Token(TokenType.OBRACKET, '['), '[')
        self.assertLexed(Token(TokenType.CBRACKET, ']'), ']')
        self.assertLexed(Token(TokenType.OPAREN, '('), '(')
        self.assertLexed(Token(TokenType.CPAREN, ')'), ')')
        self.assertLexed(Token(TokenType.COMMA, ','), ',')

    def test_integers(self):
        '''
        Ensure that we can lex the basic integers.
        '''
        self.assertLexed(Token(TokenType.INTEGER, '1'), '1')
        self.assertLexed(Token(TokenType.INTEGER, '10'), '10')

    def test_float(self):
        '''
        Ensure that we can lex the basic floats.
        '''
        self.assertLexed(Token(TokenType.FLOAT, '.1'), '.1')
        self.assertLexed(Token(TokenType.FLOAT, '0.1'), '0.1')
        self.assertLexed(Token(TokenType.FLOAT, '1e2'), '1e2')
        self.assertLexed(Token(TokenType.FLOAT, '1e+2'), '1e+2')
        self.assertLexed(Token(TokenType.FLOAT, '1e-2'), '1e-2')
        self.assertLexed(Token(TokenType.FLOAT, '1E2'), '1E2')
        self.assertLexed(Token(TokenType.FLOAT, '1E+2'), '1E+2')
        self.assertLexed(Token(TokenType.FLOAT, '1E-2'), '1E-2')
        self.assertLexed(Token(TokenType.FLOAT, '1.e2'), '1.e2')
        self.assertLexed(Token(TokenType.FLOAT, '1.e+2'), '1.e+2')
        self.assertLexed(Token(TokenType.FLOAT, '1.e-2'), '1.e-2')
        self.assertLexed(Token(TokenType.FLOAT, '1.E2'), '1.E2')
        self.assertLexed(Token(TokenType.FLOAT, '1.E+2'), '1.E+2')
        self.assertLexed(Token(TokenType.FLOAT, '1.E-2'), '1.E-2')
        self.assertLexed(Token(TokenType.FLOAT, '1.0e2'), '1.0e2')
        self.assertLexed(Token(TokenType.FLOAT, '1.0e+2'), '1.0e+2')
        self.assertLexed(Token(TokenType.FLOAT, '1.0e-2'), '1.0e-2')
        self.assertLexed(Token(TokenType.FLOAT, '1.0E2'), '1.0E2')
        self.assertLexed(Token(TokenType.FLOAT, '1.0E+2'), '1.0E+2')
        self.assertLexed(Token(TokenType.FLOAT, '1.0E-2'), '1.0E-2')

    def test_string(self):
        '''
        Ensure that we can lex strings.
        '''
        self.assertLexed(Token(TokenType.STRING, 'apple'), 'apple')
        self.assertLexed(Token(TokenType.STRING, 'meta-data'), 'meta-data')
        self.assertLexed(Token(TokenType.STRING, 'meta.data'), 'meta.data')
        self.assertLexed(Token(TokenType.STRING, 'AABBA'), 'AABBA')

    def test_invalid_numeric(self):
        '''
        Raise an error if an invalid numeric value is encountered
        '''
        with self.assertRaises(LexerError):
            Lexer().lex('1t')
        with self.assertRaises(LexerError):
            Lexer().lex('.1t')
        with self.assertRaises(LexerError):
            Lexer().lex('.')
        with self.assertRaises(LexerError):
            Lexer().lex('.+')
        with self.assertRaises(LexerError):
            Lexer().lex('.-')
        with self.assertRaises(LexerError):
            Lexer().lex('1.1t')
        with self.assertRaises(LexerError):
            Lexer().lex('1.1e')
        with self.assertRaises(LexerError):
            Lexer().lex('1e.')
        with self.assertRaises(LexerError):
            Lexer().lex('1e+.')
        with self.assertRaises(LexerError):
            Lexer().lex('.e+.')

    def test_compound_statements(self):
        '''
        Ensure that compound statements are lexed as expected.
        '''
        self.assertLexed([Token(TokenType.LT,'<'),
                          Token(TokenType.STRING,'meta-data'),
                          Token(TokenType.GT,'>'),
                          Token(TokenType.NL,'\n'),
                          Token(TokenType.NL,'\n')],
                          '< meta-data >\n\n')
        self.assertLexed([Token(TokenType.LT,'<'),
                          Token(TokenType.DASH,'--')],
                          '<--')
        self.assertLexed([Token(TokenType.LT,'<'),
                          Token(TokenType.DASH,'--'),
                          Token(TokenType.GT,'>')],
                          '<-->')
        self.assertLexed([Token(TokenType.LT,'<'),
                          Token(TokenType.ARROW,'->')],
                          '<->')
        self.assertLexed([Token(TokenType.OBRACKET,'['),
                          Token(TokenType.INTEGER,'12'),
                          Token(TokenType.CBRACKET,']'),
                          Token(TokenType.STRING,'AABA')],
                          '[12] AABA')

        reaction = [Token(TokenType.OBRACKET,'['),
                    Token(TokenType.INTEGER,'3'),
                    Token(TokenType.CBRACKET,']'),
                    Token(TokenType.OBRACKET,'['),
                    Token(TokenType.STRING,'AA'),
                    Token(TokenType.CBRACKET,']'),
                    Token(TokenType.PLUS,'+'),
                    Token(TokenType.INTEGER,'2'),
                    Token(TokenType.OBRACKET,'['),
                    Token(TokenType.STRING,'AB'),
                    Token(TokenType.CBRACKET,']'),
                    Token(TokenType.DASH,'--'),
                    Token(TokenType.FLOAT,'1.e-1'),
                    Token(TokenType.ARROW,'->'),
                    Token(TokenType.OBRACKET,'['),
                    Token(TokenType.STRING,'ABAAAB'),
                    Token(TokenType.CBRACKET,']'),
                    Token(TokenType.STRING, 'STD'),
                    Token(TokenType.OPAREN,'('),
                    Token(TokenType.FLOAT,'1E2'),
                    Token(TokenType.OBRACKET,'['),
                    Token(TokenType.STRING,'ABA'),
                    Token(TokenType.CBRACKET,']'),
                    Token(TokenType.COMMA,','),
                    Token(TokenType.OBRACKET,'['),
                    Token(TokenType.STRING,'BAB'),
                    Token(TokenType.CBRACKET,']'),
                    Token(TokenType.CPAREN,')'),
                    Token(TokenType.NL,'\n')]
        self.assertLexed(reaction,
             '[3][AA]+2[AB]--1.e-1->[ABAAAB]STD(1E2[ABA],[BAB])\n')
        self.assertLexed(reaction,
             '[3] [AA] + 2[AB] -- 1.e-1 -> [ABAAAB] STD (1E2[ABA], [BAB])\n')

    def test_lex_override_filename(self):
        '''
        Ensure that the `Lexer` properly handles the filename overrides when
        `lex` is called.
        '''
        lexer = Lexer('<no-filename>')
        lexer.lex('apples')
        self.assertEqual('<no-filename>', lexer.filename)
        lexer.lex('bananas', filename='<hardcoded>')
        self.assertEqual('<hardcoded>', lexer.filename)

        lexer = Lexer('<no-filename>')
        lexer.lex('apples', reset=False)
        self.assertEqual('<no-filename>', lexer.filename)
        lexer.lex('bananas', filename='<hardcoded>', reset=False)
        self.assertEqual('<hardcoded>', lexer.filename)


    def test_lex_unicode(self):
        '''
        Ensure that we can properly lex (most) unicode (UTF-8) characters.
        '''
        self.assertLexed(Token(TokenType.STRING, u'α'), u'α')
        self.assertLexed([Token(TokenType.OBRACKET, u'['),
                          Token(TokenType.STRING, u'αβ-apple'),
                          Token(TokenType.CBRACKET, u']')],
                          u'[αβ-apple]')

        self.assertLexed(Token(TokenType.STRING, u'α'), 'α')
        self.assertLexed([Token(TokenType.OBRACKET, u'['),
                          Token(TokenType.STRING, u'αβ-apple'),
                          Token(TokenType.CBRACKET, u']')],
                          '[αβ-apple]')

    def test_configs_from_string(self):
        '''
        Ensure that the configuration files in configs/lexer/valid all lex
        without error while those in configs/lexer/invalid do not.
        '''
        valid = 'test/configs/lexer/valid'
        for filename in os.listdir(valid):
            with open(os.path.join(valid, filename)) as f:
                expect = int(os.path.splitext(filename)[0])
                tokens = Lexer().lex(f.read())
                self.assertEqual(expect, len(tokens))

        invalid = 'test/configs/lexer/invalid'
        for filename in os.listdir(invalid):
            with open(os.path.join(invalid, filename)) as f:
                with self.assertRaises(LexerError):
                    Lexer().lex(f.read())

    def test_lex_file(self):
        '''
        Ensure that the configuration files in configs/lexer/valid all lex
        without error and produce the same sequence of tokens when using
        `lex_file` as when using `lex`. Ensure that files in
        configs/lexer/invalid raise errors.
        '''
        valid = 'test/configs/lexer/valid'
        for filename in os.listdir(valid):
            path = os.path.join(valid, filename)
            lexer = Lexer()
            with open(path) as f:
                expected = lexer.lex(f.read(), reset=True)

            # Lex the file from a file handle
            with open(path) as f:
                got = lexer.lex_file(f, reset=True)
            self.assertEqual(expected, got)

            # Lex the file from a filename
            got = lexer.lex_file(path, reset=True)
            self.assertEqual(expected, got)


        invalid = 'test/configs/lexer/invalid'
        for filename in os.listdir(invalid):
            path = os.path.join(invalid, filename)
            with open(path) as f:
                with self.assertRaises(LexerError):
                    Lexer().lex_file(f)
            with self.assertRaises(LexerError):
                Lexer().lex_file(path)

