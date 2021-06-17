'''
This script contains function to manage pull requests in gitlab.
'''

import gitlab

from libs.kafka.logging import LogMessage
from libs.gitlabl.repository import get_projectid_by_name

def get_list_of_relevant_prs(gitlabserver, token, repository, servicename):
    '''
    get_list_of_relevant_prs will return a list of pr-objects (gitlab-class)
        with the status open and the label "Ready".
    @param gitlabserver will be the address of the gitlab entdpoint.
    @parma token will be the access-token for gitlab.
    @param repository will be the name of the repository.
    @param servicename will be the name of the service calling this function.
    @return will return a list of pr-objects (gitlab-class) incase a at least
        one pr will match the conditions above else a empty list will be
        returned.
    '''
    relevant_prs = []
    try:
        if (gitlab_instance := gitlab.Gitlab(gitlabserver, token)) is not None:
            if (projectid := get_projectid_by_name(gitlab_instance, repository, servicename)) is not None:
                gprojects = gitlab_instance.projects.get(projectid)
                open_prs = gprojects.mergerequests.list(state="opened", labels=['Ready'])
                for pull_request in open_prs:
                    relevant_prs.append(pull_request)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return relevant_prs


def merge_pull_request(prs, servicename):
    '''
    merge_pull_request will merge all given pull_requests.
    @param servicename will be the name of the service calling this function.
    '''
    try:
        for merge_request in prs:
            try:
                merge_request.merge()
            except gitlab.GitlabMRClosedError:
                continue
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
