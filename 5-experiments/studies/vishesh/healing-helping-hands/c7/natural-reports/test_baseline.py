import unittest,json,copy,hashlib
from pathlib import Path
from baseline import reconcile,actor_input
ROOT=Path(__file__).resolve().parent
class Audit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.sources=json.loads((ROOT/'sources.json').read_text());cls.cases=json.loads((ROOT/'cases.json').read_text())
 def test_all_gold(self):
  for c in self.cases:self.assertEqual(reconcile(c['query'],[s for s in self.sources if s['id'] in c['source_ids']])['label'],c['expected'])
 def test_snapshot_hashes(self):
  for s in self.sources:self.assertEqual(hashlib.sha256(s['excerpt'].encode()).hexdigest(),s['excerpt_sha256'])
 def test_reorder_duplicate(self):
  for c in self.cases:
   s=[s for s in self.sources if s['id'] in c['source_ids']];self.assertEqual(reconcile(c['query'],s)['label'],reconcile(c['query'],list(reversed(s+s)))['label'])
 def test_metric_geography_publisher_scope(self):
  for key in ('metric','geography','publisher'):
   for c in self.cases:
    q={**c['query'],key:'NOT_SUPPLIED'};self.assertEqual(reconcile(q,self.sources)['label'],'UNCERTAIN')
 def test_historical_cutoff_changes_applicable_vintage(self):
  c=next(x for x in self.cases if x['id']=='bls-2024jan-superseded');q={**c['query'],'cutoff':'2024-02-02'}
  self.assertEqual(reconcile(q,self.sources)['label'],'SUPPORT');self.assertEqual(reconcile(c['query'],self.sources)['label'],'REFUTE')
 def test_unresolved_conflict_synthetic_fault_only(self):
  s=copy.deepcopy(next(s for s in self.sources if s['id']=='bea-q1'));t={**s,'id':'SYNTHETIC-FAULT','excerpt':s['excerpt'].replace('rate of 1.3','rate of 9.9')};q=self.cases[0]['query'];self.assertEqual(reconcile(q,[s,t])['label'],'UNCERTAIN')
 def test_unknown_format_abstains(self):
  s={**self.sources[0],'excerpt':'No measurement supplied.'};self.assertEqual(reconcile(self.cases[0]['query'],[s])['label'],'UNCERTAIN')
 def test_actor_gold_isolation(self):
  for c in self.cases:
   a=actor_input(c,self.sources);d={**c,'expected':'CHANGED','rationale':'SECRET','label_evidence':[{'foo':'gold'}]};self.assertEqual(a,actor_input(d,self.sources));self.assertEqual(set(a),{'instruction','query','sources'})
if __name__=='__main__':unittest.main()
