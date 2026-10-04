"""Offline software checks. All policy fixtures are synthetic, never model evidence."""
import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from domain import *
from engine import acquire, continuation
from analyze import recompute, summarize
from preflight import validate_plan, validate_receipt
from provider import StopRun, reserve
from runner import assignments


class OracleFixture:
    """Evaluator-aware control for unit checks ONLY, never an experimental policy."""
    def __init__(self, seed, scenario, mode='current'):
        self.seed, self.scenario, self.mode = seed, scenario, mode
    def complete(self, request):
        obs = request['observation']; step = obs['step']
        r = rules(self.seed, self.scenario, 0 if self.mode == 'stale' else step)
        docs = commands(self.scenario, 0 if self.mode == 'old_commands' else step)
        decisions = []
        for c in obs['cases']:
            a = oracle(c, self.scenario, r)
            if self.mode == 'trust_summary': a = 'ship' if c['summary'] == 'looks clear' else 'hold'
            if self.mode == 'always_check': a = r[c['service_class']]
            if self.mode == 'never_check': a = 'none'
            decisions.append({'id': c['id'], 'command': docs[a]})
        return {'value': {'decisions': decisions, 'notebook': 'UNIT FIXTURE — not learned model behavior'},
                'error': None, 'usage': None}


def trajectory(seed=1, scenario='release', arm='rolling', mode='current'):
    events = []; policy = OracleFixture(seed, scenario, mode)
    checkpoint = acquire(seed, scenario, policy, events.append)
    continuation(checkpoint, arm, policy, events.append)
    for e in events: e['run'] = f'unit-{scenario}-{seed}-{arm}'
    return checkpoint, events


