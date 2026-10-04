"""Bounded new-context wire; reuses the published phase-specific instructions."""
import copy,json,hashlib
from decimal import Decimal
import scale_families
import commit_v3,selection_v2,contract
MAX_BYTES=12000
PER_CALL=Decimal('0.0364')
CAPS={'Q50':60,'S50':1150}
PRIOR=Decimal('1.9468005437')
HISTORICAL_UNKNOWN=Decimal('0.033102')
STUDY_CAP=Decimal('60')

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def wire(phase,family,packet):
 body=commit_v3.wire(phase,family,{})
 if phase in ('learn','select'):
  body['messages'][0]['content']+=' Sparse history declares eligible positive records for every other roster position, with only the named veto_source false in that episode. Infer the pair from outcomes; no source is explicitly labeled authoritative.'
 body['messages'][1]['content']=json.dumps(packet,separators=(',',':'))
 validate(body);return body

def validate(body):
 expected=commit_v3.wire('commit','failover',{})
 if {k:v for k,v in body.items() if k!='messages'}!={k:v for k,v in expected.items() if k!='messages'}:raise ValueError('route')
 if len(body.get('messages',[]))!=2 or [x.get('role') for x in body['messages']]!=['system','user']:raise ValueError('messages')
 if any(not isinstance(x.get('content'),str) for x in body['messages']) or 'JSON' not in body['messages'][0]['content']:raise ValueError('content')
 if len(json.dumps(body,separators=(',',':')).encode())>MAX_BYTES:raise ValueError('oversized_no_truncation')
 return True

def to_engine(phase,value):return selection_v2.to_engine(phase,value)
