"""Bounded dynamic T1-Q0 relay; local credential never leaves this machine."""
import argparse,hmac,json,sqlite3,time,urllib.request,urllib.error
from contextlib import closing
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import native as n
import instrument as i

def reserve(db,ident,cost):
    with db:
        db.execute('BEGIN IMMEDIATE');count,total=db.execute('SELECT count(*),coalesce(sum(reserved),0) FROM calls').fetchone()
        if count>=72 or total+cost>1.70:raise ValueError('budget')
        db.execute('INSERT INTO calls VALUES(?,?,?,?)',(ident,cost,'started',None))
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kw):raise ValueError('redirect_refused')
def serve(port,credential,capability,ledger):
    assert credential.is_file() and not credential.is_symlink() and credential.stat().st_mode&0o077==0
    assert not ledger.exists();key=credential.read_text().strip();cap=capability.read_text().strip();assert key and len(cap)>=32
    allowed={a['id']:a for a in i.qualification_manifest()['assignments']};deadline=time.monotonic()+5400
    opener=urllib.request.build_opener(NoRedirect())
    with closing(sqlite3.connect(ledger)) as db:
        db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved REAL,status TEXT,cost REAL)');db.commit()
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                r={'value':None,'raw_text':None,'error':'relay_rejected','actual_usd':None,'usage':None,'response_received':False}
                try:
                    if self.path!='/t1' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
                    if time.monotonic()>=deadline:raise ValueError('deadline')
                    size=int(self.headers.get('Content-Length','0'))
                    if not 0<size<=20000:raise ValueError('size')
                    p=json.loads(self.rfile.read(size));a=allowed[p['assignment']];body=p['request'];n.validate_request(a,body)
                    encoded=json.dumps(n.wire(body)).encode();cost=(len(encoded)+512+5120)/1e6;reserve(db,a['id'],cost)
                    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',encoded,{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                    try:
                        with opener.open(req,timeout=60) as response:raw=response.read(1_000_001)
                        if len(raw)>1_000_000:raise ValueError('response_bound')
                        r=n.decode(json.loads(raw))
                    except urllib.error.HTTPError as e:
                        from provider_diagnostics import http_failure
                        r.update(http_failure(e,time.time()));r['error']='http_'+str(e.code);e.close()
                    with db:db.execute('UPDATE calls SET status=?,cost=? WHERE id=?',('terminal',r['actual_usd'],a['id']))
                except Exception:r['error']='relay_transport_or_admission_failure'
                r['finished_epoch']=time.time();body=json.dumps(r).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers()
                try:self.wfile.write(body)
                except (BrokenPipeError,ConnectionResetError):pass
        server=HTTPServer(('127.0.0.1',port),Handler);server.timeout=1
        print(json.dumps({'status':'ready','max_calls':72,'cap_usd':1.70,'credential_on_host':False}),flush=True)
        try:
            while time.monotonic()<deadline and not ledger.with_suffix('.stop').exists():server.handle_request()
        finally:server.server_close()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,required=True)
    for flag in ('credential','capability','ledger'):p.add_argument('--'+flag,type=Path,required=True)
    a=p.parse_args()
    try:serve(a.port,a.credential,a.capability,a.ledger)
    except Exception as e:print(json.dumps({'status':'blocked','error_class':type(e).__name__}));raise SystemExit(1)
