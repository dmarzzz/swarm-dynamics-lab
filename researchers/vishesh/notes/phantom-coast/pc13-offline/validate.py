"""Offline acceptance and packet freezing; never dispatches requests."""
import json,math,secrets,sys
from pathlib import Path
from packet import *
from analysis import summarize
here=Path(__file__).resolve().parent;dev=roots('PC13-development-v1');rows=assignments(dev);checks=[]
def ok(name,value):assert value,name;checks.append(name)
ok('assignment_manifest_unique_768',len(rows)==len({r['id'] for r in rows})==768)
maxerr=max(abs(exact(r['packet'])-enumerated(r['packet'])) for r in rows);ok('independent_joint_enumeration',maxerr<1e-12)
blind=0;archive_failures=0
for w in dev:
 for false,evidence,after in itertools.product((False,True),('single','copies','independent'),(False,True)):
  p=packet(w,false,evidence,'flat',after);l=packet(w,false,evidence,'linked',after);idx=p.pop('index');ok('representation_factual_parity',p==l);ok('index_is_visible_graph_closure',idx=={t:sorted(ancestors(l,t)) for t in l['tips']})
  ok('no_hidden_condition_or_truth_fields',set(l)=={'target','obs','link','tips','direct'})
  if not after and evidence=='copies':blind+=abs(exact(l,True)-exact(l))>.1
  if not after:
   archive=json.loads(compact(l));archive['tips']=list(archive['obs']);archive_failures+=abs(exact(archive)-exact(l))>.05
  if after:ok('direct_truth_override',exact(l)==float(w['truth']=='LAND'))
 for false in (False,True):
  p=packet(w,false,'single','linked',False);c=packet(w,false,'copies','linked',False);i=packet(w,false,'independent','linked',False)
  ok('arm_archive_parity',p['obs']==c['obs']==i['obs']);ok('node_count_not_arm_cue',len(p['link'])==len(c['link'])==len(i['link'])==13);ok('copies_are_same_evidence',abs(exact(p)-exact(c))<1e-12);ok('independent_observation_adds_evidence',abs(exact(i)-exact(c))>.10)
p=packet(dev[0],True,'copies','linked',False);key=next(iter(p['link']));p['link'][key]=[key]
try:ancestors(p,key);raise AssertionError('cycle accepted')
except ValueError:checks.append('cycle_rejected')
p=packet(dev[0],True,'single','linked',False);p['tips']=['missing']
try:observations(p);raise AssertionError('missing reference accepted')
except ValueError:checks.append('missing_reference_rejected')
answers={r['id']:exact(r['packet']) for r in rows};a=summarize(rows,answers);ok('oracle_null_analysis',a['primary']==0 and a['absolute_drift_max']==0)
for r in rows:
 if r['false'] and r['evidence']=='copies' and r['representation']=='linked' and not r['after']:
  claim=next(v[1] for v in r['packet']['obs'].values() if v[0]==r['packet']['target']);answers[r['id']]+= .1 if claim=='LAND' else -.1
b=summarize(rows,answers);ok('known_effect_analysis',abs(b['primary']-.1)<1e-12)
for r in rows:
 if r['root']=='R00' and r['block']==1 and r['false'] and r['evidence']=='copies' and r['representation']=='linked' and not r['after']:answers[r['id']]=1-answers[r['id']]
c=summarize(rows,answers);ok('heterogeneous_root_drift_detected',c['absolute_drift_max']>.1 and c['absolute_drift_p90']==0)
for r in rows:
 if r['false'] and r['evidence']=='copies' and r['representation']=='linked' and not r['after']:answers[r['id']]=None;break
m=summarize(rows,answers);ok('missing_not_zero_filled',m['primary'] is None and m['primary_bounds'][0]<m['primary_bounds'][1])
try:summarize(rows,{rows[0]['id']:True});raise AssertionError('bool accepted')
except ValueError:checks.append('malformed_probability_rejected')
# Scope one seed per freeze; do not regenerate an existing sealed packet.
private=Path(sys.argv[1]);private.mkdir(parents=True,exist_ok=True)
manifest=private/'main.json'
if manifest.exists():main=json.loads(manifest.read_text())
else:
 ws=roots(secrets.token_hex(32));main=dict(roots=ws,assignments=assignments(ws));manifest.write_text(json.dumps(main,indent=2));manifest.chmod(0o600)
ok('sealed_manifest_matches_frozen_generator',main['assignments']==assignments(main['roots']))
q=qualification(dev);size=max(len(compact(request(r['packet'])).encode()) for r in main['assignments']+q)
ok('complete_request_envelope',size<=1536)
ok('archive_counting_has_no_challenge_shortcut',archive_failures==96)
report=dict(request_cap_bytes=1536,output_cap_tokens=32,reserve_per_call_usd=.00448,maximum_new_api_usd=3.584,cumulative_api_bound_usd=5.182553490,cumulative_all_in_bound_usd=6.182553490,offline_only=True,checks_executed=len(checks),unique_checks=sorted(set(checks)),development_roots=16,main_roots=16,main_assignments=768,qualification_assignments=32,maximum_body_bytes=size,arithmetic_max_error=maxerr,blind_control_divergences=blind,ignore_graph_archive_failures=archive_failures,manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),qualification_sha256=digest(q),source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in here.glob('*.py')},new_model_calls=0)
(here/'OFFLINE.json').write_text(json.dumps(report,indent=2)+'\n');(here/'development-controls.json').write_text(json.dumps(q,indent=2)+'\n');(here/'analysis-fixtures.json').write_text(json.dumps(dict(null=a,effect=b,heterogeneous=c,missing=m),indent=2)+'\n');print(json.dumps(report,indent=2))
