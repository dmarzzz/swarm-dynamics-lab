import copy,sys,unittest,tempfile,sqlite3,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from budget import Budget
from p30_budget import amend
from common import digest
class P30BudgetTests(unittest.TestCase):
 def test_amendment_preserves_uncertain_rows_once_and_rejects_faults(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'budget.sqlite';now=time.time();b=Budget(p,'old','sim-vishesh',1500000000,288,now+100)
   for i in range(79):b.reserve(str(i),'fixture',10000);b.settle(str(i),100 if i%2 else None)
   rows=b.db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall();old=b.db.execute('SELECT hash,host,cap,calls,deadline FROM authority WHERE id=1').fetchone();b.close()
   a=dict(study='poietic-agents',stage='P30',owner_approved=True,reference='OFFLINE',api_cap_usd=9.25,infrastructure_cap_usd=.75,total_cumulative_cap_usd=10,physical_call_cap=6535,deadline=now+10000)
   packet=dict(attempt='P30-01',authorization=a,qualification=dict(attempt='Q30-02',passed=True,summary_sha256='fixture',contract_sha256='fixture'),allocation=dict(host='sim-vishesh',exclusive=True,approved_account_verified=True,checked_at=now,expires_at=now+12000),workers_stopped=True,source_commit='fixture',plan_sha256='fixture',prior_authority=list(old),prior_charges_sha256=digest(rows))
   for section,key,value in [('authorization','total_cumulative_cap_usd',11),('authorization','deadline',now+10801),('qualification','passed',False),('allocation','exclusive',False),('allocation','checked_at',now-301)]:
    bad=copy.deepcopy(packet);bad[section][key]=value
    with self.subTest(key=key),self.assertRaises(ValueError):amend(p,bad,now)
   bad=copy.deepcopy(packet);bad['prior_charges_sha256']='wrong'
   with self.assertRaises(ValueError):amend(p,bad,now)
   out=amend(p,packet,now);self.assertEqual(out['preserved_calls'],79)
   with self.assertRaises(ValueError):amend(p,packet,now)
   c=sqlite3.connect(p);self.assertEqual(c.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall(),rows);self.assertEqual(c.execute('SELECT COUNT(*) FROM p30_amendments').fetchone()[0],1);c.close()
if __name__=='__main__':unittest.main()
