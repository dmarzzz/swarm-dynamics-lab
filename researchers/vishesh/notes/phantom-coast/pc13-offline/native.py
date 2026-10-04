"""PC11 exact route, bounded request and safe response contract. No credential lookup."""
import json,math,re
from decimal import Decimal,ROUND_CEILING
from packet import compact as canonical,request as packet_request
MODEL='openai/gpt-6-sol'
RESERVE=4480000
MAX_BYTES=1536

def request(p):
 b=packet_request(p)
 if len(canonical(b).encode())>MAX_BYTES:raise ValueError('input_bound')
 return b

def validate_decision(d,p):
 if not isinstance(d,dict) or set(d)!={'p'} or type(d['p']) not in (int,float) or not math.isfinite(d['p']) or not 0<=d['p']<=1:raise ValueError('output_schema')
 return d

def unique(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate_json_key')
  d[k]=v
 return d

def decode(r,p):
 if not isinstance(r,dict):raise ValueError('response_schema')
 if not re.fullmatch(r'(?:openai/)?gpt-6-sol(?:-\d{4}-\d{2}-\d{2})?',str(r.get('model'))):raise ValueError('served_model')
 if r.get('provider')!='OpenAI':raise ValueError('served_provider')
 usage=r.get('usage',{});cost=usage.get('cost')
 if type(cost) not in (int,float) or not math.isfinite(cost) or cost<0:raise ValueError('missing_cost')
 actual=int((Decimal(str(cost))*10**9).to_integral_value(rounding=ROUND_CEILING))
 if actual>RESERVE:raise ValueError('cost_bound')
 for k,cap in [('prompt_tokens',MAX_BYTES+128),('completion_tokens',32)]:
  if type(usage.get(k))!=int or not 0<=usage[k]<=cap:raise ValueError('token_bound')
 if usage.get('completion_tokens_details',{}).get('reasoning_tokens',0)!=0:raise ValueError('unexpected_reasoning')
 cs=r.get('choices',[])
 if len(cs)!=1:raise ValueError('choice_count')
 choice=cs[0];msg=choice.get('message',{})
 if choice.get('finish_reason')!='stop' or msg.get('refusal'):raise ValueError('nonterminal_or_refusal')
 decision=validate_decision(json.loads(msg['content'],object_pairs_hook=unique),p)
 safe=dict(model=r['model'],provider=r['provider'],usage={k:usage[k] for k in ('prompt_tokens','completion_tokens','cost')},content=msg['content'],finish_reason=choice['finish_reason'])
 return decision,actual,safe
