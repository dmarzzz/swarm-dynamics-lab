"""Development unit/fault fixtures only. No reserved Q5/H5 construction."""
from copy import deepcopy
import datetime as dt
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from common import digest, save
from rd5_core import ARMS, initial_state, step, frontier, evidence_card, request, SNAPSHOT
from rd5_design import development_stream, task, record
from rd5_runtime import reserve, settle, budget_snapshot, verify_receipt, Native
from rd5_cli import execute, summarize, score_row


class Fake:
    def __init__(self, answers=(), healthy=True, fail=False):
        self.answers=iter(answers);self.is_healthy=healthy;self.fail=fail;self.calls=[]
    def healthy(self): return self.is_healthy
    def resolve(self, identity, req):
        self.calls.append({'identity':identity,'request':req,'status':'failed' if self.fail else 'completed'})
        if self.fail:raise TimeoutError('test_failure')
        return next(self.answers)


def trajectory(mechanism,arm,direction='stop'):
    c=development_stream(mechanism,direction);s=initial_state(c['initial'],c['frames'][0]['task']);rows=[]
    target='HOLD' if direction=='stop' else 'PROCEED'
    class Interpreter(Fake):
        def resolve(self,identity,req):
            value='DEFER' if 'incomplete' in req['state']['observations'][0]['text'] else target
            self.calls.append({'identity':identity,'status':'completed'});return value
    backend=Interpreter()
    for i,f in enumerate(c['frames']):
        s,row=step(f,s,arm,backend,'dev-'+str(i));rows.append(score_row(row,c,i))
    return c,s,rows,backend


