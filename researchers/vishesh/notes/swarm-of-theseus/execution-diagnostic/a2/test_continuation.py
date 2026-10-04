import json,subprocess,sys,unittest
from pathlib import Path
from design import assignments,execution_request,digest,ROOT,MODEL
from admission import validate,GateError
from test_a2 import receipt
from test_provider_diagnostics import error
from provider_diagnostics import http_failure

class ContinuationTests(unittest.TestCase):
    def test_frozen_actor_input_parity(self):
        code="import sys,json;sys.path.insert(0,sys.argv[1]);from design import assignments,execution_request,digest;print(json.dumps([digest(a['request'] if a['kind']=='learn' else execution_request(a,a['rule'])) for a in assignments()]))"
        old=json.loads(subprocess.check_output([sys.executable,'-c',code,str(ROOT/'a1')],text=True))
        current=[digest(a['request'] if a['kind']=='learn' else execution_request(a,a['rule'])) for a in assignments()]
        self.assertEqual(old,current)
        self.assertTrue(all(a['id'].startswith('A2-') for a in assignments()))
    def test_known_spend_code_and_poisoned_details(self):
        for code in ('enforced_spend_limit_reached','SECRET_MARKER',[],None):
            with error({'error':{'type':'rate_limit_error','details':{'error_code':code,'secret':'SECRET_MARKER'}}}) as response:
                value=http_failure(response,0)
            self.assertEqual(value['provider_error_code'],'enforced_spend_limit_reached' if code=='enforced_spend_limit_reached' else 'unknown')
            self.assertNotIn('SECRET_MARKER',json.dumps(value))
    def test_provider_health_cannot_be_metadata_or_stale(self):
        for field,value in [('model','different'),('route_verified',False),('restriction_resolved',False),('evidence_kind','model_metadata'),('evidence_ref',''),('verified_epoch',0),('last_rejection_epoch',10**12)]:
            r=receipt();r['provider_health'][field]=value
            with self.assertRaises(GateError):validate(r,r['source_commit'],assignments())
    def test_prior_reservation_and_old_authority_rejected(self):
        for field,value in [('prior_unresolved_usd',0),('prior_spend_usd',.8122310437),('authority_allocation_id','theseus-a1-7300-7305-v1'),('attempt','A1')]:
            r=receipt();r[field]=value
            with self.assertRaises(GateError):validate(r,r['source_commit'],assignments())
if __name__=='__main__':unittest.main()
