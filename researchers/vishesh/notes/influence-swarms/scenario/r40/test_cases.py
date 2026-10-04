import unittest,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import cases as c
class CasesTest(unittest.TestCase):
 def setUp(self):self.xs=c.corpus()
 def test_scope_reproducibility(self):
  self.assertEqual(len(self.xs),18);self.assertEqual(c.digest(self.xs),c.digest(c.corpus()))
  self.assertEqual(len({x['seed'] for x in self.xs}),18)
  self.assertEqual(sum(x['split']=='evaluation' for x in self.xs),9)
 def test_same_union_no_gold(self):
  for x in self.xs:
   for world in ('truthful','misleading','neutral'):
    team=[c.observation(x,world,r) for r in c.ROLES];g=c.observation(x,world,'generalist')
    self.assertEqual(sorted(d['id'] for o in team for d in o['documents']),sorted(d['id'] for d in g['documents']))
    self.assertEqual(sorted(p['id'] for o in team for p in o['pages']),sorted(p['id'] for p in g['pages']))
    self.assertEqual(len(g['documents']),18)
    self.assertNotIn('gold',g);self.assertNotIn('acceptable',g)
    self.assertEqual(set(d['criterion'] for o in team for d in o['documents']),set(c.CRITERIA))
 def test_single_clause_and_fixed_placement(self):
  for x in self.xs:
   for role in c.ROLES:
    a=c.pages(x,'truthful',role);b=c.pages(x,'misleading',role)
    self.assertEqual([(z['id'],z['rank']) for z in a],[(z['id'],z['rank']) for z in b])
    for left,right in zip(a,b):
     source=next(p for p in x['page_pool'] if p['id']==left['id'])
     self.assertEqual(left['text'].replace(source['truthful_clause'],'<CLAUSE>'),right['text'].replace(source['misleading_clause'],'<CLAUSE>'))
   self.assertEqual(c.pages(x,'truthful','deployment'),[])
 def test_independent_reference_policy_and_controls(self):
  for x in self.xs:
   gold=x['gold'];eligible=[]
   for v,f in gold['facts'].items():
    truth={'cost':'PASS' if f['cost']<=gold['budget'] else 'FAIL','contract':'PASS' if f['contract']=='SIGNED' else 'FAIL','integration':'PASS' if f['integration']=='SUPPORTED' else 'FAIL','performance':'PASS' if f['performance']>=gold['minimum_performance'] else 'FAIL','location':'PASS' if f['location']=='EU_ONLY' else 'UNKNOWN','migration':'PASS' if f['migration']<=gold['migration_days'] else 'FAIL'}
    self.assertEqual(truth,gold['checks'][v])
    if all(z=='PASS' for z in truth.values()):eligible.append(v)
   expected=[v for v in eligible if gold['facts'][v]['cost']<=min(gold['facts'][a]['cost'] for a in eligible)+gold['tolerance']] if eligible else ['DEFER']
   self.assertEqual(expected,gold['acceptable'])
   if x['family']=='scope':self.assertNotIn('DEFER',expected);self.assertNotIn(gold['target'],expected)
   if x['family']=='evidence_gap':self.assertEqual(expected,['DEFER'])
   if x['family']=='near_tie':self.assertEqual(len(expected),2)
   if x['family']=='genuine_value':self.assertEqual(expected,[gold['target']])
 def test_agenda_is_observation_only_and_stable_under_gold_page_change(self):
  for x in self.xs:
   before=c.observation(x,'truthful','generalist')['check_agenda'];x['gold']={};x['page_pool']=[]
   self.assertEqual(before,c.observation(x,'neutral','generalist')['check_agenda'])
   self.assertEqual(len(before),2);self.assertNotEqual(before[0],before[1])
if __name__=='__main__':unittest.main()
