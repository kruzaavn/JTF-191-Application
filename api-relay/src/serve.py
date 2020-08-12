import os
import requests
import datetime
import json
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop


def log(string):
    print(f'{datetime.datetime.now()}: {string}', flush=True)


class APIRelay(TCPServer):

    async def handle_stream(self, stream, address):
        log(f'connected to {address[0]}')

        while True:
            try:
                data = await stream.read_until(b"\n")
                data = json.loads(data)
                log(data)
                r = requests.post('http://api-server:8000/api/roster/stats/', data=data)

            except StreamClosedError:
                log(f'{address[0]} disconnected')
                break


if __name__ == '__main__':

    server = APIRelay()
    port = int(os.getenv('PORT', 7225))
    log(f'listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
