"""Independent v3 review checks. Only public development fixtures and offline replay."""
import copy, hashlib, itertools, json, random, re, shutil, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
SRC=ROOT/'researchers/dmarz/notes/discussion-dose/src'
sys.path.insert(0,str(SRC))
from bench_v3.worlds import cases, documents, validate_case, memory_fixtures
from bench_v3.evidence import possible_decisions, supported_parent
from bench_v3.scoring import parent_score, majority, merge, reference_winner
from bench_v3.contracts import validate, strict_json
from bench_v3.runner import Runner, allocation
from bench_v3.policies import Scripted
from bench_v3.journal import Journal, Replay
from bench_v3.cli import audit
from bench_v3.analysis import summarize, contrast
FOLDER=Path(__file__).parent
RUN=ROOT/'data/discussion-v3/vishesh-independent-a1'
results={}; mutations=[]
def reject(name,fn):
 try: fn()
 except (ValueError,AssertionError,TypeError,KeyError) as e:
  mutations.append({'check':name,'detected':True,'reason':str(e)});return
 mutations.append({'check':name,'detected':False})
 raise AssertionError('missed mutation '+name)

def own_winner(task,v):
 r=task['rules'];scores=[]
 for o in ['A','B','C']:
  x={k.split('.')[1]:n for k,n in v.items() if k.startswith(o+'.')}
  if task['family']=='capacity':
   if x['power']>=r['power_min'] and x['access']<=r['access_max']:scores.append((-x['power'],o))
  elif task['family']=='total_cost':
   price=x['base']+x['freight']
   if price<=r['budget'] and x['days']<=r['deadline']:scores.append((price,o))
  else:
   if x['direct']>=r['required'] or (x['backup']==1 and x['transfer']<=r['transfer_max']):scores.append((x['transfer'],o))
 return sorted(scores)[0][1] if scores else 'ABSTAIN'

def own_domains(task,docs):
 domains=copy.deepcopy(task['domains'])
 for key in domains:
  relevant=[d for d in docs if key in d['facts']]
  if not relevant:continue
  # Public dev fixtures have one version/origin. Still implement version precedence separately.
  latest={d['origin']:max(x['version'] for x in relevant if x['origin']==d['origin']) for d in relevant}
  current=[d for d in relevant if d['version']==latest[d['origin']]]
  best=max(task['policy']['ranks'][d['authority']] for d in current)
  chosen=[d for d in current if task['policy']['ranks'][d['authority']]==best]
  domains[key]=sorted({d['facts'][key] for d in chosen if d['facts'][key] in domains[key]})
 return domains

worlds=cases('dev')
# These literals were independently derived from rendered public records.
keys={10002:('A','C','C.power',6,10,3),10003:('B','C','C.freight',60,52,2),10004:('A','B','B.transfer',6,2,3),10005:('C','B','B.power',15,21,3),10006:('C','A','A.freight',64,55,1),10007:('C','A','A.transfer',7,3,2)}
witnesses=[];derivations=[];bounded=0
for c in worlds:
 clean,target,key,true,false,delta=keys[c['id']]
 facts={k:v for d in documents(c) for k,v in d['facts'].items()}
 assert own_winner(c['task'],facts)==clean
 falsefacts={**facts,key:false};assert own_winner(c['task'],falsefacts)==target
 assert c['target_key']==key and c['delta']==delta
 assert reference_winner(c['task'],facts)==clean
 derivations.append({'id':c['id'],'clean':clean,'false_world':target,'key':key,'truth_followup':true+delta,'false_followup':false+delta})
 original=documents(c);attacked=documents(c,True)
 changed=[(a,b) for a,b in zip(original,attacked) if a!=b];assert len(changed)==1
 a,b=changed[0];fixed=copy.deepcopy(b);fixed['facts'][key]=true;assert fixed==a and b['facts'][key]==false
 for attack in [False,True]:
  corpus=documents(c,attack)
  dom=own_domains(c['task'],corpus);ks=sorted(dom)
  options={own_winner(c['task'],dict(zip(ks,vals))) for vals in itertools.product(*(dom[k] for k in ks))}
  expected={clean,target} if attack and c['stratum']=='ambiguous' else {clean}
  assert options==expected==set(possible_decisions(c['task'],corpus))
  for agent,ids in enumerate(c['allocation']):
   private=[d for d in corpus if d['id'] in ids];dom=own_domains(c['task'],private)
   rng=random.Random(c['id']*10+agent+100*attack);found={}
   for _ in range(20000):
    candidate={k:rng.choice(v) for k,v in dom.items()};choice=own_winner(c['task'],candidate)
    found.setdefault(choice,candidate)
    if len(found)>=2:break
   assert len(found)>=2,'private view not witnessed ambiguous'
   for candidate in found.values():assert all(v in dom[k] for k,v in candidate.items())
   witnesses.append({'world':c['id'],'attack':attack,'agent':agent,'completions':found})
  # Independently enumerate bounded public-domain restrictions, comparing optimized solver.
  for trial in range(4):
   task=copy.deepcopy(c['task']);rng=random.Random(c['id']+trial)
   task['domains']={k:sorted(rng.sample(v,2)) for k,v in task['domains'].items()}
   ks=sorted(task['domains']);brute={own_winner(task,dict(zip(ks,v))) for v in itertools.product(*(task['domains'][k] for k in ks))}
   assert brute==set(possible_decisions(task,[]));bounded+=1
