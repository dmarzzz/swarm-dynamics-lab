"""Retrospective analysis of saved evidence only. No provider imports or model calls."""
import collections, hashlib, itertools, json, random, sys
from pathlib import Path
SOURCES=('probe','ledger','canary')
def truth(c,scenario,source):
 e=c['evidence'][source]
 return (source if e['signal'] else 'none') if scenario=='incident' else ('ship' if e['signal'] and e['fresh'] else 'hold')
def rule(seed,scenario,step):
 v=random.Random(seed).sample(list(SOURCES),2)
 if scenario!='migration' and step>=5:v[0]=SOURCES[(SOURCES.index(v[0])+1)%3]
 return dict(zip('AB',v))
def run(root):
 checks=collections.Counter();groups=collections.defaultdict(lambda:collections.Counter());errors=[];candidate=collections.defaultdict(lambda:collections.Counter());histories=[];events=[];hashes={};equivalence=[];coverage=collections.defaultdict(collections.Counter)
 for stage in ('S0','S0-repair'):
  p=root/stage
  starts={x['call']:x for f in (p/'calls').glob('*-started.json') for x in [json.loads(f.read_text())]}
  finishes={x['call']:x for f in (p/'calls').glob('*-finished.json') for x in [json.loads(f.read_text())]}
  for f in sorted((p/'events').glob('*.json')):
   raw=f.read_bytes();hashes[str(f.relative_to(root))]=hashlib.sha256(raw).hexdigest();e=json.loads(raw);events.append(e)
   call=e['calls'][0];req=call['request'];obs=req['observation'];result=call['result'];num=result['call'];cases=e['cases'];sc=e['scenario'];r=rule(e['seed'],sc,e['step']);out={d['id']:d['command'] for d in result['value']['decisions']};inverse={v:k for k,v in obs['commands'].items()};actions={i:inverse[v] for i,v in out.items()};scores={x['id']:x for x in e['scores']}
   assert starts[num]['request']==req and finishes[num]==result;checks['durable_request_response_matches']+=1
   assert r==e['evaluator']['rule'] and cases==obs['cases'];checks['rule_and_case_matches']+=1
   assert len(out)==len(cases)==6 and set(out)=={c['id'] for c in cases};checks['complete_unique_valid_commands']+=1
   assert result['stop_reason']=='end_turn' and not result['error'];checks['complete_provider_outputs']+=1
   if stage=='S0-repair':
    text=starts[num]['exact_user_text'];tail=text.split('CURRENT CASES. Read each row independently. Return exactly these IDs and one valid command per row.\n')[1];lines=tail.splitlines();assert len(lines)==7
    for line,c in zip(lines[1:],cases):
     v=line.split(' | ');expect=[c['id'],c['service_class'],c['summary'],c['queue']]+['YES' if c['evidence'][s][k] else 'NO' for s in SOURCES for k in ('signal','fresh')];assert v==expect;checks['exact_current_table_rows']+=1
    if e['arm']=='ceiling':
     assert set(obs)=={'step','cases','commands','explicit_current_rule'} and obs['explicit_current_rule'] in text;checks['clean_ceiling_rule_delivered']+=1
     if 'ONE unknown governing source' in req['instructions'] and 'Learn which source' in req['instructions']:checks['ceiling_system_learner_framing']+=1
   if obs.get('history'):
    for cls in 'AB':
     fit=[s for s in SOURCES if all(truth(h['observation'],sc,s)==h['accepted_action'] for h in obs['history'] if h['observation']['service_class']==cls)]
     assert fit==[rule(e['seed'],sc,0)[cls]];checks['uniquely_identifiable_history_classes']+=1
   group=f'{stage}/{sc}/{e["arm"]}/{e["step"]}';preds=collections.defaultdict(list)
   buckets=collections.defaultdict(list)
   for c in cases:
    ev=c['evidence'][r[c['service_class']]];key=(c['service_class'],ev['signal'],ev['fresh'] if sc!='incident' else None);buckets[key].append(c)
    for source in SOURCES:coverage[stage+'/'+e['arm']+'/'+source]['stale']+=int(not c['evidence'][source]['fresh']);coverage[stage+'/'+e['arm']+'/'+source]['n']+=1
   for key,cs in buckets.items():
    if len(cs)>1:
     equivalence.append({'stage':stage,'run':e['run'],'step':e['step'],'key':key,'decisions':[{ 'id':c['id'],'action':actions[c['id']]} for c in cs],'inconsistent':len({actions[c['id']] for c in cs})>1})
   expected=[truth(c,sc,r[c['service_class']]) for c in cases];actual=[actions[c['id']] for c in cases]
   for pos,c in enumerate(cases):
    i=c['id'];src=r[c['service_class']];bits=c['evidence'][src];t=expected[pos];a=actual[pos];s=scores[i];assert (s['truth'],s['action'],s['correct'],s['observed'])==(t,a,t==a,True);checks['independent_scores_match']+=1
    for g in [group,stage+'/'+sc+'/'+e['arm'],stage+'/'+e['arm'],stage+'/all',group+'/position'+str(pos),stage+'/'+sc+'/'+e['arm']+'/bits'+str(int(bits['signal']))+str(int(bits['fresh']))]:groups[g]['n']+=1;groups[g]['correct']+=int(a==t)
    if a!=t:errors.append({'stage':stage,'run':e['run'],'step':e['step'],'position':pos,'id':i,'source':src,'governing':bits,'evidence':c['evidence'],'summary':c['summary'],'truth':t,'action':a,'notebook':result['value']['notebook']})
    preds['correct'].append(t)
    for source in SOURCES:preds['always_source_'+source].append(truth(c,sc,source))
    preds['swapped_class'].append(truth(c,sc,r['B' if c['service_class']=='A' else 'A']))
    preds['stale_rule'].append(truth(c,sc,rule(e['seed'],sc,0)[c['service_class']]))
    if sc!='incident':
     for name,value in [('signal_only',bits['signal']),('fresh_only',bits['fresh']),('signal_OR_fresh',bits['signal'] or bits['fresh']),('all_sources_ready',all(x['signal'] and x['fresh'] for x in c['evidence'].values())),('summary_shortcut',c['summary']=='looks clear'),('always_hold',False),('always_ship',True)]:preds[name].append('ship' if value else 'hold')
    for shift in (-1,1):preds['row_shift_'+str(shift)].append(expected[(pos+shift)%6])
   for name,pred in preds.items():
    k=f'{stage}/{sc}/{e["arm"]}/{name}';candidate[k]['decisions']+=6;candidate[k]['matches']+=sum(x==y for x,y in zip(actual,pred));candidate[k]['whole_batches']+=int(actual==pred);candidate[k]['batches']+=1
 return {'scope':'Retrospective descriptive audit; candidate signature matches are nonexclusive, not causal evidence. No model calls.','checks':dict(checks),'groups':dict(groups),'candidate_signatures':dict(candidate),'errors':errors,'equivalent_input_groups':equivalence,'freshness_coverage':dict(coverage),'input_event_sha256':hashes}
if __name__=='__main__':
 out=run(Path(sys.argv[1]));Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':out['checks'],'groups':{k:v for k,v in out['groups'].items() if k.endswith('/all') or k.count('/')==2},'errors':len(out['errors'])},indent=2))
