"""Pure paired turnover engine; no dispatcher, credentials or launch authority."""
import copy
import engine as e,contract as c,families as f
ARMS=('interactive','static','broken','retained')

def replace(g,owner,arm,call):
 inherited=copy.deepcopy(g.notes[owner]);question=None;inspection=None;teacher=None
 if arm in ('interactive','static'):
  q=call(g.family,'question',{'position':owner,'successor_identity':owner+'/g1','inherited_note':inherited},arm+'-handover')
  if not isinstance(q,dict) or set(q)!={'question'} or not isinstance(q['question'],str) or len(q['question'])>400:raise ValueError('question_contract')
  if arm=='interactive':question=q
  else:inspection=q
  p=g.actor(owner)
  if question is not None:p['question']=question
  teacher=c.teacher_delivery(call(g.family,'teach',p,arm+'handover'))
 old=g.actor(owner)['identity'];g.notes.pop(owner);g.generations[owner]+=1
 p=c.successor(owner,g.actor(owner)['roster'],arm,inherited if arm!='broken' else None,teacher,inspection);p['identity']=owner+'/g1'
 value=call(g.family,'commit',p,arm+'-handover');note=value.get('note') if isinstance(value,dict) else None
 if not isinstance(value,dict) or set(value)!={'note'} or not e.valid_note(note,g.w,owner):raise ValueError('commit_schema')
 g.notes[owner]=copy.deepcopy(note)
 return {'owner':owner,'retired':old,'successor':owner+'/g1','note_correct':e.route_ok(note,g.w,owner)}

def controller(w,family,changed):
 """Infer legally available history; no route truth supplied to controller."""
 result=[]
 for owner in w['members']:
  peers=[p for p in w['members'] if p!=owner];history=f.history(w,family,owner)
  if changed and set(w['routes'][owner])!=set(w['changed_routes'][owner]):history=f.history(w,family,owner,True)
  pair=f.infer(owner,peers,history);cases=f.panel(w,family,owner,index=6 if changed else w['members'].index(owner),changed=changed)
  rows=[]
  for peer in pair:
   for item in f.witness_inbox(cases,peer):rows+=item['records']
  p=f.decision_packet(owner,{'witnesses':pair},cases,rows)
  actions={'actions':[{'case':x['case'],'action':f.decide(pair,p['received_records']+p['public_audit_records'],x)} for x in p['cases']]}
  result.append({'owner':owner,**f.score(actions,cases)})
 return result

def trajectory(w,family,call):
 notes,founders=e.initialize(w,family,call)
 out={'family':family,'founders':founders,'arms':{},'complete':False}
 if not all(x['qualified'] for x in founders):out['stop']='founder_gate';return out
 g=e.Institution(w,family,notes);initial=e.checkpoint(g,call,0);out['initial']=initial
 if not initial['passed']:out['stop']='initial_gate';return out
 out['common_notes']=copy.deepcopy(g.notes)
 out['controller_initial']=controller(w,family,False);out['controller_terminal']=controller(w,family,True)
 if not all(x['correct']==x['assigned'] and x['harmful']==0 for x in out['controller_initial']+out['controller_terminal']):raise ValueError('controller_gate')
 for arm in ARMS:
  state=copy.deepcopy(g);record={'initial_notes':copy.deepcopy(state.notes),'replacements':[]}
  def scoped(family,phase,packet,condition):return call(family,phase,packet,arm+'-'+condition)
  if arm!='retained':
   for owner in w['replacement_order']:record['replacements'].append(replace(state,owner,arm,scoped))
  record['terminal']=e.checkpoint(state,scoped,1,changed=True);record['terminal_generations']=copy.deepcopy(state.generations);out['arms'][arm]=record
 out['complete']=True;out['stop']=None
 return out
