'''
This script contains function to manage gitlab commits.
'''

import gitlab

from libs.kafka.logging import LogMessage
from libs.gitlabl.repository import get_branch_name
from libs.gitlabl.repository import get_projectid_by_name

def file_applies_rules(file, servicename): #TODO REFACTOR and integrate
    '''DEPRECATED
    file_applies_rules will check a commit file against some rules in order
        to avoid duplicates or unappropriate files.
    @param files will be a files-dict from a commit.
    @param servicename will be the name of the service calling this function.
    @return a boolean indicating whether or not all rules are fulfilled.
    '''
    try:
        return all([file['new_file'], not (file['deleted_file'] and file['renamed_file']), file['new_path'].endswith(".md")])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
        return False

def get_filename_since_last_timestamp(gitlabserver, token, repository, timestamp, servicename): #TODO REFACTOR
    '''
    get_filename_since_last_timestamp will return all files which have changed since the given
        timestamp.
    @param gitlabserver will be the address of the gitlab entdpoint.
    @parma token will be the access-token for gitlab.
    @param repository will be the name of the repository.
    @param timestamp will be a datetime-object or string.
    @param servicename will be the name of the service calling this function.
    @return a list with filename if is no change then a empty array
        will be returned.
    '''
    filenames = []
    forbidden_files = 'README.md'
    branch_name = get_branch_name()
    try:
        if (gitlab_instance := gitlab.Gitlab(gitlabserver, token)) is not None:
            if (projectid := get_projectid_by_name(gitlab_instance, repository, servicename)) is not None:
                gprojects = gitlab_instance.projects.get(projectid)
                commits = gprojects.commits.list(ref_name=branch_name, since=timestamp)
                for i in commits:
                    if (commit_diff := i.diff()) is not None:
                        for file in commit_diff:
                            if file['new_file'] and not (file['deleted_file'] and file['renamed_file']):
                                if file['new_path'].endswith(".md") and file['new_path'] not in filenames and file['new_path'].endswith("report.md"):
                                    filenames.append(file['new_path'])
        filenames = list(filter(lambda name: name not in forbidden_files, filenames))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return filenames

def get_latest_commit_hash_by_branch(gitlabserver, token, repository, branch, servicename):
    '''
    get_latest_commit_hash_by_branch will return the hash-value of the last commit of a
        given branch.
    @param gitlabserver will be the address of the gitlab entdpoint.
    @parma token will be the access-token for gitlab.
    @param repository will be the name of the repository.
    @param branch will be the name of the branch.
    @param servicename will be the name of the service calling this function.
    @return will return the commit-hash as a string.
    '''
    chash = None
    try:
        if (gitlab_instance := gitlab.Gitlab(gitlabserver, token)) is not None:
            if (projectid := get_projectid_by_name(gitlab_instance, repository, servicename)) is not None:
                gprojects = gitlab_instance.projects.get(projectid)
                if (commits := gprojects.commits.list(ref_name=branch)) is not None and len(commits) > 0:
                    chash = str((commits[0]).id)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return chash
