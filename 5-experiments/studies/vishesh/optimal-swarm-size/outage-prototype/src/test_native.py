import json,tempfile,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
from native import Native,payload,QUOTE,SCHEMA
from run_outage import assignments,admission_errors,FLAGS
from engine import execute
from world import make_case,ARMS
from test_outage import scripted
from budget import Budget
from failures import SafeFailure
from replay_outage import render

class NativeTests(unittest.TestCase):
    def test_admission_requires_each_scope_fact_and_freshness(self):
        a={k:True for k in FLAGS}|dict(source_commit='a',attempt_id='outage-o1',credential_alias='local-openrouter-relay',claim_id='x',verified_epoch=100,claim_expiry_epoch=8000,dispatch_origin='owner-directed-outage-prototype')
        self.assertEqual(admission_errors(a,'a',100),[])
        for k in FLAGS:self.assertIn(k,admission_errors(a|{k:False},'a',100))
        self.assertIn('source_mismatch',admission_errors(a,'b',100))
        self.assertIn('admission_stale',admission_errors(a,'a',401))
        self.assertIn('claim_too_short',admission_errors(a|{'claim_expiry_epoch':200},'a',100))
    def test_assignment_envelope(self):
        rows=assignments();self.assertEqual(len(rows),12);self.assertEqual(len({r['id'] for r in rows}),12)
        self.assertEqual([r['root'] for r in rows[:4]],list(range(4)))
        self.assertTrue(all(r['arm']=='single' for r in rows[:4]))
        self.assertEqual(sum(8*(1 if r['arm']=='single' else 0 if r['arm']=='scheduled' else 4) for r in rows),176)
        self.assertLessEqual(224*QUOTE,6000000)
    def test_full_schema_payload_bound_on_all_fixtures(self):
        sizes=[]
        def call(messages,actor,tick):sizes.append(len(json.dumps(payload(messages)).encode()));return scripted(messages,actor,tick)
        for root in range(4):
            for arm in ARMS:execute(make_case(root,True,10),arm,call)
        self.assertLess(max(sizes),12000)
    def test_budget_reservations_are_atomic_and_holds_persist(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'ledger';bank=Budget(path,20_000_000,'outage-o1',6000000)
            for i in range(32):bank.reserve(str(i),'episode',QUOTE,850000)
            self.assertEqual(bank.exposure('episode'),32*QUOTE)
            with self.assertRaises(ValueError):bank.reserve('33','episode',QUOTE,720000)
            with self.assertRaises(ValueError):bank.reserve('0','episode',QUOTE,850000)
            reopened=Budget(path,20_000_000,'outage-o1',6000000);self.assertEqual(reopened.exposure('episode'),32*QUOTE)
    def test_no_dispatch_after_stop_or_oversized_input(self):
        with tempfile.TemporaryDirectory() as t:
            b=Budget(Path(t)/'ledger',20_000_000,'outage-o1',6000000);stop=threading.Event();stop.set()
            n=Native(b,'ep',lambda _:None,time.time()+9000,stop)
            with patch('native.request_child') as transport:
                with self.assertRaises(SafeFailure):n([{'role':'user','content':'x'}],0,0)
                with self.assertRaises(SafeFailure):n([{'role':'user','content':'x'*13000}],0,0)
                transport.assert_not_called()
            self.assertEqual(b.exposure('ep'),0)
    def test_saved_replay_handles_zero_tick_failure(self):
        def fail(*args):raise SafeFailure('http_429')
        r=execute(make_case(0),'single',fail)
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'replay.html';render(r,path);s=path.read_text()
            self.assertIn('http_429',s);self.assertIn('no completed simulation ticks',s);self.assertIn('unobserved',s)

    def test_openrouter_cost_and_fee_hold(self):
        from openrouter_route import charge,settle
        self.assertEqual(charge({'prompt_tokens':10,'completion_tokens':2,'cost':.000021}),21)
        with self.assertRaises(SafeFailure):charge({'prompt_tokens':1,'completion_tokens':2})
        with tempfile.TemporaryDirectory() as t:
            bank=Budget(Path(t)/'ledger',20_000_000,'outage-o1',6000000);bank.reserve('call','ep',QUOTE,850000)
            settle(bank,'call',21)
            self.assertEqual(bank.exposure('ep'),24)
            with bank.connect() as db:self.assertEqual(db.execute('SELECT actual,state FROM calls').fetchone(),(21,'settled_with_fee_hold'))
    def test_relay_finite_call_allowlist(self):
        from local_relay import allowed_calls
        ids=allowed_calls();self.assertEqual(len(ids),176)
        self.assertNotIn('outage-o1/qualification/0/1/single/0/1',ids)
        self.assertFalse(any('/scheduled/' in i for i in ids))

if __name__=='__main__':unittest.main()
