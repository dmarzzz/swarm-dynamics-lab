"""Post-run audit of saved PC-1L records. No provider calls or fitted thresholds."""
import argparse
import collections
import hashlib
import json
import statistics
from pathlib import Path
from instrument import CELLS, world, digest, deterministic


def score(m, truth, cells=CELLS):
    # Reference calculation independent of instrument.bounds/aggregate.
    values = [(m.get(c, 'UNKNOWN'), truth[c]) for c in cells]
    wrong = len([1 for p, t in values if p != 'UNKNOWN' and p != t])
    unknown = len([1 for p, _ in values if p == 'UNKNOWN'])
    return dict(wrong=wrong, missing=unknown, denominator=len(values),
                lower=wrong/len(values), upper=(wrong+unknown)/len(values))


def audit(root):
    records = json.loads((root/'records.json').read_text())
    summary = json.loads((root/'summary.json').read_text())
    manifest = json.loads((root/'manifest.json').read_text())
    assert len(records) == len({r['id'] for r in records}) == 522
    assert {r['id'] for r in records} == {r['id'] for r in manifest['assignments']}
    assert digest(manifest['assignments']) == manifest['sha256']
    assert all(r['status'] in ('valid', 'invalid', 'failed', 'timeout', 'not-started') for r in records)
    grouped = collections.defaultdict(list)
    usage = collections.defaultdict(lambda: dict(calls=0, input_tokens=0, output_tokens=0, cost_usd=0.0))
    reset_groups = collections.defaultdict(list)
    for r in records:
        if 'request' in r:
            assert digest(r['request']) == r['request_sha256']
            assert not {'truth', 'exposed', 'seed', 'history', 'communication'} & set(r['request']['state'])
        key = f"{r['kind']}/{r.get('communication')}/{r.get('state')}"
        usage[key]['calls'] += r['status'] != 'not-started'
        if r['status'] == 'valid':
            assert r['checked']['request_sha256'] == r['request_sha256']
            for k in ('input_tokens', 'output_tokens'):
                usage[key][k] += r['checked']['usage'][k]
            usage[key]['cost_usd'] += r['checked']['usage']['cost']
        if r['kind'] == 'swarm':
            grouped[r['seed'], r['history'], r['communication'], r['state'], r['step']].append(r)
            if r['step'] == 2 and r['state'] == 'reset':
                reset_groups[r['seed'], r['actor']].append(r)
    def mapping(r):
        return r.get('checked', {}).get('response', {}).get('map', {}) if r['status'] == 'valid' else {}
    def majority(rows):
        assert len(rows) == 3
        result = {}
        for cell in CELLS:
            votes = [mapping(r).get(cell, 'UNKNOWN') for r in rows]
            result[cell] = next((v for v in ('LAND', 'WATER') if votes.count(v) >= 2), 'UNKNOWN')
        return result
    trajectories = []
    history_disagreements = []
    for wd in summary['worlds']:
        w = world(wd['seed'], stage='S0')
        for t in wd['trajectories']:
            rows = grouped[wd['seed'], t['history'], t['communication'], t['state'], t['step']]
            m = majority(rows)
            assert m == t['map'] and score(m, w['truth']) == t['error']
            trajectories.append(dict(seed=wd['seed'], **{k:t[k] for k in ('history','communication','state','step')},
                                     whole=score(m,w['truth']),
                                     land=score(m,w['truth'],[c for c in CELLS if w['truth'][c]=='LAND']),
                                     exposed=score(m,w['truth'],w['exposed']),
                                     outside=score(m,w['truth'],[c for c in CELLS if c not in w['exposed']])))
        d = {}
        for comm in ('private','social'):
            for state in ('reset','retain'):
                a,b = [majority(grouped[wd['seed'],h,comm,state,2]) for h in ('A','B')]
                missing=sum(a[c]=='UNKNOWN' or b[c]=='UNKNOWN' for c in CELLS)
                unequal=sum(a[c]!='UNKNOWN' and b[c]!='UNKNOWN' and a[c]!=b[c] for c in CELLS)
                d[comm,state]=(unequal/36,(unequal+missing)/36)
                history_disagreements.append(dict(seed=wd['seed'],communication=comm,state=state,
                                                   lower=d[comm,state][0],upper=d[comm,state][1]))
        # social-retain - social-reset - private-retain + private-reset.
        signs=[(('social','retain'),1),(('social','reset'),-1),(('private','retain'),-1),(('private','reset'),1)]
        interval={key:sum(sign*d[arm][i if sign==1 else 1-i] for arm,sign in signs)
                  for i,key in enumerate(('lower','upper'))}
        assert interval == wd['history_interaction']
    reset = []
    for (seed, actor), rows in sorted(reset_groups.items()):
        assert len(rows) == 4 and len({r['request_sha256'] for r in rows}) == 1
        reset.append(dict(seed=seed,actor=actor,calls=4,unique_requests=1,
                          valid=sum(r['status']=='valid' for r in rows),
                          distinct_valid_maps=len({digest(mapping(r)) for r in rows if r['status']=='valid'})))
    clean = []
    deterministic_endpoint = []
    for r in records:
        w = world(r['seed'],stage='S0')
        if r['kind']=='clean':
            clean.append(dict(id=r['id'],**score(mapping(r),w['truth'])))
        if r['step']==2 and 'request' in r:
            deterministic_endpoint.append(score(deterministic(r['request']['state'])['map'],w['truth']))
    latency = [r['elapsed_seconds'] for r in records if 'elapsed_seconds' in r]
    return dict(audit='same-author post-run reference arithmetic; not independent researcher review',
                assignment_and_request_hashes_pass=True, reference_majority_and_scores_pass=True,
                reset_groups=reset, trajectories=trajectories, clean=clean,
                history_disagreements=history_disagreements,
                deterministic_endpoint_count=len(deterministic_endpoint),
                deterministic_endpoint_max_upper=max(x['upper'] for x in deterministic_endpoint),
                usage_by_condition=dict(usage),
                latency_seconds=dict(n=len(latency),median=statistics.median(latency),maximum=max(latency)),
                known_stage_cost_usd=sum(x['cost_usd'] for x in usage.values()),
                files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir()) if p.is_file()})


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('records_directory',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();a.output.write_text(json.dumps(audit(a.records_directory),indent=2)+'\n')
