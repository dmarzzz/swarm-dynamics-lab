"""Explicit extraction; comparisons and votes are deterministic, never model labels."""
import hashlib,json
ATTEMPT='QM-R1-01';MODEL='anthropic/claude-sonnet-4.6';RESERVE=.048
SYSTEM='''Extract facts from authenticated source receipts and bound reports independently. Resolve source facts for the query entity, time and property; ignore plans, old times and other entities, and use explicit corrections over initial entries. Preserve the actual report entity and time, even when different from the query. Normalize mass to grams and running/stopped to 1/0. Negated running means stopped. Unknown observation has value null and status unknown; never guess from a plan. Reports may assert, hedge, or plan a value. Preserve that value in every mode: ASSERTION, HEDGE or PLAN. For a multi-claim report select the clause matching the query entity/time/property; otherwise preserve the sole claim as written. Include the uncertainty or plan marker in its quotation. Extract what the REPORT SAYS even when its source is unknown or contradictory. Report values must never become unknown because source support is absent. Report claims are separate from source evidence. Return the fact and a literal quotation containing the full selected proposition, not irrelevant context. Equivalent wording or units and omitted irrelevant context do not change a fact. Return sources and reports as arrays, each fact carrying its exact input id exactly once. Return only JSON; no explanations or hidden reasoning. Code will compare exact facts, not just threshold votes; missing evidence is not contradiction.'''
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def core(f):return {k:f[k] for k in ['entity','time','property','value','status']+(['mode'] if 'mode' in f else [])}
def compare(source,report):
 if source['status']!='observed' or report.get('mode')!='ASSERTION' or any(source[k]!=report[k] for k in ['entity','time','property']):return 'NOT_ESTABLISHED'
 return 'SUPPORTED' if source['value']==report['value'] else 'CONTRADICTED'
def vote(f,q):
 if f['status']!='observed':return None
 return f['value']>=q['threshold']
def decision(facts,q):
 vs=[vote(f,q) for f in facts.values()]
 return 'ONE' if vs.count(True)>=2 else 'ZERO' if vs.count(False)>=2 else 'DEFER'
