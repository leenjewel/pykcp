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
