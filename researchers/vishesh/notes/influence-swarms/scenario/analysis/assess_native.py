"""Reconcile native decisions and describe paired contrasts without pseudo-N."""
import argparse,json,collections
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('out');a=p.parse_args();base=Path(a.run)
rows=json.loads((base/'outcomes.json').read_text());summary=json.loads((base/'summary.json').read_text());groups=collections.defaultdict(dict)
for r in rows:groups[(r['case_id'],r['world'])][r['arm']]=r
pairs=[]
for (case,world),arms in groups.items():
 b,e=arms.get('team_ballots'),arms.get('team_evidence')
 if b and e:
  valid=b['valid'] and e['valid'];pairs.append({'case':case,'world':world,'both_valid':valid,
   'same_choice':b['decision']['choice']==e['decision']['choice'] if valid else None,
   'ballots_minus_evidence_harm':b['evaluation']['harmful_target']-e['evaluation']['harmful_target'] if valid else None})
report={'summary':summary,'case_worlds':len(groups),'distinct_buyers':len({r['case_id'] for r in rows}),'paired_chairs':pairs,
 'per_arm':{arm:{'assigned':len(rs),'valid':sum(r['valid'] for r in rs),'acceptable':sum(r['evaluation']['acceptable_decision'] for r in rs if r['valid']),
                 'choices':[r['decision']['choice'] if r['valid'] else 'INVALID' for r in rs],
                 'absolute_cost_errors_usd':[r['evaluation']['cost_claim_error_usd'] for r in rs if r['valid']]}
            for arm,rs in ((arm,[r for r in rows if r['arm']==arm]) for arm in ('team_ballots','team_evidence','solo'))},
 'inference':'Descriptive paired pilot only. Shared prefixes and reused buyer worlds are not independent replicates. No p-value or population confidence interval.'}
Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
