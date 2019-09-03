import socket
import selectors
import types
import json


class Server:

    def __init__(self, port=8081, host=socket.gethostname()):
        self.data = {}
        self.port = port
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

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            inbound_data = sock.recv(4096)
            if inbound_data:
                self.process_data(inbound_data)
            else:
                print(f'closing connection to {data.addr}')
                self.selector.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            pass

    def process_data(self, data):
        chunks = data.split(b'n')

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

    def listen_to_port(self):
        self.selector = selectors.DefaultSelector()

        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen(5)
            print(f'listening on {self.host}: {self.port}')
            s.setblocking(False)
            self.selector.register(s, selectors.EVENT_READ, data=None)

            while True:

                events = self.selector.select(timeout=None)

                for key, mask in events:

                    if key.data:
                        self.service_connection(key, mask)
                    else:
                        self.accept_connection(key.fileobj)


class Client:

    def __init__(self, port=8081, host=socket.gethostname()):
        self.port = port
        self.host = host

class Message:

    def __init__(self):
        pass