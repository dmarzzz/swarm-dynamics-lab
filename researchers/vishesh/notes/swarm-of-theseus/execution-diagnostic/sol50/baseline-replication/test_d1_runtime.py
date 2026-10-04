import json,sqlite3,tempfile,unittest
from pathlib import Path
import d1_runtime as r,selection_v2 as s
class D1Tests(unittest.TestCase):
 def test_unfunded_before_access(self):
  with self.assertRaisesRegex(ValueError,'unfunded'):r.admit({}, {}, 'not-funded')
 def test_wrong_pair_persists(self):
  self.assertEqual(s.to_engine('select',{'witnesses':['wrong1','wrong2']})['note']['witnesses'],['wrong1','wrong2'])
 def test_original_ledger_and_six_call_cap(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'ledger.sqlite'
   with sqlite3.connect(path) as db:
    db.execute('CREATE TABLE calls(actual_usd REAL,reserved_usd REAL)');db.executemany('INSERT INTO calls VALUES(?,?)',[(.122835/44,.02265)]*44)
    db.execute('CREATE TABLE r3_calls(stage TEXT,reserved TEXT,actual TEXT,status TEXT)');db.executemany('INSERT INTO r3_calls VALUES(?,?,?,?)',[('Q3','0.02265',None,'ambiguous'),('C1','0.02265','0.000172','terminal')])
   l=r.x.Ledger(path,True)
   with l.connect() as db:
    db.executemany('INSERT INTO r3_successor VALUES(?,?,?,?,?,?,?,?,?)',[(f'old-{i}','Q3-A2','old',i,'.02265','0.169662' if i==0 else '0','terminal','{}',1) for i in range(69)])
   l=r.ledger(path,True)
   for i in range(6):
    ident=l.reserve('D1',r.TRAJECTORY,i);l.settle(ident,.0001,{'x':i},1)
   with self.assertRaisesRegex(ValueError,'stage_cap'):l.reserve('D1',r.TRAJECTORY,6)
   self.assertEqual(len(l.history(r.TRAJECTORY)),6);self.assertEqual(l.summary()['Q3-A2']['actual_usd'],'0.169662')
if __name__=='__main__':unittest.main()
