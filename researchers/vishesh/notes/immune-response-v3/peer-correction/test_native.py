import copy
from contextlib import closing
import datetime
import json
import sqlite3
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import peer_native as n
import peer_admission as a
import peer_run


def ledger(path,cap=28.368215):
    with closing(sqlite3.connect(path)) as db,db:
        db.execute('create table budget(id integer primary key,cap real,reserved real,calls integer)')
        db.execute('insert into budget values(1,?,15.524695,709)',(cap,))
        db.execute('create table immune_requests(request_id text primary key,run_id text,request_hash text,state text,reserved_usd real,input_tokens integer,output_tokens integer,actual_usd real,started real,ended real)')


class LedgerTests(unittest.TestCase):
    def test_persistent_stage_campaign_limits_keep_history(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);db=root/'original.sqlite';ledger(db)
            q=n.Policy(db,root/'q.jsonl','peer-correction-q1','frozen',time.time()+600)
            for _ in range(48):q.reserve(b'x'*8000)
            with self.assertRaisesRegex(ValueError,'persistent_budget'):q.reserve(b'x')
            with self.assertRaisesRegex(ValueError,'already_dispatched'):n.Policy(db,root/'other','peer-correction-q1','frozen',time.time()+600)
            p=n.Policy(db,root/'p.jsonl','peer-correction-p1','frozen',time.time()+600)
            for _ in range(184):p.reserve(b'x'*8000)
            with self.assertRaisesRegex(ValueError,'persistent_budget'):p.reserve(b'x')
            with closing(sqlite3.connect(db)) as connection:
                used,calls=connection.execute('select reserved,calls from budget').fetchone()
                self.assertAlmostEqual(28.368215,used)
                self.assertEqual(941,calls)
                self.assertEqual(232,connection.execute("select count(*) from immune_requests where state='reserved_unresolved'").fetchone()[0])

    def test_no_missing_ledger_reset_duplicate_zero_call_claim_or_paid_dispatch(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);db=root/'original.sqlite'
            with self.assertRaisesRegex(ValueError,'original_ledger'):n.Policy(db,root/'u','peer-correction-q1','x',time.time()+100)
            self.assertFalse(db.exists());ledger(db,15.53)
            q=n.Policy(db,root/'u','peer-correction-q1','x',time.time()+100)
            with self.assertRaisesRegex(ValueError,'already_claimed'):n.Policy(db,root/'u2','peer-correction-q1','x',time.time()+100)
            with self.assertRaisesRegex(ValueError,'wire_limit'):q.reserve(b'x'*8001)
            with self.assertRaisesRegex(ValueError,'persistent_budget'):q.reserve(b'x'*8000)
            with patch('urllib.request.urlopen',side_effect=AssertionError('network must not execute')):
                with self.assertRaisesRegex(ValueError,'dispatch_disabled'):q.complete({})
                with self.assertRaisesRegex(ValueError,'dispatch_disabled'):peer_run.execute(root/'out','missing',db)
            self.assertFalse((root/'out').exists())
            with closing(sqlite3.connect(db)) as connection:self.assertEqual((15.524695,709),connection.execute('select reserved,calls from budget').fetchone())

    def test_deadline_checked_each_request(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);db=root/'l';ledger(db)
            deadline=time.time()+100
            q=n.Policy(db,root/'u','peer-correction-q1','x',deadline)
            with patch('peer_native.time.time',return_value=deadline):
                with self.assertRaisesRegex(ValueError,'deadline'):q.reserve(b'x')


