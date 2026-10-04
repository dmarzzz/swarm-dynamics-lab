"""Fail-closed SOL50 qualification/conditional pilot runner, no automatic retries."""
import argparse,hashlib,json,os,socket,sqlite3,subprocess,time,urllib.request
from pathlib import Path
import instrument as i
import native as n
import coordinator as c
ROOT=Path(__file__).resolve().parent
EXPERIMENT='swarm-of-theseus-sol50'

def save(path,value):
    with Path(path).open('x') as f:json.dump(value,f,sort_keys=True);f.flush();os.fsync(f.fileno())

def source_hash():return i.digest({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('*.py'))})

def validate(receipt,revision,now=None):
    now=time.time() if now is None else now
    expected={'model':n.MODEL,'reasoning_effort':'none','members':50,'cumulative_cap_usd':60,'prior_exposure_usd':1.0408920437,'model_cap_usd':53.1456,'max_calls':2400,'retries':0,'source_commit':revision,'source_sha256':source_hash(),'approved_account_verified':True,'exclusive_allocation_verified':True,'worker_idle_verified':True,'host_key_verified':True,'ledger_reconciled':True,'public_page_verified':True,'public_disclosure_authorized':True,'runtime_verified':True}
    for key,value in expected.items():
        if receipt.get(key)!=value:raise ValueError('admission_'+key)
    if receipt.get('stage') not in ('qualification','evaluation'):raise ValueError('stage')
    if not 0<=now-receipt.get('verified_epoch',0)<=900:raise ValueError('stale_admission')
    if receipt.get('claim_until_epoch',0)<now+14400:raise ValueError('claim_expiry')
    if receipt.get('stage')=='evaluation' and receipt.get('qualification_passed') is not True:raise ValueError('qualification_required')
    for key in ('host','allocation_id','owner_decision_sha256','allocation_sha256','design_sha256','plan_url','plan_sha256'):
        if not receipt.get(key):raise ValueError('missing_'+key)
    if receipt['plan_sha256']!=hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest():raise ValueError('plan_content')
    expected_url='https://github.com/dmarzzz/swarm-lab/blob/'+revision+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/sol50/PLAN.md'
    if receipt['plan_url']!=expected_url:raise ValueError('immutable_plan')
    return True

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Theseus-SOL50','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=30) as response:data=response.read(10_000_001)
    if len(data)>10_000_000:raise ValueError('public_response_bound')
    return data

def public_check(r):
    state=json.loads(fetch('https://swarm-live.pages.dev/api/state'))
    exp=next((x for x in state['experiments'] if x.get('id')==EXPERIMENT),{})
    if exp.get('url')!=r['plan_url'] or not exp.get('description','').startswith('TLDR: '):raise ValueError('registration')
    raw=r['plan_url'].replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    if hashlib.sha256(fetch(raw)).hexdigest()!=r['plan_sha256']:raise ValueError('public_plan_hash')
    return {'verified_epoch':time.time(),'plan_url':r['plan_url'],'plan_sha256':r['plan_sha256']}

