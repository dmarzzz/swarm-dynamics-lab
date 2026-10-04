"""Versioned wire representations; the original strict local contract is unchanged."""
import copy,hashlib,json
from output_contract_d8 import compile_item as original_compile,verify_item as original_verify,MAX_BYTES

def expand(schema):
    defs=schema.get('$defs',{})
    def walk(node,seen=()):
        if isinstance(node,list):return [walk(x,seen) for x in node]
        if not isinstance(node,dict):return node
        if '$ref' in node:
            ref=node['$ref'];assert set(node)=={'$ref'} and ref.startswith('#/$defs/')
            key=ref[len('#/$defs/'):];assert key not in seen and key in defs
            return walk(defs[key],seen+(key,))
        return {k:walk(v,seen) for k,v in node.items() if k!='$defs'}
    return walk(schema)

def compile_item(parent):
    item=original_compile(parent)
    variant=item.get('wire_variant','original')
    if variant=='original':return item
    if variant!='shared_groups_v1' or not item['arm'].startswith('typed'):raise ValueError('wire variant')
    schema=item['wire_body']['response_format']['json_schema']['schema'];original=copy.deepcopy(schema)
    candidates=schema['properties']['candidate_facts']['properties'];defs={}
    for candidate in candidates.values():
        for group,node in candidate['properties'].items():
            if group in defs:assert defs[group]==node
            else:defs[group]=copy.deepcopy(node)
            candidate['properties'][group]={'$ref':'#/$defs/'+group}
    schema['$defs']=defs
    assert expand(schema)==original
    raw=json.dumps(item['wire_body']).encode();assert len(raw)<=MAX_BYTES
    item.update(wire_bytes=len(raw),wire_sha256=hashlib.sha256(raw).hexdigest())
    return item

def verify_item(item):
    if item.get('wire_variant','original')=='original':return original_verify(item)
    expected=compile_item(item)
    if any(item.get(k)!=expected[k] for k in ('wire_body','wire_bytes','wire_sha256','maximum_reservation_usd')):raise ValueError('wire representation mismatch')
    return item
