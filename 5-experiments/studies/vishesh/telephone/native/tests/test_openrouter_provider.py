import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import request,response
from openrouter_provider import build_request,count_tokens,normalize,generate,ROUTER_MODEL

class OpenRouterTests(unittest.TestCase):
 def setUp(self):
  self.req=request('P',1,[{'id':'x','text':'The vote is provisional.'}])
  self.raw={'id':'gen-fixture','model':ROUTER_MODEL,'provider':'Anthropic',
    'choices':[{'finish_reason':'stop','native_finish_reason':'end_turn','message':{'role':'assistant','content':'The vote is provisional.'}}],
    'usage':{'prompt_tokens':100,'completion_tokens':20,'total_tokens':120,'cost':0.0002}}
 def test_route_and_no_fallback(self):
  body=build_request(self.req)
  self.assertEqual(body['provider']['only'],['anthropic'])
  self.assertFalse(body['provider']['allow_fallbacks'])
  self.assertTrue(body['provider']['require_parameters'])
  self.assertEqual(body['provider']['data_collection'],'deny')
  self.assertFalse(body['reasoning']['enabled'])
  self.assertLess(count_tokens(self.req),8192)
 def test_worker_compatible_and_cost_retained(self):
  normalized=normalize(self.raw)
  self.assertEqual(response(normalized,'P')['token_cost_nano'],200000)
  self.assertEqual(normalized['openrouter']['actual_cost_nano'],200000)
  self.assertEqual(normalized['openrouter_response'],self.raw)
 def test_discount_conservatively_accounted(self):
  self.raw['usage']['cost']=0.0001
  self.assertEqual(normalize(self.raw)['openrouter']['token_rate_cost_nano'],200000)
 def test_one_nanodollar_rounding_tolerance(self):
  self.raw['usage']['cost']='0.00020000000001'
  self.assertEqual(normalize(self.raw)['openrouter']['actual_cost_nano'],200001)
  self.raw['usage']['cost']='0.0002000011'
  with self.assertRaises(ValueError):normalize(self.raw)
 def test_wrong_model_provider_truncation_and_tools_fail(self):
  for mutate in (lambda x:x.update(model='other'),lambda x:x.update(provider='Azure'),
    lambda x:x['choices'][0].update(finish_reason='length'),
    lambda x:x['choices'][0]['message'].update(tool_calls=[{}]),
    lambda x:x['choices'][0]['message'].update(reasoning='hidden')):
   raw=copy.deepcopy(self.raw);mutate(raw)
   with self.assertRaises(ValueError):normalize(raw)
 def test_bad_usage_and_price_fail(self):
  for patch in ({'cost':None},{'cost':'NaN'},{'cost':0.000201},{'cost':True},
    {'prompt_tokens':8193},{'completion_tokens':513},{'total_tokens':119},
    {'prompt_tokens_details':{'cached_tokens':1}}, {'completion_tokens_details':{'reasoning_tokens':1}}, {'is_byok':True}):
   raw=copy.deepcopy(self.raw);raw['usage'].update(patch)
   with self.assertRaises(ValueError):normalize(raw)
 def test_actual_prompt_must_fit_preflight(self):
  with self.assertRaises(ValueError):normalize(self.raw,99)
 def test_no_retry_and_no_generation_for_oversize(self):
  calls=[]
  def fail(body):calls.append(body);raise TimeoutError('fixture')
  with self.assertRaises(TimeoutError):generate(self.req,fail)
  self.assertEqual(len(calls),1)
  self.req['messages'][0]['content']='a'*9000
  with self.assertRaises(ValueError):generate(self.req,fail)
  self.assertEqual(len(calls),1)
 def test_injected_transport_called_once(self):
  calls=[]
  def post(body):calls.append(body);return self.raw
  self.assertEqual(generate(self.req,post)['model'],self.req['model'])
  self.assertEqual(len(calls),1)
if __name__=='__main__':unittest.main()
