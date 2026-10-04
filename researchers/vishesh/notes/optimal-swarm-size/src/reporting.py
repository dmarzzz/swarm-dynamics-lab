"""Hub reporting wrapper. The installed client consumes host credentials privately."""
import contextlib
import hashlib
import json
import os
import time
import urllib.request

@contextlib.contextmanager
def quiet_client():
    # Existing client diagnostics can contain private hub addresses; suppress them at source.
    with open(os.devnull,'w') as sink,contextlib.redirect_stderr(sink),contextlib.redirect_stdout(sink):yield

class Reporter:
    def __init__(self,experiment,row,tldr):
        import swarm_report as sr
        self.sr=sr;self.id=experiment+'/'+hashlib.sha256(row['id'].encode()).hexdigest()[:16]
        with quiet_client():
            self.run=sr.start(experiment,run=self.id,params=row|{'tldr':tldr},message=tldr)
            if not self.run.progress(step=0,total=16,message=tldr,force=True):raise RuntimeError('hub_registration_failed')
        # A run-specific public registration check precedes any actor call.
        try:
            with urllib.request.urlopen(urllib.request.Request('https://swarm-live.pages.dev/api/runs/'+self.id,headers={'User-Agent':'SwarmLab-PlanPreflight/1.0'}),timeout=20) as response:
                public=json.load(response)
            record=public if isinstance(public,dict) else {}
            if not isinstance(record,dict) or record.get('params',{}).get('tldr')!=tldr:
                raise ValueError('public_run_tldr_unverified')
        except Exception:
            with quiet_client():self.run.fail('Public run preflight failed; no model calls dispatched.')
            raise RuntimeError('public_run_preflight_failed') from None
    def progress(self,completed):
        with quiet_client():self.run.progress(step=completed,total=16,message='Measured qualification work-item completion',completed_items=completed)
    def finish(self,target,record):
        with quiet_client():
            for name in ('assignment.json','trace.jsonl','outcome.json','replay.html'):
                if (target/name).exists():self.run.artifact(str(target/name),name)
            metrics={'quality':record['evaluation']['quality'],'success':int(record['operational_success']),
                     'elapsed_s':record['elapsed_s'],'cost_exposure_usd':record['exposure_microdollars']/1000000}
            if record['failure']:self.run.fail('Qualification execution failure; artifacts retained.',**metrics)
            else:self.run.done('Qualification execution complete; success is reported separately.',**metrics)
