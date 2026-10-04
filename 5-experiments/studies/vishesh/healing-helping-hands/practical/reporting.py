"""Acknowledged reporting adapter. Host is configured by SWARM_HOST, not report()."""
import contextlib,io,json,time
from pathlib import Path
class ReportingFailure(RuntimeError):pass
class Reporter:
 def __init__(self,sdk,experiment,run,journal):
  self.sdk=sdk;self.experiment=experiment;self.run=run;self.journal=Path(journal)
 def emit(self,kind,**fields):
  # Explicitly forbid infrastructure fields unsupported by the SDK signature.
  if 'host' in fields:raise ValueError('host_must_use_environment')
  result={'kind':kind,'time':time.time()}
  with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
   try:
    acknowledged=self.sdk.report(kind,self.experiment,self.run,source='vishesh/codex-regrowth-docs',role='worker',strict=True,**fields)
    result['status']='acknowledged' if acknowledged else 'unacknowledged'
   except Exception as e:result.update(status='failed',error_type=type(e).__name__)
  with self.journal.open('a') as f:f.write(json.dumps(result)+'\n');f.flush()
  if result['status']!='acknowledged':raise ReportingFailure(result.get('error_type',result['status']))
  return True

def launch(out,parent,tldr,sdk):
 from execute import check,run
 if out.exists():raise FileExistsError('attempt_output_exists')
 receipt=check('healing-helping-hands',tldr)
 r=Reporter(sdk,'healing-helping-hands','healing-helping-hands/'+out.name+'-review',out.parent/(out.name+'-reporting.jsonl'))
 r.emit('start',url=receipt['url'],params={'attempt_id':out.name,'stage':'S0','arm':'analysis'},message=tldr)
 def progress(kind,d):
  if d['completed']%15==0:r.emit('metric',step=d['completed'],metrics={'completed_worlds':d['completed'],'assigned_worlds':d['assigned']})
 result=run(out,parent,tldr,progress,attempt=out.name,cap=16 if out.name=="practical-02" else 4)
 # Completion is finalized separately only after artifact audit/upload.
 r.emit('metric' if result['status']=='completed' else 'fail',metrics={'completed_worlds':result['terminal_counts'].get('completed',0)},message='Computation terminal; artifact reconciliation required.')
 return result
