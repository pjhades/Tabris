# -*- coding: utf-8 -*-

import unittest
import trampoline

class TramplineTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTrampoline(self):
        # trampolined factorial
        def fact(n, ans):
            if n < 2:
                return trampoline.fall(ans)
            else:
                return trampoline.bounce(fact, n-1, n*ans)

        ans = trampoline.pogo_stick(fact(5, 1))
        self.assertEqual(ans, 120)

        ans = trampoline.pogo_stick(fact(1, 1))
        self.assertEqual(ans, 1)


        # member search
        def memq(target, lst):
            if lst == []:
                return trampoline.fall(False)
            elif target == lst[0]:
                return trampoline.fall(True)
            else:
                return trampoline.bounce(memq, target, lst[1:])

        ans = trampoline.pogo_stick(memq(3, [1, 2, 3, 4, 5]))
        self.assertEqual(ans, True)

        ans = trampoline.pogo_stick(memq(3, [1, 2, 4, 5, 6]))
        self.assertEqual(ans, False)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TramplineTest('testTrampoline'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
