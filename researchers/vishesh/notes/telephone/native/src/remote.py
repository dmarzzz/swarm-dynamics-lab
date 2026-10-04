"""Admitted Linux worker with one-shot in-memory credential receiver. Never auto-restart."""
import argparse,contextlib,fcntl,hashlib,json,os,resource,socket,stat,struct,subprocess,sys,time,urllib.request
from pathlib import Path
from contract import sha,MODEL
from ledger import Ledger
from worker import execute,write
ROOT=Path(__file__).resolve().parents[6]
BASE=Path(__file__).resolve().parents[1]
TLDR='TLDR: Test three-hop native fidelity on eight original clean cases; compare prose, structured handoffs and original-source lookup. Measure supported meaning retention and unsupported additions. This authored diagnostic does not establish AI Village effects or model necessity.'
CONDITION_TLDR={
 'P':'TLDR: Prose-only three-hop handoff of original authored facts; compare structured handoffs using supported retention and unsupported additions; eight development roots, no population claim.',
 'S':'TLDR: Structured claims and source IDs through three fresh hops; compare prose with identical token limits using supported retention and unsupported additions; authored clean-case diagnostic only.',
 'R':'TLDR: Reopen original source records at each hop and return prose; compare handoff-only arms on supported retention and unsupported additions; deliberately greater evidence access, no pure-format claim.'}

def check(config,now=None,host=None):
 now=time.time() if now is None else now;host=socket.gethostname() if host is None else host
 if config.get('study')!='telephone' or config.get('stage')!='A0' or config.get('host')!=host:raise ValueError('scope_host')
 if config.get('owner_scope_ref')!='Telephone owner approval of both scopes, 2026-10-04':raise ValueError('scope_authority')
 if config.get('cap_nano')!=2000000000 or config.get('authority_ref')!='Telephone cumulative default USD2; owner-directed launch 2026-10-04':raise ValueError('budget_authority')
 if not now+90<config.get('deadline',0)<=now+7200:raise ValueError('deadline')
 alloc=config.get('allocation',{})
 if not all(alloc.get(k) is True for k in ('approved_account_match','inventory_match','merged_exclusive_claim','workload_idle')):raise ValueError('allocation')
 if not 0<=now-alloc.get('checked_at',0)<=300 or alloc.get('expires_at',0)<config['deadline']+120:raise ValueError('allocation_stale')
 if alloc.get('claim')!='vishesh-telephone' or alloc.get('operator')!='vishesh/codex-village-fit':raise ValueError('claim')
 if type(alloc.get('infrastructure_reserve_nano')) is not int or not 0<alloc['infrastructure_reserve_nano']<=500000000:raise ValueError('infrastructure_reserve')
 if config.get('central_origin')!='orbital-one' or not config.get('central_start_receipt'):raise ValueError('central_start')
 if config.get('public_page_verified') is not True:raise ValueError('public_page')
 return True

def prepare(config):
 check(config)
 rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 if rev!=config['source_commit']:raise ValueError('source_revision')
 for rel,h in config['file_hashes'].items():
  path=(ROOT/rel).resolve()
  if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest()!=h:raise ValueError('source_hash')
 packet=json.loads((BASE/'a0/packet.json').read_text())
 if sha(packet)!=config['packet_sha256']:raise ValueError('packet_hash')
 url='https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/telephone/native/a0/PLAN.md'
 if config.get('plan_url')!=url:raise ValueError('plan_url')
 raw=url.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/')
 with urllib.request.urlopen(raw,timeout=25) as response:data=response.read()
 if data!=(BASE/'a0/PLAN.md').read_bytes():raise ValueError('public_plan_bytes')
 return packet

