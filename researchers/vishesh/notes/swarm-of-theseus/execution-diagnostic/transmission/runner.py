"""One admitted T1-Q0 attempt; no retries/resume/automatic successors."""
import argparse,hashlib,json,os,resource,socket,sqlite3,subprocess,sys,time,urllib.request
from pathlib import Path
from contextlib import closing
import native as n
import instrument as i

def write(path,value):
    with Path(path).open('x') as f:json.dump(value,f,sort_keys=True);f.flush();os.fsync(f.fileno())
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Theseus-Q0'}),timeout=30) as r:data=r.read(10_000_001)
    if len(data)>10_000_000:raise ValueError('public_response_bound')
    return data.decode()
def public_check(r):
    state=json.loads(fetch('https://swarm-live.pages.dev/api/state'))
    exp=next((x for x in state['experiments'] if x.get('id')==n.EXPERIMENT),{})
    assert exp.get('url')==r['plan_url'] and exp.get('description','').startswith('TLDR: ')
    raw=r['plan_url'].replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    assert hashlib.sha256(fetch(raw).encode()).hexdigest()==r['plan_sha256']
    return {'checked_epoch':time.time(),'plan_url':r['plan_url'],'plan_sha256':r['plan_sha256']}
def validate(r,rev,m,now=None):
    now=time.time() if now is None else now
    required={'attempt':'T1-Q0-A1','experiment':n.EXPERIMENT,'status':'diagnostic-only','source_commit':rev,'instrument_sha256':n.source_hash(),'manifest_sha256':i.digest(m),'max_calls':72,'model_cap_usd':1.70,'infrastructure_cap_usd':.10,'attempt_cap_usd':1.80,'total_authority_usd':25,'prior_exposure_usd':.9793100437,'prior_unknown_usd':.010452,'owner_topup_usd':20,'retries':0,'max_seconds':5400,'exclusive_claim_verified':True,'approved_account_verified':True,'workload_verified':True,'ledger_reconciled':True,'public_page_verified':True,'runtime_verified':True,'host_key_verified':True,'credential_local_only':True,'no_central_dispatch':True,'researcher_review':'not-required-owner-direction'}
    for k,v in required.items():
        if r.get(k)!=v:raise ValueError('admission_'+k)
    for k in ('owner_decision_sha256','runtime_sha256','claim_id','host','allocation_id','allocation_receipt_path','allocation_receipt_sha256'):
        if not r.get(k):raise ValueError('admission_missing_'+k)
    if not 0<=now-r.get('verified_epoch',0)<=900 or r.get('claim_until_epoch',0)<now+5400:raise ValueError('admission_stale')
    if r.get('plan_sha256')!=hashlib.sha256((n.ROOT/'Q0-AUTHORIZED.md').read_bytes()).hexdigest():raise ValueError('plan_hash')
    if r.get('plan_url')!='https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/transmission/Q0-AUTHORIZED.md':raise ValueError('plan_revision')
    if r.get('allocation_id')!='theseus-t1-q0-a1':raise ValueError('allocation_id')
    return True

def reserve(dbpath,cost,deadline):
    if time.time()>=deadline:raise ValueError('deadline')
    with closing(sqlite3.connect(dbpath)) as db,db:
        db.execute('BEGIN IMMEDIATE');used,calls=db.execute('SELECT used,calls FROM budget').fetchone()
        if calls>=72 or used+cost>1.70:raise ValueError('budget')
        db.execute('UPDATE budget SET used=?,calls=?',(used+cost,calls+1))
    return calls+1

