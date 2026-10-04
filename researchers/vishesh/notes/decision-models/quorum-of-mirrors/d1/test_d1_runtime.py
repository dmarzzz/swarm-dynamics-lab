from contextlib import closing
import json
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import runtime
from contract import QUAL, MAIN, make_manifest, digest, RESERVE
from test_contract import response, receipts
from test_next_stage import original_ledger
import next_stage


def history(path):
    old=original_ledger(path)
    with closing(old.connect()) as db,db:
        db.execute('CREATE TABLE next_attempts (attempt TEXT PRIMARY KEY,manifest TEXT,source TEXT,status TEXT)')
        db.execute('CREATE TABLE bounded_settlements (id TEXT PRIMARY KEY,upper_bound REAL,evidence_sha256 TEXT)')
        db.execute('INSERT INTO calls VALUES (?,?,?,NULL)',('QM-Q1-01-006',RESERVE,'failed_or_uncertain'))
        db.execute('INSERT INTO bounded_settlements VALUES (?,?,?)',('QM-Q1-01-006',RESERVE,'245fffab4ddf7e9617965fab64f1d0db9247a3ba382b86b66d59737b6a79d1ca'))
        db.execute('INSERT INTO next_attempts VALUES (?,?,?,?)',('QM-Q1-02','historical','historical','complete'))
        for row in next_stage.make_manifest('QM-Q1-02')['assignments']:
            db.execute('INSERT INTO calls VALUES (?,?,?,?)',(row['id'],RESERVE,'complete',.00001))
    return runtime.Ledger(path)


class RuntimeTests(unittest.TestCase):
    def test_pending_refuses_before_provider_or_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            pending=Path(tmp)/'pending.json';pending.write_text(json.dumps({'owner_approved':False}))
            with patch('runtime.metadata_check') as provider,patch('runtime.parent.native_call') as native:
                with self.assertRaisesRegex(ValueError,'owner_update_pending'):
                    runtime.run({'update_approval':str(pending)},make_manifest(QUAL),Path(tmp)/'out',Path(tmp)/'nonexistent-credential')
                provider.assert_not_called();native.assert_not_called()
                self.assertFalse((Path(tmp)/'out').exists())
    def test_approval_bound_to_source_plan_and_named_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'approval.json'
            # Fixture only, never exported as operational approval.
            record={'owner_approved':True,'decision_ref':'UNIT TEST ONLY','attempts':[QUAL,MAIN],
                'source_sha256':runtime.hashes(),'plan_sha256':runtime.hashes()['PLAN.md'],
                'manifests_sha256':{a:digest(make_manifest(a)) for a in (QUAL,MAIN)},
                'max_new_calls':168,'api_cap_usd':1,'infrastructure_cap_usd':1,'max_infrastructure_hours':6}
            path.write_text(json.dumps(record));runtime.approval_check({'update_approval':str(path)})
            for key,value in [('max_new_calls',169),('plan_sha256','changed'),('attempts',[MAIN]),('source_sha256',{})]:
                path.write_text(json.dumps(record|{key:value}))
                with self.assertRaises(ValueError):runtime.approval_check({'update_approval':str(path)})
    def test_original_budget_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'ledger'
            with self.assertRaises(ValueError):runtime.Ledger(path)
            original_ledger(path)
            with self.assertRaises(ValueError):runtime.Ledger(path)
    def test_reservations_survive_and_attempt_cannot_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger=history(Path(tmp)/'ledger');manifest=make_manifest(QUAL)
            self.assertEqual(ledger.audit()['calls'],49)
            ledger.begin_attempt(manifest,runtime.hashes());row=manifest['assignments'][0]
            ledger.reserve(manifest,row['id'],runtime.hashes())
            with self.assertRaises(sqlite3.IntegrityError):ledger.reserve(manifest,row['id'],runtime.hashes())
            ledger.finish(row['id'],'complete',.00001);ledger.close(QUAL,False)
            self.assertEqual(ledger.audit()['calls'],50);self.assertAlmostEqual(ledger.audit()['reserved_usd'],.0672)
            with self.assertRaises(sqlite3.IntegrityError):ledger.begin_attempt(manifest,runtime.hashes())
            with self.assertRaises(ValueError):ledger.begin_attempt(make_manifest(MAIN),runtime.hashes())
    def test_unsettled_new_failure_blocks_new_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger=history(Path(tmp)/'ledger');manifest=make_manifest(QUAL);ledger.begin_attempt(manifest,runtime.hashes())
            row=manifest['assignments'][0];ledger.reserve(manifest,row['id'],runtime.hashes())
            ledger.finish(row['id'],'failed_or_uncertain');ledger.close(QUAL,False)
            with self.assertRaisesRegex(ValueError,'unreconciled_prior_call'):ledger.begin_attempt(make_manifest(MAIN),runtime.hashes())
    def test_main_recomputes_clean_gate_from_saved_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);ledger=history(path/'ledger');manifest=make_manifest(QUAL)
            (path/'manifest.json').write_text(json.dumps(manifest))
            (path/'preflight.json').write_text(json.dumps({'source_sha256':runtime.hashes(),'session_started_at':1,'deadline':2701}))
            (path/'receipts.jsonl').write_text('\n'.join(json.dumps(r) for r in receipts(manifest,lambda r:'DEFER')))
            with self.assertRaisesRegex(ValueError,'clean_qualification_failed'):
                runtime.qualification_check({'qualification_results':str(path),'session_started_at':1,'deadline':2701},ledger)
            with self.assertRaisesRegex(ValueError,'session_deadline_reset'):
                runtime.qualification_check({'qualification_results':str(path),'session_started_at':2,'deadline':2702},ledger)
    def test_failed_answer_preserves_accounting_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);ledger=history(path/'ledger');credential=path/'credential';credential.write_text('UNIT FIXTURE');credential.chmod(0o600)
            reporter=SimpleNamespace(progress=lambda *a,**k:None,artifact=lambda *a,**k:None,done=lambda **k:None,fail=lambda **k:None)
            def reject(request,credential,on_accounting):
                accounting={'usage':response('ONE')['usage'],'provider_request_id':'gen-dec-test'}
                on_accounting(accounting);raise runtime.parent.ResponseRejected('choice_invalid',accounting)
            with patch('runtime.preflight',return_value={}),patch('runtime.parent.native_call',side_effect=reject) as native,patch.dict('sys.modules',{'swarm_report':SimpleNamespace(start=lambda *a,**k:reporter)}):
                result=runtime.run({'ledger':str(path/'ledger'),'run_tldr':'UNIT FIXTURE'},make_manifest(QUAL),path/'out',credential)
            self.assertEqual(native.call_count,1);self.assertEqual((result['failed'],result['unstarted']),(1,7))
            self.assertEqual(ledger.audit()['uncertain'],0)
            self.assertEqual(json.loads((path/'out/accounting.jsonl').read_text())['usage']['output_tokens'],39)

