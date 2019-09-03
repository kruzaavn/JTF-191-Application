from models import Server
import sys

if len(sys.argv) > 1:
    server = Server(*sys.argv[1:])
else:
    server = Server()
