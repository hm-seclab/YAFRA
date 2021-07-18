'''
Entrypoint for the IoC-Puller service.
'''

from flask_script import Manager

# pylint: disable=E0611
from core.server import Filter
from core.server import flaskapp

from libs.core.environment import envvar

# ENVIRONMENT-VARS
SERVERPORT = envvar("SERVER_PORT", "8087")
SERVERADDRESS = envvar("SERVER_ADDRESS", "0.0.0.0")

app = flaskapp()
manager = Manager(app)

manager.add_command('runserver', Filter(host=SERVERADDRESS, port=SERVERPORT))

if __name__ == "__main__":
    manager.run()