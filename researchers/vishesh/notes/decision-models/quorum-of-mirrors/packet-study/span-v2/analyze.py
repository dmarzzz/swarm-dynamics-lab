"""Replay raw span selections and software-derived facts without new calls."""
from pathlib import Path
import json,sys,html
from contract import request,digest,score,summarize,normalize,core,decode
out=Path(sys.argv[1]);packet=json.loads(Path(sys.argv[2]).read_text());rows=packet['rows']
records=[json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines()];by={r['id']:r for r in records};assert len(by)==len(records)
reqs={r['id']:r for r in map(json.loads,(out/'requests.jsonl').read_text().splitlines())};audit=[];misses=[]
for assignment,row in zip(packet['manifest']['assignments'],rows):
 rec=by.get(assignment['id']);entry={'assignment':assignment,'case':row,'receipt':rec}
 if rec:
  req=reqs[rec['id']];assert req['sha256']==assignment['request_sha256']==digest(request(row['actor']));assert req['request']==request(row['actor']);entry['request']=req
  if rec['valid']:
   assert rec['parsed']==json.loads(rec['content']);assert rec['decoded']==decode(row['actor'],rec['parsed']);s=score(row,rec['parsed']);assert s==rec['score']
   if not(s['grounded_quotes_valid'] and s['labels_correct'] and s['decision_correct']):misses.append(entry)
  else:misses.append(entry)
 audit.append(entry)
summary=summarize(rows,records);saved=json.loads((out/'summary.json').read_text());assert all(saved[k]==v for k,v in summary.items())
pairs=[]
for root in sorted({r['root'] for r in rows}):
 entries=sorted([e for e in audit if e['case']['root']==root],key=lambda e:e['case']['condition']['copies']);valid=all(e['receipt'] and e['receipt']['valid'] for e in entries)
 p={'root':root,'family':entries[0]['case']['family'],'both_valid':valid,'source_evidence_identical':entries[0]['case']['actor']['sources']==entries[1]['case']['actor']['sources']}
 if valid:
  aa=[normalize(e['case']['actor'],e['receipt']['parsed']) for e in entries];common=set(aa[0]['reports'])&set(aa[1]['reports']);p['common_claims_invariant']=all(core(aa[0]['reports'][i])==core(aa[1]['reports'][i]) for i in common);p['decisions']=[e['receipt']['score']['decision'] for e in entries];p['expected_decisions']=[e['case']['gold']['decision'] for e in entries];p['exact_both']=all(e['receipt']['score']['grounded_quotes_valid'] and e['receipt']['score']['labels_correct'] and e['receipt']['score']['decision_correct'] for e in entries)
 pairs.append(p)
for n,v in [('audit.json',audit),('misses.json',misses),('analysis.json',{'summary':summary,'pairs':pairs,'all_assignment_statuses_checked':len(rows),'native_responses_replayed':len(records),'component_miss_packets':len(misses),'raw_vs_derived':'parsed is native literal selection; decoded is deterministic software output; neither contains model-generated numeric facts'})]:(out/n).write_text(json.dumps(v,indent=2)+'\n')
body='''<!doctype html><meta charset="utf-8"><title>Quorum span repair qualification</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;background:#111827;color:#eee}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1f2937;padding:16px}details{border-top:1px solid #64748b;padding:12px}summary{cursor:pointer}td,th{padding:10px;text-align:left;border-bottom:1px solid #64748b}</style><h1>Quorum SP-02 · Evidence selection</h1><p>40 assigned qualification calls,20 paired authored roots. Native output selects clauses; decoded numeric facts and modes are software output. Plan-only source quotations are retained; code derives unknown status and no observed value. No field reliability or swarm efficacy claim.</p>'''
body+='<pre>'+html.escape(json.dumps(summary,indent=2))+'</pre><table><tr><th>Family / root</th><th>One → three copies</th><th>Common report facts invariant</th></tr>'
for p in pairs:body+='<tr><td>'+html.escape(p['family']+' / '+p['root'][:8])+'</td><td>'+html.escape(' → '.join(p.get('decisions',['NOT STARTED / INVALID'])))+'</td><td>'+str(p.get('common_claims_invariant','MISSING'))+'</td></tr>'
body+='</table>'
for e in audit:
 rec=e['receipt'];status='NOT STARTED' if rec is None else 'INVALID' if not rec['valid'] else 'PASS' if rec['score']['grounded_quotes_valid'] and rec['score']['labels_correct'] and rec['score']['decision_correct'] else 'MISS'
 body+='<details><summary>'+html.escape(e['assignment']['id']+' · '+e['case']['family']+' · copies='+str(e['case']['condition']['copies'])+' · '+status)+'</summary><pre>'+html.escape(json.dumps(e,indent=2))+'</pre></details>'
(out/'traces.html').write_text(body);assert body.count('<details>')==40
print(json.dumps({'native_replayed':len(records),'assigned':40,'miss_packets':len(misses),'summary':summary}))
