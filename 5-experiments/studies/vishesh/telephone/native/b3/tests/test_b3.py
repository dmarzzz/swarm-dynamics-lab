import copy,json,sqlite3,sys,tempfile,threading,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from corpus import cases,mutation,reference,assignments,canonical,sha
from contract import request,parse,normalize,MODEL,PER
from prepare import build,ROOT,envelope
from native import packet,ExistingLedger,Runner,release_unstarted
from report import analyze

class Cases(unittest.TestCase):
 def test_balance_and_provenance(self):
  cs=cases();self.assertEqual(len(cs),24)
  for family in {c['family'] for c in cs}:self.assertEqual(sorted(c['gold']['answer'] for c in cs if c['family']==family),['NO','UNKNOWN','YES'])
  for label in ('YES','NO','UNKNOWN'):self.assertEqual(sum(c['gold']['initial_decision']=='GO' for c in cs if c['gold']['answer']==label),4)
 def test_all_labels_mutations_and_permutations(self):
  for c in cases():
   self.assertEqual(reference(c['actor'],c['question']),c['gold']['answer']);m=mutation(c);self.assertNotEqual(reference(m['actor'],m['question']),c['gold']['answer'])
   p=copy.deepcopy(c['actor']);p['records'].reverse();self.assertEqual(reference(p,c['question']),c['gold']['answer'])
   witness=next(r['text'] for r in c['actor']['records'] if r['id']==c['gold']['witness_id']);self.assertIn(c['gold']['witness'],witness)
 def test_lossless_copy_controller_after_three_hops(self):
  for c in cases():
   prior={'handoff':'\n'.join(r['text'] for r in c['actor']['records']),'decision':c['gold']['initial_decision']}
   for _ in range(3):prior=parse(canonical(prior),'writer')
   copied={'records':[{'id':str(i),'time':'00:00','text':line} for i,line in enumerate(prior['handoff'].splitlines())]}
   self.assertEqual(reference(copied,c['question']),c['gold']['answer'])
 def test_question_and_gold_isolation(self):
  c=cases()[0];prev={'handoff':'unchanged raw prose GO with spaces  ','decision':'GO'}
  for arm in ('P','R'):
   writer=json.loads(request(arm,c['actor'],prev)['messages'][1]['content']);self.assertNotIn('question',writer);self.assertNotIn('gold',writer)
   reader=json.loads(request(arm,c['actor'],prev,c['question'])['messages'][1]['content']);self.assertEqual(reader['handoff_text'],prev['handoff']);self.assertNotIn('previous_handoff',reader);self.assertNotIn('decision',reader);self.assertEqual('source_packet' in reader,arm=='R')
 def test_schema_and_bounds(self):
  with self.assertRaises(ValueError):parse('{"answer":"YES","evidence":"x","decision":"GO"}','reader')
  with self.assertRaises(ValueError):request('P',cases()[0]['actor'],{'handoff':'x'*9000,'decision':'GO'})
 def test_assignment_genealogy(self):
  aa=assignments();self.assertEqual(len(aa),384);self.assertEqual(len({a['id'] for a in aa}),384);self.assertEqual(sum(a['role']=='reader' for a in aa),96)
  seen=set()
  for a in aa:
   if a['parent']:self.assertIn(a['parent'],seen);self.assertTrue(a['parent'].startswith(a['chain']))
   seen.add(a['id'])
 def test_budget(self):
  e=envelope();self.assertEqual(e['additional_max_nano'],12503184386);self.assertEqual(e['cumulative_max_nano'],12954070896);self.assertFalse(e['funded'])

