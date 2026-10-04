"""One fresh paced cheap-role screen; exact Q30-03 actor contract is reused."""
from q30v3 import Swarm, models, probe, apply, wire, World, job
from common import digest
ROLES=('cheap_generative',)

def assignments():
    return [dict(id=f'Q30-04:{r}:{c}:{s}',role=r,case=c,step=s,root=1000+4*c) for r in ROLES for c in range(12) for s in range(4)]

def make_case(case,development=False):
    if not 0<=case<12:raise ValueError('case_range')
    root=case if development else 1000+4*case;world=World(root)
    return dict(world=world,job=job(root,1,case),engine=Swarm(world,root=root,split='dev' if development else 'Q30-04'),case=case)

def analyze(records):
    allowed={x['id']:x for x in assignments()};by={r['id']:r for r in records}
    if len(by)!=len(records) or not set(by)<=set(allowed):raise ValueError('assignment_identity')
    groups={}
    for role in ROLES:
        rows=[by[x['id']] for x in allowed.values() if x['role']==role and x['id'] in by]
        g={k:sum(bool(r.get(field)) for r in rows) for k,field in [('started','started'),('schema_valid','schema_valid'),('correct','correct'),('protected_access_violations','protected_access_violation')]}
        g.update(assigned=48,terminal=sum(r.get('status') in ('valid','invalid','failed','not_started') for r in rows));g['passed']=g['schema_valid']==48 and g['correct']>=44 and not g['protected_access_violations'];groups[role]=g
    return dict(attempt='Q30-04',contracts=groups,assigned=48,started=sum(g['started'] for g in groups.values()),terminal=sum(g['terminal'] for g in groups.values()),qualification_passed=all(g['passed'] for g in groups.values()),scientific_result=False)

def complete_records(records,started_ids):
    allowed={x['id']:x for x in assignments()};by={r['id']:r for r in records}
    if len(by)!=len(records) or not set(by)<=set(allowed) or not set(started_ids)<=set(allowed):raise ValueError('assignment_identity')
    return [by.get(x['id'],dict(x,status='failed' if x['id'] in started_ids else 'not_started',started=x['id'] in started_ids)) for x in allowed.values()]
