import os
import requests
import datetime
import json
import pprint
from tornado.tcpserver import TCPServer
from tornado.websocket import websocket_connect
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

        while websocket:
            try:
                data = json.loads(await stream.read_until(b"\n"))
                await websocket.write_message(data)

            except StreamClosedError:
                log(f"disconnect websocket")
                websocket.close()
                websocket = None

        # log(f"registering connection {connection_config['name']} for {source}")
        #
        # r = requests.post('http://api-server:8000/api/gci/server/list/',
        #                   data={'name': connection_config['name'].replace(' ', '_'),
        #                         'ip': address[0]})
        #
        # registered_server = r.json()
        # if r.status_code == 201:
        #
        #     websocket_url = f"ws://api-server:8000/ws/gci/{connection_config['name'].replace(' ', '_')}/"
        #     log(f'establishing websocket connection to {websocket_url}')
        #     websocket = await websocket_connect(websocket_url)
        #
        #     while True:
        #         try:
        #             data = await stream.read_until(b"\n")
        #             await websocket.write_message(data)
        #
        #         except StreamClosedError:
        #             r = requests.delete(f'http://api-server:8000/api/gci/server/detail/{registered_server["id"]}/')
        #             websocket.close()
        #             log(f'disconnecting websocket connection to {websocket_url}')
        #
        #             if r.status_code == 204:
        #                 log(f'de-registered {registered_server["name"]}')
        #             else:
        #                 log(f'error de-registering {registered_server["name"]}')
        #
        #             break
        #
        # else:
        #     log(f"unable to register {connection_config['name']} for {source}")

    def register_or_update_server(self, session, config):

        registered_servers = [x for x in session.get('http://api-server:8000/api/gci/server/list/').json() if x['name'] == config['name']]

        server_date = {k.lower(): v for k, v in config.pop('date').items()}
        server_time = config.pop('start_time')

        dt = datetime.datetime(**server_date) + datetime.timedelta(seconds=server_time)

        config['start_time'] = dt.isoformat()

        if registered_servers:

            id = registered_servers[0]['id']

            r = session.put(f'http://api-server:8000/api/gci/server/detail/{id}/', data=config)
            log(r.json())
            log(f'updated server {config["name"]}')

        else:

            r = session.post(f'http://api-server:8000/api/gci/server/list/', data=config)
            log(r.json())
            log(f'registered server {config["name"]}')

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
