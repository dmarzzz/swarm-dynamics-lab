"""Admitted six-call D1 only. No warm-up, retries, qualification or successor."""
import argparse,fcntl,hashlib,json,os,subprocess,sys,time,urllib.request
from pathlib import Path
from capture import run_once
ROOT=Path(__file__).resolve().parent
STUDY=ROOT.parent
EXP='antsy-targeted-v8';ATTEMPT='D1-latency-attempt-1';RUN=EXP+'/'+ATTEMPT
ORDER=(60,61,62,60,61,62)
DOCS=('PLAN.md','D1-PRE.md')

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(v,category):
    if not v:raise ValueError(category)
def write(p,v):
    with p.open('w') as f:json.dump(v,f,indent=2);f.flush();os.fsync(f.fileno())

def validate(r,source,runtime,now=None):
    now=time.time() if now is None else now
    expected={'experiment':EXP,'attempt':ATTEMPT,'source':source,'max_ocr_calls':6,'max_model_calls':0,'new_charge_cap_usd':0,'order':list(ORDER),'deadline_s':90,'eligibility_s':45,'stage_limit_s':600,'host':'sim-vishesh','claim':'vishesh-antsy-d1','automatic_successor':False}
    require(all(r.get(k)==v for k,v in expected.items()),'scope_mismatch')
    require(all(r.get(k) is True for k in ('owner_approved','exclusive_claim_verified','approved_team_verified','host_idle_verified','runtime_matches_q0','public_page_verified','budget_reconciled','duplicate_dispatch_fenced','host_class_matches_q0')),'admission_missing')
    require(bool(r.get('authority_reference')),'owner_reference_missing')
    require(0<=now-r['verified_at']<900 and now+660<r['claim_expires_at'],'stale_admission')
    require(r['runtime_sha256']==digest(runtime),'runtime_mismatch')
    require(r['documents']=={n:sha(ROOT/n) for n in DOCS},'document_mismatch')
    return True

def collect(invoke,save,clock=time.monotonic):
    start=clock();records=[];stop='completed'
    for seq,receipt in enumerate(ORDER,1):
        if clock()-start+92>600:stop='stage_deadline';break
        try:result=invoke(seq,receipt)
        except Exception:
            result={'status':'error','category':'supervisor_exception','latency_eligible':False,'wall_s':None,'phases':{'events':[],'valid':False,'complete':False}}
        row={'seq':seq,'receipt':receipt,'repeat':1 if seq<=3 else 2,**result};records.append(row);save(records)
        if result['status']!='valid':stop=result['category'];break
        if not result['latency_eligible']:stop='over_45s';break
        if not result['phases']['valid'] or not result['phases']['complete']:stop='invalid_phases';break
    return records,stop

def summarize(records,stop):
    return {'assigned':6,'receipt_units_planned':3,'started':len(records),'valid':sum(r['status']=='valid' for r in records),'failed':sum(r['status']!='valid' for r in records),'latency_eligible':sum(r['status']=='valid' and r['latency_eligible'] for r in records),'unstarted':6-len(records),'stop_reason':stop,'complete':len(records)==6,'diagnostic_within_limit':len(records)==6 and stop=='completed','qualification_passed':False,'hosted_model_calls':0,'new_charge_usd':0,'automatic_successor':False}

def render(out,records,summary):
    from PIL import Image,ImageDraw
    im=Image.new('RGB',(1600,900),'#101b29');d=ImageDraw.Draw(im)
    def text(x,y,s,size=24,color='white'):d.text((x,y),s,fill=color,font_size=size)
    text(45,35,'Antsy D1 | where does the checker spend its time?',35)
    text(45,94,'Reused receipts; cold processes; 45s eligibility unchanged; 90s diagnostic ceiling.',24)
    phases=[('imports_begin','imports_end','#6ba9ef'),('reader_init_begin','reader_init_end','#ba8be9'),('ocr_begin','ocr_end','#efb366'),('extract_begin','extract_end','#45cba1'),('output_begin','output_end','#b1c2ce')]
    for j,i in enumerate(ORDER):
        y=190+j*85;text(45,y,f'{j+1}. receipt {i}',23)
        if j>=len(records):text(260,y,'UNSTARTED',22,'#8e9caf');continue
        r=records[j];ev={e['phase']:e['elapsed_s'] for e in r['phases']['events']}
        for a,b,color in phases:
            if a in ev:
                end=ev.get(b,ev[a]);d.rectangle((260+ev[a]*11,y,260+max(end,ev[a]+.1)*11,y+26),fill=color)
        text(260,y+34,f"{r['wall_s'] if r['wall_s'] is not None else 'unknown'}s | {r['category']} | eligible: {r['latency_eligible']}",19)
    d.line((755,160,755,690),fill='#fa6767',width=2);text(720,140,'45s',19)
    text(45,738,f"Started {summary['started']}/6 | valid {summary['valid']} | unstarted {summary['unstarted']} | stop: {summary['stop_reason']}",26)
    text(45,787,'Blue: imports | purple: initialization | orange: OCR | green: extraction | pale: output',22)
    text(45,832,'Phase bars omit interpreter startup/parent overhead. Missing phases are not zero. No efficacy inference.',20)
    im.save(out/'final_frame.png')

