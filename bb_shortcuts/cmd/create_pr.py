import optparse

from bb_shortcuts.bitbucket_create_pr import create_pr


def wrapper():
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

    options, _ = parser.parse_args()
    create_pr(options.title, options.commit_message, options.target_branch,
              options.close_source_branch)
