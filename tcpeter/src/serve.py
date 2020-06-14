import os
import uuid
import datetime
import json
from tornado.tcpserver import TCPServer
from tornado.websocket import websocket_connect
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop


websockets = {}


def log(string):
    return f'{datetime.datetime.now}:{string}'


class TCPeter(TCPServer):

    async def handle_stream(self, stream, address):
        log(f'connected to {address[0]}')
        websockets[address[0]] = await websocket_connect(f'ws://172.18.0.1:8000/ws/chat/BOB/')
        log(f'{websockets[address[0]]}')

        while True:
            try:
                data = await stream.read_until(b"\n")
                message = {"message": json.loads(data)}
                websockets[address[0]].write_message(json.dumps(message))

            except StreamClosedError:
                break


if __name__ == '__main__':

    server = TCPeter()
    port = int(os.getenv('PORT', 7224))
    log(f'listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
