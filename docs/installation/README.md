# Installation guide

## Installation and rebuild

After you have changed all fields in the docker-compose, you have to rebuild all container. In order to do this, run the following command. If you dont have changed the docker-compose yet, have a look in the docs/configurations file for more information. Also notice the requirements in the docs/requirements

```bash
make build
```

## System start

After the installation the system can be booted up by using make.

### Zookeeper

```bash
make zookeeper
```

### KAFKA

```bash
make kafka
```
``` Notice: Kafka needs Zookeeper in order to run properly. If kafka returns a status code 1 just hold on for a few seconds until zookeeper has started up. Than rerun the command.```

### Kroki (Optional)

If no instance of kroki is running on this server or you dont have an kroki server yet, run the following command.

```bash
make krokiinit
```

### Start of the Microservers

```bash
make up
```
