'''
Provide a Parser class and support classes (e.g. ParserError) for parsing
Chemevolve configuration files.
'''
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

