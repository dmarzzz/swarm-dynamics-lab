"""Evidence-grounded metrics; unobserved choices never become correct outcomes."""
from contract import ACTORS

def summarize(episode):
 w=episode['world'];sites=list(w['truth']);target=w['target'];timelines=[]
 for t in episode['turns']:
  target_counts=dict(correct=0,wrong=0,unknown=0,invalid=0,missing=0,failed=0);allcounts=dict(correct=0,wrong=0,unknown=0,unobserved=0);loss=0.;post=dict(wrong=0,unknown=0,unobserved=0,denominator=0);votes=[];seed_target=None
  for e in t['entries']:
   valid=e['status']=='valid';m=e.get('decision',{}).get('map',{})
   for s in sites:
    if not valid:allcounts['unobserved']+=1;continue
    v=m[s];category='unknown' if v=='UNKNOWN' else 'correct' if v==w['truth'][s] else 'wrong';allcounts[category]+=1;loss+=.25 if category=='unknown' else int(category=='wrong')
   if e['agent']==w['seed_actor']:
    seed_target=dict(status=e['status'],choice=m.get(target),category=e['status'] if not valid else 'unknown' if m[target]=='UNKNOWN' else 'correct' if m[target]==w['truth'][target] else 'wrong');continue
   category=e['status'] if not valid else 'unknown' if m[target]=='UNKNOWN' else 'correct' if m[target]==w['truth'][target] else 'wrong'
   target_counts[category]+=1
   if valid:votes.append(m[target])
   visible=any(r['site']==target for r in e['packet']['observations'])
   if visible:
    post['denominator']+=1
    if not valid:post['unobserved']+=1
    elif category in ('wrong','unknown'):post[category]+=1
  absent=sum(target_counts[k] for k in ['invalid','missing','failed']);den=len(ACTORS)-1
  timelines.append(dict(time=t['time'],unexposed_target=target_counts,seed_target=seed_target,target_wrong_bounds=[target_counts['wrong']/den,(target_counts['wrong']+absent)/den],all_locations=allcounts,mean_loss_bounds=[loss/20,(loss+allcounts['unobserved'])/20],after_target_receipt=post,unexposed_known_wrong_consensus=len(votes)==den and len(set(votes))==1 and votes[0] not in ('UNKNOWN',w['truth'][target]),selected=t['selected'],slot=t['slot']))
 inspected=[t['selected'] for t in episode['turns'] if t['selected'] is not None]
 # Use actual slot times, not compacted successful-inspection indices.
 target_slots=[t['time']+1 for t in episode['turns'] if t['selected']==target]
 return dict(timeline=timelines,assigned=15,valid=sum(e['status']=='valid' for t in episode['turns'] for e in t['entries']),unique_coverage=len(set(inspected)),repeat_slots=sum(t['slot']=='repeat' for t in episode['turns']),failed_slots=sum(t['slot']=='failed' for t in episode['turns']),first_target_inspection=target_slots[0] if target_slots else None,target_inspection_censored=not bool(target_slots),inspection_horizon=2)

def contrast(episodes):
 if len(episodes)!=4 or len({e['world']['id'] for e in episodes})!=1 or any(e['world']!=episodes[0]['world'] for e in episodes):raise ValueError('paired_world')
 arms={(e['condition']['poison'],e['condition']['peers']):e for e in episodes}
 if len(arms)!=4:raise ValueError('missing_arm')
 def diff(a,b):return [a[0]-b[1],a[1]-b[0]]
 def endpoint(p,s):return arms[(p,s)]['summary']['timeline'][-1]['target_wrong_bounds']
 social=diff(endpoint(True,True),endpoint(False,True));isolated=diff(endpoint(True,False),endpoint(False,False))
 return dict(world_id=episodes[0]['world']['id'],poison_effect_with_peers_bounds=social,poison_effect_without_peers_bounds=isolated,collective_interaction_bounds=diff(social,isolated),interpretation='world-paired descriptive bounds; no population or mediation inference')
