from contextlib import closing
import unittest,tempfile,sqlite3,json,sys,datetime,threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import cases as c,instrument as i,runtime as r
class RuntimeTest(unittest.TestCase):
 def setup_session(self,base,remaining=3744):
  ledger=base/'original.sqlite'
  with closing(sqlite3.connect(ledger)) as db:
   db.executescript('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER);CREATE TABLE b1_dispatch(attempt TEXT,ordinal INTEGER,wire_sha256 TEXT,reserved REAL,status TEXT,cost REAL,PRIMARY KEY(attempt,ordinal));CREATE TABLE r41_work(grant_id TEXT,stage TEXT,root TEXT,node TEXT,attempt TEXT,ordinal INTEGER,PRIMARY KEY(grant_id,stage,root,node));CREATE TABLE r41_scope(grant_id TEXT PRIMARY KEY,source TEXT,manifest TEXT,maximum_model REAL,model_debited REAL,max_calls INTEGER,calls INTEGER,status TEXT);')
   db.execute('INSERT INTO budget VALUES(1,50,23.070816,3533)');db.execute('INSERT INTO r41_scope VALUES(?,?,?,?,?,?,?,?)',(r.GRANT,'fixture-source','fixture-manifest',r.MAXIMUM_MODEL,0,remaining,0,'funded'));db.commit()
  # For partial allowance test retain immutable max_calls and predebit consumed slots.
  if remaining!=3744:
   with closing(sqlite3.connect(ledger)) as db:db.execute('UPDATE r41_scope SET max_calls=3744,calls=?',(3744-remaining,));db.commit()
  return r.Session(c.corpus(),base/'output',ledger,'fixture-q0','R41-D1','fixture-source','fixture-manifest',{'reserved':23.070816,'calls':3533},(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=1)).isoformat(),interval=0)
 def transport(self,session,bad=None):
  def fn(raw,root_id,node_id):
   root=session.lookup[root_id];node=next(n for n in root.nodes if n['id']==node_id)
   if bad and bad(root_id,node_id):content=' ';finish='length'
   else:content=json.dumps(i.wire_answer(i.answer_fixture(root.case,node)));finish='stop'
   return c.encoded({'provider':'OpenAI','model':i.MODEL,'usage':{'cost':.00001,'prompt_tokens':100,'completion_tokens':100},'choices':[{'finish_reason':finish,'message':{'content':content}}]})
  return fn
 def test_complete_parallel_native_shaped_fixture(self):
  with tempfile.TemporaryDirectory()as tmp:
   s=self.setup_session(Path(tmp));records,summary=s.run(self.transport(s),concurrency=16)
   self.assertEqual(summary['calls'],84);self.assertEqual(summary['valid_calls'],84);self.assertTrue(i.partial_qualification(c.corpus(),records,'R41-D1')['qualified']);self.assertIsNone(summary['failure']);self.assertAlmostEqual(summary['new_reserved_usd'],.478464)
 def test_atomic_remaining_and_global_stop(self):
  with tempfile.TemporaryDirectory()as tmp:
   s=self.setup_session(Path(tmp),remaining=5);records,summary=s.run(self.transport(s),concurrency=16)
   self.assertEqual(summary['calls'],5);self.assertEqual(summary['failure'],'grant_exhausted');self.assertLessEqual(summary['budget_after'][1],23.070816+5*i.RESERVATION+1e-9)
 def test_failed_shared_check_preserves_missing_endpoints(self):
  with tempfile.TemporaryDirectory()as tmp:
   s=self.setup_session(Path(tmp));first=next(iter(s.lookup));records,summary=s.run(self.transport(s,lambda root,node:root==first and node=='check-0'),concurrency=8)
   self.assertEqual(summary['known_format_failures'],1);self.assertTrue(summary['complete']);self.assertEqual(summary['blocked_nodes'],3);self.assertFalse(i.partial_qualification(c.corpus(),records,'R41-D1')['qualified'])
 def test_duplicate_work_cannot_dispatch_twice(self):
  with tempfile.TemporaryDirectory()as tmp:
   base=Path(tmp);one=self.setup_session(base)
   two=r.Session(c.corpus(),base/'other-output',base/'original.sqlite','other-attempt','R41-D1','fixture-source','fixture-manifest',{'reserved':23.070816,'calls':3533},one.until,interval=0)
   root=one.roots[0];one.dispatch(root,root.nodes[0],self.transport(one))
   with self.assertRaises(sqlite3.IntegrityError):two.dispatch(two.roots[0],two.roots[0].nodes[0],self.transport(two))
   with r.database(base/'original.sqlite')as db:
    self.assertEqual(db.execute('SELECT count(*) FROM b1_dispatch').fetchone()[0],1)
    self.assertEqual(db.execute('SELECT count(*) FROM r41_work').fetchone()[0],1)
 def test_main_requires_source_bound_native_qualification(self):
  with tempfile.TemporaryDirectory()as tmp:
   base=Path(tmp);s=self.setup_session(base)
   with self.assertRaisesRegex(r.Stop,'source_bound_native_qualification'):
    r.Session(c.corpus(),base/'main',base/'original.sqlite','fixture-main','R41-E0','fixture-source','fixture-manifest',{'reserved':23.070816,'calls':3533},s.until)
 def test_relay_checks_exact_wire_before_provider(self):
  with tempfile.TemporaryDirectory()as tmp:
   relay=r.Relay(c.corpus(),'R41-D1',Path(tmp)/'relay');root=next(iter(relay.roots.values()));item=root.next();calls=[]
   with self.assertRaisesRegex(r.Stop,'relay_wire'):
    relay.send(c.encoded(item['wire'])+b' ',r.key(root),item['node']['id'],lambda raw:calls.append(raw))
   self.assertEqual(calls,[]);self.assertTrue(relay.stopped)
 def test_actual_diagnostic_only_grant(self):
  with tempfile.TemporaryDirectory()as tmp:
   base=Path(tmp);one=self.setup_session(base)
   with r.database(base/'original.sqlite')as db:db.execute('UPDATE r41_scope SET maximum_model=?,max_calls=?',(.478464,84))
   two=r.Session(c.corpus(),base/'diagnostic',base/'original.sqlite','actual-D1','R41-D1','fixture-source','fixture-manifest',{'reserved':23.070816,'calls':3533},one.until,interval=0)
   records,summary=two.run(self.transport(two));self.assertEqual(summary['calls'],84);self.assertTrue(i.partial_qualification(c.corpus(),records,'R41-D1')['qualified']);self.assertAlmostEqual(summary['new_reserved_usd'],.478464)
 def test_route_failure_stops_and_keeps_cost(self):
  with tempfile.TemporaryDirectory()as tmp:
   s=self.setup_session(Path(tmp));ordinary=self.transport(s)
   def wrong(*args):
    x=json.loads(ordinary(*args));x['provider']='Other';return c.encoded(x)
   records,summary=s.run(wrong,concurrency=1);self.assertEqual(summary['calls'],1);self.assertEqual(summary['failure'],'route');self.assertEqual(summary['usage_missing'],0);self.assertFalse(summary['complete'])
if __name__=='__main__':unittest.main()
