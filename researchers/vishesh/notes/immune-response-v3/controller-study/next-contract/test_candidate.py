import unittest
import candidate
import cases
class Candidate(unittest.TestCase):
 def test_only_serialization_instruction_and_schema_order_differ(self):
  c=cases.development()[0];o=cases.observe(c,c['initial'],1,[],[]);d=cases.diagnosis(o);a=candidate.action_request(c,o,d,'action_first');b=candidate.action_request(c,o,d,'justification_first')
  self.assertEqual(a['observation'],b['observation']);self.assertEqual(a['response_schema']['properties'],b['response_schema']['properties']);self.assertEqual(list(b['response_schema']['properties']),['reason','action_id']);self.assertEqual(a['instructions'].split('Serialize fields')[0],b['instructions'].split('Serialize fields')[0])
 def test_definitions_do_not_add_gold_or_change_scoring(self):
  c=cases.make('configuration',123);o=cases.observe(c,c['initial'],1,[],[]);req=candidate.diagnosis_request(o);self.assertEqual(req['observation'],o);self.assertNotIn('diagnosis',o);self.assertIn('configuration-only',req['instructions'])
