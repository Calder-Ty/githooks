#! /usr/bin/env python3
'''Tests for My hooks'''
import unittest
from unittest.mock import patch, PropertyMock, mock_open

from src.prepush import prepush_main
from src.precommit import precommit_main


class PreCommitTest(unittest.TestCase):
    '''Tests for precommit hook'''
    def test_main_fails_when_config_keys_not_set(self):
        '''Main should exit with non zero status when KeyError occurs'''
        config = {}
        with self.assertRaises(SystemExit) as cm:
            precommit_main(config=config)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        self.assertRaises(SystemExit, precommit_main, config)

    @patch('subprocess.run')
    @patch('src.precommit.open', new_callable=mock_open(read_data='Hi\nThis Is a word\n'))
    def test_writes_to_file(self, mockopen, mockrun):
        '''Test if files are written to when stuff works'''
        config = {'test_command': 'ls',
                  'readme_path': 'README'
                 }
        subprocess_out = mockrun.return_value
        subprocess_out.returncode = 0
        precommit_main(config=config)
        mockopen.assert_called_with('README', 'w')


class PrePushTests(unittest.TestCase):
    '''Tests for the pre-push hooks'''
    def setUp(self):
        self.config = {"test_command": "", "protected_branch": "master"}

    def test_non_zero_exit_when_config_keys_not_set(self):
        '''Does process exit with non-zero status when the configuration keys were not set?'''
        self.config = {}
        with self.assertRaises(SystemExit) as cm:
            prepush_main(config=self.config)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        self.assertRaises(SystemExit, prepush_main, self.config)

    @patch('subprocess.run')
    def test_zero_exit_when_no_new_commits(self, mock_run):
        '''Does process exit with zero status when no new commits are found'''
        completed_process = mock_run.return_value
        completed_process.stdout = ""

        with self.assertRaises(SystemExit) as cm:
            prepush_main(config=self.config)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    @patch('subprocess.run')
    def test_exits_with_0_when_on_master_and_test_pass(self, mock_run):
        '''When everything goes right does the function exit with 0?'''
        completed_process = mock_run.return_value
        stdout = PropertyMock(side_effect=['asda', 'master'])
        type(completed_process).stdout = stdout
        return_code = PropertyMock(return_value=0)
        type(completed_process).returncode = return_code

        with self.assertRaises(SystemExit) as cm:
            prepush_main(config=self.config)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)
        return_code.assert_called_once_with()

    @patch('subprocess.run')
    def test_exists_with_non_zero_when_tests_fail(self, mock_run):
        completed_process = mock_run.return_value
        stdout = PropertyMock(side_effect=['asda', 'master'])
        type(completed_process).stdout = stdout
        return_code = PropertyMock(return_value=1)
        type(completed_process).returncode = return_code

        with self.assertRaises(SystemExit) as cm:
            prepush_main(config=self.config)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        return_code.assert_called_once_with()





if __name__ == "__main__":
    unittest.main()
