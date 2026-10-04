"""Pure development cases. No provider, credential, sealed input or native collection."""
from pathlib import Path
import sys,json,itertools,random,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import instrument as i,native as n

def dev_world(seed):
 w=i.world(seed,6);order=list(range(6));random.Random(seed).shuffle(order);order[0],order[1]=order[1],order[0]
 labels=w['members'];w['changed_routes']={labels[x]:[labels[order[(j-1)%6]],labels[order[(j+1)%6]]] for j,x in enumerate(order)}
 return w

def demonstrations(w,owner):
 peers=[p for p in w['members'] if p!=owner];rows=[]
 for index,veto in enumerate([None]+peers):
  case=f'episode-{index}';rs=[i.receipt(owner,p,case,0,p!=veto) for p in peers]
  rows.append({'case':case,'epoch':0,'receipts':rs,'outcome':i.reference(w['routes'][owner],rs,owner,case,0)})
 return rows

def infer(owner,peers,episodes):
 return [list(pair) for pair in itertools.combinations(peers,2) if all(i.reference(pair,e['receipts'],owner,e['case'],e['epoch'])==e['outcome'] for e in episodes)]

def validate():
 sizes=[];units=0;order_checks=0;strata=[]
 for seed in range(7300,7320):
  w=dev_world(seed);rng=random.Random(seed)
  strata.append(sum(set(w['routes'][p])!=set(w['changed_routes'][p]) for p in w['members']))
  for owner in w['members']:
   demos=demonstrations(w,owner);matches=infer(owner,[p for p in w['members'] if p!=owner],demos)
   assert len(matches)==1 and set(matches[0])==set(w['routes'][owner]);assert all('authorized_witnesses' not in e for e in demos)
   packet,cases=n.founder_packet(w,owner);scoped=[{'case':e['case'],'epoch':e['epoch'],'receipts':[{'witness':r['witness'],'allow':r['allow']} for r in e['receipts']],'outcome':e['outcome']} for e in demos]
   expanded=[{'case':e['case'],'epoch':e['epoch'],'receipts':[i.receipt(owner,r['witness'],e['case'],e['epoch'],r['allow']) for r in e['receipts']],'outcome':e['outcome']} for e in scoped]
   assert expanded==demos
   packet['current_observations']=scoped
   rng.shuffle(packet['tests'])
   for e in packet['tests']:rng.shuffle(e['receipts'])
   wire=n.request('learn',packet)
   wire['messages'][0]['content']+=' In founder current_observations only, each receipt inherits owner from your position and case/epoch from its enclosing episode. Its witness and allow fields remain explicit. Test receipts retain full metadata.'
   size=i.packet_bytes(wire);sizes.append(size)
   for c in cases:
    rows=copy.deepcopy(c['receipts']);rng.shuffle(rows);assert i.reference(matches[0],rows,owner,c['case'],c['epoch'])==c['truth'];order_checks+=1
   units+=1
 result={'evidence_type':'offline development only','generated_development_worlds':20,'founder_contracts_checked':units,'unique_inferred_policies':units,'permutation_truth_checks':order_checks,'maximum_founder_request_bytes':max(sizes),'candidate6500byte_fit':max(sizes)<=6500,'changed_routes_per_world':sorted(set(strata)),'unchanged_routes_per_world':sorted({6-n for n in strata}),'native_calls':0,'sealed_inputs_opened':False,'domain_families_validated':False,'nuisance_joint_channel_implemented':False,'qualification_max_calls':36,'evaluation_max_calls':2304,'maximum_additional_usd':54.001,'maximum_cumulative_usd':55.1647270437}
 Path(__file__).with_name('DEVELOPMENT-VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':validate()
