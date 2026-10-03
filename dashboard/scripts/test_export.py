"""Validate generated dashboard data without third-party test dependencies."""
import json
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'public/data'

def load(name):
    return json.loads((DATA / f'{name}.json').read_text())

class ContractTest(unittest.TestCase):
    def test_counts_and_identity(self):
        entries, summary = load('library'), load('summary')
        self.assertEqual(len(entries), summary['counts']['total'])
        self.assertEqual(len(entries), len({e['id'] for e in entries}))
        mapping = {'papers':'paper','blogs':'blog','threads':'thread','code':'code','datasets':'dataset','talks':'talk'}
        for folder, kind in mapping.items():
            self.assertEqual(summary['counts'][folder], sum(e['kind'] == kind for e in entries))
        for entry in entries:
            self.assertIsInstance(entry['topics'], list)
            self.assertIsInstance(entry['authors'], str)
            self.assertLessEqual(len(entry['summary']), 280)
        self.assertTrue(all(e['added_at'] for e in entries))

    def test_graph_and_sizes(self):
        graph = load('graph')
        ids = {n['id'] for n in graph['nodes']}
        self.assertEqual(ids, {e['id'] for e in load('library')})
        self.assertTrue(all(e['s'] in ids and e['t'] in ids for e in graph['edges']))
        for path in DATA.glob('*.json'):
            self.assertLess(path.stat().st_size, 5_000_000)

    def test_agents_and_gate(self):
        self.assertEqual(sum(a['entries_added'] for a in load('agents')), len(load('library')))
        for survey in load('surveys'):
            self.assertEqual(survey['gate']['passes'], not survey['gate']['missing'])
        self.assertTrue(all(row['n_entries'] > 0 for row in load('timeline')))

if __name__ == '__main__':
    unittest.main()
