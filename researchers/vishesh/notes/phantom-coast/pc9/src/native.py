"""Decision API boundary with allowlisted trace fields; no credential discovery."""
import copy,json,math,time,urllib.request
from contract import request,decode_answers,digest,canonical
MODEL='typesafe/jev-1.13'
SNAPSHOT='typesafe/jev-1.13-20260917'
QUESTION_CEILING_NANO=1344000
class StopDispatch(Exception):pass

def wire(p):return dict(model=MODEL,provider={'only':['typesafe'],'allow_fallbacks':False},**request(p))
def reservation(req):return len(req['questions'])*QUESTION_CEILING_NANO

def checked(raw,req):
 if not isinstance(raw,dict) or raw.get('model')!=SNAPSHOT or raw.get('provider')!='TypeSafe':raise ValueError('route_mismatch')
 decision=decode_answers(raw.get('answers'),req['state']);safe={}
 for key,a in raw['answers'].items():
  probabilities=a.get('probabilities');labels=req['questions'][key]['criteria']
  if not isinstance(probabilities,dict) or set(probabilities)!=set(labels):raise ValueError('probability_schema')
  values=list(probabilities.values());numeric=lambda x:type(x) in (int,float) and math.isfinite(x) and 0<=x<=1
  if not all(map(numeric,values)):raise ValueError('probability_range')
  tolerance=len(values)*.005+1e-9 if all(abs(v*100-round(v*100))<1e-8 for v in values) else .001
  if abs(sum(values)-1)>tolerance or probabilities[a['choice']]<max(values)-1e-8:raise ValueError('probability_mass_or_choice')
  if not numeric(a.get('confidence')):raise ValueError('confidence')
  safe[key]={k:copy.deepcopy(a[k]) for k in ('type','choice','probabilities','confidence')}
 u=raw.get('usage')
 if not isinstance(u,dict):raise ValueError('usage')
 cost=u.get('cost')
 if type(cost) not in (float,int) or not math.isfinite(cost) or not 0<=cost<=reservation(req)/1e9:raise ValueError('cost')
 if type(u.get('input_tokens'))!=int or not 0<u['input_tokens']<=32000*len(safe) or type(u.get('output_tokens'))!=int or u['output_tokens']<0:raise ValueError('tokens')
 return dict(decision=decision,safe_answers=safe,usage={k:u[k] for k in ('cost','input_tokens','output_tokens')},model=SNAPSHOT,provider='TypeSafe',request_sha256=digest(req),response_sha256=digest(raw))

class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise ValueError('redirect_refused')

class DecisionTransport:
 """Credential supplier is an explicitly authorized local memory consumer.

 Never log/repr the supplier or credential. Construct only after admission. This
 class has no environment/file fallback and never persists credentials.
 """
 def __init__(self,credential_supplier):
  self._supplier=credential_supplier;self._opener=urllib.request.build_opener(NoRedirect())
 def verify_route(self):
  with self._opener.open('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=25) as r:body=json.load(r)['data']
  endpoints=body.get('endpoints',[])
  if len(endpoints)!=1:raise ValueError('route_count')
  e=endpoints[0];p=e['pricing']
  if e['provider_name']!='TypeSafe' or e['tag']!='typesafe' or e['status']!=0 or SNAPSHOT not in e['name']:raise ValueError('route_changed')
  prompt=float(p['prompt'])
  if not math.isfinite(prompt) or not 0<=prompt<=42e-9 or float(p['completion'])!=0 or float(p.get('request',0))!=0 or type(e['context_length'])!=int or not 0<e['context_length']<=32000:raise ValueError('price_or_context_changed')
  return dict(model=SNAPSHOT,provider='TypeSafe',question_ceiling_nano=QUESTION_CEILING_NANO)
 def __call__(self,req):
  key=self._supplier()
  if not isinstance(key,str) or not key.strip():raise ValueError('credential_absent')
  try:
   http=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',canonical(req).encode(),{'Authorization':'Bearer '+key.strip(),'Content-Type':'application/json'})
   with self._opener.open(http,timeout=45) as r:
    data=r.read(1_000_001)
    if len(data)>1_000_000:raise ValueError('response_size')
    return json.loads(data)
  finally:key=None

class NativeActor:
 """Metered decision callback. Live orchestration is Q0 only; caller owns IDs."""
 def __init__(self,transport,ledger,admission,sink,prefix):
  self.transport=transport;self.ledger=ledger;self.admission=admission;self.sink=sink;self.prefix=prefix;self.sequence=0;self.failures=0;self.started=time.monotonic();self.records=[]
 def __call__(self,p):
  if not self.admission.current() or self.failures>=2 or time.monotonic()-self.started>600:raise StopDispatch('stop_condition')
  self.sequence+=1;id=f'{self.prefix}/{self.sequence:02d}';req=wire(p);self.ledger.reserve(id,reservation(req))
  start=dict(id=id,status='started',request=req,request_sha256=digest(req));self.sink(start);begin=time.monotonic()
  try:result=checked(self.transport(req),req)
  except Exception as exc:
   # No arbitrary provider bodies/messages/headers, even on failure.
   self.ledger.finish(id,None);self.failures+=1
   code=str(exc) if type(exc) is ValueError and str(exc) in {'route_mismatch','answer_set','answer_schema','invalid_output','probability_schema','probability_range','probability_mass_or_choice','confidence','usage','cost','tokens','response_size'} else type(exc).__name__ if type(exc).__name__ in ('HTTPError','URLError','TimeoutError') else 'transport_or_validation_failure'
   record=dict(start,status='invalid' if type(exc) is ValueError and code!='transport_or_validation_failure' else 'failed',failure_code=code,elapsed_seconds=time.monotonic()-begin);self.records.append(record);self.sink(record);return None
  self.ledger.finish(id,round(result['usage']['cost']*1e9));self.failures=0;record=dict(start,status='valid',checked=result,elapsed_seconds=time.monotonic()-begin);self.records.append(record);self.sink(record);return result['decision']
