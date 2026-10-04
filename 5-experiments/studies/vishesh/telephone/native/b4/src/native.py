"""Bounded B4 native core. Existing ledger only; injected one-attempt transport.

Four independent chains may execute concurrently. Each chain remains sequential.
No credentials, allocation, budget amendment, retry, resume or fallback here.
"""
import argparse,hashlib,importlib.util,json,os,sqlite3,threading,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from corpus import canonical,sha
from contract import request,normalize,MODEL,MAX_INPUT,PER
from prepare import ROOT,envelope

def write(p,x):
    with Path(p).open('x') as f:json.dump(x,f,indent=2);f.flush();os.fsync(f.fileno())
def file_sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def packet():
    manifest=json.loads((ROOT/'prepared/manifest.json').read_text())
    for name,digest in manifest.items():
        if file_sha(ROOT/name)!=digest:raise ValueError('source_mismatch')
    load=lambda n:json.loads((ROOT/'prepared'/n).read_text())
    return {'gold_sha256':sha(load('gold.json')),'actors':load('actors.json'),'questions':load('questions.json'),'assignments':load('assignments.json'),'qualification':load('qualification.json'),'envelope':load('envelope.json'),'manifest_sha256':file_sha(ROOT/'prepared/manifest.json')}

class ExistingLedger:
    def __init__(self,path):
        if not Path(path).is_file():raise ValueError('original_ledger_required')
        self.db=sqlite3.connect(path,check_same_thread=False,timeout=30);self.lock=threading.RLock()
        if self.db.execute('SELECT COUNT(*) FROM authority').fetchone()[0]!=1:raise ValueError('authority')
    def reserve(self,p):
        ids=['q01','q02']+[x['id'] for x in p['assignments']]
        with self.lock:
            self.db.execute('BEGIN IMMEDIATE')
            try:
                if len(ids)!=92 or len(set(ids))!=92 or self.db.execute("SELECT 1 FROM charges WHERE stage='B4' AND kind='model'").fetchone():raise ValueError('packet_or_duplicate')
                cap=self.db.execute('SELECT cap FROM authority').fetchone()[0]
                total=self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserve)),0) FROM charges').fetchone()[0]
                if total+len(ids)*PER>min(cap,50000000000):raise ValueError('budget')
                for cid in ids:self.db.execute('INSERT INTO charges VALUES (?,?,?,?,NULL,?,?)',('B4:'+cid,'B4','model',PER,'reserved',p['manifest_sha256']))
                self.db.commit()
            except Exception:self.db.rollback();raise
    def check(self,cid):
        with self.lock:
            if self.db.execute('SELECT reserve,status FROM charges WHERE id=?',('B4:'+cid,)).fetchone()!=(PER,'reserved'):raise ValueError('not_reserved')
    def settle(self,cid,actual):
        with self.lock:
            self.check(cid)
            if actual is not None and (type(actual)is not int or not 0<=actual<=PER):raise ValueError('settlement_bound')
            self.db.execute('UPDATE charges SET actual=?,status=? WHERE id=?',(actual,'known' if actual is not None else 'unknown','B4:'+cid));self.db.commit()
    def summary(self):
        with self.lock:
            rows=self.db.execute('SELECT status,COUNT(*),SUM(COALESCE(actual,reserve)) FROM charges GROUP BY status').fetchall()
            return {'cumulative_by_status':rows,'authority_cap_nano':self.db.execute('SELECT cap FROM authority').fetchone()[0]}

