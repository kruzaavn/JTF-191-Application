import os
import uuid
from tornado.tcpserver import TCPServer
from tornado.websocket import websocket_connect
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
import datetime

websockets = {}


class TCPeter(TCPServer):

    async def handle_stream(self, stream, address):

        websockets[address[0]] = websocket_connect(f'ws://localhost:8000/ws/chat/{uuid.uuid4()}/')

        while True:
            try:
                data = await stream.read_until(b"\n")
                print(data, websockets[address[0]])

            except StreamClosedError:
                break


if __name__ == '__main__':

    server = TCPeter()
    port = int(os.getenv('PORT', 7224))
    print(f'{datetime.datetime.now()} listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
