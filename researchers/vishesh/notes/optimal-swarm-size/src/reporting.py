"""Bounded hub delivery; no client diagnostics or private URLs enter records.

Client contract: report() is True only when sent; False may mean spooled.
upload() returns an acknowledgment dict, or a dict with spooled=True.
Each operation runs in a child terminated at 30 seconds. An ambiguous timeout
remains unconfirmed, even if the hub eventually accepted it. No implicit replay.
"""
import contextlib
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import time
import urllib.request
from failures import SafeFailure

@contextlib.contextmanager
def quiet_client():
    with open(os.devnull,'w') as sink,contextlib.redirect_stderr(sink),contextlib.redirect_stdout(sink):yield


def delivery_child(connection, operation, experiment, run, payload):
    try:
        with quiet_client():
            import swarm_report as sr
            if operation == 'artifact':
                result=sr.upload(run,payload['path'],payload['name'])
                acknowledged=isinstance(result,dict) and bool(result) and not result.get('spooled',False)
                spooled=isinstance(result,dict) and result.get('spooled') is True
            else:
                result=sr.report(operation,experiment,run,**payload)
                acknowledged=result is True;spooled=False
        connection.send({'acknowledged':acknowledged,'spooled':spooled,'code':None if acknowledged else 'reporting_failed'})
    except Exception:
        connection.send({'acknowledged':False,'spooled':False,'code':'reporting_failed'})
    finally:connection.close()


def deliver(operation,experiment,run,payload):
    ctx=multiprocessing.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
    proc=ctx.Process(target=delivery_child,args=(child,operation,experiment,run,payload),daemon=True)
    try:
        proc.start();child.close()
        if not parent.poll(30):return {'acknowledged':False,'spooled':False,'code':'reporting_timeout'}
        return parent.recv()
    except Exception:return {'acknowledged':False,'spooled':False,'code':'reporting_failed'}
    finally:
        if proc.pid:
            if proc.is_alive():proc.terminate()
            proc.join(timeout=2)
        parent.close();child.close()


class Reporter:
    def __init__(self,experiment,row,tldr):
        self.experiment=experiment;self.id=experiment+'/'+hashlib.sha256(row['id'].encode()).hexdigest()[:16]
        self.total=row.get('width',16)
        if type(self.total) is not int or self.total<1:raise ValueError('invalid_progress_total')
        self.last_progress=0
        result=deliver('start',experiment,self.id,{'params':row|{'tldr':tldr},'message':tldr})
        if not result['acknowledged']:raise SafeFailure('hub_registration_failed')
        try:
            request=urllib.request.Request('https://swarm-live.pages.dev/api/runs/'+self.id,headers={'User-Agent':'SwarmLab-PlanPreflight/1.0'})
            with urllib.request.urlopen(request,timeout=20) as response:public=json.load(response)
            if not isinstance(public,dict) or public.get('params',{}).get('tldr')!=tldr:raise ValueError()
        except Exception:
            deliver('fail',experiment,self.id,{'message':'Public run preflight failed; no model calls dispatched.'})
            raise SafeFailure('public_run_preflight_failed') from None

    def progress(self,completed):
        # Coalesce frequent item completions; suppressed updates are not delivery failures.
        now=time.monotonic()
        if now-self.last_progress<2 and completed!=self.total:return {'acknowledged':False,'coalesced':True,'code':None}
        self.last_progress=now
        return deliver('progress',self.experiment,self.id,{'step':completed,'total':self.total,'message':'Measured qualification work-item completion','metrics':{'completed_items':completed}})

    def finish(self,target,record):
        target=Path(target);receipt={'run':self.id,'complete':False,'artifacts':{},'terminal':None}
        path=target/'publication.json'
        def save():
            pending=path.with_suffix('.tmp');pending.write_text(json.dumps(receipt,indent=2)+'\n');pending.replace(path)
        save()
        for name in ('assignment.json','trace.jsonl','outcome.json','replay.html'):
            if not (target/name).exists():receipt['artifacts'][name]={'acknowledged':False,'code':'missing_artifact'}
            else:receipt['artifacts'][name]=deliver('artifact',self.experiment,self.id,{'path':str(target/name),'name':name})
            save()
        uploaded=all(v.get('acknowledged') is True for v in receipt['artifacts'].values())
        metrics={'quality':record['evaluation']['quality'],'success':int(record['operational_success']),
                 'elapsed_s':record['elapsed_s'],'cost_exposure_usd':record['exposure_microdollars']/1000000}
        failed=bool(record['failure']) or not uploaded
        receipt['terminal']=deliver('fail' if failed else 'done',self.experiment,self.id,
            {'message':'Qualification execution or publication incomplete; local evidence retained.' if failed else 'Qualification execution complete; success is reported separately.','metrics':metrics})
        receipt['complete']=uploaded and receipt['terminal'].get('acknowledged') is True
        save();return receipt
