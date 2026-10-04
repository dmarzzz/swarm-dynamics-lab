import copy,json,tempfile,unittest
import cases,controller
from native_provider import wire,validate_wire
class Cases(unittest.TestCase):
 def test_all_families_reference_and_diagnosis(self):
  for kind in cases.KINDS+cases.HOLDOUT_KINDS:
   for seed in range(100,110):
    c=cases.make(kind,seed);state=copy.deepcopy(c['initial']);trace=[];history=[]
    for tick in (1,2):
     o=cases.observe(c,state,tick,history,[]);d=cases.diagnosis(o);controller.validate_diagnosis(o,d);validate_wire(wire(controller.diagnosis_request(o)));validate_wire(wire(controller.action_request(c,o,d)))
     action=cases.reference(o);x=cases.f.step(c['fixture'],state,action);trace.append(x);history.append({'action':action,'result':x['result']})
    self.assertTrue(cases.gate(c,trace),(kind,seed))
 def test_stale_unknown_and_separate_stages(self):
  c=cases.make('masked_crash',123);o=cases.observe(c,c['initial'],1,[],[]);d=cases.diagnosis(o);self.assertEqual(d['fault'],'unknown');self.assertEqual(d['failed_service'],'none');self.assertNotIn('action_id',controller.diagnosis_request(o)['response_schema']['properties'])
  wrong=dict(d,fault='configuration');self.assertEqual(controller.action_request(c,o,wrong)['observation']['diagnosis'],wrong)
 def test_advice_changes_only_declared_note(self):
  for c in cases.development():
   for condition in ['none','correct','stale','incorrect']:
    o=cases.observe(c,c['initial'],1,[],cases.advice(c,condition));plain=cases.observe(c,c['initial'],1,[],[]);o['team_advice']=[];self.assertEqual(o,plain)
 def test_fixed_outcome_gates_fail_noop_crash(self):
  c=cases.make('worker_crash',123);state=copy.deepcopy(c['initial']);trace=[cases.f.step(c['fixture'],state,cases.f.action('wait')) for _ in range(2)];self.assertFalse(cases.gate(c,trace))
if __name__=='__main__':unittest.main()

class StageGates(unittest.TestCase):
 def exercise(self,fail=False,transport=False):
  import hashlib,os,run
  from pathlib import Path
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);packet=root/'packet.json';packet.write_text(json.dumps({m:[cases.make(k,300+i) for i,k in enumerate(cases.HOLDOUT_KINDS)] for m in ['sonnet','opus']}));(root/'holdout-seal.json').write_text(json.dumps({'sha256':hashlib.sha256(packet.read_bytes()).hexdigest()}));admission=root/'admission.json';admission.write_text(json.dumps({'commit':'abc'}));seen=[]
   class Fake:
    def __init__(self):
     self.model=os.environ['SWARM_ATTEMPT_ID'];self.calls=0;self.actual_usd=0;self.usage_missing=0;self.usage_path=root/(self.model+'.jsonl');self.usage_path.write_text('')
    def complete(self,req,_):
     self.calls+=1;seen.append(self.model)
     if transport:raise ValueError('transport')
     o=req['observation']
     if 'fault' in req['response_schema']['properties']:return cases.diagnosis(o)
     action=cases.reference(o)
     if fail and self.model.endswith('sonnet'):action=cases.f.action('wait')
     aid=next(k for k,v in o['legal_actions'].items() if all(v[x]==action[x] for x in ['action','service','version']))
     return {'action_id':aid,'reason':'offline test action'}
   with patch.object(run,'BASE',root),patch.object(run.subprocess,'check_output',return_value='abc'),patch.dict(os.environ,SWARM_A10_ADMISSION=str(admission)),patch('native_provider.NativePolicy',Fake):
    if transport:
     with self.assertRaises(ValueError):run.execute(root/'out',packet,'openrouter')
     self.assertEqual(seen,['controller-a10-sonnet']);return
    result=run.execute(root/'out',packet,'openrouter')
   return result,seen
 def test_pass_opens_advice_only(self):
  s,c=self.exercise();self.assertEqual(len(c),80);self.assertEqual(set(c),{'controller-a10-sonnet'});self.assertTrue(s['core_qualified']);self.assertEqual(s['recorded'],20)
 def test_fail_opens_opus_not_sonnet_holdout_or_advice(self):
  s,c=self.exercise(fail=True);self.assertEqual(c.count('controller-a10-sonnet'),16);self.assertEqual(c.count('controller-a10-opus'),32);self.assertEqual(s['recorded'],12);self.assertTrue(s['core_qualified'])
 def test_transport_does_not_escalate(self):self.exercise(transport=True)
