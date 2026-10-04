import json,sqlite3,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from contextlib import closing
from test_next_stage import response, original_ledger
from next_stage import checked_response,make_manifest
from next_runtime import safe_accounting,native_call,ResponseRejected,run,hashes

HERE=Path(__file__).parent
class Q1Repair(unittest.TestCase):
    def test_documented_positive_output_is_valid(self):
        r=response('ONE');r['usage']['output_tokens']=70
        self.assertEqual(checked_response(r)['usage']['output_tokens'],70)
        for invalid in [-1,True,1.5]:
            r['usage']['output_tokens']=invalid
            with self.assertRaises(ValueError):checked_response(r)
    def test_accounting_allowlist_rejects_invalid_usage_and_secret_fields(self):
        r=response('ONE');r.update(id='gen-dec-123-fixture',private='DO-NOT-EXPORT')
        self.assertEqual(set(safe_accounting(r)),{'usage','provider_request_id'})
        r['id']='sk-or-DO-NOT-EXPORT';self.assertNotIn('provider_request_id',safe_accounting(r))
        for field,val in [('cost',float('nan')),('cost',.5),('input_tokens',True),('output_tokens',-1)]:
            q=response('ONE');q['usage'][field]=val;self.assertIsNone(safe_accounting(q))
    def test_rejected_answer_billing_survives_and_stops(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);b=original_ledger(p/'ledger');cred=p/'credential';cred.write_text('UNIT-FIXTURE');cred.chmod(0o600)
            raw=response('ONE');raw['usage']['output_tokens']=70;raw['answers']['decision']['choice']='INVALID';raw['private']='DO-NOT-EXPORT';raw['id']='gen-dec-123-fixture'
            class Reply:
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read(self,*args):return json.dumps(raw).encode()
            reporter=SimpleNamespace(progress=lambda *a,**k:None,artifact=lambda *a,**k:None,done=lambda **k:None,fail=lambda **k:None)
            cfg={'ledger':str(p/'ledger'),'source_sha256':hashes(),'public_manifest_url':'fixture','run_tldr':'fixture'}
            with patch('next_runtime.urllib.request.urlopen',return_value=Reply()) as call,patch('next_runtime.preflight',return_value={}),patch.dict('sys.modules',{'swarm_report':SimpleNamespace(start=lambda *a,**k:reporter)}):
                result=run(cfg,make_manifest(),p/'out',cred)
            self.assertEqual(call.call_count,1);self.assertEqual(result['failed'],1);self.assertEqual(result['unstarted'],15);self.assertEqual(b.audit()['uncertain'],0)
            a=json.loads((p/'out/accounting.jsonl').read_text());self.assertEqual(a['usage']['output_tokens'],70)
            receipt=json.loads((p/'out/receipts.jsonl').read_text());self.assertEqual(receipt['reason'],'choice_invalid');self.assertEqual(receipt['accounting']['usage']['cost'],.00001)
            self.assertNotIn('DO-NOT-EXPORT',(p/'out/accounting.jsonl').read_text()+(p/'out/receipts.jsonl').read_text())
            with closing(b.connect()) as db:self.assertEqual(db.execute("SELECT status,actual FROM calls WHERE id=?",(receipt['id'],)).fetchone(),('failed_accounted',.00001))
    def test_conservative_parent_settlement_keeps_failure_and_reservation(self):
        with tempfile.TemporaryDirectory() as d:
            b=original_ledger(Path(d)/'ledger');m=make_manifest();b.begin_attempt(m,hashes());ident=m['assignments'][0]['id'];self.assertEqual(ident,'QM-Q1-01-006');b.reserve(m,ident,hashes());b.finish(ident,'failed_or_uncertain');b.close(m['attempt'],False)
            before=b.audit();prior=HERE/'results/QM-Q1-01';r=b.settle_parent_contract_failure(prior/'receipts.jsonl',prior/'preflight.json');after=b.audit()
            self.assertIsNone(r['actual_usd']);self.assertEqual(after['reserved_usd'],before['reserved_usd']);self.assertEqual(after['uncertain'],0)
            with closing(b.connect()) as db:self.assertEqual(db.execute('SELECT status,actual FROM calls WHERE id=?',(ident,)).fetchone(),('failed_or_uncertain',None))
            with self.assertRaises(sqlite3.IntegrityError):b.settle_parent_contract_failure(prior/'receipts.jsonl',prior/'preflight.json')
            b.begin_attempt(make_manifest('QM-Q1-02'),hashes())
    def test_settlement_does_not_cover_other_uncertain_calls_or_forged_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);b=original_ledger(p/'ledger');m=make_manifest();b.begin_attempt(m,hashes())
            for row in m['assignments'][:2]:b.reserve(m,row['id'],hashes());b.finish(row['id'],'failed_or_uncertain')
            b.close(m['attempt'],False);prior=HERE/'results/QM-Q1-01';wrong=p/'wrong';wrong.write_text('{}')
            with self.assertRaises(ValueError):b.settle_parent_contract_failure(wrong,prior/'preflight.json')
            b.settle_parent_contract_failure(prior/'receipts.jsonl',prior/'preflight.json');self.assertEqual(b.audit()['uncertain'],1)
            with self.assertRaises(ValueError):b.begin_attempt(make_manifest('QM-Q1-02'),hashes())
if __name__=='__main__':unittest.main()
