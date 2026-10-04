"""Full reference scoring, implemented separately from D1 truth/command helpers."""
import json,collections

def reference(a,result):
 # Reparse retained actor text independently where available.
 try:v=json.loads(result['raw_text']) if result.get('raw_text') is not None else result.get('value')
 except (ValueError,TypeError):v=None
 ids=[c['id'] for c in a['cases']];docs=({'none':'console1/none','probe':'console1/probe','ledger':'console1/ledger','canary':'console1/canary'} if a['context']=='incident' else {'ship':'console1/ship','hold':'console1/hold'})
 inverse={v:k for k,v in docs.items()};ds=v.get('decisions') if isinstance(v,dict) else None
 schema=isinstance(v,dict) and set(v)=={'decisions'} and isinstance(ds,list)
 if not isinstance(ds,list):ds=[]
 valid_rows=[d for d in ds if isinstance(d,dict) and set(d)=={'id','command'} and isinstance(d['id'],str) and isinstance(d['command'],str)]
 schema=schema and len(valid_rows)==len(ds)
 counts=collections.Counter(d['id'] for d in valid_rows)
 valid=schema and counts==collections.Counter(ids) and all(d['command'] in inverse for d in valid_rows) and not result.get('error')
 rows=[]
 for c in a['cases']:
  source=a['rule'][c['class']];e=c['evidence'][source];truth=(source if e['signal'] else 'none') if a['context']=='incident' else ('ship' if e['signal'] and e['fresh'] else 'hold')
  command=next((d['command'] for d in valid_rows if d['id']==c['id']),None) if counts[c['id']]==1 else None
  action=inverse.get(command);semantic=action if action is not None else (command if command in docs else None)
  rows.append({'id':c['id'],'truth':truth,'action':action,'correct':bool(valid and action==truth),'partial_correct':action==truth,'valid_response':bool(valid),'response_received':bool(result.get('response_received',v is not None)),'id_present_once':counts[c['id']]==1,'schema_valid':bool(schema),'command_valid':command in inverse,'semantic_action':semantic,'semantic_correct':semantic==truth})
 return rows
