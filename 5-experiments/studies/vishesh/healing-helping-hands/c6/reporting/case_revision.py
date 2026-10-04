"""Offline development examples; no model calls or changes to frozen native cases."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Three paired contrasts: sign with distractor, contradiction vs scoped distractor,
# absent target evidence vs explicitly measured negative evidence.
conditions=[('sign-positive',[('ALPHA',8),('BETA',-5)],'SUPPORT'),('sign-negative',[('ALPHA',-8),('BETA',-5)],'REFUTE'),('conflict',[('ALPHA',8),('ALPHA',-5)],'UNCERTAIN'),('other-task',[('ALPHA',8),('BETA',-5)],'SUPPORT'),('absent',[('BETA',5)],'UNCERTAIN'),('measured-negative',[('ALPHA',-8),('BETA',5)],'REFUTE')]
rows=[]
for name,pairs,label in conditions:
 facts=[{'task':t,'session':'ONE','delta':d} for t,d in pairs]
 values=[f['delta'] for f in facts if f['task']=='ALPHA']
 report=' '.join(f"In session ONE on task {f['task']}, method M accuracy was {abs(f['delta'])} percentage points {'higher' if f['delta']>0 else 'lower'} than baseline." for f in facts)
 if len(values)>1:report+=' Both reports concern the same session and task; neither result supersedes the other.'
 if not values:report+=' Task ALPHA has no accuracy measurement for session ONE.'
 baseline='UNCERTAIN' if not values or min(values)<=0<max(values) else ('SUPPORT' if min(values)>0 else 'REFUTE')
 assert baseline==label
 rows.append({'id':'development-'+name,'claim':'Method M had higher measured accuracy than baseline on task ALPHA in session ONE.','report':report,'facts':facts,'expected':label,'label_rule':'Conflicting same-task same-session results with no precedence are UNCERTAIN; other tasks are irrelevant.'})
assert Counter(r['expected'] for r in rows)=={'SUPPORT':2,'REFUTE':2,'UNCERTAIN':2}
result={'status':'offline_development_only','native_calls':0,'baseline':'structured fact ledger, not a natural-language parser','cases':rows,'checks':{'case_count':6,'fact_labels_match':True,'holdout':False,'independent_adjudication':False,'manual_wording_review':'All six reports inspected: target scope, contradictions, missingness and paired labels explicit.'}}
(ROOT/'CASE-REVISION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
