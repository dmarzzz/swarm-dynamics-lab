"""Local-only credential consumer for an explicitly admitted SOL50 allocation."""
import argparse,hmac,json,sqlite3,time,urllib.request,urllib.error
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
import instrument as i
import native as n
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise ValueError('redirect_refused')
def reserve(db,ident,cost=None):
 with db:
  db.execute('BEGIN IMMEDIATE');count,total=db.execute('SELECT count(*),coalesce(sum(reserved_usd),0) FROM calls').fetchone();cost=i.budget()['per_call_reserved_usd'] if cost is None else cost
  if count>=2400 or total+cost>53.1456+1e-10:raise ValueError('allocation_exhausted')
  db.execute('INSERT INTO calls(id,reserved_usd,status) VALUES(?,?,?)',(ident,cost,'started'))
def validate_payload(payload,allocation):
 ident=payload.get('id','')
 if not any(ident.startswith(prefix+'-') for prefix in allocation['attempts']):raise ValueError('attempt_not_admitted')
 body=n.request(payload['phase'],payload['packet'])
 if payload['request']!=body:raise ValueError('request_changed')
 i.check_wire(body);return body

def serve(credential,capability,ledger,allocation_file,port=18563):
 allocation=json.loads(allocation_file.read_text())
 required={'status':'reserved','model':'openai/gpt-6-sol','model_cap_usd':53.1456,'cumulative_cap_usd':60,'prior_exposure_usd':1.0408920437,'approved_account_verified':True,'exclusive_allocation_verified':True,'public_disclosure_authorized':True,'public_plan_verified':True}
 if any(allocation.get(k)!=v for k,v in required.items()):raise ValueError('allocation_not_admitted')
 if time.time()>=allocation.get('expires_epoch',0):raise ValueError('allocation_expired')
 if not ledger.is_file():raise ValueError('existing_allocated_ledger_required')
 if not credential.is_file() or credential.is_symlink() or credential.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=credential.read_text().strip();cap=capability.read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 opener=urllib.request.build_opener(NoRedirect());db=sqlite3.connect(ledger)
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   result={'error':'relay_rejected','actual_usd':None}
   try:
    if self.path!='/sol50' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    if time.time()>=allocation['expires_epoch']:raise ValueError('deadline')
    length=int(self.headers.get('Content-Length','0'))
    if not 0<length<=25000:raise ValueError('request_bound')
    payload=json.loads(self.rfile.read(length));body=validate_payload(payload,allocation);reserve(db,payload['id'],i.reservation_usd(body))
    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(body,separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
     with opener.open(req,timeout=150) as response:raw=response.read(1_000_001)
     if len(raw)>1_000_000:raise ValueError('response_bound')
     response=json.loads(raw);usage=response.get('usage',{});cost=usage.get('cost')
     known=type(cost) in (int,float) and cost>=0
     result={'error':None if known else 'unknown_cost','actual_usd':cost if known else None,'response':response,'finished_epoch':time.time()}
    except urllib.error.HTTPError as e:
     result={'error':'http_'+str(e.code),'actual_usd':None,'finished_epoch':time.time()};e.close()
    with db:db.execute('UPDATE calls SET status=?,actual_usd=? WHERE id=?',('terminal',result['actual_usd'],payload['id']))
   except Exception as e:result['error']=type(e).__name__
   encoded=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers()
   try:self.wfile.write(encoded)
   except (BrokenPipeError,ConnectionResetError):pass
 server=HTTPServer(('127.0.0.1',port),Handler);server.timeout=1
 print(json.dumps({'status':'ready','model':n.MODEL,'maximum_requests':2400,'allocation_model_cap_usd':53.1456}),flush=True)
 try:
  while time.time()<allocation['expires_epoch'] and not ledger.with_suffix('.stop').exists():server.handle_request()
 finally:server.server_close();db.close()
if __name__=='__main__':
 parser=argparse.ArgumentParser()
 for key in ('credential','capability','ledger','allocation'):parser.add_argument('--'+key,type=Path,required=True)
 args=parser.parse_args()
 try:serve(args.credential,args.capability,args.ledger,args.allocation)
 except Exception as e:print(json.dumps({'status':'blocked','error_class':type(e).__name__}));raise SystemExit(1)
