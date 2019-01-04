#!/usr/bin/env python

from __future__ import absolute_import
from pykcp.tcpclient import TCPClient
from tornado.ioloop import IOLoop

class TestClient(TCPClient):

    def handle_connect(self):
        self.kcpstream.send('hello kcp')

    def handle_message(self, kcpstream, msg):
        print('RECV: %s' % msg)
        kcpstream.send('++++ %s' %msg)

if __name__ == '__main__':
    client = TestClient()
    client.kcp_connect('127.0.0.1', 8888)
    IOLoop.current().start()

