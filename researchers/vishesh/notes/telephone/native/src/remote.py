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
 if config.get('study')!='telephone' or config.get('stage') not in ('A0','V0') or config.get('host')!=host:raise ValueError('scope_host')
 if config.get('stage')=='V0' and config.get('private_transfer_review') is not True:raise ValueError('real_transfer_not_reviewed')
 if config.get('owner_scope_ref')!='Telephone owner approval of both scopes, 2026-10-04':raise ValueError('scope_authority')
 if config.get('cap_nano')!=5000000000 or config.get('authority_ref')!='Telephone owner USD5 cumulative direct OpenRouter authorization, 2026-10-04':raise ValueError('budget_authority')
 if not now+90<config.get('deadline',0)<=now+7200:raise ValueError('deadline')
 alloc=config.get('allocation',{})
 if not all(alloc.get(k) is True for k in ('approved_account_match','inventory_match','merged_exclusive_claim','workload_idle')):raise ValueError('allocation')
 if not 0<=now-alloc.get('checked_at',0)<=300 or alloc.get('expires_at',0)<config['deadline']+120:raise ValueError('allocation_stale')
 if alloc.get('claim')!='vishesh-telephone' or alloc.get('operator')!='vishesh/codex-village-fit':raise ValueError('claim')
 if type(alloc.get('infrastructure_reserve_nano')) is not int or not 0<alloc['infrastructure_reserve_nano']<=500000000:raise ValueError('infrastructure_reserve')
 if config.get('dispatch_authority')!='owner-direct-2026-10-04' or config.get('central_queue_fenced') is not True:raise ValueError('direct_dispatch')
 if config.get('public_page_verified') is not True:raise ValueError('public_page')
 return True

def prepare(config):
 check(config)
 rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 if rev!=config['source_commit']:raise ValueError('source_revision')
 for rel,h in config['file_hashes'].items():
  path=(ROOT/rel).resolve()
  if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest()!=h:raise ValueError('source_hash')
 stage=config['stage']
 if stage=='A0':packet=json.loads((BASE/'a0/packet.json').read_text())
 else:
  packet=json.loads(Path('/srv/swarm/telephone-private/v0-packet.json').read_text())
  receipt=json.loads(Path('/srv/swarm/telephone-private/A0-QUALIFICATION.json').read_text())
  if receipt.get('native_case_screen_passed') is not True or receipt.get('scored')!=72 or receipt.get('model')!=MODEL or receipt.get('source_commit')!=config['source_commit'] or receipt.get('provider')!='openrouter-anthropic':raise ValueError('A0_not_semantically_qualified')
  review=Path('/srv/swarm/telephone-private/A0-semantic-review.json')
  if hashlib.sha256(review.read_bytes()).hexdigest()!=receipt.get('review_sha256'):raise ValueError('qualification_review_hash')
  cohort=json.loads((BASE/'v0/COHORT.json').read_text())
  if sha(packet)!=cohort['packet_sha256'] or config.get('private_transfer_review') is not True:raise ValueError('real_cohort_or_transfer')
 if sha(packet)!=config['packet_sha256']:raise ValueError('packet_hash')
 url='https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/telephone/native/'+stage.lower()+'/PLAN.md'
 if config.get('plan_url')!=url:raise ValueError('plan_url')
 raw=url.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/')
 with urllib.request.urlopen(raw,timeout=25) as response:data=response.read()
 if data!=(BASE/stage.lower()/'PLAN.md').read_bytes():raise ValueError('public_plan_bytes')
 return packet

