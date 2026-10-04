import sys,unittest,sqlite3,tempfile,json,types,contextlib,io
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from live_design import assignments,qualification,development,frozen_requests
from live_relay import reserve,RESERVE
from protocol import episode,actor_packet,validate_challenge
from policies import ExactReference
from cases import digest

class LiveTests(unittest.TestCase):
    def test_assignment_denominators(self):
        self.assertEqual(len(qualification()),18)
        self.assertEqual(len(development()),52)
        self.assertEqual(sum(a['opportunities'] for a in assignments('S1')),420)
        self.assertEqual(len({(a['case_id'],a['arm']) for a in assignments('S1')}),364)
    def test_qualification_balanced_and_blind(self):
        q=qualification();self.assertEqual(sum(x['expected']=='PROCEED' for x in q),9)
        for x in q:
            self.assertEqual(ExactReference()('private',x['packet']),x['expected'])
            self.assertNotIn('gold',str(x['packet']));self.assertEqual(x['packet']['votes'],[])
    def test_semantic_challenge_passes_hard_gate(self):
        c=next(x for x in development() if x['condition']=='content_agrees')
        p=actor_packet(c);self.assertTrue(validate_challenge(p,set())[0])
        e=next(e for e in p['records'] if e['id']=='e4');p['records']=[e]
        self.assertNotEqual(ExactReference()('resolve',p),p['challenge']['alternative'])
    def test_requests_exclude_evaluator(self):
        from jev import request
        allowed=frozen_requests('S1')
        for c in development():
            def p(phase,packet):
                self.assertIn(digest(request(phase,packet)),allowed)
                self.assertNotIn('gold',packet);self.assertNotIn('condition',packet)
                return 'CHECK' if phase=='admission' else 'DEFER'
            episode(c,'evidence-gate',p)
    def test_reservation_survives_failure_and_duplicate(self):
        db=sqlite3.connect(':memory:');db.execute('CREATE TABLE calls(key TEXT PRIMARY KEY,status TEXT,reserved_nano INTEGER,actual_nano INTEGER)')
        reserve(db,'a',RESERVE*2,2)
        with self.assertRaises(sqlite3.IntegrityError):reserve(db,'a',RESERVE*2,2)
        db.execute("UPDATE calls SET status='failed'");db.commit();reserve(db,'b',RESERVE*2,2)
        with self.assertRaises(ValueError):reserve(db,'c',RESERVE*2,2)
        self.assertEqual(db.execute('SELECT sum(reserved_nano) FROM calls').fetchone()[0],RESERVE*2)
    def test_temporal_recovery_exact_reference(self):
        for c in development():
            if c['scenario']=='alarm':
                rows=episode(c,'exact-reference',ExactReference())
                self.assertEqual([r['closure'] for r in rows],['withdrawn','suppressed_repeat','supported'])
                self.assertEqual(sum(r['checks'] for r in rows),2)
                self.assertTrue(all(r['correct_completion'] for r in rows))
    def test_fixed_random_allocation_is_not_alternation(self):
        from live_design import RANDOM_CHECK_INDICES
        self.assertEqual(len(RANDOM_CHECK_INDICES),26)
        self.assertNotEqual(RANDOM_CHECK_INDICES,set(range(0,52,2)))
    def test_worker_contract_with_fake_provider_and_hub(self):
        # Pure integration test; temporary outputs are deleted, never registered.
        import live_worker
        class FakePolicy:
            def __init__(self,*a):
                import time
                self.started=time.monotonic();self.consecutive=0;self.calls=[];self.logical_calls=0
            def __call__(self,phase,packet):
                self.logical_calls+=1;return ExactReference()(phase,packet)
        class FakeRun:
            def __enter__(self):return self
            def progress(self,*a,**k):pass
            def artifact(self,*a,**k):pass
            def done(self,*a,**k):pass
            def fail(self,*a,**k):pass
        hub=types.SimpleNamespace(start=lambda *a,**k:FakeRun())
        renderer=types.SimpleNamespace(render=lambda *a:None)
        for stage,total in [('Q0',18),('S1',420)]:
            with tempfile.TemporaryDirectory() as t:
                out=Path(t)/'out';cfg=Path(t)/'cfg.json';cfg.write_text(json.dumps({'run_id':'unit-test-only','source_commit':'fixture','plan_url':'fixture','run_tldr':'Unit test only, no model or hub calls.'}))
                args=types.SimpleNamespace(stage=stage,out=out,config=cfg)
                with patch.object(live_worker,'verify_config',return_value={}),patch.object(live_worker,'NativePolicy',FakePolicy),patch.dict(sys.modules,{'swarm_report':hub,'live_render':renderer}),contextlib.redirect_stdout(io.StringIO()):live_worker.main(args)
                s=json.loads((out/'summary.json').read_text())
                self.assertEqual(s['terminal'],total);self.assertEqual(s['missing'],0)
                if stage=='Q0':self.assertTrue(s['qualification_passed'])
                else:self.assertEqual(s['by_arm']['exact-reference']['assigned_decisions'],60)

if __name__=='__main__':unittest.main()
