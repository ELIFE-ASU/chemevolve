'''
Provide a Lexer class and support classes (e.g. TokenType and Token) for lexing
(tokenizing) ChemEvolve configuration files.
'''
from enum import Enum

class TokenType(Enum):
    '''
    The `TokenType` enumeration provides a type to represent the various kinds
    of tokens that may be observed in a ChemEvole configuration file.
    '''
    NL       = 0  # Newline
    LT       = 1  # Less-than (<)
    GT       = 2  # Greater-than (>)
    EQ       = 3  # Equal-to (=)
    PLUS     = 4  # Plus-sign (+)
    MINUS    = 5  # Minus-sign (-)
    DASH     = 6  # Dash (--)
    ARROW    = 7  # Arrow (->)
    OBRACKET = 8  # Open bracket ([)
    CBRACKET = 9  # Close bracket (])
    OPAREN   = 10 # Open parentheses [(]
    CPAREN   = 11 # Close parentheses [)]
    COMMA    = 12 # Comma (,)
    INTEGER  = 13 # An integer
    FLOAT    = 14 # A floating-point number
    STRING   = 15 # A generic alpha-numeric string, starts with letter

    def __str__(self):
        '''
        Convert a `TokenType` instance into a human-readable string.
        '''
        return self.name

    def __repr__(self):
        '''
        Create a python-evaluable string representation of a `TokenType`.
        '''
        return 'TokenType.{}'.format(self.name)

class Token(object):
    '''
    The `Token` class provides basic 
    '''
    def __init__(self, type, data):
        '''
        Initialize a token from a `TokenType` and the lexed string
        '''
        if not isinstance(type, TokenType):
            raise TypeError('type argument must be a TokenType')
        elif not isinstance(data, str):
            raise TypeError('data argument must be a string')

        self.type = type
        self.data = data

    def convert(self):
        '''
        Convert a token to a python value appropriate for it's `TokenType`.
        '''
        if self.type == TokenType.INTEGER:
            return int(self.data)
        elif self.type == TokenType.FLOAT:
            return float(self.data)
        else:
            return self.data

    def validate(self):
        '''
        Raise a `ValueError` if the data is incompatible with the `TokenType`.
        '''
        def guard(expect, msg=None):
            if self.data == expect:
                pass
            else:
                if msg:
                    msg = '{}, found {}'.format(msg, repr(self.data))
                else:
                    msg = 'expected {}, found {}'.format(repr(expect), repr(self.data))
                raise ValueError(msg)

        if self.type == TokenType.NL:
            guard('\n')
        elif self.type == TokenType.LT:
            guard('<')
        elif self.type == TokenType.GT:
            guard('>')
        elif self.type == TokenType.EQ:
            guard('=')
        elif self.type == TokenType.PLUS:
            guard('+')
        elif self.type == TokenType.MINUS:
            guard('-')
        elif self.type == TokenType.DASH:
            guard('--')
        elif self.type == TokenType.ARROW:
            guard('->')
        elif self.type == TokenType.OBRACKET:
            guard('[')
        elif self.type == TokenType.CBRACKET:
            guard(']')
        elif self.type == TokenType.OPAREN:
            guard('(')
        elif self.type == TokenType.CPAREN:
            guard(')')
        elif self.type == TokenType.COMMA:
            guard(',')
        elif self.type == TokenType.INTEGER:
            try:
                self.convert()
            except ValueError:
                guard(None, 'expected an integer value')
        elif self.type == TokenType.FLOAT:
            try:
                self.convert()
            except ValueError:
                guard(None, 'expected a floating-point value')
        elif self.type == TokenType.STRING:
            pass
        else:
            raise ValueError('unexpected type/data combination encountered')

    def __str__(self):
        '''
        Convert a `Token` into a human-readable string.
        '''
        return '({}, {})'.format(self.type, repr(self.data))

    def __repr__(self):
        '''
        Create a python-evaluable string representation of a `Token`.
        '''
        return 'Token({},{})'.format(repr(self.type), repr(self.data))

