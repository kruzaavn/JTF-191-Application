from models import TCPProtocol, WSHandler
import tornado.platform.asyncio as tp
import tornado.httpserver
import tornado.web as web
import asyncio

application = web.Application([(r'/', WSHandler)])

tp.AsyncIOMainLoop().install()

loop = asyncio.get_event_loop()

# Create tornado HTTP server
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8082)
print('listening on 8082 for clients')

# Start asyncio TCP server

coro = loop.create_server(TCPProtocol, 'localhost', 8081)
server = loop.run_until_complete(coro)

# Run forever
loop.run_forever()
