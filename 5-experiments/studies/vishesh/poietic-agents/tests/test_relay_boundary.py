"""Exercise the actual loopback handler with a fake provider; no external/model traffic."""
import io
import json
import http.client
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import relay
import diagnostic_relay
import p30_relay,p30
import q30v4_relay,q30v4
from budget import Budget
from common import digest
from common import canonical
from native import request
from qualification import make_case,probe

class RelayBoundaryTests(unittest.TestCase):
    def run_boundary(self,provider_result,relay_module=relay):
        relay=relay_module
        q4_stage=relay is q30v4_relay
        p30_stage=relay is p30_relay
        diagnostic=relay is diagnostic_relay
        stage="Q30-01" if p30_stage else ("D0-01" if diagnostic else "S0-02")
        worker_module="p30_launch" if p30_stage else ("diagnostic_launch" if diagnostic else "launch")
        models=p30.models() if p30_stage else json.loads((BASE/'models.json').read_text())['models']
        state=make_case(0,development=True);packet=probe(state,0,'generalist')
        payload={'id':stage+':generalist:0:0:physical-0','role':'generalist','request':request(models['generalist'],packet['sections'])}
        if p30_stage:payload['request']=p30.wire(models['generalist'],p30.probe(p30.make_case(0,development=True),0,'generalist')['sections'])
        if q4_stage:
            stage='Q30-04';worker_module='q30v4_launch';models=q30v4.models()
            payload=dict(id='Q30-04:cheap_generative:0:0:physical-0',role='cheap_generative',request=q30v4.wire(models['cheap_generative'],q30v4.probe(q30v4.make_case(0,development=True),0,'cheap_generative')['sections']))
        current=time.time();deadline=current+120;clock=[current]
        original_server=relay.HTTPServer
        class OneRequest(original_server):
            def handle_request(self):
                super().handle_request();clock[0]=deadline+1
        class Provider:
            def open(self,*args,**kwargs):
                if isinstance(provider_result,Exception):raise provider_result
                return io.BytesIO(canonical(provider_result).encode())
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);key=root/'fixture-key';key.write_text('FAKE_UNIT_CREDENTIAL_NOT_USABLE');key.chmod(0o600)
            config=root/'config.json';config.write_text(json.dumps({'attempt':stage,'allocation':{'host':'fixture'},'authorization':{'deadline':deadline}}))
            port=root/'port';ledger=root/'budget.sqlite';errors=[]
            if p30_stage or q4_stage:
                cfg=json.loads(config.read_text());cfg['prior_budget']={'physical_calls':54,'exposure_nano':496781964};config.write_text(json.dumps(cfg))
                if q4_stage:cfg['prior_budget']={'physical_calls':144,'exposure_nano':503255445};config.write_text(json.dumps(cfg))
                b=Budget(ledger,digest(cfg['authorization']),'fixture',1_500_000_000,288,deadline)
                for i in range(cfg['prior_budget']['physical_calls']):b.reserve('history-'+str(i),'fixture',cfg['prior_budget']['exposure_nano']-(cfg['prior_budget']['physical_calls']-1) if i==0 else 1);b.settle('history-'+str(i))
                b.close()
            def target():
                try:relay.serve(config,key,ledger,port)
                except BaseException as exc:errors.append(type(exc).__name__)
            with patch.object(relay,'verify'),patch.object(relay,'verify_public'),patch(worker_module+'.source_check'),patch.object(relay,'verify_catalog'),patch(worker_module+'.read_json',return_value={}),patch.object(relay.urllib.request,'build_opener',return_value=Provider()),patch.object(relay,'HTTPServer',OneRequest),patch.object(relay.time,'time',side_effect=lambda:clock[0]):
                thread=threading.Thread(target=target,daemon=True);thread.start()
                until=time.monotonic()+3
                while not port.exists() and time.monotonic()<until and not errors:time.sleep(.01)
                self.assertEqual(errors,[]);self.assertTrue(port.exists())
                connection=http.client.HTTPConnection('127.0.0.1',int(port.read_text()),timeout=3)
                connection.request('POST','/invoke',canonical(payload),{'Content-Type':'application/json'})
                response=connection.getresponse();status=response.status;body=json.loads(response.read());connection.close();thread.join(3)
                self.assertFalse(thread.is_alive());self.assertEqual(errors,[])
            db=sqlite3.connect(ledger);charge=db.execute('SELECT settled,status FROM charges WHERE id LIKE ?', (stage+':%',)).fetchone();db.close()
            saved=[json.loads(line) for line in (root/'provider-responses.jsonl').read_text().splitlines()]
            return status,body,charge,saved
    def test_actual_q30_loopback_preserves_history_and_known_or_uncertain_charge(self):
        c=p30.models()['generalist']
        raw=dict(model=c['accepted_response_model_ids'][0],provider=c['provider_name'],choices=[dict(finish_reason='stop',message={'content':'invalid JSON'})],usage=dict(prompt_tokens=10,completion_tokens=5,cost=.000004))
        status,body,charge,saved=self.run_boundary(raw,p30_relay)
        self.assertEqual(status,200);self.assertEqual(charge,(4000,'known'));self.assertEqual(body,raw)
        failure=urllib.error.HTTPError('https://provider.invalid',429,'fixture',{},io.BytesIO(b'{"error":{"code":429,"message":"private detail"}}'))
        status,body,charge,saved=self.run_boundary(failure,p30_relay)
        self.assertEqual(status,429);self.assertEqual(charge,(None,'uncertain'));self.assertNotIn('private detail',canonical(saved))

    def test_q304_relay_one_cheap_route_known_and_429_settlement(self):
        c=q30v4.models()['cheap_generative']
        raw=dict(model=c['accepted_response_model_ids'][0],provider=c['provider_name'],choices=[dict(finish_reason='stop',message={'content':'invalid JSON'})],usage=dict(prompt_tokens=10,completion_tokens=5,cost=.000004))
        status,body,charge,saved=self.run_boundary(raw,q30v4_relay)
        self.assertEqual(status,200);self.assertEqual(charge,(4000,'known'))
        failure=urllib.error.HTTPError('https://provider.invalid',429,'fixture',{},io.BytesIO(b'{"error":{"code":429,"message":"private detail"}}'))
        status,body,charge,saved=self.run_boundary(failure,q30v4_relay)
        self.assertEqual(status,429);self.assertEqual(charge,(None,'uncertain'));self.assertEqual(len(saved),1)
        self.assertNotIn('private detail',canonical(saved))

    def test_invalid_action_is_retained_and_known_usage_settled(self):
        c=json.loads((BASE/'models.json').read_text())['models']['generalist']
        raw={'model':c['accepted_response_model_ids'][0],'provider':c['provider_name'],'choices':[{'finish_reason':'stop','message':{'content':'invalid JSON'}}],'usage':{'prompt_tokens':10,'completion_tokens':5,'cost':.00004}}
        status,body,charge,saved=self.run_boundary(raw)
        self.assertEqual(status,200);self.assertEqual(body,raw);self.assertEqual(charge,(40000,'known'));self.assertEqual(saved[0]['response'],raw)
    def test_provider_rejection_retains_status_and_safe_markers(self):
        failure=urllib.error.HTTPError('https://provider.invalid',400,'rejected',{},io.BytesIO(b'{"error":{"message":"Unsupported response_format parameter"}}'))
        status,body,charge,saved=self.run_boundary(failure)
        self.assertEqual(status,502);self.assertEqual(body['http_status'],400);self.assertIn('response_format',body['error_markers']);self.assertEqual(charge[1],'uncertain');self.assertEqual(saved[0]['error'],body)

    def test_429_metadata_is_safe_and_retains_full_reserve_in_both_relays(self):
        for module in (relay,diagnostic_relay):
            with self.subTest(relay=module.__name__):
                failure=urllib.error.HTTPError('https://provider.invalid',429,'fixture',
                    {'Retry-After':'12','X-RateLimit-Remaining':'0','Authorization':'DO_NOT_LOG'},
                    io.BytesIO(b'{"error":{"code":429,"message":"provider DO_NOT_LOG rate limit","metadata":{"error_type":"rate_limit_exceeded","provider_name":"Anthropic","provider_code":"rate_limited","raw":"DO_NOT_LOG"}}}'))
                status,body,charge,saved=self.run_boundary(failure,module)
                self.assertEqual(status,429);self.assertEqual(charge,(None,'uncertain'))
                self.assertEqual(body['retry_after_seconds'],12)
                self.assertEqual(body['provider_error_type'],'rate_limit_exceeded')
                self.assertEqual(body['provider_name'],'Anthropic')
                self.assertEqual(body['rate_remaining'],0)
                self.assertNotIn('DO_NOT_LOG',canonical(saved));self.assertEqual(len(saved),1)

    def test_http200_provider_error_is_a_transport_failure_not_missing_action(self):
        for module in (relay,diagnostic_relay):
            with self.subTest(relay=module.__name__):
                raw={'error':{'code':429,'message':'private detail','metadata':{'error_type':'rate_limit_exceeded'}}}
                status,body,charge,saved=self.run_boundary(raw,module)
                self.assertEqual(status,429);self.assertEqual(body['http_status'],200)
                self.assertEqual(body['error_type'],'provider_body_error')
                self.assertEqual(charge,(None,'uncertain'));self.assertEqual(len(saved),1)
                self.assertNotIn('response',saved[0]);self.assertNotIn('private detail',canonical(saved))

if __name__=='__main__':unittest.main()
