import unittest,json,datetime as dt,threading,time,sys
from pathlib import Path
import acquisition as p
import cases as c,instrument as i,runtime as r,test_runtime
from test_b1 import cell
class Tests(unittest.TestCase):
 body=test_runtime.RuntimeTests.body
 transport=test_runtime.RuntimeTests.transport
 budget=test_runtime.RuntimeTests.budget
 def setUp(self):
  test_runtime.RuntimeTests.setUp(self)
  with r.database(self.ledger) as db:
   db.execute('UPDATE budget SET reserved=9.965664,calls=942');db.execute('CREATE TABLE e1_scope(grant_id TEXT PRIMARY KEY,maximum_model REAL,model_debited REAL,status TEXT)');db.execute('INSERT INTO e1_scope VALUES(?,9.728,0,"funded")',(p.GRANT,));db.execute('CREATE TABLE IF NOT EXISTS b1_dispatch(attempt TEXT,ordinal INTEGER,wire_sha256 TEXT,reserved REAL,status TEXT,cost REAL,PRIMARY KEY(attempt,ordinal))')
  self.expected={'reserved':9.965664,'calls':942};self.until=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat()
  self.q=[cell(next(x for x in self.cases if x['id']==row['case_id']),row['condition'],row['arm'])[0] for row in i.schedule(self.cases,'development') if row['case_id'] in ('b2-location-0','b2-cost-0')]
 def test_80_native_protocol_rehearsal(self):
  relay=p.Relay(self.cases,self.dir/'relay',stage='E1-Q0',interval=0)
  s=p.collect(self.cases,self.dir/'q',self.ledger,'q',lambda raw,aid,step:relay.send(raw,aid,step,self.transport),self.until,self.expected,stage='E1-Q0',interval=0)
  self.assertTrue(s['complete']);self.assertTrue(s['all_cells_observed']);self.assertEqual(s['calls'],80);self.assertTrue(json.loads((self.dir/'q/assessment.json').read_text())['qualified'])
 def test_full1920_exact_wires_and_bounds(self):
  relay=p.Relay(self.cases,self.dir/'relay',self.q,interval=0);seen=set();lock=threading.Lock()
  def t(raw,aid,step):
   with lock:self.assertNotIn((aid,step),seen);seen.add((aid,step))
   return relay.send(raw,aid,step,self.transport)
  s=p.collect(self.cases,self.dir/'main',self.ledger,'main',t,self.until,self.expected,self.q,interval=0)
  self.assertTrue(s['complete']);self.assertEqual(s['valid_calls'],1920);self.assertEqual(len(seen),1920)
  batch=p.Batch(self.cases,self.q);lookup={x.id:x for x in batch.cells}
  for n in range(1,1921):
   a=json.loads((self.dir/f'main/{n:04d}-assignment.json').read_text());v=json.loads((self.dir/f'main/{n:04d}-validated.json').read_text());x=lookup[a['assignment_id']];item=x.protocol.next();self.assertEqual((self.dir/f'main/{n:04d}-request.bin').read_bytes(),c.encoded(item['wire']));x.protocol.accept(item,v['answer'])
  self.assertEqual(batch.export(),json.loads((self.dir/'main/records.json').read_text()));review=json.loads((self.dir/'main/assessment.json').read_text());self.assertEqual(review['missingness_bounds']['overall_bounds'],[0.,0.]);self.assertEqual(review['original_analysis']['overall_mean'],0.)
 def test_local_failure_contained_no_peer_ingestion(self):
  relay=p.Relay(self.cases,self.dir/'relay',self.q,interval=0);target=relay.batch.cells[0].id;seen=[];lock=threading.Lock()
  def t(raw,aid,step):
   with lock:seen.append((aid,step))
   def provider(raw):
    body=json.loads(self.transport(raw))
    if aid==target:body['choices'][0]['message']['content']='malformed'
    return c.encoded(body)
   return relay.send(raw,aid,step,provider)
  s=p.collect(self.cases,self.dir/'main',self.ledger,'main',t,self.until,self.expected,self.q,interval=0)
  self.assertTrue(s['complete']);self.assertFalse(s['all_cells_observed']);self.assertEqual(s['format_failed_cells'],1);self.assertEqual([x for x in seen if x[0]==target],[(target,0)]);self.assertFalse(relay.stopped)
  records=json.loads((self.dir/'main/records.json').read_text());self.assertEqual(len(records),288);self.assertEqual(sum(x['execution']=='complete' for x in records),287);self.assertEqual(records[0]['answers'],[])
  review=json.loads((self.dir/'main/assessment.json').read_text());self.assertIsNone(review['original_analysis']['overall_mean']);self.assertEqual(review['missingness_bounds']['assigned_groups']['neutral/peer']['missing'],1);self.assertAlmostEqual(review['missingness_bounds']['overall_bounds'][0],-1/48);self.assertEqual(review['missingness_bounds']['overall_bounds'][1],0)
 def test_global_failure_drains_inflight(self):
  barrier=threading.Barrier(4);seen=[];lock=threading.Lock()
  def t(raw,aid,step):
   with lock:seen.append(aid);n=len(seen)
   barrier.wait(timeout=10)
   if n==1:raise RuntimeError('transport_ambiguity')
   time.sleep(.1);return self.transport(raw)
  s=p.collect(self.cases,self.dir/'failed',self.ledger,'failed',t,self.until,self.expected,self.q,concurrency=4,interval=0)
  self.assertFalse(s['complete']);self.assertEqual(s['calls'],4);self.assertEqual(s['valid_calls'],3);self.assertEqual(s['usage_missing'],1)
 def test_atomic_grant_limit(self):
  with r.database(self.ledger) as db:db.execute('UPDATE e1_scope SET model_debited=maximum_model-?',(2*i.RESERVATION,))
  s=p.collect(self.cases,self.dir/'limited',self.ledger,'limited',lambda raw,*_:self.transport(raw),self.until,self.expected,self.q,interval=0)
  self.assertEqual(s['calls'],2);self.assertFalse(s['complete']);self.assertAlmostEqual(self.budget()[1],9.965664+2*i.RESERVATION)
 def test_all_missing_bounds(self):
  b=p.bounds(self.cases,[]);self.assertEqual(b['overall_bounds'],[-2.,2.]);self.assertTrue(all(v['assigned']==48 and v['missing']==48 for v in b['assigned_groups'].values()))
if __name__=='__main__':unittest.main()