def execute(a):
    source=subprocess.check_output(['git','-C',str(a.repo),'rev-parse','HEAD'],text=True).strip()
    require(not subprocess.check_output(['git','-C',str(a.repo),'status','--porcelain']),'dirty_source')
    r=json.loads(a.admission.read_text())
    # Exact Q0 checker package/model inspection; no inference.
    check=subprocess.run([str(a.python),str(STUDY/'src/native_worker.py'),'--engine','C','--models',str(a.models),'--inspect'],capture_output=True,timeout=90)
    require(check.returncode==0,'runtime_inspection_failed');runtime=json.loads(check.stdout)
    baseline=json.loads((STUDY/'results/Q0-attempt-1/manifest.json').read_text())['runtime']['C']
    require(runtime==baseline,'runtime_differs_from_q0');validate(r,source,runtime)
    for n in DOCS:
        url=f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{source}/researchers/vishesh/notes/antsy-targeted-v8/execution-repair-v1/{n}'
        with urllib.request.urlopen(url,timeout=30) as f:require(hashlib.sha256(f.read()).hexdigest()==sha(ROOT/n),'public_plan_drift')
    traces=json.loads((STUDY/'results/Q0-attempt-1/trace-audit.json').read_text())['calls'];hashes={x['id']:x['image_sha256'] for x in traces}
    for i in (60,61,62):require(sha(a.inputs/f'train-{i}.png')==hashes[i],'input_mismatch')
    sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
    existing=[x for x in sr.runs(EXP,limit=5000) if x['run']==RUN]
    require(not any(x.get('status') in ('running','done','failed') for x in existing),'attempt_already_started')
    require(a.out.name==ATTEMPT and not a.out.exists(),'output_exists')
    os.umask(0o077);a.out.mkdir();private=a.out/'private';private.mkdir();(private/'calls').mkdir()
    write(a.out/'reservation.json',{'attempt':ATTEMPT,'max_ocr_calls':6,'max_model_calls':0,'new_charge_cap_usd':0,'historical_exposure':'unchanged','order':list(ORDER),'reserved_before_dispatch':True})
    manifest={'attempt':ATTEMPT,'source':source,'runtime_sha256':digest(runtime),'input_sha256':{str(i):hashes[i] for i in (60,61,62)},'documents':r['documents'],'started_at':time.time(),'complete':False}
    write(a.out/'manifest.json',manifest)
    plan_url=f'https://github.com/dmarzzz/swarm-lab/blob/{source}/researchers/vishesh/notes/antsy-targeted-v8/execution-repair-v1/D1-PRE.md'
    sr.report('start',EXP,RUN,params={'stage':'D1','attempt':ATTEMPT},message='TLDR: Cold EasyOCR latency diagnosis on three reused receipts, six calls maximum.45s eligibility;90s censoring; stop at first slow/error. No efficacy or qualification claim.',url=plan_url,strict=True)
    def save(records):write(a.out/'records.json',records)
    def invoke(seq,i):
        require(time.time()+100<r['claim_expires_at'],'claim_expiring')
        result=run_once([str(a.python),str(ROOT/'worker.py'),'--image',str(a.inputs/f'train-{i}.png'),'--models',str(a.models),'--out','{out}','--phases','{phases}'],private/'calls'/f'{seq:02d}',a.inputs/f'train-{i}.png',hashes[i],90,45)
        p=private/'calls'/f'{seq:02d}'/'private/output.json'
        if result['status']=='valid':result['candidate']=json.loads(p.read_text())['candidate']
        return result
    records,stop=collect(invoke,save)
    summary=summarize(records,stop);manifest.update(complete=True,wall_s=time.time()-manifest['started_at'])
    write(a.out/'manifest.json',manifest);write(a.out/'summary.json',summary);render(a.out,records,summary)
    for p in sorted(a.out.iterdir()):
        if p.is_file():sr.upload(RUN,p,p.name)
    sr.report('done' if summary['failed']==0 else 'fail',EXP,RUN,step=len(records),total=6,metrics={'valid_calls':summary['valid'],'latency_eligible':summary['latency_eligible'],'unstarted':summary['unstarted']},message=f"D1 stop: {stop}; qualification remains closed; no automatic successor.",strict=True)
    print(json.dumps(summary))

def main():
    p=argparse.ArgumentParser()
    for n in ('repo','admission','python','models','inputs','out'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True)
    with (a.out.parent/'D1.lock').open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);execute(a)
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps({'blocked_or_failed':type(e).__name__}));raise SystemExit(1)
