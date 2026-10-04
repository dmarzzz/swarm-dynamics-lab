"""Source-pinned Q3 semantic engine. Injected caller owns native transport/custody."""
import copy,json
import scale_families as f,contract as c

class Institution:
 def __init__(self,w,family,notes):
  self.w=w;self.family=family;self.notes=copy.deepcopy(notes);self.generations={p:0 for p in w['members']}
 def actor(self,p,current=None):
  return {'position':p,'identity':p+'/g'+str(self.generations[p]),'roster':[{'position':q,'identity':q+'/g'+str(self.generations[q])} for q in self.w['members']],'private_note':copy.deepcopy(self.notes.get(p)),'current_observations':copy.deepcopy(current or [])}

def valid_note(value,w,owner):
 if not isinstance(value,dict) or set(value)!={'witnesses'} or not isinstance(value['witnesses'],list):return False
 pair=value['witnesses']
 return len(pair)==2 and all(isinstance(x,str) and x in w['members'] and x!=owner for x in pair) and len(set(pair))==2

def route_ok(note,w,owner,changed=False):
 return valid_note(note,w,owner) and set(note['witnesses'])==set(w['changed_routes' if changed else 'routes'][owner])

def invoke(call,family,phase,packet,condition):return call(family,phase,packet,condition)

def initialize(w,family,call):
 notes={};grades=[]
 for p in w['members']:
  packet=Institution(w,family,{}).actor(p);packet['history']=f.history(w,family,p)
  value=invoke(call,family,'learn',packet,'founder-acquisition');note=value.get('note') if isinstance(value,dict) else None
  valid=isinstance(value,dict) and set(value)=={'note'} and valid_note(note,w,p)
  if not valid:raise ValueError('founder_schema')
  notes[p]=copy.deepcopy(note);grades.append({'owner':p,'valid':valid,'qualified':valid and route_ok(note,w,p)})
 return notes,grades

def checkpoint(g,call,index,owners=None,changed=False):
 w=g.w;family=g.family;owners=list(owners or w['members']);inbox={p:[] for p in w['members']};received={p:[] for p in owners};cases={};selected=[];overflow=[]
 for owner in owners:
  is_changed=changed and set(w['routes'][owner])!=set(w['changed_routes'][owner])
  # Initial owners cover consecutive invalid-evidence variants; final covers variant6.
  case_index=w['members'].index(owner) if index==0 else 1
  cases[owner]=f.panel(w,family,owner,index=case_index,changed=changed)
  current=f.history(w,family,owner,True) if is_changed else []
  p=g.actor(owner,current);value=invoke(call,family,'select',p,'checkpoint-'+str(index));note=value.get('note') if isinstance(value,dict) else None
  peers=value.get('witnesses') if isinstance(value,dict) else None
  if not isinstance(value,dict) or set(value)!={'note','witnesses'} or not valid_note(note,w,owner) or not valid_note({'witnesses':peers},w,owner):raise ValueError('selection_schema')
  g.notes[owner]=copy.deepcopy(note);selected.append({'owner':owner,'selected':peers,'route_correct':set(peers)==set(w['changed_routes' if changed else 'routes'][owner]),'note_correct':route_ok(note,w,owner,changed)})
  for peer in peers:
   if len(inbox[peer])==2:overflow.append({'owner':owner,'peer':peer});continue
   inbox[peer]+=f.witness_inbox(cases[owner],peer)
 witnesses=[]
 for peer in w['members']:
  if not inbox[peer]:continue
  packet=g.actor(peer);packet['private_inbox']=inbox[peer];value=invoke(call,family,'attest',packet,'checkpoint-'+str(index))
  delivered=f.hydrate(peer,inbox[peer],value)
  expected={r['id'] for row in inbox[peer] for r in row['records']};actual={r['id'] for r in delivered}
  witnesses.append({'witness':peer,'exact':actual==expected,'expected_records':len(expected),'delivered_records':len(actual)})
  for report in value['reports']:
   # Preserve invalid record owner metadata; delivery uses addressed envelope.
   received[report['owner']]+=f.hydrate(peer,inbox[peer],{'reports':[report]})
 grades=[]
 for owner in owners:
  packet=f.decision_packet(owner,g.notes[owner],cases[owner],received[owner]);value=invoke(call,family,'decide',packet,'checkpoint-'+str(index))
  grades.append({'owner':owner,'stratum':'updated' if changed and set(w['routes'][owner])!=set(w['changed_routes'][owner]) else 'preserved',**f.score(value,cases[owner])})
 return {'checkpoint':index,'owners':owners,'selections':selected,'witnesses':witnesses,'overflow':overflow,'decisions':grades,'passed':not overflow and all(x['route_correct'] and x['note_correct'] for x in selected) and all(x['exact'] for x in witnesses) and all(x['correct']==x['assigned'] and x['harmful']==0 for x in grades)}

