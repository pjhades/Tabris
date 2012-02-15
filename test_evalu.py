# -*- coding: utf-8 -*-

import unittest
import evalu
import enviro
from typedef import *
from number import *
from parser import Tokenizer, parse 
from pair import to_str

class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.tk = Tokenizer()
        self.env = enviro.Env()

    def tearDown(self):
        self.tk = None
        self.env = None

    def p(self, code):
        "Taste sweet? >_< "
        return parse(self.tk.tokenize_single(code + "\n"))[0]

    def testSelfEvaluating(self):
        exp = self.p('"foo"')
        self.assertEqual(String('foo'), evalu.eval(exp, self.env))

        exp = self.p('#f')
        self.assertEqual(Boolean(False), evalu.eval(exp, self.env))

        exp = self.p('7/6-8i')
        self.assertEqual(Complex(Rational(7, 6), Rational(-8, 1)), \
                         evalu.eval(exp, self.env))

    def testQuote(self):
        exp = self.p("'''x")
        self.assertEqual('(quote (quote x))', to_str(evalu.eval(exp, self.env)))

        exp = self.p("'(quote 'x quote)")
        self.assertEqual('(quote (quote x) quote)', to_str(evalu.eval(exp, self.env)))

    def testDefine(self):
        evalu.eval(self.p('(define foo 111)'), self.env)
        exp = self.p('foo')
        self.assertEqual(Rational(111, 1), evalu.eval(exp, self.env))

    def testSet(self):
        evalu.eval(self.p('(define bar 111)'), self.env)
        exp = self.p('bar')
        self.assertEqual(Rational(111, 1), evalu.eval(exp, self.env))
        evalu.eval(self.p('(set! bar 999)'), self.env)
        exp = self.p('bar')
        self.assertEqual(Rational(999, 1), evalu.eval(exp, self.env))

    def testLambda(self):
        evalu.eval(self.p('(define foo (lambda x x))'), self.env)
        func = evalu.eval(self.p('foo'), self.env)
        print('params:', to_str(func.params))
        print('body:', func.body)
        print('is_prim:', func.is_prim)
        print('is_var_args:', func.is_var_args)
        for var in func.env.bindings:
            print(var, func.env.bindings[var])


def suite():
    #TODO:
    # add unit test here
    suite = unittest.TestSuite()

    # syntax transformation
    #suite.addTest(EvaluatorTest('testSelfEvaluating'))
    #suite.addTest(EvaluatorTest('testQuote'))
    #suite.addTest(EvaluatorTest('testDefine'))
    #suite.addTest(EvaluatorTest('testSet'))
    suite.addTest(EvaluatorTest('testLambda'))

    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
