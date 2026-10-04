"""Local credential consumer. The dedicated worker receives no provider secret.

Run only after admission. Connect using an SSH reverse tunnel with host-key checking;
the local persistent ledger is the sole credential-bearing spending authority.
"""
import argparse
import json
import math
import os
import resource
import time
import urllib.error
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from diagnostic_admission import BASE, verify, verify_public
from budget import Budget
from common import canonical, digest, append
from native import reserve_nano, usage_receipt, verify_catalog
from diagnostic import assignments


def validate_payload(data, models):
    if not isinstance(data,dict) or set(data)!={'id','role','request'}:raise ValueError('relay_envelope')
    allowed={a['id']:a['role'] for a in assignments()}
    logical, separator, attempt=data['id'].rpartition(':physical-')
    if not separator or attempt != '0' or logical not in allowed or allowed[logical]!=data['role']:
        raise ValueError('unassigned_request')
    c=models[data['role']];r=data['request']
    if r.get('model')!=c['requested_model_id'] or r.get('provider')!={'only':[c['provider_tag']],'allow_fallbacks':False}:
        raise ValueError('relay_model_route')
    if len(canonical(r).encode())>7500 or not canonical(r).isascii():raise ValueError('relay_input_bound')
    if c['kind']=='chat':
        required={'model','provider','messages','temperature','max_tokens','response_format','stream'}
        if c['provider_tag']=='alibaba':required.add('reasoning')
        if set(r)!=required or r['temperature']!=0 or r['max_tokens']!=1024 or r['response_format']!={'type':'json_object'} or r['stream'] is not False:
            raise ValueError('relay_generation_contract')
        if len(r['messages'])!=1 or set(r['messages'][0])!={'role','content'} or r['messages'][0]['role']!='user':raise ValueError('relay_message_contract')
        if c['provider_tag']=='alibaba' and r['reasoning']!={'enabled':False}:raise ValueError('relay_reasoning')
    else:
        if set(r)!={'model','provider','state','questions'} or set(r['questions'])!={'action'}:raise ValueError('relay_decision_contract')
        q=r['questions']['action']
        if set(q)!={'type','instructions','criteria'} or q['type']!='choice' or not 2<=len(q['criteria'])<=12:raise ValueError('relay_choices')
    return c


def serve(config_path,credential_file,ledger,port_file):
    from diagnostic_launch import NoRedirect, source_check, read_json
    import sys
    config=json.loads(config_path.read_text())
    # Private-fleet/source receipts are also rechecked by the remote worker on its actual hostname.
    verify(config,actual_host=config['allocation']['host']);source_check(config)
    sys.path.insert(0,str(BASE.parent/'experiment-documentation'));import public_plan
    verify_public(config,public_plan.check)
    if credential_file.is_symlink() or credential_file.stat().st_mode&0o077 or credential_file.stat().st_uid!=os.getuid():
        raise ValueError('credential_file_permissions')
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    key=credential_file.read_text().strip()
    if not key or '\n' in key:raise ValueError('credential_format')
    models=json.loads((BASE/'models.json').read_text())['models'];opener=urllib.request.build_opener(NoRedirect())
    for c in models.values():verify_catalog(read_json(opener,c['catalog_url']),c)
    auth=config['authorization']
    budget=Budget(ledger,digest(auth),config['allocation']['host'],1_500_000_000,288,auth['deadline'])
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            if self.path!='/health':self.send_error(404);return
            summary=budget.summary()
            payload=canonical(dict(experiment='poietic-agents',attempt=config['attempt'],source_commit=config['source_commit'],
                assignment_sha256=config['assignment_sha256'],credential_ready=bool(key),deadline=auth['deadline'],
                api_cap_usd=1.5,physical_calls=summary['physical_calls'],api_exposure_usd=summary['charged_upper_usd'])).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
        def do_POST(self):
            status=400;result={'error_type':'request_refused'};reserved=False;physical_id=None
            try:
                size=int(self.headers.get('Content-Length','0'))
                if self.path!='/invoke' or not 0<size<=10000 or time.time()>=auth['deadline']-45:raise ValueError('relay_deadline_or_size')
                data=json.loads(self.rfile.read(size));c=validate_payload(data,models);physical_id=data['id']
                budget.reserve(physical_id,digest(data['request']),reserve_nano(c));reserved=True
                suffix='/api/alpha/decisions' if c['kind']=='decision' else '/api/v1/chat/completions'
                req=urllib.request.Request('https://openrouter.ai'+suffix,canonical(data['request']).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                with opener.open(req,timeout=45) as r:raw=json.loads(r.read(1000000))
                if key in canonical(raw): raise ValueError('credential_in_provider_response')
                result={k:raw[k] for k in ('id','model','provider','choices','answers','usage') if k in raw}
                append(ledger.parent/'provider-responses.jsonl',dict(id=physical_id,attempt=config['attempt'],utc=time.time(),http_status=200,response=result))
                # Billing is independent of action/schema validity. Keep the response for worker diagnosis.
                try:
                    measured=usage_receipt(raw,c)
                    budget.settle(physical_id,math.ceil(measured['cost_usd']*1e9));reserved=False
                except (ValueError,KeyError,TypeError):
                    budget.settle(physical_id);reserved=False
                status=200
            except urllib.error.HTTPError as exc:
                status=429 if exc.code==429 else 502
                result={'error_type':'provider_http','http_status':exc.code}
                try:
                    error=json.loads(exc.read(32000));message=str(error.get('error',{}).get('message','')).lower()
                    result['error_markers']=[word for word in ('response_format','json','model','provider','unsupported','not found','credits','quota','rate','max_tokens','authentication','region','parameter','stream','valid') if word in message]
                except Exception:pass
                append(ledger.parent/'provider-responses.jsonl',dict(id=physical_id,attempt=config['attempt'],utc=time.time(),error=result))
            except Exception as exc:
                safe=str(exc) if isinstance(exc,ValueError) and str(exc).replace('_','').isalnum() else type(exc).__name__
                result={'error_type':type(exc).__name__,'diagnostic_code':safe};status=502 if reserved else 400
                append(ledger.parent/'provider-responses.jsonl',dict(id=physical_id,attempt=config['attempt'],utc=time.time(),error=result))
            finally:
                if reserved:budget.settle(physical_id)
            data=canonical(result).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    server=HTTPServer(('127.0.0.1',0),Handler);server.timeout=1
    port_file.write_text(str(server.server_port));print('Poietic local relay ready; 36 diagnostic IDs, 36 new physical attempts maximum, prior exposure retained, USD 1.50 cumulative API cap.',flush=True)
    try:
        while time.time()<auth['deadline']:server.handle_request()
    finally:server.server_close();budget.close();key=''


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--credential-file',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--port-file',type=Path,required=True)
    a=p.parse_args()
    try:serve(a.config,a.credential_file,a.ledger,a.port_file)
    except Exception as exc:print('Relay blocked: '+type(exc).__name__);raise SystemExit(1)
