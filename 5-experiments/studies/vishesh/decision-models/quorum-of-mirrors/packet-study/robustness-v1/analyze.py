"""Offline all-assignment replay; stages remain separate, missing is explicit."""
from pathlib import Path
import json,sys,html
from contract import request,digest,score,summarize,normalize,core
out=Path(sys.argv[1]);packet=json.loads(Path(sys.argv[2]).read_text());rows=packet['rows']
records=[json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines()];by={r['id']:r for r in records}
reqs={r['id']:r for r in map(json.loads,(out/'requests.jsonl').read_text().splitlines())};audit=[];misses=[]
assert len(by)==len(records)
for assignment,row in zip(packet['manifest']['assignments'],rows):
 rec=by.get(assignment['id']);entry={'assignment':assignment,'case':row,'receipt':rec}
 if rec:
  req=reqs[rec['id']];assert req['sha256']==assignment['request_sha256']==digest(request(row['actor']));assert req['request']==request(row['actor']);entry['request']=req
  if rec['valid']:
   assert rec['parsed']==json.loads(rec['content']);s=score(row,rec['parsed']);assert rec['score']==s
   if not(s['labels_correct'] and s['grounded_quotes_valid'] and s['decision_correct']):misses.append(entry)
  else:misses.append(entry)
 audit.append(entry)
assert set(by)<=set(a['id'] for a in packet['manifest']['assignments'])
summary=summarize(rows,records)
if (out/'summary.json').exists():
 saved=json.loads((out/'summary.json').read_text())
 # Frozen runtime iterates a set of roots: delta-array order is not stable across processes.
 # Compare their multisets, then reconstruct root-keyed pairs below; preserve raw summary.
 import copy
 left=copy.deepcopy(summary);right={k:copy.deepcopy(saved[k]) for k in summary}
 for stage in ['qualification','evaluation']:
  for key in ['paired_decision_delta','paired_extraction_delta']:
   left['stages'][stage][key].sort();right['stages'][stage][key].sort()
 assert left==right
pairs=[]
for root in sorted({r['root'] for r in rows}):
 entries=sorted([e for e in audit if e['case']['root']==root],key=lambda e:e['case']['condition']['copies']);valid=all(e['receipt'] and e['receipt']['valid'] for e in entries)
 p={'root':root,'stage':entries[0]['case']['stage'],'family':entries[0]['case']['family'],'both_valid':valid,'source_evidence_identical':entries[0]['case']['actor']['sources']==entries[1]['case']['actor']['sources']}
 if valid:
  aa=[normalize(e['case']['actor'],e['receipt']['parsed']) for e in entries];common=set(aa[0]['reports'])&set(aa[1]['reports']);p['common_claims_invariant']=all(core(aa[0]['reports'][i])==core(aa[1]['reports'][i]) for i in common);p['decisions']=[e['receipt']['score']['decision'] for e in entries];p['expected_decisions']=[e['case']['gold']['decision'] for e in entries];p['decisions_correct']=p['decisions']==p['expected_decisions'];p['exact_both']=all(e['receipt']['score']['grounded_quotes_valid'] and e['receipt']['score']['labels_correct'] and e['receipt']['score']['decision_correct'] for e in entries)
 pairs.append(p)
for n,v in [('audit.json',audit),('misses.json',misses),('analysis.json',{'summary':summary,'pairs':pairs,'roots':25,'all_assigned_replayed':True,'component_miss_packets':len(misses)})]:(out/n).write_text(json.dumps(v,indent=2)+'\n')
body='''<!doctype html><meta charset="utf-8"><title>Quorum R1 robustness traces</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;background:#111827;color:#eee}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1f2937;padding:16px}details{border-top:1px solid #64748b;padding:12px}summary{cursor:pointer}td,th{padding:10px;text-align:left;border-bottom:1px solid #64748b}</style><h1>Quorum R1 · Larger robustness screen</h1><p>Five authored families, five qualification roots and twenty evaluation roots. One versus three claim copies; evidence stays fixed. Native engineering test, not field or swarm efficacy.</p>'''
for stage in ['qualification','evaluation']:
 body+='<h2>'+stage.title()+'</h2><pre>'+html.escape(json.dumps(summary['stages'][stage],indent=2))+'</pre><table><tr><th>Family / root</th><th>One → three copies</th><th>Claims invariant</th></tr>'
 for p in pairs:
  if p['stage']==stage:body+='<tr><td>'+html.escape(p['family']+' / '+p['root'][:8])+'</td><td>'+html.escape(' → '.join(p.get('decisions',['NOT STARTED / INVALID'])))+'</td><td>'+str(p.get('common_claims_invariant','MISSING'))+'</td></tr>'
 body+='</table>'
 for e in audit:
  if e['case']['stage']!=stage:continue
  rec=e['receipt'];status='NOT STARTED' if rec is None else 'INVALID' if not rec['valid'] else 'PASS' if rec['score']['grounded_quotes_valid'] and rec['score']['labels_correct'] and rec['score']['decision_correct'] else 'MISS'
  body+='<details><summary>'+html.escape(e['assignment']['id']+' · '+e['case']['family']+' · copies='+str(e['case']['condition']['copies'])+' · '+status)+'</summary><pre>'+html.escape(json.dumps(e,indent=2))+'</pre></details>'
(out/'traces.html').write_text(body);assert body.count('<details>')==50
print(json.dumps({'replayed':len(records),'assigned':50,'miss_packets':len(misses),'summary':summary}))
