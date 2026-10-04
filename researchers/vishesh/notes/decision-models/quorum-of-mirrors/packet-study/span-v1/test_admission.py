import unittest,time,socket,copy
from unittest.mock import patch
import runtime
class Admission(unittest.TestCase):
 def config(self):
  now=time.time()
  return {'source_sha256':runtime.hashes(),'owner_directed_qualification':True,'max_calls':40,'max_reserved_usd':1.92,'allocation':{'host':socket.gethostname().split('.')[0],'exclusive':True,'approved_account_verified':True,'merged_claim_verified':True,'workload_verified_clear':True,'checked_at':now,'expires_at':now+600},'deadline':now+600,'infrastructure_total_bound_usd':.2,'cumulative_hours_bound':2}
 def test_source_drift(self):
  c=self.config();c['source_sha256']={}
  with self.assertRaisesRegex(AssertionError,'source_changed'):runtime.preflight(c,{})
 def test_scope_expansion(self):
  c=self.config();c['max_calls']=41
  with self.assertRaisesRegex(AssertionError,'scope'):runtime.preflight(c,{})
 def test_stale_allocation(self):
  c=self.config();c['allocation']['checked_at']-=1000
  with self.assertRaisesRegex(AssertionError,'allocation_expired'):runtime.preflight(c,{})
 def test_wrong_account_or_shared(self):
  for key in ['approved_account_verified','exclusive','workload_verified_clear']:
   c=self.config();c['allocation'][key]=False
   with self.assertRaisesRegex(AssertionError,'allocation'):runtime.preflight(c,{})
 def test_manifest_mismatch(self):
  with self.assertRaisesRegex(AssertionError,'manifest'):runtime.preflight(self.config(),{'manifest':{}})
if __name__=='__main__':unittest.main()
