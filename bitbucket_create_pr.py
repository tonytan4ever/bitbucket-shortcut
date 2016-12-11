'''

'''

import json
import logging
import optparse
import os

import git
import requests

from utils import remote_parser


log = logging.getLogger(__name__)

REPO_PATH = "<your_repo_path>" or os.getcwd()
REPO = git.Repo(REPO_PATH)

USERNAME,REPONAME = remote_parser.get_user_and_repo_name(REPO)
##############################
# Credentials here, caution.
# PASSWORD = '<your_password_or_apppassword>'
PASSWORD = os.environ.get('BITBUCKET_PASS','<your_password_or_apppassword>' )
##############################

SOURCE_BRANCH = REPO.active_branch.name
TARGET_BRANCH = "master"

BITBUCKET_API_URL = (
    'https://bitbucket.org/api/2.0/repositories/'
    '{username}/{reponame}/pullrequests').format(
        username=USERNAME, reponame=REPONAME)
    

def main(title, commit_message, target_branch=TARGET_BRANCH,
          close_source_branch=False):
    if not title:
        raise ValueError("Please input title for your PR")
    
    if not commit_message:
        raise ValueError("Please input a commit message for your PR")
    
    repo_full_name = '{username}/{reponame}'.format(
        username=USERNAME, reponame=REPONAME
    )    
    
    post_body = {
        "title": title, 
        "description": commit_message, 
        
        "source": { 
              "branch": { "name": SOURCE_BRANCH }, 
              "repository": { "full_name": repo_full_name } 
        }, 
        
        "destination": { 
              "branch": { "name": TARGET_BRANCH } 
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
    resp = requests.post(BITBUCKET_API_URL,
                         data=json.dumps(post_body),
                         headers=post_headers)
    
    if resp.ok:
        # Echo the PR html url link:
        success_resp_dict = json.loads(resp.text)
        log.info("PR create successful")
        log.info("Review your PR: {pr_url}".format(
            pr_url=success_resp_dict["links"]["html"])
        )
    else:
        log.info("Creating PR failed:")
        log.info(resp.text)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    
    parser.add_option('-c', '--close_source_branch',
                      action="store_true", default=False)
    parser.add_option('-g', '--target_branch', action="store", 
                      default="master")
    parser.add_option('-m', '--commit_message', action="store")
    parser.add_option('-t', '--title', action="store")
    
    options, remainder = parser.parse_args()
    main(options.title, options.commit_message, options.target_branch,
         options.close_source_branch)

    