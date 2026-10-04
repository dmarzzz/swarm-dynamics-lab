"""J005: recover remote batch issues and persist mappings before body edits."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from test_batches_worktree import batches


class PublishTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cand = self.root / 'candidates'
        (self.cand / 'blog').mkdir(parents=True)
        (self.cand / 'blog/demo.jsonl').write_text('{"url":"https://example.org","topic":"meta"}\n')
        for name, value in [('ROOT', self.root), ('CAND', self.cand), ('MAP', self.cand / 'ISSUES.tsv')]:
            p = patch.object(batches, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.args = argparse.Namespace(batch=['demo'], force=False)

    def test_reconciles_remote_without_creating_or_editing(self):
        remote = {'number': 42, 'url': 'https://example.org/42',
                  'title': '[batch] blog/meta: 1 candidates (demo)', 'body': 'Batch `demo`: 1'}
        with patch.object(batches, 'gh_json', return_value=[remote]) as query, \
             patch.object(batches, 'gh') as gh:
            self.assertEqual(batches.cmd_publish(self.args), 0)
            gh.assert_not_called()
            self.assertIn('all', query.call_args.args)
        self.assertEqual(batches.read_map(), {'demo': ('42', remote['url'])})

    def test_failed_body_edit_retains_mapping(self):
        with patch.object(batches, 'gh_json', return_value=[]), \
             patch.object(batches, 'gh', side_effect=['https://example.org/43', SystemExit('edit failed')]):
            with self.assertRaises(SystemExit):
                batches.cmd_publish(self.args)
        self.assertEqual(batches.read_map(), {'demo': ('43', 'https://example.org/43')})
        with patch.object(batches, 'gh') as gh:
            self.assertEqual(batches.cmd_publish(self.args), 0)
            gh.assert_not_called()

    def test_exact_marker_and_duplicate_remote_fail_closed(self):
        remote = {'number': 42, 'url': 'https://example.org/42',
                  'title': '[batch] blog/meta: 1 candidates (demo)', 'body': 'Batch `demo`: 1'}
        with patch.object(batches, 'gh_json', return_value=[remote, dict(remote, number=43)]):
            with self.assertRaises(SystemExit):
                batches.remote_batch_issue('demo')
        with patch.object(batches, 'gh_json', return_value=[dict(remote, body='Unrelated')]):
            self.assertIsNone(batches.remote_batch_issue('demo'))

    def test_atomic_map_updates_preserve_concurrent_entries_and_comments(self):
        batches.MAP.write_text('# header\n')
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda n: batches.record_issue(str(n), str(n), f'https://example.org/{n}'), range(16)))
        self.assertEqual(len(batches.read_map()), 16)
        self.assertTrue(batches.MAP.read_text().startswith('# header\n'))
        before = batches.MAP.read_text()
        batches.record_issue('0', '0', 'https://example.org/0')
        self.assertEqual(batches.MAP.read_text(), before)
        with self.assertRaises(SystemExit):
            batches.record_issue('0', '99', 'https://example.org/99')
        self.assertEqual(batches.MAP.read_text(), before)


if __name__ == '__main__':
    unittest.main()
