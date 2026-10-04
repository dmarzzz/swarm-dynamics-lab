import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from common import sha,write,original
from cases import suite,words,validate
from compare import evaluate,qualify
from pack_cases import label
from worker import settings
import runner

class ComparisonTests(unittest.TestCase):
    def test_all_case_controls(self):self.assertTrue(validate()['passed'])
    def test_label_grammar(self):
        for text,value in [('17.999','17999.00'),('3.600.000','3600000.00'),('Rp 12,50','12.50'),('1,234.50','1234.50')]:
            self.assertEqual(label(text),value)
        for text in ('Total 12','12-50','1.2.3',None):self.assertIsNone(label(text))
    def test_wrong_accept_not_rescue(self):
        records={'a':{'P':{'status':'valid','raw_words':words([['Subtotal','100']]),'wall_s':2},
                      'C':{'status':'valid','raw_words':words([['Total','200']]),'wall_s':3}}}
        r=evaluate([{'id':'a','value':'100.00'}],records)
        self.assertEqual(r['introduced_wrong_accepts'],1);self.assertEqual(r['rescues'],0)
    def test_correct_primary_never_uses_checker(self):
        records={'a':{'P':{'status':'valid','raw_words':words([['Total','100']]),'wall_s':2}}}
        r=evaluate([{'id':'a','value':'100.00'}],records)
        self.assertEqual(r['policies']['selective_checker']['correct'],1)
        self.assertEqual(r['policies']['selective_checker']['checker_requests'],0)
    def test_failed_primary_not_valid_abstention(self):
        r=evaluate([{'id':'a','value':'100.00'}],{})
        self.assertTrue(all(v['failed_or_missing']==1 for v in r['policies'].values()))
    def test_unscorable_not_correct(self):
        r=evaluate([{'id':'a','value':None}],{'a':{'P':{'status':'valid','raw_words':words([['Total','100']]),'wall_s':1}}})
        self.assertEqual(r['policies']['repaired_primary']['unscorable'],1)
    def test_correlated_wrong_reported(self):
        c={'status':'valid','raw_words':words([['Total','200']]),'wall_s':1}
        r=evaluate([{'id':'a','value':'100.00'}],{'a':{'P':c,'C':c}})
        self.assertEqual(r['same_wrong_value'],1)

