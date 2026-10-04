"""Retrospective projection only: old quotes are not new model outputs."""
from pathlib import Path
import json
from contract import score
here=Path(__file__).resolve().parent
entries=json.loads((here.parents[1]/'results/QM-R1-01/audit.json').read_text());rows=[]
for entry in entries:
 rec=entry['receipt']
 if not rec:continue
 answer={kind:[{'id':f['id'],'quote':None if kind=='sources' and f.get('status')=='unknown' else f['quote']} for f in rec['parsed'][kind]] for kind in ['sources','reports']}
 s=score(entry['case'],answer)
 rows.append({'id':rec['id'],'original_valid':rec['valid'],'original_fully_exact':bool(rec['valid'] and rec['score']['grounded_quotes_valid']),'projected_fully_exact':s['grounded_quotes_valid'] and s['decision_correct'] and s['labels_correct']})
out={'evidence_type':'RETROSPECTIVE SOFTWARE PROJECTION, NOT NATIVE REPAIR QUALIFICATION','transformation':'Retain old literal quotations; explicitly map previously returned unknown source status to null selection; decode only selected clauses. Do not overwrite historical outcomes.','responses':len(rows),'original_fully_exact':sum(r['original_fully_exact'] for r in rows),'projected_fully_exact':sum(r['projected_fully_exact'] for r in rows),'observed_failures':{'QM-R1-01-032':'quoted operating but predicted value0; selected quote deterministically decodes1','QM-R1-01-034':'unknown status with value0; explicit projection maps unknown status to null selection'},'cause_limit':'Observed output divergences are reproduced. No causal claim about repetition, attention or what a new native model will select.','rows':rows}
(here/'saved-trace-diagnosis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
