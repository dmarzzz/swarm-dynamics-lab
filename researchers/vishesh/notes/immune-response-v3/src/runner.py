"""Finite qualification runner with durable per-round telemetry and explicit validity."""
import argparse,hashlib,json,os,platform,subprocess,time
from pathlib import Path
import immune
from provider import ScriptedPolicy,AnthropicPolicy
ROOT=Path(__file__).resolve().parents[1]

def write_json(path,data):path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def source_hash():return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in sorted((ROOT/'src').glob('*')) if p.is_file())).hexdigest()
def execute(out,stage,backend,progress=lambda *args:None):
    design=json.loads((ROOT/'design.json').read_text());plan=design['plans'][stage]
    if backend!=plan['backend']:raise ValueError('backend differs from frozen plan')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    cfg=design['cfg'];policy=ScriptedPolicy() if backend=='scripted' else AnthropicPolicy()
    assigned=[{'task_id':t,'world':w,'arm':a,'seed':1,'dose':1} for t in plan['tasks'] for w in plan['worlds'] for a in plan['arms']]
    manifest={'study':'immune-response-v3','stage':stage,'backend':backend,'model':policy.model,'model_backed':backend!='scripted','assigned':assigned,'config':cfg,'source_hash':source_hash(),'design_sha256':hashlib.sha256((ROOT/'design.json').read_bytes()).hexdigest(),'protocol_sha256':hashlib.sha256((ROOT/'preregistration.md').read_bytes()).hexdigest(),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'python':platform.python_version(),'started_unix':time.time()}
    write_json(out/'manifest.json',manifest)
    rows=[];start=time.monotonic()
    with (out/'events.jsonl').open('x') as journal,(out/'episodes.jsonl').open('x') as outcomes:
        for task in plan['tasks']:
            for world in plan['worlds']:
                def emit(event):
                    event.update(task_id=task,world=world,seed=1)
                    journal.write(json.dumps(event,sort_keys=True)+'\n');journal.flush()
                    if 'score' in event:os.fsync(journal.fileno());progress(event,len(rows),len(assigned))
                class Audited:
                    def complete(self,request,fallback):
                        if backend!='scripted':emit({'kind':'policy_request','request':request})
                        try:
                            result=policy.complete(request,fallback)
                            if backend!='scripted':emit({'kind':'policy_response','answer':result})
                            return result
                        except Exception as e:
                            emit({'kind':'policy_failure','error_type':type(e).__name__});raise
                try:batch=immune.run_episode(task,1,world,1,plan['arms'],cfg,Audited(),emit)
                except Exception as e:
                    batch=[dict(a,validity={'ok':False,'error_type':type(e).__name__},trajectory=[],evaluation={'utility':0,'failed_slots':None}) for a in assigned if a['task_id']==task and a['world']==world]
                for row in batch:
                    rows.append(row);outcomes.write(json.dumps(row,sort_keys=True)+'\n');outcomes.flush()
                os.fsync(outcomes.fileno())
    from analyze import summarize
    summary=summarize(rows,assigned)
    summary.update(model_backed=backend!='scripted',api_calls=policy.calls,actual_usd=getattr(policy,'actual_usd',0),usage_missing=getattr(policy,'usage_missing',0),seconds=round(time.monotonic()-start,3),source_hash=manifest['source_hash'])
    write_json(out/'summary.json',summary)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--stage',choices=['engineering','native-repair'],required=True);p.add_argument('--backend',choices=['scripted','anthropic'],required=True);a=p.parse_args()
    try:
        s=execute(a.out,a.stage,a.backend);print(json.dumps({k:s[k] for k in ['assigned','recorded','invalid','execution_qualified','api_calls','actual_usd']}))
    except Exception as e:print('Run failed: '+type(e).__name__);raise SystemExit(1)
