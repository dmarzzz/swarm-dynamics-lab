import concurrent.futures as cf,datetime as dt,json,threading,time,unittest
import cases as c,instrument as i,runtime as r,parallel_runtime as p
import test_runtime
from test_b1 import cell
class ParallelTests(unittest.TestCase):
 setUp=test_runtime.RuntimeTests.setUp
 body=test_runtime.RuntimeTests.body
 transport=test_runtime.RuntimeTests.transport
 budget=test_runtime.RuntimeTests.budget
 def setup_e0(self):
  with r.database(self.ledger) as db:db.execute('UPDATE budget SET reserved=9.596,calls=866');db.execute('UPDATE b1_scope SET model_debited=.466944')
  return [cell(next(x for x in self.cases if x['id']==row['case_id']),row['condition'],row['arm'])[0] for row in i.schedule(self.cases,'development')]
 def test_threaded_full_exact_reconstruction_and_reservations(self):
  d0=self.setup_e0();relay=p.Relay(self.cases,self.dir/'parallel-relay',d0,interval=0);seen=[];lock=threading.Lock()
  def transport(raw,aid,step):
   with lock:seen.append((aid,step))
   return relay.send(raw,aid,step,self.transport)
  s=p.collect(self.cases,self.dir/'parallel',self.ledger,'parallel',transport,(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat(),{'reserved':9.596,'calls':866},d0,interval=0)
  self.assertTrue(s['complete']);self.assertEqual(s['calls'],1920);self.assertEqual(s['valid_calls'],1920);self.assertEqual(len(set(seen)),1920);self.assertEqual(relay.count,1920)
  self.assertAlmostEqual(self.budget()[1],r.MODEL_CEILING);self.assertEqual(self.budget()[2],2786)
  batch=p.Batch(self.cases,d0);lookup={x.id:x for x in batch.cells}
  for ordinal in range(1,1921):
   m=json.loads((self.dir/f'parallel/{ordinal:04d}-assignment.json').read_text());v=json.loads((self.dir/f'parallel/{ordinal:04d}-validated.json').read_text());x=lookup[m['assignment_id']]
   self.assertEqual(m['step'],len(x.protocol.answers));item=x.protocol.next();self.assertEqual((self.dir/f'parallel/{ordinal:04d}-request.bin').read_bytes(),c.encoded(item['wire']));self.assertEqual(item['wire_sha256'],v['wire_sha256']);x.protocol.accept(item,v['answer'])
  self.assertEqual(batch.export(),json.loads((self.dir/'parallel/records.json').read_text()));self.assertEqual(relay.batch.export(),batch.export())
 def test_failure_drains_inflight_no_additional_starts(self):
  d0=self.setup_e0();barrier=threading.Barrier(4);lock=threading.Lock();seen=[]
  def transport(raw,aid,step):
   with lock:seen.append(aid);n=len(seen)
   barrier.wait(timeout=10)
   if n==1:
    body=json.loads(self.transport(raw));body['choices'][0]['message']['content']='malformed';return c.encoded(body)
   time.sleep(.2);return self.transport(raw)
  s=p.collect(self.cases,self.dir/'failed-parallel',self.ledger,'failed-parallel',transport,(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat(),{'reserved':9.596,'calls':866},d0,concurrency=4,interval=0)
  self.assertFalse(s['complete']);self.assertEqual(s['calls'],4);self.assertEqual(s['valid_calls'],3);self.assertEqual(s['usage_missing'],0);self.assertEqual(s['unstarted_calls'],1916);self.assertAlmostEqual(s['reported_usd'],4*.00006);self.assertEqual(len(seen),4)
 def test_relay_duplicate_and_out_of_order_close_globally(self):
  d0=self.setup_e0();relay=p.Relay(self.cases,self.dir/'reject-relay',d0,interval=0);x=relay.batch.cells[0];raw=c.encoded(x.protocol.next()['wire']);relay.send(raw,x.id,0,self.transport)
  with self.assertRaises(r.Stop):relay.send(raw,x.id,0,self.transport)
  self.assertTrue(relay.stopped);self.assertEqual(relay.count,1)
 def test_atomic_finite_scope_with_threads(self):
  d0=self.setup_e0()
  with r.database(self.ledger) as db:db.execute('UPDATE b1_scope SET model_debited=maximum_model-?',(2*i.RESERVATION,))
  def transport(raw,aid,step):time.sleep(.2);return self.transport(raw)
  s=p.collect(self.cases,self.dir/'finite',self.ledger,'finite',transport,(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat(),{'reserved':9.596,'calls':866},d0,concurrency=16,interval=0)
  self.assertEqual(s['calls'],2);self.assertEqual(s['valid_calls'],2);self.assertFalse(s['complete']);self.assertEqual(self.budget()[2],868)
 def test_parallel_diagnostic_exact_scope(self):
  relay=p.Relay(self.cases,self.dir/'d0-relay',stage='B2-D0',interval=0)
  summary=p.collect(self.cases,self.dir/'d0-parallel',self.ledger,'d0-parallel',lambda raw,aid,step:relay.send(raw,aid,step,self.transport),(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat(),{'reserved':9.129056,'calls':770},stage='B2-D0',interval=0)
  self.assertTrue(summary['complete']);self.assertEqual(summary['calls'],96);self.assertEqual(summary['valid_calls'],96);self.assertEqual(len(relay.batch.cells),20)
  self.assertTrue(json.loads((self.dir/'d0-parallel/assessment.json').read_text())['qualified'])
if __name__=='__main__':unittest.main()
