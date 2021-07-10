# Makefile to run different parts of the system.
up:
	git submodule update --init
	sudo docker-compose up --build extractor pusher puller reporter sysmon scraper
config:
	git submodule update --init
	sudo docker-compose config
build:
	git submodule update --init
	sudo docker-compose build extractor puller pusher reporter sysmon
zookeeper:
	git submodule update --init
	sudo docker-compose up zookeeper
kafka:
	git submodule update --init
	sudo docker-compose up kafka
neo4j:
	git submodule update --init
	sudo docker-compose up neo4j
krokiinit:
	sudo docker run -d --name kroki -p 7777:8000 yuzutech/kroki
kroki:
	sudo docker run -d yuzutech/kroki -p 7777:8000