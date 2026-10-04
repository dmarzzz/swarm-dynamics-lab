"""Explicit extraction; comparisons and votes are deterministic, never model labels."""
import hashlib,json
ATTEMPT='QM-PQ-02';MODEL='anthropic/claude-sonnet-4.6';RESERVE=.06
SYSTEM='''Extract facts from authenticated source receipts and bound reports independently. Resolve source facts for the query entity, time and property; ignore plans, old times and other entities, and use explicit corrections over initial entries. Preserve the actual report entity and time, even when different from the query. Normalize mass to grams and running/stopped to 1/0. Negated running means stopped. Unknown observation has value null and status unknown; never guess from a plan. Each report here states one observation. Return the fact and a literal quotation containing the full selected proposition, not irrelevant context. Equivalent wording or units and omitted irrelevant context do not change a fact. Return only JSON; no explanations or hidden reasoning. Code will compare exact facts, not just threshold votes; missing evidence is not contradiction.'''
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def core(f):return {k:f[k] for k in ['entity','time','property','value','status']}
def compare(source,report):
 if source['status']!='observed' or report['status']!='observed' or any(source[k]!=report[k] for k in ['entity','time','property']):return 'NOT_ESTABLISHED'
 return 'SUPPORTED' if source['value']==report['value'] else 'CONTRADICTED'
def vote(f,q):
 if f['status']!='observed':return None
 return f['value']>=q['threshold']
def decision(facts,q):
 vs=[vote(f,q) for f in facts.values()]
 return 'ONE' if vs.count(True)>=2 else 'ZERO' if vs.count(False)>=2 else 'DEFER'
def request(actor):
 obj=lambda p:{'type':'object','properties':p,'required':list(p),'additionalProperties':False}
 fact=obj({'entity':{'type':'string'},'time':{'type':'string'},'property':{'type':'string','enum':['mass_g','running']},'value':{'type':['integer','null']},'status':{'type':'string','enum':['observed','unknown']},'quote':{'type':'string'}})
 schema=obj({kind:obj({r['id']:fact for r in actor[kind]}) for kind in ['sources','reports']})
 return {'model':MODEL,'provider':{'only':['Anthropic'],'allow_fallbacks':False,'require_parameters':True},'temperature':0,'max_tokens':1600,'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(actor,separators=(',',':'))}],'response_format':{'type':'json_schema','json_schema':{'name':'facts','strict':True,'schema':schema}},'usage':{'include':True}}
def bound(req):return len(json.dumps(req,separators=(',',':')).encode())+1024

def score(row,answer):
 a=row['actor'];g=row['gold']
 if not isinstance(answer,dict) or set(answer)!={'sources','reports'}:raise ValueError('output_schema')
 counts={};quotes=True
 for kind in ['sources','reports']:
  if not isinstance(answer[kind],dict) or set(answer[kind])!={r['id'] for r in a[kind]}:raise ValueError('output_schema')
  counts[kind]=0
  for r in a[kind]:
   f=answer[kind][r['id']];gold=g[kind][r['id']]
   if not isinstance(f,dict) or set(f)!={'entity','time','property','value','status','quote'}:raise ValueError('output_schema')
   if any(not isinstance(f[k],str) for k in ['entity','time','property','status','quote']) or f['property'] not in ['running','mass_g'] or f['status'] not in ['observed','unknown']:raise ValueError('output_schema')
   if f['value'] is not None and type(f['value'])!=int:raise ValueError('output_schema')
   if (f['status']=='unknown')!=(f['value'] is None) or not 1<=len(f['quote'])<=500:raise ValueError('output_schema')
   counts[kind]+=core(f)==core(gold)
   quotes=quotes and f['quote'] in r['text'] and gold['quote'].lower() in f['quote'].lower()
 labels={r['id']:compare(answer['sources'][r['source_id']],answer['reports'][r['id']]) for r in a['reports']}
 confusion={};fp=fn=unknown_errors=0
 for rid,target in g['labels'].items():
  pred=labels[rid];key=target+'->'+pred;confusion[key]=confusion.get(key,0)+1
  fp+=target!='CONTRADICTED' and pred=='CONTRADICTED';fn+=target=='CONTRADICTED' and pred!='CONTRADICTED';unknown_errors+=target=='NOT_ESTABLISHED' and pred!=target
 return {'source_facts_correct':counts['sources'],'report_facts_correct':counts['reports'],'reports_total':len(a['reports']),'labels':labels,'labels_correct':labels==g['labels'],'quotes_valid':quotes,'decision':decision(answer['sources'],a['query']),'decision_correct':decision(answer['sources'],a['query'])==g['decision'],'source_votes_correct':sum(vote(answer['sources'][i],a['query'])==vote(f,a['query']) for i,f in g['sources'].items()),'false_contradictions':fp,'missed_contradictions':fn,'unknown_errors':unknown_errors,'confusion':confusion}
def summarize(rows,records):
 good=[r for r in records if r.get('valid')];ss=[r['score'] for r in good]
 out={'assigned':len(rows),'started':len(records),'valid':len(good),'unstarted':len(rows)-len(records),'known_actual_usd':sum(r.get('usage',{}).get('cost',0) for r in records)}
 for k in ['source_facts_correct','report_facts_correct','reports_total','labels_correct','quotes_valid','decision_correct','source_votes_correct','false_contradictions','missed_contradictions','unknown_errors']:out[k]=sum(s[k] for s in ss)
 out['confusion']={}
 for s in ss:
  for k,v in s['confusion'].items():out['confusion'][k]=out['confusion'].get(k,0)+v
 out['qualified']=out['valid']==24 and out['labels_correct']>=23 and out['false_contradictions']==0 and out['missed_contradictions']==0 and out['unknown_errors']==0 and out['source_facts_correct']>=70 and out['decision_correct']>=23 and out['quotes_valid']==24
 return out
