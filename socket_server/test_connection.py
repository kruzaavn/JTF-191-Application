from models import Client
import sys


if len(sys.argv) > 1:

    client = Client(*sys.argv[1:])

else:

    client = Client()

