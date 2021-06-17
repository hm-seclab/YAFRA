'''
The entrypoint for the sysmon-service.
'''

from core.server import Sysmonserver
from core.server import flaskapp

from libs.core.environment import envvar

from flask_script import Manager

SERVERPORT = envvar("SERVER_PORT", "8080")
SERVERADDRESS = envvar("SERVER_ADDRESS", "0.0.0.0")

app = flaskapp()
manager = Manager(app)

manager.add_command('runserver', Sysmonserver(host=SERVERADDRESS, port=SERVERPORT))

if __name__ == "__main__":
    manager.run()