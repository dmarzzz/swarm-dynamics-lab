import copy,json,tempfile,unittest
from pathlib import Path
import instrument as i
import verification as v

class Instrument(unittest.TestCase):
    def test_assignment_balance_and_identical_initial_inputs(self):
        aa=i.assignments();self.assertEqual(len(aa),48);self.assertEqual(len({a['id'] for a in aa}),48)
        worlds={c['id']:c for c in v.roots()};inputs={}
        for a in aa:
            c=worlds[a['case_id']];o=v.observation(c,c['initial'],1,[]);q,b=i.request(c,o,'diagnosis')
            inputs.setdefault(a['case_id'],set()).add(i.digest(b))
            self.assertFalse(any(k in o for k in ('root','branch','guarded','repeat')))
        self.assertTrue(all(len(x)==1 for x in inputs.values()))
        self.assertEqual(aa,i.assignments())

    def test_full_rule_replay_and_paired_analysis(self):
        worlds={c['id']:c for c in v.roots()};rows=[i.episode(worlds[a['case_id']],a) for a in i.assignments()]
        self.assertTrue(all(r['qualified'] for r in rows));self.assertEqual(sum(len(r['events']) for r in rows),192)
        s=i.analyze(rows);self.assertEqual(s['completed'],48);self.assertEqual(len(s['paired_contrasts']),24)
        self.assertTrue(all(not any(x['outcome_disagrees'].values()) and not x['proposal_sequence_disagrees'] for x in s['fresh_repeat_disagreement']))
        self.assertTrue(all(x['complete_pairs']==4 for x in s['family_summaries']))
        self.assertTrue(all(x['complete_pairs']==2 for x in s['root_summaries']))
        partial=i.analyze(rows[:-1]);self.assertEqual(len(partial['missing_ids']),1)
        self.assertEqual(sum(not x['complete'] for x in partial['paired_contrasts']),1)
        with self.assertRaises(ValueError):i.analyze(rows+[rows[0]])

    def test_wrong_schema_order_stops_before_transition(self):
        c=v.roots()[0];a=i.assignments()[0];calls=[]
        def bad(q,b):
            calls.append(q)
            if len(calls)==1:return i.public_reference.labels(q['observation'])
            return {'action_id':'wait','reason':'wrong order'}
        with self.assertRaisesRegex(ValueError,'action_order_failed'):i.episode(c,a,bad)
        self.assertEqual(len(calls),2)

    def test_wrong_schema_valid_diagnosis_is_not_corrected(self):
        c=v.roots()[0];a=i.assignments()[0];seen=[]
        def wrong(q,b):
            if 'diagnosis' not in q['observation']:
                d=i.public_reference.labels(q['observation']);d['fault']='none';seen.append(d);return d
            self.assertEqual(q['observation']['diagnosis'],seen[-1])
            action=i.public_reference.choose(q['observation']);return {'reason':action['reason'],'action_id':action['action_id']}
        row=i.episode(c,a,wrong);self.assertFalse(row['diagnosis_pass']);self.assertFalse(row['qualified'])

    def test_actual_verification_timing_and_no_credit_for_protection(self):
        c=v.roots()[0];tr,s=v.simulate(c,False);self.assertTrue(s['post_action_verified'])
        self.assertIs(v.summarize(c,list(reversed(tr)))['post_action_verified'],False)
        for mutation in ('refresh','stale','unhealthy','rejected','not_useful'):
            t=copy.deepcopy(tr)
            if mutation=='refresh':t[1]['action']['action']='refresh'
            if mutation=='stale':t[1]['state']['probe']['epoch']-=1
            if mutation=='unhealthy':t[1]['state']['probe']['checks']['processes_live']=False
            if mutation=='rejected':t[0]['rejected']=1
            if mutation=='not_useful':t[0]['useful_restart']=0
            self.assertIsNot(v.summarize(c,t)['post_action_verified'],True,mutation)
        healthy=v.roots()[1];self.assertIsNone(v.simulate(healthy,True)[1]['post_action_verified'])

    def test_all_first_actions_fit_second_tick_bounds(self):
        # Explore each legal first action, both guard arms, not only the successful rule path.
        for c in v.roots():
            o=v.observation(c,c['initial'],1,[])
            schema=i.candidate.action_request(c,o,i.public_reference.labels(o),'justification_first')['response_schema']
            for action_id in schema['properties']['action_id']['enum']:
                for guarded in (False,True):
                    state=copy.deepcopy(c['initial']);a=v.cases.f.controller.decode(c['fixture'],{'action_id':action_id,'reason':'x'*512})
                    x=v.step(c,state,a,o,guarded)
                    o2=v.observation(c,state,2,[{'proposal':a,'action':x['action'],'result':x['result']}])
                    d=i.public_reference.labels(o2)
                    # Longest permitted enum spellings plus false booleans bound diagnosis encoding.
                    ds=i.controller.diagnosis_request(o2)['response_schema']
                    d={k:False if z['type']=='boolean' else max(z['enum'],key=len) for k,z in ds['properties'].items()}
                    for phase in ('diagnosis','action'):
                        q,b=i.request(c,o2,phase,d);self.assertLessEqual(len(json.dumps(b).encode()),8000)
        with self.assertRaises(AssertionError):i.request(c,dict(o,padding='x'*8000),'diagnosis')

    def test_packet_cost_and_disabled_native(self):
        p=json.loads((i.BASE/'packet.json').read_text())
        self.assertEqual(p['max_calls'],192);self.assertFalse(p['native_dispatch_enabled'])
        self.assertAlmostEqual(((8000+512)*5+512*25)/1000000,.055360)
        self.assertAlmostEqual(p['max_calls']*p['max_request_usd'],p['model_max_usd'])
        self.assertGreater(p['required_model_cap_usd'],p['current_model_cap_usd'])
        self.assertAlmostEqual(p['prior_reserved_usd']+p['model_max_usd'],p['required_model_cap_usd'])

