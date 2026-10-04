#!/usr/bin/env python3
"""Network-blocked qualification of transport, accounting, leakage and replay."""
import copy
import json
import socket
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import common,coordinator,provider,sim,worker
from policy import mock_opener,MockResponse,Policy

def observation():
    d=common.design();market=sim.task(20)
    return sim.make_observation(market,{'trace':[],'n':1,'cash':20000,'rival_q':market['rival_capacities']},'firm',0.38,d['cfg'])
class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)
        self.ledger=provider.Ledger(self.path/'ledger.jsonl')
    def tearDown(self):self.tmp.cleanup()
    def client(self,opener=mock_opener):return provider.Anthropic(self.ledger,opener,key='offline',workspace='offline')
    def test_real_transport_shape_and_action(self):
        seen=[]
        def transport(req,timeout):
            seen.append(json.loads(req.data));return mock_opener(req,timeout)
        action,account=self.client(transport).call(observation(),'ok')
        sim.validate(action,observation());self.assertTrue(account['usage_reported'])
        body=seen[0];self.assertEqual(body['model'],common.design()['model']);self.assertEqual(body['temperature'],0)
        self.assertEqual(body['output_config']['format']['schema'],provider.SCHEMA)
        self.assertEqual(len(body['messages']),1)
        self.assertEqual(self.ledger.transact()['attempted_calls'],1)
    def test_failures_spend_reservation_no_retry(self):
        n=[]
        def fail(req,timeout):n.append(1);raise urllib.error.HTTPError(req.full_url,429,'SECRET-MARKER',{},None)
        with self.assertRaises(provider.CallFailure) as e:self.client(fail).call(observation(),'http')
        self.assertEqual(str(e.exception),'http_429');self.assertEqual(len(n),1)
        self.assertEqual(self.ledger.transact()['attempted_calls'],1)
        self.assertNotIn('SECRET-MARKER',(self.path/'ledger.jsonl').read_text())
    def test_duplicate_and_durable_limit(self):
        self.client().call(observation(),'same')
        with self.assertRaises(provider.CallFailure):self.client().call(observation(),'same')
        d=common.design();d['budget']['max_attempted_calls']=1
        with patch.object(common,'design',return_value=d):
            with self.assertRaises(provider.CallFailure):self.client().call(observation(),'new')
        self.assertEqual(provider.Ledger(self.path/'ledger.jsonl').transact()['attempted_calls'],1)
    def test_corrupt_ledger_fail_closed(self):
        (self.path/'ledger.jsonl').write_text('{broken')
        with self.assertRaises(json.JSONDecodeError):self.client().call(observation(),'never')
    def test_nonterminal_and_missing_usage(self):
        for name,edit in [('stop',lambda x:x.update(stop_reason='max_tokens')),('usage',lambda x:x.pop('usage'))]:
            def malformed(req,timeout):
                x=mock_opener(req,timeout).data;edit(x);return MockResponse(x)
            with self.assertRaises(provider.CallFailure):self.client(malformed).call(observation(),name)
        self.assertEqual(self.ledger.transact()['attempted_calls'],2)
    def test_invalid_actions_preserved(self):
        def invalid(req,timeout):
            x=mock_opener(req,timeout).data;x['content'][0]['text']='{"operation":"register","quantities":[[999,999]],"note":"invalid"}';return MockResponse(x)
        pol=Policy(self.client(invalid),self.path/'calls.jsonl','invalid','anthropic',60)
        rs=sim.run_episode(20,31,'none',0.38,['neutral_dynamic'],{**common.design()['cfg'],'rounds':3},pol)
        self.assertFalse(rs[0]['validity']['ok']);self.assertEqual(len(pol.calls),1)
        self.assertIn('999',json.loads((self.path/'calls.jsonl').read_text())['accounting']['response_text'])
    def test_input_size_before_reservation(self):
        obs=observation();obs['oversize']='x'*21000
        with self.assertRaises(provider.CallFailure):self.client().call(obs,'large')
        self.assertEqual(self.ledger.transact()['attempted_calls'],0)
    def test_no_evaluator_or_hint_leakage(self):
        obs=observation();self.assertEqual(set(obs),{'round','market','portfolio','rules','last_competitor_outputs','history'})
        text=json.dumps(obs)+provider.SYSTEM
        for forbidden in ('strategic_fragmentation','counterfactual','split_control','profit_search','MKT-03','evasion','sybil'):
            self.assertNotIn(forbidden,text)
        self.assertNotIn('owner_hhi',json.dumps(obs))
    def test_locked_arm_and_common_draws(self):
        seen=[]
        def policy(obs,arm):
            seen.append(obs);return sim.scripted_action(obs,'merged')
        cfg={**common.design()['cfg'],'rounds':4,'max_firms':1}
        a=sim.run_episode(20,31,'none',0.38,['neutral_locked'],cfg,policy)[0]
        b=sim.run_episode(20,31,'firm',0.38,['neutral_locked'],cfg,policy)[0]
        self.assertEqual(a['draws_sha256'],b['draws_sha256'])
        self.assertTrue(all(o['portfolio']['max_firms']==1 for o in seen))
        bad={'operation':'register','quantities':[[1,1],[1,1]],'note':''}
        with self.assertRaises(ValueError):sim.validate(bad,seen[0])
    def test_gates_and_visual_bundle(self):
        with self.assertRaises(ValueError):coordinator.gate('S1',[])
        p=coordinator.plans('S0','selftest')[0];p['rounds']=5
        m=worker.execute_bundle(p,self.path/'bundle')
        self.assertEqual(m['invalid'],0);self.assertEqual(m['model_calls'],0);self.assertEqual(m['api_cost_usd'],0)
        self.assertEqual(m['visual_ok'],1)
        with Image.open(self.path/'bundle/replay.gif') as im:
            self.assertEqual(im.n_frames,5);self.assertEqual(im.size,(1080,720))
        rows=[json.loads(s) for s in (self.path/'bundle/episodes.jsonl').read_text().splitlines()]
        self.assertEqual(rows[0]['draws_sha256'],rows[1]['draws_sha256'])
        locked=next(r for r in rows if r['arm']=='neutral_locked');self.assertEqual(locked['evaluation']['final_firm_count'],1)
if __name__=='__main__':
    with patch.object(socket.socket,'connect',side_effect=AssertionError('network disabled')):
        unittest.main(verbosity=2)
