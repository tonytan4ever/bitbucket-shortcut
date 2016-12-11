'''
Utility functions to parse the repo from a git repo object
'''
import urlparse


def parse_bitbucket_path(parsed_remote_url):
    # Assume bitbucket's path is in <username>/<reponame>.git form
    compartments = parsed_remote_url.path.split('/')
    return compartments[1], compartments[2].replace('.git')

def get_user_and_repo_name(repo_obj):
    ### This will return something like:
    ### origin    https://<u>@bitbucket.org/<username>/<reponame>.git (fetch)
    ### origin    https://<u>@bitbucket.org/<username>/<reponame>.git (push)
    remote_description = repo_obj.git.remote(verbose=True)
    ### get the part of: https://<u>@bitbucket.org/<username>/<reponame>.git
    remote_url = remote_description.split()[1]
    parsed_remote_url = urlparse.urlparse(remote_url)
    return parse_bitbucket_path



    
    