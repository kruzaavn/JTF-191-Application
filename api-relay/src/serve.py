import os
import requests
import datetime
import json
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
from pprint import pprint


def log(string):
    print(f'{datetime.datetime.now()}: {string}', flush=True)


user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')


host = 'http://api-server:8000'


def get_url(path, host=host):

    return f'{host}{path}'


class APIRelay(TCPServer):

    async def handle_stream(self, stream, address):
        source = f'{address[0]}:{address[1]}'
        log(f'connected to {source}')

        session = requests.session()

        if user and password:
            session.auth = (user, password)

        while True:
            try:
                data = await stream.read_until(b"\n")
                data = json.loads(data)

                event = data.get('event')
                stores = data.get('stores')

                if event and event != 'keepalive':

                    log(f'{source} {pprint(data)}')

                    if stores:
                        r = session.post(get_url('/api/roster/stores/'), json=data)
                    else:
                        r = session.post(get_url('/api/roster/stats/'), json=data)

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
