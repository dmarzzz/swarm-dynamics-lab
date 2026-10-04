"""B2 reserved native packet; operator admission/transport are explicit inputs.

No credential discovery, allocation, retry, or model fallback. CLI exceptions
print only their type. Qualification requires saved-response semantic review.
"""
import argparse, hashlib, importlib.util, json, os, time
from pathlib import Path
from decimal import Decimal, ROUND_CEILING
from corpus import canonical
from prepare import ROOT, base, request

PER=31744001
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def file_sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    with Path(p).open('x') as f:
        json.dump(x,f,indent=2);f.flush();os.fsync(f.fileno())

def packet():
    manifest=json.loads((ROOT/'prepared/manifest.json').read_text())
    for name,digest in manifest.items():
        if file_sha(ROOT/name)!=digest:raise ValueError('source_mismatch')
    load=lambda n:json.loads((ROOT/'prepared'/n).read_text())
    return {'actors':load('actor-packets.json'),'assignments':load('assignments.json'),
            'qualification':load('qualification-actor.json'),'envelope':load('envelope.json'),
            'manifest_sha256':file_sha(ROOT/'prepared/manifest.json')}

def normalize(raw,bound):
    if not isinstance(raw,dict) or raw.get('model')!=base.MODEL or raw.get('provider')!='OpenAI' or raw.get('error') or not isinstance(raw.get('id'),str) or not raw['id']:raise ValueError('route')
    choices=raw.get('choices');u=raw.get('usage',{})
    if not isinstance(choices,list) or len(choices)!=1:raise ValueError('choices')
    c=choices[0];m=c.get('message',{})
    if c.get('finish_reason')!='stop' or m.get('role')!='assistant' or any(m.get(k) for k in ('tool_calls','function_call','reasoning','reasoning_details','refusal')):raise ValueError('completion')
    inp,out=u.get('prompt_tokens'),u.get('completion_tokens')
    if type(inp)is not int or not 0<inp<=bound<=base.MAX_INPUT or type(out)is not int or not 0<out<=base.MAX_OUTPUT or type(u.get('total_tokens'))is not int or u['total_tokens']!=inp+out:raise ValueError('usage')
    details=u.get('completion_tokens_details') or {};pd=u.get('prompt_tokens_details') or {}
    if any(details.get(k,0)!=0 for k in ('reasoning_tokens','audio_tokens')) or any(pd.get(k,0)!=0 for k in ('audio_tokens','video_tokens','cache_write_tokens')):raise ValueError('extra_usage')
    cached=pd.get('cached_tokens',0)
    if type(cached)is not int or not 0<=cached<=inp or u.get('is_byok',False)is not False:raise ValueError('billing_route')
    if isinstance(u.get('cost'),bool) or u.get('cost')is None:raise ValueError('cost')
    cost=Decimal(str(u['cost']))
    if not cost.is_finite() or cost<0:raise ValueError('cost')
    nano=int((cost*1000000000).to_integral_value(rounding=ROUND_CEILING))
    if nano>inp*2000+out*10000+1:raise ValueError('price')
    return base.parse(m.get('content')),{'input_tokens':inp,'output_tokens':out,'cached_input_tokens':cached,'cost_nano':nano,'generation_id':raw['id']}

def check_admission(p,a,ledger,transport_path):
    now=time.time()
    if a.get('stage')!='B2' or a.get('manifest_sha256')!=p['manifest_sha256'] or a.get('model')!=base.MODEL:raise ValueError('admission_scope')
    if not a.get('pi_decision_id') or a.get('additional_cap_nano')!=4884624146 or a.get('cumulative_cap_nano')!=5000000000:raise ValueError('allocation')
    if not now<a.get('deadline',0)<=now+5400 or not a['deadline']<=a.get('claim_expires',0):raise ValueError('admission_time')
    if not isinstance(a.get('public_plan_url'),str) or not a['public_plan_url'].startswith('https://'):raise ValueError('public_plan')
    for k in ('portfolio_reserved','public_plan_verified','condition_tldrs_registered','account_verified','exclusive_claim_verified','worker_idle_verified','runtime_verified'):
        if a.get(k)is not True:raise ValueError(k)
    if a.get('transport_sha256')!=file_sha(transport_path):raise ValueError('transport_source')
    # Existing external allocation reserve is counted once, never added again here.
    infra=ledger.db.execute('SELECT reserve,actual,status,kind FROM charges WHERE id=?',(a.get('infrastructure_reservation_id'),)).fetchone()
    if not infra or infra[2]!='reserved' or infra[3]!='infrastructure' or not 0<infra[0]<=250000000:raise ValueError('infrastructure_reserve')
    if ledger.db.execute("SELECT 1 FROM charges WHERE stage!='B2' AND kind='model' AND status!='known'").fetchone():raise ValueError('prior_unknown_model_cost')

