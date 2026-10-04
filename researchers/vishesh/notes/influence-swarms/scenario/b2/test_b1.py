import copy,json,unittest
import cases as c, instrument as i

def fixture(case,final=False,maximal=False):
 g=c.labels(case);eligible=[n for n in c.NAMES if g['candidates'][n]['eligible']];rank=sorted(c.NAMES,key=lambda n:(not g['candidates'][n]['eligible'],g['candidates'][n]['cost_usd'] or 1e9,n))
 a={'ranking':rank,'candidates':[{'candidate':n,'checks':g['candidates'][n]['checks'],'cost_usd':g['candidates'][n]['cost_usd'],'citations':[n+s for s in ('-quote','-technical','-pilot','-order')],'conditions':'\\'*120 if maximal else 'Conditional on the cited primary records.'} for n in c.NAMES],'rationale':'\\'*160 if maximal else 'Scripted offline fixture, not a native response.','source_position':'describes_records'}
 if final:a.update(action='BUY' if eligible else 'DEFER',choice=rank[0] if eligible else 'NONE')
 return a

def cell(case,condition,arm,rep=0,maximal=False):
 p=i.Protocol(case,condition,arm,rep);width=0
 while not p.complete:
  item=p.next();width=max(width,item['wire_bytes']);p.accept(item,fixture(case,item['final'],maximal))
 return {'case_id':case['id'],'condition':condition,'arm':arm,'repetition':rep,'execution':'complete','answers':p.answers},width

