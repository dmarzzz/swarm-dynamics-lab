import unittest,json
import instrument as i
import native as n
class NativeTests(unittest.TestCase):
 def test_all_fifty_actual_founder_packets_fit(self):
  w=i.world(20261004)
  for p in w['members']:
   packet,cases=n.founder_packet(w,p);wire=n.request('learn',packet)
   self.assertLessEqual(i.packet_bytes(wire),8000);self.assertNotIn('"truth"',json.dumps(wire));self.assertNotIn('"routes"',json.dumps(wire))
 def test_oracle_and_fault_grades(self):
  w=i.world(100);p=w['members'][0];packet,cases=n.founder_packet(w,p)
  answer={'note':i.note(p,w['routes'][p]),'actions':[{'case':c['case'],'action':c['truth']} for c in cases]}
  self.assertTrue(n.grade_founder(answer,w,p,cases)['qualified']);answer['actions'][0]['action']='hold';self.assertFalse(n.grade_founder(answer,w,p,cases)['qualified'])
 def test_no_duplicate_or_invented_actions(self):
  w=i.world(3);p=w['members'][0];_,cases=n.founder_packet(w,p)
  self.assertFalse(n.score_actions({'actions':[{'case':cases[0]['case'],'action':'allow'}]*6},cases)['valid'])
 def test_static_has_no_question(self):
  w=i.world(4);p=w['members'][0];g=i.Institution(w,'static');g.notes[p]=i.note(p,w['routes'][p]);packet=n.teach_packet(g,p);self.assertNotIn('question',packet)
 def test_teacher_requires_correct_semantics(self):
  w=i.world(5);p=w['members'][0];reply={'note':i.note(p,w['routes'][p]),'explanation':'Consult both witnesses.'};self.assertTrue(n.qualified_teacher(reply,w,p));reply['note']['witnesses']=['position_00','position_01'];self.assertFalse(n.qualified_teacher(reply,w,p))
 def test_truncation_and_model_substitution_fail(self):
  for model,finish in [('gpt-6-sol-pro','stop'),('gpt-6-sol','length')]:
   with self.assertRaises(ValueError):n.parse({'model':model,'choices':[{'finish_reason':finish,'message':{'content':'{}'}}]})
if __name__=='__main__':unittest.main()
