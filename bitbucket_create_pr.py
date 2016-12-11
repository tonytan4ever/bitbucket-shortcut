'''

'''

import json
import logging
import optparse
import os
import sys

import git
import requests

from utils import remote_parser

loghandler = logging.StreamHandler(stream=sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(loghandler)
log.setLevel(logging.DEBUG)

REPO_PATH =  os.getcwd() # or hardcode: "<your_repo_path>"
REPO = git.Repo(REPO_PATH)

REPO_ORG,REPONAME = remote_parser.get_repo_org_and_name(REPO)
##############################
# Credentials here, caution.
USERNAME = os.environ.get('BITBUCKET_USER', '<your_bitbucket_user_name>')
PASSWORD = os.environ.get('BITBUCKET_PASS','<your_password_or_apppassword>' )
# PASSWORD = '<your_password_or_apppassword>'
##############################

SOURCE_BRANCH = REPO.active_branch.name
TARGET_BRANCH = "master"

BITBUCKET_API_URL = (
    'https://bitbucket.org/api/2.0/repositories/'
    '{reporg}/{reponame}/pullrequests').format(
        reporg=REPO_ORG, reponame=REPONAME)
    

def main(title, commit_message, target_branch=TARGET_BRANCH,
          close_source_branch=False):
    if not title:
        raise ValueError("Please input title for your PR")
    
    if not commit_message:
        raise ValueError("Please input a commit message for your PR")
    
    repo_full_name = '{reporg}/{reponame}'.format(
        reporg=REPO_ORG, reponame=REPONAME
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
    
    auth = (USERNAME, PASSWORD)
    
    post_headers = {
        "Content-Type": "application/json"
    } 
    
    log.info("Creating PR: {source} to {destination}".format(
        source=SOURCE_BRANCH, destination=TARGET_BRANCH
    ))
    log.debug('API_URL:' + BITBUCKET_API_URL)
    log.debug("Post body: {post_body}".format(post_body=post_body))
    log.debug("Post headers: {post_headers}".format(post_headers=post_headers))
    
    # Actual Post
    resp = requests.post(BITBUCKET_API_URL,
                         data=json.dumps(post_body),
                         auth=auth,
                         headers=post_headers)
    
    if resp.ok:
        # Echo the PR html url link:
        success_resp_dict = json.loads(resp.text)
        log.info("PR create successful")
        log.info("Review your PR: {pr_url}".format(
            pr_url=success_resp_dict["links"]["html"])
        )
    else:
        log.info("Creating PR failed: {resp_code}".format(
            resp_code=resp.status_code)
        )
        log.info(resp.text)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    
    parser.add_option('-c', '--close_source_branch',
                      help="whether to remove branch after merge",
                      action="store_true", default=False)
    parser.add_option('-g', '--target_branch', action="store", 
                       help="name of target branch",
                      default="master")
    parser.add_option('-m', '--commit_message', action="store",
                       help="description of the PR")
    parser.add_option('-t', '--title', action="store",
                      help="title of the PR",)
    
    options, remainder = parser.parse_args()
    main(options.title, options.commit_message, options.target_branch,
         options.close_source_branch)

    