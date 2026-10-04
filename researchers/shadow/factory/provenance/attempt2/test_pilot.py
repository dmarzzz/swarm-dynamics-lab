"""Offline successor fault tests. Never model requests."""
import concurrent.futures
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import durable as d
import instrument as ins
import run as r


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.aa=ins.assignments('openrouter')

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.sources={'unit':'frozen'}
        for attr,value in [('RESULTS',self.base),('PAID',d.PaidLedger(self.base/'paid.jsonl')),('DEADLINE',20000000000)]:
            p=patch.object(r,attr,value);p.start();self.addCleanup(p.stop)
        for target,value in [('source_hashes',self.sources),('key_for','offline-dummy')]:
            p=patch.object(r,target,return_value=value);p.start();self.addCleanup(p.stop)
        assigned={'openrouter':self.aa}
        d.immutable(self.base/'assignments.json',assigned)
        d.immutable(self.base/'admission.json',{'study':r.SPEC_ID,'max_http_attempts':149,'source_sha256':self.sources,
            'source_revision':'offline-fixture','dependency_versions':{p:r.importlib.metadata.version(p) for p in ('tiktoken','PyYAML')},
            'assignment_file_sha256':d.sha(self.base/'assignments.json'),
            'assignment_digest':{'openrouter':ins.digest(self.aa)},'deadline':20000000000,
            'public_plan_url':'https://example.invalid/offline','registration_readback':{'id':r.SPEC_ID,'url':'https://example.invalid/offline'}})

    def response(self,a,wrong=False,model='anthropic/claude-sonnet-4.6'):
        decision=a['world']['target']
        if wrong:decision='A' if decision=='B' else 'B'
        return io.BytesIO(json.dumps({'model':model,'provider':'Anthropic','usage':{'cost':.001,'prompt_tokens':2000,'completion_tokens':30},
            'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'decision':decision,'confidence':.9})}}]}).encode())

    def test_fixed_instrument(self):
        import tiktoken
        enc=tiktoken.get_encoding('cl100k_base')
        self.assertEqual(len(self.aa),150)
        for a in self.aa:
            self.assertEqual(len(enc.encode(ins.SYSTEM))+len(enc.encode(a['prompt'])),1800)
            self.assertEqual(a['prompt'].count('MEASUREMENT:')+a['prompt'].count('IRRELEVANT:'),20)
            self.assertEqual(a['world']['target'],'A' if sum(a['world']['values'])>0 else 'B')
        self.assertEqual(len({a['id'] for a in self.aa}),150)
        self.assertEqual(self.aa[0]['world']['seed'],202610040604)
        self.assertEqual(self.aa[6]['world']['seed'],202610041114)
        for n in range(12):
            cells=[a for a in self.aa if a['stage']=='M' and a['world']['root']==n]
            self.assertEqual(len(cells),12)
            self.assertEqual(len({ins.digest(a['world']) for a in cells}),1)
            self.assertEqual(len({a['prompt'] for a in cells if a['arm']=='dedup'}),1)

    def test_historical_main_unchanged_fresh_gate_and_full_cost_envelope(self):
        historical=d.read(r.ROOT.parent/'results/assignments.json')['openrouter']
        self.assertEqual(historical[6:],self.aa[6:])
        self.assertNotEqual(historical[0]['world']['seed'],self.aa[0]['world']['seed'])
        bounds=[]
        for a in self.aa:
            size=len(ins.canonical(r.body_for('openrouter',a)))
            self.assertLessEqual(size,16000)
            bounds.append(((size+2048)*6+128*15)/1e6)
        self.assertLessEqual(sum(bounds[:149]),9)

    def test_wire_body_subset_and_fail_closed_unknown_keywords(self):
        for route in ('pool','openrouter'):
            body=r.body_for(route,self.aa[0])
            schema=body['output_config']['format']['schema'] if route=='pool' else body['response_format']['json_schema']['schema']
            self.assertTrue(ins.validate_wire_schema(schema))
        for keyword in ('minimum','maximum','exclusiveMinimum','exclusiveMaximum','multipleOf','minLength','maxLength','pattern','format','unknown'):
            schema=json.loads(json.dumps(ins.SCHEMA));schema['properties']['confidence'][keyword]=0
            with self.assertRaises(ValueError):ins.validate_wire_schema(schema)
        for value in (True,-.1,1.1,float('nan'),float('inf'),'0.9'):
            with self.assertRaises(ValueError):ins.validate_answer({'decision':'A','confidence':value})

    def test_no_registration_source_or_assignment_drift(self):
        with patch('urllib.request.build_opener') as op,patch.object(r,'key_for') as key:
            with patch.object(r,'RESULTS',self.base/'absent'):
                with self.assertRaises(FileNotFoundError):r.dispatch('openrouter',self.aa[0])
            with patch.object(r,'source_hashes',return_value={'changed':'yes'}):
                with self.assertRaises(r.AdmissionError):r.dispatch('openrouter',self.aa[0])
            with self.assertRaises(r.AdmissionError):r.dispatch('openrouter',dict(self.aa[0],prompt='changed'))
            key.assert_not_called();op.assert_not_called()

    def test_pool_disabled_and_main_needs_gate(self):
        with patch('urllib.request.build_opener') as op:
            with self.assertRaises(r.AdmissionError):r.dispatch('pool',self.aa[0])
            with self.assertRaisesRegex(r.AdmissionError,'predecessor_missing'):r.dispatch('openrouter',self.aa[6])
            op.assert_not_called()

    def test_receipts_and_reservations_before_http(self):
        a=self.aa[0]
        def fake(request,timeout):
            self.assertTrue((self.base/'openrouter/init'/f'{a["id"]}.json').exists())
            self.assertEqual(len((self.base/'calls.jsonl').read_text().splitlines()),1)
            self.assertGreater(r.PAID.liability(r.SPEC_ID),0)
            self.assertLessEqual(timeout,90)
            return self.response(a)
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=fake
            row=r.dispatch('openrouter',a)
        self.assertEqual(row['status'],'completed');self.assertAlmostEqual(r.PAID.liability(),.001)
        with self.assertRaises(r.AdmissionError):r.dispatch('openrouter',a)
        path=self.base/'openrouter/outcomes'/f'{a["id"]}.json';before=path.read_bytes()
        with self.assertRaises(FileExistsError):d.immutable(path,{'changed':True})
        self.assertEqual(path.read_bytes(),before)

    def test_http400_contract_stops_without_fallback(self):
        error=urllib.error.HTTPError('http://offline',400,'bad request',{},io.BytesIO(b'{"error":{"code":400}}'))
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=error;r.run();self.assertEqual(op.return_value.open.call_count,1)
        row=d.read(self.base/'openrouter/outcomes'/f'{self.aa[0]["id"]}.json')
        self.assertEqual(row['error_class'],'request_contract');self.assertEqual(row['provider_error_code'],400)
        self.assertTrue(row['cost_unknown']);self.assertGreater(r.PAID.liability(),0)
        self.assertEqual(d.read(self.base/'openrouter/terminal.json')['not_run'],149)
        self.assertFalse((self.base/'pool').exists())

    def test_http503_availability_still_no_retry(self):
        error=urllib.error.HTTPError('http://offline',503,'unavailable',{},None)
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=error;r.run();self.assertEqual(op.return_value.open.call_count,1)
        row=d.read(self.base/'openrouter/outcomes'/f'{self.aa[0]["id"]}.json')
        self.assertEqual(row['error_class'],'availability')

    def test_wrong_gate_answer_stops(self):
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.return_value=self.response(self.aa[0],wrong=True)
            r.run();self.assertEqual(op.return_value.open.call_count,1)
        self.assertEqual(d.read(self.base/'openrouter/terminal.json')['reason'],'clean_competence_failure')

    def test_six_clean_receipts_before_main(self):
        seq=iter(self.aa[:7])
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=lambda *args,**kwargs:self.response(next(seq))
            for a in self.aa[:7]:self.assertEqual(r.dispatch('openrouter',a)['status'],'completed')

    def test_wrong_model_retained_and_stops(self):
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.return_value=self.response(self.aa[0],model='wrong')
            row=r.dispatch('openrouter',self.aa[0])
        self.assertEqual(row['served_model'],'wrong');self.assertIn('served_model_mismatch',row['error'])

    def test_149_remaining_cap_before_network(self):
        with d.locked(self.base/'calls.jsonl') as h:
            for n in range(149):d.append_locked(h,{'call':str(n)})
        with patch('urllib.request.build_opener') as op:
            row=r.dispatch('openrouter',self.aa[0]);op.assert_not_called()
        self.assertIn('http_attempt_cap',row['error']);self.assertFalse(row['network_attempted'])

    def test_ambiguous_init_is_closed_never_retried(self):
        a=self.aa[0];d.immutable(self.base/'openrouter/init'/f'{a["id"]}.json',{'partial':'fixture'})
        with patch('urllib.request.build_opener') as op:
            terminal=r.execute_cohort('openrouter');op.assert_not_called()
        self.assertEqual(terminal['failed'],1)
        self.assertEqual(d.read(self.base/'openrouter/outcomes'/f'{a["id"]}.json')['status'],'interrupted_unknown')

    def test_full_mock_success_stops_at_remaining149_and_keeps150_denominator(self):
        seq=iter(self.aa)
        with patch('urllib.request.build_opener') as op,patch('sys.stdout',new=io.StringIO()):
            op.return_value.open.side_effect=lambda *args,**kwargs:self.response(next(seq))
            r.run();self.assertEqual(op.return_value.open.call_count,149)
        terminal=d.read(self.base/'openrouter/terminal.json')
        self.assertEqual((terminal['completed'],terminal['not_run']),(149,1))
        self.assertTrue(terminal['qualification_passed'])
        self.assertEqual(terminal['reason'],'remaining_cumulative_http_cap')
        self.assertAlmostEqual(r.PAID.liability(r.SPEC_ID),.149)

    def test_interrupted_reservation_carried_into_numeric_closeout(self):
        a=self.aa[0]
        d.immutable(self.base/'openrouter/init'/f'{a["id"]}.json',{'partial':'fixture'})
        r.PAID.reserve(r.SPEC_ID,'openrouter/'+a['id'],.04)
        r.close_cohort('openrouter','interrupted')
        row=d.read(self.base/'openrouter/outcomes'/f'{a["id"]}.json')
        self.assertEqual(row['status'],'interrupted_unknown')
        self.assertEqual(row['paid_usd'],.04);self.assertTrue(row['cost_unknown'])

    def test_nine_dollar_cap_parallel_and_unknown_carry(self):
        ledger=d.PaidLedger(self.base/'cap.jsonl');ledger.reserve('historical','old',1.851345)
        ledger.reserve('new','unknown',8)
        def reserve(n):
            try:ledger.reserve('new',str(n),.5);return True
            except d.BudgetStop:return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(reserve,range(8))),2)
        self.assertAlmostEqual(ledger.liability(),10.851345)
        self.assertAlmostEqual(ledger.liability('new'),9)
        with self.assertRaises(d.BudgetStop):ledger.reserve('another','attempt',.001)
        ledger.settle('new','unknown',.1)
        self.assertAlmostEqual(ledger.liability('historical'),1.851345)
        for v in (True,-1,float('nan')):
            with self.assertRaises(d.BudgetStop):ledger.reserve('new','invalid',v)

    # R1: order/failure/stop policy is enforced inside dispatch itself.
    def http400(self):
        return urllib.error.HTTPError('http://offline',400,'bad request',{},io.BytesIO(b'{"error":{"code":400}}'))

    def _reset_cohort(self):
        import shutil
        shutil.rmtree(self.base/'openrouter',ignore_errors=True)
        for p in (self.base/'calls.jsonl',self.base/'paid.jsonl'):p.unlink(missing_ok=True)
        p=patch.object(r,'PAID',d.PaidLedger(self.base/'paid.jsonl'));p.start();self.addCleanup(p.stop)

    def assert_rejected_unsent(self,a,why,op):
        before=op.return_value.open.call_count
        calls=(self.base/'calls.jsonl').read_text() if (self.base/'calls.jsonl').exists() else ''
        paid=r.PAID.liability()
        init=self.base/'openrouter/init'/f'{a["id"]}.json'
        init_before=init.read_bytes() if init.exists() else None
        with patch.object(r,'key_for') as key:
            with self.assertRaises(r.AdmissionError) as e:r.dispatch('openrouter',a)
            key.assert_not_called()
        self.assertIn(why,str(e.exception))
        self.assertEqual(op.return_value.open.call_count,before)
        self.assertEqual((self.base/'calls.jsonl').read_text() if (self.base/'calls.jsonl').exists() else '',calls)
        self.assertEqual(r.PAID.liability(),paid)
        self.assertEqual(init.read_bytes() if init.exists() else None,init_before)

    def test_direct_dispatch_out_of_order_rejected(self):
        with patch('urllib.request.build_opener') as op:
            self.assert_rejected_unsent(self.aa[5],'out_of_order',op)
            op.return_value.open.side_effect=lambda *x,**k:self.response(self.aa[0])
            self.assertEqual(r.dispatch('openrouter',self.aa[0])['status'],'completed')
            self.assert_rejected_unsent(self.aa[2],'out_of_order',op)
            self.assert_rejected_unsent(self.aa[0],'out_of_order',op)
            self.assertEqual(op.return_value.open.call_count,1)

    def test_direct_dispatch_after_qualification_http400_rejected(self):
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=self.http400()
            self.assertEqual(r.dispatch('openrouter',self.aa[0])['error'],'http_400')
            self.assertEqual(d.read(self.base/'openrouter/stopped.json')['assignment'],self.aa[0]['id'])
            op.return_value.open.side_effect=lambda *x,**k:self.response(self.aa[1])
            self.assert_rejected_unsent(self.aa[1],'cohort_stopped',op)
            (self.base/'openrouter/stopped.json').unlink()
            self.assert_rejected_unsent(self.aa[1],'prior_failure',op)
            self.assertEqual(op.return_value.open.call_count,1)

    def test_direct_dispatch_after_wrong_qualification_rejected(self):
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=lambda *x,**k:self.response(self.aa[0],wrong=True)
            row=r.dispatch('openrouter',self.aa[0])
            self.assertEqual(row['status'],'completed')
            self.assertTrue((self.base/'openrouter/stopped.json').exists())
            self.assert_rejected_unsent(self.aa[1],'cohort_stopped',op)
            self.assert_rejected_unsent(self.aa[6],'cohort_stopped',op)
            self.assertEqual(op.return_value.open.call_count,1)

    def test_direct_dispatch_after_invalid_qualification_rejected(self):
        bad=io.BytesIO(b'{"model":"anthropic/claude-sonnet-4.6","provider":"Anthropic","usage":{"cost":0.001},"choices":[{"finish_reason":"stop","message":{"content":"not json"}}]}')
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.return_value=bad
            row=r.dispatch('openrouter',self.aa[0])
            self.assertEqual(row['status'],'failed')
            self.assertTrue((self.base/'openrouter/stopped.json').exists())
            self.assert_rejected_unsent(self.aa[1],'cohort_stopped',op)
            self.assertEqual(op.return_value.open.call_count,1)

    def test_direct_dispatch_after_main_failure_rejected(self):
        seq=iter(self.aa[:6])
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=lambda *x,**k:self.response(next(seq))
            for a in self.aa[:6]:self.assertEqual(r.dispatch('openrouter',a)['status'],'completed')
            op.return_value.open.side_effect=self.http400()
            self.assertEqual(r.dispatch('openrouter',self.aa[6])['error'],'http_400')
            op.return_value.open.side_effect=lambda *x,**k:self.response(self.aa[7])
            self.assert_rejected_unsent(self.aa[7],'cohort_stopped',op)
            self.assert_rejected_unsent(self.aa[8],'cohort_stopped',op)
            self.assertEqual(op.return_value.open.call_count,7)

    def test_direct_dispatch_after_ambiguous_predecessor_or_terminal_rejected(self):
        d.immutable(self.base/'openrouter/init'/f'{self.aa[0]["id"]}.json',{'partial':'fixture'})
        with patch('urllib.request.build_opener') as op:
            self.assert_rejected_unsent(self.aa[1],'predecessor_missing',op)
            r.close_cohort('openrouter','operator')
            self.assert_rejected_unsent(self.aa[1],'terminal_cohort',op)

    def test_stopped_cohort_then_runner_closes_without_more_requests(self):
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=self.http400();r.dispatch('openrouter',self.aa[0])
            terminal=r.execute_cohort('openrouter');self.assertEqual(op.return_value.open.call_count,1)
        self.assertEqual((terminal['failed'],terminal['not_run']),(1,149))

    # R2: saved-data reporting/checking refuses code that drifted from admission.
    def real_admission_fixture(self,dispatch_count):
        import shutil
        base=self.base/'saved';shutil.rmtree(base,ignore_errors=True);base.mkdir()
        src=self.base/'src';shutil.rmtree(src,ignore_errors=True);src.mkdir()
        for name in d.SOURCES:shutil.copy(r.ROOT/name,src/name)
        hashes={n:d.sha(src/n) for n in d.SOURCES}
        self._reset_cohort()
        # Real historical factory ledger (USD1.851345 carried) so recompute's carry check is exercised.
        shutil.copy(r.ROOT.parents[1]/'results/paid-ledger.jsonl',self.base/'paid.jsonl')
        seq=iter(self.aa)
        with patch.object(r,'RESULTS',base),patch.object(r,'source_hashes',return_value=hashes),\
             patch('urllib.request.build_opener') as op,patch('sys.stdout',new=io.StringIO()):
            shutil.copy(self.base/'assignments.json',base/'assignments.json')
            m=d.read(self.base/'admission.json');m['source_sha256']=hashes;d.immutable(base/'admission.json',m)
            op.return_value.open.side_effect=lambda *x,**k:self.response(next(seq))
            for a in self.aa[:dispatch_count]:r.dispatch('openrouter',a)
            r.close_cohort('openrouter','fixture')
        return base,src

    def reporting_modules(self,src):
        import analyze,closeout,recompute
        for mod in (analyze,closeout,recompute):
            p=patch.object(mod,'SRC',src);p.start();self.addCleanup(p.stop)
        return analyze,closeout,recompute

    def test_sources_pin_closeout_and_checker_list_matches(self):
        import recompute
        self.assertIn('closeout.py',d.SOURCES)
        self.assertIs(r.SOURCES,d.SOURCES)
        self.assertEqual(recompute.FROZEN,d.SOURCES)

    def test_reporting_runs_when_code_matches_admission(self):
        base,src=self.real_admission_fixture(7)
        analyze,closeout,recompute=self.reporting_modules(src)
        with patch('sys.stdout',new=io.StringIO()):closeout.main(base,self.base/'paid.jsonl')
        self.assertTrue((base/'FINDING.md').exists());self.assertTrue((base/'recomputation.json').exists())

    def test_reporting_refuses_drift_after_data_collection(self):
        for drifted in ('closeout.py','analyze.py','recompute.py','run.py'):
            with self.subTest(drifted=drifted):
                base,src=self.real_admission_fixture(7)
                analyze,closeout,recompute=self.reporting_modules(src)
                with open(src/drifted,'a') as h:h.write('\n# post-data edit\n')
                with self.assertRaises(d.SourceDrift):closeout.main(base,self.base/'paid.jsonl')
                with self.assertRaises(d.SourceDrift):analyze.report(base)
                with self.assertRaises(ValueError) as e:recompute.check(base,self.base/'paid.jsonl')
                self.assertIn('running source differs',str(e.exception))
                for out in ('FINDING.md','summary.json','recomputation.json','numeric-inventory.json','numeric-evidence.zip'):
                    self.assertFalse((base/out).exists(),out)

    def test_reporting_refuses_admission_missing_closeout_pin(self):
        base,src=self.real_admission_fixture(1)
        analyze,closeout,recompute=self.reporting_modules(src)
        m=d.read(base/'admission.json');del m['source_sha256']['closeout.py']
        (base/'admission.json').write_text(json.dumps(m))
        with self.assertRaises(d.SourceDrift):closeout.main(base,self.base/'paid.jsonl')
        with self.assertRaises(ValueError):recompute.check(base,self.base/'paid.jsonl')

    def test_zero_dispatch_closeout_without_calls_ledger(self):
        base,src=self.real_admission_fixture(0)
        self.assertFalse((base/'calls.jsonl').exists())
        analyze,closeout,recompute=self.reporting_modules(src)
        with patch('sys.stdout',new=io.StringIO()):closeout.main(base,self.base/'paid.jsonl')
        self.assertIn('Qualification stopped at 0/6',(base/'FINDING.md').read_text())
        self.assertNotIn('calls.jsonl',d.read(base/'numeric-inventory.json')['files'])


if __name__=='__main__':unittest.main()
