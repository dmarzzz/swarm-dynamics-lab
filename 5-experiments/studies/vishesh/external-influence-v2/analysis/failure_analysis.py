"""Observable failure categories, not inferred mental states or causal effects."""
import argparse
import collections
import json
from pathlib import Path

def analyze(audit):
    rows=audit['episodes'];bad=[r for r in rows if not r['evaluation']['correct']]
    recovered=[r for r in bad if r['counterfactual_correct']]
    newly_wrong=[r for r in rows if r['evaluation']['correct'] and not r['counterfactual_correct']]
    return {'parent_run':audit['run'],'assigned':len(rows),'incorrect':len(bad),
            'wrong_but_recorded_rule_replay_correct':len(recovered),
            'correct_but_recorded_rule_replay_wrong':len(newly_wrong),
            'wrong_and_replay_still_wrong':sum(not r['counterfactual_correct'] for r in bad),
            'incorrect_by_domain':dict(collections.Counter(r['domain'] for r in bad)),
            'unexposed_agents_total':sum(r['evaluation']['unexposed_agents'] for r in rows),
            'attack_unexposed_observations':sum(r['evaluation']['unexposed_agents'] for r in rows if r['world'] in ('misleading','syndication')),
            'attack_unexposed_conversions':sum(r['evaluation']['unexposed_target_converts'] for r in rows if r['world'] in ('misleading','syndication')),
            'unexposed_target_conversions':sum(r['evaluation']['unexposed_target_converts'] for r in rows),
            'note':'Post-hoc replay of recorded estimates and check results; neither fresh model evidence nor a causal attribution. Categories can overlap with arithmetic, evidence extraction and objective misspecification.',
            'cases':[{'assignment':r['assignment'],'domain':r['domain'],'world':r['world'],'arm':r['arm'],
                      'chosen':r['choice'],'best_under_authored_rule':r['best'],'recorded_rule_choice':r['after_check_rule_choice'],
                      'target_votes_initial':r['evaluation']['target_votes_before'],'target_votes_revised':r['evaluation']['target_votes_after'],
                      'recorded_rule_recoverable':bool(r['counterfactual_correct']),
                      'citation_support':r['evaluation']['citation_support']} for r in bad]}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('audit');p.add_argument('out');a=p.parse_args()
    result=analyze(json.loads(Path(a.audit).read_text()));Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
