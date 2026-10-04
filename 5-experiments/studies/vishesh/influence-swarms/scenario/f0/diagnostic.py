"""F0 pure compiler and result assessor. No credentials, network or launch authority."""
import copy,hashlib,json,sys,math
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'b2'))
import cases as c,instrument as i
SUFFIX=' Return minified JSON with no whitespace outside strings. Use at most 80 characters per conditions string and 100 characters for rationale. Complete every required field and close the JSON object.'
CONDITIONS=('original_original','compact_original','original_relaxed','compact_relaxed')
RESERVE=.004864

def sha(raw):return hashlib.sha256(raw).hexdigest()
def relax(node):
 if isinstance(node,dict):
  if node.get('type')=='string':node.pop('pattern',None);node.pop('maxLength',None)
  for value in node.values():relax(value)
 elif isinstance(node,list):
  for value in node:relax(value)

def compile_packet(contexts):
 rows=[]
 for condition in CONDITIONS:
  for name in ('failed','failed','unaffected'):
   context=contexts[name];wire=copy.deepcopy(context['wire'])
   assert wire['model']==i.MODEL and wire['max_tokens']==3072
   assert wire['provider']=={'only':['openai'],'order':['openai'],'allow_fallbacks':False,'require_parameters':True,'max_price':{'prompt':.1,'completion':.5}}
   if condition.startswith('compact'):wire['messages'][0]['content']+=SUFFIX
   if condition.endswith('relaxed'):relax(wire['response_format']['json_schema']['schema'])
   raw=c.encoded(wire)
   # One token per UTF-8 byte plus512 protocol/schema overhead; include observed
   # cache-write premium (.125/M), not merely advertised .1/M input price.
   ceiling=(len(raw)+512)*.125/1e6+3072*.5/1e6
   assert ceiling<=RESERVE and len(raw)<=32768
   rows.append({'ordinal':len(rows)+1,'condition':condition,'context':name,'case_id':context['case_id'],'parent_wire_sha256':sha(c.encoded(context['wire'])),'wire_sha256':sha(raw),'wire_bytes':len(raw),'cost_bound_usd':ceiling,'wire':wire})
 return rows

def public_manifest(rows):
 return {'version':'F0','calls':12,'reservation_usd':RESERVE,'maximum_usd':12*RESERVE,'model':i.MODEL,'provider':'OpenAI','max_tokens':3072,'rows':[{k:v for k,v in row.items() if k!='wire'} for row in rows]}

def assess(body,case):
 u=body.get('usage',{});cost=u.get('cost')
 if not(all(type(u.get(k)) is int and 0<=u[k]<=10000000 for k in ('prompt_tokens','completion_tokens')) and type(cost) in (int,float) and math.isfinite(cost) and 0<=cost<=RESERVE):raise ValueError('usage_or_cost')
 if body.get('provider')!='OpenAI' or body.get('model') not in (i.MODEL,i.MODEL+'-20260922') or 'error' in body:raise ValueError('route_or_error')
 choices=body.get('choices')
 if type(choices) is not list or len(choices)!=1:raise ValueError('choices')
 x=choices[0];message=x.get('message',{});content=message.get('content');content=content if type(content) is str else ''
 result={'cost_usd':cost,'prompt_tokens':u['prompt_tokens'],'completion_tokens':u['completion_tokens'],'reasoning_tokens':u.get('completion_tokens_details',{}).get('reasoning_tokens'),'finish_reason':x.get('finish_reason'),'characters':len(content),'trailing_whitespace':len(content)-len(content.rstrip()),'local_valid':False,'score':None,'failure':None}
 if x.get('finish_reason')!='stop' or message.get('tool_calls'):result['failure']='incomplete_or_tool';return result
 try:answer=i.decode(content,case,True)
 except (ValueError,TypeError,KeyError):result['failure']='local_structure';return result
 result.update(local_valid=True,score=i.score(case,answer));return result
