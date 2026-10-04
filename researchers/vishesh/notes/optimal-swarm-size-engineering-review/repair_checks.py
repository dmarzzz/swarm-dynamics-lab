"""Reviewer-owned offline E1-E3 regression checks. No real transport/client."""
import contextlib,io,json,sys,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'optimal-swarm-size'/'src'))
import run_qualification as r
from failures import SafeFailure
from engine import execute
from tasks import generate,qualification_manifest
from reporting import Reporter
cfg=json.loads((Path(r.__file__).parent.parent/'qualification-config.json').read_text())
assignments=[a for a in qualification_manifest() if a['stage']=='Q-A']
results={}
task=generate('evidence','parallel',0)
for code in ('provider_deadline','http_429','usage_missing','route_changed','credential_unavailable','stage_budget_exhausted','episode_budget_exhausted'):
    calls=[]
    def fail(*a):calls.append(1);raise SafeFailure(code)
    record=execute(task.public,1,1,10,2,fail)
    assert record['failure']==code and len(calls)==1
    results[code]={'preserved':True,'fatal':record['fatal']}
class GoodProvider:
    calls=0
    def __init__(self,*a):pass
    def __call__(self,messages,deadline,actor,phase,item):
        GoodProvider.calls+=1;p=json.loads(messages[1]['content'])
        if phase=='plan':return json.dumps({'dependencies':p['dependencies']})
        if phase=='work':return '{"artifact":0}'
        if p['family']=='repository':return json.dumps({'files':{k:v.replace(' - ',' + ') for k,v in p['files'].items()}})
        answers={}
        for j,k in enumerate(p['items']):
            dep=p['dependencies'][k]
            v=answers[dep[0]]['value'] if dep else p['records']['opening']
            ids=(answers[dep[0]]['source_ids'] if dep else ['opening'])+[f'a_{j}',f'b_{j}']
            answers[k]={'value':v*p['records'][f'a_{j}']+p['records'][f'b_{j}'],'source_ids':ids}
        return json.dumps({'answers':answers})
class GoodReporter:
    def __init__(self,*a):pass
    def progress(self,*a):return {'acknowledged':True}
    def finish(self,*a):return {'complete':True}
class ProgressThrows(GoodReporter):
    def progress(self,*a):raise RuntimeError('synthetic non-public diagnostic')
class UploadFails(GoodReporter):
    def finish(self,*a):return {'complete':False}
class AdmissionFails(GoodReporter):
    def __init__(self,*a):raise SafeFailure('public_run_preflight_failed')
class FatalProvider:
    calls=0
    def __init__(self,*a):pass
    def __call__(self,*a):FatalProvider.calls+=1;raise SafeFailure('route_changed')
for name,reporter,provider in [('progress_throws',ProgressThrows,GoodProvider),('upload_fails',UploadFails,GoodProvider),('admission_fails',AdmissionFails,GoodProvider),('fatal_route',GoodReporter,FatalProvider)]:
    GoodProvider.calls=FatalProvider.calls=0
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp);out=p/'run';out.mkdir()
        with patch.object(r,'Reporter',reporter),patch.object(r,'Provider',provider),contextlib.redirect_stdout(io.StringIO()):
            exitcode=r.run_batch(cfg,'offline-review',out,p/'ledger.sqlite',assignments)
        rec=json.loads((out/'reconciliation.json').read_text())
        records=[json.loads(f.read_text()) for f in out.glob('*/outcome.json')]
        trace=''.join(f.read_text() for f in out.glob('*/trace.jsonl'))
        assert rec['assigned']==16 and len(rec['episodes'])==16 and len(list(out.glob('*/state.json')))==16
        assert 'synthetic non-public' not in trace
        summary={'exit':exitcode,'terminal':rec['terminal'],'stop_reason':rec['stop_reason'],'not_started':sum(x['execution']=='not_started' for x in rec['episodes']),'successful_records':sum(x['operational_success'] for x in records),'calls':GoodProvider.calls+FatalProvider.calls,'reporting_fault_recorded':'reporting_failure' in trace}
        if name=='progress_throws':assert rec['terminal']==16 and all(x['operational_success'] for x in records) and 'reporting_failure' in trace
        if name=='upload_fails':assert rec['terminal']==1 and summary['not_started']==15 and rec['stop_reason']=='publication_incomplete'
        if name=='admission_fails':assert summary['calls']==0 and rec['terminal']==0 and summary['not_started']==15
        if name=='fatal_route':assert summary['calls']==1 and rec['stop_reason']=='route_changed' and summary['not_started']==15
        results[name]=summary
with tempfile.TemporaryDirectory() as temp:
    p=Path(temp)
    for name in ('assignment.json','trace.jsonl','outcome.json','replay.html'):p.joinpath(name).write_text('{}')
    reporter=Reporter.__new__(Reporter);reporter.id='synthetic';reporter.experiment='synthetic'
    with patch('reporting.deliver',return_value={'acknowledged':False,'spooled':True,'code':'reporting_failed'}):
        receipt=reporter.finish(p,{'evaluation':{'quality':1},'operational_success':True,'elapsed_s':1,'exposure_microdollars':0,'failure':None})
    assert not receipt['complete'] and json.loads((p/'publication.json').read_text())==receipt
    results['spooled_publication']={'complete':False,'persisted':True,'artifacts':len(receipt['artifacts'])}
Path(__file__).with_name('repair-checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