class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
        self.cases=self.root/'cases';actor=self.cases/'qualification/actor';actor.mkdir(parents=True)
        ev=self.cases/'qualification/evaluator';ev.mkdir();rows=[];gold=[]
        for i in range(6):
            name=f'case-{i:03d}';image=actor/(name+'.png');image.write_bytes(b'fake image fixture')
            rows.append({'id':name,'image':image.name,'sha256':sha(image)});gold.append({'id':name,'value':'100.00'})
        write(actor/'manifest.json',{'cases':rows});write(ev/'gold.json',{'cases':gold})
        self.freeze={'splits':{'qualification':{'actor_sha256':sha(actor/'manifest.json'),'gold_sha256':sha(ev/'gold.json')}}}
    def invoke(self,reader,image,directory,runtime):
        private=directory/'private';private.mkdir(parents=True)
        w=words([['Total','100']]);write(private/'output.json',{'candidate':original.extract(w),'raw_words':w})
        write(private/'effective-context.json',{'settings':settings(reader),'input_sha256':sha(image),'worker_source_sha256':sha(runner.HERE/'worker.py')})
        for file in ('stdout.bin','stderr.bin','phases.jsonl'):(private/file).write_bytes(b'fixture bytes')
        return {'status':'valid','category':'ok','wall_s':1}
    def test_complete_capture_and_replay(self):
        r=runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=self.invoke)
        self.assertTrue(r['qualification_passed']);self.assertEqual(r['started_calls'],12)
        self.assertEqual(r['trace_status'],'verified_declared_coverage')
        self.assertFalse(r['automatic_successor'])
        with self.assertRaises(FileExistsError):runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=self.invoke)
    def test_fail_fast_preserves_unstarted(self):
        def fail(*args):self.invoke(*args);return {'status':'error','category':'timeout','wall_s':90}
        r=runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=fail)
        self.assertFalse(r['qualification_passed']);self.assertEqual(r['started_calls'],1);self.assertEqual(r['unstarted_calls'],11)
    def test_context_drift_stops(self):
        def drift(*args):
            result=self.invoke(*args);(args[2]/'private/effective-context.json').write_text('{}');return result
        r=runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=drift)
        self.assertEqual(r['stop'],'effective_context_mismatch');self.assertEqual(r['started_calls'],1)
    def test_input_tamper_prevents_dispatch(self):
        (self.cases/'qualification/actor/case-000.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'input_mismatch'):
            runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=lambda *a:self.fail('dispatched'))
    def test_interrupt_retains_unresolved_start(self):
        def interrupted(*args):raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=interrupted)
        r=json.loads((self.root/'out/summary.json').read_text())
        self.assertEqual(r['unresolved_started'],1);self.assertEqual(r['stop'],'interrupted');self.assertFalse(r['qualification_passed'])
    def test_worker_phases_with_injected_engine(self):
        from worker import execute
        from telemetry import Phases,inspect_phases
        w=words([['Total','100']])
        def loader(engine,models):return lambda:object(),lambda reader,image:w,lambda value:value
        phases=Phases(self.root/'phases.jsonl')
        try:execute(self.root/'image','P',self.root,self.root/'output.json',phases,loader=loader)
        finally:phases.close()
        self.assertTrue(inspect_phases(self.root/'phases.jsonl',True)['complete'])
        self.assertEqual(json.loads((self.root/'output.json').read_text())['candidate']['value'],'100.00')
    def test_wrong_dataset_rejected(self):
        from pack_cases import build
        source=self.root/'fake.parquet';source.write_bytes(b'wrong bytes')
        with self.assertRaisesRegex(ValueError,'dataset_shard_mismatch'):
            build(source,self.root/'pack',self.root/'qa.json')
    def test_admission_mutations(self):
        runtime={};a={'study':'antsy-targeted-v8','attempt':'Q0-comparison','instrument_sha256':runner.instrument(),
          'freeze_sha256':runner.digest(self.freeze),'runtime_sha256':runner.digest(runtime),'max_calls':12,
          'max_total_calls':48,'deadline_s':90,'eligibility_s':45,'new_charge_cap_usd':0,'automatic_retries':False,
          'authority_reference_sha256':'a'*64,'verified_at':100,'claim_expires_at':5000,'previous_calls':0}
        flags=('owner_scope_approved','exclusive_claim_verified','approved_account_verified','runtime_pinned',
               'public_plan_registered','public_page_verified','prior_budget_reconciled','duplicate_dispatch_fenced')
        a.update({f:True for f in flags});self.assertTrue(runner.admit(a,'qualification',self.freeze,runtime,now=101))
        for key,value in [(f,False) for f in flags]+[('max_calls',13),('new_charge_cap_usd',1),('verified_at',-1000),('previous_calls',1),('instrument_sha256','b'*64)]:
            changed={**a,key:value}
            with self.assertRaises(ValueError):runner.admit(changed,'qualification',self.freeze,runtime,now=101)
    def test_admission_fail_closed(self):
        with self.assertRaises(ValueError):runner.admit({},'qualification',self.freeze,{},now=0)
    def test_stage_deadline_leaves_all_unstarted(self):
        times=iter((0,1190))
        r=runner.collect('qualification',self.cases,self.root/'out',self.freeze,{},invoke=lambda *a:self.fail('dispatch'),clock=lambda:next(times))
        self.assertEqual(r['started_calls'],0);self.assertEqual(r['unstarted_calls'],12)

if __name__=='__main__':unittest.main()
