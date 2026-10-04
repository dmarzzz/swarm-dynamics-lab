import json,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
import contract as c,runner,relay
class ContractTests(unittest.TestCase):
 def test_supported_grammar(self):
  for token,want in [('14.300','14300.00'),('32,000','32000.00'),('12,34','12.34'),('12.34','12.34'),('1.234,50','1234.50'),('1,234.50','1234.50'),('0','0.00')]:self.assertEqual(c.normalize(token),want)
 def test_unsupported_refers(self):
  for token in ('-1','1e3','14.3','1,23,456','Total14.300','1.000.50',None,'1 000','NaN'):self.assertIsNone(c.normalize(token))
 def test_no_automatic_accept(self):
  l={'decision':'accept','token':'14.300','label':'Total'}
  self.assertIsNone(c.decide({'literal':l,'verify':{'verified':False}})['treatment'])
  self.assertEqual(c.decide({'literal':l,'verify':{'verified':True}})['treatment'],'14300.00')
 def test_checker_input_is_literal_not_gold(self):
  p=c.request(b'pixels','verify',{'decision':'accept','token':'14.300','label':'Total'})
  t=p['messages'][1]['content'][0]['text'];self.assertIn('14.300',t);self.assertNotIn('14300.00',t);self.assertNotIn('gold',t)
 def test_corruption_and_arm_order(self):
  p={'decision':'accept','token':'14.300','label':'Total'};self.assertEqual(c.proposed(p,True)['token'],'14.3009')
  self.assertEqual(c.order('E2',0),['direct-a','direct-b','literal','verify']);self.assertEqual(c.order('E2',1),['literal','verify','direct-a','direct-b'])
 def test_schema_bounds(self):
  self.assertIsNone(c.parse('{"verified":"true","evidence":"x"}','verify'))
  self.assertIsNone(c.parse('{"decision":"accept","token":"14300.00","label":""}','literal'))
 def test_invalid_amount_is_retained_and_referred(self):
  v=c.parse('{"decision":"accept","amount":"29.998","evidence":"Total 29.998"}','direct-a')
  self.assertIsNotNone(v);self.assertFalse(c.canonical(v));self.assertIsNone(c.decide({'direct-a':v,'direct-b':v})['baseline'])
 def test_route_accounting(self):
  b={'model':c.MODEL,'provider':'Anthropic','usage':{'prompt_tokens':10,'completion_tokens':20,'cost':.001},'choices':[{'finish_reason':'stop','message':{'content':'{"verified":false,"evidence":"no"}'}}]}
  self.assertIsNone(relay.decode(b,'corrupt')['error']);b['provider']='other';self.assertEqual(relay.decode(b,'corrupt')['error'],'route_mismatch')
class CollectorTests(unittest.TestCase):
 def test_all_assignments_and_first_error(self):
  for fail in (False,True):
   with tempfile.TemporaryDirectory() as t:
    root=Path(t).resolve();inp=root/'inputs';inp.mkdir();(inp/'images').mkdir();(inp/'images/a.png').write_bytes(b'fixture')
    cases=[{'id':str(i),'stage':'Q2','index':i,'image':'a.png','image_sha256':c.sha(inp/'images/a.png'),'gold':'1000.00'} for i in range(4)]
    (inp/'cases.json').write_text(json.dumps(cases));(inp/'specs.json').write_text('{}')
    (root/'INPUT-FREEZE.json').write_text(json.dumps({'cases_sha256':c.sha(inp/'cases.json'),'specs_sha256':c.sha(inp/'specs.json')}))
    a={'source_sha256':'0'*64,'stage':'Q2','owner_authorized':True,'public_page_verified':True,'allocation_verified':True,'budget_verified':True,'verified_at':time.time(),'claim_expires_at':time.time()+3600};(root/'a.json').write_text(json.dumps(a))
    def call(url,cap,identity,p):
     kind=identity.split('-',1)[1]
     parsed={'decision':'accept','token':'1.000','label':'Total'} if kind=='literal' else {'verified':kind=='verify','evidence':'Total 1.000'} if kind in ('verify','corrupt') else {'decision':'accept','amount':'1000.00','evidence':'Total 1.000'}
     return {'parsed':None if fail else parsed,'raw_text':json.dumps(parsed),'usage':None if fail else {'prompt_tokens':10,'completion_tokens':20},'actual_usd':None if fail else .001,'error':'http_429' if fail else None}
    with patch.object(runner,'HERE',root),patch.object(runner,'source_hash',return_value='0'*64):
     r=runner.collect('Q2',inp,root/'out',root/'a.json','cap',1,lambda *a:None,call)
    self.assertEqual(r['started'],1 if fail else 20);self.assertEqual(r['qualification_passed'],not fail);self.assertEqual(r['unstarted'],19 if fail else 0)
    if not fail:self.assertEqual(r['trace_status'],'verified_declared_coverage')
if __name__=='__main__':unittest.main()
