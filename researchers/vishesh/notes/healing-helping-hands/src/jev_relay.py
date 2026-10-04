"""Local credential relay: fixed synthetic allowlist, durable budget, no secret logs."""
import argparse,hashlib,json,sqlite3,time,urllib.request,urllib.error
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from jev import fixtures,request,validate,MODEL,RATE,RESERVE
MAX_NANO=100_000_000
RESERVE_NANO=1_344_000
canonical=lambda x:json.dumps(x,separators=(',',':')).encode()
def reserve(db,digest,max_calls=60,settle=False):
 db.execute('BEGIN IMMEDIATE')
 try:
  query='SELECT count(*),coalesce(sum(CASE WHEN status="completed" THEN round(cost*1000000000) ELSE reserved END),0) FROM calls' if settle else 'SELECT count(*),coalesce(sum(reserved),0) FROM calls'
  n,spent=db.execute(query).fetchone()
  if n>=max_calls or spent+RESERVE_NANO>MAX_NANO:raise RuntimeError('budget_exhausted')
  db.execute('INSERT INTO calls(hash,reserved,status) VALUES(?,?,?)',(digest,RESERVE_NANO,'started'));db.commit()
 except BaseException:db.rollback();raise
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise RuntimeError('redirect_refused')
def serve(credential_file,ledger,mode="qualification"):
 if credential_file.stat().st_mode&0o077:raise PermissionError('credential_mode')
 key=credential_file.read_text().strip()
 if not key:raise ValueError('empty_credential')
 # Unauthenticated official metadata; no credential is sent during pricing discovery.
 with urllib.request.urlopen('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=20) as r:meta=json.load(r)['data']
 routes=meta['endpoints'];assert len(routes)==1 and routes[0]['provider_name']=='TypeSafe' and routes[0]['tag']=='typesafe' and routes[0]['status']==0 and float(routes[0]['pricing']['prompt'])<=RATE and float(routes[0]['pricing']['completion'])==0
 if mode=='pilot-03':
  from reference import new_qualification,corpus
  payloads=[request(x,i,'pilot-03-qualification') for i,x in enumerate(new_qualification())]
  for seed in (8701,8702,8703):
   c=corpus(seed);payloads.extend(request({'claim':c['claims'][d['claim']],'report':d['text']},i,'pilot-03-seed-'+str(seed)) for i,d in enumerate(c['docs']))
 else:payloads=[request(x,i) for i,x in enumerate(fixtures())]
 allowed={hashlib.sha256(canonical(x)).hexdigest() for x in payloads}
 db=sqlite3.connect(ledger);db.execute('CREATE TABLE IF NOT EXISTS calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');db.commit();deadline=time.monotonic()+(2100 if mode=='pilot-03' else 900)
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
    reserve(db,digest,720 if mode=='pilot-03' else 60,settle=mode=='pilot-03')
    req=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',canonical(payload),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with opener.open(req,timeout=25) as response:data=json.loads(response.read(200_000))
    checked=validate(data);db.execute('UPDATE calls SET status=?,cost=? WHERE hash=?',('completed',checked['cost_usd'],digest));db.commit();body=data;status=200
   except Exception as e:
    body={'error_type':type(e).__name__}
    if isinstance(e,urllib.error.HTTPError):body['http_status']=e.code
    print(json.dumps({'relay_failure':body}),flush=True)
    if digest:db.execute("UPDATE calls SET status='failed' WHERE hash=? AND status='started'",(digest,));db.commit()
   encoded=json.dumps(body).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers();self.wfile.write(encoded)
 server=HTTPServer(('127.0.0.1',18443),Handler);server.timeout=1;print('Credential relay ready: frozen '+mode+' payloads only; cumulative USD 0.10 cap.',flush=True)
 try:
  while time.monotonic()<deadline:server.handle_request()
 finally:server.server_close();db.close()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--credential-file',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--mode',choices=['qualification','pilot-03'],default='qualification');a=p.parse_args()
 try:serve(a.credential_file,a.ledger,a.mode)
 except Exception as e:print('Relay failed: '+type(e).__name__);raise SystemExit(1)
