'''
Server for the ioc-extractor service.
'''

from core.server import Extractor
from core.server import flaskapp

from libs.core.environment import envvar

from flask_script import Manager

# ENVIRONMENT-VARS
SERVERPORT = envvar("SERVER_PORT", "8081")
SERVERADDRESS = envvar("SERVER_ADDRESS", "0.0.0.0")

app = flaskapp()
manager = Manager(app)

manager.add_command('runserver', Extractor(host=SERVERADDRESS, port=SERVERPORT))

if __name__ == "__main__":
    manager.run()
