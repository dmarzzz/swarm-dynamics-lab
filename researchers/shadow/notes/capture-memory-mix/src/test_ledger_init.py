"""J007: construction may initialize once but must never reset existing spend."""
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest
import model


def initialize_and_add(path):
    ledger = model.Ledger(Path(path))
    ledger.add('test/model', .125, 1)


class LedgerInitializationTest(unittest.TestCase):
    def test_concurrent_initialization_preserves_all_additions(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'ledger.json'
            with ProcessPoolExecutor(max_workers=4) as pool:
                list(pool.map(initialize_and_add, [str(path)] * 32))
            d = json.loads(path.read_text())
            self.assertEqual(d['spent_usd'], 4)
            self.assertEqual(d['calls'], 32)
            self.assertEqual(d['by_model']['test/model'], {'usd': 4., 'calls': 32})

    def test_existing_bytes_including_corrupt_ledger_are_never_reset(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'ledger.json'
            for original in ['{"spent_usd": 1.5, "calls": 2, "by_model": {}}', '', 'corrupt']:
                path.write_text(original)
                model.Ledger(path)
                self.assertEqual(path.read_text(), original)
            with self.assertRaises(json.JSONDecodeError):
                model.Ledger(path).spent()


if __name__ == '__main__':
    unittest.main()
