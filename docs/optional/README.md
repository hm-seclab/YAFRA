# Optional Gitlab and MISP Container

You can host your own gitlab and MISP instance using the `docker-compose.optional.yml` and the `misp-docker` submodule.

Please note, that both services start completly unconfigured and must be setup manually afterwards. This also includes setting up user accounts, access tokens or kroki.

## Usage

### Configuration

You must configure several options (e.g. the mysql credentials for misp) in your env file.

### Starting gitlab

You can start the gitlab server either by using `make gitlab` or by running a `docker-compose -f docker-compose.optional.yml up gitlab`. 

### Starting MISP

You can start the gitlab server either by using `make misp` or by running a `docker-compose -f docker-compose.optional.yml up misp`. Please note, that starting/building MISP the first time may take up to 15 minutes (depending on your infrastructure).