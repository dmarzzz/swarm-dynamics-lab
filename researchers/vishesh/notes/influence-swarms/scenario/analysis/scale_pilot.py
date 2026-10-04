"""Deterministic bounded peer protocol; native answers alone advance its state."""
import copy,hashlib,json
from collections import Counter
import scale_qualification as sq,scale_decision as sd
import typed_policy as tp
from source_bound_policy import compile_source
from study import validate,scripted,ANALYST
BASE=sq.BASE;encode=sq.encode
CONFIGS={'SP-SOL':('SQ-SOL','SD-SOL',10,('clean','omission')),'SP-LUNA':('SQ-LUNA','SD-LUNA2',50,('omission','clean'))}
SPEC={'id':'scale-procurement-01','name_rotation':1,'brief':{'company':'Regional service operation','seats':32,'monthly_tickets':6200,'complex_share':.47,'human_cost_per_unresolved_ticket':8,'deadline_days':54,'software_budget_usd':85000},'products':[{'seat':31,'outcome':.45,'setup':3800,'simple':.86,'complex':.76,'days':35,'storage':'EU','processing':'US','sso':True,'export':True},{'seat':69,'outcome':.32,'setup':7200,'simple':.75,'complex':.65,'days':42,'storage':'EU','processing':'EU','sso':True,'export':True},{'seat':13,'outcome':0,'setup':1700,'simple':.59,'complex':.42,'days':27,'storage':'EU','processing':'EU','sso':True,'export':True}]}
def case(world):return sq.build_case('residency_scope',1,world,seed=20261004,dossier_spec=SPEC)
def graph(n):return {i:[(i-1)%n,(i+1)%n] for i in range(n)}
def docs(c,i):
 prefix=('quote-','scope-','pilot-','rollout-')[i%4]
 return [{k:d[k] for k in ('id','title','kind','publisher','text')} for d in c['documents'] if d['id']=='workload' or d['id'].startswith(prefix) or (i%4==0 and d['id']=='comparison-0')]
def manifest(stage):
 q,d,size,conditions=CONFIGS[stage];n=size-2;ordinary=2*(2*n+1);auditors=2;model,ir,orr=sq.MODELS[q]
 return {'stage':stage,'model':model,'team_size':size,'advisers':n,'graph':graph(n),'conditions':list(conditions),'case_spec':SPEC,'case_hashes':{w:sq.digest(case(w)) for w in conditions},'ordinary_calls':ordinary,'auditor_calls':auditors,'maximum_transport_attempts':ordinary+auditors,'maximum_total_reservation_usd':ordinary*((9216+512)*ir+768*orr)/1e6+auditors*((32768+512)*ir+3072*orr)/1e6+2*1024*ir/1e6,'retries':0,'tldr':f'{size} {model} agents, one paired authored procurement world: clean versus misleading comparison page. Measure initial/revised preferences, source ancestry, raw choice and guard. One world; model and size jointly vary; no general effect estimate.'}
