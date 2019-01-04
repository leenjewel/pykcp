#!/usr/bin/env python

'''
Stream
'''

import time

class KCPStream(object):
    '''
    KCP stream
    '''

    __slot__ = ('kcp', 'stream', 'address',\
            'timeout_handle', 'ioloop', 'timeout', 'message_callback')

    def __init__(self, kcp, stream, address, ioloop, timeout=10, callback=None):
        self.stream = stream
        self.address = address
        self.kcp = kcp
        self.timeout_handle = None
        self.ioloop = ioloop
        self.timeout = timeout
        self.message_callback = callback

    def get_timeout(self):
        '''
        Get timeout
        '''
        return time.time() + (self.timeout / 1000.0)

    def update(self):
        assert self.ioloop
        assert self.kcp
        self.kcp.update(int(time.time() * 1000))
        data = self.kcp.recv()
        if data:
            self.handle_message(data)
        self.timeout_handle = \
                self.ioloop.add_timeout(self.get_timeout(), self.update)

    def send(self, data):
        '''
        Send
        '''
        assert self.kcp
        self.kcp.send(data)

    def close(self):
        if self.ioloop and self.timeout_handle:
            self.ioloop.remove_timeout(self.timeout_handle)

    def handle_message(self, message):
        '''
        Handle message
        '''
        if callable(self.message_callback):
            self.message_callback(self, message)
