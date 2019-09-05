from models import DummyClient
import sys


if len(sys.argv) > 1:

    client = DummyClient(*sys.argv[1:])

else:

    client = DummyClient()

