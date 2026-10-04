"""Full saved-tape reconstruction, no inference or provider access."""
import collections,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from design import cases,visible,sha,haiku,parse_label,qualification
from native import jev_request,haiku_validate,jev_validate

def audit(root):
 rows=json.loads((root/'observations.json').read_text());m=json.loads((root/'manifest.json').read_text());stage=m['stage'];planned=cases(stage);assert len(rows)==len(planned)
 for r,p in zip(rows,planned):assert all(r[k]==p[k] for k in ('id','family','claim','report','expected'))
 events=[json.loads(x) for x in (root/'calls.jsonl').read_text().splitlines()];starts={e['id']:e for e in events if e['type']=='start'};responses={e['id']:e for e in events if e['type']=='response'};completed={e['id']:e for e in events if e['type']=='completed'}
 assert len(starts)==sum(e['type']=='start' for e in events)
 costs=collections.Counter();tokens=collections.Counter();latency=collections.Counter();records=[];misses=[]
 for i,r in enumerate(rows):
  for variant in ('a','b','jev'):
   model='jev' if variant=='jev' else 'haiku';payload=jev_request(r,i,'C6R2-'+stage) if model=='jev' else haiku(r,0 if variant=='a' else 1)
   h=sha({'attempt':'C6R2-'+stage,'row':r['id'],'variant':variant,'payload':payload});s=starts[h];assert s['payload']==payload and s['row_id']==r['id'] and s['variant']==variant and s['model']==model
   raw=responses[h]['raw'];decoded=jev_validate(raw) if model=='jev' else haiku_validate(raw);assert decoded['label']==r['labels'][variant]==completed[h]['result']['label']
   assert abs(decoded['cost_usd']-completed[h]['result']['cost_usd'])<1e-12
   costs[model]+=decoded['cost_usd'];tokens[model]+=decoded['input_tokens']+decoded['output_tokens'];latency[model]+=responses[h]['seconds']
   record={'case':r['id'],'variant':variant,'truth':r['expected'],'actual':decoded['label'],'claim':r['claim'],'report':r['report'],'raw_answer':raw['answers']['label'] if model=='jev' else raw['choices'][0]['message']['content']}
   records.append(record)
   if decoded['label']!=r['expected']:misses.append(record)
 assert len(starts)==len(responses)==len(completed)==3*len(rows)
 out={'all_payloads_reconstructed':True,'all_raw_labels_reconstructed':True,'all_scores_reconstructed':True,'assigned_cases':len(rows),'completed_cases':sum(r['status']=='completed' for r in rows),'completed_calls':len(completed),'cost_usd':sum(costs.values()),'component_cost_usd':dict(costs),'component_total_tokens':dict(tokens),'component_seconds':dict(latency),'source':m['source_commit'],'miss_count':len(misses),'misses':misses,'qualification':qualification(rows) if stage=='S0' else None,'matched_successes':[next(x for x in records if x['truth']==l and x['actual']==l and x['variant']==v) for l in ('SUPPORT','REFUTE','UNCERTAIN') for v in ('a','b','jev') if any(x['truth']==l and x['actual']==l and x['variant']==v for x in records)]}
 (root/'audit.json').write_text(json.dumps(out,indent=2)+'\n');return {k:v for k,v in out.items() if k not in ('misses','matched_successes')}
if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))
