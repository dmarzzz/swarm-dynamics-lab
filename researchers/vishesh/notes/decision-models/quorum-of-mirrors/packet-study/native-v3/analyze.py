"""Saved-data replay only; never calls a model or edits a frozen actor input."""
from pathlib import Path
import sys,json,html,collections
from contract import score,summarize,request,digest,core
out=Path(sys.argv[1]);packet=json.loads(Path(sys.argv[2]).read_text());rows=packet['rows'];records=[json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines()];requests={r['id']:r for r in map(json.loads,(out/'requests.jsonl').read_text().splitlines())};by={r['id']:r for r in records};audit=[];misses=[]
for assignment,row in zip(packet['manifest']['assignments'],rows):
 rec=by.get(assignment['id']);entry={'assignment':assignment,'case':row,'receipt':rec}
 if rec:
  req=requests[assignment['id']];assert req['sha256']==assignment['request_sha256']==digest(request(row['actor']));assert req['request']==request(row['actor'])
  entry['request']=req
  if rec['valid']:
   assert json.loads(rec['content'])==rec['parsed'];s=score(row,rec['parsed']);assert s==rec['score']
   if not s['labels_correct'] or not s['quotes_valid'] or s['source_facts_correct']!=3 or s['report_facts_correct']!=len(row['actor']['reports']) or not s['decision_correct']:misses.append(entry)
 audit.append(entry)
summary=summarize(rows,records);saved=json.loads((out/'summary.json').read_text());assert all(saved[k]==v for k,v in summary.items())
families={}
for r in audit:
 f=r['case']['family'];v=families.setdefault(f,{'assigned':0,'valid':0,'exact_labels':0,'decisions':0});v['assigned']+=1
 if r['receipt'] and r['receipt']['valid']:v['valid']+=1;v['exact_labels']+=r['receipt']['score']['labels_correct'];v['decisions']+=r['receipt']['score']['decision_correct']
paired=[]
for root in sorted({r['root'] for r in rows}):
 pair=[e for e in audit if e['case']['root']==root];valid=all(e['receipt'] and e['receipt']['valid'] for e in pair)
 def normalized(e):
  s=e['receipt']['score'];return {'decision':s['decision'],'labels':sorted(set((r['source_id'],r['text'],s['labels'][r['id']]) for r in e['case']['actor']['reports']))}
 paired.append({'root':root,'both_valid':valid,'invariant':normalized(pair[0])==normalized(pair[1]) if valid else None})
for name,value in [('audit.json',audit),('misses.json',misses),('analysis.json',{'summary':summary,'families':families,'pairs':paired,'roots':12,'mechanisms':6,'all_assigned_replayed':True,'native_miss_packets':len(misses)})]:(out/name).write_text(json.dumps(value,indent=2)+'\n')
body='<!doctype html><meta charset="utf-8"><title>Quorum PQ-03 traces</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;background:#111827;color:#eee}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#1f2937;padding:16px}details{border-top:1px solid #64748b;padding:12px}summary{cursor:pointer}h1{color:#93c5fd}</style><h1>Quorum of Mirrors · PQ-03</h1><p>Native qualification. Twelve authored roots × two copy conditions; no swarm-efficacy claim. Every assigned case is shown. Missing responses are explicit.</p><pre>'+html.escape(json.dumps(summary,indent=2))+'</pre>'
for e in audit:
 rec=e['receipt'];status='NOT STARTED' if rec is None else 'INVALID' if not rec['valid'] else 'PASS' if rec['score']['labels_correct'] and rec['score']['quotes_valid'] else 'MISS'
 body+='<details><summary>'+html.escape(e['assignment']['id']+' · '+e['case']['family']+' · copies='+str(e['case']['condition']['copies'])+' · '+status)+'</summary><pre>'+html.escape(json.dumps(e,indent=2))+'</pre></details>'
(out/'traces.html').write_text(body)
assert body.count('<details>')==24
print(json.dumps({'replayed':len(records),'all_assigned':len(audit),'miss_packets':len(misses),'paired_invariant':sum(p['invariant'] is True for p in paired),'summary':summary}))
