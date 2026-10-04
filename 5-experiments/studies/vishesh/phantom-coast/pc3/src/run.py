"""PC-3 single live entry point. No resume, retries or credential fallback."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.request
from admission import Admission,BASE,fingerprint
from contract import _world
from design import STAGES,family,schedule
from wire import SNAPSHOT,digest,canonical
from ledger import Ledger
from engine import Engine,save
PARENT=BASE.parent
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k):raise ValueError('redirect_refused')

def check_route(opener):
    with opener.open('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=25) as r:data=json.load(r)['data']
    routes=data.get('endpoints',[])
    if len(routes)!=1:raise ValueError('route_count')
    r=routes[0];p=r['pricing']
    if r['provider_name']!='TypeSafe' or r['tag']!='typesafe' or r['status']!=0 or SNAPSHOT not in r['name']:raise ValueError('route_changed')
    if float(p['prompt'])>0.000000042 or float(p['completion'])!=0 or float(p.get('request',0))!=0 or r['context_length']>32000:raise ValueError('price_or_context_changed')
    return dict(snapshot=SNAPSHOT,provider='TypeSafe',input_rate=float(p['prompt']),output_rate=0)



def quiet(fn,*a,**kw):
    with open(os.devnull,'w') as sink,contextlib.redirect_stdout(sink),contextlib.redirect_stderr(sink):return fn(*a,**kw)

def prepare(stage):
    return dict(design='PC-3',stage=stage,assignments=schedule(stage),assignment_sha256=digest(schedule(stage)),instrument=fingerprint(),native_calls=0,admission='not granted')

def run(config,out,credential):
    c=json.loads(config.read_text())
    sys.path.insert(0,str(PARENT.parent/'experiment-documentation'));import public_plan
    admit=Admission(c,c['stage'],public_plan.check)
    # The existing ledger must be provisioned and lineage-verified before receipt issuance.
    ledger=Ledger(c['ledger_path'],c['predecessor_sha256'])
    try:return execute(c,out,credential,admit,ledger)
    finally:ledger.db.close()

def execute(c,out,credential,admit,ledger):
    if credential.is_symlink() or credential.stat().st_mode&0o077:raise ValueError('credential_permissions')
    key=credential.read_text().strip()
    if not key:raise ValueError('credential_absent')
    ledger.claim(c['stage'],c['attempt'])  # Credential checked before durable claim, dispatch still fenced.
    opener=urllib.request.build_opener(NoRedirect());route=check_route(opener)
    os.environ.update(SWARM_SOURCE='vishesh/codex-phantom-coast',SWARM_HOST=c['host'])
    import swarm_report as sr
    hub=sr.Run('phantom-coast-pc3/'+c['attempt'],'phantom-coast-pc3',{'stage':c['stage'],'design':'PC-3','source':c['source_commit']})
    if quiet(sr.report,'start','phantom-coast-pc3','phantom-coast-pc3/'+c['attempt'],params=hub.params,message=c['run_tldr'],strict=True) is not True:
        if hasattr(hub,'_alive'):hub._alive.set()
        raise ValueError('start_unacknowledged')
    def transport(req):
        if not admit.current():raise ValueError('admission_expired')
        wire=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',canonical(req).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        with opener.open(wire,timeout=45) as response:return json.loads(response.read(1_000_000))
    def progress(n,total,b):quiet(hub.progress,n,total,cost_usd=b['cumulative_exposure_usd'])
    try:
        worlds={seed:_world(seed,family(seed)) for seed in STAGES[c['stage']]}
        engine=Engine(c['stage'],c['attempt'],out,ledger,transport,worlds,admit,progress)
        save(out/'public-plan.json',admit.public);save(out/'route.json',route)
        summary=engine.run();summary.update(instrument=fingerprint(),model=SNAPSHOT,source_commit=c['source_commit']);save(out/'summary.json',summary)
        if c['stage']=='S1':
            from replay import render
            render(out)
        for p in out.iterdir():
            if p.suffix in ('.json','.jsonl','.png','.gif','.html'):
                ack=quiet(hub.artifact,str(p),p.name)
                if not isinstance(ack,dict) or ack.get('spooled'):raise ValueError('artifact_unacknowledged')
        quiet(hub.done,message='PC-3 execution reconciled; review summary for qualification and missing outcomes',assigned=summary['assigned'],valid=summary['valid'],cost_usd=summary['budget']['cumulative_exposure_usd'])
        return summary
    except Exception as exc:
        if out.is_dir():save(out/'worker-failure.json',{'error_type':type(exc).__name__})
        quiet(hub.fail,message='PC-3 worker failure: '+type(exc).__name__);raise
    finally:
        hub._alive.set()

if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='operation',required=True)
    q=sub.add_parser('prepare');q.add_argument('--stage',choices=['Q0','S1'],required=True);q.add_argument('--output',type=Path,required=True)
    q=sub.add_parser('run');q.add_argument('--config',type=Path,required=True);q.add_argument('--out',type=Path,required=True);q.add_argument('--credential-file',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.operation=='prepare':
            with a.output.open('x') as f:json.dump(prepare(a.stage),f,indent=2)
            print('Prepared assignments only; no worlds opened and no launch admitted.')
        else:
            result=run(a.config,a.out,a.credential_file);print(json.dumps({k:result[k] for k in ('stage','assigned','valid','stop_reason')}))
    except Exception as exc:print(json.dumps({'blocked_or_failed':type(exc).__name__}));raise SystemExit(1)
