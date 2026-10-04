"""Known-answer controls consume the actor request only; never accept a world."""
from collections import Counter
from .evidence import reported_records, resolve, justified_choice, supported_parent


class Scripted:
    scientific = False
    def __init__(self, behavior='evidence'):
        if behavior not in ('evidence', 'abstain', 'copy_count', 'wrong_entity'):
            raise ValueError('unknown scripted control')
        self.behavior = behavior
        self.name = 'scripted-v3-' + behavior
        self.calls = 0
        self.last_usage = {}

    def complete(self, request):
        self.calls += 1
        phase = request['phase']; context = request['context']; task = context['task']
        records = reported_records(context)
        if phase == 'parent':
            if self.behavior == 'abstain': return {'value': None, 'sources': []}
            if self.behavior == 'wrong_entity' and context['memory']:
                r = context['memory'][0]
                return {'value': r['value'] + context['delta'], 'sources': r['sources']}
            if self.behavior == 'copy_count':
                values = [r['facts'][context['key']] for r in records if context['key'] in r['facts']]
                if values:
                    v = Counter(values).most_common(1)[0][0]
                    return {'value': v + context['delta'], 'sources': sorted({r['id'] for r in records if r['facts'].get(context['key']) == v})}
            return supported_parent(context)
        claims = {}
        for key in task['fact_keys']:
            alternatives = resolve(key, records, task['policy'])
            if len(alternatives) == 1 and self.behavior != 'abstain':
                value, support = next(iter(alternatives.items()))
                claims[key] = {'value': value, 'sources': support['sources']}
            else: claims[key] = None
        if phase in ('report', 'work'):
            return {'message': 'Use the stated source policy; missing and conflicting evidence remains unresolved.', 'claims': claims}
        return {'vote': 'ABSTAIN' if self.behavior == 'abstain' else justified_choice(task, records), 'claims': claims}


def anthropic(config):
    """Use the existing minimal provider boundary, with the v3 syntax contract."""
    from providers import Anthropic
    from .contracts import SYSTEM, schema, strict_json
    return Anthropic(system_prompt=SYSTEM, response_schema=schema, response_decoder=strict_json, **config)
