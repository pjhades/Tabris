# -*- coding: utf-8 -*-

import unittest
from tsymbol import tsym
from tpair import to_str, from_python_list, NIL
from scmlib import *
from parser import *

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()

    def tearDown(self):
        self.tokenizer = None

    def testTokenizer(self):
        """Test the normal tokenizer.
        """
        cases = [("lambda", [("lambda", TOKEN_TYPE_SYMBOL)]), \
                 ("12345", [("12345", TOKEN_TYPE_INTEGER)]), \
                 ("i", [("i", TOKEN_TYPE_SYMBOL)]), \
                 ("-4/56", [("-4/56", TOKEN_TYPE_FRACTION)]), \
                 ("0.", [("0.", TOKEN_TYPE_FLOAT)]), \
                 (".", [(".", TOKEN_TYPE_DOT)]), \
                 ("(", [("(", TOKEN_TYPE_LPAREN)]), \
                 (")", [(")", TOKEN_TYPE_RPAREN)]), \
                 ("'", [("'", TOKEN_TYPE_SINGLE_QUOTE)]), \
                 ("-6.2350-0i", [("-6.2350-0i", TOKEN_TYPE_COMPLEX)]), \
                 ("+i", [("+i", TOKEN_TYPE_COMPLEX)]), \
                 ("-i", [("-i", TOKEN_TYPE_COMPLEX)]), \
                 ("\"this is a string\"", [("\"this is a string\"", TOKEN_TYPE_STRING)]), \
                 ("\"a string\nspans multiple\nlines\"", [("\"a string\nspans multiple\nlines\"", TOKEN_TYPE_STRING)]), \
                 ("'''x", [("'", TOKEN_TYPE_SINGLE_QUOTE), 
                           ("'", TOKEN_TYPE_SINGLE_QUOTE), 
                           ("'", TOKEN_TYPE_SINGLE_QUOTE), 
                           ("x", TOKEN_TYPE_SYMBOL)]), \
                 ("'\n'\n'\nx", [("'", TOKEN_TYPE_SINGLE_QUOTE), 
                                 ("'", TOKEN_TYPE_SINGLE_QUOTE), 
                                 ("'", TOKEN_TYPE_SINGLE_QUOTE), 
                                 ("x", TOKEN_TYPE_SYMBOL)]), \
                 ("'(a . (b . ()))", [("'", TOKEN_TYPE_SINGLE_QUOTE), 
                                      ("(", TOKEN_TYPE_LPAREN), 
                                      ("a", TOKEN_TYPE_SYMBOL), \
                                      (".", TOKEN_TYPE_DOT), 
                                      ("(", TOKEN_TYPE_LPAREN), 
                                      ("b", TOKEN_TYPE_SYMBOL), \
                                      (".", TOKEN_TYPE_DOT), 
                                      ("(", TOKEN_TYPE_LPAREN), 
                                      (")", TOKEN_TYPE_RPAREN), \
                                      (")", TOKEN_TYPE_RPAREN), 
                                      (")", TOKEN_TYPE_RPAREN)]), \
                 ("; this is \"comm\"ent", []), \
                 ('";not comment"', [('";not comment"', TOKEN_TYPE_STRING)]), \
                 ("#t", [("#t", TOKEN_TYPE_BOOLEAN)])]
        for case in cases:
            self.tokenizer.tokenize_piece(case[0] + '\n')
            self.assertEqual(self.tokenizer.get_tokens(), case[1])

    def testTokenizeSingle(self):
        """Test the single-line tokenizer.
        """
        cases = [("lambda", [("lambda", TOKEN_TYPE_SYMBOL)]), \
                 ("-4/56", [("-4/56", TOKEN_TYPE_FRACTION)]), \
                 ("0.", [("0.", TOKEN_TYPE_FLOAT)]), \
                 ("-6.2350-0i", [("-6.2350-0i", TOKEN_TYPE_COMPLEX)]), \
                 ("-i", [("-i", TOKEN_TYPE_COMPLEX)]), \
                 ("\"this is a string\"", [("\"this is a string\"", TOKEN_TYPE_STRING)])]
        for case in cases:
            self.assertEqual(self.tokenizer.tokenize(case[0] + '\n'), case[1])


    def testLexemeParsing(self):
        """Test parsing lexemes.
        """
        self.tokenizer.tokenize_piece("aaa" + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], tsym("aaa"))

        self.tokenizer.tokenize_piece("#t" + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], True)

        self.tokenizer.tokenize_piece('"helloworld"' + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], "helloworld")

        self.tokenizer.tokenize_piece('123' + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], 123)

        self.tokenizer.tokenize_piece('-4/6' + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], -2.0/3.0)

        self.tokenizer.tokenize_piece('.0' + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], 0.0)

        self.tokenizer.tokenize_piece('+i' + "\n")
        obj = self.parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], 1j)

    def testSexpParsing(self):
        """Test parsing S-expressions.
        """
        cases = [("x", tsym("x")), \
                 ("(x)", from_python_list([tsym("x")])), \
                 ("(x y)", from_python_list([tsym("x"), tsym("y")])), \
                 ("(x (y))", from_python_list([tsym("x"), [tsym("y")]])), \
                 ("(x . y)", cons(tsym("x"), tsym("y"))), \
                 ("(x y . z)", cons(tsym("x"), cons(tsym("y"), tsym("z")))), \
                 ("(x (y . z) w)", cons(tsym("x"), 
                                       cons(cons(tsym("y"), tsym("z")),
                                           cons(tsym("w"), NIL))))]
        for case in cases:
            sexp = self.parser.parse(self.tokenizer.tokenize(case[0] + '\n'))[0]
            self.assertEqual(sexp, case[1])

    def testStringRepr(self):
        """Test the string representation of the parsed S-expressions.
        """
        cases = [("'x", "(quote x)"), \
                 ("''x", "(quote (quote x))"), \
                 ("'(quote 'x)", "(quote (quote (quote x)))"), \
                 ("'(quote 'x 'y)", "(quote (quote (quote x) (quote y)))"), \
                 ("(a b c)", "(a b c)"), \
                 ("'(a b c)", "(quote (a b c))"), \
                 ("(a b . c)", "(a b . c)"), \
                 ("(a . (b . (c . ())))", "(a b c)"), \
                 ("(a . (b . (c . d)))", "(a b c . d)")]
        for case in cases:
            sexp = self.parser.parse(self.tokenizer.tokenize(case[0] + '\n'))[0]
            self.assertEqual(to_str(sexp), case[1])

    def testDeepParsing(self):
        """S-expressions that require deep recursion.
        """
        import sys
        sys.setrecursionlimit(50)

        cases = [("'"*1000 + "x", "(quote "*1000 + "x" + ")"*1000), \
                 ("(x . "*1000 + "()" + ")"*1000, "(" + "x " * 999 + "x)")]
        for case in cases:
            sexp = self.parser.parse(self.tokenizer.tokenize(case[0] + '\n'))[0]
            self.assertEqual(to_str(sexp), case[1])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ParserTest('testTokenizer'))
    suite.addTest(ParserTest('testTokenizeSingle'))
    suite.addTest(ParserTest('testLexemeParsing'))
    suite.addTest(ParserTest('testSexpParsing'))
    suite.addTest(ParserTest('testStringRepr'))
    suite.addTest(ParserTest('testDeepParsing'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