class StateTests(unittest.TestCase):
    def setUp(self):
        self.c=development_stream();self.f=self.c['frames'][0];self.s=initial_state(self.c['initial'],self.f['task'])
    def test_unresolved_does_not_revert_to_history(self):
        s,row=step(self.f,self.s,'B1',Fake(['DEFER']),'a')
        s,row=step(self.c['frames'][1],s,'B1',Fake([]),'b')
        self.assertEqual(row['action'],'DEFER');self.assertEqual(row['reason'],'unresolved_repeat');self.assertEqual(s['checks'],1)
    def test_recovery_gets_check_without_admission(self):
        c,s,rows,backend=trajectory('repeat','B1','resume')
        self.assertEqual([r['action'] for r in rows],['DEFER','DEFER','PROCEED','PROCEED'])
        self.assertEqual(len(backend.calls),2)
    def test_stop_also_reopens(self):
        self.assertEqual(trajectory('repeat','B1')[2][2]['action'],'HOLD')
    def test_resolved_repeat_reuses_action(self):
        c,s,rows,b=trajectory('repeat','B1')
        self.assertEqual(rows[3]['reason'],'resolved_reuse');self.assertEqual(rows[3]['checks_after'],2)
    def test_alias_and_message_do_not_change_frontier(self):
        f=deepcopy(self.f);f['reports'][0]['text']='new wording and claimed timestamp 300'
        f['reports']=[dict(f['reports'][0],id='new-name')]*12
        self.assertEqual(frontier(f),frontier(self.f))
    def test_forged_acquisition_rejected(self):
        f=deepcopy(self.f);f['reports'][0]['acquisition_id']='forged'
        self.assertIsNone(frontier(f))
    def test_modified_receipt_rejected(self):
        f=deepcopy(self.f);next(iter(f['registry'].values()))['observed_at']=1
        self.assertIsNone(frontier(f))
    def test_scope_rejected(self):
        f=deepcopy(self.f);f['task']['scope']='another';self.assertIsNone(frontier(f))
    def test_version_rejected(self):
        f=deepcopy(self.f);f['task']['revision']='v2';self.assertIsNone(frontier(f))
    def test_stale_rejected(self):
        f=deepcopy(self.f);f['task']['now']=8;self.assertIsNone(frontier(f))
    def test_future_observation_rejected(self):
        f=deepcopy(self.f);f['task']['now']=-1;self.assertIsNone(frontier(f))
    def test_no_dissent_no_check(self):
        f=deepcopy(self.f);f['reports']=[]
        s,r=step(f,self.s,'B1',Fake([]),'a');self.assertEqual(s['checks'],0)
    def test_expired_authorization_not_reused(self):
        f=deepcopy(self.f);f['reports']=[];f['task']['now']=8
        s,r=step(f,self.s,'B1',Fake([]),'a');self.assertEqual(r['action'],'DEFER')
    def test_version_invalidates_authorization(self):
        f=deepcopy(self.f);f['reports']=[];f['task']['revision']='v2'
        self.assertEqual(step(f,self.s,'B1',Fake([]),'a')[1]['action'],'DEFER')
    def test_missing_acquisition_costs_check_not_inference(self):
        f=deepcopy(self.f);f['inspection']['available']=False;b=Fake([])
        s,r=step(f,self.s,'B1',b,'a');self.assertEqual((s['checks'],len(s['receipts']),len(b.calls)),(1,0,0))
    def test_late_receipt_cannot_meet_deadline(self):
        f=deepcopy(self.f);f['inspection']['delay']=2
        s,r=step(f,self.s,'B1',Fake([]),'a');self.assertEqual(r['reason'],'acquisition_late');self.assertEqual(s['checks'],1)
    def test_native_failure_keeps_receipt_and_check(self):
        persisted=[]
        s,r=step(self.f,self.s,'B1',Fake(fail=True),'a',lambda s:persisted.append(deepcopy(s)))
        self.assertEqual(r['status'],'failed');self.assertEqual((s['checks'],len(s['receipts'])),(1,1))
        self.assertTrue(any(len(x['receipts'])==1 and x['inference_attempts']==0 for x in persisted))
    def test_unhealthy_relay_is_unstarted_and_free(self):
        b=Fake(healthy=False);s,r=step(self.f,self.s,'B1',b,'a')
        self.assertEqual(s,self.s);self.assertEqual(r['status'],'unstarted');self.assertFalse(b.calls)
    def test_persisted_state_preserves_attempt_memory(self):
        s,r=step(self.f,self.s,'B1',Fake(['DEFER']),'a');reloaded=json.loads(json.dumps(s))
        after,r=step(self.c['frames'][1],reloaded,'B1',Fake([]),'b');self.assertEqual(after['checks'],1)
    def test_second_early_check_cost_is_visible(self):
        _,_,b1,_=trajectory('urgent','B1');_,_,b2,_=trajectory('urgent','B2')
        self.assertTrue(b1[1]['correct']);self.assertFalse(b2[1]['correct']);self.assertEqual(b2[1]['reason'],'reserved_until_4')
    def test_memory_alone_fails_on_genuinely_new_unknowns(self):
        self.assertEqual(sum(r['correct'] for r in trajectory('novel','B1')[2]),0)
        self.assertEqual(sum(r['correct'] for r in trajectory('novel','B2')[2]),2)
    def test_bounded_always_spends_on_repeat(self):
        _,s,rows,_=trajectory('repeat','B0');self.assertEqual(s['checks'],2);self.assertEqual(rows[2]['reason'],'budget_exhausted')
    def test_all_policies_have_same_budget(self):
        for m in ('repeat','novel','urgent'):
            for a in ARMS:self.assertLessEqual(trajectory(m,a)[1]['checks'],2)