def analyze(root):
    root=Path(root);m=json.loads((root/'manifest.json').read_text());statuses={};cost=unknown=0;started=errors=0;founders=successors=0;founder_actions=successor_actions=0;misses=[];audit=[]
    states={}
    for a in m['design']['assignments']:
        p=root/'calls'/(a['id']+'-finished.json');sp=root/'calls'/(a['id']+'-started.json');o=root/'outcomes'/(a['id']+'.json')
        out=json.loads(o.read_text()) if o.exists() else {'status':'missing'};statuses[out['status']]=statuses.get(out['status'],0)+1
        if sp.exists():
            started+=1;start=json.loads(sp.read_text());r=json.loads(p.read_text()) if p.exists() else {'actual_usd':None,'error':'unfinished'}
            if r.get('actual_usd') is None:unknown+=start['reserved_usd']
            else:cost+=r['actual_usd']
            errors+=bool(r.get('error'))
            if i.digest(start['request'])!=start['request_sha256'] or n.wire(start['request'])!=start['wire_request']:audit.append(a['id'])
            if 'score' in out:
                s=n.grade(a,m['design']['worlds'][a['root']],json.loads(start['request']['messages'][0]['content'])['packet'],r.get('value'))
                if s!=out['score']:audit.append(a['id'])
                if a['phase']=='founder':founders+=s['qualified'];founder_actions+=s.get('actions_correct',0)
                if a['phase']=='commit':successors+=s['qualified'];successor_actions+=s.get('actions_correct',0)
                if not s['qualified']:misses.append({'id':a['id'],'phase':a['phase'],'score':s})
    s={'attempt':'T1-Q0-A1','evidence_type':'measured_model_outputs','assigned_calls':72,'started_calls':started,'terminal_calls':sum(1 for _ in (root/'calls').glob('*-finished.json')),'unstarted_calls':72-started,'status_counts':statuses,'founders_qualified':founders,'founders_assigned':18,'successors_qualified':successors,'successors_assigned':18,'founder_correct_actions':founder_actions,'founder_assigned_actions':144,'successor_correct_actions':successor_actions,'successor_assigned_actions':144,'provider_errors':errors,'actual_model_usd':round(cost,10),'unknown_new_usd':round(unknown,10),'prior_exposure_usd':.9793100437,'cumulative_exposure_usd':round(.9793100437+cost+unknown,10),'cumulative_cap_usd':25,'qualification_passed':founders==18 and successors==18 and not errors and not audit,'audit_disagreements':audit,'qualification_misses':misses,'native_cultural_survival_established':False}
    (root/'summary.json').write_text(json.dumps(s,indent=2)+'\n');return s

