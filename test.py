#! /usr/bin/env python3
'''Tests for My hooks'''
import unittest
from unittest.mock import patch, PropertyMock

from src.prepush import prepush_main

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
