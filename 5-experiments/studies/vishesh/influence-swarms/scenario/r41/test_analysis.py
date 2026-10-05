import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import cases as c,instrument as i,analysis as a
class AnalysisTest(unittest.TestCase):
 def test_missing_assignments_never_safe(self):
  v=a.analyze(c.corpus(),[]);self.assertEqual(v['assigned_final_decisions'],108);self.assertEqual(v['observed_final_decisions'],0);self.assertEqual(v['contrasts']['primary_large_vs_generalist']['bounds'],[-2,2]);self.assertIsNone(v['contrasts']['primary_large_vs_generalist']['point'])
 def test_final_projection_and_one_wrong_action(self):
  cases=c.corpus();records=[]
  for root in i.schedule(cases,'R41-E0'):
   records.append({'case_id':root.case['id'],'repetition':root.repetition,'nodes':[{'id':n['id'],'state':'valid','answer':i.answer_fixture(root.case,n)} for n in root.nodes if n['kind']=='final']})
  v=a.analyze(cases,records);self.assertEqual(v['observed_final_decisions'],108);self.assertEqual(v['contrasts']['primary_large_vs_generalist']['point'],0)
  bad=next(n for n in records[0]['nodes'] if n['id']=='misleading/large-final');bad['answer'].update(action='DEFER',choice='NONE');v=a.analyze(cases,records);self.assertAlmostEqual(v['contrasts']['primary_large_vs_generalist']['point'],1/18)
  bad['state']='blocked';bad['answer']=None;v=a.analyze(cases,records);self.assertEqual(v['observed_final_decisions'],107);self.assertEqual(v['contrasts']['primary_large_vs_generalist']['bounds'],[0,1/18]);self.assertIsNone(v['contrasts']['primary_large_vs_generalist']['point'])
if __name__=='__main__':unittest.main()
