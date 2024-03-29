import os
import requests
import datetime
import json
import pprint
from tornado.tcpserver import TCPServer
from tornado.websocket import websocket_connect, WebSocketClosedError
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop


def log(string):
    print(f'{datetime.datetime.now()}: {string}', flush=True)

user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')


class GCIRelay(TCPServer):

    async def handle_stream(self, stream, address):

        websocket = None

        # configure server
        try:
            server_config = json.loads(await stream.read_until(b"\n"))

            pprint.pp(server_config)

            session = requests.session()
            session.auth = (user, password)

            self.register_or_update_server(session, server_config)
            websocket = await self.connect_websocket(server_config)

        except StreamClosedError:
            pass

        # connect to websocket and push data

        if websocket:

            while True:
                try:
                    data = json.loads(await stream.read_until(b"\n"))
                    await websocket.write_message(data)

                except StreamClosedError:
                    log(f"Stream closed disconnecting {server_config['name']}")
                    websocket.close()
                    break

                except WebSocketClosedError:
                    log(f"Websocket closed disconnecting {server_config['name']}")
                    stream.close()
                    break

    def register_or_update_server(self, session, config):

        registered_servers = [x for x in session.get('http://api-server:8000/api/gci/server/list/').json() if x['name'] == config['name']]

        server_date = {k.lower(): v for k, v in config.pop('date').items()}
        server_time = config.pop('start_time')

        dt = datetime.datetime(**server_date) + datetime.timedelta(seconds=server_time)

        config['start_time'] = dt.isoformat()

        if registered_servers:

            id = registered_servers[0]['id']

            r = session.put(f'http://api-server:8000/api/gci/server/detail/{id}/', data=config)

            if r.status_code < 300:
                log(f'updated server {config["name"]}')
            else:
                log(r.json())

        else:

            r = session.post(f'http://api-server:8000/api/gci/server/list/', data=config)

            if r.status_code < 300:
                log(f'registered server {config["name"]}')
            else:
                log(r.json())

    async def connect_websocket(self, config):

        websocket_url = f"ws://api-server:8000/ws/gci/{config['name'].replace(' ', '_')}/"
        websocket = await websocket_connect(websocket_url)

        log(f'connected to websocket at {websocket_url}')

        return websocket


if __name__ == '__main__':

    server = GCIRelay()
    port = int(os.getenv('PORT', 7224))
    log(f'listening on {port}')
    server.bind(port)
    server.start()
    IOLoop.current().start()
