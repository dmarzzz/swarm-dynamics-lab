"""J030: these same tests must pass under Python and Python -O."""
import ast
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import factory as f
import paid


class OperationalGuardsTest(unittest.TestCase):
    def test_runtime_files_have_no_optimized_away_guards(self):
        for module in (f, paid):
            self.assertFalse(any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(Path(module.__file__).read_text()))))

    def test_invalid_specs_and_pins_are_rejected(self):
        for module, original in [(f, {'route':'anthropic-pool', 'model':'claude-sonnet-4-6',
                                     'max_paid_usd':0, 'max_calls':204, 'concurrency':2}),
                                 (paid, {'route':'openrouter', 'model':'anthropic/claude-sonnet-4.6',
                                         'max_paid_usd':4, 'max_calls':204, 'concurrency':2})]:
            with self.subTest(module=module.__name__), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / 'specs').mkdir()
                p = root / 'specs/example.json'
                with patch.object(f, 'ROOT', root), patch.object(f, 'REPO', root):
                    for field, bad in [('route','unapproved'), ('model','wrong'), ('max_paid_usd',999),
                                       ('max_calls',999), ('concurrency',999)]:
                        p.write_text(json.dumps(original | {field:bad}))
                        with self.subTest(field=field), self.assertRaises(AssertionError):
                            module.read_spec('example', frozen=False)
                    p.write_text(json.dumps(original | {'source_sha256':{'runtime.py':'expected'}}))
                    with patch.object(f.subprocess, 'check_output', return_value=b'different bytes'):
                        with self.assertRaises(AssertionError):
                            module.read_spec('example')
                    with patch.object(f.subprocess, 'check_output', return_value=p.read_bytes()), \
                         patch.object(f, 'sha', return_value='drifted'):
                        with self.assertRaises(AssertionError):
                            module.read_spec('example')

    def test_invalid_costs_never_append_a_reservation(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'test-ledger.jsonl'
            ledger = paid.Ledger(path)
            for value in (-1, float('nan'), float('inf')):
                with self.subTest(value=value), self.assertRaises(AssertionError):
                    ledger.event('reserve', 'test', 'call', value)
            self.assertEqual(path.read_text(), '')

    def test_invalid_answers_still_rejected(self):
        for text in ['{}', '{"values":{}}', '{"values":{"0":true,"1":0,"2":0,"3":0,"4":0,"5":0}}']:
            with self.subTest(text=text), self.assertRaises(AssertionError):
                f.parse_answer(text)


if __name__ == '__main__':
    unittest.main()
