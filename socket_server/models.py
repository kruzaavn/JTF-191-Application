import socket
import selectors
import types
import json


class Server:

    def __init__(self, host=socket.gethostname(), port=8081, ):
        self.data = {}
        self.port = int(port)
        self.host = host
        self.selector = None
        self.purge_time = 3  # seconds
        self.listen_to_port()

    def accept_connection(self, sock):
        connection, address = sock.accept()
        print(f'accepted connection from {address}')
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, inb=b'', out=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(connection, events, data=data)

    def get_message(self, sock, data):

        buffer = sock.recv(1024)

        if buffer:
            header = int(buffer[:10].decode('utf-8'))
            buffer = buffer[10:]

            while len(buffer) < header:
                buffer += sock.recv(1024)

            self.process_data(buffer)

        else:
            print(f'closing connection to {data.addr}')
            self.selector.unregister(sock)
            sock.close()



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

        max_time = max([self.data[x]['simtime'] for x in self.data])

        cull_list = [x for x in self.data if max_time - self.data[x]['simtime'] > self.purge_time]

        for item in cull_list:
            self.data.pop(item)

        print(self.data)

    def listen_to_port(self):
        self.selector = selectors.DefaultSelector()

        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(5)
            print(f'listening on {self.host}: {self.port}')
            s.setblocking(False)
            self.selector.register(s, selectors.EVENT_READ, data=None)

            while True:

                events = self.selector.select(timeout=None)

                try:
                    for key, mask in events:

                        if key.data:
                            self.service_connection(key, mask)
                        else:
                            self.accept_connection(key.fileobj)
                except KeyboardInterrupt:
                    print('disconnecting clients and stopping server')
                    quit()


class Client:

    def __init__(self, host=socket.gethostname(), port=8081):
        self.port = int(port)
        self.host = host
        self.buffer = b''
        self.connect()


    def connect(self):

        with socket.socket() as s:
            print(f'connecting to {self.host}: {self.port}')
            s.connect((self.host, self.port))

            msg = b'{"id": 1, "simtime": 1, "message": "test test"}'

            self.construct_message(msg)

            while True:
                try:
                    if self.buffer:
                        self.send_buffer(s)

                except KeyboardInterrupt:
                    print(f'disconnecting from {self.host}: {self.port}')

    def construct_message(self, msg):

        header = bytes(f'{len(msg):< 10}', 'utf-8')
        self.buffer = header + msg

    def send_buffer(self, sock):

        self.buffer = self.buffer[sock.send(self.buffer):]
