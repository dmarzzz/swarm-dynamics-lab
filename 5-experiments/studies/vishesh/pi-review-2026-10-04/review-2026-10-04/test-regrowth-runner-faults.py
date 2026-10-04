"""Isolated runner fault injections using dummy policies only; no model or network calls."""
import contextlib,io,json,pathlib,sys,tempfile
from unittest.mock import patch
R=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'regrowth-200/src'))
import run
class DummyQwen:
 def __init__(self):self.calls=0
 def __call__(self,obs):self.calls+=1;return 'WAIT',{}
class DummyLaya:
 def __init__(self,calls=0,fail=False):self.calls=calls;self.fail=fail
 def __call__(self,obs,proposal):
  self.calls+=1
  if self.fail:raise ConnectionError('synthetic failure')
  return 'WAIT',{}
results={}
with tempfile.TemporaryDirectory() as td:
 laya=DummyLaya(calls=3999)
 with contextlib.redirect_stdout(io.StringIO()):
  try:run.run_world('hybrid',False,DummyQwen(),laya,pathlib.Path(td),float('inf'))
  except RuntimeError as e:results['laya_cap']={'exception':str(e),'cap':4000,'actual_calls':laya.calls,'overshoot':laya.calls-4000}
with tempfile.TemporaryDirectory() as td:
 laya=DummyLaya(fail=True)
 with contextlib.redirect_stdout(io.StringIO()),patch.object(run.time,'monotonic',side_effect=[0.,0.,2.]):
  try:run.run_world('hybrid',False,DummyQwen(),laya,pathlib.Path(td),1.)
  except TimeoutError as e:results['laya_failure_streak']={'exception':str(e),'consecutive_laya_failures_not_stopped':laya.calls}
print(json.dumps(results,indent=2))
(R/'review-2026-10-04/regrowth-runner-faults.json').write_text(json.dumps(results,indent=2)+'\n')
