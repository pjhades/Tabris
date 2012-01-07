# -*- coding: utf-8 -*-

import unittest
import analyzer
import typedef
from parser import Tokenizer, parse 

class AnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.tk = Tokenizer()

    def tearDown(self):
        self.tk = None

    def testDefine(self):
        exp = parse(self.tk.tokenize_single("(define foo bar)" + "\n"))[0]
        self.assertEqual(analyzer.get_define_var(exp), typedef.Symbol('foo'))
        self.assertEqual(analyzer.get_define_val(exp), typedef.Symbol('bar'))

        exp = parse(self.tk.tokenize_single("(define (inc x) (+ x 1))" + "\n"))[0]
        #print(exp)
        #self.assertEqual(analyzer.get_define_var(exp), typedef.Symbol('inc'))
        #print(analyzer.get_define_val(exp))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AnalyzerTest('testDefine'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
