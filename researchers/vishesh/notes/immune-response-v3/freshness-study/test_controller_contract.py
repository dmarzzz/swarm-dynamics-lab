import copy,itertools,json,tempfile,unittest
from pathlib import Path
import jsonschema
import freshness as f
import controller_contract as c
import qualification as q
import qualification_audit
class ControllerContract(unittest.TestCase):
 def test_exact_legal_language_and_engine_across_all_cases(self):
  for case in f.CASES:
   fixture,state=f.fixture(case,9401);old=jsonschema.Draft202012Validator(f.legacy_schema(fixture));new=jsonschema.Draft202012Validator(c.schema(fixture));mapping=c.legal_actions(fixture)
   self.assertEqual(len(mapping),10);self.assertEqual(len({json.dumps(v,sort_keys=True) for v in mapping.values()}),10)
   self.assertNotIn('anyOf',json.dumps(c.schema(fixture)))
   for kind,service,version in itertools.product(['deploy','inspect','refresh','wait','bogus'],list(fixture['alias'].values())+['none','bogus'],[-1,0,1,2,3,4,True]):
    action=f.action(kind,service,version,'Keep this exact reason.');valid=old.is_valid(action)
    if not valid:
     with self.assertRaises(ValueError):c.encode(fixture,action)
     continue
    wire=c.encode(fixture,action);self.assertTrue(new.is_valid(wire));decoded=c.decode(fixture,wire);self.assertEqual(decoded,action)
    self.assertEqual(f.step(fixture,copy.deepcopy(state),decoded),f.step(fixture,copy.deepcopy(state),action))
 def test_malformed_responses_never_become_default_actions(self):
  fixture,_=f.fixture('healthy_fresh',9401)
  for value in [None,[],{},f.action('inspect'),{'action_id':'inspect','reason':1},{'action_id':1,'reason':'x'},{'action_id':'inspect','reason':'x','version':0},{'action_id':'deploy:gateway-1:3','reason':'x'},{'action_id':'INSPECT','reason':'x'},{'action_id':' inspect','reason':'x'}]:
   with self.assertRaises(ValueError):c.decode(fixture,value)
 def test_mapping_only_added_to_controller_observation(self):
  fixture,state=f.fixture('healthy_fresh',9401);obs=f.observe(fixture,state,1,[],[],False);before=copy.deepcopy(obs);request=f.controller_request(fixture,obs)
  self.assertEqual(obs,before);self.assertNotIn('legal_actions',obs);self.assertEqual(request['observation']['legal_actions'],c.legal_actions(fixture))
 def test_scripted_qualification_retains_raw_decoded_and_replays(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/'out';result=q.execute(out,'scripted');self.assertTrue(result['qualification_passed']);audit=qualification_audit.audit(out);self.assertEqual(audit['complete_episodes'],6)
   events=[json.loads(s) for s in (out/'events.jsonl').read_text().splitlines()];raw=[x for x in events if x['kind']=='decision_response'];decoded=[x for x in events if x['kind']=='decoded_action'];self.assertEqual(len(raw),12);self.assertEqual(len(decoded),12)
   for x,y in zip(raw,decoded):
    fixture,_=f.fixture(x['case'],9401);self.assertEqual(c.decode(fixture,x['response']),y['action'])
 def test_historical_live_entrypoints_cannot_spend_with_changed_contract(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/'out'
   from unittest.mock import patch
   with patch.dict('os.environ',{},clear=True),self.assertRaises(KeyError):q.execute(out,'openrouter')
   with self.assertRaisesRegex(ValueError,'requires_native_admission'):f.execute(out,'openrouter',9401,'freshness-a5')
   self.assertFalse(out.exists())
if __name__=='__main__':unittest.main()