def request(actor):
 obj=lambda p:{'type':'object','properties':p,'required':list(p),'additionalProperties':False}
 fact=obj({'id':{'type':'string'},'entity':{'type':'string'},'time':{'type':'string'},'property':{'type':'string','enum':['mass_g','running']},'value':{'type':['integer','null']},'status':{'type':'string','enum':['observed','unknown']},'quote':{'type':'string'}})
 report_props={k:v for k,v in fact['properties'].items() if k!='status'}
 report_props['value']={'type':'integer'}
 report_props['mode']={'type':'string','enum':['ASSERTION','HEDGE','PLAN']}
 schema=obj({'sources':{'type':'array','items':fact},'reports':{'type':'array','items':obj(report_props)}})
 return {'model':MODEL,'provider':{'only':['Anthropic'],'allow_fallbacks':False,'require_parameters':True},'temperature':0,'max_tokens':1600,'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(actor,separators=(',',':'))}],'response_format':{'type':'json_schema','json_schema':{'name':'facts','strict':True,'schema':schema}},'usage':{'include':True}}
def bound(req):return len(json.dumps(req,separators=(',',':')).encode())+1024

def normalize(actor,answer):
 if not isinstance(answer,dict) or set(answer)!={'sources','reports'}:raise ValueError('output_schema')
 result={}
 for kind in ['sources','reports']:
  items=answer[kind]
  if not isinstance(items,list) or any(not isinstance(f,dict) or not isinstance(f.get('id'),str) for f in items):raise ValueError('output_schema')
  ids=[f['id'] for f in items]
  if len(ids)!=len(set(ids)) or set(ids)!={r['id'] for r in actor[kind]}:raise ValueError('output_ids')
  if kind=='reports' and any(set(f)!={'id','entity','time','property','value','quote','mode'} or type(f['value'])!=int for f in items):raise ValueError('report_claim_schema')
  result[kind]={f['id']:({k:v for k,v in f.items() if k!='id'}|({'status':'observed'} if kind=='reports' else {})) for f in items}
 return result

def score(row,answer):
 answer=normalize(row['actor'],answer)
 a=row['actor'];g=row['gold']
 if not isinstance(answer,dict) or set(answer)!={'sources','reports'}:raise ValueError('output_schema')
 counts={};quotes=True
 for kind in ['sources','reports']:
  if not isinstance(answer[kind],dict) or set(answer[kind])!={r['id'] for r in a[kind]}:raise ValueError('output_schema')
  counts[kind]=0
  for r in a[kind]:
   f=answer[kind][r['id']];gold=g[kind][r['id']]
   if not isinstance(f,dict) or set(f)!=({'entity','time','property','value','status','quote'}|({'mode'} if kind=='reports' else set())):raise ValueError('output_schema')
   if any(not isinstance(f[k],str) for k in ['entity','time','property','status','quote']) or f['property'] not in ['running','mass_g'] or f['status'] not in ['observed','unknown']:raise ValueError('output_schema')
   if f['value'] is not None and type(f['value'])!=int:raise ValueError('output_schema')
   if (f['status']=='unknown')!=(f['value'] is None) or not 1<=len(f['quote'])<=500:raise ValueError('output_schema')
   if kind=='reports' and f['mode'] not in ['ASSERTION','HEDGE','PLAN']:raise ValueError('report_mode')
   counts[kind]+=core(f)==core(gold)
   quotes=quotes and f['quote'] in r['text'] and gold['quote'].lower() in f['quote'].lower()
 labels={r['id']:compare(answer['sources'][r['source_id']],answer['reports'][r['id']]) for r in a['reports']}
 confusion={};fp=fn=unknown_errors=0
 for rid,target in g['labels'].items():
  pred=labels[rid];key=target+'->'+pred;confusion[key]=confusion.get(key,0)+1
  fp+=target!='CONTRADICTED' and pred=='CONTRADICTED';fn+=target=='CONTRADICTED' and pred!='CONTRADICTED';unknown_errors+=target=='NOT_ESTABLISHED' and pred!=target
 return {'source_facts_correct':counts['sources'],'report_facts_correct':counts['reports'],'reports_total':len(a['reports']),'labels':labels,'labels_correct':labels==g['labels'],'quotes_valid':quotes,'grounded_quotes_valid':quotes and counts['sources']==3 and counts['reports']==len(a['reports']),'decision':decision(answer['sources'],a['query']),'decision_correct':decision(answer['sources'],a['query'])==g['decision'],'source_votes_correct':sum(vote(answer['sources'][i],a['query'])==vote(f,a['query']) for i,f in g['sources'].items()),'false_contradictions':fp,'missed_contradictions':fn,'unknown_errors':unknown_errors,'confusion':confusion}
def summarize_stage(rows,records):
 by={r['case_id']:r for r in records};good=[by[r['id']] for r in rows if r['id'] in by and by[r['id']].get('valid')];ss=[r['score'] for r in good]
 out={'assigned':len(rows),'started':sum(r['id'] in by for r in rows),'valid':len(good),'unstarted':sum(r['id'] not in by for r in rows)}
 for k in ['source_facts_correct','report_facts_correct','reports_total','labels_correct','quotes_valid','grounded_quotes_valid','decision_correct','source_votes_correct','false_contradictions','missed_contradictions','unknown_errors']:out[k]=sum(s[k] for s in ss)
 out['confusion']={}
 for s in ss:
  for k,v in s['confusion'].items():out['confusion'][k]=out['confusion'].get(k,0)+v
 out.update(roots=len({r['root'] for r in rows}),roots_exact=0,paired_reports_invariant=0,paired_decision_delta=[],paired_extraction_delta=[])
 def exact(r):return r.get('valid') and r['score']['grounded_quotes_valid'] and r['score']['labels_correct'] and r['score']['decision_correct']
 for root in {r['root'] for r in rows}:
  pair=sorted([r for r in rows if r['root']==root],key=lambda r:r['condition']['copies'])
  if len(pair)!=2 or not all(r['id'] in by and by[r['id']].get('valid') for r in pair):continue
  rec=[by[r['id']] for r in pair];answers=[normalize(r['actor'],v['parsed']) for r,v in zip(pair,rec)]
  common=set(answers[0]['reports'])&set(answers[1]['reports'])
  out['paired_reports_invariant']+=all(core(answers[0]['reports'][i])==core(answers[1]['reports'][i]) for i in common)
  out['roots_exact']+=all(exact(r) for r in rec)
  out['paired_decision_delta'].append(int(rec[1]['score']['decision_correct'])-int(rec[0]['score']['decision_correct']))
  out['paired_extraction_delta'].append(int(exact(rec[1]))-int(exact(rec[0])))
 out['all_exact']=out['valid']==len(rows) and out['roots_exact']==out['roots'] and out['paired_reports_invariant']==out['roots']
 return out

def summarize(rows,records):
 stages={stage:summarize_stage([r for r in rows if r['stage']==stage],records) for stage in ['qualification','evaluation']}
 q,e=stages['qualification'],stages['evaluation']
 return {'assigned':len(rows),'started':len(records),'valid':sum(bool(r.get('valid')) for r in records),'unstarted':len(rows)-len(records),'known_actual_usd':sum(r.get('usage',{}).get('cost',0) for r in records),'stages':stages,'qualified':q['assigned']==10 and q['all_exact'],'evaluation_accepted':e['valid']==40 and e['roots_exact']>=19 and e['decision_correct']>=39 and e['confusion'].get('NOT_ESTABLISHED->SUPPORTED',0)==0 and e['confusion'].get('SUPPORTED->CONTRADICTED',0)==0}
