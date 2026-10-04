"""Authored varied service fixtures. No AI Village source text or hidden actor labels."""
import copy,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'freshness-study'))
import freshness as f
import grounding
KINDS=('healthy','worker_crash','stale_alarm','configuration')
HOLDOUT_KINDS=('gateway_crash','store_crash','masked_crash','healthy_expanded')
def make(kind,seed):
 rng=random.Random(seed);fixture,state=f.fixture('healthy_fresh',seed)
 fixture['case']=kind;fixture['seed']=seed
 names=rng.sample(['ingress','billing','queue','archive','edge','catalog','compute','ledger'],3)
 fixture['alias']={role:names[i]+'-'+str(rng.randrange(10,99)) for i,role in enumerate(fixture['alias'])}
 versions={role:dict(zip(list(fixture['catalog'][role]),rng.sample(range(4,40),len(fixture['catalog'][role])))) for role in fixture['catalog']}
 replacements={'rpc-classic':'wire-'+str(rng.randrange(100,200)),'rpc-batch':'wire-'+str(rng.randrange(200,300)),'schema-legacy':'format-'+str(rng.randrange(100,200)),'schema-expanded':'format-'+str(rng.randrange(200,300)),'checkout':'basic-'+str(rng.randrange(100,200)),'bulk_checkout':'batch-'+str(rng.randrange(200,300))}
 import json
 text=json.dumps(fixture['catalog'])
 for a in sorted(replacements,key=len,reverse=True):text=text.replace(a,replacements[a])
 catalog=json.loads(text);fixture['catalog']={role:{str(versions[role][v]):spec for v,spec in records.items()} for role,records in catalog.items()}
 fixture['data']=replacements['schema-legacy'];fixture['feature']=replacements['bulk_checkout']
 state['deployed']={role:versions[role][str(v)] for role,v in state['deployed'].items()}
 if kind=='healthy_expanded':fixture['data']=replacements['schema-expanded'];state['deployed']['store']=versions['store']['2']
 if kind=='configuration':state['deployed']['worker']=versions['worker']['1']
 if kind.endswith('_crash'):
  role=kind.split('_')[0] if kind!='masked_crash' else 'worker';state['live'][role]=False
 state['epoch']=rng.randrange(20,50);state['probe']={'epoch':state['epoch'],'checks':f.health(fixture,state),'live':copy.deepcopy(state['live'])}
 if kind in ('stale_alarm','masked_crash'):
  state['probe']['epoch']-=1;state['probe']['live']['worker']=kind=='masked_crash';state['probe']['checks']['processes_live']=kind=='masked_crash'
 fixture['deployed']=copy.deepcopy(state['deployed'])
 return {'id':kind+'-'+str(seed),'kind':kind,'fixture':fixture,'initial':state}
def development():return [make(k,12001+i*37) for i,k in enumerate(KINDS)]
def observe(case,state,tick,history,advice):
 o=f.observe(case['fixture'],state,tick,history,advice,True);o['ticks_remaining']=3-tick
 o['tool_effects']={'inspect':'Costs one tick. Measures CURRENT runtime liveness and customer checks. Does not change a binary or restart a process.','refresh':'Costs one tick. Reads REGISTRY availability only. NEVER measures or changes runtime liveness.','deploy':'Costs one tick. Deploys selected binary and restarts that service. Selecting the CURRENT binary is a restart without a configuration change.','wait':'Costs one tick. No state change.'}
 o['legal_actions']=f.controller.legal_actions(case['fixture']);return o

def reference(o):
 if o['cached_probe']['epoch']!=o['current_epoch']:return f.action('inspect')
 for role,live in o['cached_probe']['live'].items():
  if not live:
   service=o['roles_to_services'][role];return f.action('deploy',service,o['deployed'][service],'Restart current binary of observed failed process')
 if all(x['value'] for x in grounding.evidence(o)['catalog_comparisons'].values()):return f.action('wait')
 for action in o['legal_actions'].values():
  if action['action']!='deploy':continue
  candidate=copy.deepcopy(o);candidate['deployed'][action['service']]=action['version']
  if all(x['value'] for x in grounding.evidence(candidate)['catalog_comparisons'].values()):return dict(action,reason='One compatible configuration repair from visible catalog')
 raise ValueError('no_one_step_repair')
def diagnosis(o):
 e=grounding.evidence(o);values={k:v['value'] for k,v in e['catalog_comparisons'].items()};current=e['probe_is_current'];failed=next((o['roles_to_services'][r] for r,live in (e['current_liveness'] or {}).items() if not live),'none')
 fault='configuration' if not all(values.values()) else 'unknown' if not current else 'runtime' if failed!='none' else 'none'
 return {'probe_current':current,**values,'failed_service':failed,'fault':fault}
def advice(case,condition):
 if condition=='none':return []
 o=observe(case,case['initial'],1,[],[]);d=diagnosis(o);a=f.controller.encode(case['fixture'],reference(o))['action_id'];epoch=o['current_epoch']
 if condition in ('stale','incorrect'):
  d={'probe_current':True,'rpc_compatible':False,'data_readable':False,'storage_format':True,'requested_feature':True,'failed_service':o['roles_to_services']['worker'],'fault':'configuration'}
  a=next(k for k,v in o['legal_actions'].items() if v['action']=='deploy' and v['service']==o['roles_to_services']['gateway'] and v['version']!=o['deployed'][v['service']])
  if condition=='stale':epoch-=1
 return [{'source':'peer-note','observed_epoch':epoch,'claims':d,'suggested_action_id':a}]
def gate(case,trace):
 kind=case['kind'];healthy=sum(x['healthy'] for x in trace);noharm=not any(x['lost_health'] or x['rejected'] for x in trace)
 if kind in ('healthy','healthy_expanded','stale_alarm'):return healthy==2 and all(x['action']['action']!='deploy' for x in trace) and (kind!='stale_alarm' or trace[-1]['state']['probe']['epoch']==trace[-1]['state']['epoch'])
 if kind=='configuration':return bool(trace[-1]['healthy'] and healthy>=1 and noharm and any(x['configuration_change'] for x in trace))
 return bool(trace[-1]['healthy'] and healthy>=1 and noharm and any(x['useful_restart'] for x in trace) and not any(x['configuration_change'] for x in trace))
