"""Frozen scope and semantic protocol. Caller owns transport; no implicit native calls."""
import copy
import scale_families as f,scale_engine as e,scale_turnover as t
from scale_contract import digest
from instrument import world
SEEDS={'Q50':90501,'S50':90502}

def packet():
 return {'version':'S50-v1','model':'openai/gpt-6-sol','family':'failover','members':50,'stages':{'Q50':{'seed':SEEDS['Q50'],'max_calls':60},'S50':{'seed':SEEDS['S50'],'max_calls':1150}},'arms':list(t.ARMS),'generations':1,'checkpoint_indices':[0,1],'max_input_bytes':12000,'max_output_tokens':512,'retry_count':0,'max_in_flight':1,'main_eligibility':'Q50 pass; no main semantic selection','prior_exposure_usd':'1.9468005437','historical_unknown_usd':'0.033102','study_cap_usd':'60','model_cap_usd':'44.044','hosting_cap_usd':'0.30','all_in_cap_usd':'44.344'}

def qowners(w):
 updated=[p for p in w['replacement_order'] if set(w['routes'][p])!=set(w['changed_routes'][p])]
 same=[p for p in w['replacement_order'] if p not in updated]
 # Each inherited arm includes one preserved and one legitimately changed route.
 return [same[0],updated[0],same[1],updated[1],same[2],same[3]]

def qualify(call):
 w=world(SEEDS['Q50'],50);family='failover';owners=qowners(w);notes={};grades=[]
 for p in owners:
  value=call(family,'learn',{**e.Institution(w,family,{}).actor(p),'history':f.history(w,family,p)},'Q50-founder')
  note=value.get('note') if isinstance(value,dict) else None
  valid=isinstance(value,dict) and set(value)=={'note'} and e.valid_note(note,w,p)
  grades.append({'owner':p,'valid':valid,'correct':e.route_ok(note,w,p)});notes[p]=copy.deepcopy(note)
 out={'stage':'Q50','founders':grades,'passed':False,'active_roster_positions':50,'acquired_owners':6}
 if not all(x['valid'] and x['correct'] for x in grades):out['stop']='founders';return out
 g=e.Institution(w,family,notes);out['initial']=e.checkpoint(g,call,0,owners)
 if not out['initial']['passed']:out['stop']='initial';return out
 out['handovers']=[]
 for k,p in enumerate(owners):
  arm='interactive' if k<2 else 'static' if k<4 else 'broken'
  out['handovers'].append({'arm':arm,**t.replace(g,p,arm,call)})
 if not all(x['note_correct'] for x in out['handovers'][:4]):out['stop']='inherited_notes';return out
 out['terminal']=e.checkpoint(g,call,1,owners[:4],True)
 out['passed']=out['terminal']['passed'];out['stop']=None if out['passed'] else 'terminal'
 return out

def main(call):return t.trajectory(world(SEEDS['S50'],50),'failover',call)

def scripted(family,phase,p,condition):
 """Observed-evidence controller for tests, never a native response or fallback."""
 if phase=='learn':return {'note':{'witnesses':f.infer(p['position'],[x['position'] for x in p['roster'] if x['position']!=p['position']],p['history'])}}
 if phase=='select':
  pair=p['private_note']['witnesses']
  if p['current_observations']:pair=f.infer(p['position'],[x['position'] for x in p['roster'] if x['position']!=p['position']],p['current_observations'])
  return {'witnesses':copy.deepcopy(pair)}
 if phase=='attest':return {'reports':[{'owner':x['owner'],'evidence_ids':[r['id'] for r in x['records']]} for x in p['private_inbox']]}
 if phase=='decide':return {'actions':[{'case':x['case'],'action':f.decide(p['private_note']['witnesses'],p['received_records']+p['public_audit_records'],x)} for x in p['cases']]}
 if phase=='question':return {'question':'Which two positions should I consult, and what should change when fresh evidence changes responsibilities?'}
 if phase=='teach':return {'note':copy.deepcopy(p['private_note']),'explanation':'Preserve this pair unless current local learning evidence establishes a changed pair.'}
 if phase=='commit':return {'note':copy.deepcopy(p.get('inherited_note') or {'witnesses':[x['position'] for x in p['roster'] if x['position']!=p['position']][:2]})}
 raise ValueError('phase')
