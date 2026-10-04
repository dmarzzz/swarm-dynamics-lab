"""Local-only finite request relay. Original remote SQLite remains budget authority.

Persisted dispatch IDs prevent replay; this receipt is not a second spending ledger.
No key or arbitrary provider error is returned to worker, logs or transcript.
"""
import argparse,json,os,resource,threading,time,urllib.request,urllib.error
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from native import payload,SCHEMA
from run_outage import assignments
from openrouter_route import MODEL,ROUTE

def allowed_calls():
    return {f"{r['id']}/{tick}/{actor}" for r in assignments() if r['arm']!='scheduled' for tick in range(8) for actor in range(1 if r['arm']=='single' else 4)}

def contracts(scope):
    if scope=='outage-o2':
        from run_outage_o2 import assignments as o2_assignments
        return {f"{r['id']}/{tick}/{actor}":payload([],1024)['response_format'] for r in o2_assignments() if r['arm']!='scheduled' for tick in range(8) for actor in range(r['n'])},1024,24000
    if scope=='outage-o1':return {rid:payload([])['response_format'] for rid in allowed_calls()},512,12000
    from tasks import generate
    from response_contract import schema_for
    rows=json.loads((Path(__file__).resolve().parents[2]/'results/q-a7-preparation/planned-manifest.json').read_text())['assignments']
    result={}
    for row in rows:
        public=generate(row['family'],row['structure'],row['root'],width=16).public
        for phase,item in [('plan',None),('plan_repair',None),('integrate',None)]+[('work',i) for i in public['items']]:
            result[f"{row['id']}/0/{phase}/{item or '-'}"]={'type':'json_schema','json_schema':{'name':'swarm_response','strict':True,'schema':schema_for(public,phase,item)}}
    if len(result)!=152:raise ValueError('q7_manifest_changed')
    return result,4096,48000

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('redirect_rejected')

def main():
    p=argparse.ArgumentParser();p.add_argument('--credential',type=Path,required=True);p.add_argument('--port-file',type=Path,required=True);p.add_argument('--dispatch-log',type=Path,required=True);p.add_argument('--expires',type=float,required=True);p.add_argument('--scope',choices=['outage-o1','outage-o2','q-a7'],default='outage-o1');a=p.parse_args()
    os.umask(0o077);resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    if a.credential.is_symlink() or a.credential.stat().st_mode&0o077 or a.credential.stat().st_uid!=os.getuid():raise ValueError('credential_permissions')
    opener=urllib.request.build_opener(NoRedirect())
    with opener.open('https://openrouter.ai/api/v1/models/anthropic/claude-haiku-4.5/endpoints',timeout=20) as r:catalog=json.load(r)['data']
    endpoints=[e for e in catalog['endpoints'] if e['provider_name']=='Anthropic' and e.get('tag')=='anthropic']
    if len(endpoints)!=1:raise ValueError('catalog_ambiguous')
    e=endpoints[0]
    if '20251001' not in e['name'] or e['status']!=0 or float(e['pricing']['prompt'])>.000001 or float(e['pricing']['completion'])>.000005 or not {'structured_outputs','response_format'}<=set(e['supported_parameters']):raise ValueError('catalog_changed')
    key=a.credential.read_text().strip()
    if not key or '\n' in key:raise ValueError('credential_format')
    if a.dispatch_log.exists():raise ValueError('relay_already_started')
    log=a.dispatch_log.open('x');allowed,max_tokens,max_bytes=contracts(a.scope);seen=set();lock=threading.Lock();stopped=threading.Event()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            result={'ok':False,'failure':'transport_failed'}
            try:
                size=int(self.headers.get('Content-Length','0'))
                if self.path!='/invoke' or not 0<size<=max_bytes+500 or time.time()+120>a.expires:raise ValueError('request_bound')
                data=json.loads(self.rfile.read(size));rid=data['id'];body=data['request']
                if set(data)!={'id','request'} or rid not in allowed:raise ValueError('unassigned_call')
                if set(body)!=set(payload([])) or body.get('model')!=MODEL or body.get('provider')!=ROUTE or body.get('max_tokens')!=max_tokens or body.get('temperature')!=0 or body.get('stream') is not False or body.get('response_format')!=allowed[rid] or len(json.dumps(body).encode())>max_bytes:raise ValueError('payload_contract')
                with lock:
                    if rid in seen or stopped.is_set():raise ValueError('replay_or_stop')
                    seen.add(rid);log.write(json.dumps({'id':rid,'dispatched_epoch':time.time()})+'\n');log.flush();os.fsync(log.fileno())
                request=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(body).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                with opener.open(request,timeout=100) as response:raw=response.read(3_000_001)
                if len(raw)>3_000_000 or key.encode() in raw:raise ValueError('response_rejected')
                d=json.loads(raw)
                if 'error' in d:raise ValueError('provider_error_body')
                choice=d['choices'][0]
                result={'ok':True,'text':choice['message']['content'],'finish_reason':choice['finish_reason'],'model':d.get('model'),'provider':d.get('provider'),'usage':d.get('usage',{})}
            except urllib.error.HTTPError as exc:
                result={'ok':False,'failure':'http_'+str(exc.code)};exc.close();stopped.set()
            except Exception:stopped.set()
            raw=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.timeout=1
    a.port_file.write_text(str(server.server_port));print('Local OpenRouter relay ready; finite '+a.scope+' IDs; no worker credential.',flush=True)
    while time.time()<a.expires:server.handle_request()
    server.server_close();log.close()

if __name__=='__main__':
    try:main()
    except Exception as exc:print('Relay stopped: '+type(exc).__name__);raise SystemExit(2)
