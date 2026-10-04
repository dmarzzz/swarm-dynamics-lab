"""Offline fault tests: no network, paid credentials or model calls."""
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
from PIL import Image
import coordinator
import provider
import render
import study
import worker


class Checks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q=study.assignments('Q0'); cls.p=study.assignments('S1')

    def test_disjoint_complete_deterministic(self):
        self.assertEqual(self.p,study.assignments('S1'))
        self.assertEqual((len(self.q),len(self.p)),(24,192))
        self.assertFalse({r['task'] for r in self.q}&{r['task'] for r in self.p})
        self.assertTrue(all(r['task']<10000 for r in self.q+self.p))

    def test_mask_is_only_treatment(self):
        paired={}
        for r in self.q+self.p:
            key=(r['kind'],r['task'],r['arm'],r['attacker_pass'])
            packet=json.loads(json.dumps(r['packet']))
            for report in packet['reports']:
                self.assertTrue(set(report)<={'node','skill','claim','age','activity','verification'})
                self.assertNotIn('truth',report)
                report.pop('verification',None)
            if key in paired: self.assertEqual(paired[key],packet)
            else: paired[key]=packet

    def test_clean_competence_and_missing(self):
        rows=[{**r,'status':'completed','evaluation':study.evaluate(r,study.scripted(r['packet']))} for r in self.q]
        self.assertTrue(study.qualification(rows)['passed'])
        wrong=study.scripted(self.q[0]['packet']); wrong['values']['0']=9999
        self.assertLess(study.evaluate(self.q[0],wrong)['qualification_accuracy'],1)
        self.assertFalse(study.qualification(rows[:-1])['passed'])

    def test_admission_independent_of_badges(self):
        groups={}
        for r in self.p:
            k=(r['task'],r['arm'],r['attacker_pass'])
            if k in groups: self.assertEqual(groups[k],r['admitted'])
            else: groups[k]=r['admitted']

    def response(self, answer=None, **kwargs):
        data={'model':study.design()['model'],'stop_reason':'end_turn',
              'usage':{'input_tokens':500,'output_tokens':50},
              'content':[{'type':'text','text':json.dumps(answer or study.scripted(self.q[0]['packet']))}]}
        data.update(kwargs)
        return io.BytesIO(json.dumps(data).encode())

    def backend(self,path,opener):
        with patch.dict(os.environ,{'SWARM_MODEL_API_KEY':'offline-test-placeholder','SWARM_MODEL_WORKSPACE_ID':'offline-test-workspace'}):
            return provider.Anthropic(provider.Ledger(path),opener)

    def test_usage_persisted_and_duplicate_refused(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'ledger.jsonl'; b=self.backend(path,lambda *a,**k:self.response())
            answer,account=b.call(self.q[0]['packet'],'q:1')
            self.assertEqual(account['actual_usd'],.00075)
            self.assertEqual(provider.Ledger(path).transact()['attempted_calls'],1)
            with self.assertRaisesRegex(provider.CallFailure,'duplicate'): b.call(self.q[0]['packet'],'q:1')

    def test_http_failure_once_and_reserved_across_restart(self):
        calls=[]
        def fail(*a,**kw):
            calls.append(1)
            raise urllib.error.HTTPError('redacted',429,'redacted',{},None)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'ledger'; b=self.backend(path,fail)
            with self.assertRaisesRegex(provider.CallFailure,'http_429'): b.call(self.q[0]['packet'],'q:2')
            state=provider.Ledger(path).transact()
            self.assertEqual(len(calls),1); self.assertGreater(state['reserved_usd'],0)
            self.assertEqual(state['usage_reported_calls'],0)

    def test_budget_refuses_before_network(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'ledger'; ledger=provider.Ledger(path)
            ledger.transact({'type':'reserve','call_id':'existing-study','micro_usd':5_000_000})
            b=self.backend(path,lambda *a,**k:self.fail('Network must not be called'))
            with self.assertRaisesRegex(provider.CallFailure,'budget'): b.call(self.q[0]['packet'],'q:3')
            self.assertEqual(ledger.transact()['attempted_calls'],1)

    def test_malformed_and_truncated_preserve_billing(self):
        for changes in ({'stop_reason':'max_tokens'},{'content':[{'type':'text','text':'invalid'}]}):
            with tempfile.TemporaryDirectory() as d:
                path=Path(d)/'ledger'; b=self.backend(path,lambda *a,**k:self.response(**changes))
                with self.assertRaises(provider.CallFailure) as caught: b.call(self.q[0]['packet'],'q:4')
                self.assertEqual(caught.exception.accounting['actual_usd'],.00075)
                self.assertEqual(provider.Ledger(path).transact()['usage_reported_calls'],1)

    def test_missing_usage_keeps_reserve(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'ledger'; b=self.backend(path,lambda *a,**k:self.response(usage={}))
            with self.assertRaisesRegex(provider.CallFailure,'missing_usage'): b.call(self.q[0]['packet'],'q:5')
            self.assertGreater(provider.Ledger(path).transact()['reserved_usd'],0)

    def test_bad_output_schema_and_holdout_blocked(self):
        with self.assertRaises(ValueError): study.validate({'values':{'0':True}})
        with self.assertRaises(ValueError): study.params('S2')

    def test_failure_stops_and_keeps_denominator(self):
        class Failure:
            n=0
            def call(self,*args):
                self.n+=1
                raise provider.CallFailure('injected_failure',{'attempted':True})
        with tempfile.TemporaryDirectory() as d:
            backend=Failure(); out=Path(d)/'out'
            with patch.dict(os.environ,{'SYBIL_API_BUDGET_LEDGER':str(Path(d)/'ledger')}):
                with self.assertRaisesRegex(RuntimeError,'preserved'):
                    worker.execute(study.params('Q0'),out,backend=backend)
            rows=[json.loads(s) for s in (out/'episodes.jsonl').read_text().splitlines()]
            self.assertEqual(backend.n,1); self.assertEqual(len(rows),24)
            self.assertEqual(sum(r['status']=='not_started' for r in rows),23)
            self.assertEqual(json.loads((out/'summary.json').read_text())['invalid'],24)
            with Image.open(out/'replay.gif') as im:
                self.assertEqual(im.size,(1800,1180)); self.assertEqual(im.n_frames,2)

    def test_coordinator_qualification_blocks(self):
        class Hub:
            def runs(self,*a,**k): return []
        with self.assertRaisesRegex(ValueError,'qualification'): coordinator.enqueue(Hub(),'S1')


if __name__=='__main__': unittest.main()
