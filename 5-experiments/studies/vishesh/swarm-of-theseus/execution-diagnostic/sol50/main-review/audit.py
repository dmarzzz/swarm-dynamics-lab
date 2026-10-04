"""Offline development audit only; never opens sealed evaluation inputs or calls a provider."""
from pathlib import Path
import sys,json,collections,copy
base=Path(__file__).resolve().parents[1];sys.path.insert(0,str(base))
import instrument as i, coordinator as c, native as n
from test_coordinator import SchedulingTests
w=i.world(321987,50);oracle=SchedulingTests().oracle(w);counts=collections.Counter();sizes=[]
def spy(phase,p):
 counts[phase]+=1;sizes.append(i.packet_bytes(n.request(phase,p)));return oracle(phase,p)
r=c.evaluate_world(w,spy)
changed=[p for p in w['members'] if set(w['routes'][p])!=set(w['changed_routes'][p])]
# Probe whether main dispatch enforces its declared teaching-message cap.
p=w['members'][0];g=i.Institution(w,'interactive',{x:i.note(x,w['routes'][x]) for x in w['members']});seen=[]
def oversized(phase,packet):
 if phase=='teach':return {'note':packet['private_note'],'explanation':'x'*1300}
 if phase=='commit':seen.append(packet['predecessor_message'])
 return oracle(phase,packet)
capacity_stop=False
try:h=c.replace(g,p,oversized,require_teacher=False)
except ValueError as error:
 assert str(error)=='teaching_message_capacity';capacity_stop=True;h={'teacher_semantics_correct':False}
# Founder qualification failures must prevent every arm from starting.
fc=[]
def failed_founder(phase,packet):
 fc.append(phase);v=oracle(phase,packet)
 if phase=='learn' and packet['position']==w['members'][0]:v['note']['witnesses']=[]
 return v
f=c.evaluate_world(w,failed_founder)
current=1.1637270437;per=(8000+512)*2.5/1e6+512*10/1e6
out={'evidence_type':'offline scripted development fixture, not native results','sealed_main_opened':False,'calls_by_phase':dict(counts),'main_max_calls':sum(counts.values()),'fixture_max_request_bytes':max(sizes),'all50_founder_gate_precedes_arms':len(fc)==50 and not f['arms'],'founders_remaining_final':{a:r['arms'][a]['checkpoints'][-1]['founders_remaining'] for a in r['arms']},'changed_route_positions':len(changed),'unchanged_route_positions':50-len(changed),'interactive_static_calls_per_replacement':3,'broken_calls_per_replacement':1,'retained_replacement_calls':0,'overlong_teacher_stopped_before_delivery':capacity_stop,'overlong_teacher_still_delivered':bool(seen) and len(json.dumps(seen[0],separators=(',',':')))>1200,'current_exposure_usd':current,'remaining_study_usd':60-current,'max_incremental_infrastructure_usd':1,'remaining_model_envelope_with_full_infrastructure_usd':60-current-1,'worst_per_request_usd':per,'main_worst_model_usd':sum(counts.values())*per,'main_worst_cumulative_with_infrastructure_usd':current+1+sum(counts.values())*per,'existing_model_hard_stop_usd':53.1456,'historical_sol50_reserved_call_count':44,'native_calls':0}
Path(__file__).with_name('REPAIRED-AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
