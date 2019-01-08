#
# Copyright 2019 leenjewel
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


'''
TCP Client
'''

import tornado.tcpclient
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
from tornado import gen
from pykcp.kcp import KCP, IKCP_OVERHEAD, KCPSeg
from pykcp.stream import KCPStream, IKCP_HANDSHAKE_KEYWORD

class TCPClient(tornado.tcpclient.TCPClient):
    '''
    TCP Client
    '''

    def __init__(self, resolver=None):
        tornado.tcpclient.TCPClient.__init__(self, resolver=resolver)
        self.kcpstream = None

    @gen.coroutine
    def kcp_connect(self, host, port):
        '''
        Connect
        '''
        try:
            stream = yield self.connect(host, port)
            conv = yield stream.read_until(b'\n\n\n')
            self.kcpstream = KCPStream(KCP(int(conv.strip()), self.output), stream, None,\
                    ioloop=IOLoop.current(), callback=self.handle_message)
            yield stream.write(IKCP_HANDSHAKE_KEYWORD)
            yield stream.read_until(IKCP_HANDSHAKE_KEYWORD)
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

    @gen.coroutine
    def output(self, kcp, data):
        '''
        Output
        '''
        assert self.kcpstream
        assert self.kcpstream.stream
        yield self.kcpstream.stream.write(data)
