# -*- coding: utf-8 -*-

import unittest
import pair

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPairCreating(self):
        self.assertEqual(pair.Pair([1, 2]), [1, 2])
        self.assertEqual(pair.Pair([[1, 2], [3, 4]]), [[1, 2], [3, 4]])

    def testConsing(self):
        self.assertEqual(pair.cons(1, 2), [1, 2])
        self.assertEqual(pair.cons(1, [2, 3]), [1, [2, 3]])
        self.assertEqual(pair.cons([1, 2], [3, 4]), [[1, 2], [3, 4]])

    def testListMaking(self):
        self.assertEqual(pair.make_list(1, 2), [1, [2, []]])
        self.assertEqual(pair.make_list(1, [2, 3]), [1, [[2, [3, []]], []])
        self.assertEqual(pair.make_list([1, 2], [3, 4]), [[1, [2, []]], [[3, [4, []]], []]])

    def testCar(self):
        self.assertEqual(pair.car(pair.cons(1, 2)), 1)
        self.assertEqual(pair.car(pair.cons([1, 2], 3)), [1, 2])

    def testCdr(self):
        self.assertEqual(pair.cdr(pair.cons(1, 2)), 2)
        self.assertEqual(pair.cdr(pair.cons(1, [2, 3])), [2, 3])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TokenizerTest('testPairCreating'))
    suite.addTest(TokenizerTest('testConsing'))
    suite.addTest(TokenizerTest('testListMaking'))
    suite.addTest(TokenizerTest('testCar'))
    suite.addTest(TokenizerTest('testCdr'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
