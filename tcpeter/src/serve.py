from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
import datetime


class TCPeter(TCPServer):

    async def handle_stream(self, stream, address):

        while True:
            try:
                data = await stream.read_until(b"\n")
                print(f'{stream} {address} {data}')

            except StreamClosedError:
                break


if __name__ == '__main__':

    server = TCPeter()
    print(f'{datetime.datetime.now()} listening on 7224')
    server.bind(7224)
    server.start()
    IOLoop.current().start()
