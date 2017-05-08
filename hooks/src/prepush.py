'''Functions taht are to be used for the Pre-push hooks'''
import subprocess
import sys

CONFIG = {}
def prepush_main(config=CONFIG):
    '''main function'''
    # Todo Throw ERROR here that is more explicit if config file not set-up
    # Translated from bash: http://blog.ittybittyapps.com/blog/2013/09/03/git-pre-push/
    try:
        test_command = config['test_command']
        protected_branch = config['protected_branch']
    except KeyError:
        print("Error, Youre configuration file is not set up appropriately")
        sys.exit(1)

    commits = subprocess.run(['git', 'log', '@{u}..'], stdout=subprocess.PIPE).stdout
    if len(commits) == 0:
        sys.exit(0)
    current_branch = subprocess.run(["git", "symbolic-ref", "HEAD", "|", "sed",
                                     "-e", "'s,.*/(.*),1,'"]).stdout

    if current_branch == protected_branch:
        test_status = subprocess.run(test_command, shell=True).returncode
        if test_status != 0:
            print("Your Tests have Failed, Push on master branch is being aborted")
            sys.exit(1)
    sys.exit(0)
