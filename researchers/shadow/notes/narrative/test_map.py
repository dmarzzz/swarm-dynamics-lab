#!/usr/bin/env python3
"""Contract tests for the map, independent of any experiment implementation."""
import json
from pathlib import Path
import unittest
import build_map

ROOT = Path(__file__).resolve().parent


class UnitTests(unittest.TestCase):
    def test_attribution(self):
        self.assertEqual(build_map.owner_of('Cytonomy', '[vishesh/codex-1] task'), ('vishesh', 'vishesh/codex-1'))
        self.assertEqual(build_map.owner_of('wakesync', '[dmarz/a] test')[0], 'dmarz')
        self.assertIsNone(build_map.owner_of('swarm-lab-bot', '[shadow/a] test')[0])
        self.assertEqual(build_map.owner_of('Ultron', 'update')[0], 'vishesh')
        self.assertIsNone(build_map.owner_of('unmapped', 'update')[0])

    def test_status_is_not_hub_done(self):
        row = {'status_at_assessment': 'unrun', 'evidence_confidence': {'score': 0}}
        self.assertEqual(build_map.scientific_status(row), 'designing')
        row['status_at_assessment'] = 'qualification_failed'
        self.assertEqual(build_map.scientific_status(row), 'negative')

    def test_activity_phase_does_not_invent_execution(self):
        self.assertEqual(build_map.activity_phase('[shadow/a] sync: 1 file'), 'phase unverified')
        self.assertEqual(build_map.activity_phase('[dmarz/a] design: code ready; nothing launched'), 'designing')
        self.assertEqual(build_map.activity_phase('[vishesh/a] task: done assay'), 'done')
        self.assertEqual(build_map.activity_phase('[vishesh/a] qualification failed on fixed fixtures'), 'gated')
        self.assertEqual(build_map.activity_phase('[shadow/a] audit saved results'), 'analyzing')

    def test_score_cannot_use_commit_volume(self):
        candidate = {'evidence_ids': ['a','b','missing'], 'brief_fit': 1, 'readiness': 1}
        nodes = {'a': {'id': 'a', 'strength': .8, 'owner': 'dmarz', 'commits': 1},
                 'b': {'id': 'b', 'strength': .4, 'owner': 'shadow', 'commits': 99999}}
        result = build_map.score_headline(candidate, nodes, dict.fromkeys(['evidence','brief_fit','coverage','readiness'],1))
        self.assertAlmostEqual(result['components']['evidence'], .6)
        self.assertAlmostEqual(result['components']['coverage'], 2/3)
        self.assertAlmostEqual(result['components']['readiness'], 2/3)
        self.assertAlmostEqual(result['score'], 26.67)
        self.assertEqual(result['missing_evidence'], ['missing'])

    def test_design_is_not_evidence_coverage(self):
        candidate = {'evidence_ids':['a'], 'brief_fit':1, 'readiness':1}
        nodes = {'a': {'id':'a','strength':0,'owner':'shadow'}}
        self.assertEqual(build_map.score_headline(candidate,nodes,dict.fromkeys(['evidence','brief_fit','coverage','readiness'],1))['score'],0)

    def test_output_contract(self):
        d = json.loads((ROOT/'narrative.json').read_text())
        self.assertEqual(d['provenance']['model_calls'], 0)
        self.assertEqual(len(d['headlines']), 3)
        self.assertEqual(len(d['researchers']), 3)
        self.assertEqual(len(d['themes']), 5)
        ids = {n['id'] for n in d['findings']}
        self.assertEqual(len(ids), len(d['findings']))
        for n in d['findings']:
            self.assertIn(n['owner'], build_map.OWNERS)
            self.assertTrue(0 <= n['strength'] <= 1)
            self.assertTrue(n['source']['url'].startswith(build_map.BASE+d['source_commit']))
            if n['audit']:
                self.assertIn('scope', n['audit'])
        for h in d['headlines']:
            self.assertTrue(set(h['evidence_present']) <= ids)
            self.assertTrue(0 <= h['score'] <= 100)
            self.assertTrue(all(0<=x<=1 for x in h['components'].values()))
        for t in d['transfers']:
            self.assertIn(t['from'], ids)
            self.assertIn(t['to'], ids)
        self.assertNotIn('\u2014', json.dumps(d, ensure_ascii=False))
        self.assertNotIn('hosts', d['hub'])
        self.assertNotIn('events', d['hub'])


if __name__ == '__main__':
    unittest.main()
