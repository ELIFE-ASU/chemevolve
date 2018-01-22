'''
Provide a Parser class and support classes (e.g. ParserError) for parsing
Chemevolve configuration files.
'''
from Lexer import TokenType, Lexer
from enum import Enum
from CoreClasses import CRS, Reaction

class ParserError(Exception):
    '''
    The `ParserError` class provides a basic error type to be raised when an
    error is encountered during the parsing phase of parsing a Chemevolve
    configuration.
    '''
    def __init__(self, message, filename, linenum):
        '''
        Initialize a `ParserError` providing a message to describe the error,
        the filename, and the line number at which the error occurred.
        '''
        self.message = message
        self.filename = filename
        self.linenum = linenum

        msg = ParserError.format(self.message, self.filename, self.linenum)
        super(ParserError, self).__init__(msg)

    @staticmethod
    def format(message, filename, linenum):
        '''
        Format an error message include a base message and the filename, line
        at which the error occurred.
        '''
        if filename is not None:
            return '{} ({}:{})'.format(message, filename, linenum)
        else:
            return '{} (:{})'.format(message, linenum)

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
        '''
        Reset the parser to a freshly-initialized state.
        '''
        if filename:
            self.filename = filename
        self.linenum = 1
        self.phase = ParserPhase.START

        self.lexer.reset(filename)
        self.tokens = []
        self.numtokens = 0
        self.metadata = dict()
        self.molecule_list = list()
        self.molecule_dict = dict()
        self.reaction_list = list()
        self.crs = None

    def parse(self, s, filename=None):
        '''
        Parse a string into a `CoreClasses.CRS` object.
        '''
        self.reset(filename)

        self.tokens = self.lexer.lex(s, reset=True)
        self.numtokens = len(self.tokens)
        if self.numtokens == 0:
            return None

        return self.process()

    def parse_file(self, f, name='None'):
        '''
        Parse the contents of a file `f` using the optional `name` argument for
        error reporting. 

        If `f` is a file, then we attempt to read from it and parse the
        contents. If the `f` argument is a filename, then we attempt to open it
        (read-only), parse the contents and close it upon exit.

        If `name is not None`, then that value is used as the filename for
        error reporting purposes. If `name is None`, and `f` is a filename`,
        then `name` is overriddent and `f` is used for error reporting.

        :param f: an open `file` handle or a filename
        :type f: `file`, `str` or `unicode`
        :param name: an optional name used for reporting errors
        :type name: `str` or `unicode`
        '''
        self.reset(name)
        self.tokens = self.lexer.lex_file(f, name=name, reset=True)
        self.numtokens = len(self.tokens)
        if self.numtokens == 0:
            return None

        return self.process()

    def process(self):
        '''
        Process any tokens that have so far been lexed.
        '''
        i = 0
        while not self.eof(i):
            i = self.process_tokens(i)
        self.process_tokens(i)

        self.process_molecules()
        self.process_reactions()

        if len(self.molecule_list) == 0 or len(self.reaction_list) == 0:
            self.crs = None
        else:
            self.crs = CRS(self.molecule_list, self.molecule_dict, self.reaction_list)

        return self.crs


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
        elif self.phase == ParserPhase.MOLECULES:
            return self.molecules_phase(i)
        elif self.phase == ParserPhase.MOLECULE:
            return self.molecule_phase(i)
        elif self.phase == ParserPhase.REACTIONS:
            return self.reactions_phase(i)
        elif self.phase == ParserPhase.REACTION:
            return self.reaction_phase(i)
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
            elif heading == 'molecules':
                self.phase = ParserPhase.MOLECULES
            elif heading == 'reactions':
                self.phase = ParserPhase.REACTIONS
            else:
                self.error('unrecognized section heading "' + heading + '"')

            if self.phase != ParserPhase.METADATA and self.metadata == dict():
                self.error('the first section must be "meta-data"')

            return i
        except ParserError as e:
            self.error(e.message + ' while parsing heading')

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
            self.error(e.message + ' while parsing key-value pair')

    def molecules_phase(self, i):
        '''
        Parse the MOLECULES phase.
        '''
        i = self.newlines(i)
        if not self.eof(i):
            token = self.tokens[i]
            if token.isobracket():
                self.phase = ParserPhase.MOLECULE
            elif token.islessthan():
                self.phase = ParserPhase.HEADING
            else:
                self.error('unexpected token {} in molecules section'.format(token.type))
        return i

    def molecule_phase(self, i):
        '''
        Parse the MOLECULE phase.
        '''
        try:
            index, i = self.index(i)
            name, i = self.string(i)
        except ParserError as e:
            self.error(e.message + ' while parsing molecule')

        if index >= len(self.molecule_list):
            self.error('invalid reaction ID (too large, see meta-data.nrMolecules)')
        elif self.molecule_list[index] is not None:
            self.error('duplicate molecule index')
        elif name in self.molecule_dict:
            self.error('duplicate molecule name')

        self.molecule_list[index] = name
        self.molecule_dict[name] = index
        self.phase = ParserPhase.MOLECULES

        return i

    def reactions_phase(self, i):
        '''
        Parse the REACTIONS phase.
        '''
        i = self.newlines(i)
        if not self.eof(i):
            token = self.tokens[i]
            if token.isobracket():
                self.phase = ParserPhase.REACTION
            elif token.islessthan():
                self.process_metadata()
                self.phase = ParserPhase.HEADING
            else:
                self.error('unexpected token {} in reactions section'.format(token.type))
        return i

    def reaction_phase(self, i):
        '''
        Parse the REACTION phase.
        '''
        try:
            ID, j = self.index(i)
            reactant_coeffs, reactants, j = self.reactants(j)
            _, j = self.eat(j, TokenType.DASH)
            rate_constant, j = self.float(j)
            _, j = self.eat(j, TokenType.ARROW)
            product_coeffs, products, j = self.reactants(j)
            propensity, j = self.string(j)
            catalyzed_constants, catalysts, j = self.catalysts(j, optional=True)

            if catalysts is None:
                catalysts = list()
            if catalyzed_constants is None:
                catalyzed_constants = list()

            if ID >= len(self.reaction_list):
                self.error('invalid reaction ID (too large, see meta-data.nrReactions)')
            elif self.reaction_list[ID] is not None:
                self.error('duplicate reaction ID')

            self.reaction_list[ID] = Reaction(ID=ID,
                    reactants=reactants,
                    reactant_coeff=reactant_coeffs,
                    products=products,
                    product_coeff=product_coeffs,
                    constant=rate_constant,
                    catalysts=catalysts,
                    catalyzed_constants=catalyzed_constants,
                    prop=propensity)
            self.phase = ParserPhase.REACTIONS

            return j
        except ParserError as e:
            self.error(e.message + ' while parsing reaction')

    def reactants(self, i, optional=False):
        '''
        Parse a sequence of reactants
        '''
        coefficients = []
        reactants = []
        c, r, j = self.reactant(i, optional)
        if c and r:
            coefficients.append(c)
            reactants.append(r)
            plus, j = self.eat(j, TokenType.PLUS, optional=True)
            while plus:
                c, r, j = self.reactant(j, optional=False)
                coefficients.append(c)
                reactants.append(r)
                plus, j = self.eat(j, TokenType.PLUS, optional=True)
            return coefficients, reactants, j
        else:
            return None, None, i

    def reactant(self, i, optional=False):
        '''
        Parse a reactant of the form (INTEGER? "[" STRING "]").
        '''
        coefficient, j = self.eat(i, TokenType.INTEGER, optional=True)
        if not coefficient:
            coefficient = 1
        else:
            optional=False

        reactant, j = self.bracketed(j, TokenType.STRING, optional=optional)

        if reactant:
            return coefficient, reactant, j
        elif optional:
            return None, None, i
        else:
            self.error('expected a reactant')

    def catalysts(self, i, optional=False):
        '''
        Parse catalysts for a reaction
        '''
        paren, j = self.eat(i, TokenType.OPAREN, optional=optional)
        if paren:
            constants = []
            catalysts = []
            constant, catalyst, j = self.catalyst(j, optional)
            if constant and catalyst:
                constants.append(constant)
                catalysts.append(catalyst)
                comma, j = self.eat(j, TokenType.COMMA, optional=True)
                while comma:
                    constant, catalyst, j = self.catalyst(j, optional=False)
                    constants.append(constant)
                    catalysts.append(catalyst)
                    comma, j = self.eat(j, TokenType.COMMA, optional=True)
            paren, j = self.eat(j, TokenType.CPAREN, optional=False)
            return constants, catalysts, j
        else:
            return None, None, j

    def catalyst(self, i, optional=False):
        '''
        Parse a catalyst of the form (+?FLOAT "[" STRING "]")
        '''
        constant, j = self.float(i, optional=optional)
        if constant and constant <= 0.0:
            self.error('catalyzed constant must be positive, non-zero')
        elif constant:
            catalyst, j = self.bracketed(j, TokenType.STRING, optional=False)
            return constant, catalyst, j
        else:
            return None, None, i


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
                self.error('expected {}, found {}'.format(ttype, token.type))
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
        Eat a sign (+/-) and return it as an integer
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

    def index(self, i, optional=False):
        '''
        Parse an index of the form ("[" INTEGER "]").
        '''
        return self.bracketed(i, TokenType.INTEGER, optional)

    def bracketed(self, i, ttype, optional=False):
        '''
        Parse a brackted value of the form ("[" ttype "]").
        '''
        try:
            _, j = self.eat(i, TokenType.OBRACKET)
            value, j = self.eat(j, ttype)
            _, j = self.eat(j, TokenType.CBRACKET)

            return value, j
        except ParserError:
            if optional:
                return None, i
            else:
                raise

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

    def process_molecules(self):
        '''
        Ensure that the molecule_list and molecule_dict are valid
        '''
        for i, molecule in enumerate(self.molecule_list):
            if molecule is None:
                self.error('missing molecule: [{}]'.format(i))
            elif molecule not in self.molecule_dict:
                self.error('missing molecule in dictionary: [{}] {}'.format(i,molecule))

        n = len(self.molecule_list)
        for molecule in self.molecule_dict.keys():
            v = self.molecule_dict[molecule]
            if molecule is None:
                self.error('key in molecule dictionary is None')
            elif v < 0:
                self.error('molecule index is negative: {} => {}'.format(molecule, v))
            elif v > n:
                self.error('molecule index is too large: {} => {}'.format(molecule, v))
            elif self.molecule_list[v] != molecule:
                self.error('molecule list and dict incompatible at {}'.format(molecule))

    def process_reactions(self):
        '''
        Ensure that the reaction_list is valid
        '''
        for i, reaction in enumerate(self.reaction_list):
            if reaction is None:
                self.error('missing reaction: [{}]'.format(i))

