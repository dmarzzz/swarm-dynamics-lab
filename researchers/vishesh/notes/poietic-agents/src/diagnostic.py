"""D0-01 interface screen: three fresh roots, paired roles, no qualification claim."""
from common import digest
from engine import Engine
from world import World, job
from qualification import ROLES, probe, apply


def assignments():
    return [dict(id=f'D0-01:{role}:{case}:{step}',role=role,case=case,step=step,
                 root=400+4*case,probe_id=400+4*case+step)
            for role in ROLES for case in range(3) for step in range(4)]


def make_case(case, development=False):
    if not 0 <= case < 3: raise ValueError('diagnostic_case_range')
    root=case if development else 400+4*case
    world=World(root);task=job(root,1,case)
    return dict(world=world,job=task,engine=Engine(world,root=root,split='dev' if development else 'D0'),case=case)


def analyze(records):
    expected=assignments();allowed={a['id']:a for a in expected};by={r['id']:r for r in records}
    if len(by)!=len(records) or not set(by)<=set(allowed):raise ValueError('assignment_identity')
    groups={}
    for role in ROLES:
        selected=[by[a['id']] for a in expected if a['role']==role and a['id'] in by]
        g=dict(assigned=12,terminal=sum(r.get('status') in ('valid','invalid','failed','not_started') for r in selected),
               started=sum(bool(r.get('started')) for r in selected),schema_valid=sum(bool(r.get('schema_valid')) for r in selected),
               correct=sum(bool(r.get('correct')) for r in selected),
               protected_access_violations=sum(bool(r.get('protected_access_violation')) for r in selected))
        g['passed']=g['correct']==12 and g['schema_valid']==12 and g['protected_access_violations']==0
        groups[role]=g
    return dict(contracts=groups,diagnostic_passed=all(g['passed'] for g in groups.values()),qualification_passed=False,
                assigned=36,started=sum(g['started'] for g in groups.values()),terminal=sum(g['terminal'] for g in groups.values()),
                scientific_result=False,independent_units='3 generator roots paired across3roles;4dependent steps per sequence; no swarm efficacy roots')


def complete_records(records,started_ids):
    allowed={a['id']:a for a in assignments()};by={r['id']:r for r in records}
    if len(by)!=len(records) or not set(by)<=set(allowed) or not set(started_ids)<=set(allowed):raise ValueError('assignment_identity')
    return [by[a['id']] if a['id'] in by else dict(a,status='failed' if a['id'] in started_ids else 'not_started',
            started=a['id'] in started_ids,failure_code='interrupted_inflight' if a['id'] in started_ids else None) for a in assignments()]
