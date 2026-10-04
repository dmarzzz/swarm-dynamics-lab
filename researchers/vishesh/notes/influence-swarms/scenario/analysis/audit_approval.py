"""Post-run audit: Decimal source arithmetic and matched-request/cost accounting.

Arithmetic derivation adapted from dmarz's independent Q4 review; this application
to D2 is the owning author's audit, not another researcher sign-off.
"""
import argparse,copy,json,re
from decimal import Decimal as D
from pathlib import Path
ARMS=('team_ballots','team_evidence','solo','general_review','approval_review')
def source_score(case):
 b=case['brief'];rows={}
 for name in case['candidates']:
  docs={prefix:next(d['text'] for d in case['documents'] if d['id'].startswith(prefix) and d['title'].startswith(name+' ')) for prefix in ('quote','pilot','scope','rollout')}
  seat,unit,setup=map(D,re.findall(r'\$(\d+(?:\.\d+)?)',docs['quote']));simple,complex_=map(D,re.findall(r'(\d+) of 100',docs['pilot']));mix=D(str(b['complex_share']));rate=((1-mix)*simple+mix*complex_)/100;volume=D(b['monthly_tickets']*12)
  software=D(b['seats']*12)*seat+volume*rate*unit+setup;labor=volume*(1-rate)*D(b['human_cost_per_unresolved_ticket']);days=sum(map(int,re.findall(r'(\d+) days',docs['rollout'])[:3]))
  feasible=('storage region EU;' in docs['scope'] and 'processing region EU.' in docs['scope'] and days<=b['deadline_days'] and software<=b['software_budget_usd'] and rate>=D(str(b['minimum_automation'])) and 'SSO included: True' in docs['quote'] and 'complete export: True' in docs['quote'])
  rows[name]={'automation':float(rate),'software':float(software),'total':float(software+labor),'days':days,'feasible':feasible}
 feasible=[r['total'] for r in rows.values() if r['feasible']];minimum=min(feasible) if feasible else None
 acceptable=[n for n,r in rows.items() if r['feasible'] and r['total']<=minimum*(1+b['cost_tolerance_fraction'])] or ['DEFER']
 return rows,acceptable

def analyze(root):
 root=Path(root);summary=json.loads((root/'summary.json').read_text());outcomes=json.loads((root/'outcomes.json').read_text());case_audits=[];workflow={a:{'standalone_usd':0.,'standalone_calls':0,'recorded_call_seconds':0.,'acceptable':0,'valid':0} for a in ARMS};total_usage=0.;requests_total=responses_total=0
 for path in sorted(root.glob('case-*.json'),key=lambda x:int(x.stem.split('-')[1])):
  case=json.loads(path.read_text());i=path.stem.split('-')[1];events=[json.loads(s) for s in (root/f'events-{i}.jsonl').read_text().splitlines()];computed,acceptable=source_score(case);selected=[r for r in outcomes if r['case_id']==case['case_id']];reqs={e['call']:e for e in events if e['kind']=='request'};responses={e['call']:e for e in events if e['kind']=='response'};requests_total+=len(reqs);responses_total+=len(responses)
  for r in selected:
   if r['valid']:
    assert bool(r['evaluation']['acceptable_decision'])==(r['decision']['choice'] in acceptable)
    assert set(r['evaluation']['acceptable'])==set(acceptable)
    for name,values in computed.items():
     score=r['evaluation']['scorecard'][name];assert score['feasible']==values['feasible'];assert abs(score['total']-values['total'])<.011
  for q in reqs.values():
   obs=q['request']['observation'];assert not any(k in obs for k in ('evaluator','truth_hash','scorecard','acceptable'))
  extra={arm:[q['request'] for q in reqs.values() if q.get('diagnostic_arm')==arm] for arm in ('general_review','approval_review')}
  matched=False
  if all(extra.values()):
   matched=extra['general_review'][0]['observation']==extra['approval_review'][0]['observation'];assert matched
  prefix_usd=prefix_calls=prefix_seconds=0;solo=False;review_lengths={};reviews={};chair_only={}
  for call,q in reqs.items():
   response=responses.get(call);obs=q['request']['observation'];arm=q.get('diagnostic_arm')
   if not arm and obs.get('role')=='generalist':solo=True
   if not response:continue
   u=response['usage'];cost=u['actual_usd'];calls=u['calls'];total_usage+=cost;seconds=response['elapsed_seconds']-q['elapsed_seconds']
   if arm:
    workflow[arm]['standalone_usd']+=cost;workflow[arm]['standalone_calls']+=calls;workflow[arm]['recorded_call_seconds']+=seconds
    if obs['phase']=='initial':
     reviews[arm]=response['answer'];review_lengths[arm]=sum(len(f['claim']) for f in response['answer']['findings'])
   elif solo:workflow['solo']['standalone_usd']+=cost;workflow['solo']['standalone_calls']+=calls;workflow['solo']['recorded_call_seconds']+=seconds
   elif obs['phase']=='chair':
    chair_arm='team_ballots' if 'choice' in obs['reports'][0] else 'team_evidence';workflow[chair_arm]['standalone_usd']+=cost;workflow[chair_arm]['standalone_calls']+=calls;workflow[chair_arm]['recorded_call_seconds']+=seconds
   else:prefix_usd+=cost;prefix_calls+=calls;prefix_seconds+=seconds
  for arm in ARMS:
   if arm!='solo':workflow[arm]['standalone_usd']+=prefix_usd;workflow[arm]['standalone_calls']+=prefix_calls;workflow[arm]['recorded_call_seconds']+=prefix_seconds
   row=next(r for r in selected if r['arm']==arm);workflow[arm]['valid']+=int(row['valid']);workflow[arm]['acceptable']+=row['evaluation']['acceptable_decision'] if row['valid'] else 0
  case_audits.append({'case_id':case['case_id'],'source_scorecard':computed,'source_acceptable':acceptable,'matched_review_observations':matched,'review_claim_characters':review_lengths,'candidate_name_coverage':{arm:{name:sum(bool(re.search(r'\b'+re.escape(name)+r'\b',f['claim'])) for f in review['findings']) for name in case['candidates']} for arm,review in reviews.items()},'reviews':reviews,'choices':{r['arm']:r['decision']['choice'] if r['valid'] else 'INVALID' for r in selected}})
 assert len(outcomes)==summary['planned']==30;assert abs(total_usage-summary['actual_usd'])<1e-8
 return {'grader_agreement':True,'matched_review_observations':all(c['matched_review_observations'] for c in case_audits),'assigned':30,'terminal':len(outcomes),'recorded_requests':requests_total,'recorded_responses':responses_total,'usage_reconciles':True,'actual_usd':total_usage,'workflow_costs':workflow,'cases':case_audits,'limits':'Owning-author audit, adapted from independent Q4 Decimal probe. Standalone workflow costs duplicate common prefix for practical comparison; do not sum them as collection spend. Six authored clusters; no population inference.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('out');a=p.parse_args();Path(a.out).write_text(json.dumps(analyze(a.root),indent=2)+'\n')
