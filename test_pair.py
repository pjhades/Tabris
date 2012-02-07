# -*- coding: utf-8 -*-

import unittest
from pair import *

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPairCreating(self):
        self.assertEqual(Pair([1, 2]), [1, 2])
        self.assertEqual(Pair([[1, 2], [3, 4]]), [[1, 2], [3, 4]])

    def testConsing(self):
        self.assertEqual(cons(1, 2), [1, 2])
        self.assertEqual(cons(1, [2, 3]), [1, [2, 3]])
        self.assertEqual(cons([1, 2], [3, 4]), [[1, 2], [3, 4]])

    def testListMaking(self):
        self.assertEqual(make_list(1, 2), [1, [2, []]])
        self.assertEqual(make_list(1, [2, 3]), [1, [[2, 3], []]])
        self.assertEqual(make_list([1, 2], [3, 4]), [[1, 2], [[3, 4], []]])

    def testCarCdr(self):
        self.assertEqual(car(cons(1, 2)), 1)
        self.assertEqual(car(cons([1, 2], 3)), [1, 2])
        self.assertEqual(cdr(cons(1, 2)), 2)
        self.assertEqual(cdr(cons(1, [2, 3])), [2, 3])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TokenizerTest('testPairCreating'))
    suite.addTest(TokenizerTest('testConsing'))
    suite.addTest(TokenizerTest('testListMaking'))
    suite.addTest(TokenizerTest('testCarCdr'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
