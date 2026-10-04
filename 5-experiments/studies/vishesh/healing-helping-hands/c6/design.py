"""Frozen C6 actor contracts and offline analysis. No network or credentials."""
import copy, hashlib, importlib.util, json, random, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
COHORT='C6R2'
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C5=load('c6_previous_scenarios',BASE/'c5/scenarios.py')
CONTRACT=load('c6_previous_contract',BASE/'c5/contract.py')
def sha(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def visible(row):return {k:row[k] for k in ('claim','report')}
def diagnostic_cases():
 rows=json.loads((BASE/'c5/results/C5-S0/observations.json').read_text());selected=[]
 for label in LABELS:
  for form in range(4):
   selected.append(next(r for r in sorted(rows,key=lambda x:x['id']) if r['expected']==label and r['family']==f'qualification-{form}'))
 return [{**visible(r),'id':'C6-D0-'+str(i),'expected':r['expected'],'family':r['family'],'parent_id':r['id']} for i,r in enumerate(selected)]
def cases(stage):
 if stage=='D0':return diagnostic_cases()
 if stage not in ('S0','S1'):raise ValueError('stage')
 conditions=[(f,l,j) for f in (range(4) if stage=='S0' else C5.FAMILIES) for l in LABELS for j in range(5 if stage=='S0' else 12)]
 random.Random('C6R2-identity-'+stage).shuffle(conditions);out=[]
 for i,(family,label,j) in enumerate(conditions):
  r=C5.fixture(label,family,'C6R2-'+stage) if stage=='S0' else C5.main_fixture(family,label,77+j,'C6R2-'+stage,i)
  if stage=='S0':
   old=C5.opaque_name('C6R2-'+stage,family);new=C5.opaque_name('C6R2-'+stage,i+100)
   for k in ('claim','report'):r[k]=r[k].replace(old,new)
  r.update(id='C6R2-'+stage+'-'+str(i),status='planned',labels={});out.append(r)
 random.Random('C6R2-call-order-'+stage).shuffle(out);return out
SIMPLE='Read the report. Is the claim established? SUPPORT means measured accuracy is higher than baseline. REFUTE means it is equal or lower. UNCERTAIN means the needed measurement is absent. Return only JSON: {"label":"SUPPORT"}, {"label":"REFUTE"}, or {"label":"UNCERTAIN"}.\n'
def qwen(row,prompt,decoder):
 if prompt not in ('original','simple') or decoder not in ('schema','text'):raise ValueError('condition')
 p=CONTRACT.qwen_payload(row,0)
 if prompt=='simple':p['messages'][0]['content']=SIMPLE+'CLAIM: '+row['claim']+'\nREPORT: '+row['report']
 if decoder=='text':p.pop('format')
 return p
HMODEL='anthropic/claude-haiku-4.5';HSNAPSHOT='anthropic/claude-4.5-haiku-20251001'
def haiku(row,variant):
 if variant not in (0,1):raise ValueError('variant')
 order=LABELS[variant:]+LABELS[:variant]
 text='Classify REPORT relative to CLAIM. SUPPORT: measured accuracy improved over baseline. REFUTE: measured accuracy was worse or unchanged. UNCERTAIN: the named comparison is not established. Use only REPORT. Return only a JSON object with one key, label. Allowed labels: '+', '.join(order)+'.\nCLAIM: '+row['claim']+'\nREPORT: '+row['report']
 return {'model':HMODEL,'provider':{'only':['anthropic'],'allow_fallbacks':False,'require_parameters':True},'messages':[{'role':'user','content':text}],'temperature':0,'max_tokens':64,'response_format':{'type':'json_schema','json_schema':{'name':'classification','strict':True,'schema':{'type':'object','properties':{'label':{'type':'string','enum':list(order)}},'required':['label'],'additionalProperties':False}}},'reasoning':{'enabled':False},'stream':False}
def parse_label(text):
 text=text.strip()
 if text.startswith('```json\n') and text.endswith('\n```'):text=text[8:-4].strip()
 x=json.loads(text)
 if not isinstance(x,dict) or set(x)!={'label'} or x['label'] not in LABELS:raise ValueError('invalid_label')
 return x['label']
def qualification(rows):
 correct={a:{l:sum(r.get('labels',{}).get(a)==l for r in rows if r['expected']==l) for l in LABELS} for a in ('a','b','jev')}
 complete=len(rows)==60 and len({r['id'] for r in rows})==60 and all(sum(r['expected']==l for r in rows)==20 for l in LABELS) and all(r.get('status')=='completed' and all(r.get('labels',{}).get(a) in LABELS for a in correct) for r in rows)
 return {'qualified':complete and all(sum(c.values())>=51 and min(c.values())>=14 for c in correct.values()),'complete':complete,'correct':correct}
def score(rows):
 result=CONTRACT.score(rows)
 result['model_role_note']='The historical qwen score key denotes Haiku A in C6; no Qwen call is part of S0/S1.'
 return result
def conservative_haiku_cost(payload):
 # Byte bound is deliberately conservative, plus protocol overhead. Never forecast as a cap.
 return (len(json.dumps(payload,separators=(',',':')).encode())+512)*1e-6+64*5e-6
