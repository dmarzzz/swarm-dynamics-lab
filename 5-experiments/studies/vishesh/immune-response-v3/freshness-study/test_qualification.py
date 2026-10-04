import json,tempfile,unittest
from pathlib import Path
import qualification as q
class QualificationTests(unittest.TestCase):
 def test_full_visible_reference_grid_and_denominators(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'out';d=q.execute(p,'scripted');self.assertTrue(d['qualification_passed']);self.assertEqual(d['recorded'],6)
   ev=[json.loads(l) for l in (p/'events.jsonl').read_text().splitlines()];self.assertEqual(sum(e['kind']=='advice_response' for e in ev),6);self.assertEqual(sum(e['kind']=='decision_response' for e in ev),12)
   for e in ev:
    if 'request' in e:self.assertNotIn('case',e['request']['observation']);self.assertLessEqual(e['request']['observation']['ticks_remaining'],2)
 def test_wrong_actions_cannot_pass_on_explanation(self):
  f,s=q.f.fixture('healthy_fresh',9401);trace=[]
  for t in [1,2]:trace.append(q.f.step(f,s,q.f.action('deploy',f['alias']['gateway'],1,'Waiting is safest')))
  self.assertFalse(q.gate({'case':'healthy_fresh','trace':trace}))
 def test_inspect_without_crash_repair_fails(self):
  f,s=q.f.fixture('fresh_crash',9401);t=[q.f.step(f,s,q.f.action('inspect')) for _ in [1,2]];self.assertFalse(q.gate({'case':'fresh_crash','trace':t}))
if __name__=='__main__':unittest.main()
