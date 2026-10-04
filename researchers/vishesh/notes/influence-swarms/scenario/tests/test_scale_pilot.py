import copy,json,sys,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import scale_pilot as sp,scale_qualification as sq
from study import scripted

def fixture(p,item):
 o=json.loads(item['wire_body']['messages'][1]['content'])
 if item['role']=='auditor':return sq.td.fixture_answer(o)
 if item['role']=='opinion':
  a=scripted(o)
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
  a=fixture(p,i);a['findings'][0]['claim']='x'*151
  with self.assertRaises(AssertionError):p.check(i,response(i,a))
 def test_revisions_use_only_initial_neighbors(self):
  p=sp.Protocol('SP-SOL')
  for _ in range(p.n):i=p.next();p.accept(i,fixture(p,i))
  i=p.next();o=json.loads(i['wire_body']['messages'][1]['content']);self.assertEqual(['adviser-07','adviser-01'],[v['agent'] for v in o['peers']]);self.assertEqual('revision',o['round'])