if __name__=='__main__':unittest.main()

class NativeBounds(unittest.TestCase):
    def ledger(self,path,cap=16.877155):
        import sqlite3
        with sqlite3.connect(path) as db:
            db.execute('create table budget(id integer primary key,cap real,reserved real,calls integer)')
            db.execute('insert into budget values(1,?,?,517)',(cap,6.248035))
            db.execute('create table immune_requests(request_id text primary key,run_id text,request_hash text,state text,reserved_usd real,input_tokens integer,output_tokens integer,actual_usd real,started real,ended real)')
    def test_persistent_192_cap_not_legacy_120(self):
        import native
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.ledger(p/'budget.sqlite');policy=native.Policy(p/'budget.sqlite',p/'usage.jsonl')
            for _ in range(192):policy.reserve(b'x'*8000)
            with self.assertRaisesRegex(ValueError,'persistent_budget'):policy.reserve(b'x')
            self.assertEqual(policy.calls,192)
            with self.assertRaisesRegex(ValueError,'already_dispatched'):native.Policy(p/'budget.sqlite',p/'other.jsonl')
    def test_no_new_ledger_or_reset_and_missing_funding(self):
        import native,native_run
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            with self.assertRaises(ValueError):native.Policy(p/'absent.sqlite',p/'u.jsonl')
            self.assertFalse((p/'absent.sqlite').exists())
            self.ledger(p/'budget.sqlite',6.25);policy=native.Policy(p/'budget.sqlite',p/'u.jsonl')
            with self.assertRaises(ValueError):policy.reserve(b'x'*8000)
            (p/'receipt.json').write_text(json.dumps({'stage':'verification-v1','funded':False}))
            with self.assertRaises(AssertionError):native_run.verify_admission(p/'receipt.json')

class PartialAccounting(unittest.TestCase):
    def test_partial_failure_keeps_assignment_denominator_and_events(self):
        import os,native,native_run
        from unittest.mock import patch
        class Failing:
            calls=0;actual_usd=0
            def __init__(self,*a):pass
            def complete(self,q):
                self.calls+=1
                if self.calls==3:raise ValueError('scripted_transport_failure')
                if self.calls==1:return i.public_reference.labels(q['observation'])
                a=i.public_reference.choose(q['observation']);return {'reason':a['reason'],'action_id':a['action_id']}
        with tempfile.TemporaryDirectory() as d,patch.object(native_run,'verify_admission',return_value={'offline_test':True}),patch.object(native,'Policy',Failing),patch.dict(os.environ,{'SWARM_BUDGET_LEDGER':'test-only-unused'}):
            out=Path(d)/'out'
            with self.assertRaises(ValueError):native_run.execute(out,'test-only')
            s=json.loads((out/'summary.json').read_text());self.assertEqual((s['assigned'],s['started'],s['completed'],s['incomplete'],s['unstarted']),(48,1,0,1,47))
            events=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()]
            self.assertTrue(any(e.get('kind')=='frame' for e in events));self.assertEqual(s['api_calls'],3)
