"""Pure six-call selector/writeback diagnostic, using inspected qualification contexts."""
import copy
import selection_v2 as s,families as f

def run(packet,call):
 out=[]
 for row in packet['contexts']:
  family=row['family'];p=copy.deepcopy(row['selector_packet']);owner=p['position'];value=call(family,'select',p,row['name']);adapted=s.to_engine('select',value);pair=adapted['witnesses'];note=adapted['note']
  if len(set(pair))!=2 or any(x==owner or x not in row['world']['members'] for x in pair):raise ValueError('roster_pair')
  history=p['current_observations'];expected=f.infer(owner,[x['position'] for x in p['roster'] if x['position']!=owner],history) if history else p['private_note']['witnesses']
  cases=f.panel(row['world'],family,owner,index=6,changed=True);records=[]
  for peer in pair:
   for item in f.witness_inbox(cases,peer):records+=item['records']
  decision=f.decision_packet(owner,note,cases,records);actions=call(family,'decide',decision,row['name']);score=f.score(actions,cases)
  out.append({'context':row['name'],'family':family,'selected_pair_correct':set(pair)==set(expected),'selection_equals_persisted_note':pair==note['witnesses'],'controller_correct':sum(f.decide(expected,[v for peer in expected for item in f.witness_inbox(cases,peer) for v in item['records']]+decision['public_audit_records'],case['target'])==case['gold'] for case in cases),**score})
 return {'contexts':out,'passed':len(out)==3 and all(v['selected_pair_correct'] and v['correct']==6 and v['harmful']==0 for v in out),'scripted_record_delivery':True,'full_native_qualification':False}
