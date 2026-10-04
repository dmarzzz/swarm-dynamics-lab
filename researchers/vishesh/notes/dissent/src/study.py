"""Reusable executor for an explicitly supplied policy; fixture runs are software tests.

No transport is installed here. Future approved native executors can inject a
strict provider after checking live registration, allocation and authorization.
"""
import json,time
from pathlib import Path
from cases import digest
from protocol import episode,summarize,actor_packet,majority,ARMS
from copy import deepcopy


def private_packets(case):
    """One initial observation per agent; no peer votes or challenge leakage."""
    packets=[]
    for evidence in sorted(case['evidence'],key=lambda e:e['id']):
        p=actor_packet(case);p['records']=[deepcopy(evidence)];p['votes']=[];p['challenge']=None
        packets.append(p)
    return packets


def collect_private(case, policy):
    """Produce an unselected initial team. Keeps unanimous/no-dissent cases."""
    votes=[]
    for packet in private_packets(case):
        result=policy('private',packet)
        if result not in ('PROCEED','HOLD','DEFER'):raise ValueError('invalid_private_action')
        votes.append(result)
    return votes


def natural_challenge_case(case, votes):
    c=deepcopy(case);records=sorted(c['evidence'],key=lambda e:e['id'])
    if len(votes)!=len(records):raise ValueError('private_vote_count')
    c['votes']=votes;initial=majority(votes)
    dissent=[(v,e) for v,e in zip(votes,records) if v!='DEFER' and v!=initial]
    if initial=='DEFER' or not dissent:c['challenge']=None
    else:
        # Predeclared stable first eligible witness; no evaluator selection.
        v,e=dissent[0]
        c['challenge']={'claim':'My observation conflicts with the initial action.','alternative':v,
                        'evidence_ids':[e['id']],'check':'independent-check','withdraw_if':initial,
                        'expires_at':c['task']['deadline']}
    return c


def execute(cases, arms, policy, out, *, origin='unit-test-fixtures', random_schedule=None):
    if origin not in ('unit-test-fixtures','externally-collected-response-tape'):
        raise ValueError('unsupported_origin')
    if any(a not in ARMS for a in arms):raise ValueError('unknown_arm')
    if 'matched-random' in arms and (not isinstance(random_schedule,dict) or set(random_schedule)!={c['case_id'] for c in cases} or any(type(v) is not bool for v in random_schedule.values())):
        raise ValueError('frozen_random_schedule_required')
    keys=[(c['case_id'],a) for c in cases for a in arms]
    if len(set(keys))!=len(keys):raise ValueError('duplicate_assignment')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    def write(name,value):
        tmp=out/(name+'.tmp');tmp.write_text(json.dumps(value,indent=2,allow_nan=False));tmp.replace(out/name)
    assignments=[{'case_id':c['case_id'],'arm':a,'status':'planned','decision_opportunities':len(c['frames']) or 1} for c in cases for a in arms]
    manifest={'schema':'right-dissenter-attempt-v1','origin':origin,'scientific_run':False,
              'plan_version':'RD-1','source_case_hash':digest(cases),'assignments':assignments,'random_schedule':random_schedule}
    write('manifest.json',manifest);records=[];write('records.json',records)
    for c in cases:
        for arm in arms:
            a=next(x for x in assignments if x['case_id']==c['case_id'] and x['arm']==arm)
            a['status']='started';write('manifest.json',manifest)
            start=time.monotonic()
            rows=episode(c,arm,policy,random_check=random_schedule[c['case_id']] if arm=='matched-random' else None)
            a.update(status='completed',terminal_decisions=len(rows),elapsed_seconds=time.monotonic()-start)
            # A policy failure is a terminal recorded outcome, not a missing assignment.
            records.extend(rows);write('records.json',records);write('manifest.json',manifest)
    expected=sum(a['decision_opportunities'] for a in assignments)
    if len(records)!=expected:raise ValueError('assignment_reconciliation_failed')
    report={'assigned':expected,'terminal':len(records),'unstarted':0,'outcomes':summarize(records),
            'by_arm':{a:summarize([r for r in records if r['arm']==a]) for a in arms},
            'mode':origin,'inference':'Software contract validation only; no empirical Jev effect.'}
    write('summary.json',report)
    return report


def audit_attempt(out):
    """Reconcile completed or interrupted attempts without dropping planned units."""
    out=Path(out);m=json.loads((out/'manifest.json').read_text())
    rows=json.loads((out/'records.json').read_text()) if (out/'records.json').exists() else []
    assigned=sum(a['decision_opportunities'] for a in m['assignments'])
    terminal=len(rows)
    known={(a['case_id'],a['arm']):a['decision_opportunities'] for a in m['assignments']}
    seen={}
    for row in rows:
        key=(row['case_id'],row['arm'])
        seen[key]=seen.get(key,0)+1
        if key not in known or seen[key]>known[key]:raise ValueError('unexpected_terminal_record')
    return {'assigned':assigned,'terminal':terminal,'missing':assigned-terminal,
            'correct_on_time_all_assigned':sum(r['correct_completion'] for r in rows)/assigned if assigned else None,
            'status':'reconciled' if terminal==assigned else 'incomplete'}
