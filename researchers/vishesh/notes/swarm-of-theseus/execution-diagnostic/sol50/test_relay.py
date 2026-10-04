import sqlite3,unittest
import instrument as i
import native as n
import relay as r
class RelayTests(unittest.TestCase):
 def test_exact_body_required(self):
  w=i.world(4);packet,_=n.founder_packet(w,w['members'][0]);p={'id':'SOL50-Q1-0000','phase':'learn','packet':packet,'request':n.request('learn',packet)};a={'attempts':['SOL50-Q1']}
  self.assertEqual(r.validate_payload(p,a)['model'],'openai/gpt-6-sol');p['request']['model']='other'
  with self.assertRaises(ValueError):r.validate_payload(p,a)
 def test_unadmitted_attempt(self):
  with self.assertRaises(ValueError):r.validate_payload({'id':'unauthorized'},{'attempts':['SOL50-Q1']})
 def test_reservations_survive_errors_and_duplicate_rejected(self):
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved_usd REAL,status TEXT,actual_usd REAL)');r.reserve(db,'call1')
  with self.assertRaises(sqlite3.IntegrityError):r.reserve(db,'call1')
  self.assertEqual(db.execute('SELECT count(*) FROM calls').fetchone()[0],1);self.assertAlmostEqual(db.execute('SELECT sum(reserved_usd) FROM calls').fetchone()[0],i.budget()['per_call_reserved_usd'])
if __name__=='__main__':unittest.main()
