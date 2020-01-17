import asyncio

import tornado.websocket as ws


class WSHandler(ws.WebSocketHandler):

    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        self.set_nodelay(True)
        WSHandler.clients.append(self)
        print(f'New Connection Established, clients connected {len(self.clients)}')

    def on_close(self):
        WSHandler.clients.remove(self)
        print(f'Connection Closed, clients connected {len(self.clients)}')
        del self

    def close(self, code: int = None, reason: str = None) -> None:
        WSHandler.clients.remove(self)
        print(f'Connection Closed, clients connected {len(self.clients)}')
        del self

    @classmethod
    def write_to_clients(cls, message):
        for client in cls.clients:
            try:
                client.write_message(message)
            except ws.WebSocketClosedError:
                client.close()


class TCPProtocol(asyncio.Protocol):

    transport = None

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):
        WSHandler.write_to_clients(data.decode())