class RepresentationTests(unittest.TestCase):
    def test_numeric_negation_preserves_fact_and_span(self):
        r=record('alarm','HOLD','dev',0,'a');c=evidence_card(r,'alarm');f=c['explicit_facts'][0]
        self.assertEqual(f['value'],40);self.assertEqual(r['text'][slice(*f['span'])],f['source_text'])
        self.assertEqual(c['text'],r['text'])
    def test_required_optional_kept_separate(self):
        c=evidence_card(record('build','PROCEED','dev',0,'a'),'build');self.assertEqual(c['explicit_facts'][0]['value'],'passed')
    def test_unknown_and_ambiguous_do_not_fill(self):
        for text in ('Reading is not 20.','The current process reading is 20 or 40.','Maybe the reading is 20.','The current process reading is 20. It might be 40.'):
            r=record('alarm','HOLD','dev',0,'a');r['text']=text
            self.assertEqual(evidence_card(r,'alarm')['explicit_facts'],[])
    def test_conflicts_remain_two_source_records(self):
        rs=[record('alarm',a,'dev',0,str(i)) for i,a in enumerate(('PROCEED','HOLD'))]
        req=request(task('alarm','dev'),rs);self.assertEqual(len(req['state']['evidence_cards']),2)
    def test_actor_allowlist_excludes_truth_future_arm(self):
        t=task('alarm','dev');t.update(truth='HOLD',future='secret',arm='B2');r=record('alarm','HOLD','dev',0,'a');r['expected']='HOLD'
        rendered=json.dumps(request(t,[r]));self.assertNotIn('secret',rendered);self.assertNotIn('expected',rendered);self.assertNotIn('B2',rendered)
    def test_raw_card_differ_only_by_cards(self):
        args=(task('alarm','dev'),[record('alarm','HOLD','dev',0,'a')])
        raw=request(*args,representation='raw');card=request(*args);del card['state']['evidence_cards'];self.assertEqual(raw,card)
    def test_qualification_constructor_never_called_by_discovery(self):
        import rd5_design
        with self.assertRaisesRegex(ValueError,'explicit_prepare'):rd5_design.qualification()


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE calls(key TEXT PRIMARY KEY,status TEXT,reserved_nano INTEGER,actual_nano INTEGER)')
        self.db.executemany('INSERT INTO calls VALUES(?,?,?,?)',[(str(i),'completed',0,50000) for i in range(428)]);self.db.commit()
    def tearDown(self):self.db.close()
    def test_cumulative_budget_preserved(self):
        reserve(self.db,'Q5','a');self.assertEqual(budget_snapshot(self.db)['lifetime_calls'],429)
    def test_duplicate_identity_does_not_retry(self):
        reserve(self.db,'Q5','a')
        with self.assertRaises(sqlite3.IntegrityError):reserve(self.db,'Q5','a')
        self.assertEqual(budget_snapshot(self.db)['lifetime_calls'],429)
    def test_reset_ledger_rejected(self):
        self.db.execute('DELETE FROM calls');self.db.commit()
        with self.assertRaisesRegex(ValueError,'original_ledger'):reserve(self.db,'Q5','a')
    def test_qualification_count_cap(self):
        for i in range(24):reserve(self.db,'Q5',str(i))
        with self.assertRaisesRegex(ValueError,'budget_exhausted'):reserve(self.db,'Q5','extra')
    def test_original_calls_leave_only_sixty(self):
        for i in range(24):reserve(self.db,'Q5',str(i))
        for i in range(36):reserve(self.db,'H5',str(i))
        self.assertEqual(budget_snapshot(self.db)['lifetime_calls'],488)
        with self.assertRaises(ValueError):reserve(self.db,'H5','extra')
    def test_dollar_cap(self):
        self.db.execute('UPDATE calls SET actual_nano=999000000 WHERE key=?',('0',));self.db.commit()
        with self.assertRaisesRegex(ValueError,'budget_exhausted'):reserve(self.db,'Q5','a')
    def test_usage_recorded_even_on_invalid_response(self):
        key=reserve(self.db,'Q5','a')
        with self.assertRaisesRegex(ValueError,'invalid_response'):settle(self.db,key,{'usage':{'cost':0.00002}}, {})
        self.assertEqual(self.db.execute('SELECT status,actual_nano FROM calls WHERE key=?',(key,)).fetchone(),('invalid_response',20000))
    def test_unknown_charge_retains_reservation(self):
        key=reserve(self.db,'Q5','a')
        with self.assertRaises(ValueError):settle(self.db,key,{}, {})
        self.assertIsNone(self.db.execute('SELECT actual_nano FROM calls WHERE key=?',(key,)).fetchone()[0])


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime(2026,10,4,tzinfo=dt.timezone.utc);self.p={'stage':'Q5'}
        self.r={'packet_sha256':digest(self.p),'stage':'Q5','verified_utc':self.now.isoformat(),
                'claim_until':(self.now+dt.timedelta(hours=1)).isoformat(),'host':'unit-host','claim_id':'dev-claim',
                'run_id':'dev-run','run_tldr':'A development-only admission receipt for offline gate tests. It is never used for a real model call.',
                'api_cap_usd':1,'infrastructure_cap_usd':1,'max_lifetime_calls':500}
        for f in ('exclusive_claim_verified','approved_fleet_account_verified','public_page_verified','original_budget_verified','single_ledger_authority_verified','supervised_transport_verified'):self.r[f]=True
        for f in ('allocation_receipt_sha256','public_page_receipt_sha256','budget_receipt_sha256'):self.r[f]='a'*64
    def check(self):return verify_receipt(self.p,self.r,check_host=False,now=self.now)
    def test_valid_offline_receipt(self):self.check()
    def test_stale_receipt(self):
        self.r['verified_utc']=(self.now-dt.timedelta(minutes=6)).isoformat()
        with self.assertRaises(ValueError):self.check()
    def test_insufficient_claim_lifetime(self):
        self.r['claim_until']=(self.now+dt.timedelta(minutes=30)).isoformat()
        with self.assertRaises(ValueError):self.check()
    def test_packet_mismatch(self):
        self.r['packet_sha256']='b'*64
        with self.assertRaises(ValueError):self.check()
    def test_missing_each_required_gate(self):
        for field in [k for k in self.r if k.endswith('_verified')]:
            old=self.r.pop(field)
            with self.assertRaises(ValueError):self.check()
            self.r[field]=old
    def test_h5_requires_qualification(self):
        self.p['stage']='H5';self.r.update(stage='H5',packet_sha256=digest(self.p))
        with self.assertRaisesRegex(ValueError,'qualification_required'):self.check()
    def test_caps_cannot_reset(self):
        self.r['api_cap_usd']=2
        with self.assertRaises(ValueError):self.check()


