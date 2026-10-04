"""Each deliberate defect must make its focused regression test fail."""
import io,json,re,unittest
from unittest.mock import patch
import contract as c
from test_contract import ContractTests

def run():
 original_grade=c.grade;original_actor=c.actor;original_policy=c.run_policy
 def bad_grade(r,g):return original_grade(r,g)|{'correct':True}
 def bad_actor(r):return original_actor(r)|{'gold':r['gold']}
 def bad_policy(a,checker,arm):return original_policy(a,checker,'always-check' if arm=='selective-check' else arm)
 mutants=[('subtotal_is_total','EXCLUDE',re.compile('NEVERMATCH'),'test_reject_other_fields'),('strip_anything_into_number','amount',lambda s:re.sub(r'\D','',s) if isinstance(s,str) else None,'test_reject_unsafe'),('abstention_is_correct','grade',bad_grade,'test_abstention_not_accuracy'),('leak_reference','actor',bad_actor,'test_actor_whitelist'),('ignore_stop','run_policy',bad_policy,'test_selective_stop'),('single_source_is_consensus','consensus',lambda xs:next(iter(xs.values()))['value'],'test_agreement_requires_distinct_sources')]
 rows=[]
 for name,attribute,replacement,test in mutants:
  with patch.object(c,attribute,replacement):
   result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.TestSuite([ContractTests(test)]))
  rows.append({'mutant':name,'test':test,'killed':not result.wasSuccessful()})
 assert all(r['killed'] for r in rows),'surviving mutant'
 return {'mutants':rows,'killed':len(rows),'survived':0}
if __name__=='__main__':print(json.dumps(run(),indent=2))