class AdmissionTests(unittest.TestCase):
    def receipt(self):
        now=datetime.datetime(2026,10,4,23,0,tzinfo=datetime.timezone.utc)
        r={'stage':'peer-correction-q1','funded':True,'decision_reference':'offline-unit-test-only',
           'stage_max_calls':48,'stage_model_max_usd':2.657280,'campaign_max_calls':232,'campaign_model_max_usd':12.843520,
           'model':'anthropic/claude-opus-4.6','input_rate':5,'output_rate':25,
           'rates_verified':True,'runtime_tests_passed':True,'runtime_source_verified':True,
           'infrastructure_centrally_reconciled':True,'infrastructure_reserved_usd':.15,
           'verified_at':now.isoformat(),'contract_sha256':'offline',
           'allocation':{'host':'offline','exclusive':True,'approved_account_verified':True,'claim_reference':'offline',
                         'status':'active','started':now.isoformat(),'expires':(now+datetime.timedelta(minutes=60)).isoformat()}}
        return r,now
    def test_missing_funding_account_runtime_or_stale_evidence_blocks(self):
        r,now=self.receipt();p={'contract_sha256':'offline'}
        self.assertTrue(a.validate_contract(r,p,now,'offline'))
        for key,value in [('funded',False),('stage_max_calls',49),('runtime_tests_passed',False),('input_rate',4),('contract_sha256','changed')]:
            bad=copy.deepcopy(r);bad[key]=value
            with self.assertRaises(ValueError):a.validate_contract(bad,p,now,'offline')
        for key,value in [('exclusive',False),('approved_account_verified',False),('host','another'),('status','released')]:
            bad=copy.deepcopy(r);bad['allocation'][key]=value
            with self.assertRaises(ValueError):a.validate_contract(bad,p,now,'offline')
        with self.assertRaisesRegex(ValueError,'stale'):a.validate_contract(r,p,now+datetime.timedelta(seconds=301),'offline')
    def test_exact_horizon_and_main_requires_bound_native_qualification(self):
        r,now=self.receipt();p={'contract_sha256':'offline'}
        for minutes,okay in ((19,False),(20,True),(60,True),(61,False)):
            bad=copy.deepcopy(r);bad['allocation']['expires']=(now+datetime.timedelta(minutes=minutes)).isoformat()
            if okay:self.assertTrue(a.validate_contract(bad,p,now,'offline'))
            else:
                with self.assertRaises(ValueError):a.validate_contract(bad,p,now,'offline')
        r.update(stage='peer-correction-p1',stage_max_calls=184,stage_model_max_usd=10.186240,
                 qualification={'contract_sha256':'offline','completed_worlds':4,'api_calls':48,'native':True,'all_automated_pass':True,'manual_reason_review_pass':True,'usage_reconciled':True})
        self.assertTrue(a.validate_contract(r,p,now,'offline'))
        r['qualification']['native']=False
        with self.assertRaisesRegex(ValueError,'qualification'):a.validate_contract(r,p,now,'offline')

class CloseoutHook(unittest.TestCase):
    def test_only_saved_data_with_worker_attestation(self):
        import peer_closeout
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'scripts').mkdir();(root/'scripts/experiment.py').write_text('# offline fixture')
            saved=root/'data/saved';saved.mkdir(parents=True);(saved/'summary.json').write_text('{}')
            args=peer_closeout.command(root,saved,'peer-correction-q1','failed',True)
            self.assertIn('finalize',args);self.assertIn('--worker-stopped',args)
            with self.assertRaises(ValueError):peer_closeout.command(root,saved,'peer-correction-q1','failed',False)
            with self.assertRaises(ValueError):peer_closeout.command(root,root/'elsewhere','peer-correction-q1','failed',True)

class QualificationEvidenceBinding(unittest.TestCase):
    def fixture(self):
        import hashlib
        trace=json.dumps([{'case':c['id'],'automated_pass':True,'trace':[{}]*6} for c in a.iroots()]).encode()
        science={'contract_sha256':'contract','completed_worlds':4,'api_calls':48,'native':True,'all_automated_pass':True,'manual_reason_review_pass':True,'usage_reconciled':True,'trace_sha256':hashlib.sha256(trace).hexdigest()}
        r={'qualification':science,'packet_sha256':'packet','commit':'source','model':'anthropic/claude-opus-4.6'}
        q={'stage':'peer-correction-q1','funded':True,'packet_sha256':'packet','contract_sha256':'contract','commit':'source','model':r['model']}
        return r,{'contract_sha256':'contract'},science,q,trace
    def test_unrelated_or_stale_hashed_evidence_cannot_unlock_comparison(self):
        r,p,science,q,trace=self.fixture()
        self.assertTrue(a.verify_qualification_binding(r,p,science,q,'packet',trace))
        unrelated=dict(science,contract_sha256='old-contract')
        with self.assertRaisesRegex(ValueError,'scientific_receipt'):a.verify_qualification_binding(r,p,unrelated,q,'packet',trace)
        for key,value in (('packet_sha256','other-packet'),('commit','other-source'),('stage','other-stage')):
            bad=dict(q);bad[key]=value
            with self.assertRaisesRegex(ValueError,'origin'):a.verify_qualification_binding(r,p,science,bad,'packet',trace)
        with self.assertRaisesRegex(ValueError,'origin'):a.verify_qualification_binding(r,p,science,q,'unrelated-ledger-claim',trace)
        with self.assertRaisesRegex(ValueError,'trace_binding'):a.verify_qualification_binding(r,p,science,q,'packet',b'[]')
    def test_saved_failed_outcome_cannot_be_relabelled_passing(self):
        import hashlib
        r,p,science,q,trace=self.fixture()
        episodes=json.loads(trace);episodes[0]['automated_pass']=False;bad=json.dumps(episodes).encode()
        science['trace_sha256']=hashlib.sha256(bad).hexdigest()
        with self.assertRaisesRegex(ValueError,'outcomes_failed'):a.verify_qualification_binding(r,p,science,q,'packet',bad)

if __name__=='__main__':unittest.main()
