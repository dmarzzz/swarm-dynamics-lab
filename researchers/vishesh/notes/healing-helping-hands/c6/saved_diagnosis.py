"""Inspect prior native evidence only. No new model calls."""
import collections,json
from pathlib import Path
from design import BASE,sha,parse_label,CONTRACT

def run():
 result={}
 for stage in ('S0','S1'):
  root=BASE/'c5/results'/('C5-'+stage);rows=json.loads((root/'observations.json').read_text());byid={r['id']:r for r in rows}
  events=[json.loads(x) for x in (root/'calls.jsonl').read_text().splitlines()];starts={e['id']:e for e in events if e['type']=='start'}
  matrices={a:{l:dict(collections.Counter(r['labels'][a] for r in rows if r['expected']==l)) for l in ('SUPPORT','REFUTE','UNCERTAIN')} for a in ('a','b')}
  reconstructed=0;stop=collections.Counter();lengths=collections.Counter();examples=[]
  for e in events:
   if e['type']!='completed' or starts[e['id']]['model']!='qwen':continue
   s=starts[e['id']];r=byid[s['row_id']];p=s['payload'];variant=0 if s['variant']=='a' else 1
   assert p==CONTRACT.qwen_payload(r,variant)
   raw=e['result']['raw'];label=parse_label(raw['message']['content']);assert label==r['labels'][s['variant']]
   reconstructed+=1;stop[raw.get('done_reason','not_retained')]+=1;lengths[raw.get('eval_count')]+=1
   if r['expected']=='SUPPORT' and len(examples)<3:examples.append({'case':r['id'],'claim':r['claim'],'report':r['report'],'expected':r['expected'],'actual':label,'raw_content':raw['message']['content']})
  result[stage]={'cases':len(rows),'qwen_calls_reconstructed':reconstructed,'confusion':matrices,'stop_reasons':dict(stop),'output_token_counts':dict(lengths),'examples':examples}
 result['interpretation']={'first_divergence':'raw classification with relevant evidence delivered','ruled_out':['actor payload differs from frozen contract','stored label differs from raw JSON label'], 'not_identified':['model competence','prompt interpretation','constrained decoder interaction','non-thinking runtime behavior'],'native_diagnostic':'prospective C6 D0 2x2 prompt/decoder intervention; no hidden reasoning inferred'}
 return result
if __name__=='__main__':print(json.dumps(run(),indent=2))
