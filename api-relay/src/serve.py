import os
import requests
import datetime
import json
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop


def log(string):
    print(f'{datetime.datetime.now()}: {string}', flush=True)


user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')


class APIRelay(TCPServer):

    async def handle_stream(self, stream, address):
        source = f'{address[0]}:{address[1]}'
        log(f'connected to {source}')

        while True:
            try:
                data = await stream.read_until(b"\n")
                data = json.loads(data)

                event = data.get('event')

                if not event or event != 'keepalive':
                    log(f'{source} {data}')
                    r = requests.post('http://api-server:8000/api/roster/stats/', data=data)

            except StreamClosedError:
                log(f'{source} disconnected')
                break


if __name__ == '__main__':

    server = APIRelay()
    port = int(os.getenv('PORT', 7225))
    log(f'listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
