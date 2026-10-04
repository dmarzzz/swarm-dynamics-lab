"""Observer-only reference. Never imported by actor context or the action executor."""
from common import digest


def reference(job, packets):
    # Intentionally independent of the actor's normalization and expression interpreter.
    data = []
    for packet in packets:
        for row in packet['rows']:
            if packet['schema_version'] == 1:
                data.append(dict(row))
            else:
                r = dict(row['body'], entity_id=row['entity_id'])
                if 'unit_millicents' in r:
                    r['unit_cents'] = r.pop('unit_millicents') // 1000
                data.append(r)
    if job['kind'] == 'replenish':
        eligible = [r for r in data if r['capacity'] >= job['quantity'] and r['lead_days'] <= job['max_lead']]
        if not eligible:
            return {'supplier': None, 'total_cents': 0}
        row = sorted(eligible, key=lambda r: (r['unit_cents'], r['supplier']))[0]
        return {'supplier': row['supplier'], 'total_cents': row['unit_cents']*job['quantity']}
    if job['kind'] == 'exceptions':
        return sorted(r['entity_id'] for r in data if r['available']-r['reserved'] < job['threshold'])
    if job['kind'] == 'reconcile':
        return sum(max(0, r['expected']-r['received']) for r in data if r['due_day'] <= job['day'])
    raise ValueError('job_kind')


def grade(job, response, world, issued, finished_s):
    expected_packets = [world.fetch(e, entity, job['epoch']) for e in job['endpoints'] for entity in job['entities']]
    expected = reference(job, expected_packets)
    valid = isinstance(response, dict) and set(response) == {'value', 'receipts'} and isinstance(response['receipts'], list)
    correct = valid and digest(response['value']) == digest(expected)
    wanted = {p['receipt'] for p in expected_packets}
    supplied = set(response['receipts']) if valid and all(isinstance(x, str) for x in response['receipts']) else set()
    # A receipt must both be current and have actually reached the actor via the adapter.
    fresh = valid and wanted <= supplied and supplied <= set(issued) and all(
        issued[r]['valid_from_epoch'] <= job['epoch'] <= issued[r]['expires_after_epoch'] for r in supplied)
    on_time = finished_s <= job['deadline_s']
    return dict(schema_valid=valid, correct=bool(correct), fresh=bool(fresh), on_time=on_time,
                success=bool(correct and fresh and on_time))


def summarize(assigned, outcomes, deployment_usd):
    ids = {j['id'] for j in assigned}
    by = {o['id']: o for o in outcomes}
    if len(ids) != len(assigned) or len(by) != len(outcomes) or not set(by) <= ids:
        raise ValueError('duplicate_or_unassigned_outcome')
    success = sum(bool(o.get('success')) for o in outcomes)
    return dict(assigned=len(assigned), terminal=len(outcomes), unstarted=len(ids)-len(by), successful=success,
                quality=success/len(ids), deployment_usd=deployment_usd, cost_per_assigned=deployment_usd/len(ids),
                cost_per_success=deployment_usd/success if success else None,
                cost_per_success_label='finite' if success else 'infinity')
