"""Forty-agent bounded collector; no model credential installed on this host."""
import argparse,concurrent.futures,json,os,sys,time,urllib.request
from pathlib import Path
from design import MODEL,PROVIDER,SYSTEM,BASE,ROLES,request,role,digest,sha,summarize
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[4]
sys.path.insert(0,str(REPO/'scripts'))
from experiment_ops.trace_receipts import KINDS,retain,audit
EXP='antsy-haiku-panel';ATTEMPTS={'Q0':'Q0-haiku-attempt-1','E0':'E0-haiku-attempt-1'}

def source_hash():return digest({str(p.relative_to(REPO)):sha(p) for p in sorted([*ROOT.glob('src/*.py'),ROOT/'PLAN.md',ROOT/'INPUT-FREEZE.json',REPO/'scripts/experiment_ops/trace_receipts.py'])})
def save(path,value):
    temp=path.with_suffix('.partial')
    with temp.open('w') as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)

def validate(a,stage,inputs):
    expected={'experiment':EXP,'stage':stage,'attempt':ATTEMPTS[stage],'source_sha256':source_hash(),
      'case_sha256':sha(inputs/'cases.json'),'allowlist_sha256':sha(inputs/'allowlist.json'),'max_calls':80 if stage=='Q0' else 720,
      'total_cap_usd':20,'historical_hold_usd':5,'max_concurrency':4}
    if any(a.get(k)!=v for k,v in expected.items()):raise ValueError('scope_mismatch')
    for flag in ('owner_authorized','exclusive_claim_verified','approved_team_verified','public_page_verified','runtime_verified','budget_reconciled','payload_allowlist_verified','prior_dispatch_fenced'):
        if a.get(flag) is not True:raise ValueError('admission_missing')
    if not (0<=time.time()-a['verified_at']<900 and a['claim_expires_at']>time.time()+5400):raise ValueError('stale_claim')
    if stage=='E0' and not a.get('qualification_passed'):raise ValueError('qualification_missing')

