# YAFRA

YAFRA stands for `[y]et [a]nother [f]ramework for [r]eport [a]nalysis `

## Description

<p align="justify">
YAFRA is a semi-automated framework for analysing and representing reports about IT security incidents. Users can provide reports as PDF and YAFRA will extract IOCs (indicators of compromise). After extraction these IOCs will be enriched by external sources such as VirusTotal or MITRE in order to provide more context.
</p>

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

## Installation and Configuration

For information about the installation and configuration have a look in the docs folder. 

## Examples

Example reports can be found on the website of the US-CERT (CISA): https://us-cert.cisa.gov/ncas/analysis-reports 

## Extensions

YAFRA provides a simple to use extension system called YAFRA-Extensions. For more information, have a look at the extensions folder.

## System architecture

![Alt-Text](/assets/arch/Arch3.0_TECH.png)

### Meaning

- Blue clouds are Microservices
- Green arrows are data to kafka
- Purple arrows are data from kafka
- Orange arrows are data without kafka interaction
