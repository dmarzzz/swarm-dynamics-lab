"""Quorum-only loopback relay. Credentials stay in this local process."""
import argparse,json,os,sqlite3,stat,time,urllib.request,urllib.error
from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler
from qualification import manifest,digest,validate_response,MODEL,SNAPSHOT,PROVIDER,RESERVE

class Budget:
    def __init__(self,path,cap=1.):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS authority (id INTEGER PRIMARY KEY CHECK(id=1), experiment TEXT, cap REAL)')
            db.execute('INSERT OR IGNORE INTO authority VALUES (1,?,?)',('quorum-of-mirrors',cap))
            if db.execute('SELECT experiment,cap FROM authority').fetchone()!=('quorum-of-mirrors',cap):
                raise ValueError('authority_mismatch')
            db.execute('CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, reserved REAL, status TEXT, actual REAL)')
    def reserve(self,rid):
        with sqlite3.connect(self.path,timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            used,count=db.execute('SELECT COALESCE(SUM(reserved),0),COUNT(*) FROM calls').fetchone()
            cap=db.execute('SELECT cap FROM authority').fetchone()[0]
            if used+RESERVE>cap or count>=32:raise ValueError('budget_exhausted')
            db.execute('INSERT INTO calls VALUES (?,?,?,NULL)',(rid,RESERVE,'reserved'))
    def finish(self,rid,status,cost=None):
        with sqlite3.connect(self.path) as db:
            db.execute('UPDATE calls SET status=?,actual=? WHERE id=?',(status,cost,rid))


def metadata_check():
    with urllib.request.urlopen('https://openrouter.ai/api/v1/models/'+MODEL+'/endpoints',timeout=20) as r:
        data=json.load(r)['data']
    endpoints=[e for e in data['endpoints'] if e['provider_name']==PROVIDER and e['status']==0
               and SNAPSHOT in e['name'] and e['context_length']==32000
               and float(e['pricing']['prompt'])<=.000000042 and float(e['pricing']['completion'])==0]
    if len(endpoints)!=1:raise ValueError('route_or_price_unavailable')
    return {'model':MODEL,'snapshot':SNAPSHOT,'provider':PROVIDER,'price_ceiling_verified':True,'checked':time.time()}


def main():
    p=argparse.ArgumentParser();p.add_argument('--credential',type=Path,required=True)
    p.add_argument('--ledger',type=Path,required=True);p.add_argument('--port-file',type=Path,required=True)
    p.add_argument('--authorization',type=Path,required=True);p.add_argument('--deadline',type=float,required=True)
    a=p.parse_args();os.umask(0o077)
    authorization=json.loads(a.authorization.read_text())
    if authorization.get('experiment')!='quorum-of-mirrors' or authorization.get('api_cap_usd')!=1 or not authorization.get('owner_approved'):
        raise ValueError('authorization_missing')
    if stat.S_IMODE(a.credential.stat().st_mode)!=0o600:raise ValueError('credential_permissions')
    metadata_check();budget=Budget(a.ledger)
    allowed={r['id']:r['request_sha256'] for r in manifest()['assignments']}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def reply(self,data):
            raw=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def do_POST(self):
            rid=None;reserved=False
            try:
                if time.time()>a.deadline:raise ValueError('deadline')
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=16000:raise ValueError('request_size')
                data=json.loads(self.rfile.read(size));rid=data['id'];request=data['request']
                if rid not in allowed or digest(request)!=allowed[rid]:raise ValueError('request_not_allowed')
                budget.reserve(rid);reserved=True
                # No raw response, headers or exception text ever leave the relay.
                key=a.credential.read_text().strip()
                req=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',json.dumps(request).encode(),
                    {'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                del key
                with urllib.request.urlopen(req,timeout=30) as response:
                    raw=response.read(1_000_001)
                if len(raw)>1_000_000:raise ValueError('response_size')
                checked=validate_response(json.loads(raw))
                safe={'model':checked['model'],'provider':checked['provider'],'usage':checked['usage'],
                      'answers':{'decision':{'choice':checked['choice'],'probabilities':checked['probabilities']}}}
                budget.finish(rid,'complete',checked['usage']['cost']);self.reply({'ok':True,'response':safe})
            except Exception as exc:
                if reserved:budget.finish(rid,'failed_or_uncertain')
                reason=str(exc) if isinstance(exc,ValueError) and str(exc) in ('route_changed','usage_invalid','choice_invalid','deadline','request_size','request_not_allowed','response_size','budget_exhausted') else type(exc).__name__
                self.reply({'ok':False,'reason':reason,'http_status':exc.code if isinstance(exc,urllib.error.HTTPError) else None})
    server=HTTPServer(('127.0.0.1',0),Handler);a.port_file.write_text(str(server.server_port))
    print('Quorum relay ready; finite 32-request allowlist; isolated $1 ledger',flush=True)
    server.serve_forever()

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('Quorum relay stopped: '+type(exc).__name__,flush=True);raise SystemExit(1)
