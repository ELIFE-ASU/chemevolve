'''
Provide a Parser class and support classes (e.g. ParserError) for parsing
Chemevolve configuration files.
'''
from Lexer import Lexer
from enum import Enum

class ParserError(Exception):
    '''
    The `ParserError` class provides a basic error type to be raised when an
    error is encountered during the parsing phase of parsing a Chemevolve
    configuration.
    '''
    def __init__(self, msg, filename, linenum):
        '''
        Initialize a `ParserError` providing a message to describe the error,
        the filename, and the line number at which the error occurred.
        '''
        message = ParserError.format(msg, filename, linenum)

        super(ParserError, self).__init__(message)
        
        self.filename = filename
        self.linenum = linenum

    @staticmethod
    def format(msg, filename, linenum):
        '''
        Format an error message include a base message (msg) and the filename,
        line at which the error occurred.
        '''
        if filename is not None:
            return '{} ({}:{})'.format(msg, filename, linenum)
        else:
            return '{} (:{})'.format(msg, linenum)

class ParserPhase(Enum):
    '''
    The `ParserPhase` enumeration provides a type for representing the states in
    which the parser may be found.
    '''
    START     = 0 # The phase when the parser is initialized or restarted
    HEADING   = 1 # The phase when a header is being read, e.g. <meta-data>
    METADATA  = 2 # The phase after 'meta-data' is encountered
    MOLECULES = 3 # The phase after 'molecules' is encountered
    REACTIONS = 4 # The phase after 'reactions' is encountered
    KEYVALUE  = 5 # The phase while parsing a key-value pair: nrMolecules = 100
    MOLECULE  = 6 # The phase while parsing a molecule, [0] A
    REACTION  = 7 # The phase while parsing a reaction, [0] 2[A] -- 1.0 -> [AA]

class Parser(object):
    '''
    The `Parser` class parses a configuraiton file into a full
    `CoreClasses.CRS` object.
    '''
    def __init__(self, filename=None):
        '''
        Initialize the `Parser` object.
        '''
        self.filename = filename
        self.linenum = 1
        self.phase = ParserPhase.START
        self.lexer = Lexer(filename)
        self.tokens = []

    def parse(self, s):
        '''
        Parse a string into a `CoreClasses.CRS` object.
        '''
        self.tokens = self.lexer.lex(s)
        if len(self.tokens) == 0:
            return None

