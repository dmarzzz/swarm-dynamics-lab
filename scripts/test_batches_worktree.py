"""Regression: done validates local entries and entries from another checkout."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import lab

spec = importlib.util.spec_from_file_location('batches', Path(__file__).with_name('batches.py'))
batches = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batches)


def entry_text(name):
    return f'''---
id: {name}
type: blog
title: Test {name}
url: https://example.org/{name}
topics: [meta]
added_by: test/worker
accessed: 2026-10-04
read_depth: abstract
relevance: 2
year: 2026
authors: [Test]
---
## Summary
This synthetic offline test fixture contains enough words to exercise the existing library quality validator without accessing a network source or claiming that an actual research paper exists.
'''


class WorktreeDoneTest(unittest.TestCase):
    def test_published_local_and_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote, writer, reader = [root / name for name in ('remote.git', 'writer', 'reader')]
            def git(cwd, *args):
                subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True)
            git(root, 'init', '--bare', str(remote))
            git(root, 'clone', str(remote), str(writer))
            git(writer, 'checkout', '-b', 'main')
            git(writer, 'config', 'user.name', 'Test')
            git(writer, 'config', 'user.email', 'test@example.com')
            (writer / '1-library/blogs').mkdir(parents=True)
            (writer / '1-library/topics.yaml').write_text('- slug: meta\n')
            (writer / 'lab/researchers/test').mkdir(parents=True)
            (writer / 'lab/researchers/test/README.md').write_text('test')
            git(writer, 'add', '.')
            git(writer, 'commit', '-m', 'seed')
            git(writer, 'push', 'origin', 'main')
            git(root, 'clone', '--branch', 'main', str(remote), str(reader))
            (writer / '1-library/blogs/published.md').write_text(entry_text('published'))
            git(writer, 'add', '.')
            git(writer, 'commit', '-m', 'another worktree writes entry')
            git(writer, 'push', 'origin', 'main')
            (reader / '1-library/blogs').mkdir(exist_ok=True)
            local = reader / '1-library/blogs/local.md'
            local.write_text(entry_text('local'))
            args = argparse.Namespace(entries=['1-library/blogs/published.md', '1-library/blogs/local.md'],
                                      force=False, agent='test/worker', issue='1', skipped=None)
            claimed = {'state': 'OPEN', 'labels': [{'name': name} for name in
                       ('claimed', 'source:blog', 'topic:meta')], 'comments': [
                       {'body': 'claimed by `test/worker`', 'createdAt': '2026-10-04T12:00:00Z'}]}
            with patch.object(batches, 'ROOT', reader), patch.object(lab, 'ROOT', reader), \
                 patch.object(batches, 'gh') as gh, patch.object(batches, 'issue', return_value=claimed):
                self.assertEqual(batches.cmd_done(args), 0)
                self.assertEqual(gh.call_count, 3)
                self.assertFalse((reader / '1-library/blogs/published.md').exists())
                for entry in ['1-library/blogs/missing.md', '1-library/topics.yaml',
                              '../outside.md', str(local), '1-library/talks/local.md']:
                    args.entries = [entry]
                    args.force = True
                    with self.subTest(entry=entry), self.assertRaises(SystemExit):
                        batches.cmd_done(args)
                    self.assertEqual(gh.call_count, 3)
                args.entries = ['1-library/blogs/local.md']
                for text in [entry_text('local').replace('topics: [meta]', 'topics: [other]'),
                             entry_text('local').replace('type: blog', 'type: talk'),
                             entry_text('local').replace('## Summary', '## Not summary'),
                             'not valid frontmatter']:
                    local.write_text(text)
                    with self.assertRaises(SystemExit):
                        batches.cmd_done(args)
                    self.assertEqual(gh.call_count, 3)
                link = reader / '1-library/blogs/link.md'
                link.symlink_to(local)
                args.entries = ['1-library/blogs/link.md']
                with self.assertRaises(SystemExit):
                    batches.cmd_done(args)
                link.unlink()
                args.entries = ['1-library/blogs/local.md']
                local.unlink()
                local.mkdir()
                with self.assertRaises(SystemExit):
                    batches.cmd_done(args)
                self.assertEqual(gh.call_count, 3)


if __name__ == '__main__':
    unittest.main()
