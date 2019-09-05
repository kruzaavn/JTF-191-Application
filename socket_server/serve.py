from models import SocketServer
import asyncio
import websockets


async def hello(websocket, path):

    server = SocketServer()

    while True:

        server.poll_connections()
        data = server.get_data()

        if data:
            await websocket.send(data)


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
