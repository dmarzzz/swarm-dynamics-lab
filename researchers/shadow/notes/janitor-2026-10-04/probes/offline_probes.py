import sys,importlib.util,pathlib,json,tempfile,threading,concurrent.futures,io,urllib.error
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[5]
DIR=ROOT/'researchers/shadow/notes/capture-memory-mix/src';sys.path.insert(0,str(DIR));import model
results={}
class FakeResponse:
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self,*a):return json.dumps({'choices':[{'message':{'content':'amber'}}],'model':'other/model','usage':{'cost':.001}}).encode()
p=model.HTTPPolicy.__new__(model.HTTPPolicy)
p.model='test/model';p.T=1;p.mode='sample';p.provider_order=None;p.in_rate=.5;p.out_rate=1;p.cap=1;p.max_calls=1;p.calls=0;p.reserved=0;p.spent_session=0;p.base='https://example.invalid';p.key='SYNTHETIC';p.retries=2;p.timeout=1
with tempfile.TemporaryDirectory() as tmp:
 p.ledger=model.Ledger(pathlib.Path(tmp)/'ledger.json')
 with patch.object(model.urllib.request,'urlopen',return_value=FakeResponse()):
  r=p._request('test')
 results['wrong_returned_model_accepted']=r['model']!='test/model'
 p.calls=0;p.reserved=0
 e=urllib.error.HTTPError('https://example.invalid',503,'synthetic',{},io.BytesIO(b'synthetic'))
 with patch.object(model.urllib.request,'urlopen',side_effect=e) as mock,patch.object(model.time,'sleep'):
  try:p._request('test')
  except model.ModelFailure:pass
  results['retry_dispatch_count']=mock.call_count;results['retry_budget_count']=p.calls
 p.ledger.add('test/model',-.5,0)
 results['negative_cost_accepted']=p.ledger.spent()<0
spec=importlib.util.spec_from_file_location('batches',ROOT/'scripts/batches.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
results['talk_issue_uses_blog']='new blog' in b.issue_body('synthetic','talk','llm-agent-swarms',[])
results['web_issue_targets_talks']='library/talks/' in b.issue_body('synthetic','web','llm-agent-swarms',[])
spec=importlib.util.spec_from_file_location('lab',ROOT/'scripts/lab.py');lab=importlib.util.module_from_spec(spec);sys.modules['lab']=lab;spec.loader.exec_module(lab)
def fakegit(*args,**kwargs):
 class R:returncode=0;stdout='';stderr=''
 return R()
class Crash:
 returncode=1;stdout='';stderr='Traceback synthetic'
with patch.object(lab,'git',side_effect=fakegit),patch.object(lab.subprocess,'run',return_value=Crash()):results['tree_errors_on_checker_crash']=sorted(lab.tree_errors('HEAD'))
print(json.dumps(results,indent=2))
