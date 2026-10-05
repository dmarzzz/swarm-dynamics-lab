import concurrent.futures as cf,copy,json,tempfile,unittest
from pathlib import Path
import engine as e
DDL='''CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER);INSERT INTO budget VALUES(1,50,27.382688,4290);CREATE TABLE r43_scope(attempt TEXT PRIMARY KEY,source TEXT,manifest TEXT,calls INTEGER,reserved REAL,retries INTEGER,status TEXT);INSERT INTO r43_scope VALUES('main','source','manifest',0,0,0,'funded');CREATE TABLE r43_calls(attempt TEXT,root TEXT,node TEXT,try INTEGER,ordinal INTEGER,wire TEXT,reserved REAL,status TEXT,error TEXT,cost REAL,PRIMARY KEY(attempt,root,node,try),UNIQUE(attempt,ordinal));'''
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name);self.db=self.p/'budget.sqlite';self.cases=e.c.corpus()
  with e.r.database(self.db)as db:db.executescript(DDL)
  self.q=[]
  for rt in e.i.schedule(self.cases,'R41-FULL-Q'):
   while(rt.next_node()):
    n=rt.next_node();rt.accept(rt.item(n['id']),e.i.answer_fixture(rt.case,n))
   self.q.append(rt.export())
 def tearDown(self):self.t.cleanup()
 def reserve(self,node,wire='wire',source='source'):return e.reserve(self.db,'main',source,'manifest','root',node,wire,'2099-01-01T00:00:00+00:00')
 def result(self,answer=None,finish='stop'):
  return e.c.encoded({'provider':'OpenAI','model':e.i.MODEL,'usage':{'cost':.001,'prompt_tokens':100,'completion_tokens':100},'choices':[{'finish_reason':finish,'message':{'content':json.dumps(e.i.wire_answer(answer))if answer else '{'}}]})
 def session(self,roots=None):return e.Session(self.cases,self.p/'out',self.db,'main','source','manifest','2099-01-01T00:00:00+00:00',(27.382688,4290),self.q,roots=roots)
 def test_duplicate_and_unknown_retry_denied(self):
  self.reserve('n')
  with self.assertRaises(e.r.Stop):self.reserve('n')
  with e.r.database(self.db)as db:self.assertEqual(db.execute('SELECT calls FROM budget').fetchone()[0],4291)
 def test_only_one_known_length_same_wire_retry(self):
  n,_=self.reserve('n');e.settle(self.db,'main',n,'length',.001)
  with self.assertRaises(e.r.Stop):self.reserve('n',wire='changed')
  n,trial=self.reserve('n');self.assertEqual(trial,2);e.settle(self.db,'main',n,'length',.001)
  with self.assertRaises(e.r.Stop):self.reserve('n')
 def test_valid_and_structure_failures_not_retried(self):
  for status in('validated','local_structure'):
   n,_=self.reserve(status);e.settle(self.db,'main',n,status,.001)
   with self.assertRaises(e.r.Stop):self.reserve(status)
 def test_atomic_concurrent_pool_exhaustion(self):
  for j in range(31):n,_=self.reserve(str(j));e.settle(self.db,'main',n,'length',.001)
  def retry(j):
   try:self.reserve(str(j));return True
   except e.r.Stop:return False
  with cf.ThreadPoolExecutor(max_workers=16)as pool:self.assertEqual(sum(pool.map(retry,range(31))),30)
  with e.r.database(self.db)as db:self.assertEqual(db.execute('SELECT calls,retries FROM r43_scope').fetchone(),(61,30))
 def test_source_ceiling_and_restart_refusal(self):
  with self.assertRaises(e.r.Stop):self.reserve('n',source='wrong')
  with e.r.database(self.db)as db:db.execute('UPDATE budget SET reserved=44.574240')
  with self.assertRaises(e.r.Stop):self.reserve('n')
  with e.r.database(self.db)as db:db.execute('UPDATE budget SET reserved=27.382688')
  self.reserve('n')
  with self.assertRaises(e.r.Stop):self.session()
 def test_stable_wave_and_retry_priority(self):
  roots=e.i.schedule(self.cases,'R41-E0');b=e.wave(roots,set());self.assertEqual([x[0]for x in b],[e.r.key(r)for r in roots[:16]])
  pending={(e.r.key(roots[1]),'check-1'),(e.r.key(roots[0]),'check-0')};self.assertEqual(e.wave(roots,pending)[:2],[(e.r.key(roots[0]),'check-0'),(e.r.key(roots[1]),'check-1')])
 def test_full_scripted_2988_and_analysis(self):
  session=self.session();lookup=session.lookup
  def transport(raw,rid,nid):
   rt=lookup[rid];item=rt.item(nid);self.assertEqual(raw,e.c.encoded(item['wire']));return self.result(e.i.answer_fixture(rt.case,item['node']))
  records,first,s=session.run(transport);self.assertEqual(s['physical_calls'],2988);self.assertEqual(s['retry_calls'],0);self.assertEqual(records,first);self.assertEqual(e.analysis.analyze(self.cases,records)['observed_final_decisions'],108)
 def test_recovery_and_first_pass_dependency_closure(self):
  roots=e.i.schedule(self.cases,'R41-E0')[:1];session=self.session(roots);rt=roots[0];bad='truthful/large-commercial-11/initial';seen={}
  def transport(raw,rid,nid):
   seen[nid]=seen.get(nid,0)+1
   if nid==bad and seen[nid]==1:return self.result(finish='length')
   return self.result(e.i.answer_fixture(rt.case,rt.item(nid)['node']))
  records,first,s=session.run(transport);self.assertEqual(s['retry_calls'],1);self.assertEqual(s['logical_valid'],166);self.assertEqual(s['first_pass_available'],160)
  nodes={n['id']:n for n in first[0]['nodes']};self.assertEqual(nodes['truthful/large-final']['state'],'blocked');self.assertEqual(nodes['misleading/large-final']['state'],'valid')
 def test_second_failure_blocks_only_branch(self):
  roots=e.i.schedule(self.cases,'R41-E0')[:1];session=self.session(roots);rt=roots[0];bad='truthful/large-commercial-11/initial'
  records,first,s=session.run(lambda raw,rid,nid:self.result(finish='length')if nid==bad else self.result(e.i.answer_fixture(rt.case,rt.item(nid)['node'])))
  self.assertEqual(s['retry_calls'],1);self.assertEqual(s['logical_valid'],160);self.assertIsNone(s['global_failure'])
 def test_transport_global_stop_retains_unknown(self):
  roots=e.i.schedule(self.cases,'R41-E0')[:1];session=self.session(roots)
  def fail(*args):raise TimeoutError()
  records,first,s=session.run(fail);self.assertEqual(s['physical_calls'],16);self.assertEqual(s['unknown_usage'],16);self.assertEqual(s['retry_calls'],0);self.assertIsNotNone(s['global_failure'])
 def test_relay_exact_wire_one_retry_and_parent_reuse(self):
  relay=e.Relay(self.cases,self.p/'relay');rt=next(iter(relay.roots.values()));node=rt.next_node();raw=e.c.encoded(rt.item(node['id'])['wire']);rid=e.r.key(rt)
  relay.send(raw,rid,node['id'],lambda _:self.result(finish='length'))
  relay.send(raw,rid,node['id'],lambda _:self.result(e.i.answer_fixture(rt.case,node)))
  self.assertEqual(relay.count,2);self.assertEqual(relay.retries,1)
  with self.assertRaises(Exception):relay.send(raw,rid,node['id'],lambda _:self.result(finish='length'))
 def test_pool_exhaustion_continues_independent_branches(self):
  roots=e.i.schedule(self.cases,'R41-E0')[:1];session=self.session(roots);rt=roots[0];bad='truthful/large-commercial-11/initial'
  with e.r.database(self.db)as db:db.execute('UPDATE r43_scope SET retries=30')
  records,first,s=session.run(lambda raw,rid,nid:self.result(finish='length')if nid==bad else self.result(e.i.answer_fixture(rt.case,rt.item(nid)['node'])))
  self.assertEqual(s['retry_calls'],0);self.assertEqual(s['logical_valid'],160);self.assertIsNone(s['global_failure'])
if __name__=='__main__':unittest.main()
