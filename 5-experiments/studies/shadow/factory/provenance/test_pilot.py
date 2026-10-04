"""Offline software fixtures only: every model HTTP call is mocked."""
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


class InstrumentTests(unittest.TestCase):
    def test_fixed_roots_tokens_padding_and_counterbalance(self):
        aa=ins.assignments('pool');self.assertEqual(len(aa),150)
        self.assertEqual(len({a['id'] for a in aa}),150)
        import tiktoken
        enc=tiktoken.get_encoding('cl100k_base')
        for a in aa:
            self.assertEqual(len(enc.encode(ins.SYSTEM))+len(enc.encode(a['prompt'])),1800)
            self.assertEqual(a['prompt'].count('MEASUREMENT:')+a['prompt'].count('IRRELEVANT:'),20)
            if a['stage']=='M':
                w=a['world'];self.assertLess(w['unique_total']*(w['unique_total']+3*w['values'][w['copied_origin']]),0)
        for root in range(12):
            cells=[a for a in aa if a['stage']=='M' and a['world']['root']==root]
            self.assertEqual(len(cells),12)
            self.assertEqual(len({ins.digest(a['world']) for a in cells}),1)
            self.assertEqual(len({a['prompt'] for a in cells if a['arm']=='dedup'}),1)
        self.assertEqual(len({tuple(a['world']['order']) for a in aa if a['stage']=='M'}),10)

    def test_clean_disjoint_streams_and_oracle(self):
        pool=ins.assignments('pool');paid=ins.assignments('openrouter')
        self.assertNotEqual([x['world'] for x in pool[:6]],[x['world'] for x in paid[:6]])
        for a in pool:
            decision='A' if sum(a['world']['values'])>0 else 'B'
            self.assertEqual(ins.score({'decision':decision,'confidence':1},a),{'accuracy':1,'false_confidence':0})

    def test_wire_schema_omits_unsupported_numeric_bounds(self):
        # Anthropic raw structured-output schemas do not accept these keywords;
        # SDK transformation normally strips them. Local validation stays strict.
        unsupported={'minimum','maximum','exclusiveMinimum','exclusiveMaximum','multipleOf'}
        def visit(node):
            if isinstance(node,dict):
                self.assertFalse(unsupported.intersection(node))
                for value in node.values():visit(value)
            elif isinstance(node,list):
                for value in node:visit(value)
        visit(ins.SCHEMA)
        self.assertEqual(ins.SCHEMA['properties']['confidence'],{'type':'number'})
        for value in (-.001,1.001,float('nan'),True):
            with self.assertRaises(ValueError):ins.validate_answer({'decision':'A','confidence':value})

    def test_schema_domain(self):
        for value in [True,-.1,1.1,float('nan'),float('inf'),'0.9']:
            with self.assertRaises(ValueError):ins.validate_answer({'decision':'A','confidence':value})
        with self.assertRaises(ValueError):ins.validate_answer({'decision':'C','confidence':.5})


class DurableTests(unittest.TestCase):
    def test_immutable_duplicate_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'record.json';d.immutable(p,{'value':1});before=p.read_bytes()
            with self.assertRaises(FileExistsError):d.immutable(p,{'value':2})
            self.assertEqual(p.read_bytes(),before)
            with self.assertRaises(ValueError):d.immutable(Path(t)/'nan.json',{'value':float('nan')})

    def test_shared_caps_and_parallel_last_reservation(self):
        with tempfile.TemporaryDirectory() as t:
            ledger=d.PaidLedger(Path(t)/'ledger.jsonl')
            for i in range(4):ledger.reserve('historical'+str(i),'a',4)
            def reserve(i):
                try:ledger.reserve('new',str(i),1);return True
                except d.BudgetStop:return False
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as p:
                self.assertEqual(sum(p.map(reserve,range(12))),4)
            self.assertEqual(ledger.liability(),20)
            with self.assertRaises(d.BudgetStop):ledger.reserve('other','a',.001)

    def test_unknown_liability_and_invalid_cost(self):
        with tempfile.TemporaryDirectory() as t:
            ledger=d.PaidLedger(Path(t)/'ledger.jsonl');ledger.reserve('study','first',3)
            self.assertEqual(ledger.liability('study'),3)
            with self.assertRaises(d.BudgetStop):ledger.reserve('study','second',2)
            ledger.settle('study','first',.1);ledger.reserve('study','second',2)
            self.assertAlmostEqual(ledger.liability(),2.1)
            for value in [-1,float('nan'),float('inf'),True]:
                with self.assertRaises(d.BudgetStop):ledger.reserve('study','bad',value)


