'''Pre Commit hook code'''

# This should allow for several different processes happen as per
# the config file.

# Things that should happen:
#    Tests should be run:
#    Warning given if test fails?
#    Code Coverage run?
#    README FILE Updated with new status of Code
import subprocess
import sys


def _run_tests(test_command: str)->bool:
    '''
    Runs specified tests specified and returns bool if
    test passed or failed
    '''
    test_status = subprocess.run(test_command, shell=True).returncode
    return not test_status

def _update_readme(test_status, readme_path):
    if test_status:
        # Update Readme with passed img
        new_header = '# Build Status: ![Build is Passing]\
                      (https://raw.githubusercontent.com/Calder-Ty/\
                      BuildImgs/master/passing.png\\n'
    else:
        # Update Readme with failed img

        new_header = '# Build Status: ![Build is Passing]\
                      (https://raw.githubusercontent.com/Calder-Ty/\
                      BuildImgs/master/Failing.png\\n'
    with open(readme_path, 'r') as readme:
        lines = readme.readline()
    lines[0] = new_header
    with open(readme_path, 'w') as readme:
        readme.writelines(lines)


def precommit_main(config: dict)->None:
    '''main function of the pre-commit hook'''
    try:
        readme_path = config['readme_path']
        test_command = config['test_command']
    except KeyError:
        print("You have not set your config file correctly")
        sys.exit(1)

    if readme_path is None:
        update_readme = False
    else:
        update_readme = True

    test_passed = _run_tests(test_command)
    if update_readme:
        _update_readme(test_passed, readme_path)
    if test_passed:
        print("Tests are passing")
    else:
        print("Build is not passing")
