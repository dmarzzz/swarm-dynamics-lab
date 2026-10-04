"""Prepare new private evaluation roots; no inspection or native dispatch."""
from pathlib import Path
import argparse,json,secrets,hashlib
import admission as a
from development import dev_world

def freeze(destination,q3_path):
 root=Path(destination);root.mkdir(exist_ok=False)
 prior=json.loads(Path(q3_path).read_text());assignments={};used={x['world']['seed'] for x in prior['assignments']}
 assignments['Q3-A2']=[{'family':x['family'],'world':x['world'],'reuse':'Q3 qualification; not held-out evaluation'} for x in prior['assignments']]
 for stage in ('P1','P2'):
  rows=[]
  for family in ('release','failover','delegation'):
   seed=secrets.randbits(52)
   while seed<2**40 or seed in used:seed=secrets.randbits(52)
   used.add(seed);rows.append({'world_id':stage+'-'+family,'family':family,'world':dev_world(seed),'repeats':[0,1]})
  assignments[stage]=rows
 packet={'lineage':'R3','assignments':assignments,'max_calls':{'Q3-A2':108,'P1':828,'P2':828},'arms':['interactive','static','broken','retained'],'automatic_successor':False}
 path=root/'manifest.json';path.write_text(json.dumps(packet,sort_keys=True));path.chmod(0o600)
 summary={'manifest_sha256':a.digest(packet),'prior_Q3_packet_sha256':a.digest(prior),'Q3_worlds_reused':3,'P1_new_worlds':3,'P2_new_worlds':3,'fresh_executions_per_world':2,'independent_templates':3,'seeds_and_cases_private':True,'native_calls':0,'native_scheduler_ready':False,'stage_source_sha256':a.source_hash(),'assignment_digests':{k:a.digest(v) for k,v in assignments.items()}}
 return summary
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--destination',required=True);p.add_argument('--prior-q3',required=True);args=p.parse_args();print(json.dumps(freeze(args.destination,args.prior_q3),indent=2))
