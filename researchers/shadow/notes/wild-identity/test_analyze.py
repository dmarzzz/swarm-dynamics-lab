import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('analyze', Path(__file__).with_name('analyze.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class AnalysisTests(unittest.TestCase):
    def test_gini(self):
        self.assertEqual(m.gini([1, 1, 1]), 0)
        self.assertAlmostEqual(m.gini([0, 0, 3]), 2/3)
        self.assertEqual(m.gini([]), 0)
        self.assertEqual(m.gini([0, 0]), 0)

    def test_exact_identifier_matching(self):
        regex = m.matcher(['AgentOne', 'AgentOneX', 'shadow/lane'])
        self.assertEqual(m.references(regex, 'AgentOne AgentOneX AgentOne AgentOneXX @shadow/lane shadow/lane-long', 'AgentOne'), {'AgentOneX', 'shadow/lane'})
        self.assertEqual(m.references(regex, 'agentone', 'nobody'), set())

    def test_added_hunks_drop_inherited_reference(self):
        row = {'body': 'OldAgent\nnew note\n', 'hunks': [{'op': 'insert', 'b0': 1, 'b1': 2}], 'rev_id': 'example'}
        self.assertEqual(m.added_text(row), 'new note')
        row['hunks'][0]['b1'] = 99
        with self.assertRaises(ValueError): m.added_text(row)

    def test_archive_trailing_newline_offsets(self):
        row = {'body': 'old\nnew\n', 'hunks': [{'op': 'insert', 'b0': 1, 'b1': 3}], 'rev_id': 'example'}
        self.assertEqual(m.added_text(row), 'new\n')

    def test_zero_span_and_accounting(self):
        p = m.Population('wiki')
        p.event('a', 100); p.event('a', 100); p.event('b', 100); p.event('b', 3700); p.event(None, 3700)
        summary = p.summarize()
        self.assertEqual(summary['events'], 5)
        self.assertEqual(summary['attributed_events'], 4)
        self.assertEqual(summary['zero_span_identities'], 1)
        self.assertEqual(summary['singleton_identities'], 0)
        self.assertEqual(summary['median_span_hours'], .5)
        self.assertEqual(summary['unattributed_events'], 1)

    def test_reference_graph_and_isolates(self):
        p = m.Population('wiki')
        for i in ['a', 'b', 'c']: p.event(i, 100)
        regex = m.matcher(p.ids)
        p.graph_event('a', 'a b b b', regex, 'snapshot')
        p.graph_event('a', 'b', regex, 'fresh')
        p.graph_event('b', 'a', regex, 'fresh')
        graph = m.graph_summary(p, 'fresh')
        self.assertEqual(graph['directed_edges'], 2)
        self.assertEqual(graph['event_edge_occurrences'], 2)
        self.assertEqual(graph['largest_weak_component'], 2)
        self.assertEqual(graph['weak_components_including_isolates'], 2)
        self.assertEqual(graph['reciprocal_edge_fraction'], 1)

    def test_signoff_probe_not_identity(self):
        self.assertEqual(m.SIGNOFF.findall('- seed.json\n'), ['seed.json'])
        self.assertEqual(m.EXPLICIT_SIGNOFF.findall('Signed: AgentOne\n'), ['AgentOne'])
        self.assertEqual(m.EXPLICIT_SIGNOFF.findall("name='file'\n"), [])

    def test_dates_do_not_impute(self):
        self.assertIsNone(m.timestamp(None))
        self.assertIsNone(m.timestamp('R12345'))
        self.assertIsNone(m.timestamp('2026-01-01T00:00:00'))
        self.assertEqual(m.timestamp('1970-01-01T01:00:00Z'), 3600)

    def test_agent_prefix(self):
        self.assertEqual(m.AGENT.match('[shadow/sol-identity] notes: x').group('id'), 'shadow/sol-identity')
        self.assertIsNone(m.AGENT.match('[bot] index: x'))
        self.assertIsNone(m.AGENT.match('Merge branch main'))


if __name__ == '__main__':
    unittest.main()