def invoke(url,cap,identity,payload):
    req=urllib.request.Request(url,json.dumps({'assignment':identity,'request':payload}).encode(),{'Authorization':'Bearer '+cap,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=120) as response:return json.load(response)

def render(summary,out):
    from PIL import Image,ImageDraw
    im=Image.new('RGB',(1800,1100),'#111c29');d=ImageDraw.Draw(im)
    def text(x,y,s,size=25,color='white'):d.text((x,y),str(s),fill=color,font_size=size)
    text(45,28,'Antsy | forty readers, shared mistakes?',40)
    text(45,92,summary['attempt']+' | '+summary['stop'],27)
    text(45,137,f"{summary['started']}/{summary['assigned']} calls started | {summary['valid']} valid | {summary['unstarted']} unstarted",25)
    colors={'correct':'#4bd0a3','wrong':'#fc7974','refer':'#e4b35e','unscorable':'#958ed2','incomplete':'#697689'}
    for i,(policy,counts) in enumerate(summary['policies'].items()):
        y=215+i*96;text(45,y,policy,23);x=340
        for k,color in colors.items():
            width=1050*counts[k]/max(1,summary['receipts'])
            if width:d.rectangle((x,y,x+width,y+27),fill=color)
            x+=width
        text(340,y+34,' | '.join(f'{k} {counts[k]}' for k in colors),19)
    text(45,933,'Each row is a policy on the same receipts. Agent votes are not independent receipt samples.',24)
    text(45,982,f"Known new API cost ${summary['actual_usd']:.4f} | missing usage {summary['usage_missing']} | trace {summary['trace_status']}",24)
    text(45,1031,'Green correct | red wrong | amber refer | purple unscorable | grey incomplete',23)
    im.save(out/'final_frame.png')

def collect(stage,inputs,out,admission,url,cap,reporter,call=invoke):
    validate(admission,stage,inputs)
    out.mkdir(mode=0o700,exist_ok=False);(out/'private').mkdir(mode=0o700)
    cases=[c for c in json.loads((inputs/'cases.json').read_text()) if c['stage']==stage]
    expected=2 if stage=='Q0' else 18
    if len(cases)!=expected:raise ValueError('case_count')
    allowed=json.loads((inputs/'allowlist.json').read_text())
    assignments=[{'id':f"{c['id']}-a{s:02d}",'unit':c['id'],'arm':role(s)} for c in cases for s in range(1,41)]
    manifest={'schema_version':1,'study':'antsy-targeted-v8','attempt':ATTEMPTS[stage], 'source_sha256':source_hash(),'config_sha256':digest({'model':MODEL,'provider':PROVIDER,'roles':ROLES,'system':SYSTEM,'base':BASE}),
      'assignments':assignments,'calls':[{'assignment':a['id'],'call_id':None,'status':'unstarted','artifacts':{}} for a in assignments]}
    path=out/'trace-manifest.json';save(path,manifest);records=[];stop='completed';start=time.monotonic()
    def store(data):
        ref=retain(out/'private/blobs',data);ref['path']='private/blobs/'+ref['path'];return ref
    reporter('start',0,len(assignments),{'agents':40},'Forty independent-context readers; receipt is the sample unit')
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for c in cases:
                image=inputs/'images'/c['image']
                if sha(image)!=c['image_sha256']:raise ValueError('image_changed')
                for offset in range(0,40,4):
                    if time.monotonic()-start>5100:stop='deadline';break
                    batch=[]
                    for seat in range(offset+1,offset+5):
                        identity=f"{c['id']}-a{seat:02d}";payload=request(image.read_bytes(),seat)
                        if digest(payload)!=allowed[identity]:raise ValueError('payload_drift')
                        index=next(i for i,a in enumerate(assignments) if a['id']==identity);row=manifest['calls'][index]
                        artifacts={k:{'absent':'not_reached'} for k in KINDS}
                        for k in ('transition','stdout','stderr'):artifacts[k]={'absent':'not_applicable'}
                        artifacts['input']=store(json.dumps(payload,sort_keys=True).encode())
                        artifacts['context']=store(json.dumps({'agent':seat,'role':role(seat),'fresh_context':True,'model':MODEL,'provider':PROVIDER,'temperature':.4,'max_tokens':512,'image_sha256':c['image_sha256'],'request_sha256':digest(payload)},sort_keys=True).encode())
                        row.update(call_id=identity,status='started',artifacts=artifacts);save(path,manifest)
                        batch.append((seat,index,time.monotonic(),pool.submit(call,url,cap,identity,payload)))
                    for seat,index,t,future in batch:
                        try:r=future.result()
                        except Exception:r={'error':'relay_connection_failure','parsed':None,'raw_text':None,'usage':None,'actual_usd':None}
                        record={'case':c['id'],'seat':seat,'role':role(seat),**r};records.append(record)
                        row=manifest['calls'][index];row['status']='valid' if not r.get('error') else 'failed'
                        row['artifacts']['response']=store(json.dumps(r,sort_keys=True).encode())
                        row['artifacts']['phases']=store(json.dumps({'start':t,'end':time.monotonic(),'scope':'parent wall clock, provider internals unobserved'}).encode())
                        if r.get('parsed') is not None:row['artifacts']['parsed']=store(json.dumps(r['parsed'],sort_keys=True).encode())
                        if r.get('usage') is not None:row['artifacts']['usage']=store(json.dumps({'usage':r['usage'],'actual_usd':r.get('actual_usd')},sort_keys=True).encode())
                        else:row['artifacts']['usage']={'absent':'not_collected'}
                        parsed=r.get('parsed');correct=parsed is not None and c['gold'] is not None and parsed.get('decision')=='accept' and parsed.get('amount')==c['gold']
                        row['artifacts']['grade']=store(json.dumps({'scorable':c['gold'] is not None,'correct':correct,'parser_valid':parsed is not None}).encode())
                        save(path,manifest);save(out/'private/records.json',records)
                        if r.get('error'):stop=r['error']
                    coverage=audit(out,'antsy-targeted-v8',ATTEMPTS[stage])
                    if coverage['status']!='verified_declared_coverage' and stop=='completed':stop='trace_gap'
                    reporter('progress',len(records),len(assignments),{'valid':sum(not r.get('error') for r in records),'cost_usd':sum(r.get('actual_usd') or 0 for r in records)},'Bounded collection; all assigned seats retained')
                    if stop!='completed':break
                if stop!='completed':break
    except BaseException:
        stop='interrupted_or_instrument_failure'
        raise
    finally:
        coverage=audit(out,'antsy-targeted-v8',ATTEMPTS[stage]);analysis=summarize(cases,records)
        qualified=stage=='Q0' and stop=='completed' and len(records)==80 and coverage['status']=='verified_declared_coverage' and all(row['correct_votes'] is not None and row['correct_votes']>=32 and row['decisions']['homogeneous20']['outcome']=='correct' and row['decisions']['varied20']['outcome']=='correct' for row in analysis['rows'])
        result={**analysis,'attempt':ATTEMPTS[stage],'source_sha256':source_hash(),'assigned':len(assignments),'started':coverage.get('started_count',len(records)),
          'valid':sum(not r.get('error') for r in records),'unstarted':sum(r['status']=='unstarted' for r in manifest['calls']),
          'stop':stop,'qualification_passed':qualified,'actual_usd':sum(r.get('actual_usd') or 0 for r in records),
          'usage_missing':sum(r.get('usage') is None for r in records),'trace_status':coverage['status'],'historical_hold_usd':5,'scope_cap_usd':20}
        save(out/'summary.json',result);save(out/'trace-audit.json',coverage);render(result,out)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['Q0','E0'],required=True)
    for k in ('inputs','out','admission','capability'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--relay-port',type=int,required=True);a=p.parse_args();os.umask(0o077)
    import swarm_report as sr
    run_id=EXP+'/'+ATTEMPTS[a.stage]
    def reporter(kind,step,total,metrics,message):sr.report(kind,experiment=EXP,run=run_id,step=step,total=total,metrics=metrics,message=message)
    result=collect(a.stage,a.inputs,a.out,json.loads(a.admission.read_text()),'http://127.0.0.1:'+str(a.relay_port)+'/antsy',a.capability.read_text().strip(),reporter)
    for filename in ('summary.json','trace-audit.json','final_frame.png'):sr.upload(run_id,a.out/filename,name=filename)
    reporter('done' if result['stop']=='completed' else 'fail',result['started'],result['assigned'],{'valid':result['valid'],'unstarted':result['unstarted'],'cost_usd':result['actual_usd'],'qualification_passed':result['qualification_passed']},'Qualification/evaluation outcome retained; see summary and traces')
    reporter('log',result['started'],result['assigned'],{'started_calls':result['started'],'unstarted':result['unstarted']},'Actual started count; terminal status does not imply every assignment ran')
    print(json.dumps({k:result[k] for k in ('attempt','started','valid','unstarted','stop','qualification_passed','actual_usd','trace_status')}))

if __name__=='__main__':
    try:main()
    except Exception:raise SystemExit('native_stopped_see_retained_evidence') from None
