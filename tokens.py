# -*- coding: utf-8 -*-

"""
    Input processing and tokenization
    
    This module reads input code from stdin or source files and
    returns the tokenized code. It extracts the lexical elements
    in the code and removes all comments and insignificant whitespaces.
"""

from errors import *

LEX_INITIAL = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '!$%&*/:<=>?^_~@'
LEX_DOT = '.'
LEX_SLASH = '/'
LEX_SIGN = '+-'
LEX_DIGIT = '0123456789'
LEX_QUOTATION = '\''
LEX_QUOTE = '"'
LEX_SEMICOLON = ';'
LEX_SHARP = '#'
LEX_IMGUNIT = 'i'
LEX_LPAREN = '('
LEX_RPAREN = ')'
LEX_WHITESPACE = ' \n\t'

class Tokenizer:
    """
        Tokenize the given code string with simple DFAs.

        Status: 
            self.expr: current code string
            self.cursor: current cursor position
            self.lineno: current line number
            self.paren_level: parenthesis level, `(' is +1, `)' is -1
            self.token_list: tokens found
            self.more_str: if we're in a string
            self.more_expr : if we need more code to complete an expression
            self.more_quote: if we're in a quote
            self.eof: if we reach EOF of the source file
            self.infile: source file
    """
    def __init__(self, expr='', infile=''):
        self.expr = expr
        self.cursor = 0
        self.lineno = 0
        self.paren_level = 0
        self.token_list = []

        self.more_str = False
        self.more_expr = True
        self.more_quote = False
        self.eof = False

        if infile == '':
            self.infile = ''
        else:
            try:
                self.infile = open(infile, 'r')
            except Exception:
                self.infile = None
                raise SchemeSysError('cannot read source file')

    def reset(self):
        """
            Reset the token list for next parsing
        """
        self.token_list = []
        self.more_expr = True

    def close(self):
        self.infile.close()

    def read_new_line(self):
        if self.infile == '':
            self.expr = input() + '\n'
        else:
            self.expr = self.infile.readline()
            self.eof = True if self.expr == '' else False
        self.lineno += 1
        self.cursor = 0

    def get_numberid(self):
        """
            Parse a number(integer, fraction, decimal) or
            identifier
        """
        START = -1
        INTEGER = 0
        DECIMAL = 1
        FRACTION = 2 # we see `/'
        DENOMINATOR = 3
        SINGLE_DOT = 4 # we see `.'
        SINGLE_SIGN = 5 # we see `+' or `-'
        IDENTIFIER = 6
        COMPLEX = 7 # we see `i'

        state = START
        imaginary = False # if we read number and sign, imaginary part begins
        cur_token = ''

        while self.cursor < len(self.expr):
            char = self.expr[self.cursor]
            if state == START:
                if char in LEX_DIGIT:
                    state = INTEGER 
                elif char in LEX_DOT:
                    state = SINGLE_DOT
                elif char in LEX_SIGN:
                    state = SINGLE_SIGN
                elif char in LEX_INITIAL:
                    state = IDENTIFIER

            elif state == INTEGER: 
                if char in LEX_DIGIT:
                    state = INTEGER
                elif char in LEX_DOT:
                    state = DECIMAL
                elif char in LEX_SLASH:
                    state = FRACTION
                elif char in LEX_SIGN:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    imaginary = True
                    state = SINGLE_SIGN
                elif char in LEX_IMGUNIT:
                    state = COMPLEX
                elif char in LEX_WHITESPACE:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad number syntax')

            elif state == DECIMAL:
                if char in LEX_DIGIT:
                    state = DECIMAL
                elif char in LEX_SIGN:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    imaginary = True
                    state = SINGLE_SIGN
                elif char in LEX_IMGUNIT:
                    state = COMPLEX
                elif char in LEX_WHITESPACE:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad decimal number syntax')

            elif state == FRACTION:
                if char in LEX_DIGIT:
                    state = DENOMINATOR
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad fraction syntax')

            elif state == DENOMINATOR:
                if char in LEX_DIGIT:
                    state = DENOMINATOR
                elif char in LEX_SIGN:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    imaginary = True
                    state = SINGLE_SIGN
                elif char in LEX_IMGUNIT:
                    state = COMPLEX
                elif char in LEX_WHITESPACE:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad fraction syntax')

            elif state == SINGLE_DOT:
                if char in LEX_DIGIT:
                    state = DECIMAL
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN or char in LEX_WHITESPACE:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad floating point number syntax')

            elif state == SINGLE_SIGN:
                if char in LEX_DOT:
                    state = SINGLE_DOT
                elif char in LEX_DIGIT:
                    state = INTEGER
                elif char in LEX_IMGUNIT:
                    state = COMPLEX
                elif char in LEX_INITIAL:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    state = IDENTIFIER
                elif char in LEX_WHITESPACE:
                    if imaginary:
                        raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad identifier syntax')

            elif state == COMPLEX:
                if char in LEX_WHITESPACE:
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad complex number syntax')

            elif state == IDENTIFIER:
                if char in LEX_INITIAL or char in LEX_SIGN or char in LEX_DIGIT or \
                   char in LEX_DOT or char in LEX_SHARP:
                    state = IDENTIFIER
                elif char in LEX_WHITESPACE:
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad identifier syntax')
                
            cur_token += char
            self.cursor += 1

    def get_string(self):
        """
            Parse a string, decide if we're in a string
            and need to read more code
        """
        START = -1
        CONTENT = 0
        END = 1

        state = START if not self.more_str else CONTENT
        cur_token = ''

        while self.cursor < len(self.expr):
            char = self.expr[self.cursor]
            if state == START: 
                state = CONTENT
            elif state == CONTENT:
                if char not in LEX_QUOTE: 
                    state = CONTENT
                else:
                    state = END
            elif state == END:
                if self.more_str:
                    self.token_list[-1] += cur_token
                else:
                    self.token_list.append(cur_token)
                    self.more_quote = False
                self.more_str = False
                self.cursor -= 1
                return
            cur_token += char
            self.cursor += 1

        if self.more_str:
            self.token_list[-1] += cur_token
        else:
            self.token_list.append(cur_token)
            self.more_quote = False

        if state == CONTENT:
            self.more_str = True

    def get_sharp(self):
        """
            Parse a #xxx expression, only boolean now
            TODO: more expression types
        """
        START = -1
        SHARP = 0
        BOOLEAN = 1

        state = START
        cur_token = ''

        while self.cursor < len(self.expr):
            char = self.expr[self.cursor]
            if state == START:
                state = SHARP
            elif state == SHARP:
                if char in 'tf':
                    state = BOOLEAN
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad boolean syntax')
            elif state == BOOLEAN:
                if char in LEX_WHITESPACE:
                    return cur_token
                elif char in LEX_QUOTATION or char in LEX_QUOTE or \
                     char in LEX_SEMICOLON or char in LEX_LPAREN or \
                     char in LEX_RPAREN:
                    self.cursor -= 1
                    return cur_token
                else:
                    raise SchemeParseError(self.lineno, self.expr, 'bad boolean syntax')
            cur_token += char
            self.cursor += 1

    def tokenize(self):
        """
            Tokenize the code currently we have. Decide which
            automata we are going to, check if parentheses match
            and if we're in an unfinished quotation.
        """
        while self.cursor < len(self.expr):
            char = self.expr[self.cursor]

            if self.more_str:
                self.get_string()
            elif char in LEX_DIGIT or char in LEX_DOT or char in LEX_SIGN or char in LEX_INITIAL:
                self.token_list.append(self.get_numberid())
                self.more_quote = False
            elif char in LEX_QUOTE:
                self.get_string()
            elif char in LEX_SEMICOLON:
                break
            elif char in LEX_SHARP:
                self.token_list.append(self.get_sharp())
                self.more_quote = False
            elif char in LEX_QUOTATION:
                self.more_quote = True
                self.token_list.append(char)
            elif char in LEX_LPAREN:
                self.token_list.append(char)
                self.more_quote = False
                self.paren_level += 1
            elif char in LEX_RPAREN:
                self.token_list.append(char)
                self.more_quote = False
                self.paren_level -= 1

            elif char in LEX_WHITESPACE:
                pass;
            else:
                raise SchemeParseError(self.lineno, self.expr, 'bad syntax')

            self.cursor += 1
        
        if self.paren_level < 0:
            raise SchemeParseError(self.lineno, self.expr, "unexpected `)'")
        elif self.paren_level > 0:
            self.more_expr = True
        else:
            if not self.more_quote and not self.more_str and self.token_list != []:
                self.more_expr = False

