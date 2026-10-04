import json,tempfile,unittest
from pathlib import Path
import diagnostic as d
class DiagnosticTests(unittest.TestCase):
 def test_paired_packet_and_blinding(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);i=root/'inputs';i.mkdir();(i/'images').mkdir();(i/'images/a.png').write_bytes(b'fake')
   (i/'cases.json').write_text(json.dumps([{'id':str(n),'stage':'Q0','image':'a.png','image_sha256':d.design.sha(i/'images/a.png'),'gold':'999.00'} for n in range(2)]))
   out=root/'packet';r=d.prepare(i,out);self.assertEqual(r['assignments'],16)
   rows=json.loads((out/'rows.json').read_text());self.assertEqual([r['arm'] for r in rows],['original','locale']*8)
   for r in rows:
    p=json.loads((out/(r['id']+'.json')).read_text());self.assertNotIn('999.00',json.dumps(p));self.assertEqual(d.design.digest(p),r['payload_sha256'])
    self.assertEqual(p['messages'][1]['content'][1],d.design.request(b'fake',1)['messages'][1]['content'][1])
 def test_ledger_admission_retains_original(self):
  import importlib.util,sqlite3
  spec=importlib.util.spec_from_file_location('d1relay',Path(__file__).with_name('relay.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'ledger'
   with sqlite3.connect(p) as db:
    db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved REAL,status TEXT,cost REAL)')
    db.executemany('INSERT INTO calls VALUES(?,?,?,?)',[(str(i),.015,'terminal',.001) for i in range(80)])
   m.validate_prior(p,{'D1-new':'hash'})
   with sqlite3.connect(p) as db:self.assertEqual(db.execute('select count(*) from calls').fetchone()[0],80)
   with sqlite3.connect(p) as db:db.execute("UPDATE calls SET cost=NULL WHERE id='0'")
   with self.assertRaises(ValueError):m.validate_prior(p,{'D1-new':'hash'})
if __name__=='__main__':unittest.main()
