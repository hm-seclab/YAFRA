## Requirements

### Technical

* Docker
* Docker-compose
* Make
* GitLab
* Kroki Server
* MISP

` Notice: MISP and GitLab will not be installed via docker-compose. GitLab also needs an active Kroki or PlantUML-Server.`

You can use the kroki Docker-Container provide in the make file by running the following command:

> make krokiinit

This will open a port on the host-machine at 7777.

> Kroki: https://docs.gitlab.com/ee/administration/integration/kroki.html

> PlantUML: https://docs.gitlab.com/ee/administration/integration/plantuml.html

` Notice: The address have to be put into gitlab by an admin. `

### Non-Technical/External-sources:

* VirusTotal-API-Key
* Twitter-Consumer-Key
* Twitter-Consumer-Key-Secret
* Twitter-Access-Token
* Twitter-Access-Token-Secret
* Leakix-API-Key