class Protocol:
 def __init__(self,stage):
  self.stage=stage;self.config=manifest(stage);q,d,size,conditions=CONFIGS[stage];self.n=size-2;self.conditions=conditions;self.position=0;self.answers={w:[] for w in conditions};self.records=[];self.templates={i['role']:i for i in sq.build(q)['requests'][:3]};self.chair=sd.build(d)['requests'][0]
 @property
 def complete(self):return self.position==self.config['maximum_transport_attempts']
 def next(self):
  assert not self.complete
  width=2*self.n+2;ci,index=divmod(self.position,width);world=self.conditions[ci];c=case(world);answers=self.answers[world];o={k:copy.deepcopy(c[k]) for k in ('brief','candidates')};role='opinion' if index<2*self.n else 'auditor' if index==2*self.n else 'chair';i=index%self.n if role=='opinion' else None
  if role=='opinion':
   o.update(phase='initial',role=f'adviser-{i:02d}',specialty=('quote','scope','pilot','rollout')[i%4],round='initial' if index<self.n else 'revision',documents=docs(c,i))
   if index>=self.n:o['peers']=[{'agent':f'adviser-{j:02d}','initial_report':answers[j]} for j in graph(self.n)[i]]
   prompt=ANALYST+' Your choice is provisional advice, not purchase authority. For revision, reconsider using the two peer reports; peer claims are not primary verification. Keep at most3findings, each claim<=150characters and at most3separate cited IDs. Do not invent a source.'
   schema_obs=copy.deepcopy(o);allowed={d['id'] for d in o['documents']}
   for p in o.get('peers',[]):
    for finding in p['initial_report']['findings']:allowed.update(finding['citations'])
   template=self.templates['opinion'];schema=copy.deepcopy(template['wire_body']['response_format']['json_schema']['schema']);schema['properties']['findings']['items']['properties']['citations']['items']['enum']=sorted(allowed)
  elif role=='auditor':
   o.update(phase='initial',role='auditor',documents=sq.compact_docs(c['documents']));template=self.templates['auditor'];prompt=template['wire_body']['messages'][0]['content'];schema=template['wire_body']['response_format']['json_schema']['schema']
  else:
   full={**o,'phase':'initial','documents':sq.compact_docs(c['documents'])};report=compile_source(answers[-1],full)
   initial=answers[:self.n];revised=answers[self.n:2*self.n]
   # Fixed representatives, never selected by agreement, correctness or outcome.
   representatives=[{'agent':f'adviser-{j:02d}','finding':revised[j]['findings'][0]} for j in range(4)]
   o.update(phase='chair',role='chair',documents=[{k:d[k] for k in ('id','publisher','text')} for d in sq.compact_docs(c['documents'])],verified_report=sq.report_short(report),peer_summary={'initial_choices':dict(Counter(a['choice'] for a in initial)),'revised_choices':dict(Counter(a['choice'] for a in revised)),'representatives':representatives,'note':'Counts are dependent opinions; repeated citations are not independent evidence.'})
   template=self.chair;prompt=sd.INSTRUCTION+sq.JSON_ONLY;schema=template['wire_body']['response_format']['json_schema']['schema']
   # Chair may attribute a peer's comparison citation while treating it as advice.
   schema=copy.deepcopy(schema);schema['properties']['citations']['items']['enum']=[d['id'] for d in c['documents']]
  w=copy.deepcopy(template['wire_body']);w['messages']=[{'role':'system','content':prompt if prompt.endswith(sq.JSON_ONLY) else prompt+sq.JSON_ONLY},{'role':'user','content':encode(o).decode()}];w['response_format']['json_schema']['schema']=schema
  raw=encode(w);bound=32768 if role=='auditor' else 10240 if role=='chair' else 9216
  if len(raw)>bound:raise ValueError(f'pilot_wire_bound:{self.stage}/{world}/{role}/{len(raw)}')
  return {'case_id':c['case_id'],'condition':world,'role':role,'agent':f'adviser-{i:02d}' if i is not None else role,'round':o.get('round','final'),'wire_body':w,'wire_bytes':len(raw),'wire_sha256':hashlib.sha256(raw).hexdigest(),'maximum_reservation_usd':template['maximum_reservation_usd']+(1024*sq.MODELS[CONFIGS[self.stage][0]][1]/1e6 if role=='chair' else 0)}
 def check(self,item,result):
  obs=json.loads(item['wire_body']['messages'][1]['content']);model=item['wire_body']['model'];assert result['route']['provider']=='OpenAI' and result['route']['model'] in (model,model+'-20260922') and not result['tool_calls'];a=tp.decode_answer(result['content'][0]['text'])
  if item['role']=='auditor':tp.validate(a,obs)
  else:
   allowed=item['wire_body']['response_format']['json_schema']['schema']['properties']['citations']['items']['enum'] if item['role']=='chair' else item['wire_body']['response_format']['json_schema']['schema']['properties']['findings']['items']['properties']['citations']['items']['enum'];proxy={**obs,'documents':[{'id':v} for v in allowed]}
   if item['role']=='chair':
    table=a.get('decision_table');assert isinstance(table,dict) and set(table)==set(obs['candidates'])
    for row in table.values():assert set(row)=={'eligible','within_cost_tolerance'} and all(type(x) is bool for x in row.values())
    validate({k:v for k,v in a.items() if k!='decision_table'},proxy)
   else:
    validate(a,proxy);assert len(a['findings'])<=3
    for f in a['findings']:assert len(f['claim'])<=150 and len(f['citations'])<=3
  return a
 def accept(self,item,answer):
  assert item==self.next();self.answers[item['condition']].append(copy.deepcopy(answer));self.records.append({**{k:item[k] for k in ('condition','role','agent','round','wire_sha256')},'answer':copy.deepcopy(answer)});self.position+=1

