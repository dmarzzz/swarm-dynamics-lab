"""Local-only key consumer. Fixed route, unique IDs, bounded spend, zero retries."""
import argparse,json,os,time,resource,urllib.request,urllib.error
from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import cases
import freshness
from diagnostic_errors import safe_error
from native_provider import validate_wire,MODELS
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**k):return None
def main():
 p=argparse.ArgumentParser();p.add_argument('--credential-file',required=True);p.add_argument('--journal',required=True);p.add_argument('--port-file',required=True);a=p.parse_args()
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));path=Path(a.credential_file);assert not path.is_symlink() and path.stat().st_uid==os.getuid() and not path.stat().st_mode&0o077
 key=path.read_text().strip();assert key and '\n' not in key
 journal=Path(a.journal).open('x');os.chmod(a.journal,0o600);seen=set();counts={m:0 for m in MODELS};reserved=0.;failed=False;deadline=time.time()+3600;opener=urllib.request.build_opener(NoRedirect())
 def record(d):journal.write(json.dumps(d)+'\n');journal.flush();os.fsync(journal.fileno())
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   nonlocal reserved,failed
   status=400;result={'error':'refused'}
   try:
    size=int(self.headers.get('Content-Length','0'));assert self.path=='/invoke' and 0<size<=18000 and not failed and time.time()<deadline
    data=json.loads(self.rfile.read(size));assert set(data)=={'request_id','body'};rid=data['request_id'];assert isinstance(rid,str) and len(rid)==32 and rid not in seen and len(seen)<32
    body=data['body'];validate_wire(body);encoded=json.dumps(body).encode();model=body['model'];assert model==MODELS[1] and counts[model]<32;rate=5;cost=((len(encoded)+512)*rate+512*rate*5)/1e6;assert reserved+cost<=1.771520
    seen.add(rid);counts[model]+=1;reserved+=cost;record({'request_id':rid,'state':'reserved','reserved_usd':cost})
    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',encoded,{'Content-Type':'application/json','Authorization':'Bearer '+key})
    with opener.open(req,timeout=55) as r:raw=r.read(1_000_001)
    assert len(raw)<=1_000_000 and key.encode() not in raw;value=json.loads(raw);result={k:value[k] for k in ['id','model','provider','choices','usage'] if k in value};status=200
    record({'request_id':rid,'state':'response','body':result})
   except urllib.error.HTTPError as e:
    failed=True;status=e.code;result={'error':'provider_http','http_status':e.code,**safe_error(e)};record({'request_id':rid,**result})
   except Exception as e:
    failed=True;status=502;result={'error':type(e).__name__};record(result)
   wire=json.dumps(result).encode();self.send_response(status);self.send_header('Content-Length',str(len(wire)));self.end_headers();self.wfile.write(wire)
 server=HTTPServer(('127.0.0.1',0),Handler);server.timeout=1;Path(a.port_file).write_text(str(server.server_port));print('relay_ready',flush=True)
 try:
  while time.time()<deadline and not failed and len(seen)<32:server.handle_request()
 finally:server.server_close();journal.close();key=''
if __name__=='__main__':main()
