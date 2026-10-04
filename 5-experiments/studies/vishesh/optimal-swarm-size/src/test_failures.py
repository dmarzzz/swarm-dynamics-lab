import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from engine import execute
from failures import SafeFailure
from tasks import generate,qualification_manifest,reference_answer
import run_qualification as runner

class Failures(unittest.TestCase):
    def test_allowlisted_codes_and_no_plan_retries(self):
        task=generate('evidence','parallel',0)
        for code in ('provider_deadline','http_429','usage_missing','route_changed','credential_unavailable','stage_budget_exhausted'):
            calls=[]
            def fail(*args):calls.append(1);raise SafeFailure(code)
            result=execute(task.public,1,1,10,2,fail)
            self.assertEqual(result['failure'],code);self.assertEqual(len(calls),1)
        self.assertEqual(SafeFailure('secret-value').code,'transport_failed')

    def test_fatal_work_error_stops_integration(self):
        task=generate('evidence','parallel',0);calls=[]
        def call(messages,deadline,actor,phase,item):
            calls.append(phase)
            if phase=='plan':return json.dumps({'dependencies':task.public['dependencies']})
            raise SafeFailure('route_changed')
        result=execute(task.public,1,1,10,2,call)
        self.assertEqual(calls,['plan','work']);self.assertTrue(result['fatal'])

    def run_mock_batch(self,reporter,provider):
        cfg=json.loads((Path(runner.__file__).parent.parent/'qualification-config.json').read_text())
        assignments=[r for r in qualification_manifest() if r['stage']=='Q-A']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);out=root/'run';out.mkdir()
            with patch.object(runner,'Reporter',reporter),patch.object(runner,'Provider',provider),contextlib.redirect_stdout(io.StringIO()):
                runner.run_batch(cfg,'offline',out,root/'ledger.sqlite',assignments)
            result=json.loads((out/'reconciliation.json').read_text())
            records=[json.loads(p.read_text()) for p in out.glob('*/outcome.json')]
            traces=[p.read_text() for p in out.glob('*/trace.jsonl')]
            self.assertEqual(len(result['episodes']),16)
            self.assertEqual(len(list(out.glob('*/assignment.json'))),16)
            return result,records,traces

    def test_admission_failure_reconciles_all(self):
        class Failed:
            def __init__(self,*a):raise SafeFailure('public_run_preflight_failed')
        result,records,_=self.run_mock_batch(Failed,None)
        self.assertEqual(len(records),0);self.assertEqual(result['episodes'][0]['execution'],'admission_failed')
        self.assertEqual(sum(s['execution']=='not_started' for s in result['episodes']),15)

    def test_progress_fault_does_not_abort_model(self):
        class Reporter:
            def __init__(self,*a):pass
            def progress(self,*a):raise RuntimeError('private unlogged error')
            def finish(self,*a):return {'complete':True}
        result,records,traces=self.run_mock_batch(Reporter,ScriptedProvider)
        self.assertEqual(len(records),16);self.assertTrue(result['execution_complete'])
        self.assertTrue(all(r['failure'] is None and r['completed_items']==16 for r in records))
        self.assertTrue(any('reporting_failure' in t for t in traces));self.assertTrue(all('private unlogged' not in t for t in traces))

    def test_upload_fault_preserves_outcome_stops_batch(self):
        class Reporter:
            def __init__(self,*a):pass
            def progress(self,*a):return {'acknowledged':True}
            def finish(self,*a):return {'complete':False}
        result,records,_=self.run_mock_batch(Reporter,ScriptedProvider)
        self.assertEqual(len(records),1);self.assertEqual(result['stop_reason'],'publication_incomplete')
        self.assertEqual(result['episodes'][0]['publication'],'incomplete')
        self.assertEqual(sum(s['execution']=='not_started' for s in result['episodes']),15)

    def test_fatal_transport_stops_batch(self):
        class Reporter:
            def __init__(self,*a):pass
            def progress(self,*a):return {'acknowledged':True}
            def finish(self,*a):return {'complete':True}
        calls=[]
        class FailedProvider:
            def __init__(self,*a):pass
            def __call__(self,*a):calls.append(1);raise SafeFailure('stage_budget_exhausted')
        result,records,_=self.run_mock_batch(Reporter,FailedProvider)
        self.assertEqual(len(calls),1);self.assertEqual(len(records),1)
        self.assertEqual(result['stop_reason'],'stage_budget_exhausted')

class ScriptedProvider:
    def __init__(self,*a):pass
    def __call__(self,messages,deadline,actor,phase,item):
        public=json.loads(messages[1]['content'])
        if phase=='plan':return json.dumps({'dependencies':public['dependencies']})
        return json.dumps({'artifact':0})
