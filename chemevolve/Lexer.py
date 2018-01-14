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