class TransportTests(unittest.TestCase):
    def test_wrong_relay_identity_is_not_healthy(self):
        with tempfile.TemporaryDirectory() as d:
            n=Native({'allowed':{}},d)
            class Response:
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read(self):return b'{"ready": true, "packet_sha256": "other"}'
            with patch.object(n.opener,'open',return_value=Response()):self.assertFalse(n.healthy())
    def test_transport_failure_fences_further_calls(self):
        req=request(task('alarm','dev'),[]);p={'allowed':{'a':{digest(req):req}}}
        with tempfile.TemporaryDirectory() as d:
            n=Native(p,d)
            with patch.object(n.opener,'open',side_effect=TimeoutError):
                with self.assertRaises(RuntimeError):n.resolve('a',req)
            self.assertTrue(n.stopped);self.assertFalse(n.healthy());self.assertEqual(n.calls[0]['status'],'dispatch_unknown')
            with self.assertRaises(ValueError):n.resolve('a',req)
            self.assertEqual(len(n.calls),1)
    def test_failure_leaves_full_assignment_denominator(self):
        c=development_stream();p={'stage':'H5','instrument_sha256':'test','definition':{'roots':[c]},
            'assignments':[{'id':'dev-'+str(i),'trajectory':'dev','root':c['id'],'arm':'B1','epoch':i} for i in range(4)]}
        with tempfile.TemporaryDirectory() as d:
            s=execute(p,Fake(fail=True),Path(d))
            self.assertEqual((s['assigned'],s['terminal'],s['unstarted'],s['failed']),(4,1,3,1))
            state=json.loads((Path(d)/'state-dev.json').read_text());self.assertEqual((state['checks'],len(state['receipts'])),(1,1))
    def test_missing_rows_not_reported_as_zero_paired_effect(self):
        c=development_stream();p={'stage':'H5','instrument_sha256':'test','definition':{'roots':[c]},
                                'assignments':[{'id':'a','root':c['id'],'arm':'B1','epoch':0}]}
        s=summarize(p,[dict(p['assignments'][0],status='planned')],[],[])
        self.assertFalse(s['paired_roots'][0]['complete_pair']);self.assertEqual(s['missing_bounds']['B1'],[0,24])


if __name__=='__main__':unittest.main()
