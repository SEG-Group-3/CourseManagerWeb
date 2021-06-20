from app import create_app, plugins

v = create_app()
plugins.sio.run(v)
