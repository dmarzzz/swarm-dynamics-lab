"""J019: reject invalid financial and timeout inputs before dispatch."""
import argparse
import unittest
from unittest.mock import patch
import collect


class ApifyBudgetTest(unittest.TestCase):
    def args(self, **updates):
        return argparse.Namespace(**({'max_usd': .5, 'hard_cap': 4., 'timeout': 300} | updates))

    def test_invalid_budget_fails_before_secret_or_network(self):
        for name in ('max_usd', 'hard_cap'):
            for value in (float('nan'), float('inf'), -float('inf'), -1, 0, True):
                with self.subTest(name=name, value=value), patch.object(collect, 'secret') as key, \
                     patch.object(collect, 'http') as http:
                    with self.assertRaises(SystemExit):
                        collect.cmd_apify(self.args(**{name: value}))
                    key.assert_not_called()
                    http.assert_not_called()

    def test_invalid_timeout_fails_before_secret(self):
        for value in (0, -1, 1.5, float('nan'), float('inf'), True):
            with self.subTest(value=value), patch.object(collect, 'secret') as key:
                with self.assertRaises(SystemExit):
                    collect.cmd_apify(self.args(timeout=value))
                key.assert_not_called()

    def test_valid_parameters_reach_credential_admission(self):
        with patch.object(collect, 'secret', side_effect=RuntimeError('synthetic sentinel')) as key:
            with self.assertRaisesRegex(RuntimeError, 'sentinel'):
                collect.cmd_apify(self.args())
            key.assert_called_once_with('apify_token')

    def test_invalid_provider_account_values_never_dispatch(self):
        for spent, cap in [(float('nan'), 5), (-1, 5), (0, float('inf')), (0, 0), (0, -1)]:
            with self.subTest(spent=spent, cap=cap), patch.object(collect, 'secret', return_value='synthetic'), \
                 patch.object(collect, 'apify_spent', return_value=(spent, cap)), \
                 patch.object(collect, 'http') as http:
                with self.assertRaises(SystemExit):
                    collect.cmd_apify(self.args())
                http.assert_not_called()


if __name__ == '__main__':
    unittest.main()
