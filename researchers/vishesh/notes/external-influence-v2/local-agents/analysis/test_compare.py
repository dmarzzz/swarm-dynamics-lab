import contextlib,copy,io,json,tempfile,unittest
from pathlib import Path
from compare import compare
class CompareTests(unittest.TestCase):
 def setup_files(self,root):
  old=root/'old';new=root/'new';old.mkdir();new.mkdir()
  row={'domain':'procurement','task_id':7100,'seed':17,'world':'clean','dose':0,'n_agents':9,'verification':'fresh','arm':'private_review','truth_hash':'t','corpus_hash':'c','exposure_hash':'e','choice':'A','validity':{'ok':True},'evaluation':{'correct':1,'harmful_target':0,'regret':0}}
  (old/'manifest.json').write_text(json.dumps({'model':'claude-haiku-4-5-20251001','params':{'stage':'S1'},'git_commit':'source'}))
  (old/'episodes.jsonl').write_text(json.dumps(row)+'\n');(new/'episodes.jsonl').write_text(json.dumps(row)+'\n')
  return old,new,row
 def test_invalid_is_not_zero_harm(self):
  with tempfile.TemporaryDirectory() as td:
   old,new,row=self.setup_files(Path(td));row.update(validity={'ok':False},evaluation={'correct':0,'harmful_target':None,'regret':100});row.pop('choice')
   (new/'episodes.jsonl').write_text(json.dumps(row)+'\n')
   with contextlib.redirect_stdout(io.StringIO()):v=compare(new,old)
   self.assertEqual(v['correct_delta'],-1);self.assertEqual(v['local']['harmful_unknown'],1);self.assertEqual(v['historical_only_correct'],1)
 def test_fixture_mismatch_stops_comparison(self):
  with tempfile.TemporaryDirectory() as td:
   old,new,row=self.setup_files(Path(td));row['truth_hash']='different';(new/'episodes.jsonl').write_text(json.dumps(row)+'\n')
   with self.assertRaises(ValueError):compare(new,old)
 def test_duplicate_assignment_stops_comparison(self):
  with tempfile.TemporaryDirectory() as td:
   old,new,row=self.setup_files(Path(td));(new/'episodes.jsonl').write_text((json.dumps(row)+'\n')*2)
   with self.assertRaises(ValueError):compare(new,old)
 def test_scripted_is_not_historical_model(self):
  with tempfile.TemporaryDirectory() as td:
   old,new,row=self.setup_files(Path(td));(old/'manifest.json').write_text(json.dumps({'model':'scripted-observation-policy-v1'}))
   with self.assertRaises(ValueError):compare(new,old)
if __name__=='__main__':unittest.main()
