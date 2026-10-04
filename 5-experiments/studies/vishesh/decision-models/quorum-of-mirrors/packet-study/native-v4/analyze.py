"""Offline full-cohort request/score replay and paired trace view."""
from pathlib import Path
import json,sys,html
from contract import request,digest,score,summarize,normalize,core
out=Path(sys.argv[1]);packet=json.loads(Path(sys.argv[2]).read_text());rows=packet['rows'];records=[json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines()];by={r['id']:r for r in records};reqs={r['id']:r for r in map(json.loads,(out/'requests.jsonl').read_text().splitlines())};audit=[];misses=[]
for assignment,row in zip(packet['manifest']['assignments'],rows):
 rec=by.get(assignment['id']);entry={'assignment':assignment,'case':row,'receipt':rec}
 if rec:
  req=reqs[rec['id']];assert req['sha256']==assignment['request_sha256']==digest(request(row['actor']));assert req['request']==request(row['actor']);entry['request']=req
  if rec['valid']:
   assert rec['parsed']==json.loads(rec['content']);s=score(row,rec['parsed']);assert rec['score']==s
   if not (s['labels_correct'] and s['grounded_quotes_valid'] and s['decision_correct']):misses.append(entry)
 audit.append(entry)
summary=summarize(rows,records);saved=json.loads((out/'summary.json').read_text());assert all(saved[k]==v for k,v in summary.items())
pairs=[]
for root in sorted({r['root'] for r in rows}):
 entries=sorted([e for e in audit if e['case']['root']==root],key=lambda e:not e['case']['condition']['source_observed']);valid=all(e['receipt'] and e['receipt']['valid'] for e in entries)
 p={'root':root,'family':entries[0]['case']['family'],'both_valid':valid,'reports_identical':entries[0]['case']['actor']['reports']==entries[1]['case']['actor']['reports']}
 if valid:
  aa=[normalize(e['case']['actor'],e['receipt']['parsed']) for e in entries];p['report_assertions_invariant']={i:core(f) for i,f in aa[0]['reports'].items()}=={i:core(f) for i,f in aa[1]['reports'].items()};p['decisions']=[e['receipt']['score']['decision'] for e in entries];p['expected_decisions']=[e['case']['gold']['decision'] for e in entries];p['decisions_correct']=p['decisions']==p['expected_decisions'];p['exact_labels_both_correct']=all(e['receipt']['score']['labels_correct'] for e in entries)
 pairs.append(p)
for n,v in [('audit.json',audit),('misses.json',misses),('analysis.json',{'summary':summary,'pairs':pairs,'roots':4,'all_assigned_replayed':True,'component_miss_packets':len(misses)})]:(out/n).write_text(json.dumps(v,indent=2)+'\n')
body='<!doctype html><meta charset="utf-8"><title>Quorum PQ-04 paired traces</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;background:#111827;color:#eee}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1f2937;padding:16px}details{border-top:1px solid #64748b;padding:12px}summary{cursor:pointer}td,th{padding:10px;text-align:left;border-bottom:1px solid #64748b}</style><h1>Quorum PQ-04 · Claims and evidence</h1><p>Four authored paired roots. The reports stay fixed; source evidence changes. Native qualification only, not population accuracy or a swarm study.</p><pre>'+html.escape(json.dumps(summary,indent=2))+'</pre><table><tr><th>Root</th><th>Observed → plan-only decision</th><th>Report assertions preserved</th></tr>'
for p in pairs:body+='<tr><td>'+html.escape(p['family'])+'</td><td>'+html.escape(' → '.join(p.get('decisions',['MISSING'])))+'</td><td>'+str(p.get('report_assertions_invariant','MISSING'))+'</td></tr>'
body+='</table>'
for e in audit:
 rec=e['receipt'];status='NOT STARTED' if rec is None else 'INVALID' if not rec['valid'] else 'PASS' if rec['score']['grounded_quotes_valid'] and rec['score']['labels_correct'] and rec['score']['decision_correct'] else 'MISS'
 body+='<details><summary>'+html.escape(e['assignment']['id']+' · '+e['case']['family']+' · source observed='+str(e['case']['condition']['source_observed'])+' · '+status)+'</summary><pre>'+html.escape(json.dumps(e,indent=2))+'</pre></details>'
(out/'traces.html').write_text(body);assert body.count('<details>')==8
print(json.dumps({'replayed':len(records),'assigned':8,'miss_packets':len(misses),'summary':summary,'pairs':pairs}))