def admission(p,a,ledger,transport):
    now=time.time();e=envelope()
    if a.get('stage')!='B4' or a.get('manifest_sha256')!=p['manifest_sha256'] or a.get('model')!=MODEL:raise ValueError('scope')
    if not a.get('pi_decision_id') or a.get('additional_cap_nano')!=e['additional_max_nano']:raise ValueError('funding')
    if not e['cumulative_max_nano']<=a.get('cumulative_cap_nano',0)<=50000000000:raise ValueError('study_amendment')
    if not now<a.get('deadline',0)<=now+1800 or not a['deadline']<=a.get('claim_expires',0):raise ValueError('deadline')
    if not isinstance(a.get('public_plan_url'),str) or not a['public_plan_url'].startswith('https://'):raise ValueError('public_plan')
    for key in ('portfolio_reserved','public_plan_verified','condition_tldrs_registered','account_verified','exclusive_claim_verified','worker_idle_verified','runtime_verified'):
        if a.get(key)is not True:raise ValueError(key)
    if file_sha(transport)!=a.get('transport_sha256'):raise ValueError('transport_hash')
    cap=ledger.db.execute('SELECT cap FROM authority').fetchone()[0]
    if cap!=a['cumulative_cap_nano']:raise ValueError('ledger_amendment_missing')
    infra=ledger.db.execute('SELECT reserve,actual,status,kind FROM charges WHERE id=?',(a.get('infrastructure_reservation_id'),)).fetchone()
    if not infra or infra[2:]!=('reserved','infrastructure') or not 0<infra[0]<=250000000:raise ValueError('infra')
    prior=ledger.db.execute("SELECT COALESCE(SUM(COALESCE(actual,reserve)),0) FROM charges WHERE stage!='B4' AND id!=?",(a['infrastructure_reservation_id'],)).fetchone()[0]
    if prior!=e['prior_nano']:raise ValueError('stale_prior_cost')
    if ledger.db.execute("SELECT 1 FROM charges WHERE stage!='B4' AND kind='model' AND status!='known'").fetchone():raise ValueError('prior_unknown_cost')

