"""C1 local credential boundary, fixed input allowlist and original shared ledger."""
import argparse,sqlite3,time,json,urllib.request,urllib.error,fcntl,os
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from definition import cases,request,wire,digest,SEEDS,LABELS,ATTEMPT,UPSTREAM_TIMEOUT,LEDGER_CALL_CAP
from jev import validate,RATE
from jev_relay import reserve,NoRedirect
from reference import corpus

def safe_error(e):
    data={'error_type':type(e).__name__}
    if isinstance(e,urllib.error.HTTPError):data['http_status']=e.code
    if isinstance(e,urllib.error.URLError):data['cause_type']=type(e.reason).__name__
    return data

def payloads(stage):
    observations=[]
    if stage=='S0':observations=[(c,i,ATTEMPT+'-S0') for i,c in enumerate(cases())]
    elif stage=='S1':
        for s in SEEDS:
            c=corpus(s)
            observations.extend(({'claim':c['claims'][d['claim']],'report':d['text']},i,f'{ATTEMPT}-S1-{s}') for i,d in enumerate(c['docs']))
    else:raise ValueError('unknown_stage')
    return {digest(request(o,i,scope,p)):request(o,i,scope,p) for o,i,scope in observations for p in (None,*LABELS)}

def stored_response(db,h):
    row=db.execute('SELECT body FROM composite_responses WHERE hash=?',(h,)).fetchone()
    return json.loads(row[0]) if row else None

def store_response(db,h,data):
    checked=validate(data)
    # Commit successful response and settled usage atomically before writing to the client.
    with db:
        db.execute('INSERT INTO composite_responses VALUES(?,?)',(h,json.dumps(data)))
        db.execute('UPDATE calls SET status=?,cost=? WHERE hash=?',('completed',checked['cost_usd'],h))

def serve(key_path,ledger,stage,unlink_credential=False):
    # Held for the whole server lifetime, not just each SQLite transaction.
    lock=ledger.with_suffix('.writer.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if key_path.stat().st_mode&0o077:raise PermissionError('credential_mode')
    key=key_path.read_text().strip()
    if unlink_credential:
        if not str(key_path.resolve()).startswith('/dev/shm/'):raise ValueError('credential_not_ephemeral')
        key_path.unlink()
    if not key:raise ValueError('credential_missing')
    with urllib.request.urlopen('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=20) as r:routes=json.load(r)['data']['endpoints']
    if len(routes)!=1 or routes[0]['name']!='TypeSafe | typesafe/jev-1.13-20260917' or routes[0]['status']!=0 or float(routes[0]['pricing']['prompt'])>RATE or float(routes[0]['pricing']['completion'])!=0:raise ValueError('route_changed')
    if not ledger.exists():raise ValueError('original_ledger_required')
    db=sqlite3.connect(ledger);n,cost=db.execute('SELECT count(*),sum(cost) FROM calls').fetchone()
    if n<720 or cost<.013004123:raise ValueError('historical_ledger_missing')
    db.execute('CREATE TABLE IF NOT EXISTS composite_slots(slot TEXT PRIMARY KEY,hash TEXT NOT NULL)');db.execute('CREATE TABLE IF NOT EXISTS composite_responses(hash TEXT PRIMARY KEY,body TEXT NOT NULL)');db.commit()
    allowed=payloads(stage);limit=120 if stage=='S0' else 1200;deadline=time.monotonic()+(900 if stage=='S0' else 3600);opener=urllib.request.build_opener(NoRedirect());calls=0
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            if self.path.startswith('/result/'):
                h=self.path[len('/result/'):]
                if h not in allowed:self.send_error(404);return
                data=stored_response(db,h)
                if data is None:self.send_error(404);return
                b=wire(data);self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
            if self.path!='/health':self.send_error(404);return
            b=wire({'ready':time.monotonic()<deadline,'pid':os.getpid(),'attempt':ATTEMPT,'stage':stage,'seconds_remaining':max(0,deadline-time.monotonic())})
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
        def do_POST(self):
            nonlocal calls
            h=None;status=502
            try:
                if self.path!='/decision' or time.monotonic()>=deadline or calls>=limit:raise ValueError('stage_limit')
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=5000:raise ValueError('size')
                p=json.loads(self.rfile.read(length));h=digest(p)
                if h not in allowed:raise ValueError('payload_not_frozen')
                cached=stored_response(db,h)
                if cached is not None:
                    b=wire(cached);self.send_response(200);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b);return
                slot=p['session_id']+('-composite' if 'qwen_proposal' in p['state'] else '-jev')
                # Slot is committed first: uncertainty fails closed, never alternate-proposal retries.
                db.execute('INSERT INTO composite_slots VALUES(?,?)',(slot,h));db.commit()
                reserve(db,h,LEDGER_CALL_CAP,settle=True);calls+=1
                # session_id is request namespace only, not model-visible state.
                with opener.open(urllib.request.Request('https://openrouter.ai/api/alpha/decisions',wire(p),{'Authorization':'Bearer '+key,'Content-Type':'application/json'}),timeout=UPSTREAM_TIMEOUT) as r:data=json.loads(r.read(200000))
                store_response(db,h,data);status=200
            except Exception as e:
                data=safe_error(e)
                if h:db.execute("UPDATE calls SET status='failed' WHERE hash=? AND status='started'",(h,));db.commit()
                print(json.dumps({'relay_error':data}),flush=True)
            b=wire(data)
            try:
                self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
            except (BrokenPipeError,ConnectionResetError):
                print(json.dumps({'relay_client_disconnected':True,'request_reserved':h is not None}),flush=True)
    server=HTTPServer(('127.0.0.1',18443),Handler);server.timeout=1
    print(json.dumps({'ready':True,'stage':stage,'historical_calls':n,'historical_cost':cost,'stage_call_cap':limit,'cumulative_cap_usd':.1}),flush=True)
    try:
        while time.monotonic()<deadline:server.handle_request()
    finally:server.server_close();db.close();lock.close()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--credential-file',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--stage',choices=['S0','S1'],required=True);p.add_argument('--unlink-credential',action='store_true');a=p.parse_args()
    try:serve(a.credential_file,a.ledger,a.stage,a.unlink_credential)
    except Exception as e:print(json.dumps({'startup_failure':type(e).__name__}));raise SystemExit(1)