class Native(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.p=packet();db=sqlite3.connect(self.root/'budget.sqlite');db.executescript('CREATE TABLE authority(cap INTEGER,ref TEXT); CREATE TABLE charges(id TEXT PRIMARY KEY,stage TEXT,kind TEXT,reserve INTEGER,actual INTEGER,status TEXT,source TEXT);');db.execute('INSERT INTO authority VALUES (?,?)',(50000000000,'offline-fixture'));db.execute('INSERT INTO charges VALUES (?,?,?,?,?,?,?)',('historical','old','model',450886510,450886510,'known','fixture'));db.commit();db.close();self.ledger=ExistingLedger(self.root/'budget.sqlite');self.gold={c['id']:c['gold'] for c in cases()};self.calls=[];self.lock=threading.Lock();self.active=0;self.peak=0
 def tearDown(self):self.ledger.db.close();self.tmp.cleanup()
 def generate(self,cid,req):
  with self.lock:self.calls.append(cid);self.active+=1;self.peak=max(self.peak,self.active)
  try:
   time.sleep(.001);payload=json.loads(req['messages'][1]['content'])
   if cid in ('q01','q02'):obj={'answer':'YES' if cid=='q01' else 'UNKNOWN','evidence':'fixture evidence'}
   elif 'question' in payload:
    c=next(c for c in cases() if c['question']==payload['question'] and (c['id'] in cid));obj={'answer':c['gold']['answer'],'evidence':c['gold']['witness']}
   else:
    text='\n'.join(r['text'] for r in payload['source_packet']['records']) if 'source_packet' in payload else payload['previous_handoff']['handoff'];obj={'handoff':text,'decision':'GO'}
   return {'id':'generation-'+cid,'model':MODEL,'provider':'OpenAI','choices':[{'finish_reason':'stop','message':{'role':'assistant','content':canonical(obj)}}],'usage':{'prompt_tokens':100,'completion_tokens':100,'total_tokens':200,'cost':.0012}}
  finally:
   with self.lock:self.active-=1
 def runner(self,generate=None):return Runner(self.p,self.root/'out',self.ledger,generate or self.generate,time.time()+600)
 def qualification(self,r):
  r.qualify();review={'manifest_sha256':self.p['manifest_sha256'],'assessor':'offline fixture','responses':{}}
  for cid in ('q01','q02'):
   raw=json.loads((r.out/(cid+'.response.json')).read_text());review['responses'][cid]={'response_sha256':sha(raw),'evidence_supported':True,'rationale':'mock proof, no native competence claim'}
  return review
 def test_full_parallel_packet_and_replay(self):
  r=self.runner();review=self.qualification(r);result=r.main(review);self.assertEqual(result['valid'],384);self.assertEqual(len(self.calls),386);self.assertLessEqual(self.peak,4);self.assertGreater(self.peak,1)
  report=analyze(self.p,r.out,self.gold);self.assertTrue(all(x['status']=='valid' for x in report['rows']));self.assertTrue(all(c['correct']==24 for c in report['cells']));self.assertLessEqual(len(report['audit_required_ids']),32)
  self.assertEqual(self.ledger.db.execute("SELECT COUNT(*) FROM charges WHERE status!='known'").fetchone()[0],0)
  with self.assertRaises(ValueError):r.main(review)
 def test_global_stop_no_retry_and_uncertain_cost(self):
  def fail(cid,req):
   if cid not in ('q01','q02'):raise RuntimeError('synthetic transport failure')
   return self.generate(cid,req)
  r=self.runner(fail);review=self.qualification(r);result=r.main(review);self.assertLessEqual(result['failed'],4);self.assertGreater(result['unstarted'],370);self.assertEqual(len(self.calls),2)
  self.assertGreater(self.ledger.db.execute("SELECT COUNT(*) FROM charges WHERE status='unknown'").fetchone()[0],0)
 def test_cap_and_duplicate_reservation(self):
  self.ledger.db.execute('UPDATE authority SET cap=5000000000');self.ledger.db.commit()
  with self.assertRaises(ValueError):self.ledger.reserve(self.p)
  self.assertEqual(self.ledger.db.execute('SELECT COUNT(*) FROM charges').fetchone()[0],1)
  self.ledger.db.execute('UPDATE authority SET cap=50000000000');self.ledger.db.commit();self.ledger.reserve(self.p)
  with self.assertRaises(ValueError):self.ledger.reserve(self.p)
 def test_qualification_tamper_and_parent_tamper(self):
  r=self.runner();review=self.qualification(r);bad=copy.deepcopy(review);bad['responses']['q02']['response_sha256']='bad'
  with self.assertRaises(ValueError):r.main(bad)
  r.main(review);a=self.p['assignments'][1];path=r.out/(a['id']+'.request.json');req=json.loads(path.read_text());req['messages'][1]['content']='{}';path.write_text(json.dumps(req));report=analyze(self.p,r.out,self.gold);row=next(x for x in report['rows'] if x['id']==a['id']);self.assertEqual(row['status'],'invalid')
 def test_no_release_before_stop_and_preserve_uncertain(self):
  def fail(cid,req):
   if cid not in ('q01','q02'):raise RuntimeError('synthetic failure')
   return self.generate(cid,req)
  r=self.runner(fail);review=self.qualification(r);r.main(review)
  with self.assertRaises(ValueError):release_unstarted(self.p,r.out,self.ledger,False)
  unknown=self.ledger.db.execute("SELECT COUNT(*) FROM charges WHERE status='unknown'").fetchone()[0]
  released=release_unstarted(self.p,r.out,self.ledger,True);self.assertGreater(len(released),370)
  self.assertEqual(self.ledger.db.execute("SELECT COUNT(*) FROM charges WHERE status='unknown'").fetchone()[0],unknown)
 def test_gold_hash_is_enforced(self):
  r=self.runner();review=self.qualification(r);r.main(review);bad=copy.deepcopy(self.gold);bad['restore-yes']['answer']='NO'
  with self.assertRaises(ValueError):analyze(self.p,r.out,bad)
 def test_invalid_route_and_json(self):
  raw=self.generate('q01',request('R',self.p['qualification']['q01']['actor'],question='x'));raw['provider']='other'
  with self.assertRaises(ValueError):normalize(raw,3000,'reader')
  raw['provider']='OpenAI';raw['choices'][0]['message']['content']='bad'
  with self.assertRaises(ValueError):normalize(raw,3000,'reader')
if __name__=='__main__':unittest.main()
