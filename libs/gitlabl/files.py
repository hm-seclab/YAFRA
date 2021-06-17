'''
This script contains function to manage gitlab reads.
'''

from libs.kafka.logging import LogMessage
from libs.gitlabl.repository import get_branch_name
from libs.gitlabl.repository import get_project_handle

def read_file_from_gitlab(gitlabserver, token, repository, file, servicename, branch_name=""):
    '''
    read_file_from_gitlab will read in a file from gitlab and return its content.
    @param gitlabserver will be the address of the gitlab entdpoint.
    @parma token will be the access-token for gitlab.
    @param repository will be the name of the repository.
    @param file with be a path in on a branch. The branch will always be the dailybranch.
    @param servicename will be the name of the service calling this function.
    '''
    file_content = ""
    try:
        if branch_name == "":
            branch_name = get_branch_name()
        gprojects = get_project_handle(gitlabserver, token, repository, servicename)
        file_handle = gprojects.files.get(file_path=file, ref=branch_name)
        file_content = (file_handle.decode()).decode('UTF-8')
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return file_content
