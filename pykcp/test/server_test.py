#!/usr/bin/env python

from __future__ import absolute_import
from pykcp.tcpserver import TCPServer
from tornado.ioloop import IOLoop

class TestServer(TCPServer):

    def handle_message(self, kcpstream, msg):
        print('RECV: %s' % msg)
        kcpstream.send('>>>> %s' %msg)

if __name__ == '__main__':
    server = TestServer()
    server.listen(8888)
    IOLoop.current().start()