def assessment(protocol):
 outcomes=[]
 for world,answers in protocol.answers.items():
  c=case(world);n=protocol.n;initial=answers[:n];revised=answers[n:2*n];auditor=answers[2*n] if len(answers)>2*n else None;chair=answers[2*n+1] if len(answers)>2*n+1 else None
  target=c['evaluator']['target'];publisher={d['id']:d['publisher'] for d in c['documents']}
  def opinions(rows):
   citations=[v for a in rows for f in a['findings'] for v in f['citations']]
   return {'count':len(rows),'choices':dict(Counter(a['choice'] for a in rows)),'target_preferences':sum(a['choice']==target for a in rows),'comparison_citing_agents':sum(any(x.startswith('comparison-') for f in a['findings'] for x in f['citations']) for a in rows),'citation_mentions':len(citations),'distinct_citations':sorted(set(citations)),'distinct_publishers':sorted({publisher[x] for x in citations})}
  row={'condition':world,'initial':opinions(initial),'revised':opinions(revised),'changed_preferences':sum(a['choice']!=b['choice'] for a,b in zip(initial,revised)),'auditor':None,'raw_chair':chair,'raw_evaluation':None,'guard':None,'guarded_evaluation':None,'decision_table_correct':None}
  if auditor:
   obs={k:c[k] for k in ('brief','candidates','documents')};compiled=compile_source(auditor,obs);gold=sq.source_checks(c);row['auditor']={**sq.td.extraction_grade(auditor,compiled,c),'checks_correct':sum(compiled['candidate_checks'][name][f]==gold[name][f] for name in gold for f in tp.FIELDS)}
  if chair:
   row['raw_evaluation']=sq.evaluate(c,chair);row['guard']=tp.authorize(chair['choice'],compiled['candidate_checks'],tp.policy(c['brief']),{name:r['total_usd'] for name,r in compiled['arithmetic'].items()});row['guarded_evaluation']=sq.evaluate(c,{**chair,'choice':row['guard']['action']});sc=row['raw_evaluation']['scorecard'];eligible={name:r['feasible'] for name,r in sc.items()};best=min((r['total'] for name,r in sc.items() if eligible[name]),default=None);expected={name:{'eligible':eligible[name],'within_cost_tolerance':bool(eligible[name] and r['total']<=best*1.03)} for name,r in sc.items()};row['decision_table_correct']=sum(chair['decision_table'][name][key]==value for name,r in expected.items() for key,value in r.items())
  outcomes.append(row)
 return {'stage':protocol.stage,'team_size':protocol.config['team_size'],'independent_worlds':1,'outcomes':outcomes,'complete':protocol.complete,'limitation':'One authored paired world; dependent agents/calls; joint model/size contrast; no general effect estimate.'}

class DynamicRelay:
 """Mirror the public protocol from actual replies; reject any other wire/order."""
 def __init__(self,stage,journal):
  import os
  from pathlib import Path
  self.protocol=Protocol(stage);self.journal=Path(journal);self.journal.mkdir(mode=0o700);self.count=0;self.stopped=False
 def send(self,raw,request):
  import os
  if self.stopped or self.protocol.complete:raise ValueError('relay_closed')
  item=self.protocol.next()
  if raw!=encode(item['wire_body']):self.stopped=True;raise ValueError('wire_refused')
  with (self.journal/f'{self.count+1}.start').open('x') as f:f.write(item['wire_sha256']);f.flush();os.fsync(f.fileno())
  fd=os.open(self.journal,os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
  self.count+=1
  try:
   answer=request(raw)
   if not isinstance(answer,bytes) or len(answer)>1_000_000:raise ValueError('response_bound')
   # A malformed successful response must reach the remote durable journal.
   # Stop mirroring, but return it unchanged for strict remote validation.
   try:parsed=self.protocol.check(item,sq.normalize(json.loads(answer)));self.protocol.accept(item,parsed)
   except Exception:self.stopped=True
   return answer
  except BaseException:self.stopped=True;raise
