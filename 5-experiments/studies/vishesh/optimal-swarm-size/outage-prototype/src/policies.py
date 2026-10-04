"""Controllers consume only declared observations. No evaluator/case imports."""
def reference_actions(observation,limit=4):
    latest={}
    invalidated=set()
    for r in observation['recent_tool_results']:
        name=r['action'].get('service')
        if r['result']['status']=='observed':latest[name]=r['result'];invalidated.discard(name)
        elif r['action']['op']=='patch':invalidated.add(name)
    actions=[]
    for name in observation['service_ids']:
        if observation['health'][name]:continue
        record=latest.get(name)
        if not record or name in invalidated:
            actions.append({'op':'inspect','service':name});continue
        s=record['config'];d=record['directory']
        actions.append({'op':'patch','service':name,'service_version':s['version'],'directory_version':d['version'],
                        'capacity_version':record['capacity_version'],
                        'set':{'endpoint':d['endpoint'],'protocol':d['protocol'],'pool':s['minimum_pool']}})
    return actions[:limit] or [{'op':'wait'}]

def should_contract(receipts):
    writes=[r for r in receipts if r['action'].get('op')=='patch'][-4:]
    return sum(r['result']['status']=='stale_version' for r in writes)>=2
