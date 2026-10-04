"""One admitted native C5 stage; no credential access or retry dispatch."""
import argparse,os,json,time,signal,collections,urllib.request,urllib.error
from pathlib import Path
from runtime import HERE,preflight,wire,digest,request,validate,QWEN_DIGEST
from contract import LIMITS,qwen_payload,score,qualify
from scenarios import assignments
from reporting import Reporter

def write(p,value):
    t=p.with_suffix('.tmp');t.write_text(json.dumps(value,indent=2));t.replace(p)
def append(p,value):
    with p.open('a') as f:f.write(json.dumps(value)+'\n');f.flush();os.fsync(f.fileno())
def health(stage):
    with urllib.request.urlopen('http://127.0.0.1:18443/health',timeout=5) as r:h=json.load(r)
    if h.get('ready') is not True or h.get('attempt')!='C5' or h.get('stage')!=stage or h.get('seconds_remaining',0)<60:raise ValueError('transport_not_ready')
    return h

class RejectedResponse(ValueError):
    def __init__(self,raw):
        super().__init__('invalid_task_response')
        self.raw=raw

def task_response(raw,model):
    # Retain only protocol task fields, never headers or arbitrary error bodies.
    keys=('message','model','prompt_eval_count','eval_count') if model=='qwen' else ('answers','model','provider','usage','id')
    return {k:raw[k] for k in keys if k in raw} if isinstance(raw,dict) else {'invalid_shape':type(raw).__name__}

def call_http(model,payload,timeout):
    path='http://127.0.0.1:'+('11434/api/chat' if model=='qwen' else '18443/decision')
    cached=False
    try:
        with urllib.request.urlopen(urllib.request.Request(path,wire(payload),{'Content-Type':'application/json'}),timeout=timeout) as r:raw=json.load(r)
    except (urllib.error.URLError,TimeoutError,ConnectionError):
        if model!='jev':raise
        with urllib.request.urlopen('http://127.0.0.1:18443/result/'+digest(payload),timeout=5) as r:raw=json.load(r)
        cached=True
    try:
        if model=='jev':
            if raw.get('rejected_task_response') is not None:raise RejectedResponse(raw['rejected_task_response'])
            return {**validate(raw),'raw':raw,'recovered_cached_response':cached}
        label=json.loads(raw['message']['content'])['label']
        if label not in ('SUPPORT','REFUTE','UNCERTAIN'):raise ValueError('invalid_qwen_label')
    except RejectedResponse:raise
    except (ValueError,KeyError,TypeError,AttributeError):raise RejectedResponse(task_response(raw,model)) from None
    return {'label':label,'raw':raw,'input_tokens':raw.get('prompt_eval_count',0),'output_tokens':raw.get('eval_count',0)}

def run(out,stage,admission,parent=None):
    if out.exists():raise ValueError('duplicate_attempt')
    a=json.loads(admission.read_text());hashes,receipt,tldr=preflight(a,stage,parent)
    transport=health(stage)
    with urllib.request.urlopen('http://127.0.0.1:11434/api/tags',timeout=10) as r:models=json.load(r)['models']
    q=next(x for x in models if x['name']=='qwen3:0.6b')
    if q['digest']!=QWEN_DIGEST:raise ValueError('qwen_digest_mismatch')
    out.mkdir(parents=True,exist_ok=False)
    for n,v in [('admission',a),('plan-receipt',receipt),('transport-receipt',transport)]:write(out/(n+'.json'),v)
    rows=assignments(stage);write(out/'observations.json',rows)
    import swarm_report as sdk
    reporter=Reporter(sdk,'healing-helping-hands','healing-helping-hands/C5-'+stage,out/'reporting.jsonl');reporter.emit('start',url=receipt['url'],params={'attempt_id':'C5','stage':stage,'arm':'selective-referral'},message=tldr)
    counts={'qwen':0,'jev':0};started=time.monotonic();deadline=started+(900 if stage=='S0' else 3600)
    m={'attempt':'C5-'+stage,'stage':stage,'status':'running','source_hashes':hashes,'plan':receipt,'calls':counts,'qwen_metadata':q,'host':a['host'],'claim':a['claim_id']};write(out/'manifest.json',m)
    def call(model,payload,rowid,variant):
        health(stage)
        if time.monotonic()>=deadline or counts[model]>=LIMITS[stage][model]:raise RuntimeError('stage_limit')
        counts[model]+=1;cid=model+'-'+str(counts[model]);t=time.monotonic()
        append(out/'calls.jsonl',{'type':'start','id':cid,'row_id':rowid,'variant':variant,'model':model,'payload':payload,'payload_hash':digest(payload)})
        try:
            result=call_http(model,payload,min(90,deadline-time.monotonic()));append(out/'calls.jsonl',{'type':'completed','id':cid,'result':result,'seconds':time.monotonic()-t});return result['label']
        except Exception as e:append(out/'calls.jsonl',{'type':'failed','id':cid,'error_type':type(e).__name__,'seconds':time.monotonic()-t,**({'rejected_task_response':e.raw} if isinstance(e,RejectedResponse) else {})});raise
    def stop(*args):raise InterruptedError('supervisor_stop')
    signal.signal(signal.SIGTERM,stop)
    try:
        for i,r in enumerate(rows):
            r['status']='running';write(out/'observations.json',rows)
            order=(('jev',None),('qwen',0),('qwen',1)) if i%2==0 else (('qwen',1),('qwen',0),('jev',None))
            for model,variant in order:
                key='jev' if model=='jev' else ('a' if variant==0 else 'b')
                payload=request(r,i,'C5-'+stage) if model=='jev' else qwen_payload(r,variant)
                r['labels'][key]=call(model,payload,r['id'],key)
            r['status']='completed';write(out/'observations.json',rows)
            if (i+1)%10==0:reporter.emit('metric',step=i+1,metrics={'completed_cases':i+1,'assigned_cases':len(rows),'model_calls':sum(counts.values())})
        m['status']='completed'
    except BaseException as e:m.update(status='failed',error_type=type(e).__name__)
    finally:
        for r in rows:
            if r['status']=='running':r['status']='failed'
            elif r['status']=='planned':r['status']='not_run'
        m.update(seconds=time.monotonic()-started,observation_counts=dict(collections.Counter(r['status'] for r in rows)))
        write(out/'observations.json',rows);write(out/'manifest.json',m);write(out/'summary.json',score(rows))
        if stage=='S0':write(out/'qualification.json',qualify(rows))
    reporter.emit('metric' if m['status']=='completed' else 'fail',metrics={'completed_cases':m['observation_counts'].get('completed',0)},message='C5 native stage terminal; audit and qualification/scientific assessment follow.')
    print(json.dumps({'status':m['status'],'counts':m['observation_counts'],'calls':counts}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--stage',choices=['S0','S1'],required=True);p.add_argument('--admission',type=Path,required=True);p.add_argument('--parent',type=Path);a=p.parse_args()
    try:run(a.out,a.stage,a.admission,a.parent)
    except Exception as e:print(json.dumps({'launch_failed':type(e).__name__}));raise SystemExit(1)
