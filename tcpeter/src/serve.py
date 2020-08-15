import os
import requests
import datetime
import json
from tornado.tcpserver import TCPServer
from tornado.websocket import websocket_connect
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop


def log(string):
    print(f'{datetime.datetime.now()}: {string}', flush=True)


class TCPeter(TCPServer):

    async def handle_stream(self, stream, address):
        source = f'{address[0]}:{address[1]}'
        log(f'connected to {source}')

        connection_config = json.loads(await stream.read_until(b"\n"))

        log(f"registering connection {connection_config['name']} for {source}")

        r = requests.post('http://api-server:8000/api/gci/server/detail/',
                          data={'name': connection_config['name'].replace(' ', '_'),
                                'ip': address[0]})

        if r.status_code == 201:

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
        else:
            log(f"unable to register {connection_config['name']} for {source}")


if __name__ == '__main__':

    server = TCPeter()
    port = int(os.getenv('PORT', 7224))
    log(f'listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
