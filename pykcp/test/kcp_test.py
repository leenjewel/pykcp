#!/usr/bin/env python

from __future__ import absolute_import
import unittest
import time
from pykcp.kcp import KCP

class KCPTest(unittest.TestCase):

    def test_kcp(self):
        self.kcp1 = KCP(123, self.output_1)
        self.kcp2 = KCP(123, self.output_2)
        i = 0
        while True:
            self.assertEquals(self.kcp1.send('hello 1-%d' % i), 0)
            self.assertEquals(self.kcp2.send('hello 2-%d' % i), 0)
            time.sleep(1)
            self.kcp1.update(int(time.time()*1000))
            self.kcp2.update(int(time.time()*1000))
            print('kcp1 recv: '+str(self.kcp1.recv()))
            print('kcp2 recv: '+str(self.kcp2.recv()))
            i += 1
            if i > 5:
                break

    def output_1(self, kcp, data):
        print('kcp1 output: '+data)
        print(self.kcp2.input(data))

    def output_2(self, kcp, data):
        print('kcp2 output: '+data)
        print(self.kcp1.input(data))

if __name__ == '__main__':
    unittest.main()
