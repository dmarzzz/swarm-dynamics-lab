import contextlib,io,json,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import live_worker as w
import native as n
from instrument import deterministic
class FakeRun:
 def __init__(self,id,experiment,params):self.params=params;self._alive=types.SimpleNamespace(set=lambda:None)
 def progress(self,*a,**k):return True
 def artifact(self,*a,**k):return {'uploaded':True}
 def done(self,*a,**k):return True
 def fail(self,*a,**k):return True
class Worker(unittest.TestCase):
 def exercise(self,fail=False,ack=True):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);config=root/'config.json';key=root/'fixture-credential';key.write_text('nonsecret-test-fixture');key.chmod(0o600)
   c={'host':'unit-test-host','run_id':'fixture','run_tldr':'software fixture','source_commit':'fixture','plan_url':'fixture','plan_sha256':'fixture'};config.write_text(json.dumps(c));calls=[]
   class Opener:
    def open(self,req,timeout):
     calls.append(1)
     if fail:raise TimeoutError()
     req=json.loads(req.data);m=deterministic(req['state'])['map']
     raw={'model':n.SNAPSHOT,'provider':'TypeSafe','usage':{'cost':.001,'input_tokens':100,'output_tokens':100},'answers':{}}
     for cell,label in m.items():raw['answers']['cell_'+cell.replace(',','_')]={'type':'choice','choice':label,'confidence':1,'probabilities':{k:int(k==label) for k in n.CRITERIA}}
     return io.BytesIO(json.dumps(raw).encode())
   sr=types.SimpleNamespace(Run=FakeRun,report=lambda *a,**k:ack)
   pp=types.SimpleNamespace(check=lambda *a,**k:{'url':'fixture','plan_sha256':'fixture'})
   renderer=types.SimpleNamespace(render=lambda *a,**k:None)
   args=types.SimpleNamespace(config=config,credential_file=key,stage='Q0',out=root/'out',ledger=root/'ledger')
   with patch.dict(sys.modules,{'swarm_report':sr,'public_plan':pp,'live_render':renderer}),patch.object(w.subprocess,'check_output',return_value=str(root)),patch.object(w,'verify_config',return_value=2),patch.object(w,'check_route',return_value={}),patch.object(w.urllib.request,'build_opener',return_value=Opener()),contextlib.redirect_stdout(io.StringIO()):
    if not ack:
     with self.assertRaisesRegex(ValueError,'hub_start_unacknowledged'):w.run(args)
     self.assertEqual(len(calls),0);return
    w.run(args)
   return json.loads((args.out/'summary.json').read_text()),json.loads((args.out/'records.json').read_text()),len(calls)
 def test_successful_offline_pipeline(self):
  summary,rows,calls=self.exercise();self.assertEqual(calls,18);self.assertTrue(summary['qualification_passed']);self.assertEqual(len(rows),18)
 def test_failures_stop_and_preserve_assignments(self):
  summary,rows,calls=self.exercise(fail=True);self.assertEqual(calls,5);self.assertFalse(summary['qualification_passed']);self.assertEqual(sum(r['status']=='not-started' for r in rows),13)
  self.assertAlmostEqual(summary['budget']['cost_with_unresolved_reservations_usd'],5*n.RESERVE_NANO/1e9)
 def test_hub_ack_before_paid_dispatch(self):self.exercise(ack=False)
