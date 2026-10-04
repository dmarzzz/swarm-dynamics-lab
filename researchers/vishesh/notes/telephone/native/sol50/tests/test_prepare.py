import sys,json,unittest,copy,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import cases,contract
class Preparation(unittest.TestCase):
 def test_all_targets_have_visible_spans(self):
  b=cases.build();ids={x['id'] for x in b['case']['records']}
  self.assertEqual(len(b['gold']['targets']),12)
  self.assertTrue(all(x['source_id'] in ids and x['required_meaning'] for x in b['gold']['targets']))
 def test_machine_and_text_reference_agree_on_controls(self):
  for c in cases.controls():self.assertEqual(cases.exact_source_baseline(cases.control_packet(c['name'])),cases.decide(c['state']));self.assertEqual(cases.decide(c['state']),c['expected'])
 def test_reorder_ids_and_aliases_preserve_reference(self):
  for c in cases.controls():
   p=cases.control_packet(c['name']);random.Random(73).shuffle(p['records'])
   for i,r in enumerate(p['records']):r['id']='opaque-'+str(i);r['text']=r['text'].replace('Cedar','Juniper').replace('Bay','Delta')
   self.assertEqual(cases.exact_source_baseline(p),c['expected'])
 def test_duplicate_reports_do_not_supply_missing_conditions(self):
  p=cases.actor_packet();p['records']+=copy.deepcopy(p['records'][2:3])*5
  self.assertEqual(cases.exact_source_baseline(p),'HOLD')
 def test_corrected_threshold_matters(self):
  p=cases.control_packet('all_conditions');self.assertEqual(cases.exact_source_baseline(p),'GO')
  p['records'][1]['text']='Correction: the latency limit is 80 ms, replacing 120 ms. This changes the limit, not earlier measurements.'
  self.assertEqual(cases.exact_source_baseline(p),'HOLD')
 def test_lossless_copy_fits_and_survives_fifty_hops(self):
  p=cases.actor_packet();a={'handoff':cases.copy_handoff(p),'decision':'HOLD'};original=contract.canonical(a)
  self.assertLessEqual(len(original.encode()),contract.MAX_OUTPUT)
  for _ in range(50):a=contract.parse(contract.canonical(a));contract.request(previous=a)
  self.assertEqual(contract.canonical(a),original)
 def test_actor_has_no_gold_or_operator_history(self):
  p=cases.actor_packet();req=contract.request(p)
  self.assertEqual(set(json.loads(req['messages'][1]['content'])),{'source_packet'})
  self.assertNotIn('gold',contract.canonical(req));self.assertNotIn('state',json.loads(req['messages'][1]['content'])['source_packet'])
  bad=copy.deepcopy(p);bad['gold']='HOLD'
  with self.assertRaises(ValueError):contract.request(bad)
 def test_chain_exactly_fifty_unique_fresh_agents(self):
  a=contract.assignments();self.assertEqual(len(a),50);self.assertEqual(len({x['agent_id'] for x in a}),50)
  for i,x in enumerate(a):self.assertEqual(x['parent'],None if i==0 else a[i-1]['agent_id'])
 def test_bounded_envelope_preserves_prior_cost(self):
  e=contract.envelope();self.assertEqual(e['max_calls'],52);self.assertEqual(e['prior_cumulative_nano'],113744701);self.assertLess(e['total_upper_nano'],e['cap_nano'])
 def test_json_fence_only_no_prose_repair(self):
  t=contract.canonical({'handoff':'Evidence as reported; approval unknown.','decision':'HOLD'})
  self.assertEqual(contract.parse(t),contract.parse('```json\n'+t+'\n```'))
  for bad in ('prefix'+t,t+'suffix','{"handoff":"x","decision":"GO","gold":1}','{"handoff":"","decision":"HOLD"}'):
   with self.assertRaises(ValueError):contract.parse(bad)
 def test_long_input_refused_without_truncation(self):
  with self.assertRaises(ValueError):contract.request(previous={'handoff':'x'*9000,'decision':'HOLD'})
 def test_prior_handoff_is_forwarded_exactly(self):
  x={'handoff':'  quoted\ntext and unicode ✓  ','decision':'UNKNOWN'}
  self.assertEqual(json.loads(contract.request(previous=x)['messages'][1]['content'])['previous_handoff'],x)
if __name__=='__main__':unittest.main()
