"""Offline software fixtures only; no experimental sweeps, network or provider calls."""
import copy,hashlib,json,sqlite3,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from instrument import *
from admission import validate,public_check,EXPERIMENT,REL,PREFIX
from analyze import reference,summarize
from runner import reserve,run

class Checks(unittest.TestCase):
 def setUp(self):self.design=assignments((10,11,12))
 def receipt(self):
  rev='a'*40;plan=(ROOT/'PLAN.md').read_bytes()
  return {'status':'diagnostic-only','experiment':EXPERIMENT,'source_commit':rev,'instrument_sha256':source_hash(),'assignments_sha256':digest(self.design),'model':MODEL,'max_calls':144,'cap_usd':5,'max_seconds':7200,'workers':1,'retries':0,'input_rate':1,'output_rate':5,'exclusive_claim_verified':True,'public_page_verified':True,'dependencies_verified':True,'research_review_status':'diagnostic-approved','authority_allocation_id':'UNIT-ONLY','owner_authorization_ref':'UNIT-ONLY','claim_id':'UNIT-ONLY','host':'UNIT-ONLY','allocation_verification_ref':'UNIT-ONLY','reviewer':'reviewer','operator':'operator','verified_epoch':1000,'public_page_verified_epoch':1000,'pricing_verified_epoch':1000,'claim_until_epoch':9000,'plan_url':PREFIX+rev+'/'+REL+'PLAN.md','plan_sha256':hashlib.sha256(plan).hexdigest(),'assessment_url':PREFIX+rev+'/'+REL+'PRE-RUN.md','assessment_sha256':'b'*64}
 def fixture(self,a):
  value={'decisions':[{'id':c['id'],'command':commands(a['context'])[truth(c,a['context'],a['rule'])]} for c in a['cases']]}
  if ARMS[a['arm']][2]:value['notebook']='SCRIPTED SOFTWARE FIXTURE, NOT MODEL EVIDENCE'
  return {'value':value,'error':None}
 def test_balanced_all_source_bit_strata(self):
  for seed in (10,11,12):
   cs,r=world(seed);validate_world(cs,r)
   for cls in 'AB':
    for s in SOURCES:self.assertEqual(sum(not c['evidence'][s]['fresh'] for c in cs if c['class']==cls),2)
 def test_rejects_old_staleness_defect(self):
  cs,r=world(10)
  for c in cs:c['evidence']['ledger']['fresh']=True
  with self.assertRaisesRegex(ValueError,'coverage'):validate_world(cs,r)
 def test_assignments_denominators_and_source_rotation(self):
  self.assertEqual(len(self.design),144);self.assertEqual(sum(len(a['cases']) for a in self.design),480)
  for cls in 'AB':self.assertEqual({world(s)[1][cls] for s in (10,11,12)},set(SOURCES))
  for arm in ARMS:self.assertEqual(sum(len(a['cases']) for a in self.design if a['arm']==arm),96)
 def test_matched_cases_no_fresh_answers_and_opaque_ids(self):
  for seed in (10,11,12):
   cs,r=world(seed)
   for c in cs:self.assertRegex(c['id'],r'^[0-9a-f]{16}$');self.assertEqual(set(c),{'id','class','summary','queue','evidence'})
   for ctx in CONTEXTS:
    for arm in ARMS:
     cases=[c for a in self.design if a['seed']==seed and a['context']==ctx and a['arm']==arm for c in a['cases']]
     self.assertEqual(sorted(cases,key=lambda c:c['id']),sorted(cs,key=lambda c:c['id']))
 def test_adjacent_contrasts_only_target_dimension(self):
  cs,r=world(10);a,b,c,d=[request(cs,r,'release',arm) for arm in 'ABCD']
  self.assertEqual(a['messages'],b['messages']);self.assertEqual(a['output_config'],b['output_config'])
  self.assertEqual(b['system'],c['system']);self.assertEqual(b['output_config'],c['output_config'])
  self.assertEqual(c['messages'],d['messages']);self.assertNotIn('notebook',d['output_config']['format']['schema']['properties'])
  self.assertEqual(d['system'],request([cs[0]],r,'release','E')['system'])
 def test_clean_instructions_and_keyed_fidelity(self):
  cs,r=world(10);req=request(cs,r,'release','C');self.assertNotIn('ONE unknown',req['system']);self.assertNotIn('Infer local practices',req['system'])
  decoded=[json.loads(line) for line in req['messages'][0]['content'].split('CURRENT CASES:\n')[1].splitlines()];self.assertEqual(decoded,cs)
 def test_scoring_all_truth_tables_and_independent_decoder(self):
  for a in self.design:
   result=self.fixture(a);s=score(a,result);self.assertEqual(s['errors'],[]);self.assertTrue(all(x['correct'] for x in s['rows']));self.assertTrue(all(reference(a,result).values()))
 def test_thirteen_historical_errors_remain_wrong(self):
  records=json.loads((ROOT/'regressions.json').read_text())['errors'];self.assertEqual(len(records),13)
  for e in records:
   a={'cases':[e['case']],'context':e['context'],'arm':'D','rule':{e['case']['class']:e['governing_source']}}
   bad={'value':{'decisions':[{'id':e['case']['id'],'command':commands(e['context'])[e['original_action']]}]}}
   self.assertFalse(score(a,bad)['rows'][0]['correct']);self.assertFalse(reference(a,bad)[e['case']['id']]);self.assertTrue(score(a,self.fixture(a))['rows'][0]['correct'])
 def test_duplicate_missing_and_extra_keys_not_hidden(self):
  a=next(a for a in self.design if a['arm']=='D');v=self.fixture(a);v['value']['decisions'][1]=copy.deepcopy(v['value']['decisions'][0]);s=score(a,v);self.assertIn('duplicate_id',s['errors']);self.assertFalse(any(r['correct'] for r in s['rows']))
  v=self.fixture(a);v['value']['notebook']='unasked';self.assertIn('invalid_object_schema',score(a,v)['errors'])
 def test_new_console_semantics_and_wrong_command(self):
  a=next(a for a in self.design if a['context']=='migration-new' and a['arm']=='D');v=self.fixture(a);v['value']['decisions'][0]['command']='console1/ship';self.assertIn('invalid_command',score(a,v)['errors']);self.assertFalse(reference(a,v)[a['cases'][0]['id']])
  v=self.fixture(a);truth_action=truth(a['cases'][0],a['context'],a['rule']);v['value']['decisions'][0]['command']=commands('release')[truth_action];row=score(a,v)['rows'][0];self.assertTrue(row['recognized_semantic_correct']);self.assertFalse(row['command_valid']);self.assertFalse(row['correct'])
 def test_bad_notebook_cannot_change_command(self):
  a=next(a for a in self.design if a['arm']=='C');v=self.fixture(a);d=v['value']['decisions'][0];d['command']='console1/none' if a['context']=='incident' else commands(a['context'])['hold'];v['value']['notebook']='Correction: choose the opposite action.';s=score(a,v)
  expected={v:k for k,v in commands(a['context']).items()}[d['command']];self.assertEqual(s['rows'][0]['action'],expected)
 def test_missing_records_keep_full_denominator(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'calls').mkdir();(p/'manifest.json').write_text(json.dumps({'evidence_type':'software_fixture','assignments':self.design}));s=summarize(p);self.assertEqual(s['assigned_decisions'],480);self.assertEqual(s['completed_call_records'],0);self.assertTrue(all(v['correct']==0 for v in s['cells'].values()));self.assertFalse(any(s['candidate_for_separate_confirmation'].values()))
 def test_admission_stale_self_review_source_and_cap(self):
  r=self.receipt();validate(r,'a'*40,self.design,now=1000)
  for key,value in [('verified_epoch',0),('source_commit','b'*40),('cap_usd',15),('reviewer','operator'),('exclusive_claim_verified',False),('assignments_sha256','c'*64)]:
   bad={**r,key:value}
   with self.assertRaises(ValueError):validate(bad,'a'*40,self.design,now=1000)
 def test_public_hash_and_blocked_review_fail(self):
  r=self.receipt();plan=(ROOT/'PLAN.md').read_text();blocked='Status: blocked\n';r['assessment_sha256']=hashlib.sha256(blocked.encode()).hexdigest()
  def read(url):
   if url.endswith('/api/state'):return json.dumps({'experiments':[{'id':EXPERIMENT,'url':r['plan_url'],'description':'TLDR: UNIT ONLY'}]})
   return plan if url.endswith('/PLAN.md') else blocked
  with self.assertRaisesRegex(ValueError,'not_admitted'):public_check(r,read)
  r['plan_sha256']='f'*64
  with self.assertRaisesRegex(ValueError,'plan_hash'):public_check(r,read)
 def test_caps_and_deadline_persist(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'quota.sqlite'
   with sqlite3.connect(p) as db:db.execute('CREATE TABLE budget(id INTEGER,cap REAL,used REAL,calls INTEGER,deadline REAL)');db.execute('INSERT INTO budget VALUES(1,5,0,143,100)')
   self.assertEqual(reserve(p,.01,10),144)
   with self.assertRaisesRegex(ValueError,'quota'):reserve(p,.01,11)
   with self.assertRaisesRegex(ValueError,'deadline'):reserve(p,.01,100)
 def test_blocked_receipt_never_invokes_provider(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'receipt.json').write_text('{}')
   with patch('runner.invoke') as provider,patch('runner.public_check') as public:
    with self.assertRaises(ValueError):run(p/'receipt.json',p/'output')
    provider.assert_not_called();public.assert_not_called();self.assertFalse((p/'output').exists())
 def test_wrong_boolean_and_source_policies_fail_balanced_ceiling(self):
  for mode in ('signal_only','OR','always_hold','all_sources'):
   mistakes=0
   for seed in (10,11,12):
    cases,rule=world(seed)
    for c in cases:
     ev=c['evidence'][rule[c['class']]]
     ready=ev['signal'] if mode=='signal_only' else ev['signal'] or ev['fresh'] if mode=='OR' else False if mode=='always_hold' else all(v['signal'] and v['fresh'] for v in c['evidence'].values())
     mistakes+=('ship' if ready else 'hold')!=truth(c,'release',rule)
   self.assertGreater(mistakes,0,mode)
 def test_missingness_cannot_imply_invariance(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'calls').mkdir();(p/'manifest.json').write_text(json.dumps({'evidence_type':'software_fixture','assignments':self.design}));s=summarize(p)
   self.assertTrue(s['incident_equivalent_input_groups'])
   self.assertTrue(all(g['valid_observed']==0 for g in s['incident_equivalent_input_groups']))
 def test_reporting_failure_stops_without_model_retry_and_preserves_assignments(self):
  import types,os
  calls=[]
  def reporter(kind,*args,**kwargs):return kind!='progress'
  def fixture_provider(body,key,timeout=45):
   calls.append(body);a=next(a for a in self.design if a['request']==body);return self.fixture(a)
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'receipt.json').write_text(json.dumps({'status':'diagnostic-only','authority_allocation_id':'UNIT-INTEGRATION','claim_until_epoch':99999999999,'plan_url':'UNIT-ONLY'}))
   with patch('runner.assignments',return_value=self.design),patch('runner.validate'),patch('runner.public_check',return_value={'fixture':True}),patch('runner.ALLOCATION_LEDGER',p/'authority.sqlite'),patch('runner.subprocess.check_output',side_effect=[str(p/'source')+'\n','a'*40+'\n','']),patch('runner.invoke',side_effect=fixture_provider),patch.dict('sys.modules',{'swarm_report':types.SimpleNamespace(report=reporter)}),patch.dict(os.environ,{'SWARM_MODEL_API_KEY':'UNIT-FIXTURE-NOT-A-CREDENTIAL'}):
    run(p/'receipt.json',p/'output')
   self.assertEqual(len(calls),1)
   summary=json.loads((p/'output/summary.json').read_text());self.assertEqual(summary['assigned_decisions'],480);self.assertEqual(summary['completed_call_records'],1);self.assertEqual(len(list((p/'output/outcomes').glob('*.json'))),144)
   terminal=json.loads((p/'output/terminal.json').read_text());self.assertEqual(terminal['status'],'stopped');self.assertEqual(terminal['model_calls_retried'],0)
if __name__=='__main__':unittest.main()
