#!/usr/bin/env python

'''
TCP Client
'''

import time
import tornado.tcpclient
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
from tornado import gen
from pykcp.kcp import KCP, IKCP_OVERHEAD, KCPSeg
from pykcp.stream import KCPStream

class TCPClient(tornado.tcpclient.TCPClient):
    '''
    TCP Client
    '''

    def __init__(self, timeout=10, resolver=None):
        tornado.tcpclient.TCPClient.__init__(self, resolver=resolver)
        self.kcpstream = None
        self.timeout = timeout

    @gen.coroutine
    def kcp_connect(self, host, port):
        try:
            stream = yield self.connect(host, port)
            conv = yield stream.read_until(b'\n\n\n')
            self.kcpstream = KCPStream(KCP(int(conv.strip()), self.output), stream, None,\
                    timeout=self.timeout, ioloop=IOLoop.current(), callback=self.handle_message)
            yield stream.write('ok\n\n\n')
            yield stream.read_until('ok\n\n\n')
            self.handle_connect()
            self.kcpstream.update()
            seg = None
            head = None
            while True:
                try:
                    if seg is None:
                        head = yield stream.read_bytes(IKCP_OVERHEAD)
                        seg = KCPSeg.decode(head)
                    else:
                        data = yield stream.read_bytes(seg.len)
                        self.kcpstream.kcp.input(head+data)
                        head = None
                        seg = None
                except StreamClosedError:
                    break
        finally:
            if self.kcpstream:
                self.kcpstream.close()

    def handle_connect(self):
        '''
        Handle connect
        '''
        raise NotImplementedError()

    def handle_message(self, kcpstream, message):
        '''
        Handle message
        '''
        raise NotImplementedError()

    def output(self, kcp, data):
        '''
        Output
        '''
        assert self.kcpstream
        assert self.kcpstream.stream
        self.kcpstream.stream.write(data, callback=self.write_callback)

    def write_callback(self, *args, **kw_args):
        '''
        Write callback
        '''
        pass
