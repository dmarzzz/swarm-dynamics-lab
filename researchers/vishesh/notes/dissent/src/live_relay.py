"""Study-only credential relay with frozen hashes and one cumulative ledger."""
import argparse,json,sqlite3,time,urllib.request,urllib.error
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
from cases import digest
from jev import validate,response_fingerprint,VALIDATION_CODES
from live_design import SNAPSHOT,frozen_requests

RATE=0.000000042
RESERVE=1_344_000  # nanodollars, maximum 32k input tokens

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k):raise ValueError('redirect_refused')

def reserve(db,key,cap_nano=1_000_000_000,max_calls=500):
    db.execute('BEGIN IMMEDIATE')
    try:
        n,spent=db.execute('SELECT count(*),coalesce(sum(coalesce(actual_nano,reserved_nano)),0) FROM calls').fetchone()
        if n>=max_calls or spent+RESERVE>cap_nano:raise ValueError('budget_exhausted')
        db.execute('INSERT INTO calls(key,status,reserved_nano) VALUES(?,?,?)',(key,'started',RESERVE));db.commit()
    except BaseException:db.rollback();raise

def main(a):
    auth=json.loads(a.authorization.read_text())
    if auth.get('approved') is not True or not 0<auth.get('api_cap_usd',0)<=1 or auth.get('max_calls')!=500:raise ValueError('study_budget_required')
    if a.credential_file.stat().st_mode&0o077:raise ValueError('credential_permissions')
    key=a.credential_file.read_text().strip()
    if not key:raise ValueError('empty_credential')
    opener=urllib.request.build_opener(NoRedirect())
    with opener.open('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=25) as r:meta=json.load(r)['data']
    routes=meta['endpoints']
    if len(routes)!=1:raise ValueError('route_count')
    route=routes[0]
    if route['provider_name']!='TypeSafe' or route['tag']!='typesafe' or route['status']!=0 or SNAPSHOT not in route['name'] or float(route['pricing']['prompt'])>RATE or float(route['pricing']['completion'])!=0 or route['context_length']>32000:raise ValueError('route_price_mismatch')
    if a.stage in ('Q4','S4'):
        from rd4_design import frozen_requests as rd4_requests
        allowed=rd4_requests(a.stage)
    else:allowed=frozen_requests(a.stage)
    db=sqlite3.connect(a.ledger);db.execute('CREATE TABLE IF NOT EXISTS calls(key TEXT PRIMARY KEY,status TEXT,reserved_nano INTEGER,actual_nano INTEGER)');db.commit()
    expires=time.monotonic()+2700;failures=0
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            nonlocal failures
            status=502;body={'error':'relay_failure'};call_key=None;reserved=False;diagnostic=None
            try:
                if self.path!='/decision' or time.monotonic()>expires or failures>=5:raise ValueError('relay_stopped')
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=20000:raise ValueError('request_size')
                req=json.loads(self.rfile.read(length));h=digest(req)
                if h not in allowed or req!=allowed[h]:raise ValueError('request_not_frozen')
                call_key=a.stage+':'+h
                reserve(db,call_key,round(auth['api_cap_usd']*1e9),481 if a.stage in ('Q4','S4') else 500);reserved=True
                data=json.dumps(req,separators=(',',':')).encode()
                wire=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',data,{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                with opener.open(wire,timeout=35) as r:response=json.loads(r.read(200000))
                diagnostic=response_fingerprint(response,req,SNAPSHOT)
                checked=validate(response,req,SNAPSHOT)
                cost=round(checked['cost_usd']*1e9)
                if cost>RESERVE:raise ValueError('cost_above_reservation')
                db.execute('UPDATE calls SET status=?,actual_nano=? WHERE key=?',('completed',cost,call_key));db.commit()
                # No provider text/error bodies escape the relay.
                body={'checked':checked};status=200;failures=0
            except Exception as e:
                failures+=1
                code='http_'+str(e.code) if isinstance(e,urllib.error.HTTPError) else ('duplicate_request' if isinstance(e,sqlite3.IntegrityError) else str(e) if isinstance(e,ValueError) and str(e) in VALIDATION_CODES else type(e).__name__)
                body={'error':code}
                if diagnostic is not None:body['diagnostic']=diagnostic
                if reserved:db.execute('UPDATE calls SET status=? WHERE key=?',('failed',call_key));db.commit()
            encoded=json.dumps(body).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers()
            try:self.wfile.write(encoded)
            except OSError:pass
    server=HTTPServer(('127.0.0.1',18449),Handler);server.timeout=1
    print(json.dumps({'relay':'ready','stage':a.stage,'allowed_requests':len(allowed),'cap_usd':auth['api_cap_usd']}),flush=True)
    try:
        while time.monotonic()<expires:server.handle_request()
    finally:server.server_close();db.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--credential-file',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--authorization',type=Path,required=True);p.add_argument('--stage',choices=['Q0','Q1','S1','D1','Q4','S4'],required=True)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'relay_start_failed':type(e).__name__}));raise SystemExit(1)
