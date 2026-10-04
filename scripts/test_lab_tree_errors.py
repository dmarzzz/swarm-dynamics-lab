"""J021: failed checker execution is not an empty or subtractable error set."""
import subprocess
import unittest
from unittest.mock import patch
import lab


class TreeErrorsTest(unittest.TestCase):
    def run_checker(self, status=0, stdout='', stderr=''):
        with patch.object(lab, 'git', return_value=subprocess.CompletedProcess([], 0)) as git, \
             patch.object(lab.subprocess, 'run', return_value=subprocess.CompletedProcess([], status, stdout, stderr)):
            try:
                return lab.tree_errors('HEAD')
            finally:
                self.assertEqual(git.call_args.args[:3], ('worktree', 'remove', '--force'))

    def test_success(self):
        self.assertEqual(self.run_checker(stdout='0 errors, 5 warnings. 10 library entries.\n'), set())

    def test_validation_errors_remain_reportable(self):
        self.assertEqual(self.run_checker(1, 'ERROR library/x.md: invalid\n1 errors, 0 warnings. 10 library entries.\n'),
                         {'library/x.md: invalid'})

    def test_crash_and_incomplete_output_raise_not_empty_set(self):
        for status, stdout in [(1, ''), (0, ''), (2, 'ERROR x: invalid\n'),
                               (1, '0 errors, 0 warnings. 10 library entries.\n'),
                               (0, 'ERROR x: invalid\n1 errors, 0 warnings. 10 library entries.\n'),
                               (1, '2 errors, 0 warnings. 10 library entries.\n')]:
            with self.subTest(status=status, stdout=stdout):
                with self.assertRaises(RuntimeError) as exc:
                    self.run_checker(status, stdout, 'Traceback: synthetic-secret')
                self.assertNotIn('synthetic-secret', str(exc.exception))

    def test_worktree_creation_failure_raises_and_cleans(self):
        with patch.object(lab, 'git', return_value=subprocess.CompletedProcess([], 1)) as git, \
             patch.object(lab.subprocess, 'run') as run:
            with self.assertRaises(RuntimeError):
                lab.tree_errors('HEAD')
            run.assert_not_called()
            self.assertEqual(git.call_count, 2)


if __name__ == '__main__':
    unittest.main()
