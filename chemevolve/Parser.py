'''
Provide a Parser class and support classes (e.g. ParserError) for parsing
Chemevolve configuration files.
'''
from Lexer import TokenType, Lexer
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
        self.filename = None
        self.lexer = Lexer(filename)
        self.reset(filename)

    def reset(self, filename=None):
        self.lexer.reset(filename)
        self.tokens = []
        self.numtokens = 0
        self.metadata = dict()
        self.molecule_list = list()
        self.molecule_dict = dict()
        self.reaction_list = list()

        self.restart(filename)

    def restart(self, filename=None):
        if filename:
            self.filename = filename
        self.linenum = 1
        self.phase = ParserPhase.START

    def parse(self, s, filename=None, reset=True):
        '''
        Parse a string into a `CoreClasses.CRS` object.
        '''
        if reset:
            self.reset(filename)
        else:
            self.restart(filename)

        self.tokens = self.lexer.lex(s)
        self.numtokens = len(self.tokens)
        if self.numtokens == 0:
            return None
        
        i = 0
        while not self.eof(i):
            i = self.process_tokens(i)
        self.process_tokens(i)

    def process_tokens(self, i):
        '''
        Process the next "unit" of tokens.
        '''
        if self.phase == ParserPhase.START:
            return self.start_phase(i)
        elif self.phase == ParserPhase.HEADING:
            return self.heading_phase(i)
        elif self.phase == ParserPhase.METADATA:
            return self.metadata_phase(i)
        elif self.phase == ParserPhase.KEYVALUE:
            return self.keyvalue_phase(i)
        else:
            self.error('unimplemented parser phase {}'.format(self.phase))

    def start_phase(self, i):
        '''
        Parse the START phase
        '''
        i = self.newlines(i)
        if not self.eof(i):
            token = self.tokens[i]
            if token.islessthan():
                self.phase = ParserPhase.HEADING
            else:
                self.error('unexpected token {}'.format(token))
        return i

    def heading_phase(self, i):
        '''
        Parse the HEADING phase of the form ["<" STRING ">"] (with optional
        spaces)
        '''
        try:
            _, i = self.eat(i, TokenType.LT)
            heading, i = self.string(i)
            _, i = self.eat(i, TokenType.GT)

            if heading == 'meta-data':
                self.phase = ParserPhase.METADATA
            else:
                self.error('unrecognized section heading "' + heading + '"')
            return i
        except ParserError as e:
            self.error(e.args[0] + ' while parsing heading')

    def metadata_phase(self, i):
        '''
        Parse the METADATA phase.
        '''
        i = self.newlines(i)
        if not self.eof(i):
            token = self.tokens[i]
            if token.isstring():
                self.phase = ParserPhase.KEYVALUE
            elif token.islessthan():
                self.process_metadata()
                self.phase = ParserPhase.HEADING
            else:
                self.error('unexpected token {} in meta-data section'.format(token.type))
        else:
            self.process_metadata()
        return i

    def keyvalue_phase(self, i):
        '''
        Parse the KEYVALUE phase.
        '''
        try:
            key, i = self.string(i)
            _, i = self.eat(i, TokenType.EQ)
            value, i = self.value(i)

            self.phase = ParserPhase.METADATA
            self.metadata[key] = value

            return i
        except ParserError as e:
            self.error(e.args[0] + ' while parsing key-value pair')

    def error(self, msg):
        '''
        Raise a parser error with a given message.
        '''
        raise ParserError(msg, self.filename, self.linenum)

    def newlines(self, i):
        '''
        Eat up any newline tokens.
        '''
        while not self.eof(i) and self.tokens[i].isnewline():
            self.linenum += 1
            i += 1
        return i

    def eat(self, i, ttype, optional=False):
        '''
        Eat a token of a given type.
        '''
        if not self.eof(i):
            token = self.tokens[i]
            if token.type == ttype:
                return token.convert(), i+1
            elif optional:
                return None, i
            else:
                self.error('expected {}, found {}'.format(token.type, ttype))
        elif optional:
            return None, i
        else:
            self.error('expected {}, found EOF'.format(ttype))

    def string(self, i, optional=False):
        '''
        Eat a STRING token.
        '''
        return self.eat(i, TokenType.STRING, optional)

    def sign(self, i, optional=False):
        '''
        '''
        if not self.eof(i):
            token = self.tokens[i]
            if token.isplus():
                return 1, i+1
            elif token.isminus():
                return -1, i+1
            elif optional:
                return None, i
            else:
                self.error('expected {}, found {}'.format(token.type, ttype))
        elif optional:
            return None, i
        else:
            self.error('expected {}, found EOF'.format(ttype))

    def integer(self, i, optional=False):
        '''
        Eat an integer, with or without a leading sign.
        '''
        sign, j = self.sign(i, optional=True)
        value, j = self.eat(j, TokenType.INTEGER, optional)
        if value and sign:
            value *= sign
        return value, j

    def float(self, i, optional=False):
        '''
        Eat an float, with or without a leading sign.
        '''
        sign, j = self.sign(i, optional=True)
        value, j = self.eat(j, TokenType.FLOAT, optional)
        if value and sign:
            value *= sign
        return value, j

    def value(self, i, optional=False):
        '''
        Eat a "value", i.e. a string, integer or float.
        '''
        value, i = self.string(i, optional=True)
        if value:
            return value, i

        value, i = self.integer(i, optional=True)
        if value:
            return value, i

        value, i = self.float(i, optional=True)
        if value:
            return value, i
        elif optional:
            return None, i
        else:
            self.error('value must be a STRING, INTEGER or FLOAT')

    def eof(self, i):
        '''
        Have we reached (or exceeded) the end-of-file (EOF). That is, have we
        run out of tokens?
        '''
        return i >= self.numtokens        

    def process_metadata(self):
        '''
        Process the metadata so far parsed.
        '''
        try:
            value = self.metadata['nrMolecules']
            if not isinstance(value, int) or value < 1:
                self.error('value of nrMolecules must be a positive, non-zero integer')
            self.molecule_list = [None] * value
        except KeyError:
            self.error('nrMolecules must be provided in meta-data')

        try:
            value = self.metadata['nrReactions']
            if not isinstance(value, int) or value < 1:
                self.error('value of nrReactions must be a positive, non-zero integer')
            self.reaction_list = [None] * value
        except KeyError:
            self.error('nrReactions must be provided in meta-data')

