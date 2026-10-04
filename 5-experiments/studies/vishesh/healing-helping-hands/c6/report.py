"""Saved C6 results only; measured-label inspector and actual cost accounting."""
import argparse,collections,html,json
from pathlib import Path
from design import LABELS,qualification,score

def report(root):
 rows=json.loads((root/'observations.json').read_text());m=json.loads((root/'manifest.json').read_text());stage=m['stage'];events=[json.loads(s) for s in (root/'calls.jsonl').read_text().splitlines()];starts={e['id']:e for e in events if e['type']=='start'};completed=[e for e in events if e['type']=='completed']
 costs=collections.defaultdict(dict)
 for e in completed:
  s=starts[e['id']];costs[s['row_id']][s['variant']]=e['result']['cost_usd']
 result={'stage':stage,'assigned':len(rows),'completed_cases':sum(r.get('status')=='completed' for r in rows),'assigned_calls':48 if stage=='D0' else 3*len(rows),'started_calls':len(starts),'completed_calls':len(completed),'actual_cost_usd':sum(sum(v.values()) for v in costs.values()),'independence':'12 authored wording/family blocks; nested cells; finite synthetic evidence'}
 if stage=='D0':
  result['conditions']={}
  for condition in ('original/schema','original/text','simple/schema','simple/text'):
   correct={l:sum(r.get('labels',{}).get(condition)==l for r in rows if r['expected']==l) for l in LABELS}
   result['conditions'][condition]={'correct':correct,'restored_competence':min(correct.values())>=3,'confusion':{l:dict(collections.Counter(r.get('labels',{}).get(condition) or 'MISSING' for r in rows if r['expected']==l)) for l in LABELS}}
 else:
  result['qualification']=qualification(rows) if stage=='S0' else None
  result['policies']=score(rows)
  if result['completed_cases']==len(rows):
   policy_cost={'haiku_a':sum(c['a'] for c in costs.values()),'always_jev':sum(c['jev'] for c in costs.values()),'agreement_routing':sum(costs[r['id']]['a']+costs[r['id']]['b']+(costs[r['id']]['jev'] if r['labels']['a']!=r['labels']['b'] else 0) for r in rows)}
   result['derived_policy_cost_usd']=policy_cost;result['cost_advantage']=policy_cost['agreement_routing']<policy_cost['always_jev'];result['useful_descriptive_result']=result['policies']['useful_descriptive_result'] and result['cost_advantage']
 result_path=root/'review-summary.json';result_path.write_text(json.dumps(result,indent=2)+'\n')
 columns=('original/schema','original/text','simple/schema','simple/text') if stage=='D0' else ('a','b','jev')
 table=''.join('<tr><td>'+html.escape(r['id'])+'</td><td>'+html.escape(r['expected'])+'</td>'+''.join('<td class="'+('good' if r.get('labels',{}).get(k)==r['expected'] else 'bad')+'">'+html.escape(r.get('labels',{}).get(k) or 'MISSING')+'</td>' for k in columns)+'<td><details><summary>Evidence</summary>'+html.escape(r['claim'])+'<p>'+html.escape(r['report'])+'</p></details></td></tr>' for r in rows)
 page='<!doctype html><meta charset="utf-8"><title>Healing C6 '+stage+'</title><style>body{font:16px system-ui;background:#101725;color:#eef2ff;margin:36px}table{border-collapse:collapse;width:100%}td,th{padding:12px;border-bottom:1px solid #394459;text-align:left}.good{color:#65dfb0}.bad{color:#ffad9f}summary{cursor:pointer}pre{white-space:pre-wrap}</style><h1>Healing Helping Hands · C6 '+stage+'</h1><p>Recorded cases, in execution order. Synthetic authored families; no population or 200-agent claim.</p><pre>'+html.escape(json.dumps({k:v for k,v in result.items() if k not in ('policies','conditions')},indent=2))+'</pre><table><tr><th>Case</th><th>Truth</th>'+''.join('<th>'+x+'</th>' for x in columns)+'<th>Actor evidence</th></tr>'+table+'</table>'
 (root/'inspector.html').write_text(page);return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();print(json.dumps(report(a.root)))
