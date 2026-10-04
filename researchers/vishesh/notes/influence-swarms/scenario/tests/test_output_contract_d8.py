import copy,json,sys,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import output_contract_d8 as d8
import typed_policy as tp
from candidate_checks import matrix_schema
class OutputContractTests(unittest.TestCase):
 def parents(self):return json.loads((BASE/'reviews/D7-acquisition-packet.json').read_text())['requests']
 def test_both_schemas_delivered_without_observation_changes(self):
  for parent in self.parents():
   item=d8.compile_item(parent);d8.verify_item(item);wire=item['wire_body']
   self.assertEqual(item['request'],parent['request']);self.assertEqual(wire['messages'][1:],parent['wire_body']['messages'][1:])
   self.assertEqual(wire['messages'][0]['content'],parent['request']['instructions']+d8.JSON_ONLY)
   expected=(tp.schema if item['arm'].startswith('typed') else matrix_schema)(item['request']['observation'])
   self.assertEqual(wire['response_format']['json_schema']['schema'],expected)
   self.assertTrue(wire['response_format']['json_schema']['strict']);self.assertLessEqual(len(json.dumps(wire).encode()),d8.MAX_BYTES)
   for k in ('model','provider','temperature','max_tokens','reasoning','stream'):self.assertEqual(wire[k],parent['wire_body'][k])
 def test_missing_contract_or_instruction_rejected(self):
  for parent in self.parents():
   for change in ('schema','instruction','hash'):
    item=d8.compile_item(parent)
    if change=='schema':del item['wire_body']['response_format']
    elif change=='instruction':item['wire_body']['messages'][0]['content']=parent['request']['instructions']
    else:item['wire_sha256']='bad'
    with self.assertRaises(ValueError):d8.verify_item(item)
 def test_markdown_stays_invalid(self):
  with self.assertRaises(ValueError):tp.decode_answer('# Procurement Review\nCHOICE: Birch')

 def test_original_anthropic_schema_survives_translation(self):
  original=json.loads((BASE/'reviews/D6-acquisition-packet.json').read_text())['requests']
  for old,parent in zip(original,self.parents()):
   self.assertEqual(set(old['wire_body']),{'model','system','temperature','max_tokens','messages','output_config'})
   fixed=d8.compile_item(parent)['wire_body']
   self.assertEqual(fixed['response_format']['json_schema']['schema'],old['wire_body']['output_config']['format']['schema'])