def ids(p):return ['q01','q02']+[r['id'] for r in p['assignments']]

def reserve_packet(p,ledger):
    db=ledger.db;db.execute('BEGIN IMMEDIATE')
    try:
        if db.execute("SELECT 1 FROM charges WHERE stage='B2'").fetchone():raise ValueError('already_reserved')
        total=db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserve)),0) FROM charges').fetchone()[0]
        cap=db.execute('SELECT cap FROM authority').fetchone()[0]
        if len(ids(p))!=146 or total+146*PER>min(cap,5000000000):raise ValueError('budget')
        for cid in ids(p):db.execute('INSERT INTO charges VALUES (?,?,?,?,NULL,?,?)',('B2:'+cid,'B2','model',PER,'reserved',p['manifest_sha256']))
        db.commit()
    except Exception:db.rollback();raise

def perform(cid,req,out,ledger,generate,deadline):
    if time.time()+60>=deadline:raise ValueError('deadline')
    bound=len(canonical(req).encode())+1024
    if bound>base.MAX_INPUT:raise ValueError('input_bound')
    row=ledger.db.execute('SELECT reserve,status FROM charges WHERE id=?',('B2:'+cid,)).fetchone()
    if row!=(PER,'reserved'):raise ValueError('not_reserved')
    name=cid.replace(':','_');write(out/(name+'.request.json'),req)
    started=time.time();write(out/(name+'.started.json'),{'started_at':started,'request_sha256':sha(req)})
    try:
        raw=generate(req);write(out/(name+'.response.json'),raw)
        obj,usage=normalize(raw,bound);ledger.settle('B2:'+cid,usage['cost_nano'])
    except Exception:
        ledger.settle('B2:'+cid,None);raise
    return obj,{'status':'valid','started_at':started,'latency_seconds':time.time()-started,'request_sha256':sha(req),'response_sha256':sha(raw),'decision':obj['decision'],**usage}

def qualify(p,out,ledger,generate,deadline):
    out.mkdir(mode=0o700,parents=True,exist_ok=False);write(out/'packet.json',p)
    reserve_packet(p,ledger);rows=[]
    for cid in ('q01','q02'):
        try:
            _,row=perform(cid,request('P',p['qualification'][cid]),out,ledger,generate,deadline)
            rows.append({'id':cid,**row})
        except Exception as e:
            rows.append({'id':cid,'status':'failed','failure_type':type(e).__name__});break
    write(out/'qualification-summary.json',{'rows':rows,'semantic_review_complete':False,'budget':ledger.summary()})
    return rows

def review_qualification(p,out,review):
    if review.get('manifest_sha256')!=p['manifest_sha256'] or not review.get('assessor'):raise ValueError('qualification_review')
    gold=json.loads((ROOT/'prepared/qualification-gold.json').read_text())
    generations=set()
    for cid in ('q01','q02'):
        raw=json.loads((out/(cid+'.response.json')).read_text());req=json.loads((out/(cid+'.request.json')).read_text())
        if req!=request('P',p['qualification'][cid]):raise ValueError('qualification_request')
        obj,usage=normalize(raw,len(canonical(req).encode())+1024);r=review.get('responses',{}).get(cid,{})
        if usage['generation_id'] in generations:raise ValueError('duplicate_qualification_generation')
        generations.add(usage['generation_id'])
        if obj['decision']!=gold[cid] or r.get('response_sha256')!=sha(raw) or r.get('decision_rule_preserved')is not True or r.get('uncertainty_preserved')is not True or not r.get('rationale'):raise ValueError('qualification_not_passed')