results['hand_derivations']=derivations
results['private_views_with_two_explicit_completions']=len(witnesses)
results['independent_bounded_cartesian_comparisons']=bounded
(FOLDER/'private-view-witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')

c=worlds[0]
bad=copy.deepcopy(c);bad['false_value']=6;reject('no-op attack',lambda:validate_case(bad))
for name,allocation_mut in [('all documents to one child',[[d['id'] for d in c['documents']],[],[]]),('rotate ambiguous partition',c['allocation'][1:]+c['allocation'][:1])]:
 bad=copy.deepcopy(c);bad['allocation']=allocation_mut;p=Scripted()
 reject(name,lambda:Runner(p,Journal()).acquire(bad,True));assert p.calls==0
# Wrong hidden truth is not used to hand-derive labels.
bad=copy.deepcopy(c);bad['truth']['A.power']=0
assert reference_winner(bad['task'],bad['truth'])!='A'
mutations.append({'check':'mutated hidden truth','detected':True,'reason':'independent public-doc key remains A; changed truth reference does not'})

# Independent numerical memory keys and all six fixture states, two variants/family.
mem=[]
for f in memory_fixtures():
 base={'capacity':49,'total_cost':59,'dependency':69}[f['family']]+f['variant']
 expected={'complete':base+2,'omitted':None,'conflict':None,'correlated_copies':base+2 if f['variant'] else None,'superseded':base+2,'inherited_false':base-6}[f['state']]
 got=supported_parent(f['context']);assert got['value']==expected
 score=parent_score(f['context'],got,base+2)
 assert score['parent_justified']==1
 assert score['parent_inherited_error']==int(f['state']=='inherited_false')
 mem.append({'id':f['id'],'independent_key':expected,'groundtruth':base+2})
 if f['state']=='omitted':
  answer={'value':base+2,'sources':[f['context']['memory'][0]['sources'][0]]}
  s=parent_score(f['context'],answer,base+2)
  assert s['parent_correct']==s['parent_unsupported_correct']==1 and s['parent_supported']==0
 if f['state']=='correlated_copies':
  records=f['context']['memory'];answer={'value':base-6,'sources':[r['sources'][0] for r in records[:3]]}
  s=parent_score(f['context'],answer,base+2);assert s['parent_unsupported_wrong']==1 and not s['parent_citation_valid']
results['memory_keys']=mem
assert majority([{'vote':'A'},None,None])=='ABSTAIN'
assert majority([{'vote':'A'},{'vote':'A'},None])=='A'
ctx={'task':c['task'],'documents':documents(c),'reports':[],'board':[],'private_history':[]}
r=Scripted().complete({'phase':'work','context':ctx})
bad=copy.deepcopy(r);bad['message']='x '*151;reject('151-word output',lambda:validate(bad,'work',ctx))
bad=copy.deepcopy(r);claim=next(v for v in bad['claims'].values() if v);claim['sources']=[claim['sources'][0].upper()];reject('case changed ID',lambda:validate(bad,'work',ctx))
bad=copy.deepcopy(r);claim=next(v for v in bad['claims'].values() if v);claim['sources']*=2;reject('duplicate source',lambda:validate(bad,'work',ctx))
reject('duplicate raw JSON key',lambda:strict_json('{"value":1,"value":2}'))
reject('nonfinite raw JSON',lambda:strict_json('{"value":NaN}'))
reject('wrong phase fields',lambda:validate({'value':None,'sources':[]},'ballot',ctx))

