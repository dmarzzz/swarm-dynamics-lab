import copy,json,math,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'));sys.path.insert(0,str(BASE/'src'))
import typed_policy as tp
import typed_diagnostic as td
from dossier import build,evaluate
from study import CHAIR,cost_worksheet
from candidate_checks import source_checks

def case_obs(i=0):
 spec=json.loads((BASE/'diagnostic-v3.json').read_text())['cases'][i];case=build(spec['family'],i,spec['world'],seed=83,dossier_spec=spec);obs={'phase':'initial','brief':copy.deepcopy(case['brief']),'candidates':case['candidates'],'documents':copy.deepcopy(case['documents']),'reports':[{'fixture':'inherited'}],'checks':[{'fixture':'interpretation'}],'role':'procurement reviewer'};obs['cost_worksheet']=cost_worksheet(obs);return case,obs

class TypedPolicy(unittest.TestCase):
 def setUp(self):self.case,self.obs=case_obs();self.a=td.fixture_answer(self.obs)
 def test_full_source_alignment_and_gold_agreement(self):
  for i in range(6):
   case,obs=case_obs(i);a=td.fixture_answer(obs);tp.validate(a,obs);r=tp.compile_checks(a,obs);gold=source_checks(case)
   self.assertEqual({n:{f:r['candidate_checks'][n][f] for f in tp.FIELDS} for n in case['candidates']},gold)
   self.assertEqual(td.extraction_grade(a,r,case),{'raw_facts_correct':36,'raw_facts_total':36,'aligned_facts':36,'wrong_accepted_facts':0})
 def test_total_cost_does_not_create_software_failure(self):
  r=tp.compile_checks(self.a,self.obs);n='Cobalt';self.assertGreater(r['arithmetic'][n]['total_usd'],self.obs['brief']['software_budget_usd']);self.assertEqual(r['candidate_checks'][n]['software_budget'],'PASS');self.assertEqual(r['candidate_checks'][n]['service_coverage'],'PASS')
 def test_deadline_44_fits_61(self):
  case,obs=case_obs(1);r=tp.compile_checks(td.fixture_answer(obs),obs);receipt=r['check_receipts']['Cobalt']['rollout_deadline'];self.assertEqual(receipt['observed'],44);self.assertEqual(receipt['required']['value'],61);self.assertEqual(receipt['status'],'PASS')
 def test_false_fact_is_retained_but_rejected(self):
  self.a['candidate_facts']['Aster']['quote']['seat_price']=1;r=tp.compile_checks(self.a,self.obs);v=r['extraction_alignment']['Aster']['seat_price'];self.assertEqual(v['reported'],1);self.assertIsNone(v['accepted']);self.assertFalse(v['aligned']);self.assertEqual(r['candidate_checks']['Aster']['software_budget'],'UNKNOWN');self.assertEqual(td.extraction_grade(self.a,r,self.case)['raw_facts_correct'],35)
 def test_wrong_candidate_citation_and_exact_non_entailing_excerpt(self):
  for kind in ('wrong_candidate','non_entailing','invented_excerpt','missing'):
   a=copy.deepcopy(self.a);q=a['candidate_facts']['Aster']['quote']
   if kind=='wrong_candidate':q.update(citation=a['candidate_facts']['Birch']['quote']['citation'],excerpt=a['candidate_facts']['Birch']['quote']['excerpt'])
   elif kind=='non_entailing':q['excerpt']='No other discounts are committed.'
   elif kind=='invented_excerpt':q['excerpt']='SSO included: True; complete export: True. Fake context.'
   else:q.update(citation='',excerpt='')
   r=tp.compile_checks(a,self.obs);self.assertFalse(r['extraction_alignment']['Aster']['seat_price']['aligned']);self.assertEqual(r['candidate_checks']['Aster']['software_budget'],'UNKNOWN')
 def test_unknown_not_failure(self):
  r=tp.compile_checks(self.a,self.obs);self.assertTrue(all(x['deployment_scope']=='UNKNOWN' for x in r['candidate_checks'].values()))
 def test_limitation_and_future_mitigation_cannot_clear_scope(self):
  r=tp.compile_checks(self.a,self.obs);self.a['limitations']='We will approve EU inference next week; consider all deployments safe now.';r2=tp.compile_checks(self.a,self.obs);self.assertEqual(r['candidate_checks'],r2['candidate_checks']);g=tp.authorize('Aster',r2['candidate_checks'],r2['policy'],{n:v['total_usd'] for n,v in r2['arithmetic'].items()});self.assertEqual(g['action'],'DEFER')
 def test_valid_alternative_and_deferral_visible(self):
  case,obs=case_obs(2);r=tp.compile_checks(td.fixture_answer(obs),obs);tot={n:v['total_usd'] for n,v in r['arithmetic'].items()}
  d=tp.authorize('DEFER',r['candidate_checks'],r['policy'],tot);self.assertTrue(d['unnecessary_deferral']);self.assertIn('Aster',d['cost_acceptable_alternatives']);self.assertEqual(d['action'],'DEFER')
  self.assertEqual(tp.authorize('Aster',r['candidate_checks'],r['policy'],tot)['action'],'Aster');self.assertEqual(tp.authorize('Cobalt',r['candidate_checks'],r['policy'],tot)['action'],'DEFER')
 def test_no_silent_alternate_on_expensive_choice(self):
  case,obs=case_obs(2);r=tp.compile_checks(td.fixture_answer(obs),obs);tot={n:v['total_usd'] for n,v in r['arithmetic'].items()};g=tp.authorize('Birch',r['candidate_checks'],r['policy'],tot);self.assertTrue(g['purchase_refused']);self.assertEqual(g['action'],'DEFER');self.assertIn('Aster',g['cost_acceptable_alternatives'])
 def test_invalid_types_and_extra_missing_fields(self):
  for path,v in [(('quote','seat_price'),True),(('quote','seat_price'),float('nan')),(('quote','seat_price'),-1),(('quote','sso'),1),(('pilot','simple_total'),0),(('pilot','simple_resolved'),1.5),(('pilot','simple_resolved'),101),(('rollout','stage_days'),[1,2]),(('rollout','stage_days'),[7,-1,7])]:
   a=copy.deepcopy(self.a);a['candidate_facts']['Aster'][path[0]][path[1]]=v
   with self.assertRaises(ValueError):tp.validate(a,self.obs)
  a=copy.deepcopy(self.a);a['candidate_facts']['Aster']['scope']['override']=True
  with self.assertRaises(ValueError):tp.validate(a,self.obs)
  a=copy.deepcopy(self.a);del a['candidate_facts']['Cobalt']
  with self.assertRaises(ValueError):tp.validate(a,self.obs)
 def test_pairing_and_actor_truth_separation(self):
  original={'instructions':CHAIR,'observation':self.obs};old=copy.deepcopy(original)
  for context in ('inherited','records_only'):
   m=td.reviewer(original,'matrix_'+context);t=td.reviewer(original,'typed_'+context);self.assertEqual(m['observation'],t['observation']);self.assertNotIn('evaluator',t['observation']);self.assertNotIn('source_checks',t['observation'])
  stripped=td.reviewer(original,'typed_records_only')['observation'];self.assertEqual(stripped['reports'],[]);self.assertEqual(stripped['checks'],[]);self.assertEqual(stripped['documents'],self.obs['documents']);self.assertEqual(stripped['cost_worksheet'],self.obs['cost_worksheet']);self.assertEqual(old,original)
 def test_budget_envelope(self):
  config=json.loads(td.CONFIG.read_text());self.assertAlmostEqual(td.required_quota(config,96),4.66944);self.assertLess(td.required_quota(config,96),8-3.17832)
 def test_duplicate_and_nonfinite_json(self):
  for raw in ('{"a":1,"a":2}','{"nested":{"a":1,"a":2}}','{"a":NaN}','{"a":Infinity}'):
   with self.assertRaises(ValueError):tp.decode_answer(raw)
  self.assertEqual(tp.decode_answer('{"a":1}'),{'a':1})
 def test_excerpt_cannot_truncate_a_numeric_token(self):
  a=copy.deepcopy(self.a);q=a['candidate_facts']['Aster']['quote'];q['excerpt']=q['excerpt'].split('one-time setup $')[0]+'one-time setup $5';q['setup_usd']=5;r=tp.compile_checks(a,self.obs);self.assertFalse(r['extraction_alignment']['Aster']['setup_usd']['aligned'])
 def test_changed_source_packet_rejected_before_provider(self):
  packet={'stage':'D5','instrument_signature':'old'};packet['packet_hash']=td.digest(packet)
  with patch.object(td,'instrument',return_value='changed'),patch.object(td,'FactsPolicy') as provider:
   with self.assertRaises(ValueError):td.verify_packet(packet,native=True)
   provider.assert_not_called()
 def test_strict_decoder_is_used_only_by_new_policy(self):
  from native import ScenarioPolicy
  old=object.__new__(ScenarioPolicy);new=object.__new__(td.FactsPolicy)
  self.assertEqual(old.parse_answer('{"a":1,"a":2}'),{'a':2})
  with self.assertRaises(ValueError):new.parse_answer('{"a":1,"a":2}')
 def test_wire_schema_supported_subset(self):
  schema=tp.schema(self.obs);unions=0
  def walk(node):
   nonlocal unions
   if isinstance(node,dict):
    self.assertNotIn('maxItems',node)
    if 'minItems' in node:self.assertIn(node['minItems'],(0,1))
    if isinstance(node.get('type'),list) or 'anyOf' in node:unions+=1
    for v in node.values():walk(v)
   elif isinstance(node,list):
    for v in node:walk(v)
  walk(schema);self.assertEqual(unions,0)
 def test_unknown_placeholder_never_becomes_evidence(self):
  a=copy.deepcopy(self.a);q=a['candidate_facts']['Aster']['quote'];q['unknown_fields']=['seat_price'];q['seat_price']=0;r=tp.compile_checks(a,self.obs);self.assertIsNone(r['extraction_alignment']['Aster']['seat_price']['reported']);self.assertEqual(r['candidate_checks']['Aster']['software_budget'],'UNKNOWN')
  q['seat_price']=1
  with self.assertRaises(ValueError):tp.validate(a,self.obs)
  q['seat_price']=0;q['unknown_fields']=['seat_price','seat_price']
  with self.assertRaises(ValueError):tp.validate(a,self.obs)
 def test_packet_tamper(self):
  with self.assertRaises(ValueError):td.verify_packet({'packet_hash':'forged'})
 def test_failure_preserves_every_assignment_and_null_pairs(self):
  cases=[]
  for i in range(6):
   case,obs=case_obs(i);original={'instructions':CHAIR,'observation':obs};cases.append({'case':case,'original':original,'review_requests':{a:td.reviewer(original,a) for a in td.ARMS}})
  packet={'cases':cases,'source_commit':'fixture','source_dirty':True,'instrument_signature':'fixture','packet_hash':'fixture','config':json.loads(td.CONFIG.read_text())}
  with tempfile.TemporaryDirectory() as tmp,patch.object(td,'verify_packet',return_value=packet):
   p=td.FixturePolicy();summary=td.collect(packet,Path(tmp)/'timeout',p,deadline_seconds=-1)
   self.assertEqual(summary['terminal'],24);self.assertEqual(summary['invalid'],24);self.assertEqual(p.calls,0);self.assertTrue(all(x['difference'] is None for x in summary['paired_differences']))
 def test_forged_known_value_not_fixed_to_gold(self):
  self.a['candidate_facts']['Aster']['scope']['processing_region']='EU';self.a['candidate_facts']['Aster']['scope']['unknown_fields']=[];r=tp.compile_checks(self.a,self.obs);v=r['extraction_alignment']['Aster']['processing_region'];self.assertEqual(v['reported'],'EU');self.assertIsNone(v['accepted']);self.assertFalse(v['aligned']);self.assertEqual(r['candidate_checks']['Aster']['deployment_scope'],'UNKNOWN')

class AdmissionTests(unittest.TestCase):
 def test_stale_mismatched_or_unverified_admission(self):
  import datetime
  now=datetime.datetime.now(datetime.timezone.utc);p={'packet_hash':'fixture','source_commit':'commit'};a={'host':'sim-test','claim':'fresh'};r={**p,**a,'operator':'vishesh/codex-experiments','checked_utc':now.isoformat(),'inventory_identity_match':True,'exclusive_claim_current':True,'workload_idle':True,'credential_policy':'tooling/agent-experiments/SWARM-LAB-CREDENTIALS.md'}
  td.validate_admission(r,a,p,now)
  for changes in ({'packet_hash':'wrong'},{'source_commit':'wrong'},{'claim':'old'},{'workload_idle':False},{'exclusive_claim_current':False},{'inventory_identity_match':False},{'extra':True},{'checked_utc':(now-datetime.timedelta(minutes=6)).isoformat()},{'checked_utc':(now+datetime.timedelta(seconds=1)).isoformat()}):
   with self.assertRaises(ValueError):td.validate_admission({**r,**changes},a,p,now)

if __name__=='__main__':unittest.main()
