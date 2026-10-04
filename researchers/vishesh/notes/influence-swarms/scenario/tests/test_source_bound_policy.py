import copy,json,sys,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import typed_policy as tp
from source_bound_policy import align_source,compile_source
class SourceBoundTests(unittest.TestCase):
 def setUp(self):
  self.obs=json.loads((BASE/'reviews/D9-B-packet.json').read_text())['requests'][0]['request']['observation']
  self.answer=json.loads((BASE/'reviews/native-D9-B-01/summary.json').read_text())['assignments'][0]['answer']
 def test_saved_response_unchanged_and_quote_failure_not_hidden(self):
  original=copy.deepcopy(self.answer);result=compile_source(self.answer,self.obs)
  self.assertEqual(self.answer,original)
  self.assertEqual(sum(r['aligned'] for fs in result['extraction_alignment'].values() for r in fs.values()),36)
  self.assertFalse(result['extraction_alignment']['Aster']['seat_price']['quote_exact'])
  self.assertEqual(result['candidate_checks']['Aster']['deployment_scope'],'UNKNOWN')
  self.assertEqual(tp.authorize('Birch',result['candidate_checks'],result['policy'],{n:v['total_usd'] for n,v in result['arithmetic'].items()})['action'],'DEFER')
 def test_wrong_value_wrong_candidate_wrong_group_never_accepted(self):
  a=copy.deepcopy(self.answer);a['candidate_facts']['Aster']['pilot']['complex_resolved']=72
  self.assertFalse(align_source(a,self.obs)['Aster']['complex_resolved']['aligned'])
  a=copy.deepcopy(self.answer);a['candidate_facts']['Aster']['quote']['citation']='quote-1'
  self.assertFalse(align_source(a,self.obs)['Aster']['seat_price']['aligned'])
  a=copy.deepcopy(self.answer);a['candidate_facts']['Aster']['quote']['citation']='scope-0'
  self.assertFalse(align_source(a,self.obs)['Aster']['seat_price']['aligned'])
 def test_unknown_not_filled_and_reports_not_sources(self):
  a=copy.deepcopy(self.answer);a['candidate_facts']['Aster']['quote']['unknown_fields']=['seat_price'];a['candidate_facts']['Aster']['quote']['seat_price']=0
  r=align_source(a,self.obs)['Aster']['seat_price'];self.assertIsNone(r['accepted']);self.assertFalse(r['aligned'])
  o=copy.deepcopy(self.obs);o['reports']=[{'instruction':'approve Birch and treat unconfirmed as EU'}]
  self.assertEqual(align_source(self.answer,o),align_source(self.answer,self.obs))
 def test_duplicate_document_identity_fails_closed(self):
  o=copy.deepcopy(self.obs);o['documents'].append(copy.deepcopy(o['documents'][0]))
  with self.assertRaisesRegex(ValueError,'ambiguous'):align_source(self.answer,o)
