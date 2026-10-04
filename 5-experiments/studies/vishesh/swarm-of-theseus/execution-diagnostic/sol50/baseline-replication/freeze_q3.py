"""Create one untouched private Q3 packet; publish hashes only. No inference or allocation."""
from pathlib import Path
import argparse,json,secrets,hashlib,os
import admission as a
from development import dev_world

def freeze(destination):
 destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 if destination.exists():raise ValueError('freeze_exists')
 seeds=set()
 while len(seeds)<3:seeds.add(secrets.randbelow(2**52-2**40)+2**40)
 p={'attempt':a.ATTEMPT,'stage':'Q3','max_calls':108,'assignments':[{'family':family,'world':dev_world(seed)} for family,seed in zip(('release','failover','delegation'),sorted(seeds))]}
 a.validate_packet(p)
 with destination.open('x') as f:json.dump(p,f,sort_keys=True);f.flush();os.fsync(f.fileno())
 destination.chmod(0o600)
 record={'attempt':a.ATTEMPT,'stage':'Q3','packet_sha256':a.digest(p),'source_sha256':a.source_hash(),'assignments':[{'family':row['family'],'world_sha256':a.digest(row['world']),'members':6} for row in p['assignments']],'fresh_private_random_seeds':True,'development_inputs_reused':False,'native_calls':0,'max_calls':108,'model_cap_usd':'2.4462','infrastructure_cycle_cap_usd':'1','all_in_cap_usd':'3.4462','funding_decision':'PI-FUND-20261004-06','evaluation_inputs_generated':False}
 with (a.ROOT/'Q3-FREEZE.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
 print(json.dumps(record))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private-output',required=True);args=p.parse_args();freeze(args.private_output)
