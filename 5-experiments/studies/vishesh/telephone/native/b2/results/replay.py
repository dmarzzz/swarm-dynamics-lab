"""Recompute saved B2 decisions/retention without credentials or fresh model calls."""
import json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'src'))
from native import packet,sha
from report import analyze,validate_annotations
rows=json.loads((ROOT/'AUTHORED-TRACE-AUDIT.json').read_text())
with tempfile.TemporaryDirectory() as tmp:
 out=Path(tmp);(out/'packet.json').write_text(json.dumps(packet()))
 for r in rows:
  assert sha(r['request'])==r['request_sha256'] and sha(r['response'])==r['response_sha256']
  prefix=r['assignment'].replace(':','_')
  for suffix in ('request','response'):(out/(prefix+'.'+suffix+'.json')).write_text(json.dumps(r[suffix]))
 actual=analyze(out)
 saved=json.loads((ROOT/'DECISION-ANALYSIS.json').read_text())
 assert {k:v for k,v in actual.items() if k!='semantic_annotations'}==saved
 annotations=json.loads((ROOT/'SEMANTIC-ANNOTATIONS.json').read_text());validate_annotations(actual,annotations)
 results=json.loads((ROOT/'RESULTS.json').read_text())
 for metric in results['metrics']:
  ids={r['id'] for r in actual['rows'] if (r['block'],r['arm'],r['hop'])==(metric['block'],metric['arm'],metric['hop'])}
  cells=[r for r in annotations if r['assignment']in ids]
  for view in ('report_content','strict_integrated'):
   counts={v:sum(r[view]==v for r in cells) for v in ('retained','lost','ambiguous')}
   assert counts==metric[view]['counts']
   assert metric[view]['retention_bounds']==[counts['retained']/len(cells),(counts['retained']+counts['ambiguous'])/len(cells)]
 print(json.dumps({'main_responses_replayed':len(rows),'semantic_cells_checked':len(annotations),'paired_primary_contrast':actual['complete_root_mean'],'new_model_calls':0}))
