"""Read-only forensic validation of existing artifacts; no inference, no new worlds."""
import json,hashlib,pathlib,tarfile,collections,statistics,sys
R=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'regrowth-200/src'))
import world
J=lambda p:json.loads(p.read_text())
H=lambda b:hashlib.sha256(b).hexdigest()
report={'regrowth':{},'avalon':{}}
# Validate every existing JSON and event line without echoing arbitrary contents.
files=[]
for project in ('regrowth-200','avalon-swarm'):
 for p in sorted((R/project).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts:continue
  item={'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':H(p.read_bytes())}
  if p.suffix=='.json':
   d=J(p);item['parsed']=True;item['top_level_type']=type(d).__name__;item['entries']=len(d)
  if p.suffix=='.jsonl':
   d=[json.loads(l) for l in p.read_text().splitlines()];item['parsed']=True;item['entries']=len(d)
  if p.suffix=='.log':
   lines=p.read_text().splitlines();parsed=[];nonjson=0
   for line in lines:
    try:parsed.append(json.loads(line))
    except json.JSONDecodeError:nonjson+=1
   item['lines']=len(lines);item['json_entries']=len(parsed);item['other_lines']=nonjson
   item['review_mode']='structural log check; no raw log printing'
  files.append(item)
report['file_inventory']=files
rg=R/'regrowth-200/results';runs=[]
for d in sorted(rg.glob('pilot-*')):
 if not d.is_dir():continue
 m=J(d/'manifest.json'); ws=[J(d/(a['arm']+'-'+('damage' if a['damage'] else 'control')+'.json')) for a in m['assignments']]
 info={'directory':str(d.relative_to(R)),'status':m['status'],'assignments':len(ws),'statuses':dict(collections.Counter(w['status'] for w in ws)),'calls':{k:m[k] for k in ('qwen_calls','laya_calls')},'source_matches':{name:(R/'regrowth-200'/name).exists() and H((R/'regrowth-200'/name).read_bytes())==sha for name,sha in m['source_hashes'].items()}}
 q=d/'qualification.json'
 if q.exists():
  qs=J(q);info['qualification']={model:{'strict':sum(r[model]==r['expected'] for r in qs),'any_shortest':sum(r[model]=='WAIT' if not r['observation']['routes'] else r[model] in r['observation']['routes'] and r['observation']['routes'][r[model]]==min(r['observation']['routes'].values()) for r in qs)} for model in ('qwen','laya')}; info['stored_qualification']=m.get('qualification')
 runs.append(info)
report['regrowth']['attempts']=runs
v4=rg/'pilot-v4';summ=J(v4/'summary.json');recon=[]
for s in summ:
 w=J(v4/(s['id']+'.json'));events=[json.loads(l) for l in (v4/(s['id']+'-events.jsonl')).read_text().splitlines()];ev={(e['round'],e['agent']):e for e in events};memo=[{} for _ in range(world.N)];paths=world.blank();checks=0;next_diff=[];before_damage=None;suboptimal=0;wait_nonempty=0;overrides=[]
 for f in w['frames']:
  t=f['round'];g=world.links(w['damage'] and t>=40)
  if t>=0:
   if t==40 and w['damage']:
    paths=world.erase(paths);before_damage=world.score(paths,g)['valid_fraction']
   new=world.blank()
   for i in range(world.N):
    if i==world.GOAL:continue
    c=world.candidates(i,paths,g);o=world.observe(i,c);key=json.dumps(o,sort_keys=True)
    if key in memo[i]:a=memo[i][key]
    elif w['arm']=='algorithm':a=min(o['routes'],key=o['routes'].get) if o['routes'] else 'WAIT'
    else:
     e=ev.pop((t,i));assert e['observation']==o;a=e['choice'];routes=o['routes'];suboptimal+=bool(routes) and (e['qwen'] not in routes or routes[e['qwen']]>min(routes.values()));wait_nonempty+=bool(routes) and e['qwen']=='WAIT'
     if 'laya' in e and e['qwen']!=e['laya']:overrides.append({'round':t,'agent':i,'qwen':e['qwen'],'laya':e['laya'],'routes':routes})
    memo[i][key]=a
    if a in c:new[i]=[i]+c[a]
   paths=new
  sc=world.score(paths,g)
  for k,v in sc.items():assert f[k]==v,(s['id'],t,k)
  assert f['lengths']==[len(p)-1 if p else None for p in paths]
  assert f['next']==[p[1] if len(p)>1 else None for p in paths]
  checks+=1
  reach=[]
  for i in range(world.N):
   cur=i;seen=set()
   while cur!=world.GOAL and cur not in seen and f['next'][cur] is not None and f['next'][cur] in g[cur].values():seen.add(cur);cur=f['next'][cur]
   reach.append(cur==world.GOAL)
  if reach!=f['valid']:next_diff.append({'round':t,'advertised_valid_fraction':f['valid_fraction'],'next_hop_reach_fraction':sum(reach)/world.N,'differing_cells':sum(a!=b for a,b in zip(reach,f['valid']))})
 assert not ev
 for k in s:
  assert s[k]==(w['frames'][-1][k] if k in ('valid_fraction','optimal_fraction','mean_excess_hops') else w[k]),k
 assert w['qwen_calls']==len(events)
 assert w['laya_calls']==sum('laya' in e for e in events)
 assert w['recovery_rounds']==(world.recovery(w['frames']) if w['damage'] else None)
 recon.append({'id':s['id'],'frames_exactly_reconstructed':checks,'model_event_count':len(events),'pre_update_damage_valid_fraction':before_damage,'qwen_nonminimal_new_decisions':suboptimal,'qwen_wait_with_available_route':wait_nonempty,'laya_overrides':overrides,'next_hop_metric_disagreement_frames':len(next_diff),'next_hop_disagreements':next_diff})
report['regrowth']['reconstruction']=recon
m=J(v4/'manifest.json');qs=J(v4/'qualification.json');events=[json.loads(l) for p in v4.glob('*events.jsonl') for l in p.read_text().splitlines()]
report['regrowth']['accounting']={'qwen_calls_recomputed':len(events)+len(qs),'laya_calls_recomputed':sum('laya' in e for e in events)+len(qs),'qwen_input_tokens_recomputed':sum(e['qwen_receipt']['input_tokens'] for e in events+qs),'qwen_output_tokens_recomputed':sum(e['qwen_receipt']['output_tokens'] for e in events+qs),'laya_input_tokens_estimate_recomputed':sum(e['laya_receipt']['input_tokens_estimate'] for e in events+qs if 'laya_receipt' in e)}
replay=json.loads((R/'regrowth-200/site/data.js').read_text().removeprefix('window.REGROWTH=').strip().removesuffix(';'))
assert replay['manifest']==m
for w in replay['worlds']:assert w==J(v4/(w['id']+'.json'))
report['regrowth']['replay_exact_match']=True
idx=J(rg/'evidence-index.json');archive_bytes=(rg/'evidence.tar.gz').read_bytes();assert H(archive_bytes)==idx['sha256'];arc=[];sourcebytes={}
with tarfile.open(rg/'evidence.tar.gz') as tf:
 for member in tf:
  data=tf.extractfile(member).read();p=R/member.name;arc.append({'path':member.name,'bytes':len(data),'matches_current':p.exists() and p.read_bytes()==data});sourcebytes[H(data)]=member.name
assert [a['path'].removeprefix('regrowth-200/') for a in arc]==idx['files']
report['regrowth']['archive']={'checksum_valid':True,'member_count':len(arc),'members':arc,'manifest_hashes_missing_from_current_and_archive':{d.name:[name for name,sha in J(d/'manifest.json')['source_hashes'].items() if sha not in sourcebytes and H((R/'regrowth-200'/name).read_bytes())!=sha] for d in rg.glob('pilot-*') if d.is_dir()}}
av=R/'avalon-swarm';ar=[]
for name in ('scale-final','recovery-pilot','consensus-v02'):
 d=av/'results'/name;rows=[json.loads(l) for l in (d/'outcomes.jsonl').read_text().splitlines()];plan=J(d/'plan.json');source=av/('benchmark.py' if name=='consensus-v02' else 'results/reference-v01/benchmark.py');assert (d/'source.sha256').read_text().strip()==H(source.read_bytes());assert len(rows)==len(plan)
 for config,row in zip(plan,rows):
  assert all(row[k]==v for k,v in config.items());assert row['status']=='completed';assert row['message_deliveries']<=275*row['n'];assert row['claim_deliveries']<=1100*row['n']
 chains=[]
 for p in d.glob('events-*.jsonl'):
  previous='0'*64;count=0;payload=None
  for line in p.read_text().splitlines():
   e=json.loads(line);h=e.pop('hash');assert e['seq']==count and e['previous']==previous;assert H(json.dumps(e,sort_keys=True,separators=(',',':')).encode())==h;previous=h;count+=1
   if e['kind']=='outcome':payload=e['payload']
  row=next(r for r in rows if r['recovery']==payload['recovery'] and r['seed']==payload['seed']);assert row['event_hash']==previous and row['event_count']==count
  assert all(row[k]==v for k,v in payload.items());chains.append({'path':str(p.relative_to(R)),'events':count,'valid_chain_and_terminal_outcome':True})
 item={'name':name,'outcomes':len(rows),'source_hash_valid':True,'all_assignments_present':True,'event_traces':chains}
 if name=='recovery-pilot':
  means={r:{key:statistics.mean(x[key] for x in rows if x['recovery']==r) for key in ('post_audit_mission_success_fraction','good_council_fraction','ordinary_good_brier','post_audit_contradiction_exposures','flagged_honest_origins','flagged_evil_origins')} for r in ('none','audit','repair')};diffs=[]
  for seed in range(5):
   group={r['recovery']:r for r in rows if r['seed']==seed};assert len(set(r['scenario_hash'] for r in group.values()))==1;assert len(set(next(p['brier'] for p in r['brier_trajectory'] if p['point']=='before_audit') for r in group.values()))==1
   diffs.append({'seed':seed,**{k:group['repair'][k]-group['audit'][k] for k in ('post_audit_mission_success_fraction','ordinary_good_brier','post_audit_contradiction_exposures')}})
  item.update(means=means,paired_repair_minus_audit=diffs)
 if name=='consensus-v02':
  for r in rows:assert len(r['consensus_trajectory'])==r['ticks'];assert r['belief_probe_calls']==r['ticks']*r['n']//2;assert r['good_swarm_win']==(r['mission_swarm_win'] and r['truth_consensus_pass'])
  item['passes']=sum(r['truth_consensus_pass'] for r in rows);item['failures']=dict(collections.Counter(f"{r['consensus_failure']['reason']}@{r['consensus_failure']['round']}" for r in rows))
 ar.append(item)
report['avalon']['validation']=ar
(R/'review-2026-10-04/regrowth-avalon-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'files':len(files),'regrowth_frames_reconstructed':sum(r['frames_exactly_reconstructed'] for r in recon),'regrowth_events_reconstructed':len(events),'regrowth_accounting':report['regrowth']['accounting'],'next_hop_disagreements':[{k:r[k] for k in ('id','next_hop_metric_disagreement_frames','pre_update_damage_valid_fraction','qwen_nonminimal_new_decisions')} for r in recon],'archive_missing_sources':report['regrowth']['archive']['manifest_hashes_missing_from_current_and_archive'],'avalon_outcomes':sum(x['outcomes'] for x in ar),'avalon_traces':sum(len(x['event_traces']) for x in ar),'avalon_events':sum(t['events'] for x in ar for t in x['event_traces'])},indent=2))
