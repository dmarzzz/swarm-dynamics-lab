"""Offline public-evidence paired construction and explicit guard, no native calls."""
import copy,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'controller-study'))
import cases,public_reference

def roots():
    result=[]
    for i,role in enumerate(('gateway','worker','store')):
        for j,configuration in enumerate(('legacy','expanded')):
            root=f'{role}-{configuration}';base=cases.make('healthy_expanded' if j else 'healthy',31001+i*100+j)
            old=copy.deepcopy(base['initial']['probe']);old['epoch']-=1;old['live'][role]=False;old['checks']['processes_live']=False
            for branch in ('confirmed','contradicted'):
                c=copy.deepcopy(base);c.update(id=root+'-'+branch,root=root,branch=branch,target_role=role,older_report=copy.deepcopy(old))
                if branch=='confirmed':c['kind']=role+'_crash';c['initial']['live'][role]=False
                c['initial']['probe']={'epoch':c['initial']['epoch'],'checks':cases.f.health(c['fixture'],c['initial']),'live':copy.deepcopy(c['initial']['live'])}
                result.append(c)
    return result

def observation(c,state,tick,history):
    # Fixed action/result facts only, not previous prose; identical history contract in both arms.
    history=[{'proposed_action':{k:v for k,v in h['proposal'].items() if k!='reason'},'executed_action':{k:v for k,v in h['action'].items() if k!='reason'},'result':h['result']} for h in history]
    o=cases.observe(c,state,tick,history,[])
    def record(body):
        digest=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
        return {'source':'service-monitor','source_id':'report-'+digest[:16],'sha256':digest,'observation':copy.deepcopy(body)}
    old=record(c['older_report']);current=record(o['cached_probe']);current['supersedes_source_id']=old['source_id'];o['report_lineage']={'older':old,'latest_available':current}
    return o

def admission(o,action):
    if action['action']!='deploy':return True,'non_deploy'
    d=public_reference.labels(o)
    if not d['probe_current']:return False,'current_liveness_required'
    if d['failed_service']!=action['service']:return False,'target_not_currently_observed_failed'
    candidate=copy.deepcopy(o);candidate['deployed'][action['service']]=action['version'];checks=public_reference.labels(candidate)
    if not all(checks[k] for k in ('rpc_compatible','data_readable','storage_format','requested_feature')):return False,'proposed_configuration_incompatible'
    return True,'current_failure_and_compatible_target'

def step(c,state,proposal,o,guarded):
    before=all(cases.f.health(c['fixture'],state).values());allowed,why=admission(o,proposal) if guarded else (True,'unguarded')
    executed=proposal if allowed else cases.f.action('wait',reason='Guard denied deployment; tick consumed, no substituted repair')
    frame=cases.f.step(c['fixture'],state,executed)
    frame.update(proposal=copy.deepcopy(proposal),guarded=guarded,guard_allowed=allowed,guard_reason=why,guard_denied=int(not allowed),served_opportunity=int(before and executed['action']!='deploy'),unnecessary_proposed=int(before and proposal['action']=='deploy'),unnecessary_executed=int(before and executed['action']=='deploy'))
    if not allowed:frame['result']='Deployment rejected by public-evidence guard: '+why
    return frame

def summarize(c,trace):
    deployed=[i for i,x in enumerate(trace) if x['action']['action']=='deploy' and not x['rejected']]
    verified=any(j>i and x['action']['action']=='inspect' and x['state']['probe']['epoch']==x['state']['epoch'] and all(x['state']['probe']['checks'].values()) for i in deployed for j,x in enumerate(trace))
    return {'post_state_gate':cases.gate(c,trace),'proposal_contract_pass':cases.gate(c,trace) and not any(x['guard_denied'] or x['rejected'] or x['unnecessary_proposed'] for x in trace),'proposal_restraint_pass':not any(x['unnecessary_proposed'] for x in trace),'served_opportunities':sum(x['served_opportunity'] for x in trace),'unnecessary_proposed':sum(x['unnecessary_proposed'] for x in trace),'unnecessary_executed':sum(x['unnecessary_executed'] for x in trace),'guard_denials':sum(x['guard_denied'] for x in trace),'missed_repair':int(c['branch']=='confirmed' and not trace[-1]['healthy']),'post_action_verified':verified if deployed else None}

def simulate(c,guarded,policy=public_reference.choose):
    state=copy.deepcopy(c['initial']);trace=[];history=[]
    for tick in (1,2):
        o=observation(c,state,tick,history);raw=policy(o);proposal=cases.f.controller.decode(c['fixture'],raw);x=step(c,state,proposal,o,guarded);x.update(tick=tick,observation=o);trace.append(x);history.append({'proposal':proposal,'action':x['action'],'result':x['result']})
    return trace,summarize(c,trace)
if __name__=='__main__':
    rows=[]
    for c in roots():
        for guarded in (False,True):
            _,s=simulate(c,guarded);rows.append({'root':c['root'],'branch':c['branch'],'guarded':guarded,**s})
    assert all(r['post_state_gate'] and r['proposal_restraint_pass'] and not r['missed_repair'] for r in rows)
    print(json.dumps({'native_calls':0,'kind':'offline_rule_comparator','paired_roots':6,'branch_worlds':12,'rows':rows},indent=2))