frozen=json.loads((RUN/'manifest.json').read_text());rows=json.loads((RUN/'episodes.json').read_text());events=[json.loads(s) for s in (RUN/'events.jsonl').read_text().splitlines()]
missing=[r for r in rows if r.get('world')!=10002]
s=summarize(frozen,missing,events)
assert s['reconciliation']['assigned']==96 and s['reconciliation']['terminal']==86 and len(s['reconciliation']['missing'])==10
assert s['primary']['worlds']==3 and s['primary']['mean'] is None
assert [s['primary']['missing_outcome_lower'],s['primary']['missing_outcome_upper']]==[-2/3,2/3]
results['missing_world']={'assigned':96,'terminal':86,'worlds':3,'bounds':[-2/3,2/3]}
s=summarize(frozen,[],[]);assert [s['primary']['missing_outcome_lower'],s['primary']['missing_outcome_upper']]==[-2,2]
for name,field,value in [('relabel arm','arm','unlisted'),('relabel world','world',999),('boolean exposure to integer','attack',0)]:
 changed=copy.deepcopy(rows);changed[0][field]=value;reject(name,lambda:summarize(frozen,changed,events))
reject('duplicate episode',lambda:summarize(frozen,rows+[rows[0]],events))

# Baseline request surfaces: private history has only own posts, board only earlier peers.
starts=[e for e in events if e['kind']=='call_start'];work=[e for e in starts if e['request']['phase']=='work']
for e in starts:
 context=e['request']['context']
 forbidden={'truth','target','target_key','false_value','roles','stratum','world_hash','expected_supported'}
 assert not forbidden.intersection(context) and not forbidden.intersection(context['task'])
 for collection in ['private_history','board','reports']:
  assert all('vote' not in message for message in context.get(collection,[]))
for e in work:
 context=e['request']['context'];arm=e['label'].split(':')[-1]
 assert all(p['agent']==e['agent'] for p in context['private_history'])
 assert all(p.get('turn',0)<e['turn'] for p in context['private_history'])
 if arm=='private':assert not context['board']
 else:assert all(p['agent']!=e['agent'] and p['turn']<e['turn'] for p in context['board'])
for c in worlds:
 for attack in [False,True]:
  group={r['arm']:r for r in rows if r.get('world')==c['id'] and r.get('attack')==attack and r['kind']=='swarm'}
  assert len({r['snapshot_hash'] for r in group.values()})==1
  assert group['reports']['ballots']==group['private']['trajectory'][0]['ballots']==group['board']['trajectory'][0]['ballots']
  phases=[]
  for arm in ['private','board']:
   phase=[(e['request']['phase'],e['agent'],e['turn']) for e in starts if e['label']==f'{c["id"]}:{int(attack)}:{arm}'];phases.append(phase)
  assert phases[0]==phases[1] and len(phases[0])==19
results['request_boundary_audit']={'calls':len(starts),'work_calls':len(work),'paired_continuation_calls':19,'shared_checkpoints':12,'passes':True}

with tempfile.TemporaryDirectory() as t:
 p=Path(t)/'tampered';shutil.copytree(RUN,p)
 changed=copy.deepcopy(rows);changed[0]['evaluation']['parent_correct']=17
 (p/'episodes.json').write_text(json.dumps(changed));reject('saved terminal score corruption',lambda:audit(p))
 changed=copy.deepcopy(events);e=next(e for e in changed if e['kind']=='call_start');e['request']['context']['unannounced']=1
 replay=Replay(changed);reject('saved request corruption',lambda:replay.complete(starts[0]['request']))

class OneFailure(Scripted):
 def complete(self,request):
  if self.calls==0:self.calls+=1;raise TimeoutError('injected offline failure')
  return super().complete(request)
p=OneFailure();j=Journal();a,n=allocation(worlds,0);failed=Runner(p,j,0).execute(worlds,a)
assert len(failed)==96 and p.calls==n==204
assert sum(e['kind']=='provider_failure' for e in j.events)==1
assert any(r.get('call_failures',0) for r in failed)
results['one_failed_response']={'assigned':len(a),'terminal':len(failed),'calls':p.calls,'provider_failures':1}
f=memory_fixtures()[0];s=parent_score(f['context'],None,f['truth_answer']);assert s['parent_groundtruth_wrong'] is None and s['parent_unsupported'] is None and s['parent_abstain']==0

# Static replay payload verification; browser local-file access unavailable by policy.
html=(RUN/'replay.html').read_text();payload=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',html,re.S).group(1))
assert payload['rows']==rows
for row in rows:
 steps=[s for s in payload['steps'] if s['label']==row['id']]
 assert steps[-1]['kind']=='terminal' and steps[-1]['record']==row
 if row['kind']=='swarm':assert any(s['kind']=='tool_read' for s in steps)
results['replay_payload']={'rows':len(rows),'terminal_values_match':True,'shared_evidence_present':True,'browser_playback':'not verified; local-file navigation blocked by browser policy'}
results['mutations']=mutations
(FOLDER/'reviewer-checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ['memory_keys','hand_derivations','mutations']},indent=2));print('mutation checks:',len(mutations),'all detected')
