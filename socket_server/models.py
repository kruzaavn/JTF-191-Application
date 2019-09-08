import socket
import json
import time
import random
import asyncio

import tornado.websocket as ws


class DummyClient:

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


class WSHandler(ws.WebSocketHandler):

    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print(f'New Connection Established, clients connected {len(self.clients)}')
        self.set_nodelay(True)
        WSHandler.clients.append(self)

    def on_close(self):
        print(f'Connection Closed, clients connected {len(self.clients)}')
        WSHandler.clients.remove(self)
        del self

    @classmethod
    def write_to_clients(cls, message):
        for client in cls.clients:
            client.write_message(message)


class TCPProtocol(asyncio.Protocol):

    transport = None

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):
        print(data)
        WSHandler.write_to_clients(data.decode())