def handover(g,owner,call):
 old=g.actor(owner)['identity'];inherited=copy.deepcopy(g.notes[owner]);q=invoke(call,g.family,'question',{'position':owner,'successor_identity':owner+'/g1','inherited_note':inherited},'handover')
 if not isinstance(q,dict) or set(q)!={'question'} or not isinstance(q['question'],str) or len(q['question'])>400:raise ValueError('question_contract')
 p=g.actor(owner);p['question']=q;teacher=invoke(call,g.family,'teach',p,'handover');teacher=c.teacher_delivery(teacher)
 if not route_ok(teacher['note'],g.w,owner):return {'passed':False,'teacher_correct':False,'retired':False}
 g.notes.pop(owner);g.generations[owner]+=1
 p=c.successor(owner,g.actor(owner)['roster'],'interactive',inherited,teacher);p['identity']=owner+'/g1'
 value=invoke(call,g.family,'commit',p,'handover');note=value.get('note') if isinstance(value,dict) else None
 good=isinstance(value,dict) and set(value)=={'note'} and route_ok(note,g.w,owner)
 g.notes[owner]=copy.deepcopy(note)
 return {'passed':good,'teacher_correct':True,'successor_note_correct':good,'retired':old,'successor':owner+'/g1'}

def qualify_world(w,family,call,event=lambda x:None):
 notes,founders=initialize(w,family,call);out={'family':family,'founders':founders,'passed':False};event({'phase':'founders','result':founders})
 if not all(x['qualified'] for x in founders):out['stop']='founder_gate';return out
 g=Institution(w,family,notes);out['initial']=checkpoint(g,call,0);event({'phase':'initial','result':out['initial']})
 if not out['initial']['passed']:out['stop']='initial_gate';return out
 unchanged=[p for p in w['replacement_order'] if set(w['routes'][p])==set(w['changed_routes'][p])];updated=[p for p in w['replacement_order'] if p not in unchanged]
 if len(unchanged)!=2 or len(updated)!=4:raise ValueError('strata')
 owner=unchanged[0];out['handover']=handover(g,owner,call);event({'phase':'handover','result':out['handover']})
 if not out['handover']['passed']:out['stop']='handover_gate';return out
 out['terminal']=checkpoint(g,call,1,[owner,updated[0]],changed=True);out['passed']=out['terminal']['passed'];out['stop']=None if out['passed'] else 'terminal_gate';event({'phase':'terminal','result':out['terminal']});return out

def qualify(packet,call,event=lambda x:None):
 if packet.get('stage')!='Q3' or len(packet['assignments'])!=3:raise ValueError('packet_scope')
 results=[]
 for a in packet['assignments']:
  result=qualify_world(a['world'],a['family'],call,event);results.append(result)
  if not result['passed']:break
 return {'attempt':packet['attempt'],'passed':len(results)==3 and all(r['passed'] for r in results),'families':results,'unstarted_families':3-len(results),'automatic_successor':False}
