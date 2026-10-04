import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import contract as c
class ContractTests(unittest.TestCase):
 def setUp(self):
  self.records=[{'id':'s1','text':'The test has not been performed.','gold':'private','family':'secret'}]
  self.raw={'model':c.MODEL,'role':'assistant','stop_reason':'end_turn','content':[{'type':'text','text':'The test is unperformed.'}],'usage':{'input_tokens':100,'output_tokens':20}}
 def test_72_assignments_unique_and_balanced(self):
  a=c.assignments([str(i) for i in range(8)])
  self.assertEqual(len(a),72);self.assertEqual(len({x['call_id'] for x in a}),72)
  self.assertEqual(a,c.assignments([str(i) for i in range(8)]))
  for component in range(8):
   self.assertEqual({(x['arm'],x['hop']) for x in a if x['component']==str(component)},{(a,h) for a in c.ARMS for h in (1,2,3)})
 def test_actor_projection_excludes_gold_and_context(self):
  req=c.request('P',1,self.records);mutated=copy.deepcopy(self.records);mutated[0]['gold']='changed'
  self.assertEqual(req,c.request('P',1,mutated));self.assertNotIn('secret',c.canonical(req));self.assertNotIn('private',c.canonical(req))
  self.assertEqual(len(req['messages']),1)
 def test_later_hops_only_see_previous_except_retrieval(self):
  for arm in ('P','S'):
   q=c.request(arm,2,self.records,'previous');self.assertNotIn('sources',json.loads(q['messages'][0]['content']))
  self.assertIn('sources',json.loads(c.request('R',2,self.records,'previous')['messages'][0]['content']))
 def test_no_missing_parent_or_hop_one_previous(self):
  for arm in c.ARMS:
   with self.assertRaises(ValueError):c.request(arm,2,self.records)
   with self.assertRaises(ValueError):c.request(arm,1,self.records,'unallowed')
 def test_sources_must_be_unique_and_nonempty(self):
  for rows in ([],self.records*2,[{'id':'','text':'a'}]):
   with self.assertRaises(ValueError):c.request('P',1,rows)
 def test_no_silent_truncation(self):
  with self.assertRaises(ValueError):c.request('P',1,[{'id':'a','text':'x'*7168}])
  for v in (0,-1,8193,True,None):
   with self.assertRaises(ValueError):c.validate_count(v)
 def test_actual_route_and_stop_checked(self):
  for key,value in [('model','another-model'),('stop_reason','max_tokens'),('role','user')]:
   raw={**self.raw,key:value}
   with self.assertRaises(ValueError):c.response(raw,'P')
 def test_usable_response_not_semantic_pass(self):
  got=c.response(self.raw,'P');self.assertEqual(got['token_cost_nano'],200000);self.assertNotIn('retention',got)
 def test_structured_shape_required_without_repair(self):
  with self.assertRaises(ValueError):c.response(self.raw,'S')
  raw=copy.deepcopy(self.raw);raw['content'][0]['text']=json.dumps({'claims':[{'claim':'unperformed','status':'reported','uncertainty':'none','source_ids':['s1']}]})
  self.assertEqual(c.response(raw,'S')['output_tokens'],20)
 def test_usage_and_thinking_faults(self):
  for usage in ({'input_tokens':100,'output_tokens':513},{'input_tokens':True,'output_tokens':1},{'input_tokens':1,'output_tokens':1,'cache_read_input_tokens':20}):
   with self.assertRaises(ValueError):c.response({**self.raw,'usage':usage},'P')
  with self.assertRaises(ValueError):c.response({**self.raw,'content':[{'type':'thinking','text':'not evidence'}]},'P')
 def test_envelope_preserves_total_cap(self):
  e=c.envelope(72);self.assertEqual(e['maximum_token_cost_nano'],774144000)
  self.assertEqual(e['api_cap_nano']+e['infrastructure_cap_nano'],2000000000)
  with self.assertRaises(ValueError):c.envelope(73)
if __name__=='__main__': unittest.main()
