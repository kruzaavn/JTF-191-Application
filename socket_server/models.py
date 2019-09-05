import socket
import selectors
import types
import json
import time
import random
import asyncio
import websocket


class SocketServer:

    def __init__(self, host=socket.gethostname(), port=8081, ):
        self.data = {}
        self.port = int(port)
        self.host = host
        self.selector = None
        self.purge_time = 3  # seconds
        self.socket = None
        self.listen_to_port()

    def accept_connection(self, sock):
        connection, address = sock.accept()
        print(f'accepted connection from {address}')
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, inb=b'', out=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(connection, events, data=data)

    def get_message(self, sock, data):

        buffer = sock.recv(10)

        if buffer:
            header = int(buffer.decode('utf-8'))
            buffer = sock.recv(header)

            self.process_data(buffer)

        else:
            print(f'closing connection to {data.addr}')
            self.selector.unregister(sock)
            sock.close()
            self.data = {}

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:

            self.get_message(sock, data)

    def process_data(self, data):
        chunks = data.split(b'\n')

        for chunk in chunks:
            if chunk:
                dictionary = json.loads(chunk)
                key = dictionary.pop('id')

                self.data[key] = dictionary

        self.cull_data()

    def cull_data(self):
        # consider deprecating
        max_time = max([self.data[x]['simtime'] for x in self.data])

        cull_list = [x for x in self.data if max_time - self.data[x]['simtime'] > self.purge_time]

        for item in cull_list:
            self.data.pop(item)

        print(self.data)

    def get_data(self):
        return json.dumps(self.data)

    def listen_to_port(self):
        self.selector = selectors.DefaultSelector()
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f'listening on {self.host}: {self.port}')
        self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

    def poll_connections(self):

        events = self.selector.select(timeout=None)

        for key, mask in events:

            if key.data:
                self.service_connection(key, mask)
            else:
                self.accept_connection(key.fileobj)

    def disconnect(self):
        pass
        # except KeyboardInterrupt:
        #     print('disconnecting clients and stopping server')
        #     quit()


class Client:

    def __init__(self, host=socket.gethostname(), port=8081):
        self.port = int(port)
        self.host = host
        self.buffer = b''
        self.time = 0
        self.connect()

    def connect(self):

        with socket.socket() as s:
            print(f'connecting to {self.host}: {self.port}')
            s.connect((self.host, self.port))

            while True:
                try:
                    time.sleep(1)
                    if not self.buffer:
                        self.gen_random_message()

                    self.send_buffer(s)
                    self.time += 1
                except (KeyboardInterrupt, BrokenPipeError):
                    print(f'disconnecting from {self.host}: {self.port}')
                    s.close()

    def construct_message(self, msg):

        header = bytes(f'{len(msg):< 10}', 'utf-8')
        self.buffer = header + msg

    def send_buffer(self, sock):

        print(f"sending {self.buffer}")
        self.buffer = self.buffer[sock.send(self.buffer):]

    def gen_random_message(self):

        data = {'id': random.randint(1, 11),
                'simtime': self.time,
                'message': "test " * random.randint(1, 10)}

        self.construct_message(bytes(json.dumps(data), 'utf-8'))