class Runner:
    def __init__(self,p,out,ledger,generate,deadline):
        self.p=p;self.out=Path(out);self.ledger=ledger;self.generate=generate;self.deadline=deadline
        self.stop=threading.Event();self.start_lock=threading.RLock();self.seen=set()
    def perform(self,cid,req,role):
        # Start admission serialized; an already-started call may finish after stop.
        with self.start_lock:
            if self.stop.is_set() or time.time()+60>=self.deadline:raise ValueError('stopped_or_deadline')
            bound=len(canonical(req).encode())+1024
            if bound>MAX_INPUT:raise ValueError('input_bound')
            self.ledger.check(cid);write(self.out/(cid+'.request.json'),req)
            started=time.time();write(self.out/(cid+'.started.json'),{'started_at':started,'request_sha256':sha(req)})
        try:
            raw=self.generate(cid,req);write(self.out/(cid+'.response.json'),raw)
            obj,usage=normalize(raw,bound,role)
            with self.start_lock:
                if usage['generation_id'] in self.seen:raise ValueError('duplicate_generation')
                self.seen.add(usage['generation_id'])
            self.ledger.settle(cid,usage['cost_nano'])
            return obj,{'status':'valid','started_at':started,'latency_seconds':time.time()-started,'request_sha256':sha(req),'response_sha256':sha(raw),'output':obj,**usage}
        except Exception:
            self.stop.set();self.ledger.settle(cid,None);raise
    def qualify(self):
        self.out.mkdir(parents=True,mode=0o700,exist_ok=False);write(self.out/'packet.json',self.p)
        self.ledger.reserve(self.p);rows=[]
        for cid in ('q01','q02'):
            q=self.p['qualification'][cid]
            try:
                _,r=self.perform(cid,request('R',q['actor'],question=q['question']),'reader');rows.append({'id':cid,**r})
            except Exception as e:rows.append({'id':cid,'status':'failed','failure_type':type(e).__name__});break
        write(self.out/'qualification-summary.json',{'rows':rows,'semantic_review_complete':False,'budget':self.ledger.summary()});return rows
    def review(self,review):
        if review.get('manifest_sha256')!=self.p['manifest_sha256'] or not review.get('assessor'):raise ValueError('qualification_review')
        gold=json.loads((ROOT/'prepared/qualification-gold.json').read_text());seen=set()
        for cid in ('q01','q02'):
            q=self.p['qualification'][cid];req=json.loads((self.out/(cid+'.request.json')).read_text());raw=json.loads((self.out/(cid+'.response.json')).read_text())
            if req!=request('R',q['actor'],question=q['question']):raise ValueError('qualification_request')
            obj,u=normalize(raw,len(canonical(req).encode())+1024,'reader');r=review.get('responses',{}).get(cid,{})
            if obj['answer']!=gold[cid] or r.get('response_sha256')!=sha(raw) or r.get('evidence_supported')is not True or not r.get('rationale') or u['generation_id'] in seen:raise ValueError('qualification_failed')
            seen.add(u['generation_id'])
        self.seen.update(seen)
    def main(self,review,workers=4):
        if type(workers)is not int or not 1<=workers<=4:raise ValueError('workers')
        if (self.out/'main-start.json').exists():raise ValueError('attempt_already_started')
        if json.loads((self.out/'packet.json').read_text())!=self.p:raise ValueError('packet')
        self.review(review);write(self.out/'main-start.json',{'manifest_sha256':self.p['manifest_sha256'],'workers':workers,'review_sha256':sha(review)});write(self.out/'qualification-review.json',review)
        chains={}
        for a in self.p['assignments']:chains.setdefault(a['chain'],[]).append(a)
        def run_chain(chain):
            parents={};parent_hashes={};rows=[]
            for a in chain:
                row={**a,'status':'unstarted'};rows.append(row)
                if self.stop.is_set():continue
                try:
                    previous=None if a['parent']is None else parents[a['parent']]
                    parent_hash=None if a['parent']is None else parent_hashes[a['parent']]
                    req=request(a['arm'],self.p['actors'][a['case_id']],previous,self.p['questions'][a['case_id']] if a['role']=='reader' else None)
                    previous,receipt=self.perform(a['id'],req,a['role']);row.update(receipt,parent_response_sha256=parent_hash);parents[a['id']]=previous;parent_hashes[a['id']]=receipt['response_sha256']
                except Exception as e:row.update(status='failed',failure_type=type(e).__name__);self.stop.set()
                write(self.out/(a['id']+'.receipt.json'),row)
            return rows
        with ThreadPoolExecutor(max_workers=workers) as pool:rows=[r for group in pool.map(run_chain,chains.values()) for r in group]
        result={'rows':rows,'valid':sum(r['status']=='valid' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'unstarted':sum(r['status']=='unstarted' for r in rows),'audit_complete':False,'budget':self.ledger.summary()}
        write(self.out/'summary.json',result);return result

def release_unstarted(p,out,ledger,worker_stopped):
    if worker_stopped is not True:raise ValueError('worker_stop_verification_required')
    released=[]
    for cid in ['q01','q02']+[a['id'] for a in p['assignments']]:
        with ledger.lock:
            row=ledger.db.execute('SELECT status FROM charges WHERE id=?',('B4:'+cid,)).fetchone()
            if row==('reserved',) and not (Path(out)/(cid+'.started.json')).exists() and not (Path(out)/(cid+'.response.json')).exists():
                ledger.settle(cid,0);released.append(cid)
    return released

def cli():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['qualify','main'])
    for name in ('ledger','admission','transport','out'):ap.add_argument('--'+name,required=True)
    ap.add_argument('--review');args=ap.parse_args();p=packet();a=json.loads(Path(args.admission).read_text());ledger=ExistingLedger(args.ledger);admission(p,a,ledger,args.transport)
    spec=importlib.util.spec_from_file_location('admitted_b4_transport',args.transport);t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
    if t.MAX_ATTEMPTS!=1 or not 0<t.TIMEOUT_SECONDS<=55:raise ValueError('transport_contract')
    runner=Runner(p,args.out,ledger,t.post_json,a['deadline'])
    if args.mode=='qualify':runner.qualify()
    else:runner.main(json.loads(Path(args.review).read_text()))
    print(json.dumps({'finished':True,'mode':args.mode,'automatic_retry':False}))
if __name__=='__main__':
    try:cli()
    except Exception as e:print(json.dumps({'failed':True,'error_type':type(e).__name__}));raise SystemExit(1)
