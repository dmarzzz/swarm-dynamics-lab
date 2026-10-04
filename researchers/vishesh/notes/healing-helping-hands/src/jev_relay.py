"""Local credential relay: fixed synthetic allowlist, durable budget, no secret logs."""
import argparse,hashlib,json,sqlite3,time,urllib.request,urllib.error
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from jev import fixtures,request,validate,MODEL,RATE,RESERVE
MAX_NANO=100_000_000
RESERVE_NANO=1_344_000
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def reserve(db,digest):
 db.execute('BEGIN IMMEDIATE')
 try:
  n,spent=db.execute('SELECT count(*),coalesce(sum(reserved),0) FROM calls').fetchone()
  if n>=60 or spent+RESERVE_NANO>MAX_NANO:raise RuntimeError('budget_exhausted')
  db.execute('INSERT INTO calls(hash,reserved,status) VALUES(?,?,?)',(digest,RESERVE_NANO,'started'));db.commit()
 except BaseException:db.rollback();raise
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise RuntimeError('redirect_refused')
def serve(credential_file,ledger):
 if credential_file.stat().st_mode&0o077:raise PermissionError('credential_mode')
 key=credential_file.read_text().strip()
 if not key:raise ValueError('empty_credential')
 # Unauthenticated official metadata; no credential is sent during pricing discovery.
 with urllib.request.urlopen('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=20) as r:meta=json.load(r)['data']
 routes=meta['endpoints'];assert len(routes)==1 and routes[0]['provider_name']=='TypeSafe' and routes[0]['tag']=='typesafe' and routes[0]['status']==0 and float(routes[0]['pricing']['prompt'])<=RATE and float(routes[0]['pricing']['completion'])==0
 allowed={hashlib.sha256(canonical(request(x,i))).hexdigest() for i,x in enumerate(fixtures())}
 db=sqlite3.connect(ledger);db.execute('CREATE TABLE IF NOT EXISTS calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');db.commit();deadline=time.monotonic()+900
 opener=urllib.request.build_opener(NoRedirect())
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   status=502;body={'error_type':'unclassified'};digest=None
   try:
    if self.path!='/decision' or time.monotonic()>deadline:raise ValueError('request_not_allowed')
    length=int(self.headers.get('Content-Length','0'))
    if not 0<length<=3000:raise ValueError('request_size')
    payload=json.loads(self.rfile.read(length));digest=hashlib.sha256(canonical(payload)).hexdigest()
    if digest not in allowed:raise ValueError('request_not_frozen')
    reserve(db,digest)
    req=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',canonical(payload),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with opener.open(req,timeout=25) as response:data=json.loads(response.read(200_000))
    checked=validate(data);db.execute('UPDATE calls SET status=?,cost=? WHERE hash=?',('completed',checked['cost_usd'],digest));db.commit();body=data;status=200
   except Exception as e:
    body={'error_type':type(e).__name__}
    if isinstance(e,urllib.error.HTTPError):body['http_status']=e.code
    print(json.dumps({'relay_failure':body}),flush=True)
    if digest:db.execute("UPDATE calls SET status='failed' WHERE hash=? AND status='started'",(digest,));db.commit()
   encoded=json.dumps(body).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers();self.wfile.write(encoded)
 server=HTTPServer(('127.0.0.1',18443),Handler);server.timeout=1;print('Credential relay ready: frozen synthetic requests only; maximum 60 calls / USD 0.10.',flush=True)
 try:
  while time.monotonic()<deadline:server.handle_request()
 finally:server.server_close();db.close()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--credential-file',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);a=p.parse_args()
 try:serve(a.credential_file,a.ledger)
 except Exception as e:print('Relay failed: '+type(e).__name__);raise SystemExit(1)
