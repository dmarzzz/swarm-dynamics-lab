import hashlib,json,sqlite3,tempfile,time,unittest
from native import validate_admission,haiku_validate,reserve
from design import HERE,HSNAPSHOT,HMODEL
class NativeTests(unittest.TestCase):
 def receipt(self):
  return dict(account_verified=True,exclusive_claim_verified=True,workload_verified=True,source_verified=True,public_plan_verified=True,scope_authorized=True,stage='D0',checked_epoch=1000,expires_epoch=10000,plan_sha256=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest())
 def test_missing_gate_and_staleness(self):
  a=self.receipt();self.assertTrue(validate_admission(a,'D0',1100))
  for field in ('account_verified','exclusive_claim_verified','public_plan_verified','scope_authorized'):
   b=dict(a);b[field]=False
   with self.assertRaises(ValueError):validate_admission(b,'D0',1100)
  with self.assertRaises(ValueError):validate_admission(a,'D0',1400)
 def test_paid_increase_required(self):
  a=self.receipt();a['stage']='S0'
  with self.assertRaises(ValueError):validate_admission(a,'S0',1100)
 def test_main_needs_actual_review(self):
  a=self.receipt();a.update(stage='S1',cumulative_cap_usd=50.,c6_cap_usd=3.,budget_increase_approved=True,original_ledger_verified=True)
  with self.assertRaises(ValueError):validate_admission(a,'S1',1100)
 def valid(self):return {'model':HMODEL,'provider':'Anthropic','choices':[{'finish_reason':'stop','message':{'content':'{"label":"SUPPORT"}'}}],'usage':{'cost':.0002,'prompt_tokens':150,'completion_tokens':7}}
 def test_model_provider_and_truncation(self):
  x=self.valid();self.assertEqual(haiku_validate(x)['label'],'SUPPORT')
  for key,val in [('model','wrong'),('provider','Azure')]:
   x=self.valid();x[key]=val
   with self.assertRaises(ValueError):haiku_validate(x)
  x=self.valid();x['choices'][0]['finish_reason']='length'
  with self.assertRaises(ValueError):haiku_validate(x)
 def db(self):
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');db.execute('CREATE TABLE c6_hashes(hash TEXT PRIMARY KEY,stage TEXT)')
  db.executemany('INSERT INTO calls VALUES(?,?,?,?)',[(str(i),1,'completed',.05/2731) for i in range(2731)]);db.commit();return db
 def test_original_ledger_duplicate_and_cap(self):
  db=self.db();reserve(db,'new',.001,'S0')
  with self.assertRaises(sqlite3.IntegrityError):reserve(db,'new',.001,'S0')
  with self.assertRaises(ValueError):reserve(db,'excess',3.01,'S0')
  self.assertEqual(db.execute('SELECT count(*) FROM calls').fetchone()[0],2732)
 def test_absent_history_blocks(self):
  db=self.db();db.execute('DELETE FROM calls');db.commit()
  with self.assertRaises(ValueError):reserve(db,'new',.001,'S0')
if __name__=='__main__':unittest.main()
