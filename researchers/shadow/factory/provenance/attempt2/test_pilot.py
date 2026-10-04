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
            with self.assertRaises(FileNotFoundError):r.dispatch('openrouter',self.aa[6])
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

if __name__=='__main__':unittest.main()
