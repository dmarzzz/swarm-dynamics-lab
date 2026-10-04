import copy,json,tempfile,unittest
from pathlib import Path
import freshness as f
import grounded_study as study
import grounding
from openrouter_provider import wire,validate_wire
class Grounding(unittest.TestCase):
 def test_stale_liveness_unknown_current_crash_visible(self):
  for case in f.CASES:
   fixture,state=f.fixture(case,9401);o=f.observe(fixture,state,1,[],[],True);e=grounding.evidence(o)
   self.assertEqual({k:v['value'] for k,v in e['catalog_comparisons'].items()},f.prior.health(fixture,state['deployed']))
   self.assertEqual(e['current_liveness'],state['live'] if o['cached_probe']['epoch']==o['current_epoch'] else None)
 def test_conflicting_probe_is_exposed_not_overwritten(self):
  fixture,state=f.fixture('healthy_fresh',9401);o=f.observe(fixture,state,1,[],[],True);o['cached_probe']['checks']['rpc_compatible']=False;o['cached_probe']['checks']['processes_live']=False
  e=grounding.evidence(o);self.assertEqual(set(e['current_probe_disagreements']),{'rpc_compatible','processes_live'});self.assertTrue(e['catalog_comparisons']['rpc_compatible']['value'])
 def test_catalog_mutations_follow_visible_input(self):
  fixture,state=f.fixture('healthy_fresh',9401);o=f.observe(fixture,state,1,[],[],True)
  for field,role,attribute,value in [('rpc_compatible','gateway','requires_rpc','wrong'),('data_readable','worker','reads',[]),('storage_format','store','format','wrong'),('requested_feature','gateway','features',[])]:
   changed=copy.deepcopy(o);service=o['roles_to_services'][role];version=str(o['deployed'][service]);changed['catalog'][service][version][attribute]=value;e=grounding.evidence(changed)
   self.assertFalse(e['catalog_comparisons'][field]['value']);self.assertIn(field,e['current_probe_disagreements'])
 def test_factorial_isolation_no_action_filtering_or_advisor_rewrite(self):
  packet=json.loads((study.BASE/'grounding-advice.json').read_text())
  for case in study.q.CASES:
   fixture,state=f.fixture(case,9401);advice=packet['advice'][case];original=copy.deepcopy(advice);requests={c:study.request(fixture,state,1,[],advice,c) for c in study.CONDITIONS}
   for c,r in requests.items():
    validate_wire(wire(r));self.assertEqual(r['response_schema'],f.schema(fixture));self.assertEqual(r['instructions'],requests['plain_solo']['instructions'])
    o=copy.deepcopy(r['observation']);o.pop('evidence_table',None);o['team_advice']=[]
    self.assertEqual(o,requests['plain_solo']['observation'])
   self.assertEqual(advice,original);self.assertEqual(len(requests['grounded_advice']['observation']['legal_actions']),10)
 def test_reference_passes_same_gates_and_replays(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/'out';s=study.execute(out);self.assertEqual(s['model_calls'],0);self.assertEqual(s['capability_passes'],12)
   for row in [json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()]:
    fixture,state=f.fixture(row['case'],row['seed'])
    for x in row['trace']:
     replay=f.step(fixture,state,x['action'])
     for key,value in replay.items():self.assertEqual(x[key],value)
if __name__=='__main__':unittest.main()

class NativeAdmission(unittest.TestCase):
 def test_no_admission_no_native_output_or_call(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as td,patch.dict('os.environ',{},clear=True):
   out=Path(td)/'out'
   with self.assertRaises(KeyError):study.execute(out,'openrouter')
   self.assertFalse(out.exists())
 def test_worker_import_in_fresh_process(self):
  import subprocess,sys
  r=subprocess.run([sys.executable,'-c','import grounded_worker'],cwd=study.BASE,capture_output=True);self.assertEqual(r.returncode,0)
