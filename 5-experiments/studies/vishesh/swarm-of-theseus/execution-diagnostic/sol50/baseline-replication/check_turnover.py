"""Full independent development trajectory replay; never opens frozen holdouts."""
from pathlib import Path
import copy,json
import turnover,contract,test_q3
from development import dev_world

def check():
 count=0;maximum=0;records=[]
 for family in ('release','failover','delegation'):
  for seed in (8800,8801):
   for repeat in (0,1):
    saved=[]
    def caller(fam,phase,p,condition):
     nonlocal maximum,count
     request=contract.wire(phase,fam,p);maximum=max(maximum,len(json.dumps(request,separators=(',',':')).encode()));count+=1
     if phase=='commit' and 'broken' in condition:value={'note':{'witnesses':[x['position'] for x in p['roster'] if x['position']!=p['position']][:2]}}
     else:value=test_q3.oracle(fam,phase,p,condition)
     saved.append((fam,phase,condition,request,copy.deepcopy(value)));return value
    w=dev_world(seed);result=turnover.trajectory(w,family,caller);assert result['complete'] and len(saved)<=138
    index=0
    def replay(fam,phase,p,condition):
     nonlocal index
     old=saved[index];index+=1;assert old[:3]==(fam,phase,condition) and old[3]==contract.wire(phase,fam,p);return copy.deepcopy(old[4])
    assert turnover.trajectory(w,family,replay)==result and index==len(saved)
    records.append({'family':family,'development_seed':seed,'scripted_repeat':repeat,'calls':len(saved),'complete':True,'exact_replay':True})
 return {'evidence_type':'scripted software fixture,not native replication','trajectories':len(records),'scripted_calls':count,'max_calls_per_trajectory':max(x['calls'] for x in records),'maximum_request_bytes':maximum,'replay_disagreements':0,'native_calls':0,'sealed_holdouts_opened':False,'records':records}
if __name__=='__main__':
 value=check();Path(__file__).with_name('TURNOVER-OFFLINE.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:v for k,v in value.items() if k!='records'}))
