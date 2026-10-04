import json,sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import c1,contract
class C1Tests(unittest.TestCase):
 def test_exact_fixed_body(self):
  b=c1.body();self.assertTrue(contract.validate_wire(b));self.assertEqual(b['messages'][1]['content'],'Return {"ok":true}.');self.assertLessEqual(len(json.dumps(b).encode()),6500)
 def test_missing_authority_before_credential_read(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'receipt';p.write_text('{}')
   with patch.object(c1,'public_check') as public:
    with self.assertRaisesRegex(ValueError,'admission_attempt'):c1.relay(p,'missing-ledger','missing-key','missing-cap')
    public.assert_not_called()
 def test_original_ledger_single_attempt_uncertainty_and_no_reset(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'original.sqlite'
   with sqlite3.connect(p) as db:
    db.execute('CREATE TABLE calls(actual_usd REAL,reserved_usd REAL)');db.executemany('INSERT INTO calls VALUES(?,?)',[(.122835/44,.01)]*44)
    db.execute('CREATE TABLE r3_calls(id TEXT PRIMARY KEY,stage TEXT,reserved TEXT,actual TEXT,status TEXT)');db.execute("INSERT INTO r3_calls VALUES('Q3','Q3','0.02265',NULL,'ambiguous')")
   l=c1.Ledger(p,True);l.reserve();l.settle(None)
   with self.assertRaisesRegex(ValueError,'C1_already_attempted'):l.reserve()
   self.assertEqual(l.db.execute("SELECT reserved,actual,status FROM r3_calls WHERE stage='Q3'").fetchall(),[('0.02265',None,'ambiguous')]);l.db.close()
if __name__=='__main__':unittest.main()