class InstrumentTests(unittest.TestCase):
    def test_exact_replacements_and_descendant_ancestry(self):
        _, es = trajectory()
        self.assertEqual([m['generation'] for m in es[4]['crew_after']], [1, 1, 1])
        self.assertEqual([m['generation'] for m in es[7]['crew_after']], [2, 2, 2])
        for e in es[5:8]:
            child = next(m for m in e['crew_before'] if m['onboarding'])
            self.assertTrue(all(p['generation'] >= 1 for p in child['onboarding']['entries']))
            self.assertEqual(child['onboarding']['id'], es[e['step']-1]['archive']['id'])

    def test_shared_checkpoint_immutable_and_information_masks(self):
        p = OracleFixture(1, 'release'); shared=[]
        cp = acquire(1, 'release', p, shared.append); initial_hash = digest(cp)
        traces = {}
        for arm in ARMS:
            es=[]; continuation(cp, arm, p, es.append); traces[arm]=es
            self.assertEqual(digest(cp), initial_hash)
        for arm, es in traces.items():
            for e in es:
                for c in e['calls']:
                    obs = c['request']['observation']
                    self.assertNotIn('history', obs)
                    self.assertNotIn('explicit_current_rule', obs)
                    self.assertNotIn('evaluator', obs)
                    for ticket in obs['cases']:
                        self.assertNotIn('accepted_action', ticket)
                    for feedback in obs['feedback']:
                        prior = int(feedback['observation']['id'].split(':')[3])
                        self.assertLess(prior, e['step'])
                if 2 <= e['step'] <= 7:
                    child = e['crew_before'][(e['step']-2)%3]
                    if arm == 'none': self.assertIsNone(child['onboarding'])
                    if arm == 'frozen': self.assertEqual(child['onboarding']['id'], cp['founder_archive']['id'])
                self.assertLessEqual(len(e['archive']['text']), 2400)
        self.assertEqual(traces['rolling'][0]['cases'], traces['evidence'][0]['cases'])

    def test_current_and_stale_rule_boundary(self):
        for s in SCENARIOS:
            self.assertEqual(rules(4,s,4),rules(4,s,0))
            self.assertEqual(rules(4,s,5)['B'],rules(4,s,0)['B'])
            self.assertEqual(rules(4,s,5)==rules(4,s,0),s=='migration')
            _, es = trajectory(4,s)
            self.assertTrue(all(r['correct'] for e in es for r in e['scores']))
            for e in es: self.assertEqual(e['scores'],recompute(e))

    def test_mutation_controls_fail_where_they_should(self):
        for scenario in ('release','incident'):
            _,es=trajectory(4,scenario,mode='stale')
            after=[r for e in es[5:] for r in e['scores']]
            self.assertTrue(any(not r['correct'] for r in after if r['class']=='A'))
            self.assertTrue(all(r['correct'] for r in after if r['class']=='B'))
        for mode,scenario in (('trust_summary','release'),('always_check','incident'),('never_check','incident')):
            _,es=trajectory(4,scenario,mode=mode)
            self.assertTrue(any(not r['correct'] for e in es for r in e['scores']))
        _,es=trajectory(4,'migration',mode='old_commands')
        self.assertTrue(all(r['correct'] for e in es[:5] for r in e['scores']))
        self.assertTrue(all(not r['observed'] for e in es[5:] for r in e['scores']))
        self.assertTrue(any('invalid_command' in c['validation_errors'] for e in es[5:] for c in e['calls']))

    def test_missing_votes_and_duplicates(self):
        cases=tickets(1,'release',0); r=rules(1,'release',0); docs=commands('release',0)
        vote={c['id']:oracle(c,'release',r) for c in cases}
        two=score(cases,'release',r,r,[vote,vote,{}]); one=score(cases,'release',r,r,[vote,{},{}])
        self.assertTrue(all(x['correct'] and x['valid_votes']==2 for x in two))
        self.assertTrue(all(not x['observed'] and not x['correct'] for x in one))
        value={'decisions':[{'id':cases[0]['id'],'command':docs['ship']}]*2,'notebook':''}
        votes,errors=validate_output(value,cases,docs)
        self.assertNotIn(cases[0]['id'],votes);self.assertIn('missing_or_duplicate_case',errors)

    def test_splits_and_domain_coverage(self):
        for scenario in SCENARIOS:
            hist=history(5,scenario); ids={h['observation']['id'] for h in hist}
            seen=set()
            for step in range(10):
                cs=tickets(5,scenario,step)
                self.assertEqual(len(cs),6)
                self.assertTrue(ids.isdisjoint(c['id'] for c in cs))
                self.assertTrue(seen.isdisjoint(c['id'] for c in cs)); seen.update(c['id'] for c in cs)
                patterns={tuple(v['signal'] for v in c['evidence'].values()) for c in cs}
                self.assertGreaterEqual(len(patterns),3)
            # Every founding training example agrees with founding truth.
            self.assertTrue(all(h['accepted_action']==oracle(h['observation'],scenario,rules(5,scenario,0)) for h in hist))

    def test_plan_rejects_stale_revision_and_hash(self):
        md=(Path(__file__).resolve().parents[1]/'PLAN.md').read_text()
        url='https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/researchers/vishesh/notes/swarm-of-theseus/v2/PLAN.md'
        exp={'id':'swarm-of-theseus-v2','url':url,'description':'TLDR: test'}
        sha=hashlib.sha256(md.encode()).hexdigest(); tldr='condition-specific description '*5
        validate_plan(exp,md,url,sha,tldr)
        with self.assertRaisesRegex(ValueError,'revision_mismatch'): validate_plan(exp,md,url.replace('a'*40,'b'*40),sha,tldr)
        with self.assertRaisesRegex(ValueError,'hash_mismatch'): validate_plan(exp,md,url,'0'*64,tldr)

    def test_receipt_blocks_reused_or_expired_resources(self):
        now=time.time(); r={'experiment':'swarm-of-theseus-v2','source_commit':'abc', 'exclusive_claim_verified':True,
            'claim_id':'unit','host':'unit','verified_epoch':now,'claim_until_epoch':now+8000,
            'reserved_usd':15,'max_calls':660,'authority_allocation_id':'unit','owner_authorization_ref':'unit'}
        validate_receipt(r,'abc',now)
        for key,value in [('reserved_usd',.097684),('experiment','swarm-of-theseus'),('verified_epoch',now-901),('exclusive_claim_verified',False)]:
            bad=dict(r);bad[key]=value
            with self.assertRaises(ValueError):validate_receipt(bad,'abc',now)

    def test_budget_reservation_is_atomic_and_never_refunds(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=Path(td)/'budget.sqlite'
            with sqlite3.connect(ledger) as db:
                db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)')
                db.execute('INSERT INTO budget VALUES(1,15,14.9,658)')
            def attempt(_):
                try:return reserve(ledger,.04)
                except StopRun:return None
            with ThreadPoolExecutor(max_workers=4) as p: results=list(p.map(attempt,range(8)))
            self.assertEqual(len([r for r in results if r]),2)
            with sqlite3.connect(ledger) as db:
                self.assertEqual(db.execute('SELECT calls FROM budget').fetchone()[0],660)

    def test_manifest_call_counts_and_assigned_missing_bounds(self):
        self.assertEqual(sum(len(a['steps']) for a in assignments('S0')),24)
        self.assertEqual(sum(len(a['steps'])*3 for a in assignments('S1')),612)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'events').mkdir()
            (root/'manifest.json').write_text(json.dumps({'stage':'S1','assignments':assignments('S1')}))
            result=summarize(root)
            self.assertEqual(result['primary_bounds'],[-1,1])
            self.assertFalse(result['useful_signal_threshold_met'])
            self.assertFalse(any(w['identified_without_missingness'] for w in result['paired_worlds']))
            self.assertIsNone(result['metrics']['release:400']['rolling']['observed_accuracy'])

    def test_corrupt_score_is_detected(self):
        _,es=trajectory();bad=copy.deepcopy(es[9]);bad['scores'][0]['correct']=not bad['scores'][0]['correct']
        self.assertNotEqual(bad['scores'],recompute(bad))

    def test_render_fixture_provenance(self):
        from render import render
        # Optional destination retains software-test outputs for visual QA, not a trial.
        target=os.environ.get('THESEUS_UNIT_RENDER_DIR')
        with tempfile.TemporaryDirectory() as td:
            root=Path(target or td);root.mkdir(exist_ok=True);(root/'events').mkdir(exist_ok=True)
            _,es=trajectory(1,'release')
            for e in es:(root/'events'/f"unit-{e['step']}.json").write_text(json.dumps(e))
            (root/'manifest.json').write_text(json.dumps({'evidence_type':'unit_fixture','stage':'unit'}))
            render(root)
            html=(root/'replay.html').read_text()
            self.assertIn('SCRIPTED — NOT MODEL EVIDENCE',html)
            self.assertIn('"fixture": true',html)
            from PIL import Image
            with Image.open(root/'summary.png') as image:self.assertGreaterEqual(image.width,1600)

if __name__=='__main__':unittest.main()
