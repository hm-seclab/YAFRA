# Makefile to run different parts of the system.
up:
	sudo docker-compose up --build extractor pusher puller reporter sysmon scraper
config:
	sudo docker-compose config
build:
	sudo docker-compose build extractor puller pusher reporter sysmon
zookeeper:
	sudo docker-compose up zookeeper
kafka:
	sudo docker-compose up kafka
neo4j:
	sudo docker-compose up neo4j
gitlab:	
	git submodule update --init
	sudo docker-compose -f docker-compose.optional.yml up gitlab
misp:	
	git submodule update --init
	sudo docker-compose -f docker-compose.optional.yml up misp
krokiinit:
	sudo docker run -d --name kroki -p 7777:8000 yuzutech/kroki
kroki:
	sudo docker run -d yuzutech/kroki -p 7777:8000