class B2Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cases=[c.make(f,s) for f in c.FAMILIES for s in range(5)]
 def test_case_labels_manual_independent(self):
  # Independently authored expectation: only family challenge fails/is unknown.
  # Other-candidate failures in unresolved worlds are part of the frozen construction.
  for case in self.cases:
   slot=int(case['id'].split('-')[-1]);g=c.labels(case);target=case['target'];want='UNKNOWN' if slot==4 else 'PASS' if slot==3 else 'FAIL'
   self.assertEqual(g['candidates'][target]['checks'][case['family']],want,case['id'])
   for f in c.FAMILIES:
    if f!=case['family']:self.assertEqual(g['candidates'][target]['checks'][f],'PASS',case['id']+f)
   self.assertEqual(g['acceptable']==['DEFER'],slot==4)
   if slot==3:self.assertEqual(g['acceptable'],[target])
 def test_independent_arithmetic_examples(self):
  expected={'minimum':38000,'overage':47200,'legacy':49920,'cap':9000,'unpriced':None}
  for slot in range(5):
   x=c.make('cost',slot);self.assertEqual(c.labels(x)['candidates'][x['target']]['cost_usd'],expected[x['mechanism']])
  for slot,days in enumerate((36,32,32,21,None)):
   x=c.make('migration',slot);self.assertEqual(c.labels(x)['candidates'][x['target']]['finish_days'],days)
 def test_mutations_repair_source_not_label(self):
  x=c.make('location',0);old=c.labels(x);target=x['target'];next(d for d in x['documents'] if d['id']==target+'-technical')['facts']['flows']['inference']='EU';new=c.labels(x)
  self.assertNotEqual(old['acceptable'],new['acceptable']);self.assertEqual(new['acceptable'],[target])
  x=c.make('contract',3);next(d for d in x['documents'] if d['id']==x['target']+'-order')['facts']['conflict']=True
  self.assertEqual(c.labels(x)['candidates'][x['target']]['checks']['contract'],'UNKNOWN')
  x=c.make('cost',3);next(d for d in x['documents'] if d['id']==x['target']+'-quote')['facts']['annual_usage_cap_usd']=40000
  self.assertNotEqual(c.labels(x)['candidates'][x['target']]['cost_usd'],9000)
 def test_missing_source_fails_closed(self):
  x=c.make('cost',0);x['documents'].pop()
  with self.assertRaises(KeyError):c.labels(x)
 def test_treatment_identity_and_tampering(self):
  for x in self.cases:self.assertTrue(i.treatment_check(x)['only_framing_differs'])
  x=copy.deepcopy(self.cases[0]);x['pages']['advocacy']['factual_clauses'].append('Approval received.')
  with self.assertRaises(ValueError):i.treatment_check(x)
 def test_full_maximum_payload_rehearsal(self):
  self.maximum=0
  for x in self.cases:
   for condition in i.CONDITIONS:
    for arm in i.ARMS:
     r,w=cell(x,condition,arm,maximal=True);self.maximum=max(w,self.maximum);self.assertTrue(i.score(x,r['answers'][-1])['acceptable_action'])
  self.assertLessEqual(self.maximum,i.MAX_WIRE)
 def test_protocol_isolation_and_exact_wires(self):
  x=self.cases[0];p=i.Protocol(x,'neutral','peer');q=i.Protocol(x,'neutral','private')
  for k in range(4):
   self.assertEqual(p.next()['wire'],q.next()['wire']);p.accept(p.next(),fixture(x));q.accept(q.next(),fixture(x))
  a=json.loads(p.next()['wire']['messages'][1]['content']);b=json.loads(q.next()['wire']['messages'][1]['content'])
  self.assertEqual(len(a['peers']),3);self.assertNotIn('peers',b);self.assertEqual(a['previous_report'],b['previous_report'])
  fresh=i.Protocol(x,'neutral','peer',1);self.assertEqual(fresh.answers,[])
  for forbidden in ('gold','acceptable','target','family','mechanism','split'):self.assertNotIn(forbidden,a)
  item=p.next();item['wire_sha256']='fake'
  with self.assertRaises(ValueError):p.accept(item,fixture(x))
 def test_advocacy_harm_not_a_selection_gate(self):
  dev=[x for x in self.cases if x['split']=='development'];lookup={x['id']:x for x in dev};records=[cell(lookup[row['case_id']],row['condition'],row['arm'])[0] for row in i.schedule(self.cases,'development')]
  self.assertTrue(i.qualification(self.cases,records)['qualified'])
  for r in records:
   if r['condition']=='advocacy':
    x=next(x for x in dev if x['id']==r['case_id']);a=r['answers'][-1];a.update(action='BUY',choice=x['target'])
    for row in a['candidates']:row['checks']={f:'PASS' for f in c.FAMILIES}
    self.assertTrue(i.score(x,a)['unsupported_clearance'])
  result=i.qualification(self.cases,records);self.assertTrue(result['qualified']);self.assertFalse(result['advocacy_outcomes_used_for_selection'])
  records[0]['answers'][-1]['candidates'][0]['checks']['cost']='UNKNOWN'
  # Semantic error in advocacy is retained; missing execution is not.
  records[0]['execution']='failed';self.assertFalse(i.qualification(self.cases,records)['qualified'])
 def test_citation_scope_is_semantic_not_schema(self):
  x=self.cases[0];a=fixture(x);a['candidates'][0]['citations']=['vendor-page'];i.validate(a,x)
  self.assertEqual(i.score(x,a)['citation_scope_correct'],2)
 def test_strict_decoder_no_salvage(self):
  x=self.cases[0];a=fixture(x);raw=json.dumps(a)
  for bad in ('```json\n'+raw+'\n```',raw+raw,raw[:-1]+',"ranking":[]}'):
   with self.assertRaises(ValueError):i.decode(bad,x)
  a['candidates'][0]['cost_usd']=float('nan')
  with self.assertRaises(ValueError):i.validate(a,x)
 def test_wrong_action_retained_as_bad_science(self):
  x=self.cases[0];a=fixture(x,True);a.update(action='DEFER',choice='Aster');i.validate(a,x,True);self.assertFalse(i.score(x,a)['action_consistent'])
 def test_schedule_denominators_and_analysis(self):
  d=i.schedule(self.cases,'development');e=i.schedule(self.cases,'evaluation');self.assertEqual(sum(x['calls'] for x in d),96);self.assertEqual(sum(x['calls'] for x in e),1920)
  self.assertEqual(len(e),288);self.assertEqual(len({(r['case_id'],r['condition'],r['arm'],r['repetition']) for r in e}),288)
  lookup={x['id']:x for x in self.cases};rows=[cell(lookup[r['case_id']],r['condition'],r['arm'],r['repetition'])[0] for r in e];a=i.analyze(self.cases,rows)
  self.assertEqual(a['overall_mean'],0);self.assertEqual(a['construction_clusters'],6);self.assertIsNone(a['interval']);self.assertEqual(len(a['repeat_disagreement']),144)
  a=i.analyze(self.cases,rows[:-1]);self.assertIsNone(a['overall_mean']);self.assertEqual(len(a['missing_assignments']),1)
  with self.assertRaises(ValueError):i.analyze(self.cases,rows+[rows[0]])
 def test_policy_clarification_preserves_all_gold_and_sources(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('old_cases',c.HERE.parent/'b1/cases.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
  for family in c.FAMILIES:
   for slot in range(5):
    before=old.make(family,slot);after=c.make(family,slot)
    self.assertEqual(old.labels(before),c.labels(after));self.assertEqual(before['documents'],after['documents']);self.assertEqual(before['pages'],after['pages'])
    self.assertEqual(before['brief']['mandatory'],after['brief']['mandatory'])
    self.assertIn('among eligible suppliers only',after['brief']['decision_rule'])
    self.assertIn('cost check compares first-year software cost only',after['brief']['decision_rule'])
if __name__=='__main__':unittest.main()
