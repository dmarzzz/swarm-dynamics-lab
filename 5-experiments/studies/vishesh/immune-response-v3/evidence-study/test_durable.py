import json,os,sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import study_receipts
from durable_provider import DurablePolicy
class DurableTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.ledger=self.root/'budget.sqlite'
  with sqlite3.connect(self.ledger) as db:
   db.execute('CREATE TABLE budget (id INTEGER PRIMARY KEY, cap REAL, reserved REAL, calls INTEGER)');db.execute('INSERT INTO budget VALUES (1,8,2.059367,267)')
  self.env=patch.dict(os.environ,{'SWARM_MODEL_CONFIG_FILE':str(study_receipts.ROOT/'model-config.json'),'SWARM_MODEL_BASE_URL':'https://api.anthropic.com/v1','SWARM_MODEL_API_KEY':'offline-test-placeholder','SWARM_BUDGET_LEDGER':str(self.ledger),'SWARM_ATTEMPT_ID':'offline','SWARM_USAGE_LOG':str(self.root/'usage.jsonl')});self.env.start()
 def tearDown(self):self.env.stop();self.tmp.cleanup()
 def test_existing_ledger_required(self):
  self.ledger.unlink()
  with self.assertRaisesRegex(ValueError,'existing_budget'):DurablePolicy()
 def test_reservation_survives_interruption(self):
  p=DurablePolicy();rid=p.reserve(b'{}')
  with sqlite3.connect(self.ledger) as db:
   self.assertEqual(db.execute('SELECT calls FROM budget').fetchone()[0],268)
   self.assertEqual(db.execute('SELECT state FROM immune_requests').fetchone()[0],'reserved_unresolved')
  self.assertEqual(json.loads((self.root/'usage.jsonl').read_text())['request_id'],rid)
  with self.assertRaisesRegex(ValueError,'attempt_already'):DurablePolicy()
 def test_usage_before_output_validation(self):
  p=DurablePolicy();rid=p.reserve(b'{}');p.finish(rid,'response_received',{'input_tokens':100,'output_tokens':20})
  row=json.loads((self.root/'usage.jsonl').read_text());self.assertAlmostEqual(row['actual_usd'],.0002);self.assertEqual(p.usage_missing,0)
 def test_missing_usage_not_zero_cost(self):
  p=DurablePolicy();rid=p.reserve(b'{}');p.finish(rid,'http_500');row=json.loads((self.root/'usage.jsonl').read_text());self.assertIsNone(row['actual_usd']);self.assertEqual(p.usage_missing,1)
 def test_cap_not_reset(self):
  with sqlite3.connect(self.ledger) as db:db.execute('UPDATE budget SET reserved=8')
  p=DurablePolicy()
  with self.assertRaisesRegex(ValueError,'persistent_budget'):p.reserve(b'{}')
  with sqlite3.connect(self.ledger) as db:self.assertEqual(db.execute('SELECT calls FROM budget').fetchone()[0],267)
if __name__=='__main__':unittest.main()
