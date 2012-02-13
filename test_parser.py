# -*- coding: utf-8 -*-

import unittest
import parser
import typedef
import number
import pair
import trampoline

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = parser.Tokenizer()

    def tearDown(self):
        self.tokenizer = None

    def testTokenizer(self):
        """Test the normal tokenizer."""

        cases = [("lambda", [("lambda", "symbol")]), \
                 ("12345", [("12345", "integer")]), \
                 ("i", [("i", "symbol")]), \
                 ("-4/56", [("-4/56", "fraction")]), \
                 ("0.", [("0.", "float")]), \
                 (".", [(".", ".")]), \
                 ("(", [("(", "(")]), \
                 (")", [(")", ")")]), \
                 ("'", [("'", "'")]), \
                 ("-6.2350-0i", [("-6.2350-0i", "complex")]), \
                 ("+i", [("+i", "complex")]), \
                 ("-i", [("-i", "complex")]), \
                 ("\"this is a string\"", [("\"this is a string\"", "string")]), \
                 ("\"a string\nspans multiple\nlines\"", [("\"a string\nspans multiple\nlines\"", "string")]), \
                 ("'''x", [("'", "'"), ("'", "'"), ("'", "'"), ("x", "symbol")]), \
                 ("'\n'\n'\nx", [("'", "'"), ("'", "'"), ("'", "'"), ("x", "symbol")]), \
                 ("'(a . (b . ()))", [("'", "'"), ("(", "("), ("a", "symbol"), \
                                      (".", "."), ("(", "("), ("b", "symbol"), \
                                      (".", "."), ("(", "("), (")", ")"), \
                                      (")", ")"), (")", ")")]), \
                 ("; this is \"comm\"ent", []), \
                 ('";not comment"', [('";not comment"', "string")]), \
                 ("#t", [("#t", "boolean")])]

        for case in cases:
            self.tokenizer.tokenize(case[0] + '\n')
            self.assertEqual(self.tokenizer.get_tokens(), case[1])

    def testTokenizeSingle(self):
        """Test the single-line tokenizer."""

        cases = [("lambda", [("lambda", "symbol")]), \
                 ("-4/56", [("-4/56", "fraction")]), \
                 ("0.", [("0.", "float")]), \
                 ("-6.2350-0i", [("-6.2350-0i", "complex")]), \
                 ("-i", [("-i", "complex")]), \
                 ("\"this is a string\"", [("\"this is a string\"", "string")])]

        for case in cases:
            self.assertEqual(self.tokenizer.tokenize_single(case[0] + '\n'), case[1])

    def testFileTokenizing(self):
        """Test tokenizing the source file."""

        tokens = [("(", "("), ("once", "symbol"), ("upon", "symbol"), \
                  ("(", "("), ("a", "symbol"), ("time", "symbol"), \
                  ("'", "'"), ("there", "symbol"), ("(", "("), \
                  ("+", "symbol"), ("1/2", "fraction"), ("4.5-7i", "complex"), \
                  (")", ")"), ("1.", "float"), (")", ")"), \
                  ("(", "("), ("was", "symbol"), ("a", "symbol"), \
                  ('"magic\nian"', "string"), (")", ")"), (")", ")")]

        with open('test/token.scm', 'r') as fin:
            for line in fin:
                self.tokenizer.tokenize(line)
            self.assertEqual(self.tokenizer.get_tokens(), tokens)

    def testLexemeParsing(self):
        """Test parsing lexemes"""

        self.tokenizer.tokenize("aaa" + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0], "aaa")

        self.tokenizer.tokenize("#t" + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].value, True)

        self.tokenizer.tokenize('"helloworld"' + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].value, "helloworld")

        self.tokenizer.tokenize('123' + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].numer, 123)
        self.assertEqual(obj[0].denom, 1)

        self.tokenizer.tokenize('-4/6' + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].numer, -2)
        self.assertEqual(obj[0].denom, 3)

        self.tokenizer.tokenize('.0' + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].value, 0.0)

        self.tokenizer.tokenize('+i' + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].real.numer, 0)
        self.assertEqual(obj[0].real.denom, 1)
        self.assertEqual(obj[0].imag.numer, 1)
        self.assertEqual(obj[0].imag.denom, 1)

        self.tokenizer.tokenize('-4/5+6/3i' + "\n")
        obj = parser.parse(self.tokenizer.get_tokens())
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj[0].real.numer, -4)
        self.assertEqual(obj[0].real.denom, 5)
        self.assertEqual(obj[0].imag.numer, 2)
        self.assertEqual(obj[0].imag.denom, 1)

    def testSexpParsing(self):
        """Test parsing S-expressions."""

        cases = [("x", "x"), \
                 ("(x)", ["x", []]), \
                 ("(x y)", ["x", ["y", []]]), \
                 ("(x (y))", ["x", [["y", []], []]]), \
                 ("(x . y)", ["x", "y"]), \
                 ("(x y . z)", ["x", ["y", "z"]]), \
                 ("(x (y . z) w)", ["x", [["y", "z"], ["w", []]]])]

        for case in cases:
            sexp = parser.parse(self.tokenizer.tokenize_single(case[0] + '\n'))[0]
            self.assertEqual(sexp, case[1])

    def testStringRepr(self):
        """Test the string representation of the parsed S-expressions."""

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
            sexp = parser.parse(self.tokenizer.tokenize_single(case[0] + '\n'))[0]
            self.assertEqual(pair.to_str(sexp), case[1])

    def testDeepParsing(self):
        """S-expressions that require deep recursion."""
        
        import sys
        sys.setrecursionlimit(30)

        cases = [("'"*1000 + "x", "(quote "*1000 + "x" + ")"*1000), \
                 ("(x . "*1000 + "()" + ")"*1000, "(" + "x " * 999 + "x)")]

        for case in cases:
            sexp = parser.parse(self.tokenizer.tokenize_single(case[0] + '\n'))[0]
            self.assertEqual(pair.to_str(sexp), case[1])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ParserTest('testTokenizer'))
    suite.addTest(ParserTest('testTokenizeSingle'))
    suite.addTest(ParserTest('testFileTokenizing'))
    suite.addTest(ParserTest('testLexemeParsing'))
    suite.addTest(ParserTest('testSexpParsing'))
    suite.addTest(ParserTest('testStringRepr'))
    suite.addTest(ParserTest('testDeepParsing'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
