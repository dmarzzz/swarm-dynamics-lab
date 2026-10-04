import sys,json,time,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT.parent/'src')]
# Avoid ambiguous contract module path: sol50 must precede legacy native modules.
from cases import actor_packet,copy_handoff
from contract import MODEL
from engine import execute_chain,digest
from ledger import Ledger
class EngineTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name);self.l=Ledger(self.p/'budget.sqlite',5000000000,'Telephone owner USD5 cumulative direct OpenRouter authorization, 2026-10-04');self.packet=actor_packet();self.q={'passed':True,'model':MODEL,'packet_sha256':digest(self.packet)}
  self.l.reserve('history','A1','infrastructure',113744701,'prior');self.l.settle('history',113744701)
 def tearDown(self):self.l.db.close();self.tmp.cleanup()
 def fake(self,req):
  payload=json.loads(req['messages'][1]['content']);obj=payload.get('previous_handoff') or {'handoff':copy_handoff(payload['source_packet']),'decision':'HOLD'}
  return {'model':MODEL,'provider':'OpenAI','choices':[{'finish_reason':'stop','message':{'role':'assistant','content':json.dumps(obj)}}],'usage':{'prompt_tokens':500,'completion_tokens':300,'total_tokens':800,'cost':.004}}
 def test_fifty_calls_preserve_cumulative_cost_and_exact_parent(self):
  r=execute_chain(self.packet,self.p/'run',self.l,self.fake,time.time()+600,self.q);self.assertEqual(r['valid'],50);self.assertEqual(r['budget']['total_upper_nano'],313744701)
  second=json.loads((self.p/'run/sol-02.request.json').read_text());first=json.loads((self.p/'run/sol-01.response.json').read_text())
  self.assertEqual(json.loads(second['messages'][1]['content'])['previous_handoff'],json.loads(first['choices'][0]['message']['content']))
 def test_route_failure_stops_no_retry_and_preserves_raw(self):
  def bad(req):r=self.fake(req);r['provider']='Other';return r
  s=execute_chain(self.packet,self.p/'bad',self.l,bad,time.time()+600,self.q);self.assertEqual((s['failed'],s['unstarted']),(1,49));self.assertEqual(s['budget']['unresolved_model_calls'],1);self.assertTrue((self.p/'bad/sol-01.response.json').exists())
 def test_semantic_error_is_collected_not_repaired(self):
  def badmeaning(req):r=self.fake(req);r['choices'][0]['message']['content']=json.dumps({'handoff':'Everything passed.','decision':'GO'});return r
  s=execute_chain(self.packet,self.p/'semantic',self.l,badmeaning,time.time()+600,self.q);self.assertEqual(s['valid'],50);self.assertTrue(all(x['decision']=='GO' for x in s['assignments']));self.assertFalse(s['semantic_review_complete'])
 def test_qualification_required_before_any_dispatch(self):
  with self.assertRaises(ValueError):execute_chain(self.packet,self.p/'never',self.l,lambda _:self.fail(),time.time()+600,{})
if __name__=='__main__':unittest.main()
