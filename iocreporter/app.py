'''
IoC-Reporter-Server.
'''

from flask_script import Manager

# pylint: disable=E0611
from core.server import Reporter
from core.server import flaskapp

from libs.core.environment import envvar

# ENVIRONMENT-VARS
SERVERPORT = envvar("SERVER_PORT", "8084")
SERVERADDRESS = envvar("SERVER_ADDRESS", "127.0.0.1")

app = flaskapp()
manager = Manager(app)

manager.add_command('runserver', Reporter(host=SERVERADDRESS, port=SERVERPORT))

if __name__ == "__main__":
    manager.run()
