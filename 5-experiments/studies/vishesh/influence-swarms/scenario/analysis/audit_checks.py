"""Saved-data reconciliation independent of dispatch; never makes provider calls."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from candidate_checks import ARMS,FIELDS,digest,evaluate,execution_gate,source_checks,source_score,source_signature

def audit(root):
 root=Path(root);s=json.loads((root/'summary.json').read_text());m=json.loads((root/'manifest.json').read_text());rows=json.loads((root/'outcomes.json').read_text());aa=json.loads((root/'audit.json').read_text());cost=0.;usage_calls=0;cases=[]
 assert digest(rows)==s['outcomes_hash'];assert len(rows)==s['planned']==s['terminal'];assert s['source_signature']==m['source_signature']
 for i,a in enumerate(aa):
  case=json.loads((root/f'case-{i}.json').read_text());events=[json.loads(x) for x in (root/f'events-{i}.jsonl').read_text().splitlines()];reqs={e['call']:e for e in events if e['kind']=='request'};responses={e['call']:e for e in events if e['kind']=='response'};source,acceptable=source_score(case);assert source_checks(case)==a['source_checks']
  for e in events:
   if e['kind'] in ('response','call_error'):cost+=e['usage']['actual_usd'];usage_calls+=e['usage']['calls']
  for q in reqs.values():
   assert digest(q['request'])==q['request_hash'];assert not any(k in q['request']['observation'] for k in ('evaluator','truth_hash','scorecard','acceptable','source_checks'))
  reviews={q['diagnostic_arm']:q['request'] for q in reqs.values() if q['diagnostic_arm'].endswith('_review')}
  if s['stage']=='D3':assert reviews['matrix_review']['observation']==reviews['narrative_review']['observation']
  chairs={q['diagnostic_arm']:q['request'] for q in reqs.values() if not q['diagnostic_arm'].endswith('_review')}
  if all(k in chairs for k in ARMS[1:]):assert chairs['matrix_standard']['observation']==chairs['matrix_consistent']['observation']
  matrix=a['matrix'];correct=sum(matrix['candidate_checks'][n][f]==a['source_checks'][n][f] for n in case['candidates'] for f in FIELDS) if matrix else 0;assert correct==a['matrix_correct']
  choices={}
  for r in [r for r in rows if r['case_id']==case['case_id']]:
   if not r['valid']:continue
   assert bool(r['evaluation']['acceptable_decision'])==(r['decision']['choice'] in acceptable)
   for n,score in source.items():assert score['feasible']==r['evaluation']['scorecard'][n]['feasible'];assert abs(score['total']-r['evaluation']['scorecard'][n]['total'])<.011
   if r['guarded_choice']:
    assert r['guarded_choice']==execution_gate(r['decision']['choice'],matrix)
    assert bool(r['guarded_evaluation']['acceptable_decision'])==(r['guarded_choice'] in acceptable)
   choices[r['arm']]=r['decision']['choice']
  cases.append({'case_id':case['case_id'],'source_acceptable':acceptable,'matrix_correct':correct,'choices':choices,'source_scorecard':source})
 assert abs(cost-s['actual_usd'])<1e-8;assert usage_calls==s['calls'];assert sum(a['matrix_correct'] for a in aa)==s['matrix_correct']
 pairs=[]
 for case in cases:
  rr={r['arm']:r for r in rows if r['case_id']==case['case_id']};diff={}
  for a,b in [('narrative_standard','matrix_standard'),('matrix_standard','matrix_consistent')]:
   if a in rr and b in rr:diff[b+' minus '+a]=int(rr[b]['evaluation']['acceptable_decision'])-int(rr[a]['evaluation']['acceptable_decision']) if rr[a]['valid'] and rr[b]['valid'] else None
  pairs.append({'case_id':case['case_id'],**diff})
 return {'source_grades_agree':True,'matched_observations':True,'usage_reconciles':True,'reported_cost':cost,'calls':usage_calls,'cases':cases,'paired_differences':pairs,'limits':'Owner-authored saved-data audit using Decimal source arithmetic; not independent researcher certification.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('out');a=p.parse_args();Path(a.out).write_text(json.dumps(audit(a.root),indent=2)+'\n')
