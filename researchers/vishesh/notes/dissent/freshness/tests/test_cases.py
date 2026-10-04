from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cases

class CasesTests(unittest.TestCase):
    def setUp(self):self.m=cases.build()
    def rows(self,fn):return [dict(id=a['id'],status='completed',action=fn(a),request_sha256=a['request_sha256'],ordered_request_sha256=a['ordered_request_sha256']) for a in self.m['assignments']]
    def test_exact_balance_and_reproducibility(self):
        self.assertEqual(self.m,cases.build());a=self.m['assignments'];self.assertEqual(len(a),48);self.assertEqual(len({x['root'] for x in a}),6);self.assertEqual(len({x['case'] for x in a}),12)
        for c in cases.CONDITIONS:
            for g in ('fresh','expired'):self.assertEqual(sum(x['condition']==c and x['group']==g for x in a),6)
    def test_treatment_changes_only_receipt(self):
        for c in {a['case'] for a in self.m['assignments']}:
            d={a['condition']:a['request'] for a in self.m['assignments'] if a['case']==c}
            for context in ('0','1'):
                e=deepcopy(d['E'+context]);receipt=e['state'].pop('evidence_eligibility')
                self.assertEqual(e,d['R'+context]);self.assertEqual(receipt,cases.eligibility(e))
            raw=deepcopy(d['R1']);raw['state']['historical_last_verified']=None;raw['state']['supplied_ballots']=[]
            self.assertEqual(raw,d['R0'])
    def test_labels_and_gate_from_actor_inputs(self):
        for a in self.m['assignments']:
            req=a['request'];self.assertEqual(cases.reference(req),a['expected'])
            gate=cases.gate(req);self.assertEqual(gate['action'] is None,a['group']=='fresh')
            self.assertEqual(gate['action'] or cases.reference(gate['request']),a['expected'])
            self.assertEqual(len(gate['request']['state']['observations']),int(a['group']=='fresh'))
            self.assertEqual(len(gate['request']['state']['evidence_cards']),int(a['group']=='fresh'))
            self.assertNotIn('expected',json.dumps(req));self.assertNotIn('F0-',json.dumps(req))
    def test_expiry_boundary_future_and_mismatch(self):
        req=deepcopy(self.m['assignments'][0]['request']);t=req['state']['task'];r=req['state']['observations'][0]
        for age,want in [(0,True),(6,True),(7,True),(8,False),(-1,False)]:
            r['observed_at']=t['now']-age;self.assertEqual(cases.eligibility(req)['observations'][0]['eligible'],want)
        r['observed_at']=t['now']
        for f in ('scope','revision'):
            keep=r[f];r[f]='wrong';self.assertFalse(cases.eligibility(req)['observations'][0]['eligible']);r[f]=keep
    def test_card_cannot_launder_expired_observation(self):
        req=deepcopy(self.m['assignments'][0]['request']);req['state']['evidence_cards'][0]['observed_at']+=1
        with self.assertRaises(ValueError):cases.gate(req)
    def test_separate_corpus_labels_boundary_and_mixed_sources(self):
        rows=cases.qualification_corpus(123456);self.assertEqual(len(rows),54)
        for r in rows:
            self.assertEqual(cases.reference(r['request']),r['expected']);g=cases.gate(r['request']);self.assertEqual(g['action'] or cases.reference(g['request']),r['expected'])
        self.assertEqual(len({x['id'] for x in rows}),54)
        self.assertTrue({x['id'] for x in rows}.isdisjoint({x['case'] for x in self.m['assignments']}))
    def test_fault_policies_are_detected(self):
        for action in ('PROCEED','HOLD','DEFER'):
            score=cases.score(self.m,self.rows(lambda a:action));self.assertFalse(score['explicit_repair_signal'])
        self.assertTrue(any(cases.reference(dict(a['request'],state=dict(a['request']['state'],task=dict(a['request']['state']['task'],ttl=100))))!=a['expected'] for a in self.m['assignments']))
    def test_known_paired_effect_and_missing_bounds(self):
        rows=self.rows(lambda a:'PROCEED' if a['condition'].startswith('R') and a['group']=='expired' else a['expected'])
        s=cases.score(self.m,rows)
        for c in ('0','1'):
            self.assertEqual(s['paired_contrasts']['expired/'+c]['bounds'],[1,1]);self.assertEqual(s['paired_contrasts']['expired/'+c]['corrected'],6)
        self.assertTrue(s['explicit_repair_signal']);empty=cases.score(self.m,[])
        self.assertTrue(all(x['bounds']==[-1,1] for x in empty['paired_contrasts'].values()))
    def test_failed_outcome_cannot_be_defer_or_disappear(self):
        rows=self.rows(lambda a:a['expected']);rows[0].update(status='failed',action='DEFER')
        with self.assertRaises(ValueError):cases.score(self.m,rows)
        rows[0]['action']=None;s=cases.score(self.m,rows);self.assertEqual(sum(s['statuses'].values()),48)
