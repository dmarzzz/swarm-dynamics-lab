"""Offline containment regressions, also run with python -O.

These tests do not mock the hold. Historical provider-interface tests mock it
explicitly while mocking all network I/O, to keep old interface checks useful.
"""
import unittest
from unittest.mock import patch
import factory as f
import paid
import structured
import pool_structured


class LaunchHoldTests(unittest.TestCase):
    def test_all_provider_entrypoints_block_before_context_or_network(self):
        for adapter in (f, paid, structured, pool_structured):
            with self.subTest(adapter=adapter.__name__), \
                 patch.object(f, 'load_parent') as context, \
                 patch('urllib.request.urlopen') as network:
                # Empty dicts prove the first boundary blocks before spec/input
                # access, source loading, context assembly or credential use.
                with self.assertRaisesRegex(RuntimeError, 'factory_launch_held'):
                    adapter.call({}, {}, 'offline-dummy-not-a-secret')
                context.assert_not_called()
                network.assert_not_called()

    def test_run_blocks_before_initialization_and_credentials(self):
        with patch.object(f, 'assignments') as initialize, \
             patch.object(f, 'pool_key') as credentials, \
             patch('urllib.request.urlopen') as network:
            with self.assertRaisesRegex(RuntimeError, 'factory_launch_held'):
                f.run({})
            initialize.assert_not_called()
            credentials.assert_not_called()
            network.assert_not_called()

    def test_environment_cannot_opt_out(self):
        with patch.dict('os.environ', {'FACTORY_ALLOW_LAUNCH': '1', 'FACTORY_PI_GATE': 'off'}):
            with self.assertRaisesRegex(RuntimeError, 'factory_launch_held'):
                f.enforce_launch_hold()

    def test_offline_schema_and_statistics_remain_available(self):
        self.assertEqual(f.bootstrap({'fixture': [1, 1]}, 10), [1, 1])
        self.assertEqual(f.parse_answer('{"values":{"0":0,"1":1,"2":2,"3":3,"4":4,"5":5}}')['values']['0'], 0)


if __name__ == '__main__':
    unittest.main()
