import hashlib,json
ATTEMPT='QM-PQ-01';MODEL='anthropic/claude-sonnet-4.6';RESERVE=.03
SYSTEM='Read the query and authenticated source receipts first. Resolve the relevant entity, time, negation, units and explicit correction before counting each source once. Then compare each report with its bound source. Copies never add sources. Return only the requested JSON. Quote one literal relevant source substring for each receipt. Do not provide hidden reasoning or any additional text.'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def request(actor):
 ids=[r['id'] for r in actor['receipts']];reports=[r['id'] for r in actor['reports']]
 obj=lambda properties:{'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}
 schema=obj({'decision':{'type':'string','enum':['ONE','ZERO','DEFER']},'source_votes':obj({i:{'type':'boolean'} for i in ids}),
 'source_quotes':obj({i:{'type':'string'} for i in ids}),'distorted_report_ids':{'type':'array','items':{'type':'string','enum':reports}}})
 return {'model':MODEL,'provider':{'only':['Anthropic'],'allow_fallbacks':False,'require_parameters':True},'temperature':0,'max_tokens':768,
 'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(actor,separators=(',',':'))}],
 'response_format':{'type':'json_schema','json_schema':{'name':'packet_decision','strict':True,'schema':schema}},'usage':{'include':True}}
def bound(req):return len(json.dumps(req,separators=(',',':')).encode())+1024

def score(row,answer):
 actor=row['actor'];gold=row['gold'];ids={r['id'] for r in actor['receipts']};rids={r['id'] for r in actor['reports']}
 if not isinstance(answer,dict) or set(answer)!={'decision','source_votes','source_quotes','distorted_report_ids'}:raise ValueError('output_schema')
 if answer['decision'] not in ['ONE','ZERO','DEFER']:raise ValueError('output_schema')
 if not isinstance(answer['source_votes'],dict) or set(answer['source_votes'])!=ids or any(type(v)!=bool for v in answer['source_votes'].values()):raise ValueError('output_schema')
 quotes=answer['source_quotes']
 if not isinstance(quotes,dict) or set(quotes)!=ids or any(not isinstance(v,str) or not 1<=len(v)<=250 for v in quotes.values()):raise ValueError('output_schema')
 bad=answer['distorted_report_ids']
 if not isinstance(bad,list) or any(not isinstance(x,str) for x in bad) or len(bad)!=len(set(bad)) or not set(bad)<=rids:raise ValueError('output_schema')
 correct_set={i for i,faithful in gold['report_fidelity'].items() if not faithful}
 return {'decision_correct':answer['decision']==gold['decision'],'source_votes_correct':sum(answer['source_votes'][i]==v for i,v in gold['source_votes'].items()),
 'distortions_correct':set(bad)==correct_set,'quotes_valid':all(quotes[r['id']] in r['text'] for r in actor['receipts']),
 'clean':row['condition']=={'copies':1,'inverted':False},'decision':answer['decision']}

def summarize(rows,records):
 good=[r for r in records if r.get('valid')];scores=[r['score'] for r in good];clean=[s for s in scores if s['clean']]
 totals={'assigned':len(rows),'started':len(records),'valid':len(good),'unstarted':len(rows)-len(records),'decision_correct':sum(s['decision_correct'] for s in scores),
 'source_votes_correct':sum(s['source_votes_correct'] for s in scores),'distortions_correct':sum(s['distortions_correct'] for s in scores),'quotes_valid':sum(s['quotes_valid'] for s in scores),
 'clean_correct':sum(s['decision_correct'] and s['source_votes_correct']==3 for s in clean),
 'known_actual_usd':sum(r.get('usage',{}).get('cost',0) for r in records)}
 totals['qualified']=totals['valid']==24 and totals['clean_correct']==6 and totals['decision_correct']>=23 and totals['source_votes_correct']>=70 and totals['distortions_correct']>=23 and totals['quotes_valid']==24
 return totals
