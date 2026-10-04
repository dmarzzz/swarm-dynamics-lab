"""Receipt-paired descriptive analysis and marginal checker value."""
import argparse,json,random,statistics
from pathlib import Path
from contract import ARMS

def interval(values):
 if not values:return None
 rng=random.Random(2026);n=len(values);draws=sorted(sum(rng.choices(values,k=n))/n for _ in range(2000));return [draws[49],draws[1949]]
def analyze(root):
 records=[json.loads(l) for l in (root/'records.jsonl').read_text().splitlines()];rows=json.loads((root/'outcomes.json').read_text());by={(r['id'],r['arm']):r for r in rows};scorable=[r['id'] for r in records if r['gold']['status']=='ok'];result={'independent_unit':'receipt; vendor/layout independence not established','assigned':len(records),'scorable':len(scorable),'pipelines':{},'paired':{},'uncertain_reference_bounds':{},'checker_introduced_errors':[]}
 for tool in 'ABCDE':
  outputs=[r['pipelines'][tool] for r in records];correct=sum(r['gold']['status']=='ok' and r['pipelines'][tool]['candidate']['status']=='ok' and r['pipelines'][tool]['candidate']['value']==r['gold']['value'] for r in records);times=sorted(p['wall_s'] for p in outputs)
  result['pipelines'][tool]={'correct':correct,'scorable':len(scorable),'missing':sum(p['candidate']['status']=='missing' for p in outputs),'ambiguous':sum(p['candidate']['status']=='ambiguous' for p in outputs),'failed':sum(not p['valid'] for p in outputs),'wall_s_total':sum(times),'wall_s_median':statistics.median(times),'wall_s_p90':times[min(len(times)-1,int(.9*len(times)))]}
 for a,b in [('selective-check','agreement'),('selective-check','always-check'),('agreement','confidence')]:
  key=a+' minus '+b;result['paired'][key]={}
  for metric in ['correct','wrong','refer']:
   values=[int(by[i,a][metric])-int(by[i,b][metric]) for i in scorable];result['paired'][key][metric]={'difference':sum(values)/len(values) if values else None,'bootstrap_95':interval(values)}
 for arm in ARMS:
  rs=[r for r in rows if r['arm']==arm];accepted=[r for r in rs if not r['refer']];unknown=sum(not r['scorable'] for r in accepted);wrong=sum(r['wrong'] for r in accepted)
  result['uncertain_reference_bounds'][arm]={'accepted':len(accepted),'unknown_accepted':unknown,'error_rate_bounds':[wrong/len(accepted),(wrong+unknown)/len(accepted)] if accepted else None}
 for i in scorable:
  initial=by[i,'agreement'];after=by[i,'always-check']
  if initial['correct'] and after['wrong']:result['checker_introduced_errors'].append(i)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args();r=analyze(a.run);(a.run/'analysis.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
