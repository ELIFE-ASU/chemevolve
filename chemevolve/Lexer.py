'''
Provide a Lexer class and support classes (e.g. TokenType and Token) for lexing
(tokenizing) ChemEvolve configuration files.
'''
import sys
from enum import Enum

'''
Is the running python version, version 2?
'''
is_python2 = (sys.version_info.major == 2)

'''
Is the running python version, version 3?
'''
is_python3 = (sys.version_info.major == 3)

'''
Create the `unicode` type as an alias for `str` in Python 3.

This makes unicode support a little cleaner.
'''
if is_python3:
    unicode = str

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
        elif not isinstance(data, str) and not isinstance(data, unicode):
            raise TypeError('data argument must be a string or unicode')

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

    def __eq__(self, other):
        '''
        Compare two `Token`s for equality.
        '''
        return self.type.__eq__(other.type) and self.data.__eq__(other.data)

    def isnewline(self):
        '''
        Is the token type NL?
        '''
        return self.type == TokenType.NL

    def islessthan(self):
        '''
        Is the token type LT?
        '''
        return self.type == TokenType.LT

    def isgreaterthan(self):
        '''
        Is the token type GT?
        '''
        return self.type == TokenType.GT

    def isequalto(self):
        '''
        Is the token type EQ?
        '''
        return self.type == TokenType.EQ

    def isplus(self):
        '''
        Is the token type PLUS?
        '''
        return self.type == TokenType.PLUS

    def isminus(self):
        '''
        Is the token type MINUS?
        '''
        return self.type == TokenType.MINUS

    def isdash(self):
        '''
        Is the token type DASH?
        '''
        return self.type == TokenType.DASH

    def isarrow(self):
        '''
        Is the token type ARROW?
        '''
        return self.type == TokenType.ARROW

    def isobracket(self):
        '''
        Is the token type OBRACKET?
        '''
        return self.type == TokenType.OBRACKET

    def iscbracket(self):
        '''
        Is the token type CBRACKET?
        '''
        return self.type == TokenType.CBRACKET

    def isoparen(self):
        '''
        Is the token type OPAREN?
        '''
        return self.type == TokenType.OPAREN

    def iscparen(self):
        '''
        Is the token type CPAREN?
        '''
        return self.type == TokenType.CPAREN

    def iscomma(self):
        '''
        Is the token type COMMA?
        '''
        return self.type == TokenType.COMMA

    def isinteger(self):
        '''
        Is the token type INTEGER?
        '''
        return self.type == TokenType.INTEGER

    def isfloat(self):
        '''
        Is the token type FLOAT?
        '''
        return self.type == TokenType.FLOAT

    def isstring(self):
        '''
        Is the token type STRING?
        '''
        return self.type == TokenType.STRING

class LexerError(Exception):
    '''
    The `LexerError` class provides a basic error type to be raised when an
    error is encountered during the lexing phase of parsing a Chemevolve
    configuration.
    '''
    def __init__(self, msg, filename, linenum, charnum):
        '''
        Initialize a `LexerError` providing a message to describe the error the
        filename, line and character at which the error occurred.
        '''
        message = LexerError.format(msg, filename, linenum, charnum)

        super(LexerError, self).__init__(message)

        self.filename = filename
        self.linenum = linenum
        self.charnum = charnum

    @staticmethod
    def format(msg, filename, linenum, charnum):
        '''
        Format an error message include a base message (msg) and the filename,
        line and character at which the error occurred.
        '''
        if filename is not None:
            return '{} ({}:{}:{})'.format(msg, filename, linenum, charnum)
        else:
            return '{} (:{}:{})'.format(msg, linenum, charnum)

