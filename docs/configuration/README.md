# Configuration

YAFRA allows the user to configure a lot of parts. Some of thos parts are needed in order to run properly. 
The following snipped of the docker-compose shows which information is needed in order to run as intended.
All fields with ``` {SOME_TEXT} ``` needs to be replaced in the docker-compose. 

```yaml
    ...
x-common-variables: &common-variables
    ...
    KAFKA_SERVER: "{IP_OF_KAFKA}"
    ...
x-common-variables: &GITLAB
    GITLAB_SERVER: "{THE_URL_OF_THE_GITLAB_SERVER}"
    GITLAB_TOKEN: "{THE_GITLAB_TOKEN}"
    GITLAB_REPO_NAME: "{GITLAB_REPO_NAME}"
x-common-variables: &APIKEYS
    VIRUS_TOTAL: "{VIRUS_TOTAL_TOKEN}"
x-common-variables: &MISP
    MISP_SERVER: "{MISP_URL_IP}"
    MISP_TOKEN: "{MISP_TOKEN}"
    ...
    ...
    extractor:
        build:
            context: .
            dockerfile: iocextractor/Dockerfile
        container_name: iocextractor
        ports:
            - "8081:8081"
        volumes:
            - type: bind
              source: {Absolute_path_to_your_pdfs}
              target: /app/iocextractor/reports
```
``` Notice the Extractor needs a drive/folder on the server where all reports are placed which sould be imported. In the docker-comnpose needs the be the absolute path to this folder in order to work. For groups of people a net-drive whould be the best idea. The drive to the PDF should not be changed incase yafra is running. You can add reports in the drive at any time. ```