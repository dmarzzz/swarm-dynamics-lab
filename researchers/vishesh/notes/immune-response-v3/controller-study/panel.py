"""Twelve public authored, operator-validated construction cases; no native evidence."""
import copy,json
from pathlib import Path
import cases

def build():
    recipes = [('healthy', 'healthy_batch'), ('healthy_expanded', 'healthy_expanded'), ('healthy', 'healthy_classic'),
               ('gateway_crash', 'gateway_crash'), ('worker_crash', 'worker_crash'), ('store_crash', 'store_crash'),
               ('stale_alarm', 'stale_worker_alarm'), ('masked_crash', 'stale_reassuring_worker'), ('stale_alarm', 'stale_gateway_alarm'),
               ('configuration', 'rpc_mismatch'), ('healthy', 'unreadable_data'), ('healthy', 'missing_feature')]
    result = []
    for i, (kind, variant) in enumerate(recipes):
        c = cases.make(kind, 25001 + 101*i); f, s = c['fixture'], c['initial']
        if variant == 'healthy_classic':
            for role in ('gateway','worker'): s['deployed'][role] = int(next(iter(f['catalog'][role])))
            f['feature'] = f['catalog']['gateway'][str(s['deployed']['gateway'])]['features'][0]
        if variant == 'unreadable_data':
            s['deployed']['worker'] = int(list(f['catalog']['worker'])[2]); c['kind'] = 'configuration'
        if variant == 'missing_feature':
            current = f['catalog']['gateway'][str(s['deployed']['gateway'])]
            alternate = next(v for v in f['catalog']['gateway'] if int(v) != s['deployed']['gateway'])
            f['catalog']['gateway'][alternate] = copy.deepcopy(current)
            current['features'].remove(f['feature']); c['kind'] = 'configuration'
        f['deployed'] = copy.deepcopy(s['deployed'])
        s['probe'] = {'epoch': s['epoch'], 'checks': cases.f.health(f,s), 'live': copy.deepcopy(s['live'])}
        if variant.startswith('stale_'):
            s['probe']['epoch'] -= 1
            role = 'gateway' if variant == 'stale_gateway_alarm' else 'worker'
            s['probe']['live'][role] = variant == 'stale_reassuring_worker'
            s['probe']['checks']['processes_live'] = variant == 'stale_reassuring_worker'
        c.update(id='panel-'+str(i+1), variant=variant, family=('healthy' if i<3 else 'runtime' if i<6 else 'stale' if i<9 else 'configuration'))
        result.append(c)
    return result

if __name__ == '__main__':
    import public_reference
    rows=[]
    for c in build():
        state=copy.deepcopy(c['initial']);history=[];trace=[]
        for tick in (1,2):
            o=cases.observe(c,state,tick,history,[]);d=public_reference.labels(o)
            assert d==cases.diagnosis(o)
            raw=public_reference.choose(o);a=cases.f.controller.decode(c['fixture'],raw);x=cases.f.step(c['fixture'],state,a)
            trace.append(x);history.append({'action':a,'result':x['result']})
        rows.append({'id':c['id'],'family':c['family'],'variant':c['variant'],'reference_pass':cases.gate(c,trace),'actions':[x['action']['action'] for x in trace]})
    assert all(x['reference_pass'] for x in rows)
    print(json.dumps({'backend':'offline_rule_based','native_calls':0,'worlds':12,'families':4,'rows':rows},indent=2))
