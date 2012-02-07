# -*- coding: utf-8 -*-

import unittest
import evalu
from typedef import Symbol
from parser import Tokenizer, parse 
from pair import to_str

class AnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.tk = Tokenizer()

    def tearDown(self):
        self.tk = None

    def testDefine(self):
        exp = parse(self.tk.tokenize_single("(define foo bar)" + "\n"))[0]
        self.assertEqual(evalu.get_define_var(exp), Symbol('foo'))
        self.assertEqual(evalu.get_define_val(exp), Symbol('bar'))

        exp = parse(self.tk.tokenize_single("(define (inc x) (+ x 1))" + "\n"))[0]
        self.assertEqual(evalu.get_define_var(exp), Symbol('inc'))

    def testCond(self):
        exp = parse(self.tk.tokenize_single("(cond ((a b) c) (else d))" + "\n"))[0]
        self.assertEqual(to_str(evalu.cond_to_if(exp)), "(if (a b) c d)")

        exp = parse(self.tk.tokenize_single("(cond ((a b) c) (d e) (f g))" + "\n"))[0]
        self.assertEqual(to_str(evalu.cond_to_if(exp)), "(if (a b) c (if d e (if f g #f)))")

        exp = parse(self.tk.tokenize_single("(cond (a b) (c (d e) (f g)))" + "\n"))[0]
        self.assertEqual(to_str(evalu.cond_to_if(exp)), "(if a b (if c (begin (d e) (f g)) #f))")

    def testLet(self):
        exp = parse(self.tk.tokenize_single("(let ((a 1) (b 2)) (x y) (y z))" + "\n"))[0]
        self.assertEqual(to_str(evalu.let_to_call(exp)), "((lambda (a b) (x y) (y z)) 1 2)")

        exp = parse(self.tk.tokenize_single("(let () (a b))" + "\n"))[0]
        self.assertEqual(to_str(evalu.let_to_call(exp)), "((lambda () (a b)))")

    def testAnalyzeSelfEvaluating(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AnalyzerTest('testDefine'))
    suite.addTest(AnalyzerTest('testCond'))
    suite.addTest(AnalyzerTest('testLet'))
    suite.addTest(AnalyzerTest('testAnalyzeSelfEvaluating'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