def main_run(p,out,ledger,generate,deadline,review):
    if json.loads((out/'packet.json').read_text())!=p:raise ValueError('attempt_packet_mismatch')
    review_qualification(p,out,review)
    write(out/'main-start.json',{'manifest_sha256':p['manifest_sha256'],'review_sha256':sha(review)})
    write(out/'qualification-review.json',review)
    parents={};parent_hash={};rows=[];stopped=False
    for a in p['assignments']:
        row={**a,'status':'unstarted'};rows.append(row)
        if stopped:continue
        try:
            previous=None if a['parent']is None else parents[a['parent']]
            req=request(a['arm'],p['actors'][a['case_id']],previous)
            obj,receipt=perform(a['id'],req,out,ledger,generate,deadline)
            row.update(receipt,parent_response_sha256=None if a['parent']is None else parent_hash[a['parent']])
            parents[a['id']]=obj;parent_hash[a['id']]=receipt['response_sha256']
        except Exception as e:row.update(status='failed',failure_type=type(e).__name__);stopped=True
        write(out/(a['id'].replace(':','_')+'.receipt.json'),row)
    summary={'rows':rows,'valid':sum(r['status']=='valid' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'unstarted':sum(r['status']=='unstarted' for r in rows),'semantic_review_complete':False,'budget':ledger.summary()}
    write(out/'summary.json',summary);return summary

def release_unstarted(p,out,ledger,worker_stopped):
    if worker_stopped is not True:raise ValueError('worker_not_stopped')
    # Only at closeout after exclusive stopped-worker verification. A start marker
    # or raw return keeps ambiguous exposure reserved/uncertain after any crash.
    released=[]
    for cid in ids(p):
        prefix=out/cid.replace(':','_')
        row=ledger.db.execute('SELECT status FROM charges WHERE id=?',('B2:'+cid,)).fetchone()
        if row==('reserved',) and not Path(str(prefix)+'.started.json').exists() and not Path(str(prefix)+'.response.json').exists():
            ledger.settle('B2:'+cid,0);released.append(cid)
    return released

def cli():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['qualify','main'])
    for name in ('ledger','admission','transport','out'):ap.add_argument('--'+name,required=True)
    ap.add_argument('--review');args=ap.parse_args();p=packet();a=json.loads(Path(args.admission).read_text())
    # Existing ledger only; creation is forbidden by this native entry point.
    if not Path(args.ledger).is_file():raise ValueError('missing_original_ledger')
    import sqlite3
    db=sqlite3.connect(args.ledger);cap,authority=db.execute('SELECT cap,ref FROM authority').fetchone();db.close()
    sp=importlib.util.spec_from_file_location('telephone_ledger',ROOT.parent/'src/ledger.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
    ledger=mod.Ledger(args.ledger,cap,authority)
    check_admission(p,a,ledger,args.transport)
    sp=importlib.util.spec_from_file_location('admitted_transport',args.transport);transport=importlib.util.module_from_spec(sp);sp.loader.exec_module(transport)
    # The admitted bridge must enforce <=55 s timeout and exactly one attempt.
    if transport.MAX_ATTEMPTS!=1 or not 0<transport.TIMEOUT_SECONDS<=55:raise ValueError('transport_contract')
    generate=transport.post_json;out=Path(args.out)
    if args.mode=='qualify':qualify(p,out,ledger,generate,a['deadline'])
    else:main_run(p,out,ledger,generate,a['deadline'],json.loads(Path(args.review).read_text()))
    print(json.dumps({'mode':args.mode,'finished':True,'automatic_retry':False}))

if __name__=='__main__':
    try:cli()
    except Exception as e:
        print(json.dumps({'failed':True,'error_type':type(e).__name__}));raise SystemExit(1)
