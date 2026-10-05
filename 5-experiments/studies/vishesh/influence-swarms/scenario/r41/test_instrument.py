import unittest,sys,json,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import cases as c,instrument as i
class InstrumentTest(unittest.TestCase):
 def setUp(self):self.cs=c.corpus()
 def fill(self,root,maximal=False):
  maximum=0;requests=[]
  while (item:=root.next()) is not None:
   a=i.answer_fixture(root.case,item['node'])
   if maximal:
    a['rationale']='\\"'*80
    for f in a['facts']:
     f['number']=1.2345678901234567e-300;f['text']='UNSUPPORTED';f['source']='cobalt-performance'
    for row in a['cost_components']:
     for key in i.COMPONENTS:row[key]=1.2345678901234567e-300
   self.assertEqual(i.unpack_report(i.pack_report(a)),a);i.decode(json.dumps(i.wire_answer(a)),root.case,item['node']);root.accept(item,a);maximum=max(maximum,item['bytes']);requests.append(item)
  return maximum,requests
 def test_exact_counts_and_forty_identities(self):
  for stage,n in (('R41-FULL-Q',756),('R41-E0',2988)):
   roots=i.schedule(self.cs,stage);self.assertEqual(sum(len(r.nodes) for r in roots),n)
   for r in roots:
    large={x['actor'] for x in r.nodes if x['actor'].startswith(('large-','lead-'))}
    self.assertEqual(len(large),40)
    for role in c.ROLES:
     revisions=[x for x in r.nodes if x['role']==role and x['kind']=='revision']
     self.assertTrue(all(len(x['parents'])==3 and all('/initial'in p for p in x['parents']) for x in revisions))
 def test_maximal_nested_wires_and_component_gate(self):
  maximum=0;records=[]
  for root in i.schedule(self.cs,'R41-FULL-Q'):
   n,_=self.fill(root);maximum=max(maximum,n);records.append(root.export())
  self.assertTrue(i.qualification(self.cs,records)['qualified'])
  # Valid wrong internal judgment remains observed and does not veto corrected finals.
  records[0]['nodes'][2]['answer']['facts'][0]['status']='UNKNOWN'
  q=i.qualification(self.cs,records);self.assertTrue(q['qualified']);self.assertTrue(q['internal_semantic_misses'])
  final=next(x for x in records[0]['nodes'] if x['id'].endswith('/large-final'));final['answer']['cost_components'][0]['legacy_overlap']=0
  self.assertFalse(i.qualification(self.cs,records)['qualified'])
  for root in i.schedule(self.cs,'R41-E0'):
   n,_=self.fill(root,True);maximum=max(maximum,n)
  self.assertLessEqual(maximum,i.MAX_WIRE);self.assertLessEqual((maximum+512)*.125/1e6+3072*.5/1e6,i.RESERVATION)
  print('MAXIMAL_NESTED_WIRE_BYTES',maximum)
 def test_shared_check_context_and_summary_chair(self):
  root=i.schedule(self.cs,'R41-E0')[0];_,requests=self.fill(root);checks={x['node']['id']:x for x in requests if x['node']['kind']=='check'};self.assertEqual(len(checks),2)
  for item in requests:
   n=item['node'];obs=json.loads(item['wire']['messages'][1]['content'])['observation']
   if 'reports'in obs:
    for k,v in obs['reports'].items():
     restored=i.unpack_report({**v,'facts_columns':obs['report_columns']['facts'],'cost_columns':obs['report_columns']['cost_components']});self.assertEqual(restored,root.answers[k])
   if n['kind']=='final':
    for key in checks:self.assertEqual(item['parent_hashes'][key],c.digest(root.answers[key]))
    if n['role']=='chair':self.assertNotIn('documents',obs);self.assertEqual(len(obs['reports']),5)
    else:self.assertEqual(len(obs['documents']),18)
   if n['kind']=='lead':self.assertEqual(len(obs['reports']),12);self.assertEqual(len(obs['documents']),6)
  altered=copy.deepcopy(root.case);altered['gold']={};altered['page_pool']=[]
  for node_id,item in checks.items():self.assertEqual(i.compile_wire(altered,item['node'],{})['wire'],item['wire'])
 def test_failure_propagation_and_order_independent_accept(self):
  root=i.schedule(self.cs,'R41-E0')[0]
  root.fail(root.item('check-0'),'length');self.fill(root)
  finals=[x for x in root.export()['nodes'] if x['id'].endswith('-final')];self.assertEqual(len(finals),6);self.assertTrue(all(x['state']=='blocked' for x in finals))
  root=i.schedule(self.cs,'R41-E0')[0];one=root.item('truthful/large-commercial-00/initial');two=root.item('truthful/large-technical-00/initial');root.accept(two,i.answer_fixture(root.case,two['node']));root.fail(one,'length');self.fill(root)
  states={x['id']:x['state'] for x in root.export()['nodes']};self.assertEqual(states['truthful/large-final'],'blocked');self.assertEqual(states['truthful/small-final'],'valid');self.assertEqual(states['misleading/large-final'],'valid')
 def test_fixed_slots_reject_omissions_and_wrong_identities(self):
  root=i.schedule(self.cs,'R41-D1')[0];node=next(n for n in root.nodes if n['role']=='technical');a=i.answer_fixture(root.case,node);native=i.wire_answer(a)
  self.assertEqual(i.decode(json.dumps(native),root.case,node),a)
  wrong=copy.deepcopy(native);wrong['facts']['Aster/cost']=wrong['facts'].pop('Cobalt/performance')
  with self.assertRaisesRegex(ValueError,'fields'):i.decode(json.dumps(wrong),root.case,node)
  omitted=copy.deepcopy(native);omitted['facts'].pop('Cobalt/performance')
  with self.assertRaisesRegex(ValueError,'fields'):i.decode(json.dumps(omitted),root.case,node)
  native['facts']['Aster/performance']['number']=1
  accepted=i.decode(json.dumps(native),root.case,node);self.assertEqual(accepted['facts'][1]['number'],1);self.assertLess(i.score(root.case,node,accepted)['facts_correct'],6)
 def test_agenda_isolated_and_diagnostic_partition_exact(self):
  full=i.schedule(self.cs,'R41-FULL-Q');parts=i.schedule(self.cs,'R41-D1')+i.schedule(self.cs,'R41-Q0')
  self.assertEqual([r.case['id'] for r in full],[r.case['id'] for r in parts]);self.assertEqual(len(i.schedule(self.cs,'R41-D1')),1);self.assertEqual(len(i.schedule(self.cs,'R41-Q0')),8)
  records=[]
  for root in full:
   _,requests=self.fill(root);records.append(root.export())
   for item in requests:
    obs=json.loads(item['wire']['messages'][1]['content'])['observation']
    if item['node']['kind']!='check':self.assertNotIn('check_agenda',obs)
  self.assertTrue(i.partial_qualification(self.cs,records[:1],'R41-D1')['qualified']);self.assertFalse(i.qualification(self.cs,records[:1])['qualified']);self.assertTrue(i.partial_qualification(self.cs,records[1:],'R41-Q0')['qualified']);self.assertTrue(i.qualification(self.cs,records)['qualified'])
 def test_raw_bad_action_not_repaired(self):
  root=i.schedule(self.cs,'R41-FULL-Q')[0];node=next(n for n in root.nodes if n['id'].endswith('/large-final'));a=i.answer_fixture(root.case,node);a.update(action='BUY',choice=root.case['gold']['target']);accepted=i.decode(json.dumps(i.wire_answer(a)),root.case,node);self.assertEqual(accepted['choice'],a['choice']);self.assertFalse(i.score(root.case,node,accepted)['acceptable'])
if __name__=='__main__':unittest.main()
