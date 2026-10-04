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
from common import canonical
from native import request
from qualification import make_case,probe

class RelayBoundaryTests(unittest.TestCase):
    def run_boundary(self,provider_result):
        models=json.loads((BASE/'models.json').read_text())['models']
        state=make_case(0,development=True);packet=probe(state,0,'generalist')
        payload={'id':'S0-02:generalist:0:0:physical-0','role':'generalist','request':request(models['generalist'],packet['sections'])}
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
            config=root/'config.json';config.write_text(json.dumps({'attempt':'S0-02','allocation':{'host':'fixture'},'authorization':{'deadline':deadline}}))
            port=root/'port';ledger=root/'budget.sqlite';errors=[]
            def target():
                try:relay.serve(config,key,ledger,port)
                except BaseException as exc:errors.append(type(exc).__name__)
            with patch.object(relay,'verify'),patch.object(relay,'verify_public'),patch('launch.source_check'),patch.object(relay,'verify_catalog'),patch('launch.read_json',return_value={}),patch.object(relay.urllib.request,'build_opener',return_value=Provider()),patch.object(relay,'HTTPServer',OneRequest),patch.object(relay.time,'time',side_effect=lambda:clock[0]):
                thread=threading.Thread(target=target,daemon=True);thread.start()
                until=time.monotonic()+3
                while not port.exists() and time.monotonic()<until and not errors:time.sleep(.01)
                self.assertEqual(errors,[]);self.assertTrue(port.exists())
                connection=http.client.HTTPConnection('127.0.0.1',int(port.read_text()),timeout=3)
                connection.request('POST','/invoke',canonical(payload),{'Content-Type':'application/json'})
                response=connection.getresponse();status=response.status;body=json.loads(response.read());connection.close();thread.join(3)
                self.assertFalse(thread.is_alive());self.assertEqual(errors,[])
            db=sqlite3.connect(ledger);charge=db.execute('SELECT settled,status FROM charges').fetchone();db.close()
            saved=[json.loads(line) for line in (root/'provider-responses.jsonl').read_text().splitlines()]
            return status,body,charge,saved
    def test_invalid_action_is_retained_and_known_usage_settled(self):
        c=json.loads((BASE/'models.json').read_text())['models']['generalist']
        raw={'model':c['accepted_response_model_ids'][0],'provider':c['provider_name'],'choices':[{'finish_reason':'stop','message':{'content':'invalid JSON'}}],'usage':{'prompt_tokens':10,'completion_tokens':5,'cost':.00004}}
        status,body,charge,saved=self.run_boundary(raw)
        self.assertEqual(status,200);self.assertEqual(body,raw);self.assertEqual(charge,(40000,'known'));self.assertEqual(saved[0]['response'],raw)
    def test_provider_rejection_retains_status_and_safe_markers(self):
        failure=urllib.error.HTTPError('https://provider.invalid',400,'rejected',{},io.BytesIO(b'{"error":{"message":"Unsupported response_format parameter"}}'))
        status,body,charge,saved=self.run_boundary(failure)
        self.assertEqual(status,502);self.assertEqual(body['http_status'],400);self.assertIn('response_format',body['error_markers']);self.assertEqual(charge[1],'uncertain');self.assertEqual(saved[0]['error'],body)

if __name__=='__main__':unittest.main()
