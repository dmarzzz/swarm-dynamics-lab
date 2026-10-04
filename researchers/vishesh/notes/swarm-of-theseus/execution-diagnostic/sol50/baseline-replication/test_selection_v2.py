import unittest
import selection_v2 as s,contract
class SelectionTests(unittest.TestCase):
 def test_correct_and_wrong_choices_are_preserved_without_gold(self):
  for pair in (['a','b'],['wrong-a','wrong-b']):
   value={'witnesses':pair};actual=s.to_engine('select',value);self.assertEqual(actual,{'witnesses':pair,'note':{'witnesses':pair}});actual['note']['witnesses'].append('x');self.assertEqual(value,{'witnesses':pair});self.assertEqual(len(actual['witnesses']),2)
 def test_duplicate_or_divergent_field_is_rejected(self):
  for value in ({'witnesses':['a','b'],'note':{'witnesses':['c','d']}},{'witnesses':['a','a']},{'witnesses':[]}):
   with self.assertRaises(ValueError):s.to_engine('select',value)
 def test_only_select_wire_changes(self):
  for family in ('release','failover','delegation'):
   for phase in ('learn','select','attest','decide','question','teach','commit'):
    new=s.wire(phase,family,{});old=contract.wire(phase,family,{});self.assertTrue(contract.validate_wire(new))
    if phase=='select':self.assertNotEqual(new['messages'][0]['content'],old['messages'][0]['content']);self.assertEqual({k:v for k,v in new.items() if k!='messages'},{k:v for k,v in old.items() if k!='messages'})
    else:self.assertEqual(new,old)
if __name__=='__main__':unittest.main()
