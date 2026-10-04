"""Local credential consumer; funded Q3 authority required before key access. No retries."""
import argparse,hashlib,hmac,json,time,urllib.request,urllib.error
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
import admission as a,contract as c
from q3_runner import verify_original_ledger
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise ValueError('redirect_refused')

def safe_http_error(error):
 """Bounded metadata only: never return provider text, headers or request content."""
 status=error.code if type(error.code) is int and 400<=error.code<=599 else 0
 result={'http_status':status,'category':'unclassified','body_prefix_sha256':None,'body_truncated':None}
 try:
  raw=error.read(8193)
  result['body_truncated']=len(raw)>8192
  result['body_prefix_sha256']=hashlib.sha256(raw[:8192]).hexdigest()
  if len(raw)<=8192:
   try:value=json.loads(raw)
   except (ValueError,UnicodeError):value=None
   code=value.get('error',{}).get('code') if isinstance(value,dict) and isinstance(value.get('error'),dict) else None
   allowed={'invalid_request_error','unsupported_parameter','invalid_json_schema','rate_limit_exceeded','model_not_found','insufficient_quota'}
   if isinstance(code,str) and code in allowed:result['category']=code
 except Exception:result['category']='diagnostic_read_failed'
 finally:error.close()
 return result

def payload_body(payload,receipt,next_index):
 if payload.get('id')!=a.ATTEMPT+'-'+str(next_index).zfill(4) or payload.get('attempt')!=a.ATTEMPT:raise ValueError('call_sequence')
 for field,key in [('source_sha256','source_sha256'),('frozen_packet_sha256','packet_sha256')]:
  if payload.get(field)!=receipt[key]:raise ValueError('source_packet_binding')
 if payload.get('family') not in ('release','failover','delegation'):raise ValueError('family')
 body=c.wire(payload['phase'],payload['family'],payload['packet'])
 if payload.get('request')!=body:raise ValueError('request_changed')
 return body

def serve(receipt_path,grant_path,packet_path,ledger_path,credential,capability):
 receipt=json.loads(Path(receipt_path).read_text());grant=json.loads(Path(grant_path).read_text());packet=json.loads(Path(packet_path).read_text())
 a.validate(receipt,grant,packet,receipt['source_commit']);a.public_check(receipt)
 verify_original_ledger(ledger_path,receipt['relay_ledger_sha256'],local=True)
 # No funded/current admission means no credential file is read.
 credential=Path(credential)
 if not credential.is_file() or credential.is_symlink() or credential.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=credential.read_text().strip();cap=Path(capability).read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 ledger=c.StageLedger(ledger_path,'Q3');opener=urllib.request.build_opener(NoRedirect());deadline=min(time.time()+7200,receipt['claim_until_epoch'],grant['expires_epoch']);stopped=False
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   nonlocal stopped
   result={'error':'rejected','actual_usd':None};started=False;ident=None
   try:
    if stopped or time.time()>=deadline:raise ValueError('stopped_or_deadline')
    if self.path!='/q3' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    size=int(self.headers.get('Content-Length',0))
    if not 0<size<=24000:raise ValueError('payload_bound')
    p=json.loads(self.rfile.read(size));count=ledger.db.execute("SELECT count(*) FROM r3_calls WHERE stage='Q3'").fetchone()[0]
    body=payload_body(p,receipt,count);ident=p['id'];ledger.reserve(ident,body);started=True
    request=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(body,separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
     with opener.open(request,timeout=min(150,max(1,deadline-time.time()))) as response:raw=response.read(1000001)
     if len(raw)>1000000:raise ValueError('response_bound')
     value=json.loads(raw);cost=value.get('usage',{}).get('cost')
     if type(cost) not in (int,float) or cost<0 or cost>float(c.PER_CALL):raise ValueError('cost_contract')
     ledger.settle(ident,cost);result={'error':None,'actual_usd':cost,'response':value,'finished_epoch':time.time()}
    except urllib.error.HTTPError as error:
     diagnostic=safe_http_error(error);result={'error':'http_'+str(diagnostic['http_status']),'actual_usd':None,'finished_epoch':time.time(),'diagnostic':diagnostic};ledger.settle(ident,None);stopped=True
   except Exception as error:
    result={'error':type(error).__name__,'actual_usd':None,'finished_epoch':time.time()};stopped=True
    if started:
     try:ledger.settle(ident,None)
     except ValueError:pass
   encoded=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers()
   try:self.wfile.write(encoded)
   except (BrokenPipeError,ConnectionResetError):stopped=True
 server=HTTPServer(('127.0.0.1',18565),Handler);server.timeout=1
 print(json.dumps({'status':'ready','attempt':a.ATTEMPT,'max_calls':108,'model_cap_usd':a.MODEL_CAP}),flush=True)
 try:
  while not stopped and time.time()<deadline and not Path(str(ledger_path)+'.q3-stop').exists():server.handle_request()
 finally:server.server_close();ledger.db.close()
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('receipt','grant','packet','ledger','credential','capability'):p.add_argument('--'+k,required=True)
 args=p.parse_args()
 try:serve(args.receipt,args.grant,args.packet,args.ledger,args.credential,args.capability)
 except Exception as error:print(json.dumps({'status':'blocked','error_class':type(error).__name__}));raise SystemExit(1)
