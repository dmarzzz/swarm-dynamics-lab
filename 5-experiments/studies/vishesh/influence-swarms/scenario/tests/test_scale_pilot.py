import copy,json,sys,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import scale_pilot as sp,scale_qualification as sq
from study import scripted

def fixture(p,item):
 o=json.loads(item['wire_body']['messages'][1]['content'])
 if item['role']=='auditor':return sq.td.fixture_answer(o)
 if item['role']=='opinion':
  full={d['id']:d for d in sp.case(item['condition'])['documents']};a=scripted({**o,'documents':[full[d['id']] for d in o['documents']]})
  for f in a['findings']:f['claim']=f['claim'][:150]
  return a
 c=sp.case(item['condition']);full={**o,'documents':sq.compact_docs(c['documents'])};a=scripted(full);r=o['verified_report'];eligible={n:all(r['candidate_checks'][n][f]=='PASS' for f in sq.tp.FIELDS) for n in c['candidates']};minimum=min((r['arithmetic'][n]['total_usd'] for n in eligible if eligible[n]),default=None);a['decision_table']={n:{'eligible':eligible[n],'within_cost_tolerance':bool(eligible[n] and r['arithmetic'][n]['total_usd']<=minimum*1.03)} for n in eligible};return a

def response(item,a):return {'route':{'provider':'OpenAI','model':item['wire_body']['model']},'tool_calls':None,'content':[{'type':'text','text':json.dumps(a)}]}
class PilotTests(unittest.TestCase):
 def test_full_paths_roles_rounds_and_condition_isolation(self):
  for stage,expected in [('SP-SOL',36),('SP-LUNA',196)]:
   p=sp.Protocol(stage);maxwire=0
   while not p.complete:
    i=p.next();maxwire=max(maxwire,i['wire_bytes']);a=fixture(p,i);p.accept(i,p.check(i,response(i,a)))
   self.assertEqual(expected,p.position)
   for world,rows in p.answers.items():self.assertEqual(p.n*2+2,len(rows))
   self.assertEqual(p.n+2,len({r['agent'] for r in p.records}));self.assertLessEqual(maxwire,32768)
 def test_primary_evidence_identical_and_balanced_exposure(self):
  clean=sp.case('clean');adv=sp.case('omission');self.assertEqual([d for d in clean['documents'] if d['kind']!='comparison'],[d for d in adv['documents'] if d['kind']!='comparison'])
  for n in (8,48):
   g=sp.graph(n);self.assertTrue(all(len(set(v))==2 and i not in v for i,v in g.items()))
   self.assertEqual(n//4,sum(any(d['id']=='comparison-0' for d in sp.docs(adv,i)) for i in range(n)))
   self.assertEqual({d['id'] for d in clean['documents'] if d['kind']!='comparison'},{d['id'] for i in range(n) for d in sp.docs(clean,i) if d['kind']!='comparison'})
 def test_unknown_peer_citation_and_oversized_claim_rejected(self):
  p=sp.Protocol('SP-SOL');i=p.next();a=fixture(p,i);a['findings'][0]['citations']=['unseen-secret']
  with self.assertRaises(ValueError):p.check(i,response(i,a))
  a=fixture(p,i);a['findings'][0]['claim']='x'*301
  with self.assertRaises(AssertionError):p.check(i,response(i,a))
 def test_revisions_use_only_initial_neighbors(self):
  p=sp.Protocol('SP-SOL')
  for _ in range(p.n):i=p.next();p.accept(i,fixture(p,i))
  i=p.next();o=json.loads(i['wire_body']['messages'][1]['content']);self.assertEqual(['adviser-07','adviser-01'],[v['agent'] for v in o['peers']]);self.assertEqual('revision',o['round'])
 def test_complete_native_collector_and_budget(self):
  import tempfile,sqlite3,datetime
  from contextlib import closing
  import scale_pilot_run as run
  with tempfile.TemporaryDirectory() as d:
   db=Path(d)/'b';p=run.build('SP-SOL');mirror=sp.Protocol('SP-SOL')
   with closing(sqlite3.connect(db)) as c,c:c.execute('CREATE TABLE budget(id,cap,reserved,calls)');c.execute('INSERT INTO budget VALUES(1,8,6.5593024,297)')
   def transport(raw):
    i=mirror.next();self.assertEqual(raw,sp.encode(i['wire_body']));a=fixture(mirror,i);mirror.accept(i,a)
    return json.dumps({'model':i['wire_body']['model'],'provider':'OpenAI','usage':{'prompt_tokens':1,'completion_tokens':1,'cost':.00001},'choices':[{'finish_reason':'stop','message':{'content':json.dumps(a)}}]}).encode()
   s=run.collect(p,Path(d)/'out',db,transport,(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=1)).isoformat());self.assertTrue(s['complete']);self.assertEqual((36,36,0),(s['calls'],s['valid'],s['usage_missing']))
   with closing(sqlite3.connect(db)) as c:r=c.execute('SELECT reserved,calls FROM budget').fetchone()
   self.assertAlmostEqual(7.6846784,r[0]);self.assertEqual(333,r[1]);self.assertTrue(json.loads((Path(d)/'out/assessment.json').read_text())['complete'])
 def test_dynamic_relay_refuses_modified_wire(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   relay=sp.DynamicRelay('SP-SOL',Path(d)/'relay');i=relay.protocol.next();w=copy.deepcopy(i['wire_body']);w['messages'][0]['content']='changed'
   with self.assertRaises(ValueError):relay.send(sp.encode(w),lambda _:self.fail('no dispatch'))
   self.assertEqual(0,relay.count);self.assertTrue(relay.stopped)
 def test_worst_allowed_peer_payloads_fit_without_truncation(self):
  for stage in ('SP-SOL','SP-LUNA'):
   p=sp.Protocol(stage)
   while not p.complete:
    i=p.next();a=fixture(p,i)
    if i['role']=='opinion':
     allowed=i['wire_body']['response_format']['json_schema']['schema']['properties']['findings']['items']['properties']['citations']['items']['enum'];a['findings']=[{'claim':'x'*300,'citations':allowed[:13]} for _ in range(3)]
    p.accept(i,p.check(i,response(i,a)))
   self.assertTrue(p.complete)
 def test_manifest_roundtrip_matches_frozen_packet(self):
  import scale_pilot_run as run
  for stage in sp.CONFIGS:self.assertEqual(run.build(stage),json.loads((BASE/f'reviews/{stage}-packet.json').read_text()))