class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.aa={route:ins.assignments(route) for route in ('pool','openrouter')}

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.sources={'unit':'frozen'}
        for attr,value in [('RESULTS',self.base),('PAID',d.PaidLedger(self.base/'paid.jsonl')),('DEADLINE',20000000000)]:
            p=patch.object(r,attr,value);p.start();self.addCleanup(p.stop)
        for target,value in [('source_hashes',self.sources),('key_for','offline-dummy')]:
            p=patch.object(r,target,return_value=value);p.start();self.addCleanup(p.stop)
        d.immutable(self.base/'assignments.json',self.aa)
        d.immutable(self.base/'admission.json',{'study':r.SPEC_ID,'max_http_attempts':151,'source_sha256':self.sources,
            'source_revision':'offline-fixture','dependency_versions':{p:r.importlib.metadata.version(p) for p in ('tiktoken','PyYAML')},
            'assignment_file_sha256':d.sha(self.base/'assignments.json'),
            'assignment_digest':{k:ins.digest(v) for k,v in self.aa.items()},'deadline':20000000000,
            'public_plan_url':'https://example.invalid/offline','registration_readback':{'id':r.SPEC_ID,'url':'https://example.invalid/offline'}})

    def response(self,a,model='claude-sonnet-4-6'):
        return io.BytesIO(json.dumps({'model':model,'usage':{'input_tokens':2000,'output_tokens':30},'stop_reason':'end_turn',
            'content':[{'type':'text','text':json.dumps({'decision':a['world']['target'],'confidence':.9})}]}).encode())

    def test_unregistered_direct_call_never_loads_credentials(self):
        with patch.object(r,'RESULTS',self.base/'absent'),patch.object(r,'key_for') as key,patch('urllib.request.build_opener') as op:
            with self.assertRaises(FileNotFoundError):r.dispatch('pool',self.aa['pool'][0])
            key.assert_not_called();op.assert_not_called()

    def test_init_and_reservation_precede_network_numeric_precedes_reporting(self):
        a=self.aa['pool'][0]
        def fake_open(request,timeout):
            self.assertTrue((self.base/'pool/init'/f'{a["id"]}.json').exists())
            self.assertEqual(len((self.base/'calls.jsonl').read_text().splitlines()),1)
            self.assertLessEqual(timeout,90)
            return self.response(a)
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=fake_open;row=r.dispatch('pool',a)
        self.assertEqual(row['status'],'completed')
        outcome=self.base/'pool/outcomes'/f'{a["id"]}.json';before=outcome.read_bytes()
        with self.assertRaises(RuntimeError):raise RuntimeError('fake renderer failure after numeric outcome')
        self.assertEqual(outcome.read_bytes(),before)
        with self.assertRaises(r.AdmissionError):r.dispatch('pool',a)

    def test_main_without_qualification_blocked(self):
        with patch('urllib.request.build_opener') as op:
            with self.assertRaises(FileNotFoundError):r.dispatch('pool',self.aa['pool'][6])
            op.assert_not_called()

    def test_fallback_without_pool_failure_blocked(self):
        with patch('urllib.request.build_opener') as op:
            with self.assertRaises(FileNotFoundError):r.dispatch('openrouter',self.aa['openrouter'][0])
            op.assert_not_called()

    def test_changed_assignment_and_source_blocked(self):
        with patch('urllib.request.build_opener') as op:
            a=dict(self.aa['pool'][0],prompt='modified')
            with self.assertRaises(r.AdmissionError):r.dispatch('pool',a)
            with patch.object(r,'source_hashes',return_value={'unit':'drift'}):
                with self.assertRaises(r.AdmissionError):r.dispatch('pool',self.aa['pool'][0])
            op.assert_not_called()

    def test_provider_failure_no_retry_and_closeout(self):
        a=self.aa['pool'][0]
        error=urllib.error.HTTPError('http://offline',503,'unavailable',{},None)
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=error;row=r.dispatch('pool',a)
            self.assertEqual(op.return_value.open.call_count,1)
        self.assertEqual(row['error'],'http_503')
        t=r.close_cohort('pool','transport')
        self.assertEqual((t['failed'],t['not_run']),(1,149))
        with self.assertRaises(r.AdmissionError):r.dispatch('pool',self.aa['pool'][1])

    def test_served_model_mismatch_is_retained(self):
        a=self.aa['pool'][0]
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.return_value=self.response(a,'wrong-model');row=r.dispatch('pool',a)
        self.assertEqual(row['status'],'failed');self.assertEqual(row['served_model'],'wrong-model')
        self.assertIn('served_model_mismatch',row['error'])

    def test_request_cap_blocks_before_http(self):
        with d.locked(self.base/'calls.jsonl') as h:
            for n in range(151):d.append_locked(h,{'call':str(n)})
        with patch('urllib.request.build_opener') as op:
            row=r.dispatch('pool',self.aa['pool'][0]);op.assert_not_called()
        self.assertIn('http_attempt_cap',row['error']);self.assertFalse(row['network_attempted'])

    def test_main_admitted_only_after_six_clean_receipted_answers(self):
        seq=iter(self.aa['pool'][:7])
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=lambda *args,**kwargs:self.response(next(seq))
            for a in self.aa['pool'][:7]:
                row=r.dispatch('pool',a)
                self.assertEqual(row['status'],'completed')
        self.assertEqual(row['stage'],'M')

    def test_paid_fallback_reserves_before_network_and_settles(self):
        error=urllib.error.HTTPError('http://offline',503,'unavailable',{},None)
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=error;r.dispatch('pool',self.aa['pool'][0])
        r.close_cohort('pool','transport')
        a=self.aa['openrouter'][0]
        def fake_open(*args,**kwargs):
            self.assertGreater(r.PAID.liability(r.SPEC_ID),0)
            return io.BytesIO(json.dumps({'model':'anthropic/claude-sonnet-4.6','provider':'Anthropic',
                'usage':{'cost':.001,'prompt_tokens':2000,'completion_tokens':30},
                'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'decision':a['world']['target'],'confidence':.9})}}]}).encode())
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.side_effect=fake_open;row=r.dispatch('openrouter',a)
        self.assertEqual(row['status'],'completed');self.assertAlmostEqual(r.PAID.liability(),.001)

    def test_valid_wrong_qualification_stops_without_fallback(self):
        a=self.aa['pool'][0]
        response=json.loads(self.response(a).getvalue())
        response['content'][0]['text']=json.dumps({'decision':'B' if a['world']['target']=='A' else 'A','confidence':.95})
        with patch('urllib.request.build_opener') as op:
            op.return_value.open.return_value=io.BytesIO(json.dumps(response).encode())
            r.run();self.assertEqual(op.return_value.open.call_count,1)
        term=d.read(self.base/'pool/terminal.json')
        self.assertEqual(term['reason'],'clean_competence_failure');self.assertEqual(term['completed'],1)
        self.assertEqual(d.read(self.base/'openrouter/terminal.json')['not_run'],150)

    def test_ambiguous_init_gets_unknown_not_retried(self):
        a=self.aa['pool'][0];d.immutable(self.base/'pool/init'/f'{a["id"]}.json',{'partial':'fixture'})
        with patch('urllib.request.build_opener') as op:
            terminal=r.execute_cohort('pool');op.assert_not_called()
        self.assertEqual(terminal['failed'],1)
        self.assertEqual(d.read(self.base/'pool/outcomes'/f'{a["id"]}.json')['status'],'interrupted_unknown')

if __name__=='__main__':unittest.main()
