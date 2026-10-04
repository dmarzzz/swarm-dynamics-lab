"""Native paired receipt controller with explicit qualified-stage fence."""
import sys,json,time,os,argparse,urllib.request
from pathlib import Path
import contract as c
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[4]
sys.path.insert(0,str(REPO/'scripts'))
from experiment_ops.trace_receipts import KINDS,retain,audit
EXP='antsy-literal-v2r'

def save(p,v):
 t=p.with_suffix('.partial')
 with t.open('w') as f:json.dump(v,f,indent=2);f.flush();os.fsync(f.fileno())
 os.replace(t,p)
def source_hash():
 files=[p for p in HERE.iterdir() if p.is_file()]+[c.OLD/'design.py',REPO/'scripts/experiment_ops/trace_receipts.py']
 return c.digest({str(p.relative_to(REPO)):c.sha(p) for p in sorted(files)})
def invoke(url,cap,identity,payload):
 req=urllib.request.Request(url,json.dumps({'assignment':identity,'request':payload}).encode(),{'Authorization':'Bearer '+cap,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=120) as f:return json.load(f)
def assess(cases,records):
 rows=[]
 for case in cases:
  rr=[r for r in records if r['case']==case['id']];v={r['kind']:r['parsed'] for r in rr if not r.get('error')};d=c.decide(v)
  expected=c.order(case['stage'],case['index']);complete=set(v)==set(expected)
  outcomes={k:('incomplete' if not complete else 'unscorable' if case['gold'] is None else 'refer' if amount is None else 'correct' if amount==case['gold'] else 'wrong') for k,amount in d.items()}
  rows.append({'case':case['id'],'complete':complete,'invalid_direct_decisions':sum(k in v and v[k].get('decision')=='accept' and not c.canonical(v[k]) for k in ('direct-a','direct-b')),'decisions':d,'outcomes':outcomes,'negative_control_rejected':v.get('corrupt',{}).get('verified') is False if case['stage']=='Q2' else None,'source_checker_positive':v.get('verify',{}).get('verified') is True,'literal_token':v.get('literal',{}).get('token')})
 return rows

def collect(stage,inputs,out,admission,cap,port,reporter,call=invoke):
 a=json.loads(admission.read_text());frozen=json.loads((HERE/'INPUT-FREEZE.json').read_text())
 assert a['source_sha256']==source_hash() and a['stage']==stage and a['owner_authorized'] and a['public_page_verified'] and a['allocation_verified'] and a['budget_verified']
 assert 0<=time.time()-a['verified_at']<900 and a['claim_expires_at']>time.time()+1800
 assert c.sha(inputs/'cases.json')==frozen['cases_sha256'] and c.sha(inputs/'specs.json')==frozen['specs_sha256']
 if stage=='E2':assert a.get('qualification_passed')
 cases=[x for x in json.loads((inputs/'cases.json').read_text()) if x['stage']==stage];assert len(cases)==(4 if stage=='Q2' else 18)
 assignments=[{'id':x['id']+'-'+k,'unit':x['id'],'arm':k} for x in cases for k in c.order(stage,x['index'])]
 attempt=stage+'-literal-attempt-1';out.mkdir(mode=0o700,exist_ok=False);(out/'private').mkdir(mode=0o700)
 m={'schema_version':1,'study':'antsy-targeted-v8','attempt':attempt,'source_sha256':source_hash(),'config_sha256':c.sha(inputs/'specs.json'),'assignments':assignments,'calls':[{'assignment':x['id'],'call_id':None,'status':'unstarted','artifacts':{}} for x in assignments]};save(out/'trace-manifest.json',m)
 def blob(v):
  r=retain(out/'private/blobs',json.dumps(v,sort_keys=True).encode());r['path']='private/blobs/'+r['path'];return r
 records=[];stop='completed';started=time.monotonic();reporter('start',0,len(assignments),{},'Literal extraction plus deterministic normalization and image check; paired two-call baseline')
 try:
  for case in cases:
   im=inputs/'images'/case['image'];assert c.sha(im)==case['image_sha256'];parent=None
   for kind in c.order(stage,case['index']):
    if time.monotonic()-started>1700:stop='deadline';break
    identity=case['id']+'-'+kind;p=c.request(im.read_bytes(),kind,parent);i=next(i for i,x in enumerate(assignments) if x['id']==identity)
    ar={k:{'absent':'not_reached'} for k in KINDS}
    for k in ('stdout','stderr'):ar[k]={'absent':'not_applicable'}
    ar['input']=blob(p);ar['context']=blob({'model':c.MODEL,'provider':c.PROVIDER,'kind':kind,'fresh_context':True,'image_sha256':case['image_sha256'],'parent':case['id']+'-literal' if kind in ('verify','corrupt') else None})
    ar['transition']=blob({'proposal':c.proposed(parent,kind=='corrupt')}) if kind in ('verify','corrupt') else {'absent':'not_applicable'}
    m['calls'][i].update(call_id=identity,status='started',artifacts=ar);save(out/'trace-manifest.json',m);t=time.monotonic()
    try:r=call('http://127.0.0.1:'+str(port)+'/antsy',cap,identity,p)
    except Exception:r={'error':'relay_connection_failure','parsed':None,'usage':None,'actual_usd':None}
    ar['response']=blob(r);ar['phases']=blob({'start':t,'end':time.monotonic()})
    if r.get('parsed') is not None:ar['parsed']=blob(r['parsed'])
    ar['usage']=blob({'usage':r['usage'],'actual_usd':r['actual_usd']}) if r.get('usage') else {'absent':'not_collected'}
    parsed=r.get('parsed');candidate=(parsed.get('amount') if kind in ('direct-a','direct-b') else c.normalize(parsed.get('token')) if kind=='literal' else None) if parsed else None
    ar['grade']=blob({'gold_available':case['gold'] is not None,'candidate_correct':candidate==case['gold'] if candidate is not None and case['gold'] is not None else None,'negative_control_rejected':parsed.get('verified') is False if kind=='corrupt' and parsed else None,'paired_decision_in_summary':True})
    m['calls'][i]['status']='failed' if r.get('error') else 'valid';save(out/'trace-manifest.json',m)
    records.append({'id':identity,'case':case['id'],'kind':kind,**r});save(out/'private/records.json',records)
    if kind=='literal':parent=r.get('parsed')
    if r.get('error'):stop=r['error'];break
    coverage=audit(out,'antsy-targeted-v8',attempt)
    if coverage['status']!='verified_declared_coverage':stop='trace_gap';break
    reporter('progress',len(records),len(assignments),{'valid':len(records),'cost_usd':sum(x.get('actual_usd') or 0 for x in records)},'All assigned outcomes retained')
   if stop!='completed':break
 finally:
  rows=assess(cases,records);coverage=audit(out,'antsy-targeted-v8',attempt)
  qualified=stage=='Q2' and stop=='completed' and len(records)==20 and all(r['complete'] and r['outcomes']['treatment']=='correct' and r['negative_control_rejected'] and r['source_checker_positive'] for r in rows)
  result={'attempt':attempt,'stage':stage,'assigned':len(assignments),'started':len(records),'valid':sum(not x.get('error') for x in records),'unstarted':sum(x['status']=='unstarted' for x in m['calls']),'stop':stop,'trace_status':coverage['status'],'qualification_passed':qualified,'actual_usd':sum(x.get('actual_usd') or 0 for x in records),'rows':rows,'source_sha256':source_hash()}
  save(out/'summary.json',result);save(out/'trace-audit.json',coverage)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['Q2','E2'],required=True)
 for k in ('inputs','out','admission','capability'):p.add_argument('--'+k,type=Path,required=True)
 p.add_argument('--port',type=int,required=True);a=p.parse_args();os.umask(0o077)
 import swarm_report as sr
 rid=EXP+'/'+a.stage+'-literal-attempt-1'
 def report(kind,step,total,metrics,msg):sr.report(kind,experiment=EXP,run=rid,step=step,total=total,metrics=metrics,message=msg)
 try:
  r=collect(a.stage,a.inputs,a.out,a.admission,a.capability.read_text().strip(),a.port,report)
  for n in ('summary.json','trace-audit.json'):sr.upload(rid,a.out/n,name=n)
  report('done' if r['stop']=='completed' else 'fail',r['started'],r['assigned'],{'valid':r['valid'],'cost_usd':r['actual_usd'],'qualification_passed':r['qualification_passed']},'Execution terminal; qualification and scientific interpretation recorded separately')
  print(json.dumps({k:r[k] for k in ('started','valid','stop','qualification_passed','actual_usd')}))
 except Exception:raise SystemExit('native_stopped_see_private_evidence') from None
