"""Offline transport fault tests, never opens a network connection."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import transport as t

class Response:
    status=200
    def __init__(self,model='anthropic/claude-sonnet-5.5',cost=0.001): self.model=model; self.cost=cost
    def __enter__(self): return self
    def __exit__(self,*a): pass
    def read(self):
        return json.dumps(dict(model=self.model,usage=dict(cost=self.cost),choices=[dict(message=dict(content='cedar'))])).encode()

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.oldout=t.OUT; self.oldroot=t.frozen.ROOT
        t.OUT=Path(self.tmp.name); t.frozen.ROOT=t.OUT
        self.p=t.Router(key='offline-fake-credential')
    def tearDown(self):
        t.OUT=self.oldout; t.frozen.ROOT=self.oldroot; self.tmp.cleanup()
    def call(self): return self.p.call('sonnet',{'1':'cedar','-1':'raven'},[1]*8,dict(stage='qualification',id='test'))
    @patch.object(t.urllib.request,'urlopen',return_value=Response())
    def test_same_prompt_and_cost(self,m):
        self.assertEqual(self.call()['choice'],1)
        r=t.lines('requests.jsonl')[0]['payload']
        self.assertEqual(r['messages'][0]['content'],t.frozen.SYSTEM)
        self.assertEqual(r['messages'][1]['content'],t.frozen.user_prompt({'1':'cedar','-1':'raven'},[1]*8))
        self.assertEqual(r['provider'],{'allow_fallbacks':False}); self.assertEqual(r['max_tokens'],32)
        self.assertNotIn('temperature',r); self.assertEqual(self.p.cost,t.Decimal('0.001'))
    @patch.object(t.urllib.request,'urlopen',return_value=Response(cost=None))
    def test_missing_cost_halts(self,m):
        with self.assertRaises(t.frozen.Stop): self.call()
        self.assertTrue(self.p.halted); self.assertEqual(self.p.unknown,t.RESERVE)
    @patch.object(t.urllib.request,'urlopen',return_value=Response(model='wrong-model'))
    def test_wrong_model_halts(self,m):
        with self.assertRaises(t.frozen.Stop): self.call()
        self.assertTrue(self.p.halted)
    @patch.object(t.urllib.request,'urlopen')
    def test_budget_blocks_before_network(self,m):
        self.p.cost=t.Decimal('9.80')
        with self.assertRaises(t.frozen.Stop): self.call()
        m.assert_not_called()
    @patch.object(t.urllib.request,'urlopen')
    def test_qualification_cap(self,m):
        self.p.qcount=12
        with self.assertRaises(t.frozen.Stop): self.call()
        m.assert_not_called()
    @patch.object(t.urllib.request,'urlopen')
    def test_lineage_cap(self,m):
        self.p.count=1492
        with self.assertRaises(t.frozen.Stop): self.call()
        m.assert_not_called()

if __name__=='__main__': unittest.main()
