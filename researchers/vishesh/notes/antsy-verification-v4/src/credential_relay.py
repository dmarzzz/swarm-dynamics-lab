"""Local-only approved credential consumer. Never logs headers or raw provider errors."""
import argparse,json,os,stat,urllib.error,urllib.request
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from jev import MODEL,SNAPSHOT,PROVIDER,RATE,RESERVE,digest,validate_response

def persist(path,value):
    tmp=path.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(value,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--credential',type=Path,required=True);p.add_argument('--allowlist',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--port-file',type=Path,required=True);a=p.parse_args()
    os.umask(0o077)
    assert stat.S_IMODE(a.credential.stat().st_mode)==0o600
    allowed=set(json.loads(a.allowlist.read_text()))
    # Public metadata gate, no authenticated request yet.
    with urllib.request.urlopen('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=20) as r:meta=json.load(r)['data']
    valid=[e for e in meta['endpoints'] if e['provider_name']==PROVIDER and float(e['pricing']['prompt'])<=RATE and float(e['pricing']['completion'])==0 and e['status']==0]
    assert len(valid)==1 and SNAPSHOT in valid[0]['name']
    ledger=json.loads(a.ledger.read_text()) if a.ledger.exists() else {'experiment':'antsy-verification-v4','limit_usd':5.0,'reserved_usd':0,'actual_usd':0,'calls':{}}
    assert ledger['experiment']=='antsy-verification-v4' and ledger['limit_usd']==5.0
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def respond(self,data,status=200):
            raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def do_POST(self):
            try:
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=8192:raise ValueError('size')
                data=json.loads(self.rfile.read(n));q=data['question'];h=digest(data['state'],q);rid=data['id']
                if h not in allowed or len(rid)!=64 or rid in ledger['calls']:raise ValueError('not_allowed_or_duplicate')
                if len(ledger['calls'])>=976 or ledger['reserved_usd']+RESERVE>ledger['limit_usd']:raise ValueError('budget')
                ledger['reserved_usd']+=RESERVE;ledger['calls'][rid]={'hash':h,'status':'reserved'};persist(a.ledger,ledger)
                payload={'model':MODEL,'provider':{'only':['typesafe'],'allow_fallbacks':False},'state':data['state'],'questions':{'decision':q}}
                # Secret exists only in this process and the authorized HTTPS request.
                key=a.credential.read_text().strip()
                req=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',json.dumps(payload).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                del key
                try:
                    with urllib.request.urlopen(req,timeout=30) as response:result=json.load(response)
                    result=validate_response(result,q['criteria']);ledger['calls'][rid].update(status='complete',cost=result['usage']['cost']);ledger['actual_usd']+=result['usage']['cost'];persist(a.ledger,ledger);self.respond(result)
                except Exception as exc:
                    ledger['calls'][rid].update(status='failed_or_uncertain',error=type(exc).__name__);persist(a.ledger,ledger);self.respond({'error':type(exc).__name__})
            except Exception as exc:self.respond({'error':type(exc).__name__},400)
    server=HTTPServer(('127.0.0.1',0),Handler);a.port_file.write_text(str(server.server_port));print('Antsy credential relay ready; loopback only; finite payload allowlist',flush=True);server.serve_forever()
if __name__=='__main__':main()
