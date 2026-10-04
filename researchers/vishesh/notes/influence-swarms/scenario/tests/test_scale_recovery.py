import json,sys,unittest,tempfile,sqlite3,datetime,copy
from pathlib import Path
from contextlib import closing
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import scale_recovery as sr,scale_recovery_run as run,scale_pilot as sp
from test_scale_pilot import fixture
class RecoveryTests(unittest.TestCase):
 def test_prefix_and_full_recovery(self):
  p=sr.Protocol('SC-LUNA');self.assertEqual(67,p.position);self.assertEqual('adviser-19',p.next()['agent']);self.assertEqual('low',p.next()['wire_body']['verbosity'])
  self.assertEqual(run.build('SC-LUNA'),json.loads((BASE/'reviews/SC-LUNA-packet.json').read_text()))
  with tempfile.TemporaryDirectory() as d:
   db=Path(d)/'budget'
   with closing(sqlite3.connect(db)) as c,c:c.execute('CREATE TABLE budget(id,cap,reserved,calls)');c.execute('INSERT INTO budget VALUES(1,8,7.7769408,401)')
   def transport(raw):
    i=p.next();self.assertEqual(raw,sr.encode(i['wire_body']));a=fixture(p,i);p.accept(i,a);return json.dumps({'model':i['wire_body']['model'],'provider':'OpenAI','usage':{'prompt_tokens':1,'completion_tokens':1,'cost':.000001},'choices':[{'finish_reason':'stop','message':{'content':json.dumps(a)}}]}).encode()
   result=run.collect(sr.build('SC-LUNA'),Path(d)/'out',db,transport,(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=1)).isoformat());self.assertTrue(result['complete']);self.assertEqual((129,196,197),(result['valid'],result['combined_logical_valid'],result['combined_physical_requests']))
   with closing(sqlite3.connect(db)) as c:reserved,calls=c.execute('SELECT reserved,calls FROM budget').fetchone()
   self.assertAlmostEqual(7.961696,reserved);self.assertEqual(530,calls)
 def test_original_prefix_not_recalled(self):
  p=sr.Protocol('SC-LUNA');self.assertEqual([r['answer'] for r in p.parent_rows],p.answers['omission']);self.assertEqual([],p.answers['clean']);self.assertNotIn('low',sr.encode(p.parent_rows[0]).decode())
 def test_changed_parent_wire_rejected(self):
  from unittest.mock import patch
  rows,h=sr.parent();rows=copy.deepcopy(rows);rows[0]['wire_sha256']='0'*64
  with patch.object(sr,'parent',return_value=(rows,h)):
   with self.assertRaises(AssertionError):sr.Protocol('SC-LUNA')
