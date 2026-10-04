"""Complete offline diagnostic boundary rehearsal. Development worlds only, no provider traffic."""
import copy
import contextlib
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
import urllib.error
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import diagnostic as d
import diagnostic_launch as worker
import diagnostic_admission as admission
from diagnostic_prepare import candidate
from diagnostic_relay import validate_payload
from common import canonical,digest
from native import request


class DiagnosticTests(unittest.TestCase):
    def test_manifest_ids_and_non_authorizing_candidate(self):
        rows=d.assignments()
        self.assertEqual(len(rows),36)
        self.assertEqual(len({r['id'] for r in rows}),36)
        self.assertEqual({r['root'] for r in rows},{400,404,408})
        self.assertFalse(any('expected' in r for r in rows))
        c=candidate()
        self.assertFalse(c['owner_update_approval']['approved'])
        self.assertIsNone(c['public_plan']['url'])
        with self.assertRaises(ValueError):admission.verify(c,actual_host='fixture')

    def admitted_fixture(self):
        c=candidate();now=time.time()
        c['owner_update_approval'].update(approved=True,decision_reference='FAKE-OFFLINE-ONLY')
        c['authorization'].update(owner_approved=True,reference='FAKE-OFFLINE-ONLY',deadline=now+3500)
        c['allocation'].update(host='fixture',claim_id='fixture',merged_claim_revision='0'*40,exclusive=True,
            registered_fleet_destination=True,workload_idle=True,approved_account_verified=True,checked_at=now,
            expires_at=now+7200,allocated_usd_per_hour=.07143,charge_started_at=now-10)
        c['credential']['study_authorized']=True
        url='https://github.com/dmarzzz/swarm-lab/blob/'+'0'*40+'/fixture'
        c['public_plan'].update(url=url,sha256='0'*64);c['page_verification'].update(url=url,rendered=True,checked_at=now)
        return c,now

    def test_admission_rejects_scope_budget_source_and_stale_approval(self):
        c,now=self.admitted_fixture();self.assertTrue(admission.verify(c,now=now,actual_host='fixture')['ready'])
        mutations=[('attempt','S0-02'),('maximum_new_calls',37),('stop_contract','global-only'),('proposal_sha256','0'*64),('assignment_sha256','0'*64)]
        for field,value in mutations:
            bad=copy.deepcopy(c);bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):admission.verify(bad,now=now,actual_host='fixture')
        for field,value in [('approved',False),('proposal_sha256','0'*64),('instrument_sha256','0'*64)]:
            bad=copy.deepcopy(c);bad['owner_update_approval'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):admission.verify(bad,now=now,actual_host='fixture')
        for field,value in [('deadline',now+3601),('api_cap_usd',2),('physical_call_cap',324)]:
            bad=copy.deepcopy(c);bad['authorization'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):admission.verify(bad,now=now,actual_host='fixture')
        bad=copy.deepcopy(c);bad['allocation']['charge_started_at']=now-901
        with self.assertRaises(ValueError):admission.verify(bad,now=now,actual_host='fixture')

    def test_relay_refuses_s0_ids_retries_and_wrong_roles(self):
        models=json.loads((BASE/'models.json').read_text())['models']
        packet=d.probe(d.make_case(0,development=True),0,'generalist')
        wire={'id':'D0-01:generalist:0:0:physical-0','role':'generalist','request':request(models['generalist'],packet['sections'])}
        validate_payload(wire,models)
        for value in ['S0-02:generalist:0:0:physical-0','D0-01:generalist:0:0:physical-1','D0-01:generalist:3:0:physical-0']:
            bad=dict(wire,id=value)
            with self.assertRaises(ValueError):validate_payload(bad,models)
        with self.assertRaises(ValueError):validate_payload(dict(wire,role='typed_choice'),models)

    def rehearse(self,fault=None):
        models=json.loads((BASE/'models.json').read_text())['models'];expected={}
        # Build all scripted reference outputs on disjoint development roots before invoking the real loop.
        for role in d.ROLES:
            for case in range(3):
                state=d.make_case(case,development=True);state['engine'].actors['agent-0'].model=role
                for step in range(4):
                    p=d.probe(state,step,role);req=request(models[role],p['sections'],p['choices'])
                    expected[f'D0-01:{role}:{case}:{step}:physical-0']=(copy.deepcopy(p),req)
                    self.assertTrue(d.apply(state,step,p['expected'],p['expected'])['correct'])
        dispatches=[];completions=[]
        class Provider:
            def open(self,wire,**kwargs):
                envelope=json.loads(wire.data);dispatches.append(envelope)
                packet,req=expected[envelope['id']]
                assert envelope['request']==req
                model=models[envelope['role']]
                raw={'model':model['accepted_response_model_ids'][0],'provider':model['provider_name']}
                if model['kind']=='chat':
                    raw.update(choices=[{'finish_reason':'stop','message':{'content':canonical(packet['expected'])}}],
                               usage={'prompt_tokens':100,'completion_tokens':20,'cost':.00001})
                else:
                    choice=next(k for k,v in packet['choices'].items() if v==packet['expected'])
                    raw.update(answers={'action':{'type':'choice','choice':choice,'probabilities':{k:int(k==choice) for k in packet['choices']}}},
                               usage={'input_tokens':100,'output_tokens':0,'cost':.0000042})
                if len(dispatches)==1:
                    if fault=='http':raise urllib.error.HTTPError('http://127.0.0.1:1/invoke',429,'fixture',{},io.BytesIO(b'{"error_type":"provider_http","http_status":429}'))
                    if fault=='invalid':raw['choices'][0]['message']['content']='```json\n{"fetch":{}}\n```'
                    if fault=='route':raw['provider']='unexpected'
                    if fault=='usage':raw['usage']['cost']=1
                    if fault=='protected':raw['choices'][0]['message']['content']='{"type":"fetch","endpoint":"private_truth","entities":["sku-0"]}'
                return io.BytesIO(canonical(raw).encode())
        class Run:
            def __init__(self,ident,*args):self.ident=ident;self._alive=threading.Event()
            def progress(self,*args,**kwargs):return True
            def artifact(self,*args,**kwargs):return {'spooled':False}
            def done(self,**kwargs):completions.append((self.ident,'done'))
            def fail(self,**kwargs):completions.append((self.ident,'failed'))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config=root/'config.json'
            config.write_text(json.dumps({'attempt':'D0-01','source_commit':'fixture','file_hashes':{},
                'allocation':{'host':'fixture','allocated_usd_per_hour':.07143},'authorization':{'deadline':time.time()+3600},
                'credential':{'relay_url':'http://127.0.0.1:1/invoke'},'condition_tldrs':{r:'SCRIPTED OFFLINE' for r in d.ROLES}}))
            def private_path(value):return root/'authority' if value=='/srv/swarm/poietic-agents-authority' else Path(value)
            with patch.object(worker,'verify'),patch.object(worker,'source_check'),patch.object(worker,'verify_public',return_value={}), \
                 patch.object(worker,'verify_catalog',return_value={}),patch.object(worker,'verify_relay_health'), \
                 patch.object(worker,'read_json',return_value={}),patch.object(worker.urllib.request,'build_opener',return_value=Provider()), \
                 patch.object(worker,'Path',side_effect=private_path),patch.object(worker,'make_case',side_effect=lambda case:d.make_case(case,development=True)), \
                 patch.dict(sys.modules,{'swarm_report':SimpleNamespace(Run=Run,report=lambda *args,**kwargs:True)}), \
                 patch.dict(worker.os.environ,{}),contextlib.redirect_stdout(io.StringIO()):worker.run(config,root/'out')
            records=json.loads((root/'out/records.json').read_text());summary=json.loads((root/'out/summary.json').read_text())
            with contextlib.closing(sqlite3.connect(root/'authority/budget.sqlite')) as db:charges=db.execute('SELECT status,settled FROM charges ORDER BY id').fetchall()
            self.assertEqual(len(records),36);self.assertEqual(summary['terminal'],36)
            self.assertFalse(summary['qualification_passed']);self.assertFalse(summary['scientific_result'])
            self.assertTrue((root/'out/final_frame.png').exists());self.assertEqual(len(charges),len(dispatches))
            self.assertEqual(len({x['id'] for x in dispatches}),len(dispatches))
            return summary,records,charges,completions

    def test_complete_success_is_only_diagnostic(self):
        summary,records,charges,done=self.rehearse()
        self.assertEqual(summary['started'],36);self.assertTrue(summary['diagnostic_passed'])
        self.assertTrue(all(x[0]=='known' for x in charges));self.assertEqual([s for _,s in done],['done']*3)
        for row in records:
            self.assertEqual(row['checked']['action'],row['expected_action'])
            self.assertEqual(digest(row['action_effect']['definition']),row['definition_sha256'])

    def test_format_failure_stops_role_preserves_known_billing_and_other_roles(self):
        summary,records,charges,done=self.rehearse('invalid')
        self.assertEqual(summary['started'],25);self.assertIsNone(summary['stop_reason'])
        self.assertEqual(summary['role_stop_reasons'],{'generalist':'role_interface_failure_guard'})
        self.assertEqual(sum(r['status']=='not_started' for r in records),11)
        self.assertTrue(all(x[0]=='known' for x in charges));self.assertEqual([s for _,s in done],['failed','done','done'])

    def test_transport_failure_stops_all_without_retry(self):
        summary,records,charges,done=self.rehearse('http')
        self.assertEqual(summary['started'],1);self.assertEqual(summary['stop_reason'],'transport_or_runtime_failure_guard')
        self.assertEqual(charges,[('uncertain',None)]);self.assertEqual(sum(r['status']=='not_started' for r in records),35)

    def test_route_mismatch_stops_all_with_known_bill(self):
        summary,_,charges,_=self.rehearse('route')
        self.assertEqual(summary['started'],1);self.assertEqual(summary['stop_reason'],'integrity_guard');self.assertEqual(charges,[('known',10000)])

    def test_bad_usage_stops_all_and_retains_reserve(self):
        summary,_,charges,_=self.rehearse('usage')
        self.assertEqual(summary['started'],1);self.assertEqual(summary['stop_reason'],'integrity_guard');self.assertEqual(charges,[('uncertain',None)])

    def test_protected_action_stops_all(self):
        summary,records,_,_=self.rehearse('protected')
        self.assertEqual(summary['started'],1);self.assertEqual(summary['stop_reason'],'integrity_guard')
        self.assertTrue(records[0]['protected_access_violation'])


if __name__=='__main__':unittest.main()