def main(config_path,private,check_only=False):
 if not sys.platform.startswith('linux'):raise ValueError('linux_only')
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.umask(0o077)
 for k in list(os.environ):
  if k.startswith(('ANTHROPIC','OPENAI','OPENROUTER','SWARM_MODEL','SWARM_HUB')):os.environ.pop(k)
 os.environ['SWARM_SOURCE']='vishesh/codex-village-fit'
 config=json.loads(config_path.read_text());packet=prepare(config);stage=config['stage']
 private.mkdir(mode=0o700,parents=True,exist_ok=True)
 if private.stat().st_uid!=os.getuid() or stat.S_IMODE(private.stat().st_mode)!=0o700:raise ValueError('private_directory')
 if check_only:print(json.dumps({'preflight':True,'model_calls':0}));return
 with (private/(stage+'.lock')).open('a+') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if (private/stage).exists() or (private/(stage+'-receiver.json')).exists():raise ValueError('attempt_exists')
  sys.path[:0]=[str(ROOT/'tooling/agent-experiments'),'/usr/local/lib/swarm',str(ROOT/'researchers/vishesh/notes/experiment-documentation')]
  import swarm_report as sr
  from public_plan import check as check_plan
  with contextlib.redirect_stderr(open(os.devnull,'w')):
   tldr=TLDR if stage=='A0' else 'TLDR: Test three-hop preservation of reported meaning from eight AI Village development records; compare prose, structured handoffs and original-source lookup using critical retention and unsupported assertions. No historical transmission or world-truth claim.'
   sr.register('telephone',title='Telephone',description=tldr,owner='vishesh',url=config['plan_url'],params={'stage':{'type':'str'},'arm':{'type':'str'}},metrics=['valid_outputs','model_calls'],primary_metric='valid_outputs')
  check_plan('telephone',tldr)
  if any(r.get('params',{}).get('stage')==stage for r in sr.runs('telephone',limit=5000)):raise ValueError('prior_hub_attempt')
  path=private/(stage+'-credential.sock')
  with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as listener:
   listener.bind(str(path));os.chmod(path,0o600);listener.listen(1);listener.settimeout(180)
   write(private/(stage+'-receiver.json'),{'state':'waiting','host':config['host'],'pid':os.getpid(),'created_at':time.time(),'source_commit':config['source_commit'],'packet_sha256':config['packet_sha256']})
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
    if set(payload)!={'openrouter_key'} or not isinstance(payload['openrouter_key'],str) or not 16<len(payload['openrouter_key'])<2048 or any(x.isspace() for x in payload['openrouter_key']):raise ValueError('credential_fields')
    prepare(config);key=payload['openrouter_key'];del payload
    conn.sendall(b'accepted')
  path.unlink(missing_ok=True)
  ledger=Ledger(private/'budget.sqlite',config['cap_nano'],config['authority_ref'])
  if ledger.summary()['total_upper_nano']+len(packet['assignments'])*10752001+config['allocation']['infrastructure_reserve_nano']>config['cap_nano']:raise ValueError('whole_stage_budget')
  if not ledger.db.execute("SELECT 1 FROM charges WHERE id='claim-infrastructure'").fetchone():ledger.reserve('claim-infrastructure','claim','infrastructure',config['allocation']['infrastructure_reserve_nano'],sha(config['allocation']))
  from openrouter_provider import generate,count_tokens
  wire_count=0
  def post_json(req):
   nonlocal wire_count
   wire_count+=1
   call=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(req).encode(),headers={'Authorization':'Bearer '+key,'content-type':'application/json'})
   with urllib.request.urlopen(call,timeout=50) as response:raw=response.read(2*1024**2+1)
   if len(raw)>2*1024**2:raise ValueError('response_size')
   obj=json.loads(raw)
   write(private/stage/('wire-response-%03d.json'%wire_count),obj)
   return obj
  runs={}
  with contextlib.redirect_stderr(open(os.devnull,'w')):
   for arm in ('P','S','R'):runs[arm]=sr.start('telephone',run='telephone/'+stage+'-'+arm,params={'stage':stage,'arm':arm,'roots':8,'hops':3},message=CONDITION_TLDR[arm] if stage=='A0' else CONDITION_TLDR[arm].replace('authored','AI Village development').replace('original facts','reported claims'))
   def report(s):
    for run in runs.values():run.progress(s['valid'],s['assigned'],valid_outputs=s['valid'])
   result=execute(packet,private/stage,ledger,count_tokens,lambda req:generate(req,post_json),config['deadline'],report)
   for arm,run in runs.items():
    valid=sum(x['status']=='valid' and x['arm']==arm for x in result['assignments'])
    if result['stopped']:run.fail(message='Collection stopped; semantic review and cost reconciliation pending.',valid_outputs=valid)
    else:run.done(message='Collection complete; semantic review pending, no efficacy conclusion.',valid_outputs=valid)
  del key
  write(private/(stage+'-exit.json'),{'state':'collection_stopped' if result['stopped'] else 'collection_complete','valid':result['valid'],'budget':result['budget'],'semantic_review_complete':False})
  print(json.dumps({'valid':result['valid'],'stopped':result['stopped'],'budget':result['budget']}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--private',type=Path,required=True);p.add_argument('--check-only',action='store_true');a=p.parse_args()
 try:main(a.config,a.private,check_only=a.check_only)
 except Exception as exc:print(json.dumps({'state':'stopped','error_type':type(exc).__name__}));raise SystemExit(1)
