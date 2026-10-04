import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from remote import check
class AdmissionTests(unittest.TestCase):
 def setUp(self):
  self.c={'study':'telephone','stage':'A0','host':'test-host','owner_scope_ref':'Telephone owner approval of both scopes, 2026-10-04','cap_nano':5000000000,'authority_ref':'Telephone owner USD5 cumulative direct OpenRouter authorization, 2026-10-04','deadline':1500,'dispatch_authority':'owner-direct-2026-10-04','central_queue_fenced':True,'public_page_verified':True,'allocation':{'approved_account_match':True,'inventory_match':True,'merged_exclusive_claim':True,'workload_idle':True,'checked_at':1000,'expires_at':1800,'claim':'vishesh-telephone','operator':'vishesh/codex-village-fit','infrastructure_reserve_nano':100000000}}
 def test_scope_passes_only_exact_contract(self):self.assertTrue(check(self.c,1000,'test-host'))
 def test_no_host_or_budget_or_scope_substitution(self):
  for k,v in [('host','other'),('cap_nano',10000000000),('stage','V0'),('owner_scope_ref','made-up'),('central_queue_fenced',False),('public_page_verified',False)]:
   c=copy.deepcopy(self.c);c[k]=v
   with self.assertRaises(ValueError):check(c,1000,'test-host')
 def test_allocation_unknown_or_stale_refused(self):
  for k,v in [('approved_account_match',False),('workload_idle',False),('merged_exclusive_claim',False),('checked_at',600),('expires_at',1590),('infrastructure_reserve_nano',500000001)]:
   c=copy.deepcopy(self.c);c['allocation'][k]=v
   with self.assertRaises(ValueError):check(c,1000,'test-host')
 def test_unbounded_or_expired_window_refused(self):
  for v in (1000,100000):
   c=copy.deepcopy(self.c);c['deadline']=v
   with self.assertRaises(ValueError):check(c,1000,'test-host')
if __name__=='__main__':unittest.main()
