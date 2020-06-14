import os
import uuid
import datetime
import json
from tornado.tcpserver import TCPServer
from tornado.websocket import websocket_connect
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop


def log(string):
    print(f'{datetime.datetime.now()}: {string}')


class TCPeter(TCPServer):

    async def handle_stream(self, stream, address):
        log(f'connected to {address[0]}')

        connection_config = json.loads(await stream.read_until(b"\n"))

        websocket_url = f"ws://api-server:8000/ws/gci/{connection_config['name'].replace(' ', '_')}/"
        log(f'establishing websocket connection to {websocket_url}')
        websocket = await websocket_connect(websocket_url)

        while True:
            try:
                data = await stream.read_until(b"\n")
                message = {"message": json.loads(data)}
                await websocket.write_message(json.dumps(message))

            except StreamClosedError:
                break


if __name__ == '__main__':

    server = TCPeter()
    port = int(os.getenv('PORT', 7224))
    log(f'listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
