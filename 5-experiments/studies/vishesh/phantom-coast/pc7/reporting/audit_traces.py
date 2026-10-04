"""Audit retained experimental records, never operator transcripts or credential files."""
import sys,json,hashlib,gzip,html,statistics
from pathlib import Path
B=Path(__file__).resolve().parents[1];original=Path(sys.argv[1]);out=B/'results';sys.path.insert(0,str(B.parent/'pc5/src'))
from design import schedule,grade
from contract import packet,_world
from wire import request,digest
bundle=[];hashes={};stages={}
for stage in ('Q0','S1'):
 p=original/(stage+'-A1');rs=json.loads((p/'records.json').read_text());ws={int(k):v for k,v in json.loads((p/'worlds.json').read_text()).items()};events=[json.loads(x) for x in (p/'events.jsonl').read_text().splitlines()];starts=[x['value']['id'] for x in events if x['kind']=='call-start'];ends=[x['value'] for x in events if x['kind']=='call-terminal'];expected=schedule(stage)
 assert len(starts)==len(ends)==len(rs)==len(expected) and len(set(starts))==len(starts)
 assert ws=={s:_world(s) for s in ws}
 for r,a,end in zip(rs,expected,ends):
  assert all(r[k]==v for k,v in a.items()) and r==end and r['id'] in starts
  req=request(packet(ws[r['seed']],r['reliability'],r['objective'],r['actor'],stage=='Q0'),'choice');assert r['request']==req and r['request_sha256']==digest(req)==r['checked']['request_sha256']
  assert r['status']=='valid' and r['checked']['result']['choice'] in req['questions']['target']['criteria']
  w=ws[r['seed']];choice=r['checked']['result']['choice'];correct=choice==req['state']['legal_cells'][0] if stage=='Q0' else choice==(w['unknown_cell'] if r['reliability']==.8 else w['report_cell'])
  bundle.append(dict(stage=stage,id=r['id'],seed=r['seed'],objective=r['objective'],reliability=r['reliability'],semantic_optimal=correct if stage=='S1' else None,interface_correct=correct if stage=='Q0' else None,request=r['request'],checked_response=r['checked'],request_sha256=r['request_sha256'],raw_response_retained=False,confidence_retained=False,native_tool_calls=0,action_role='report' if choice==w['report_cell'] else 'unknown',elapsed_seconds=r['elapsed_seconds']))
 stages[stage]=dict(assigned=len(expected),started=len(starts),terminal=len(ends),valid=len(rs),analyzed=len(rs),transport_or_schema_failures=0,wrong=sum(not x['semantic_optimal'] for x in bundle if x['stage']==stage) if stage=='S1' else 0)
 for n in ('records.json','worlds.json','events.jsonl','manifest.json','summary.json'):hashes[stage+'/'+n]=hashlib.sha256((p/n).read_bytes()).hexdigest()
s1=[r for r in bundle if r['stage']=='S1'];pairs=[];stats=[]
for p in (.8,.2):
 for seed in sorted({r['seed'] for r in s1}):
  a=next(r for r in s1 if r['seed']==seed and r['reliability']==p and r['objective']=='legacy');b=next(r for r in s1 if r['seed']==seed and r['reliability']==p and r['objective']=='explicit')
  aa=json.loads(json.dumps(a['request']));bb=json.loads(json.dumps(b['request']));aa['state'].pop('task');bb['state'].pop('task');assert aa==bb
  if a['semantic_optimal'] and not b['semantic_optimal']:pairs.append(dict(seed=seed,reliability=p,legacy_request=a['request_sha256'],explicit_request=b['request_sha256'],legacy_choice=a['checked_response']['result']['choice'],explicit_choice=b['checked_response']['result']['choice']))
 for o in ('legacy','explicit'):
  for good in (True,False):
   xs=[r for r in s1 if r['reliability']==p and r['objective']==o and r['semantic_optimal']==good];ps=[max(r['checked_response']['probabilities']['target'].values()) for r in xs]
   stats.append(dict(reliability=p,objective=o,optimal=good,n=len(xs),selected_probability_mean=statistics.mean(ps) if ps else None,range=[min(ps),max(ps)] if ps else None))
# Exact synthetic request/checked-output payload, compressed; no raw provider-body claim.
data=json.dumps(bundle,sort_keys=True,separators=(',',':')).encode();(out/'native-traces.json.gz').write_bytes(gzip.compress(data,mtime=0))
summary=dict(stages=stages,source_hashes=hashes,all_pairs_only_task_differs=True,regressions=pairs,probability_groups=stats,raw_provider_bodies='not retained; response hashes do not recover text',confidence='validated then discarded by historical adapter',native_tool_calls=0,operator_transcripts_included=False,bundle_sha256=hashlib.sha256((out/'native-traces.json.gz').read_bytes()).hexdigest())
(out/'trace-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
parts=['<!doctype html><meta charset="utf-8"><title>PC5 native trace audit</title><style>body{font:16px system-ui;max-width:1100px;margin:30px auto}pre{white-space:pre-wrap;background:#f4f5f7;padding:15px}details{border-bottom:1px solid #bbb;padding:8px}summary{cursor:pointer}</style><h1>PC5 retained native traces</h1><p>All 140 assigned choices: Q0 12 interface-only; S1 128 with 50 valid-but-suboptimal. Exact saved requests and checked outputs. Raw provider bodies and confidence were not retained. No operator transcripts, native tool calls or new model evidence.</p>']
for r in sorted(bundle,key=lambda r:(r['stage'],bool(r['semantic_optimal']),r['id'])):
 label='interface-only' if r['stage']=='Q0' else 'optimal' if r['semantic_optimal'] else 'VALID BUT SUBOPTIMAL'
 parts.append('<details><summary>'+html.escape(f"{r['stage']} {r['id']} — {label}; chose {r['action_role']}")+'</summary><h3>Actual saved request</h3><pre>'+html.escape(json.dumps(r['request'],indent=2))+'</pre><h3>Checked output (not raw provider body)</h3><pre>'+html.escape(json.dumps(r['checked_response'],indent=2))+'</pre></details>')
(out/'native-traces.html').write_text(''.join(parts));print(json.dumps({'stages':stages,'regressions':len(pairs),'exact_request_output_pairs':len(bundle)}))