if __name__=='__main__':unittest.main()

class LiveAdmissionTests(unittest.TestCase):
    def test_expired_claim_changed_source_and_deadline_refuse(self):
        import socket
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);manifest=make_manifest(QUAL)
            allocation={'experiment':'quorum-of-mirrors','host':socket.gethostname().split('.')[0],'claim_id':'UNIT FIXTURE',
                'exclusive':True,'approved_account_verified':True,'merged_claim_verified':True,'workload_verified_clear':True,
                'source_sha256':runtime.hashes(),'checked_at':1000,'expires_at':3000}
            allocation_path=path/'allocation.json';allocation_path.write_text(json.dumps(allocation))
            config={'source_sha256':runtime.hashes(),'manifest_sha256':digest(manifest),'session_started_at':1000,'deadline':3700,'allocation_receipt':str(allocation_path)}
            for change,now in (({},3001),({'source_sha256':{}},1100),({'deadline':3701},1100)):
                with patch('runtime.approval_check'),patch('runtime.metadata_check') as provider:
                    with self.assertRaises(ValueError):runtime.preflight(config|change,manifest,now)
                    provider.assert_not_called()

class FullScriptedSession(unittest.TestCase):
    def test_two_stage_session_preserves_217_call_cumulative_envelope(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);ledger=history(path/'ledger');credential=path/'credential';credential.write_text('UNIT FIXTURE');credential.chmod(0o600)
            reporter=SimpleNamespace(progress=lambda *a,**k:None,artifact=lambda *a,**k:None,done=lambda **k:None,fail=lambda **k:None)
            def oracle(request,credential,on_accounting):
                roots={r['visible_root']:r['value'] for r in request['state']['reports']}
                result=response('ONE' if sum(roots.values())>=2 else 'ZERO')
                on_accounting({'usage':result['usage'],'provider_request_id':'gen-dec-scripted'})
                return result
            config={'ledger':str(path/'ledger'),'run_tldr':'UNIT FIXTURE','session_started_at':1,'deadline':2701,'qualification_results':str(path/QUAL)}
            admission={'source_sha256':runtime.hashes(),'session_started_at':1,'deadline':2701}
            with patch('runtime.preflight',return_value=admission),patch('runtime.render',return_value=[]),patch('runtime.parent.native_call',side_effect=oracle) as native,patch.dict('sys.modules',{'swarm_report':SimpleNamespace(start=lambda *a,**k:reporter)}):
                first=runtime.run(config,make_manifest(QUAL),path/QUAL,credential)
                self.assertTrue(first['qualified']);runtime.qualification_check(config,ledger)
                second=runtime.run(config,make_manifest(MAIN),path/MAIN,credential)
                self.assertEqual(second['valid'],160);self.assertEqual(native.call_count,168)
            self.assertEqual(ledger.audit()['calls'],217);self.assertAlmostEqual(ledger.audit()['reserved_usd'],.291648)
