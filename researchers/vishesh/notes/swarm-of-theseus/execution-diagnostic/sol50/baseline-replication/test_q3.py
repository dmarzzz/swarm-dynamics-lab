import copy,hashlib,io,json,os,sqlite3,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
import admission as a,contract as c,engine,families as f,q3_relay as relay,q3_runner as runner
from development import dev_world

def packet():return {'attempt':a.ATTEMPT,'stage':'Q3','max_calls':108,'assignments':[{'family':family,'world':dev_world(2**44+300+i)} for i,family in enumerate(f.FAMILIES)]}
def oracle(family,phase,p,condition):
 if phase=='learn':return {'note':{'witnesses':f.infer(p['position'],[r['position'] for r in p['roster'] if r['position']!=p['position']],p['history'])}}
 if phase=='select':
  note=copy.deepcopy(p['private_note'])
  if p['current_observations']:note={'witnesses':f.infer(p['position'],[r['position'] for r in p['roster'] if r['position']!=p['position']],p['current_observations'])}
  return {'note':note,'witnesses':note['witnesses']}
 if phase=='attest':return {'reports':[{'owner':r['owner'],'evidence_ids':[v['id'] for v in r['records']]} for r in p['private_inbox']]}
 if phase=='decide':return {'actions':[{'case':x['case'],'action':f.decide(p['private_note']['witnesses'],p['received_records']+p['public_audit_records'],x)} for x in p['cases']]}
 if phase=='question':return {'question':'Which two local authorities should I retain?'}
 if phase=='teach':return {'note':p['private_note'],'explanation':'Preserve the locally learned pair; only current in-scope evidence counts.'}
 if phase=='commit':return {'note':p['inherited_note']}
 raise ValueError('phase')

def evidence(p):
 now=time.time();revision='test-only-revision-not-a-launch';g={'funding_status':'funded','reservation_status':'reserved','attempt':a.ATTEMPT,'stage':'Q3','packet_sha256':a.digest(p),'source_sha256':a.source_hash(),'model_cap_usd':a.MODEL_CAP,'all_in_cap_usd':a.ALL_IN,'prior_exposure_usd':a.PRIOR,'study_cap_usd':'60','portfolio_cap_usd':'200','infrastructure_cap_usd':'1','reservation_amount_usd':a.ALL_IN,'pi_decision_evidence':'TEST-ONLY-NOT-AUTHORITY','portfolio_reservation_id':'PI-FUND-20261004-06','expires_epoch':now+7200}
 r={k:g[k] for k in ('attempt','stage','packet_sha256','source_sha256','model_cap_usd','all_in_cap_usd','prior_exposure_usd','study_cap_usd','portfolio_cap_usd')};r.update(source_commit=revision,model='openai/gpt-6-sol',provider='OpenAI',reasoning_effort='none',max_calls=108,max_input_bytes=6500,max_output_tokens=512,retry_count=0,verified_epoch=now,claim_until_epoch=now+7000,host='fixture',claim_evidence_sha256='fixture',account_evidence_sha256='fixture',historical_ledger_sha256='fixture',plan_url=a.plan_url(revision),plan_sha256=hashlib.sha256((a.ROOT/'Q3-PLAN.md').read_bytes()).hexdigest(),grant_sha256=a.digest(g))
 for k in ('approved_account_verified','exclusive_allocation_verified','worker_idle_verified','host_key_verified','ledger_reconciled','public_page_verified','runtime_verified','provider_capacity_verified','aggregate_publication_authorized'):r[k]=True
 return r,g

