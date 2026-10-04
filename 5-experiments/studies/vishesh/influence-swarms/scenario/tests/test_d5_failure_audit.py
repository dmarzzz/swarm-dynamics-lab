"""Saved failure evidence must not be promoted to usage or behavioral evidence."""
import importlib.util,json,tarfile,tempfile,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('failure_audit',BASE/'analysis/d5_failure_audit.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class FailureAudit(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  with tarfile.open(BASE/'reviews/native-D5-01/native-artifacts.tar.gz') as t:
   for f in t.getmembers():
    if f.isfile() and '/' not in f.name:(self.root/f.name).write_bytes(t.extractfile(f).read())
 def tearDown(self):self.tmp.cleanup()
 def test_all_failed_is_not_zero_cost_or_bad_decisions(self):
  r=m.audit(self.root);self.assertIsNone(r['actual_cost_usd']);self.assertIsNone(r['source_grades_agree']);self.assertEqual(r['source_grades_assessed'],0);self.assertFalse(r['scientific_contrasts_estimable']);self.assertFalse(r['usage_coverage_complete'])
 def test_missing_request_rejected(self):
  p=self.root/'events-0.jsonl';lines=p.read_text().splitlines();p.write_text('\n'.join(lines[1:])+'\n')
  with self.assertRaises(AssertionError):m.audit(self.root)
 def test_attempt_counter_mismatch_rejected(self):
  p=self.root/'summary.json';v=json.loads(p.read_text());v['calls']=47;p.write_text(json.dumps(v))
  with self.assertRaises(AssertionError):m.audit(self.root)
