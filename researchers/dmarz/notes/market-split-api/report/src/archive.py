#!/usr/bin/env python3
"""Publish measured records from a complete audited attempt, without private hub metadata."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def archive(base, attempt, verified_path, output, expected_episodes):
    base = Path(base)
    verified = json.loads(Path(verified_path).read_text())
    assert verified and all(v['params']['attempt_id'] == attempt for v in verified)
    assert len({v['run'] for v in verified}) == len(verified)
    episodes, calls, receipts = [], [], []
    source_hashes = {}
    for v in sorted(verified, key=lambda v: v['run']):
        assert v['status'] == 'done' and v['metrics']['invalid'] == 0 and v['metrics']['visual_ok'] == 1
        folder = base / v['run'].replace('/', '__')
        for artifact in v['artifacts']:
            digest = hashlib.sha256((folder / artifact['name']).read_bytes()).hexdigest()
            assert digest == artifact['sha256'], (v['run'], artifact['name'])
            source_hashes[f"{folder.name}/{artifact['name']}"] = digest
        rs = [json.loads(line) for line in (folder / 'episodes.jsonl').read_text().splitlines()]
        cs = [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()]
        assert len(rs) == 2 and all(r['run'] == v['run'] and r['attempt_id'] == attempt for r in rs)
        assert all(r['validity']['ok'] and not r['unpriced_calls'] for r in rs)
        assert len(cs) == sum(r['model_calls'] for r in rs) == v['metrics']['model_calls']
        assert all(c['status'] == 'ok' and c['backend'] == 'anthropic' for c in cs)
        # No whole hub response, host data, private endpoint, credential or private reasoning is copied.
        assert all(set(c) <= {'call_id', 'arm', 'round', 'observation', 'prompt_sha256',
                             'backend', 'action', 'accounting', 'status'} for c in cs)
        episodes.extend(rs)
        calls.extend(cs)
        receipts.append({'run': v['run'], 'status': v['status'], 'params': v['params'],
                         'metrics': v['metrics'], 'artifacts': v['artifacts']})
    identities = [(r['task_id'], r['seed'], r['world'], r['arm']) for r in episodes]
    assert len(episodes) == expected_episodes == len(set(identities))
    assert len({(r['model'], r['engine_sha256'], r['design_sha256'], r['stage']) for r in episodes}) == 1
    assert len({c['call_id'] for c in calls}) == len(calls)
    fields = ['run', 'task_id', 'seed', 'world', 'arm', 'valid', 'rounds', 'registered_round',
              'fragmentation', 'behavioral_evasion', 'profit', 'actual_fines',
              'identity_counterfactual_savings', 'final_firms', 'model_calls', 'api_cost_usd']
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for r in sorted(episodes, key=lambda r: (r['task_id'], r['seed'], r['world'], r['arm'])):
        e = r['evaluation']
        writer.writerow(dict(run=r['run'], task_id=r['task_id'], seed=r['seed'], world=r['world'],
            arm=r['arm'], valid=r['validity']['ok'], rounds=len(r['trace']),
            registered_round=e['first_registration_round'], fragmentation=e['strategic_fragmentation'],
            behavioral_evasion=e['behavioral_evasion'], profit=e['profit'], actual_fines=e['fines'],
            identity_counterfactual_savings=e['potential_identity_fine_savings'],
            final_firms=e['final_firm_count'], model_calls=r['model_calls'], api_cost_usd=r['api_cost_usd']))
    payloads = {
        'episodes.jsonl': ''.join(json.dumps(r, sort_keys=True, allow_nan=False) + '\n' for r in episodes).encode(),
        'calls.jsonl': ''.join(json.dumps(c, sort_keys=True, allow_nan=False) + '\n' for c in calls).encode(),
        'episode-results.csv': buf.getvalue().encode(),
        'run-receipts.json': encode(receipts),
        'provenance.json': encode({'attempt': attempt, 'bundles': len(verified), 'episodes': len(episodes),
            'model_calls': len(calls), 'source_artifact_sha256': source_hashes,
            'limitations': ['Owner-produced export and replay audit, not independent researcher review.',
                           'Calls, rounds and paired arms are not independent market samples.',
                           'Private thinking is discarded; billed accounting is retained.']})
    }
    # Fail closed on private endpoint/key formats. This complements schema selection, not a secrecy proof.
    import re
    combined = b'\n'.join(payloads.values())
    assert not re.search(rb'(?:sk-ant-|Bearer |https?://[^\s"<>]*sslip\.io|SWARM_HUB_TOKEN)', combined)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    for name in ('episode-results.csv', 'run-receipts.json', 'provenance.json'):
        (output / name).write_bytes(payloads[name])
    with zipfile.ZipFile(output / 'records.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    (output / 'archive-sha256.json').write_bytes(encode({
        'records.zip': hashlib.sha256((output / 'records.zip').read_bytes()).hexdigest(),
        'members': {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()}}))
    print(json.dumps({'attempt': attempt, 'bundles': len(verified), 'episodes': len(episodes),
                      'calls': len(calls), 'zip_bytes': (output / 'records.zip').stat().st_size}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('base'); p.add_argument('attempt'); p.add_argument('verified'); p.add_argument('output')
    p.add_argument('--expected-episodes', type=int, required=True)
    a = p.parse_args()
    archive(a.base, a.attempt, a.verified, a.output, a.expected_episodes)
