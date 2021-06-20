from app import create_app, plugins
import sys

v = create_app()

if len(sys.argv) == 3:
    plugins.sio.run(v, host=sys.argv[1], port=sys.argv[2])
else:
    print("You haven't specified a host/port")
    plugins.sio.run(v)
