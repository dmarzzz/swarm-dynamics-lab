"""J022: pull/retry must validate the exact tree about to be pushed."""
import subprocess
import unittest
from unittest.mock import patch
import lab


class SyncValidationTest(unittest.TestCase):
    def run_sync(self, results, reject_first=False, changed=('5-experiments/studies/shadow/test.md',), staged=None):
        events = []
        def git(*args):
            events.append(args[0])
            if args[0] == 'status':
                return subprocess.CompletedProcess([], 0, ''.join(f' M {path}\n' for path in changed), '')
            if args[0] == 'add' and staged is not None:
                staged.extend(args[args.index('--') + 1:])
            code = int(args[0] == 'push' and reject_first and events.count('push') == 1)
            return subprocess.CompletedProcess([], code, '', '')
        remaining = iter(results)
        def tree(rev):
            events.append('validate')
            result = next(remaining)
            if isinstance(result, Exception):
                raise result
            return result
        with patch.object(lab, 'git', side_effect=git), patch.object(lab, 'heartbeat_tasks'), \
             patch.object(lab, 'Lab'), patch.object(lab, 'check', return_value=([], [])), \
             patch.object(lab, 'tree_errors', side_effect=tree), patch('time.sleep'):
            result = lab.sync_once('shadow/test')
        return result, events

    def test_remote_merge_duplicate_blocks_push(self):
        code, events = self.run_sync([set(), set(), {'library/x.md: duplicate after merge'}])
        self.assertEqual(code, 1)
        self.assertNotIn('push', events)
        self.assertEqual(events[-2:], ['pull', 'validate'])

    def test_success_checks_between_pull_and_push(self):
        code, events = self.run_sync([set(), set(), set()])
        self.assertEqual(code, 0)
        self.assertEqual(events[-3:], ['pull', 'validate', 'push'])

    def test_rejected_push_rechecks_new_remote_merge(self):
        code, events = self.run_sync([set(), set(), set(), {'library/x.md: newly duplicated'}], True)
        self.assertEqual(code, 1)
        self.assertEqual(events.count('push'), 1)
        self.assertEqual(events[-2:], ['pull', 'validate'])

    def test_stages_only_own_researcher_areas(self):
        staged = []
        code, _ = self.run_sync([set(), set(), set()], staged=staged, changed=(
            '5-experiments/studies/shadow/own/README.md', 'lab/researchers/shadow/log/today.md',
            '5-experiments/studies/dmarz/other/README.md', 'lab/researchers/vishesh/inbox.md',
            '5-experiments/toolkit/shared.md', '1-library/papers/x.md', 'lab/STATUS.md', 'lab/templates/task.md'))
        self.assertEqual(code, 0)
        self.assertEqual(staged, ['5-experiments/studies/shadow/own/README.md', 'lab/researchers/shadow/log/today.md',
                                  '5-experiments/toolkit/shared.md', '1-library/papers/x.md'])
        self.assertEqual(lab.area_owner('5-experiments/studies/dmarz/other/README.md'), 'dmarz')
        self.assertEqual(lab.area_owner('lab/researchers/vishesh/inbox.md'), 'vishesh')
        self.assertIsNone(lab.area_owner('5-experiments/EVIDENCE.md'))

    def test_checker_failure_propagates_before_push(self):
        with self.assertRaises(RuntimeError):
            self.run_sync([set(), set(), RuntimeError('checker failed')])


if __name__ == '__main__':
    unittest.main()
