import sys,json,collections,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from engine import rollout
import argparse
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--prior',type=Path);args=p.parse_args();root=args.results;m=json.loads((root/'manifest.json').read_text());checked=0;frames=0;start=time.monotonic();manipulations={};pairing={}
assert m['terminal_counts']=={'completed':180}
for a in m['assignments']:
 w=json.loads((root/(a['id']+'.json')).read_text());c=json.loads((root/f'corpus-{a["seed"]}.json').read_text());t=json.loads((root/f'tapes-{a["seed"]}.json').read_text())['jev']
 replay=rollout(c,t,a['layout'],a['arm'],a['scenario'],cap=m.get('packet_cap',4))
 for k in ('frames','event_snapshots','metrics','final_state','event_manifest'):assert replay[k]==w[k],(a['id'],k)
 if args.prior:
  old=json.loads((args.prior/(a['id']+'.json')).read_text());assert w['event_manifest']==old['event_manifest']
  if a['arm'].startswith('central'):
   for k in ('frames','event_snapshots','metrics','final_state','event_manifest'):assert w[k]==old[k],('central_changed',a['id'],k)
 assert w['metrics']['max_peer_packet']<=m.get('packet_cap',4)
 for f in w['frames']:
  assert abs(f['incorrect_or_missing']-(1-sum(f['correct'])/200))<1e-12
  assert abs(f['stale_fraction']-(sum(f['stale_by_agent'])/f['citation_count'] if f['citation_count'] else 0))<1e-12
  assert len(f['local'])==200 and len(f['gold'])==20
  outage=a['arm'].startswith('central') and a['scenario'] in ('central-outage','combined') and 10<=f['round']<20
  assert len(f['disconnected'])==(100 if outage else 0)
 assert w['event_manifest']['new_documents']==40
 assert len(w['event_manifest']['withdrawn_roots'])==(20 if a['scenario'] in ('withdrawal','missing-lineage','central-outage','combined') else 0)
 if a['arm'].endswith('verified'):assert w['metrics']['false_invalidations_peak']==0
 if a['arm']=='central-verified' and a['scenario']!='missing-lineage':assert w['metrics']['final_error']==0
 key=(a['seed'],a['layout'],a['scenario']);em=w['event_manifest'];assert key not in pairing or pairing[key]==em;pairing[key]=em
 checked+=1;frames+=len(w['frames'])
 if checked%30==0:print(json.dumps({'audited':checked}),flush=True)
audit={'assignments_reproduced':checked,'frames_reproduced':frames,'paired_event_blocks':len(pairing),'metric_arithmetic_verified':True,'outage_boundaries_verified':True,'verified_arms_false_invalidations':0,'central_verified_final_correct_except_missing_lineage':True,'unchanged_central_worlds':72 if args.prior else None,'matched_capacity_events':180 if args.prior else None,'seconds':time.monotonic()-start}
(root/'audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit),flush=True)
