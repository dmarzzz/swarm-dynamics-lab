"""Regression: done accepts entries published by another checkout."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('batches', Path(__file__).with_name('batches.py'))
batches = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batches)

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
            (writer / 'seed').write_text('seed')
            git(writer, 'add', '.')
            git(writer, 'commit', '-m', 'seed')
            git(writer, 'push', 'origin', 'main')
            git(root, 'clone', '--branch', 'main', str(remote), str(reader))
            (writer / 'library').mkdir()
            (writer / 'library/published.md').write_text('published')
            git(writer, 'add', '.')
            git(writer, 'commit', '-m', 'another worktree writes entry')
            git(writer, 'push', 'origin', 'main')
            (reader / 'local.md').write_text('local')
            args = argparse.Namespace(entries=['library/published.md', 'local.md'], force=False,
                                      agent='test/worker', issue='1', skipped=None)
            with patch.object(batches, 'ROOT', reader), patch.object(batches, 'gh') as gh:
                self.assertEqual(batches.cmd_done(args), 0)
                self.assertEqual(gh.call_count, 3)
                self.assertFalse((reader / 'library/published.md').exists())
                args.entries = ['library/missing.md']
                with self.assertRaises(SystemExit):
                    batches.cmd_done(args)
                self.assertEqual(gh.call_count, 3)

if __name__ == '__main__':
    unittest.main()
