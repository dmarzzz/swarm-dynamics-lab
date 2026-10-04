import copy,unittest
from contract import ARMS,actor,run_policy
from study import evaluate

def record(i=0,gold='1.00'):
 return {'id':i,'gold':{'status':'ok' if gold is not None else 'missing','value':gold},'pipelines':{k:{'candidate':{'status':'ok','value':'1.00','confidence':.9},'valid':True,'wall_s':.5} for k in 'ABCDE'}}
class EvalTests(unittest.TestCase):
 def test_assigned_denominator_includes_unscorable(self):
  rows,s=evaluate([record(),record(1,None)]);self.assertEqual(len(rows),10);self.assertEqual(s['assigned'],2);self.assertEqual(s['scorable'],1);self.assertEqual(s['unscorable'],1)
 def test_wrong_majority_not_hidden(self):
  rows,s=evaluate([record(gold='2.00')]);self.assertEqual(s['arms']['agreement']['wrong'],1);self.assertEqual(s['arms']['agreement']['correct'],0)
 def test_checker_cost_is_measured_calls(self):
  rows,s=evaluate([record()]);self.assertEqual(s['arms']['always-check']['checks'],2);self.assertEqual(s['arms']['always-check']['checker_wall_s'],1);self.assertEqual(s['arms']['selective-check']['checker_wall_s'],0)
 def test_label_mutation_cannot_change_actions(self):
  a=record();b=copy.deepcopy(a);b['gold']['value']='900.00'
  for arm in ARMS:self.assertEqual(run_policy(actor(a),lambda k:a['pipelines'][k]['candidate'],arm),run_policy(actor(b),lambda k:b['pipelines'][k]['candidate'],arm))
 def test_missing_checker_does_not_create_acceptance(self):
  r=record()
  for k,v in zip('ABC',['1.00','2.00','3.00']):r['pipelines'][k]['candidate']['value']=v
  for k in 'DE':r['pipelines'][k]['candidate']={'status':'missing','value':None,'confidence':0}
  rows,s=evaluate([r]);self.assertEqual(s['arms']['selective-check']['refer'],1)
 def test_error_not_silently_valid(self):
  r=record();r['pipelines']['D']['valid']=False;rows,s=evaluate([r]);self.assertEqual(s['invalid_ocr'],1);self.assertFalse(all(x['execution_valid'] for x in rows))
 def test_receipt_identity_preserved(self):
  rows,s=evaluate([record(5),record(11)]);self.assertEqual({r['id'] for r in rows},{5,11})
if __name__=='__main__':unittest.main()