class NativeCalls:
    def __init__(self,root,receipt,ledger):
        self.root=Path(root);self.receipt=receipt;self.ledger=Path(ledger);self.count=0
        if not self.ledger.is_file():raise ValueError('existing_ledger_required')
        self.deadline=min(time.time()+14400,receipt['claim_until_epoch']);self.capability=os.environ['THESEUS_SOL50_RELAY_CAPABILITY']
    def __call__(self,phase,packet):
        body=n.request(phase,packet);encoded=json.dumps(body,separators=(',',':')).encode();i.check_wire(body)
        if time.time()>=self.deadline:raise ValueError('deadline')
        if self.receipt['stage']=='qualification' and self.count>=30:raise ValueError('qualification_call_limit')
        ident=self.receipt['attempt']+'-'+str(self.count).zfill(4);reserve=i.budget()['per_call_reserved_usd']
        with sqlite3.connect(self.ledger) as db:
            db.execute('BEGIN IMMEDIATE')
            count,total=db.execute('SELECT count(*),coalesce(sum(reserved_usd),0) FROM sol50_calls').fetchone()
            if count>=2400 or total+reserve>53.1456+1e-10:raise ValueError('budget')
            db.execute('INSERT INTO sol50_calls(id,reserved_usd,status) VALUES(?,?,?)',(ident,reserve,'started'))
        self.count+=1;save(self.root/(ident+'-request.json'),{'phase':phase,'request':body,'request_sha256':i.digest(body),'reserved_usd':reserve,'started_epoch':time.time()})
        payload=json.dumps({'id':ident,'phase':phase,'packet':packet,'request':body}).encode()
        req=urllib.request.Request('http://127.0.0.1:18564/sol50',payload,{'Authorization':'Bearer '+self.capability,'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req,timeout=min(180,max(1,self.deadline-time.time()))) as response:result=json.load(response)
        except Exception as e:
            save(self.root/(ident+'-response.json'),{'error':type(e).__name__,'unknown_reservation_usd':reserve});raise ValueError('ambiguous_transport') from None
        save(self.root/(ident+'-response.json'),result)
        actual=result.get('actual_usd')
        if result.get('error') or not isinstance(actual,(int,float)) or actual<0 or actual>reserve:raise ValueError('provider_or_cost_stop')
        with sqlite3.connect(self.ledger) as db:db.execute('UPDATE sol50_calls SET status=?,actual_usd=? WHERE id=?',('terminal',actual,ident))
        return n.parse(result['response'])

def qualify(w,call):
    if len(w['members'])!=5:raise ValueError('qualification_population')
    notes,founders=c.initialize(w,call)
    if not all(row['qualified'] for row in founders):return {'passed':False,'founders':founders,'stop':'founder_gate'}
    g=i.Institution(w,'interactive',notes);joint=c.checkpoint(g,0,call)
    if not all(x['valid'] and x['correct']==6 for x in joint['decisions']) or not all(x['route_correct'] for x in joint['selections']) or not all(x['copied_exactly'] for x in joint['witnesses']):return {'passed':False,'founders':founders,'joint':joint,'stop':'joint_gate'}
    owner=w['replacement_order'][0];handover=c.replace(g,owner,call,require_teacher=True);post=c.checkpoint(g,1,call,owners=[owner])
    passed=handover['teacher_semantics_correct'] and handover['note_correct'] and all(x['valid'] and x['correct']==6 for x in post['decisions']) and all(x['route_correct'] for x in post['selections']) and all(x['copied_exactly'] for x in post['witnesses'])
    return {'passed':bool(passed),'founders':founders,'joint':joint,'handover':handover,'post_handover':post}

def run(admission,design,ledger,output):
    r=json.loads(Path(admission).read_text());d=json.loads(Path(design).read_text());revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();validate(r,revision)
    if i.digest(d)!=r['design_sha256']:raise ValueError('design_hash')
    if len(d['world']['members'])!=(5 if r['stage']=='qualification' else 50):raise ValueError('stage_population')
    if socket.gethostname().split('.')[0]!=r['host']:raise ValueError('host')
    if subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise ValueError('dirty_source')
    root=Path(output)
    if root.exists():raise ValueError('attempt_exists_no_resume')
    public=public_check(r);root.mkdir(parents=True);save(root/'manifest.json',{'admission':r,'design':d,'public_preflight':public})
    caller=NativeCalls(root,r,ledger);error=None
    try:
        result=qualify(d['world'],caller) if r['stage']=='qualification' else c.evaluate_world(d['world'],caller)
        save(root/'results.json',result)
    except Exception as e:error=type(e).__name__
    finally:
        save(root/'terminal.json',{'status':'stopped' if error else 'complete','error_class':error,'started_calls':caller.count,'retries':0,'scientific_review':'required','automatic_successor':False})
    print(json.dumps({'status':'stopped' if error else 'complete','started_calls':caller.count,'scientific_review':'required'}))
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for key in ('admission','design','ledger','output'):parser.add_argument('--'+key,required=True)
    args=parser.parse_args()
    try:run(args.admission,args.design,args.ledger,args.output)
    except Exception as e:print(json.dumps({'status':'blocked','error_class':type(e).__name__}));raise SystemExit(1)
