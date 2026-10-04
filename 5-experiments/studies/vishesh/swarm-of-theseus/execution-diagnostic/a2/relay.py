"""Local-only frozen A2 relay. Credential stays on the operator machine."""
import argparse,hashlib,hmac,json,os,sqlite3,time,urllib.request,urllib.error
from contextlib import closing
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from design import assignments,execution_request,MAPPINGS
from openrouter import wire,decode

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def allowlist():
    return {a['id']:{digest(a['request'])} if a['kind']=='learn' else {digest(execution_request(a,dict(zip('AB',m)))) for m in MAPPINGS} for a in assignments()}

def reserve(db,ident,cost):
    with db:
        db.execute('BEGIN IMMEDIATE')
        n,used=db.execute('SELECT count(*),coalesce(sum(reserved),0) FROM calls').fetchone()
        if n>=204 or used+cost>2.5:raise ValueError('budget')
        db.execute('INSERT INTO calls(id,reserved,status) VALUES(?,?,?)',(ident,cost,'started'))

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**kw):raise ValueError('redirect_refused')

def serve(port,credential,capability,ledger):
    assert credential.is_file() and not credential.is_symlink() and credential.stat().st_mode&0o077==0
    assert not ledger.exists()
    key=credential.read_text().strip();assert key
    cap=capability.read_text().strip();assert len(cap)>=32
    allowed=allowlist();opener=urllib.request.build_opener(NoRedirect());deadline=time.monotonic()+7200
    with closing(sqlite3.connect(ledger)) as db:
        db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved REAL,status TEXT,cost REAL)');db.commit()
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                result={'value':None,'raw_text':None,'error':'relay_rejected','actual_usd':None,'usage':None,'response_received':False};ident=None
                try:
                    if self.path!='/a2' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
                    if time.monotonic()>=deadline:raise ValueError('deadline')
                    size=int(self.headers.get('Content-Length','0'))
                    if not 0<size<=20000:raise ValueError('size')
                    p=json.loads(self.rfile.read(size));ident=p['assignment'];body=p['request']
                    if digest(body) not in allowed.get(ident,set()):raise ValueError('not_frozen')
                    w=wire(body);encoded=json.dumps(w).encode();cost=(len(encoded)+512+6000)/1e6
                    reserve(db,ident,cost)
                    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',encoded,{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                    try:
                        with opener.open(req,timeout=45) as response:raw=response.read(1_000_001)
                        if len(raw)>1_000_000:raise ValueError('response_bound')
                        result=decode(json.loads(raw))
                    except urllib.error.HTTPError as e:
                        result['error']='http_'+str(e.code);result['http_status']=e.code
                        # Discard arbitrary provider body; typed internal metadata is not an actor answer.
                        from provider_diagnostics import http_failure
                        result.update(http_failure(e,time.time()));e.close()
                    with db:db.execute('UPDATE calls SET status=?,cost=? WHERE id=?',('terminal',result['actual_usd'],ident))
                except Exception:
                    result['error']='relay_transport_or_admission_failure'
                result['finished_epoch']=time.time();encoded=json.dumps(result).encode()
                self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers()
                try:self.wfile.write(encoded)
                except (BrokenPipeError,ConnectionResetError):pass
        server=HTTPServer(('127.0.0.1',port),Handler);server.timeout=1
        print(json.dumps({'status':'ready','max_calls':204,'cap_usd':2.5,'credential_on_host':False}),flush=True)
        try:
            while time.monotonic()<deadline and not ledger.with_suffix('.stop').exists():server.handle_request()
        finally:server.server_close()
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--port',type=int,required=True);a.add_argument('--credential',type=Path,required=True);a.add_argument('--capability',type=Path,required=True);a.add_argument('--ledger',type=Path,required=True);p=a.parse_args()
    try:serve(p.port,p.credential,p.capability,p.ledger)
    except Exception as e:print(json.dumps({'status':'blocked','error_class':type(e).__name__}));raise SystemExit(1)
