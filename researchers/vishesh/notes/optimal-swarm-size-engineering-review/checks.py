"""Offline counterexamples only. No network, credentials or paid transport."""
import json, sys, tempfile, types
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'optimal-swarm-size'/'src'))
from engine import execute,validate_plan
from tasks import generate,evaluate
from reporting import Reporter
import run_qualification as runner
out={}
task=generate('evidence','chain',0)
answers={}
for j,item in enumerate(task.public['items']):
    deps=task.public['dependencies'][item]
    base=answers[deps[0]]['value'] if deps else task.public['records']['opening']
    sources=(answers[deps[0]]['source_ids'] if deps else ['opening'])+[f'a_{j}',f'b_{j}']
    answers[item]={'value':base*task.public['records'][f'a_{j}']+task.public['records'][f'b_{j}'],'source_ids':sources}
assert evaluate(task,json.dumps({'answers':answers}))['substantive_success']
mutated=json.loads(json.dumps(answers));mutated['item_00']['value']+=1
assert not evaluate(task,json.dumps({'answers':mutated}))['substantive_success']
repair_checks={}
for structure in ('parallel','chain'):
    repair=generate('repository',structure,0)
    files={k:v.replace(' - ',' + ') for k,v in repair.public['files'].items()}
    repaired=evaluate(repair,json.dumps({'files':files}))
    broken=evaluate(repair,json.dumps({'files':repair.public['files']}))
    assert repaired['substantive_success'] and not broken['substantive_success']
    repair_checks[structure]={'public_sign_repair_passes':True,'original_bug_rejected':True}
out['public_repair_examples']=repair_checks
out['public_arithmetic']={'reference_passes':True,'wrong_value_rejected':True,'first_value':answers['item_00']['value'],'last_value':answers['item_15']['value']}
failures={}
for reason in ('budget_exhausted','route_changed','provider_deadline','credential_unavailable'):
    def failed(*args):raise ValueError(reason)
    record=execute(task.public,1,1,10,2,failed)
    failures[reason]=record['failure']
assert len(set(failures.values()))==1
out['distinct_failures_collapse']=failures
# Scheduler accepts a plan removing all public chain prerequisites.
empty={item:[] for item in task.public['items']}
assert validate_plan({'dependencies':empty},task.public['items'])==empty
out['public_chain_edges_can_be_removed']=True
# finish() silently accepts unsuccessful artifact and terminal delivery returns.
run=Mock();run.artifact.return_value=False;run.done.return_value=False
reporter=Reporter.__new__(Reporter);reporter.run=run
with tempfile.TemporaryDirectory() as temp:
    p=Path(temp)
    for name in ('assignment.json','trace.jsonl','outcome.json','replay.html'):p.joinpath(name).write_text('{}')
    reporter.finish(p,{'evaluation':{'quality':1},'operational_success':True,'elapsed_s':1,'exposure_microdollars':0,'failure':None})
assert run.artifact.call_count==4 and run.done.call_count==1
out['failed_upload_return_ignored']={'artifact_failures':4,'terminal_failure':True,'finish_raised':False}
# Simulate progress exception after one work completion, without dispatching real transport.
class FakeReporter:
    def __init__(self,*a):pass
    def progress(self,*a):raise RuntimeError('synthetic_reporting_failure')
    def finish(self,*a):pass
class FakeProvider:
    def __init__(self,*a):pass
    def __call__(self,messages,deadline,actor,phase,item):
        public=json.loads(messages[1]['content'])
        if phase=='plan':return json.dumps({'dependencies':public['dependencies']})
        return json.dumps({'artifact':0})
with tempfile.TemporaryDirectory() as temp:
    p=Path(temp);cfg=Path(runner.__file__).parent.parent/'qualification-config.json'
    argv=['run_qualification','--config',str(cfg),'--output',str(p/'run'),'--budget-ledger',str(p/'ledger.sqlite')]
    with patch.object(sys,'argv',argv),patch.object(runner,'preflight',return_value='offline-mock'),patch.object(runner,'Reporter',FakeReporter),patch.object(runner,'Provider',FakeProvider):
        # Engine catches callback exception and writes a terminal failure; retain evidence.
        runner.main()
    rows=list((p/'run').glob('*/outcome.json'))
    records=[json.loads(r.read_text()) for r in rows]
    out['progress_exception']={'assigned':len(json.loads((p/'run'/'assigned.json').read_text())),'outcomes':len(records),'failure_classes':sorted(set(r['failure'] for r in records)),'all_stop_after_first_item':all(r['completed_items']==1 for r in records)}
# Construction failure happens outside the runner's execution boundary and leaves no terminal record.
class FailStart:
    def __init__(self,*a):raise RuntimeError('synthetic_public_preflight_failure')
with tempfile.TemporaryDirectory() as temp:
    p=Path(temp);argv=['run_qualification','--config',str(cfg),'--output',str(p/'run'),'--budget-ledger',str(p/'ledger.sqlite')]
    with patch.object(sys,'argv',argv),patch.object(runner,'preflight',return_value='offline-mock'),patch.object(runner,'Reporter',FailStart):
        try:runner.main()
        except RuntimeError:pass
    out['registration_failure_reconciliation']={'assigned':len(json.loads((p/'run'/'assigned.json').read_text())),'outcomes':len(list((p/'run').glob('*/outcome.json'))),'per_episode_assignments':len(list((p/'run').glob('*/assignment.json')))}
Path(__file__).with_name('checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