def run(receipt,designfile,output):
    r=json.loads(Path(receipt).read_text());m=json.loads(Path(designfile).read_text());rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=n.ROOT,text=True).strip();validate(r,rev,m)
    assert socket.gethostname().split('.')[0]==r['host'];assert not subprocess.check_output(['git','status','--porcelain'],cwd=n.ROOT,text=True).strip()
    root=Path(output);assert not root.exists();pub=public_check(r);key=os.environ['THESEUS_RELAY_CAPABILITY'];resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    # One exact allocation was reserved in the existing operator-held cumulative
    # lineage before dispatch. This host receives only its bounded receipt, not a
    # new copy of the total authority. Historical workers remain closed/fenced.
    allocation=json.loads(Path(r['allocation_receipt_path']).read_text())
    assert hashlib.sha256(Path(r['allocation_receipt_path']).read_bytes()).hexdigest()==r['allocation_receipt_sha256']
    assert allocation['id']==r['allocation_id'] and allocation['manifest_sha256']==i.digest(m)
    assert allocation['reserved_usd']==1.8 and allocation['cumulative_cap_usd']==25
    assert allocation['source_commit']==rev and allocation['host']==r['host']
    assert allocation['prior_exposure_usd']==.9793100437 and allocation['owner_decision_sha256']==r['owner_decision_sha256']
    root.mkdir();(root/'calls').mkdir();(root/'outcomes').mkdir();deadline=min(time.time()+5400,r['claim_until_epoch']);quota=root/'quota.sqlite'
    with closing(sqlite3.connect(quota)) as db,db:db.execute('CREATE TABLE budget(used REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(0,0)')
    write(root/'manifest.json',{'design':m,'source_commit':rev,'instrument_sha256':n.source_hash(),'admission':r,'public_preflight':pub})
    sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
    states={};outcomes={};stop=None;pending=None
    def report(kind,a,**kw):
        if not sr.report(kind,n.EXPERIMENT,a['id'],strict=True,**kw):raise ValueError('report_unacknowledged')
    try:
        for a in m['assignments']:
            ident=a['id'];world=m['worlds'][a['root']]
            if any(not outcomes[p]['score']['qualified'] for p in a['depends_on']):
                outcome={'status':'dependency_unstarted','score':{'qualified':False}};outcomes[ident]=outcome;write(root/'outcomes'/(ident+'.json'),outcome);continue
            p=n.packet(a,world,states);body=n.request(a,p);w=n.wire(body);cost=(len(json.dumps(w).encode())+512+5120)/1e6
            tldr=f"TLDR: T1-Q0 root{a['root']} {world['scenario']} role{a['role']} phase{a['phase']}: direct predecessor teaching and unseen behavior; six-root qualification only, no cultural-survival effect."
            report('plan',a,message=tldr,url=r['plan_url']);report('start',a,message=tldr);pending=a
            count=reserve(quota,cost,deadline);write(root/'calls'/(ident+'-started.json'),{'request':body,'request_sha256':i.digest(body),'wire_request':w,'wire_sha256':i.digest(w),'reserved_usd':cost,'started_epoch':time.time(),'call':count})
            result={'value':None,'error':'relay_unavailable','actual_usd':None,'response_received':False,'started_epoch':time.time()}
            try:
                req=urllib.request.Request('http://127.0.0.1:18562/t1',json.dumps({'assignment':ident,'request':body}).encode(),{'Content-Type':'application/json','Authorization':'Bearer '+key})
                with urllib.request.urlopen(req,timeout=min(90,max(1,deadline-time.time()))) as response:result.update(json.load(response))
            except Exception as e:result['error']='relay_'+type(e).__name__
            result['finished_epoch']=time.time();write(root/'calls'/(ident+'-finished.json'),result)
            score=n.grade(a,world,p,result.get('value')) if not result.get('error') else {'valid':False,'qualified':False}
            outcome={'status':'provider_failed' if result.get('error') else 'complete' if score['qualified'] else 'qualification_failed','score':score};write(root/'outcomes'/(ident+'.json'),outcome);outcomes[ident]=outcome
            if score['qualified']:states.setdefault((a['root'],a['role']),{})[a['phase']]=result['value']
            report('fail' if result.get('error') else 'done',a,message=tldr,metrics={'completed_calls':count,'qualified':int(score['qualified'])});pending=None
            if result.get('error') or result.get('actual_usd') is None or result['actual_usd']>cost:raise ValueError('provider_or_accounting_stop')
    except Exception as e:stop=type(e).__name__
    finally:
        for a in m['assignments']:
            p=root/'outcomes'/(a['id']+'.json')
            if not p.exists():write(p,{'status':'unstarted_or_interrupted'})
        reporting=[]
        if pending:
            try:report('fail',pending,message='Attempt stopped; no retries. Evidence retained.')
            except Exception:reporting=[pending['id']]
        write(root/'terminal.json',{'status':'stopped' if stop else 'complete','safe_error_class':stop,'reporting_pending':reporting,'retries':0})
        analyze(root);write(root/'handoff.json',{'scientific_review':'required','next_action':'Audit native misses, finalize, upload/readback, reconcile original ledger, release claim. No automatic successor.'})
    print(json.dumps({'status':'stopped' if stop else 'complete','scientific_review':'required'}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['run','analyze']);p.add_argument('--admission');p.add_argument('--design');p.add_argument('--output',required=True);a=p.parse_args()
    try:
        if a.mode=='run':run(a.admission,a.design,a.output)
        else:print(json.dumps(analyze(a.output)))
    except Exception as e:print(json.dumps({'status':'blocked','safe_error_class':type(e).__name__}));raise SystemExit(1)