def main(config_path,private,check_only=False):
 if not sys.platform.startswith('linux'):raise ValueError('linux_only')
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.umask(0o077)
 for k in list(os.environ):
  if k.startswith(('ANTHROPIC','OPENAI','OPENROUTER','SWARM_MODEL','SWARM_HUB')):os.environ.pop(k)
 os.environ['SWARM_SOURCE']='vishesh/codex-village-fit'
 config=json.loads(config_path.read_text());packet=prepare(config)
 private.mkdir(mode=0o700,parents=True,exist_ok=True)
 if private.stat().st_uid!=os.getuid() or stat.S_IMODE(private.stat().st_mode)!=0o700:raise ValueError('private_directory')
 if check_only:print(json.dumps({'preflight':True,'model_calls':0}));return
 with (private/'A0.lock').open('a+') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if (private/'A0').exists() or (private/'receiver.json').exists():raise ValueError('attempt_exists')
  sys.path[:0]=[str(ROOT/'tooling/agent-experiments'),'/usr/local/lib/swarm',str(ROOT/'researchers/vishesh/notes/experiment-documentation')]
  import swarm_report as sr
  from public_plan import check as check_plan
  from swarm_lab_credentials import validate_payload
  with contextlib.redirect_stderr(open(os.devnull,'w')):
   sr.register('telephone',title='Telephone',description=TLDR,owner='vishesh',url=config['plan_url'],params={'stage':{'type':'str'},'arm':{'type':'str'}},metrics=['valid_outputs','model_calls'],primary_metric='valid_outputs')
  check_plan('telephone',TLDR)
  if any(r.get('params',{}).get('stage')=='A0' for r in sr.runs('telephone',limit=5000)):raise ValueError('prior_hub_attempt')
  path=private/'credential.sock'
  with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as listener:
   listener.bind(str(path));os.chmod(path,0o600);listener.listen(1);listener.settimeout(180)
   write(private/'receiver.json',{'state':'waiting','host':config['host'],'pid':os.getpid(),'created_at':time.time(),'source_commit':config['source_commit'],'packet_sha256':config['packet_sha256']})
   print(json.dumps({'receiver':'ready','host':config['host']}),flush=True)
   with listener.accept()[0] as conn:
    conn.settimeout(30);_,uid,_=struct.unpack('3i',conn.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
    if uid!=os.getuid():raise ValueError('peer')
    data=bytearray()
    while len(data)<=4096:
     chunk=conn.recv(4097-len(data))
     if not chunk:break
     data.extend(chunk)
    if not 0<len(data)<=4096:raise ValueError('credential_size')
    payload=json.loads(data);data[:]=b'\0'*len(data)
    if set(payload)!={'secret','routing'}:raise ValueError('credential_fields')
    validate_payload(payload['secret'])
    import re
    if set(payload['routing'])!={'workspace_id'} or not re.fullmatch(r'wrkspc_[A-Za-z0-9]+',payload['routing']['workspace_id']):raise ValueError('routing')
    prepare(config);key=payload['secret']['SWARM_MODEL_API_KEY'];workspace=payload['routing']['workspace_id'];del payload
    conn.sendall(b'accepted')
  path.unlink(missing_ok=True)
  ledger=Ledger(private/'budget.sqlite',config['cap_nano'],config['authority_ref'])
  ledger.reserve('A0-infrastructure','A0','infrastructure',config['allocation']['infrastructure_reserve_nano'],sha(config['allocation']))
  def api(endpoint,req):
   call=urllib.request.Request('https://api.anthropic.com/v1/'+endpoint,data=json.dumps(req).encode(),headers={'x-api-key':key,'anthropic-workspace-id':workspace,'anthropic-version':'2023-06-01','content-type':'application/json'})
   with urllib.request.urlopen(call,timeout=50) as response:raw=response.read(2*1024**2+1)
   if len(raw)>2*1024**2:raise ValueError('response_size')
   return json.loads(raw)
  def count(req):return api('messages/count_tokens',{k:v for k,v in req.items() if k not in ('temperature','max_tokens')})['input_tokens']
  runs={}
  with contextlib.redirect_stderr(open(os.devnull,'w')):
   for arm in ('P','S','R'):runs[arm]=sr.start('telephone',run='telephone/A0-'+arm,params={'stage':'A0','arm':arm,'roots':8,'hops':3},message=CONDITION_TLDR[arm])
   def report(s):
    for run in runs.values():run.progress(s['valid'],s['assigned'],valid_outputs=s['valid'])
   result=execute(packet,private/'A0',ledger,count,lambda req:api('messages',req),config['deadline'],report)
   for arm,run in runs.items():
    valid=sum(x['status']=='valid' and x['arm']==arm for x in result['assignments'])
    if result['stopped']:run.fail(message='Collection stopped; semantic review and cost reconciliation pending.',valid_outputs=valid)
    else:run.done(message='Collection complete; semantic review pending, no efficacy conclusion.',valid_outputs=valid)
  del key,workspace
  write(private/'exit.json',{'state':'collection_stopped' if result['stopped'] else 'collection_complete','valid':result['valid'],'budget':result['budget'],'semantic_review_complete':False})
  print(json.dumps({'valid':result['valid'],'stopped':result['stopped'],'budget':result['budget']}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--private',type=Path,required=True);p.add_argument('--check-only',action='store_true');a=p.parse_args()
 try:main(a.config,a.private,check_only=a.check_only)
 except Exception as exc:print(json.dumps({'state':'stopped','error_type':type(exc).__name__}));raise SystemExit(1)
