import unittest
from public_plan import validate
class PreflightTests(unittest.TestCase):
 def setUp(self):
  self.e={'id':'test','url':'https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/plan.md','description':'TLDR: compare a treatment against a baseline.'}
  self.md='\n'.join('## '+s+'\nConcrete design details.\n' for s in ('TLDR','Question and prediction','Setup','Protocol','Metrics'))
  self.q='This run compares a treatment with a control using correct completion.'
 def test_complete(self):self.assertEqual(validate(self.e,self.md,self.q)['experiment'],'test')
 def test_no_url(self):
  self.e['url']=None
  with self.assertRaises(ValueError):validate(self.e,self.md,self.q)
 def test_mutable_url(self):
  self.e['url']=self.e['url'].replace('a'*40,'main')
  with self.assertRaises(ValueError):validate(self.e,self.md,self.q)
 def test_missing_tldr(self):
  self.e['description']='An experiment'
  with self.assertRaises(ValueError):validate(self.e,self.md,self.q)
 def test_missing_protocol(self):
  with self.assertRaises(ValueError):validate(self.e,self.md.replace('## Protocol','## Other'),self.q)
 def test_empty_question(self):
  with self.assertRaises(ValueError):validate(self.e,self.md,'')
if __name__=='__main__':unittest.main()
