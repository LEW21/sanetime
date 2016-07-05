import unittest2 as unittest
from .. import time,delta

class SaneDeltaTest(unittest.TestCase):
    def test_construction(self):
        self.assertEqual(1+1000*(2+1000*(3+60*(4+60*(5+24*(6+7*7))))),delta(us=1,ms=2,s=3,m=4,h=5,md=6,mw=7))
        self.assertEqual(1,time(10)-time(9))
        self.assertEqual(-1,time(9)-time(10))

    def test_copy_construction(self):
        self.assertEqual(123, delta(delta(123)))

    def test_clone(self):
        self.assertEqual(123, delta(123).clone())

    def test_casting(self):
        self.assertEqual(123, int(delta(123)))
        self.assertEqual(123, int(delta(123)))
        self.assertEqual('6d 5h 4m 3.002001s', str(delta(us=1,ms=2,s=3,m=4,h=5,md=6)))
        self.assertEqual('6d 5h 4m 3.002001s', str(delta(us=1,ms=2,s=3,m=4,h=5,md=6)))
        self.assertEqual(hash(123), hash(delta(123)))

    def test_add(self):
        self.assertEqual(time(2012,1,1,0,0,0,1), time(2012,1,1)+delta(us=1))
        self.assertEqual(time(2012,1,1,0,0,0,1000), time(2012,1,1)+delta(ms=1))
        self.assertEqual(time(2012,1,1,0,0,1), time(2012,1,1)+delta(s=1))
        self.assertEqual(time(2012,1,1,0,1), time(2012,1,1)+delta(m=1))
        self.assertEqual(time(2012,1,1,1), time(2012,1,1)+delta(h=1))
        self.assertEqual(time(2012,1,2), time(2012,1,1)+delta(md=1))
        self.assertEqual(time(2012,1,8), time(2012,1,1)+delta(mw=1))
        self.assertEqual(time(2012,1,31,10,30), time(2012,1,1)+delta(mm=1))
        self.assertEqual(time(2012,12,31,6), time(2012,1,1)+delta(my=1))

    def test_construct_str(self):
        self.assertEqual('0.000001s', delta(us=1).construct_str())
        self.assertEqual('0.001000s', delta(ms=1).construct_str())
        self.assertEqual('0.001s', delta(ms=1).construct_str(max_positions=1))
        self.assertEqual('0.001s', delta(ms=1).construct_str(final_position='ms'))
        self.assertEqual('0.001002s', delta(ms=1,us=2).construct_str())
        self.assertEqual('3.001002s', delta(s=3,ms=1,us=2).construct_str())
        self.assertEqual('-3.001002s', (-delta(s=3,ms=1,us=2)).construct_str())
        self.assertEqual('3.001s', delta(s=3,ms=1,us=2).construct_str(final_position='ms'))
        self.assertEqual('3.002s', delta(s=3,ms=1,us=500).construct_str(final_position='ms'))
        self.assertEqual('3s', delta(s=3,ms=499,us=500).construct_str(final_position='s'))
        self.assertEqual('4s', delta(s=3,ms=500).construct_str(final_position='s'))
        self.assertEqual('4m 4s', delta(m=4,s=3,ms=500).construct_str(final_position='s'))
        self.assertEqual('4m4s', delta(m=4,s=3,ms=500).construct_str(final_position='s',separator=''))
        self.assertEqual('4m4s', delta(m=4,s=3,ms=500).construct_str(final_position='s',max_positions=2, separator=''))
        self.assertEqual('4m0s', delta(m=4).construct_str(final_position='s',max_positions=2, separator='',no_zero_positions=False))
        self.assertEqual('4m', delta(m=4).construct_str(final_position='s',max_positions=2, separator='',no_zero_positions=True))

    def test_arithmetic(self):
        self.assertEqual(delta(15), delta(3) * 5)
        self.assertEqual(15, 5 * delta(3))
        self.assertEqual(delta(3), delta(15)/5)
        self.assertEqual(3, 15 / delta(5))

    def test_unaries(self):
        self.assertEqual(-1, delta(-1).us)
        self.assertEqual(1, abs(delta(1)).us)
        self.assertEqual(1, abs(delta(-1)).us)
        self.assertEqual(-1, (-delta(1)).us)
        self.assertEqual(+1, (+delta(1)).us)


    def test_date_subtraction(self):
        self.assertEqual(24*60**2*10**6, time(2012,1,2) - time(2012,1,1))


    def test_sleep(self):
        t1 = time()
        t2 = time()
        self.assertTrue(t2-t1 < delta(ms=10))
        t1 = time()
        delta(ms=10).sleep()
        t2 = time()
        self.assertTrue(t2-t1 >= delta(ms=10))