class Lexer(object):
    '''
    The `Lexer` class breaks a file (or string) input in a list of `Token`s
    which can subsequently be parsed into a full `CoreClasses.CRS` object.
    '''
    def __init__(self, filename=None):
        '''
        Initialize the `Lexer` with an optional filename.
        '''
        self.filename = None
        self.reset(filename)

    def reset(self, filename=None):
        '''
        Reset the `Lexer` to a "freshly initialized" state.
        '''
        self.tokens = []
        self.restart(filename)

    def restart(self, filename=None):
        '''
        Restart the lexing without discarding previously lexed tokens. This
        allows multiple inputs to be concatentated into a single lexed output.
        '''
        if filename:
            self.filename = filename
        self.linenum = 1
        self.charnum = 0
        self.data = ''
        self.token_type = None

    def lex(self, s, filename=None, reset=True):
        '''
        Lex an input string `s` optionally setting the filename for the input
        to `filename`. If `reset` is `True`, then any previously lexed tokens
        are discarded; otherwise, they are retained.
        '''
        if reset:
            self.reset(filename)
        else:
            self.restart(filename)

        if (isinstance(s, str) and is_python2) or isinstance(s, bytes):
            # If the current python version is Python 2 and the `s` argument is
            # a string, then we need to decode it as UTF-8 unicode.
            for char in s.decode('utf-8'):
                self.handle_character(char)
        elif isinstance(s, unicode):
            # If the argument is of type `unicode` then, regardless of whether
            # we are using Python 2 or 3, all is well.
            for char in s:
                self.handle_character(char)
        else:
            # No other argument types are supported.
            raise TypeError('argument is not of type "str" or "unicode"')

        self.append_token()

        return self.tokens

    def lex_file(self, f, name=None, reset=True):
        '''
        Lex the contents of a file `f` using the optional `name` argument for
        error reporting. If `reset` is `True`, then any previously lexed tokens
        are discarded; otherwise, they are retained.

        If `f` is a file, then we attempt to read from it and lex the contents.
        If the `f` argument is a filename, then we attempt to open it
        (read-only), lex it, and closes it upon exiting.

        If `name is not None`, then that value is used as the filename for
        error reporting purposes. If `name is None` and `f` is a filename, then
        `name` is overridden and `f` is used for error reporting.

        :param f: an open `file` handle or a filename
        :type f: `file`, `str` or `unicode`
        :param name: an optional name used for reporting errors
        :type name: `str` or `unicode`
        :param reset: whether or not to discard previously lexed tokens
        :type reset: `bool`
        '''
        if isinstance(f, str) or isinstance(f, unicode):
            with open(f, 'rb') as filehandle:
                if name is None:
                    return self.lex_file(filehandle, name=f, reset=reset)
                else:
                    return self.lex_file(filehandle, name=name, reset=reset)
        else:
            if reset:
                self.reset(name)
            else:
                self.restart(name)

            for char in self.characters(f):
                self.handle_character(char)
            self.append_token()

            return self.tokens

    def handle_character(self, char):
        '''
        Lex a single character. This will update the internal state of the
        `Lexer`, but may not result in the pushing of a new `Token` onto the
        tokens list; this depends on the internal state of the `Lexer` and the
        character being handled.
        '''
        self.charnum += 1
        if char == '\n':
            self.newline(char)
        elif char == '<':
            self.lessthan(char)
        elif char == '=':
            self.equalto(char)
        elif char == '[':
            self.open_bracket(char)
        elif char == ']':
            self.close_bracket(char)
        elif char == '(':
            self.open_paren(char)
        elif char == ')':
            self.close_paren(char)
        elif char == ',':
            self.comma(char)
        elif char.isspace():
            self.whitespace(char)
        elif char == '.':
            self.decimal(char)
        elif char == '+':
            self.plus(char)
        elif char == '-':
            self.minus(char)
        elif char == '>':
            self.greaterthan(char)
        elif char.isdigit():
            self.digit(char)
        elif char.isalpha():
            self.char(char)
        else:
            self.error('unexpected character type "' + char + '"')

    def error(self, msg):
        '''
        Raise a `LexerError` using the provided message and the `Lexer`'s
        internal `filename`, `linenum` and `charnum` state.
        '''
        raise LexerError(msg, self.filename, self.linenum, self.charnum)

    def append_token(self):
        '''
        Append the current `Lexer`'s state to the tokens list if there is
        anything to append.

        If the `Lexer`'s state is invalid, a `LexerError` is raised.
        '''
        if self.token_type is not None and self.data != '':
            token = Token(self.token_type, self.data)
            try:
                token.validate()
            except ValueError as e:
                self.error(e.args[0])
            else:
                self.tokens.append(token)
                self.data, self.token_type = '', None
        elif self.token_type is None and self.data == '':
            pass
        else:
            self.error('unexpected lexer state')

    def singleton(self, token_type, char):
        '''
        Lex a singleton onto the tokens list.

        This appends the current state of the `Lexer`, and then subsequently
        appends a singleton type token, e.g. a newline, less-than, etc...
        '''
        self.append_token()

        self.token_type = token_type
        self.data = char
        self.append_token()

    def newline(self, char):
        '''
        Lex a newline character. This not only lexes the singleton token, but
        also modifes the `linenum` and `charnum` state.
        '''
        self.linenum += 1
        self.charnum = 0
        self.singleton(TokenType.NL, char)

    def lessthan(self, char):
        '''
        Lex a less-than \'<\' character.
        '''
        self.singleton(TokenType.LT, char)

    def equalto(self, char):
        '''
        Lex an equal-to \'=\' character.
        '''
        self.singleton(TokenType.EQ, char)

    def open_bracket(self, char):
        '''
        Lex an open bracket \'[\' character.
        '''
        self.singleton(TokenType.OBRACKET, char)

    def close_bracket(self, char):
        '''
        Lex a close bracket \']\' character.
        '''
        self.singleton(TokenType.CBRACKET, char)

    def open_paren(self, char):
        '''
        Lex an open parentheses \'(\' character.
        '''
        self.singleton(TokenType.OPAREN, char)

    def close_paren(self, char):
        '''
        Lex a close parentheses \')\' character.
        '''
        self.singleton(TokenType.CPAREN, char)

    def comma(self, char):
        '''
        Lex a comma \',\' character.
        '''
        self.singleton(TokenType.COMMA, char)

    def whitespace(self, char):
        '''
        Lex a whitespace character, i.e. append the `Lexer`'s current state and
        move on.

        Whitespace in Chemevolve configurations only end the current token,
        they carry no more syntactic meaning. The only whitespace of greater
        significance is the newline character (\\n). Carriage returns (\\r) are
        treated as any other whitespace.
        '''
        self.append_token()

    def decimal(self, char):
        '''
        Lex a decimal point (.).
        '''
        # If the first character in the token, then the token will be a FLOAT
        if self.data == '':
            self.token_type = TokenType.FLOAT
            #  self.data = '0' + char
            self.data = char
        # If the token is already an INTEGER, then the token becomes a FLOAT
        elif self.token_type == TokenType.INTEGER:
            self.token_type = TokenType.FLOAT
            #  if self.data[-1] in '+-':
            #      self.data += '0'
            self.data += char
        # Decimal points are allowed after the first character of a STRING
        elif self.token_type == TokenType.STRING:
            self.data += char
        # If the token is a PLUS, then it becomes a (positive) FLOAT
        elif self.token_type == TokenType.PLUS:
            self.token_type = TokenType.FLOAT
            #  self.data += '0' + char
            self.data += char
        # If the token is a MINUS, then it becomes a (negative) FLOAT
        elif self.token_type == TokenType.MINUS:
            self.token_type = TokenType.FLOAT
            #  self.data += '0' + char
            self.data += char
        # If the token is alread a FLOAT, then it has too many decimals!
        elif self.token_type == TokenType.FLOAT:
            self.error('unexpected decimal in float')
        # Any other case is an "unexpected decimal"
        else:
            self.error('unexpected decimal "."')

    def plus(self, char):
        '''
        Lex a plus sign (+).
        '''
        # If it is the first character, then the token it a PLUS
        if self.data == '':
            self.token_type = TokenType.PLUS
            self.data = char
        # If the token is a FLOAT
        elif self.token_type == TokenType.FLOAT:
            # and the previous character is an 'e' or 'E', then all is well
            if self.data[-1] in 'eE':
                self.data += char
            # otherwise we push the previous FLOAT, and start a PLUS
            else:
                self.append_token()
                self.token_type = TokenType.PLUS
                self.data = char
        # If the token is an INTEGER, then we push the previous INTEGER and
        # start a PLUS
        elif self.token_type == TokenType.INTEGER:
            self.append_token()
            self.token_type = TokenType.PLUS
            self.data = char
        # Any other case is an error
        else:
            self.error('unexpected plus sign "+"')

    def minus(self, char):
        '''
        Lex a minus sign (-).
        '''
        # If this is the first character of the token, then it is a MINUS
        if self.data == '':
            self.token_type = TokenType.MINUS
            self.data = char
        # If the token is a STRING, then everything is okay
        elif self.token_type == TokenType.STRING:
            self.data += char
        # If the token is already a MINUS, then the token type becomes DASH
        elif self.token_type == TokenType.MINUS:
            self.token_type = TokenType.DASH
            self.data += char
        # If the token is a FLOAT, then check
        elif self.token_type == TokenType.FLOAT:
            # if the previous character is one of 'eE', then all is well
            if self.data[-1] in 'eE':
                self.data += char
            # otherwise push the FLOAT and start a MINUS
            else:
                self.append_token()
                self.token_type = TokenType.MINUS
                self.data = char
        # If the token is an INTEGER, push it and start a MINUS
        elif self.token_type == TokenType.INTEGER:
            self.append_token()
            self.token_type = TokenType.MINUS
            self.data = char
        # Any other case is an error
        else:
            self.error('unexpected minus sign "+"')

    def greaterthan(self, char):
        '''
        Lex a greater-than (>).
        '''
        # If this the first character, then it is a singleton
        if self.data == '':
            self.singleton(TokenType.GT, char)
        # If the token is a MINUS, then it is now an ARROW and we push it.
        elif self.token_type == TokenType.MINUS:
            self.token_type = TokenType.ARROW
            self.data += char
            self.append_token()
        # Any other case should result in a singleton
        else:
            self.singleton(TokenType.GT, char)

    def digit(self, char):
        '''
        Lex a digit ([0-9]).
        '''
        # If this is the first character, then the token is an INTEGER
        if self.data == '':
            self.token_type = TokenType.INTEGER
            self.data += char
        # If the token is already an INTEGER, then keep going
        elif self.token_type == TokenType.INTEGER:
            self.data += char
        # If the token is already a FLOAT, then keep going
        elif self.token_type == TokenType.FLOAT:
            self.data += char
        # Any other case starts a new token
        else:
            self.append_token()
            self.token_type = TokenType.INTEGER
            self.data = char

    def char(self, char):
        '''
        Lex a generic character.
        '''
        # If this is the first character, then the token is a STRING
        if self.data == '':
            self.token_type = TokenType.STRING
            self.data += char
        # If the token is already a STRING, keep going.
        elif self.token_type == TokenType.STRING:
            self.token_type = TokenType.STRING
            self.data += char
        # If the token is already an INTEGER, then we check
        elif self.token_type == TokenType.INTEGER:
            # if the character is in 'eE', then the token becomes a FLOAT
            if char in 'eE':
                self.token_type = TokenType.FLOAT
                self.data += char
            # otherwise we have an error
            else:
                self.error('characters not supported in integers "' + char + '"')
        # If the token is already an FLOAT, then we check
        elif self.token_type == TokenType.FLOAT:
            # if the character is in 'eE', then everything is okay
            if char in 'eE':
                self.data += char
            # otherwise we have an error
            else:
                self.error('characters not supported in floats "' + char + '"')
        # Any other case is an error
        else:
            self.error('unexpected character "' + char + '"')

    def characters(self, filehandle):
        '''
        Generator over the characters is a `file` with UTF-8 support
        '''
        c = filehandle.read(1)
        while c:
            while True:
                try:
                    yield c.decode('utf-8')
                except UnicodeDecodeError:
                    c += filehandle.read(1)
                else:
                    c = filehandle.read(1)
                    break

