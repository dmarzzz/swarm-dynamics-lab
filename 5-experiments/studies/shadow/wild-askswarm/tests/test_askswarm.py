import gzip
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from askswarm import Event, analyze, Clusterer, gini, normalize, parse_time, wiki, swarmtraces, table, git_log, task_events
from askswarm.report import render


class AskSwarmTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize('ＡBC, Hello_World!'), 'abc hello world')

    def test_time(self):
        self.assertEqual(parse_time('1970-01-01T01:00:00+01:00'), 0)
        self.assertIsNone(parse_time('2026-01-01'))
        self.assertIsNone(parse_time('not a date'))
        self.assertIsNone(parse_time(float('nan')))
        self.assertEqual(parse_time('1234.5'), 1234.5)
        self.assertIsNone(parse_time(1e308))

    def test_gini(self):
        self.assertEqual(gini([1, 1, 1]), 0)
        self.assertAlmostEqual(gini([0, 0, 3]), 2 / 3)
        self.assertIsNone(gini([]))

    def test_exact_short_and_empty(self):
        c = Clusterer()
        self.assertEqual(c.add('Hello, WORLD'), c.add('hello world'))
        self.assertIsNone(c.add(''))
        self.assertNotEqual(c.add('hello'), c.add('world'))

    def test_near_duplicates(self):
        c = Clusterer()
        text = ' '.join(f'token{i}' for i in range(100))
        self.assertEqual(c.add(text), c.add(text + ' addedword'))
        self.assertNotEqual(c.add(text), c.add('different set of words does not resemble that paragraph'))

    def test_minimum_tokens(self):
        c = Clusterer(.1)
        self.assertNotEqual(c.add('a b c d e'), c.add('a b c d f'))

    def test_adoption_identity_not_records(self):
        rows = [Event('a', 0, 'same words'), Event('a', 2, 'same words'), Event('b', 5, 'same words')]
        r = analyze(rows)
        c = r['clusters'][0]
        self.assertEqual(c['time_to_k_seconds']['2'], 5)
        self.assertIsNone(c['time_to_k_seconds']['3'])
        self.assertEqual(r['summary']['time_to_k']['3']['not_observed_to_reach'], 1)
        self.assertEqual(r['influence'][0]['fractional_new_adopter_credit'], 1)

    def test_ties_no_causal_order(self):
        r = analyze([Event('b', 0, 'same', event_id='z'), Event('a', 0, 'same', event_id='a'), Event('c', 1, 'same')])
        self.assertEqual(r['clusters'][0]['first_movers'], ['a', 'b'])
        self.assertEqual(r['clusters'][0]['time_to_k_seconds']['2'], 0)
        self.assertEqual(sorted(x['fractional_new_adopter_credit'] for x in r['influence']), [.5, .5])

    def test_tie_window_invariant(self):
        one = [Event('a', 0, 'same', event_id='a'), Event('b', 0, 'same', event_id='z'), Event('c', 1, 'same')]
        two = [Event('a', 0, 'same', event_id='z'), Event('b', 0, 'same', event_id='a'), Event('c', 1, 'same')]
        self.assertEqual(analyze(one, window=1)['influence'], analyze(two, window=1)['influence'])

    def test_unknown_not_an_identity(self):
        r = analyze([Event(None, None, 'same'), Event(None, None, 'same')])
        self.assertEqual(r['summary']['identities'], 0)
        self.assertIsNone(r['summary']['multi_identity_clusters'])
        self.assertIsNone(r['summary']['participation_gini'])
        self.assertEqual(r['clusters'][0]['first_movers'], [])
        self.assertIsNone(r['clusters'][0]['time_to_k_seconds']['2'])
        self.assertEqual(r['influence'], [])

    def test_unknown_clock_does_not_win(self):
        r = analyze([Event('a', None, 'same'), Event('b', 5, 'same')])
        self.assertEqual(r['clusters'][0]['first_movers'], ['b'])
        self.assertEqual(r['clusters'][0]['identities'], 2)
        self.assertEqual(r['clusters'][0]['dated_identities'], 1)

    def test_window_and_self_repeat(self):
        r = analyze([Event('a', 0, 'same'), Event('a', 1, 'same'), Event('c', 2, 'other'), Event('b', 3, 'same')], window=1)
        self.assertEqual(r['influence'], [])

    def test_empty(self):
        r = analyze([])
        self.assertEqual(r['summary']['records'], 0)
        self.assertIsNone(r['summary']['identity_coverage'])
        self.assertIn('Unavailable', render([r]))

    def test_escaping(self):
        r = analyze([Event('<script>bad()</script>', 0, 'secret source text')], name='<script>bad()</script>')
        page = render([r])
        self.assertNotIn('<script>', page)
        self.assertNotIn('secret source text', page)
        self.assertIn('&lt;script&gt;', page)

    def test_determinism(self):
        rows = [Event('a', 0, 'x', event_id='1'), Event('b', 1, 'x', event_id='2')]
        self.assertEqual(analyze(rows), analyze(reversed(rows)))

    def test_adapters(self):
        with tempfile.TemporaryDirectory() as root:
            p = Path(root) / 'revisions.jsonl.gz'
            with gzip.open(p, 'wt') as f:
                f.write(json.dumps({'rev_id': 'one', 'label': '', 'ip16': '10.2', 'time': None, 'body': 'x', 'page_id': 'p'}) + '\n')
            self.assertIsNone(next(wiki(root)).agent_id)
            self.assertEqual(next(wiki(root, 'ip16')).agent_id, '10.2')
            p = Path(root) / 'redacted.jsonl.gz'
            with gzip.open(p, 'wt') as f:
                f.write(json.dumps({'id': 'r1', 'time_utc': None, 'text': 'Agent: Alice; 2026-01-01', 'parent_id': 'r0'}) + '\n')
            event = next(swarmtraces(root))
            self.assertIsNone(event.agent_id)
            self.assertIsNone(event.time)
            self.assertEqual(event.thread, 'r0')
            p = Path(root) / 'table.csv'
            p.write_text('agent_id,time,text,thread\na,2026-01-01T00:00:00Z,hello,t\n')
            self.assertEqual(next(table(p)).agent_id, 'a')
            p.write_text('name,text\na,hello\n')
            with self.assertRaises(ValueError):
                list(table(p))

    def test_compact_export(self):
        from askswarm.cli import save_result, checksum
        result = analyze([Event('a', 0, str(i)) for i in range(120)])
        with tempfile.TemporaryDirectory() as root:
            compact = save_result(result, root)
            self.assertEqual(len(compact['clusters']), 100)
            with gzip.open(Path(root) / 'clusters.json.gz', 'rt') as stream:
                self.assertEqual(len(json.load(stream)), 120)
            before = checksum(Path(root) / 'clusters.json.gz')
            save_result(result, root)
            self.assertEqual(before, checksum(Path(root) / 'clusters.json.gz'))

    def test_git_adapter(self):
        with tempfile.TemporaryDirectory() as root:
            def git(*args):
                return subprocess.check_output(['git', '-C', root, *args], stderr=subprocess.DEVNULL)
            git('init')
            git('config', 'user.name', 'fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            git('commit', '--allow-empty', '-m', '[test/agent] task: claim fixture-task')
            git('commit', '--allow-empty', '-m', '[bot] index: rebuild')
            events = list(git_log(root))
            self.assertEqual(len(events), 2)
            self.assertEqual(sum(e.agent_id is not None for e in events), 1)
            tasks = list(task_events(root))
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].thread, 'fixture-task')


if __name__ == '__main__':
    unittest.main()
