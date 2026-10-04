"""Authenticated local-only frozen-payload relay; secrets never leave this process."""
import argparse,hmac,json,math,os,sqlite3,time,urllib.request,urllib.error
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from contract import MODEL,digest,parse,request,sha
CAP=20.;LEGACY_HOLD=5.;RESERVE=.015;MAX_CALLS=189

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('redirect_refused')

def reserve(path,identity):
    db=sqlite3.connect(path,timeout=30)
    try:
        with db:
            db.execute('BEGIN IMMEDIATE')
            n,used=db.execute('SELECT count(*),coalesce(sum(reserved),0) FROM calls').fetchone()
            if n>=MAX_CALLS or LEGACY_HOLD+used+RESERVE>CAP:raise ValueError('budget')
            db.execute('INSERT INTO calls(id,reserved,status) VALUES(?,?,?)',(identity,RESERVE,'started'))
    finally:db.close()

def decode(d,kind):
    result={'error':None,'raw_text':None,'parsed':None,'usage':None,'actual_usd':None,'served_model':None,'served_provider':None}
    if d.get('model')==MODEL:result['served_model']=MODEL
    if d.get('provider')=='Anthropic':result['served_provider']='Anthropic'
    u=d.get('usage',{});cost=u.get('cost') if isinstance(u,dict) else None
    if isinstance(u,dict) and all(type(u.get(k)) is int and u[k]>=0 for k in ('prompt_tokens','completion_tokens')) and type(cost) in (int,float) and math.isfinite(cost) and cost>=0:
        result['usage']={k:u[k] for k in ('prompt_tokens','completion_tokens')};result['actual_usd']=cost
    choices=d.get('choices',[])
    if isinstance(choices,list) and len(choices)==1:
        text=choices[0].get('message',{}).get('content')
        if isinstance(text,str):result['raw_text']=text;result['parsed']=parse(text,kind)
        result['finish_reason']=choices[0].get('finish_reason') if choices[0].get('finish_reason') in ('stop','length','content_filter') else 'other'
    if result['served_model'] is None or result['served_provider'] is None:result['error']='route_mismatch'
    elif result['usage'] is None:result['error']='usage_missing'
    elif cost>RESERVE or u['prompt_tokens']>8192 or u['completion_tokens']>512:result['error']='usage_bound_exceeded'
    elif result.get('finish_reason')!='stop':result['error']='incomplete_output'
    elif result['parsed'] is None:result['error']='invalid_schema'
    return result

def serve(port,credential,capability,ledger,allowlist,port_file):
    if credential.is_symlink() or credential.stat().st_mode&0o077 or not credential.is_file():raise ValueError('credential_permissions')
    key=credential.read_text().strip();cap=capability.read_text().strip();allowed=json.loads(allowlist.read_text())
    if not key or len(cap)<32 or len(allowed)!=92 or not ledger.exists():raise ValueError('admission')
    with sqlite3.connect(ledger) as db:
        rows=db.execute('SELECT id,status,cost FROM calls').fetchall()
        if len(rows)!=97 or any(r[1]!='terminal' or r[2] is None for r in rows):raise ValueError('prior_ledger_unreconciled')
    responses=ledger.parent/'responses';responses.mkdir(mode=0o700,exist_ok=True)
    opener=urllib.request.build_opener(NoRedirect());deadline=time.monotonic()+1800
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            result={'error':'relay_admission_failure','raw_text':None,'parsed':None,'usage':None,'actual_usd':None};identity=None;reserved=False
            start=time.monotonic()
            try:
                if self.path!='/antsy' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=16_000_000 or time.monotonic()>=deadline:raise ValueError('envelope')
                data=json.loads(self.rfile.read(n));identity=data['assignment'];payload=data['request']
                spec=allowed.get(identity)
                if spec is None:raise ValueError('assignment')
                if spec['stage']=='E2' and not ledger.with_suffix('.v2r-evaluation-enabled').is_file():raise ValueError('qualification_gate')
                im=allowlist.parent/'images'/spec['image']
                if sha(im)!=spec['image_sha256']:raise ValueError('image_changed')
                parent=None
                if spec['kind'] in ('verify','corrupt'):
                    saved=json.loads((responses/(spec['case']+'-literal.json')).read_text())
                    if saved.get('error'):raise ValueError('parent_failed')
                    parent=saved['parsed']
                if digest(payload)!=digest(request(im.read_bytes(),spec['kind'],parent)):raise ValueError('payload_not_frozen')
                reserve(ledger,identity);reserved=True
                req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(payload).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                try:
                    with opener.open(req,timeout=90) as response:raw=response.read(1_000_001)
                    if len(raw)>1_000_000:raise ValueError('response_bound')
                    result=decode(json.loads(raw),spec["kind"])
                except urllib.error.HTTPError as e:
                    result['error']='http_'+str(e.code);result['http_status']=e.code;e.close()
                except Exception:result['error']='transport_or_response_failure'
            except Exception:pass
            finally:
                if reserved:
                    with sqlite3.connect(ledger,timeout=30) as db:db.execute('UPDATE calls SET status=?,cost=? WHERE id=?',('terminal',result.get('actual_usd'),identity))
            result['wall_s']=time.monotonic()-start
            if reserved:
                try:
                    with (responses/(identity+'.json')).open('x') as f:
                        json.dump(result,f);f.flush();os.fsync(f.fileno())
                except OSError:result['error']='receipt_write_failure'
            encoded=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers()
            try:self.wfile.write(encoded)
            except (BrokenPipeError,ConnectionResetError):pass
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler);server.timeout=1
    port_file.write_text(str(server.server_port));print(json.dumps({'ready':True,'max_calls':MAX_CALLS,'legacy_hold_usd':LEGACY_HOLD,'total_cap_usd':CAP}),flush=True)
    try:
        while time.monotonic()<deadline and not ledger.with_suffix('.v2r-stop').exists():server.handle_request()
    finally:server.server_close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=0)
    for name in ('credential','capability','ledger','allowlist','port-file'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();os.umask(0o077)
    try:serve(a.port,a.credential,a.capability,a.ledger,a.allowlist,a.port_file)
    except Exception:raise SystemExit('relay_blocked_see_private_state') from None
