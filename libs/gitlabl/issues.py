'''
This script contains function to handle issues in gitlab.
'''

from libs.kafka.logging import LogMessage
from libs.gitlabl.repository import get_project_handle

def create_issues(gprojects, servicename, title, description):
    '''
    create_issues will create an issues for a submitted report.
    @param gitlabserver will be the address of the gitlab entdpoint.
    @parma token will be the access-token for gitlab.
    @param repository will be the name of the repository.
    @param servicename will be the name of the service calling this function.
    @param title will be the title of the issue
    @param description will be the text of the issue.
    '''
    try:
        issue = gprojects.issues.create({'title': title, 'description': description})
        issue.labels = ['New Report']
        issue.todo()
        issue.save()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
