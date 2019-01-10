# PyKCP

[KCP protocol](https://github.com/skywind3000/kcp) by python

## Usage

### 1.Create KCP object

```python
from pykcp.kcp import KCP

conv = 12345678

def output(kcp, data):
    '''
    KCP lower layer protocol output function
    which will be called by KCP when it needs to send data
    '''
    pass

kcp = KCP(conv, output)
```

### 2.Call update in an interval

```python
import time

kcp.update(int(time.time() * 1000))
```

### 3.Input a lower layer data packet

```python
kcp.input(data)
```

### 4. Receive data from KCP

```
data = kcp.recv()
```

## Example

There is a simple TCP server and a simple TCP client in pykcp. It base from [tornado framework](https://tornadoweb.org).

For example a echo service like this

### echo server

```python
from pykcp.tcpserver import TCPServer
from tornado.ioloop import IOLoop

class TestServer(TCPServer):

    def handle_message(self, kcpstream, msg):
        print('RECV: %s' % msg)
        kcpstream.send(b'>>>> %s' %msg)

if __name__ == '__main__':
    server = TestServer()
    server.listen(8888)
```

### echo server

```python
from pykcp.tcpclient import TCPClient
from tornado.ioloop import IOLoop

class TestClient(TCPClient):

    def handle_connect(self):
        self.kcpstream.send(b'hello kcp')

    def handle_message(self, kcpstream, msg):
        print('RECV: %s' % msg)
        kcpstream.send(b'++++ %s' %msg)

if __name__ == '__main__':
    client = TestClient()
    client.kcp_connect('127.0.0.1', 8888)
```

