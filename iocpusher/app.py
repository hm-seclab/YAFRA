'''
Server for the ioc-pusher service.
'''

from flask_script import Manager

from core.server import Pusher
from core.server import flaskapp

from libs.core.environment import envvar

# ENVIRONMENT-VARS
SERVERPORT = envvar("SERVER_PORT", "8082")
SERVERADDRESS = envvar("SERVER_ADDRESS", "0.0.0.0")

app = flaskapp()
manager = Manager(app)

manager.add_command('runserver', Pusher(host=SERVERADDRESS, port=SERVERPORT))

if __name__ == "__main__":
    manager.run()
