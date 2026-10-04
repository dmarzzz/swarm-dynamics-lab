import copy,json,random,sqlite3,tempfile,unittest
from pathlib import Path
import families as f,contract as c
from development import dev_world
class FamilyChecks(unittest.TestCase):
 def setUp(self):self.w=dev_world(8401);self.owner=self.w['members'][0]
 def test_independent_declared_labels_and_boundary_contrasts(self):
  for family in f.FAMILIES:
   for kind in f.KINDS:
    for variant in f.VARIANTS[family] if kind=='invalid' else [None]:
     x=f.example(self.w,family,self.owner,kind,variant);rs=x['private_records']+x['public_records'];pair=self.w['routes'][self.owner]
     self.assertEqual(f.decide(pair,rs,x['target']),f.LABELS[kind])
   x=f.example(self.w,family,self.owner,'allow');r=x['private_records'][1];t=x['target']
   if family=='failover':
    for at,valid in [(7,False),(8,True),(10,True),(11,False)]:r['observed_at']=at;self.assertEqual(f.eligible(r,t),valid)
   if family=='delegation':
    r['starts']=10;r['ends']=11;self.assertTrue(f.eligible(r,t));r['ends']=10;self.assertFalse(f.eligible(r,t));r['ends']=11;r['revoked_at']=11;self.assertTrue(f.eligible(r,t));r['revoked_at']=10;self.assertFalse(f.eligible(r,t))
 def test_unique_policy_inference_no_pair_answer_field(self):
  for family in f.FAMILIES:
   h=f.history(self.w,family,self.owner);peers=[p for p in self.w['members'] if p!=self.owner]
   self.assertEqual(set(f.infer(self.owner,peers,h)),set(self.w['routes'][self.owner]));self.assertNotIn('authorized_witnesses',json.dumps(h))
   with self.assertRaises(ValueError):f.infer(self.owner,peers,h[:1])
 def test_nuisance_actually_delivered_and_ignored_by_policy(self):
  for family in f.FAMILIES:
   cases=f.panel(self.w,family,self.owner);pair=self.w['routes'][self.owner];delivered=[]
   for peer in pair:
    inbox=f.witness_inbox(cases,peer);ids=[r['id'] for r in inbox[0]['records']];delivered+=f.hydrate(peer,inbox,{'reports':[{'owner':self.owner,'evidence_ids':ids}]})
   p=f.decision_packet(self.owner,{'witnesses':pair},cases,delivered);outsider=next(x for x in cases if x['kind']=='irrelevant_veto');self.assertIn(outsider['public_records'][0],p['public_audit_records'])
   self.assertEqual(f.decide(pair,p['received_records']+p['public_audit_records'],outsider['target']),'allow')
   changed=copy.deepcopy(outsider);changed['public_records'][0]['source']=pair[0];self.assertEqual(f.decide(pair,changed['private_records']+changed['public_records'],changed['target']),'defer')
 def test_witness_ids_do_not_hydrate_unavailable_or_forged_evidence(self):
  cases=f.panel(self.w,'release',self.owner);peer=self.w['routes'][self.owner][0];inbox=f.witness_inbox(cases,peer);key=inbox[0]['records'][0]['id']
  for ids in [[key,key],['unavailable']]:
   with self.assertRaises(ValueError):f.hydrate(peer,inbox,{'reports':[{'owner':self.owner,'evidence_ids':ids}]})
  self.assertEqual(f.hydrate(peer,inbox,{'reports':[]}),[])
  with self.assertRaises(ValueError):f.hydrate('impostor',inbox,{'reports':[{'owner':self.owner,'evidence_ids':[key]}]})
 def test_wrong_owner_metadata_is_delivered_to_addressed_recipient(self):
  case=f.example(self.w,'release',self.owner,'invalid','owner');peer=self.w['routes'][self.owner][1];inbox=f.witness_inbox([case],peer)
  returned=f.hydrate(peer,inbox,{'reports':[{'owner':self.owner,'evidence_ids':[r['id'] for r in inbox[0]['records']]}]})
  self.assertEqual(returned[0]['owner'],'other');self.assertEqual(inbox[0]['owner'],self.owner)
 def test_scoring_order_and_denominators(self):
  cases=f.panel(self.w,'release',self.owner);rows=[{'case':x['target']['case'],'action':x['gold']} for x in cases];rows.reverse();self.assertEqual(f.score({'actions':rows},cases)['correct'],6)
  with self.assertRaises(ValueError):f.score({'actions':rows[:-1]},cases)
  rows[-1]=rows[0]
  with self.assertRaises(ValueError):f.score({'actions':rows},cases)
 def test_wrong_peer_has_observations_without_authority_oracle(self):
  cases=f.panel(self.w,'release',self.owner);pair=self.w['routes'][self.owner];outsider=next(p for p in self.w['members'] if p!=self.owner and p not in pair)
  self.assertEqual(len(f.witness_inbox(cases,outsider)[0]['records']),6)
 def test_lossless_source_record_delivery(self):
  cases=f.panel(self.w,'delegation',self.owner);peer=self.w['routes'][self.owner][1];inbox=f.witness_inbox(cases,peer);records=inbox[0]['records'];out=f.hydrate(peer,inbox,{'reports':[{'owner':self.owner,'evidence_ids':[r['id'] for r in records]}]});self.assertEqual(records,out);out[0]['value']=not out[0]['value'];self.assertNotEqual(records,out)
class RuntimeChecks(unittest.TestCase):
 def test_source_isolation_and_wrong_lesson_preserved(self):
  message={'note':{'witnesses':['wrong-a','wrong-b']},'explanation':'Wrong but bounded.'};p=c.successor('p',['p'],'interactive',{'witnesses':[]},message);self.assertIsNone(p['private_note']);self.assertEqual(p['predecessor_message'],message);self.assertNotIn('history',p)
  with self.assertRaises(ValueError):c.successor('p',['p'],'broken',{},message)
  message['explanation']='x'*1300
  with self.assertRaises(ValueError):c.teacher_delivery(message)
 def test_wire_and_stage_budget_reservation_survive_unknown(self):
  body=c.wire('decide','release',{'cases':[]})
  with tempfile.TemporaryDirectory() as tmp:
   ledger=c.StageLedger(Path(tmp)/'ledger.sqlite','Q3');ledger.reserve('one',body);ledger.settle('one',None);self.assertEqual(ledger.exposure(),c.PER_CALL)
   with self.assertRaises(sqlite3.IntegrityError):ledger.reserve('one',body)
   for j in range(107):ledger.reserve(str(j),body)
   with self.assertRaises(ValueError):ledger.reserve('overflow',body)
   ledger.db.close()
  huge=copy.deepcopy(body);huge['messages'][1]['content']='x'*6501
  with self.assertRaises(ValueError):c.validate_wire(huge)
  body['provider']['allow_fallbacks']=True
  with self.assertRaises(ValueError):c.validate_wire(body)
if __name__=='__main__':unittest.main()
