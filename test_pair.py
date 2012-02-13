# -*- coding: utf-8 -*-

import unittest
from pair import *

class PairTest(unittest.TestCase):
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

    def testLength(self):
        self.assertEqual(pair.get_length(pair.make_list(1, 2, 3)), 3)
        self.assertEqual(pair.get_length(pair.make_list(1, (2, 2), 3)), 3)
        self.assertEqual(pair.get_length(pair.make_list()), 0)
        self.assertEqual(pair.get_length(pair.NIL), 0)

    def testAppend(self):
        p1 = pair.make_list(1, 2, 3)
        p2 = pair.make_list(4, 5)
        p3 = pair.cons(6, 7)
        p4 = pair.make_list(1, pair.cons(2, 3), 4)

        self.assertEqual(pair.append_lst(p1, p2), pair.make_list(1, 2, 3, 4, 5))
        self.assertEqual(pair.append_lst(p1, p3), \
                pair.cons(1, pair.cons(2, pair.cons(3, p3))))
        self.assertEqual(pair.append_lst(pair.NIL, 123), 123)
        self.assertEqual(pair.append_lst(pair.NIL, p4), p4)
        self.assertEqual(pair.append_lst(p4, p2), \
                pair.cons(1, pair.cons(pair.cons(2, 3), \
                pair.cons(4, pair.cons(4, pair.cons(5, pair.NIL))))))
        self.assertEqual(pair.append_lst(), pair.NIL)

    def testReverse(self):
        p1 = pair.make_list(1, 2, 3, 4, 5)
        p2 = pair.make_list(1, pair.cons(2, 3), 4)
        
        self.assertEqual(pair.reverse_lst(p1), pair.make_list(5, 4, 3, 2, 1))
        self.assertEqual(pair.reverse_lst(p2), pair.make_list(4, pair.cons(2, 3), 1))
        self.assertEqual(pair.reverse_lst(pair.NIL), pair.NIL)

    def testListTail(self):
        p1 = pair.make_list(1, 2, 3, 4)
        p2 = pair.cons(1, 2)
        p3 = pair.cons(1, pair.cons(2, pair.cons(3, 4)))

        self.assertEqual(pair.get_list_tail(p1, 2), pair.make_list(3, 4))
        self.assertEqual(pair.get_list_tail(p1, 3), pair.make_list(4))
        self.assertEqual(pair.get_list_tail(p1, 4), pair.NIL)
        self.assertEqual(pair.get_list_tail(p2, 0), pair.cons(1, 2))
        self.assertEqual(pair.get_list_tail(p2, 1), 2)
        self.assertEqual(pair.get_list_tail(p3, 2), pair.cons(3, 4))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(PairTest('testPairCreating'))
    suite.addTest(PairTest('testConsing'))
    suite.addTest(PairTest('testListMaking'))
    suite.addTest(PairTest('testCarCdr'))
    suite.addTest(PairTest('testLength'))
    suite.addTest(PairTest('testAppend'))
    suite.addTest(PairTest('testReverse'))
    suite.addTest(PairTest('testListTail'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
