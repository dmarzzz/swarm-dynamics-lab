"""Offline D8 compiler only: no transport, credentials, admission or launch."""
import copy,json,hashlib
from candidate_checks import matrix_schema
from typed_policy import schema,check_wire_schema
JSON_ONLY=' Return exactly one JSON object matching the supplied response schema. Do not include Markdown, code fences or text outside that object.'
MAX_BYTES=32768
RESERVATION=.048640

def compile_item(parent):
    item=copy.deepcopy(parent)
    contract=(schema if item['arm'].startswith('typed') else matrix_schema)(item['request']['observation'])
    check_wire_schema(contract)
    wire=item['wire_body']
    wire['messages'][0]['content']=item['request']['instructions']+JSON_ONLY
    wire['response_format']={'type':'json_schema','json_schema':{'name':'reviewer_output','strict':True,'schema':contract}}
    item['maximum_reservation_usd']=RESERVATION
    raw=json.dumps(wire).encode()
    if len(raw)>MAX_BYTES:raise ValueError('wire_bound')
    item.update(wire_bytes=len(raw),wire_sha256=hashlib.sha256(raw).hexdigest())
    return item

def verify_item(item):
    expected=compile_item(item)
    if any(item.get(k)!=expected[k] for k in ('wire_body','wire_bytes','wire_sha256')):raise ValueError('output_contract_not_delivered')
    if item['maximum_reservation_usd']!=RESERVATION:raise ValueError('reservation_mismatch')
    return item
