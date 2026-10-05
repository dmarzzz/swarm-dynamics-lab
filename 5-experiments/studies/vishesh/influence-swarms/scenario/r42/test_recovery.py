import copy,json,sqlite3,tempfile,unittest
from pathlib import Path
import recovery as x
class RecoveryTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name);self.db=self.p/'budget.sqlite';self.cases=x.c.corpus();self.case=next(c for c in self.cases if c['id']==x.CASE);root=x.i.Root(self.case,0,('truthful',));self.failed=None
  for node in root.nodes:
   if root.blocked(node):continue
   item=root.item(node['id'])
   if node['id']==x.FAILED:self.failed=x.c.encoded(item['wire']);root.fail(item,'length')
   else:root.accept(item,x.i.answer_fixture(self.case,node))
  self.original=[root.export()];self.bad=self.response(None,'length')
  with x.r.database(self.db)as db:
   db.executescript('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER);INSERT INTO budget VALUES(1,50,27.348512,4284);CREATE TABLE r42_scope(attempt TEXT PRIMARY KEY,source TEXT,manifest TEXT,max_calls INTEGER,maximum REAL,used_calls INTEGER,reserved REAL,status TEXT);CREATE TABLE r42_work(attempt TEXT,node TEXT,ordinal INTEGER,wirehash TEXT,reserved REAL,status TEXT,cost REAL,PRIMARY KEY(attempt,node),UNIQUE(attempt,ordinal));')
   db.execute('INSERT INTO r42_scope VALUES(?,?,?,?,?,?,?,?)',('r42','src','manifest',6,.034176,0,0,'funded'))
 def tearDown(self):self.t.cleanup()
 def response(self,answer,finish='stop'):
  return x.c.encoded({'provider':'OpenAI','model':x.i.MODEL,'usage':{'cost':.001,'prompt_tokens':200,'completion_tokens':100},'choices':[{'finish_reason':finish,'message':{'content':json.dumps(x.i.wire_answer(answer))if answer else '{"incomplete":'}}]})
 def root(self):return x.restore(self.cases,self.original,self.failed,self.bad)
 def reserve(self,node=x.FAILED,source='src',until='2099-01-01T00:00:00+00:00'):return x.reserve(self.db,'r42',source,'manifest',node,'hash',until)
 def test_exact_restoration_and_six_missing(self):
  r=self.root();self.assertEqual(x.c.encoded(r.item(x.FAILED)['wire']),self.failed);self.assertEqual(len(r.nodes)-len(r.answers),6)
 def test_wire_mutation_rejected(self):
  with self.assertRaises(x.r.Stop):x.restore(self.cases,self.original,self.failed+b' ',self.bad)
 def test_other_failure_rejected(self):
  bad=copy.deepcopy(self.original);bad[0]['nodes'][0]['state']='unstarted'
  with self.assertRaises(x.r.Stop):x.restore(self.cases,bad,self.failed,self.bad)
 def test_successful_response_cannot_be_retried(self):
  item=self.root().item(x.FAILED);raw=self.response(x.i.answer_fixture(self.case,item['node']))
  with self.assertRaises(x.r.Stop):x.restore(self.cases,self.original,self.failed,raw)
 def test_unknown_usage_rejected(self):
  raw=json.loads(self.bad);raw.pop('usage')
  with self.assertRaises(x.r.Stop):x.restore(self.cases,self.original,self.failed,x.c.encoded(raw))
 def test_duplicate_atomic_rollback(self):
  self.reserve()
  with self.assertRaises(sqlite3.IntegrityError):self.reserve()
  with x.r.database(self.db)as db:self.assertEqual(db.execute('SELECT calls FROM budget').fetchone()[0],4285)
 def test_source_and_expiry(self):
  for kw in({'source':'other'},{'until':'2000-01-01T00:00:00+00:00'}):
   with self.assertRaises(x.r.Stop):self.reserve(**kw)
 def test_only_six_allowed(self):
  for n in x.NODES:self.reserve(n)
  with self.assertRaises(x.r.Stop):self.reserve()
  with self.assertRaises(x.r.Stop):self.reserve('truthful/small-final')
 def test_success_preserves_original_and_counts_retry(self):
  before=copy.deepcopy(self.original);r=self.root();run=x.Continuation(r,self.p/'out',self.db,'r42','src','manifest','2099-01-01T00:00:00+00:00')
  record,s=run.run(lambda raw,node:self.response(x.i.answer_fixture(self.case,r.item(node)['node'])))
  self.assertTrue(s['complete']);self.assertEqual(s['started'],6);self.assertEqual(s['retry_calls'],1);self.assertEqual(self.original,before)
  self.assertTrue(all(n['state']=='valid' for n in record['nodes']))
 def test_new_format_failure_stops_without_second_retry(self):
  run=x.Continuation(self.root(),self.p/'out',self.db,'r42','src','manifest','2099-01-01T00:00:00+00:00');_,s=run.run(lambda raw,node:self.bad)
  self.assertEqual(s['started'],1);self.assertFalse(s['complete']);self.assertEqual(s['unknown_usage'],0)
 def test_transport_failure_keeps_reservation(self):
  def fail(*a):raise TimeoutError()
  run=x.Continuation(self.root(),self.p/'out',self.db,'r42','src','manifest','2099-01-01T00:00:00+00:00');_,s=run.run(fail)
  self.assertEqual(s['started'],1);self.assertEqual(s['unknown_usage'],1);self.assertEqual(s['retained_reservation'],x.i.RESERVATION)
if __name__=='__main__':unittest.main()
