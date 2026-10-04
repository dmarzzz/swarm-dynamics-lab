"""Public-shape-only schemas; never consumes evaluator truth or repairs model text."""
VERSION = 'anthropic-json-schema-v1'
LEGACY = 'prompt-only-v1'


def closed(properties):
    return {'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}


def schema_for(public,phase,item=None):
    if phase=='transport':
        return closed({'ok':{'type':'boolean'}})
    if not isinstance(public,dict) or public.get('family') not in ('evidence','repository'):
        raise ValueError('response_contract_task_missing')
    items=public.get('items')
    if not isinstance(items,list) or not items or any(type(i) is not str for i in items) or len(set(items))!=len(items):
        raise ValueError('response_contract_task_missing')
    strings={'type':'array','items':{'type':'string'}}
    if phase in ('plan','plan_repair'):
        return closed({'dependencies':closed({i:strings for i in items})})
    artifact=closed({'value':{'type':'integer'},'source_ids':strings}) if public['family']=='evidence' else {'type':'string'}
    if phase=='work':
        if item not in items:raise ValueError('response_contract_item_unknown')
        return closed({'artifact':artifact})
    if phase=='integrate':
        if public['family']=='evidence':return closed({'answers':closed({i:artifact for i in items})})
        return closed({'files':closed({i+'.py':artifact for i in items})})
    raise ValueError('response_contract_phase_unknown')
