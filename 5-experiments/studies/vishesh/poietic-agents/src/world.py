"""Versioned fictional read APIs. This module does not expose answer labels."""
import copy
import random
from collections import Counter
from common import digest, stream_seed

ENDPOINTS = ('inventory', 'supplier_terms', 'delivery_status')
SKILLS = ('retrieve', 'normalize', 'join_aggregate', 'validate_format')
KINDS = ('replenish', 'exceptions', 'reconcile')


def rows(root, entity, endpoint, version):
    rng = random.Random(stream_seed('source-v2', root, f'{entity}:{endpoint}:{version}'))
    if endpoint == 'inventory':
        return [dict(entity_id=entity, available=rng.randrange(0, 21), reserved=rng.randrange(0, 5))]
    if endpoint == 'supplier_terms':
        return [dict(entity_id=entity, supplier=s, unit_cents=rng.randrange(10, 91),
                     capacity=rng.randrange(0, 31), lead_days=rng.randrange(1, 8)) for s in ('a', 'b', 'c')]
    if endpoint == 'delivery_status':
        return [dict(entity_id=entity, shipment=f'{entity}-{s}', expected=10,
                     received=rng.randrange(0, 11), due_day=rng.randrange(1, 8)) for s in range(3)]
    raise PermissionError('endpoint_not_allowed')


class World:
    def __init__(self, root, scenario='schema_shift'):
        self.root, self.scenario = root, scenario

    def fetch(self, endpoint, entity, epoch):
        if endpoint not in ENDPOINTS or not isinstance(entity, str) or not entity.startswith('sku-'):
            raise PermissionError('endpoint_or_entity')
        version = (epoch - 1) // 2 + 1
        schema = 2 if self.scenario == 'schema_shift' and epoch >= 5 else 1
        data = rows(self.root, entity, endpoint, version)
        # Public v2 migration: quantities move under a nested body; money becomes millicents.
        if schema == 2:
            data = [dict(entity_id=r['entity_id'], body={
                ('unit_millicents' if k == 'unit_cents' else k): (v * 1000 if k == 'unit_cents' else v)
                for k, v in r.items() if k != 'entity_id'}) for r in data]
        result = dict(endpoint=endpoint, entity_id=entity, schema_version=schema,
                      source_version=version, valid_from_epoch=2*version-1,
                      expires_after_epoch=2*version, provenance='fictional-operations-v2', rows=data)
        result['receipt'] = digest(result)
        return result

    def notices(self, epoch):
        return dict(source_version=(epoch-1)//2+1, schema_version=2 if self.scenario == 'schema_shift' and epoch >= 5 else 1,
                    schema_v2='body nests fields; unit_millicents / 1000 gives integer unit_cents')


def normalize(packet):
    if packet['schema_version'] == 1:
        return copy.deepcopy(packet['rows'])
    if packet['schema_version'] != 2:
        raise ValueError('unknown_schema')
    result = []
    for row in packet['rows']:
        out = dict(entity_id=row['entity_id'], **row['body'])
        if 'unit_millicents' in out:
            if out['unit_millicents'] % 1000:
                raise ValueError('noninteger_money')
            out['unit_cents'] = out.pop('unit_millicents') // 1000
        result.append(out)
    return result


def job(root, epoch, index, entity=None):
    entity = entity or f'sku-{index}'
    rng = random.Random(stream_seed('jobs-v2', root, f'{epoch}:{index}'))
    kind = KINDS[index % 3]
    endpoints = {'replenish': ['supplier_terms'], 'exceptions': ['inventory'], 'reconcile': ['delivery_status']}[kind]
    return dict(id=f'{root}:{epoch}:{index}', root=root, epoch=epoch, kind=kind, entities=[entity],
                endpoints=endpoints, quantity=rng.randrange(5, 16), max_lead=4, threshold=8, day=4,
                release_s=120*(epoch-1), deadline_s=120*epoch)


def jobs(root, epoch, scenario='schema_shift'):
    # 6 required occurrences: high overlap 4/6, low 0/6. Honest discrete realization,
    # not a fictional exact 80% or 20% with six jobs. Version and endpoint are in each key.
    high = scenario != 'overlap_shift' or epoch < 5
    entities = ['sku-0', 'sku-0', 'sku-2', 'sku-0', 'sku-0', 'sku-5'] if high else [f'sku-{i}' for i in range(6)]
    return [job(root, epoch, i, entities[i]) for i in range(6)]


def overlap(assigned, world):
    keys = [(e, entity, world.fetch(e, entity, j['epoch'])['source_version'])
            for j in assigned for e in j['endpoints'] for entity in j['entities']]
    counts = Counter(keys)
    return dict(repeated_occurrences=sum(counts[k] > 1 for k in keys), required_occurrences=len(keys),
                unique_keys=len(counts), share=sum(counts[k] > 1 for k in keys)/len(keys) if keys else None)
