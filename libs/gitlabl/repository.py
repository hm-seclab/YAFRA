'''
Function for interacting with gitlab.
'''

import os
import json

from datetime import datetime

import gitlab

from libs.kafka.logging import LogMessage
from libs.core.environment import envvar

GITLAB_CERT_VERIFY = True if envvar("GITLAB_VERIF", str(True)).lower() in ("yes", "y", "true", "1", "t") else False


def create_repository_if_not_exists(gitlabserver, token, repository, servicename):
    '''
    create_repository_if_not_exists will create a repository incase
    it is not allready in gitlab.
    @param gitlabserver will be the server where gitlab is hosted.
    @param token will be the personal-access-token for gitlab.
    @param repository will be the name of the repository.
    @param servicename is the server who sends the request.
    '''
    try:
        if (gitlab_instance := gitlab.Gitlab(gitlabserver, token, ssl_verify=GITLAB_CERT_VERIFY)) is not None:
            gprojects = gitlab_instance.projects.list(all=True)
            project_names = [project.name for project in gprojects]
            if not repository in project_names:
                LogMessage(f"Creating new repository: {repository}", LogMessage.LogTyp.INFO, servicename).log()
                gprojects = gitlab_instance.projects.create({'name': repository})
                gprojects.avatar = open(os.path.abspath("../assets/icon.png"), 'rb')
                gprojects.save()
                with open(os.path.abspath("../datasets/blacklist.json")) as file:
                    gprojects.commits.create({
                        'branch': 'master',
                        'commit_message': 'initial commit',
                        'actions': [
                            {
                                'action': 'create',
                                'file_path': 'blacklist.json',
                                'content': json.dumps(json.load(file), indent=4, sort_keys=True),
                            }]
                    })
                    LogMessage(f"The blacklist has been added to the repository: {repository}", LogMessage.LogTyp.INFO, servicename).log()
                if 'README.md' in [gprojects.repository_tree(branch='master')]:
                        gprojects.commits.create({
                        'branch': 'master',
                        'commit_message': 'Remove README.md',
                        'actions': [{
                            'action': 'delete',
                            'file_path': 'README.md',
                        }]
                    })
                __create_datasources_in_repository(gprojects, servicename)
                gprojects.labels.create({'name': 'Ready', 'color': '#00cc66'})
        else:
            LogMessage("Repository already exists", LogMessage.LogTyp.WARNING, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def __create_datasources_in_repository(gprojects, servicename):
    '''
    __create_datasources_in_repository will create new datasources
    in json format within a given gitlab repository.
    Those datasources are stored within a protected branch.
    @param gprojects will be the gitlab project
    '''
    try:
        datasources_branch = gprojects.branches.create({'branch': 'datasources', 'ref': 'master'})
        with open(os.path.abspath("../datasets/sources/api_sources.json")) as api_sources, open(
                os.path.abspath("../datasets/sources/rss_sources.json")) as rss_sources, open(
                os.path.abspath("../datasets/sources/twitter_sources.json")) as twitter_sources:
            gprojects.commits.create({
                'branch': 'datasources',
                'commit_message': 'datasource commit',
                'actions': [
                    {
                        'action': 'create',
                        'file_path': 'api_sources.json',
                        'content': json.dumps(json.load(api_sources), indent=4, sort_keys=True),
                    },
                    {
                        'action': 'create',
                        'file_path': 'rss_sources.json',
                        'content': json.dumps(json.load(rss_sources), indent=4, sort_keys=True),
                    },
                    {
                        'action': 'create',
                        'file_path': 'twitter_sources.json',
                        'content': json.dumps(json.load(twitter_sources), indent=4, sort_keys=True),
                    },
                    {
                        'action': 'delete',
                        'file_path': 'blacklist.json',
                    }
                ]
            })
        datasources_branch.protect()
        LogMessage("New datasources have been added to a new protected branch with name datasources", LogMessage.LogTyp.INFO, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def get_projectid_by_name(gitlabinstance, projectname, servicename):
    '''
    get_projectid_by_name will return the id of a project by its projectname.
    @param gitlabinstance will be a gitlab-object with a connection to gitlab.
    @param projectname will be the name of the project.
    '''
    try:
        gprojects = gitlabinstance.projects.list(all=True)
        project_names = list(filter(lambda x: (x.name == projectname), gprojects))
        return project_names[0].id
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
        return None


def get_branch_name():
    '''
    get_branch_name will return the name of the daily branch.
    @return a string with the name of the daily branch. In the
        format: IoC-04.04.2021
    '''
    return "IoC-{}".format(datetime.today().strftime('%m-%Y'))


def get_project_handle(gitlabserver, token, repository, servicename):
    '''
    get_project_handle will return a handle to a project, in order
        to work on a project. Like creating files, issues, etc.
    @param gitlabserver will be the address of the gitlab entdpoint.
    @parma token will be the access-token for gitlab.
    @param repository will be the name of the repository.
    @param servicename will be the name of the service calling this function.
    '''
    gprojects = None
    try:
        if (gitlab_instance := gitlab.Gitlab(gitlabserver, token, ssl_verify=GITLAB_CERT_VERIFY)) is not None:
            if (projectid := get_projectid_by_name(gitlab_instance, repository, servicename)) is not None:
                gprojects = gitlab_instance.projects.get(projectid)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return gprojects


def create_monthly_if_not_exists(gitlabserver, token, repository, servicename):
    '''
    create_monthly_if_not_exists will create a monthly branch for the icos.
    @param gitlabserver will be the hostname of the gitlabserver.
    @param token will be the personal-access-token for gitlab.
    @param repository will be the name repository where the branch should be created in.
    @param servicename is the server who sends the request.
    '''
    try:
        branch_name = get_branch_name()
        gprojects = get_project_handle(gitlabserver, token, repository, servicename)
        if not branch_name in [branch.name for branch in gprojects.branches.list()]:
            gprojects.branches.create({'branch': branch_name, 'ref': 'master'})
            gprojects.commits.create({
                'branch': str(branch_name),
                'commit_message': 'remove blacklist',
                'actions': [
                    {
                        'action': 'delete',
                        'file_path': 'blacklist.json',
                    }
                ]
            })
        else:
            LogMessage("Monthlybranch already exists", LogMessage.LogTyp.INFO, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
