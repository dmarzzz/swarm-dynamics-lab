import unittest
from decimal import Decimal
from contract import *
class Checks(unittest.TestCase):
 def test_budget(self):
  e=envelope();self.assertEqual(e['max_calls'],1594);self.assertLess(Decimal(e['cumulative_upper_bound_usd']),Decimal(50))
 def test_forks(self):
  rows=assignments(['x','y']);self.assertEqual(len(rows),388);self.assertEqual(len({r['id'] for r in rows}),388)
  ids={r['id'] for r in rows}
  self.assertTrue(all(r['parent'] is None or r['parent'] in ids for r in rows))
 def test_missing(self):self.assertEqual(aggregate(['Supported']*53,60)['status'],'incomplete')
 def test_tie_not_unknown(self):self.assertIsNone(aggregate(['Supported']*30+['Refuted']*30,60)['verdict'])
 def test_unknown_is_label(self):self.assertEqual(aggregate(['Not Enough Evidence']*60,60)['verdict'],'Not Enough Evidence')
 def test_no_extra_votes(self):
  with self.assertRaises(ValueError):aggregate(['Supported']*61,60)
 def test_no_gold(self):
  a={'case_id':'x','claim':'c','claim_date':None,'evidence':[],'label':'secret','justification':'secret'}
  self.assertNotIn('label',actor_only(a));self.assertNotIn('justification',actor_only(a))
 def test_quotes(self):
  a={'evidence':[{'evidence_id':'a','answer':'plan only','explanation':''}]};r={'verdict':'Supported','confidence':.5,'citations':[{'evidence_id':'a','field':'answer','quote':'plan only'}],'unresolved':'','justification':''}
  self.assertTrue(validate_answer(r,a))
  r['citations'][0]['quote']='observed'
  with self.assertRaises(ValueError):validate_answer(r,a)
 def test_board(self):
  reports=[{'agent_id':str(i).zfill(2),'answer':{'verdict':'Supported','citations':[{'evidence_id':'a'}]}} for i in range(59)]
  reports.append({'agent_id':'59','answer':{'verdict':'Refuted','citations':[{'evidence_id':'b'}]}})
  b=board(reports);self.assertEqual(len(b['items']),2);self.assertEqual(sum(x['matching_report_count'] for x in b['items']),60);self.assertFalse(b['independence_claim'])
 def test_source_ids_are_not_truth(self):
  a={'evidence':[{'evidence_id':'a','answer':'a false assertion','explanation':''}]};r={'verdict':'Supported','confidence':.9,'citations':[{'evidence_id':'a','field':'answer','quote':'a false assertion'}],'unresolved':'','justification':''}
  self.assertTrue(validate_answer(r,a)) # deliberately accepts literal false text: requires separate entailment scoring
if __name__=='__main__':unittest.main()

class IntakeChecks(unittest.TestCase):
 def test_archive_identity(self):
  from prepare_cases import urlkey
  self.assertEqual(urlkey('https://web.archive.org/web/20200101000000/https://example.org/a'),urlkey('https://example.org/a'))
 def test_no_locator_leak(self):
  from prepare_cases import convert
  row={'label':'Supported','claim':'x','claim_date':None,'questions':[{'question':'q','answers':[{'answer':'a','source_url':'https://example.org/verdict-true','source_medium':'web text'}]}]*3}
  actor,reason=convert(row,0)
  self.assertIsNone(reason);self.assertNotIn('verdict-true',json.dumps(actor));self.assertNotIn('label',actor)
  self.assertEqual(len({e['document_id'] for e in actor['evidence']}),1)
 def test_bad_sources(self):
  from prepare_cases import convert
  row={'label':'Supported','claim':'x','claim_date':None,'questions':[{'question':'q','answers':[{'answer':'a','source_url':'https://google.com/search?q=answer','source_medium':'web text'}]}]*3}
  self.assertEqual(convert(row,0)[1],'placeholder_or_search_source')
  row['questions'][0]['question']='';self.assertEqual(convert(row,0)[1],'empty_question')