class Q3Tests(unittest.TestCase):
 def test_whole_qualification_has_no_hidden_inputs_and_fits(self):
  seen=[]
  def checked(family,phase,p,condition):
   self.assertNotIn('routes',p);self.assertNotIn('gold',p);c.wire(phase,family,p);seen.append((family,phase))
   if phase=='commit':self.assertIsNone(p['private_note']);self.assertEqual(p['current_observations'],[]);self.assertNotIn('history',p);self.assertNotIn('cases',p)
   return oracle(family,phase,p,condition)
  result=engine.qualify(packet(),checked);self.assertTrue(result['passed']);self.assertLessEqual(len(seen),105)
  for r in result['families']:
   self.assertEqual({x['stratum'] for x in r['terminal']['decisions']},{'preserved','updated'});self.assertTrue(r['handover']['retired'].endswith('/g0'));self.assertTrue(r['handover']['successor'].endswith('/g1'))
 def test_failed_founder_stops_all_later_stages_without_reroll(self):
  seen=[]
  def bad(family,phase,p,condition):
   seen.append((family,phase));return {'note':{'witnesses':[]}}
  result=engine.qualify(packet(),bad);self.assertFalse(result['passed']);self.assertEqual(len(seen),6);self.assertEqual(result['unstarted_families'],2)
 def test_unfunded_and_stale_or_changed_authority_rejected(self):
  p=packet();r,g=evidence(p);self.assertTrue(a.validate(r,g,p,r['source_commit']))
  for key,value in [('funding_status','pending'),('reservation_amount_usd','0'),('pi_decision_evidence','')]:
   bad=copy.deepcopy(g);bad[key]=value
   with self.assertRaises(ValueError):a.validate(r,bad,p,r['source_commit'])
  r['verified_epoch']-=901
  with self.assertRaises(ValueError):a.validate(r,g,p,r['source_commit'])
 def test_unfunded_relay_exits_before_credential_or_public_access(self):
  p=packet();r,g=evidence(p);g['funding_status']='pending'
  with tempfile.TemporaryDirectory() as tmp:
   paths=[]
   for name,value in [('r',r),('g',g),('p',p)]:path=Path(tmp)/name;path.write_text(json.dumps(value));paths.append(path)
   with patch.object(a,'public_check') as pub:
    with self.assertRaisesRegex(ValueError,'unfunded'):relay.serve(*paths,Path(tmp)/'missing-ledger',Path(tmp)/'missing-credential',Path(tmp)/'missing-capability')
    pub.assert_not_called()
 def test_relay_requires_exact_sequence_and_request(self):
  p=packet();r,g=evidence(p);body=c.wire('question','release',{'position':'p'});payload={'id':a.ATTEMPT+'-0000','attempt':a.ATTEMPT,'family':'release','phase':'question','packet':{'position':'p'},'request':body,'source_sha256':r['source_sha256'],'frozen_packet_sha256':r['packet_sha256']}
  self.assertEqual(relay.payload_body(payload,r,0),body)
  with self.assertRaises(ValueError):relay.payload_body(payload,r,1)
  payload['request']['model']='different'
  with self.assertRaises(ValueError):relay.payload_body(payload,r,0)
 def test_served_model_provider_finish_and_json(self):
  value={'response':{'model':'openai/gpt-6-sol','provider':'OpenAI','choices':[{'finish_reason':'stop','message':{'content':'{"note":{}}'}}]}}
  self.assertEqual(runner.parse(value),{'note':{}})
  for field,bad in [('model','different'),('provider','different')]:
   x=copy.deepcopy(value);x['response'][field]=bad
   with self.assertRaises(ValueError):runner.parse(x)
  value['response']['choices'][0]['finish_reason']='length'
  with self.assertRaises(ValueError):runner.parse(value)
 def test_native_accounting_settles_known_cost_before_parse_failure(self):
  class Reporter:
   def report(self,*args,**kwargs):return True
  p=packet();r,g=evidence(p)
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'THESEUS_R3_CAPABILITY':'synthetic-test-only'}):
   root=Path(tmp);caller=runner.Calls(root,r,g,root/'ledger.sqlite',Reporter())
   reply={'error':None,'actual_usd':.001,'response':{'model':'wrong'}}
   with patch('urllib.request.urlopen',return_value=io.BytesIO(json.dumps(reply).encode())):
    with self.assertRaises(ValueError):caller('release','question',{'position':'p'},'handover')
   self.assertEqual(float(caller.ledger.exposure()),.001);self.assertEqual(caller.count,1);self.assertTrue((root/(a.ATTEMPT+'-0000-response.json')).exists());caller.ledger.db.close()
if __name__=='__main__':unittest.main()
