"""Single-authority selection. No gold access, retries or retrospective rescoring."""
import copy
import contract
OLD='Return {"witnesses":[two distinct current roster positions],"note":{"witnesses":[two positions]}}. Use only your private note and delivered change history; apply change only to your position.'
NEW='Return only {"witnesses":[two distinct current roster positions]}. Infer your current pair from your private note and any delivered change history. This exact chosen pair is both your consultation route and your persisted private policy; choose once. Apply change only to your own position.'
def wire(phase,family,packet):
 body=contract.wire(phase,family,packet)
 if phase=='select':
  assert OLD in body['messages'][0]['content'];body['messages'][0]['content']=body['messages'][0]['content'].replace(OLD,NEW)
 contract.validate_wire(body);return body

def to_engine(phase,value):
 if phase!='select':return copy.deepcopy(value)
 if not isinstance(value,dict) or set(value)!={'witnesses'}:raise ValueError('single_selection_schema')
 pair=value['witnesses']
 if not isinstance(pair,list) or len(pair)!=2 or not all(isinstance(x,str) for x in pair) or len(set(pair))!=2:raise ValueError('single_selection_pair')
 return {'witnesses':copy.deepcopy(pair),'note':{'witnesses':copy.deepcopy(pair)}}
