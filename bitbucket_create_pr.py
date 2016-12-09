'''

'''
import logging
import optparse
import os

import git
import requests


log = logging.getLogger(__name__)

USERNAME = '<your_username>'
REPONAME = '<your_reponame>'
##############################
# Credentials here, caution.
PASSWORD = '<your_password_or_apppassword>'
##############################

REPO_PATH = "<your_repo_path>" or os.getcwd()
TARGET_BRANCH = "<your_target_branch>"

BITBUCKET_API_URL = (
    'https://bitbucket.org/api/2.0/repositories/'
    '{username}/{reponame}/pullrequests').format(
        username=USERNAME, reponame=REPONAME)
    

def main(title, commit_message, close_source_branch=False):
    if not title:
        raise ValueError("Please input title for your PR")
    
    if not commit_message:
        raise ValueError("Please input a commit message for your PR")
    
    repo_full_name = '{username}/{reponame}'.format(
        username=USERNAME, reponame=REPONAME
    )
    
    source_branch = git.Repo(REPO_PATH).active_branch
    target_branch = TARGET_BRANCH
    
    post_body = {
        "title": title, 
        "description": commit_message, 
        
        "source": { 
              "branch": { "name": source_branch }, 
              "repository": { "full_name": repo_full_name } 
        }, 
        
        "destination": { 
              "branch": { "name": target_branch } 
          }, 
          "close_source_branch": close_source_branch    
    }
    
    post_headers = {
        "Authorication": 'Basic {password}'.format(password=PASSWORD)
    } 
    
    log.info("Creating PR: {source} to {destination}".format(
        source=source_branch, destination=target_branch
    ))
    log.debug("Post body: {post_body}".format(post_body=post_body))
    log.debug("Post headers: {post_headers}".format(post_headers=post_headers))
    
    # Actual Post
    # requests.post()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    
    parser.add_option('-t', '--title', action="store")
    parser.add_option('-m', '--commit_message', action="store")
    parser.add_option('-c', '--close_source_branch',
                      action="store_true", default=False)
    
    options, remainder = parser.parse_args()
    main(options.title, option.commit_message, option.close_source_branch)

    