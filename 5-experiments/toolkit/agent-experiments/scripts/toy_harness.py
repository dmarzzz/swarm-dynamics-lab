#!/usr/bin/env python3
"""Offline scripted policies only. No model SDK, network, credentials or paid calls."""
import argparse
import hashlib
import json
import math
import platform
import random
import statistics
from pathlib import Path
from contracts import canonical, check, digest

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ('naive_global', 'provenance_global', 'no_communication', 'provenance_ring')


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def rng(config, *keys):
    return random.Random(int(digest([config['master_seed'], config['study_id'], *keys]), 16))


def validate_config(config):
    check(config, json.loads((ROOT / 'schemas/toy-config.schema.json').read_text()))
    if len(config['conditions']) != len(set(config['conditions'])):
        raise ValueError('Duplicate conditions')
    if not {config['primary_control'], config['primary_treatment']} <= set(config['conditions']):
        raise ValueError('Primary contrast must be in conditions')
    if config['primary_control'] == config['primary_treatment']:
        raise ValueError('Primary contrast must contain distinct conditions')
    if config['scenarios'] < 2 or config['replicates'] < 1:
        raise ValueError('Need at least two scenario clusters')
    if config['agents'] % 2 != 1:
        raise ValueError('This toy requires odd agent count for majority decisions')


def initialize(config, scenario, replicate):
    # A scenario is a independently generated sensor-quality parameter. Repetitions
    # get fresh truth and measurements; all treatments get the same paired world.
    quality = rng(config, 'scenario', scenario).uniform(0.55, 0.90)
    environment = rng(config, 'environment', scenario, replicate)
    truth = environment.randrange(2)
    signals = [truth if environment.random() < quality else 1-truth for _ in range(config['agents'])]
    return {'quality': quality, 'truth': truth, 'signals': signals}


def observe(world, condition, agent, copies):
    signals = world['signals']
    if condition == 'no_communication':
        sources = [agent]
    elif condition == 'provenance_ring':
        sources = sorted({agent, (agent-1) % len(signals), (agent+1) % len(signals)})
    else:
        sources = list(range(len(signals)))
    # Multiple copies retain their source ID; repetition creates no new evidence.
    return [{'source_id': s, 'value': signals[s]}
            for s in sources for _ in range(copies if s == 0 else 1)]


def decide(observation, condition, own_signal):
    evidence = observation
    if condition.startswith('provenance'):
        evidence = list({x['source_id']: x for x in observation}.values())
    ones = sum(x['value'] for x in evidence)
    return own_signal if 2*ones == len(evidence) else int(2*ones > len(evidence))


def summarize(config, outcomes):
    lookup = {(o['scenario_id'], o['replicate'], o['condition']): o['score'] for o in outcomes}
    differences = []
    for s in range(config['scenarios']):
        sid = 's%03d' % s
        differences.append(statistics.mean(
            lookup[sid, r, config['primary_treatment']] - lookup[sid, r, config['primary_control']]
            for r in range(config['replicates'])))
    stream = rng(config, 'analysis-bootstrap')
    boot = sorted(statistics.mean(stream.choices(differences, k=len(differences)))
                  for _ in range(config['bootstrap_samples']))
    lo = boot[int(.025*(len(boot)-1))]
    hi = boot[int(.975*(len(boot)-1))]
    sd = .25
    n_power = math.ceil(((1.9599639845 + .8416212336)*sd/.10)**2)
    n_precision = math.ceil((1.9599639845*sd/.05)**2)
    se = math.sqrt(.18**2/60 + .20**2/(60*4))
    normal = statistics.NormalDist()
    power = 1-normal.cdf(1.9599639845-.08/se)+normal.cdf(-1.9599639845-.08/se)
    return {'warning': 'SCRIPTED TOY OUTPUT; NOT LLM OR HUMAN EVIDENCE',
            'planned_runs': config['scenarios']*config['replicates']*len(config['conditions']),
            'completed_runs': len(outcomes), 'primary_contrast': [config['primary_treatment'], config['primary_control']],
            'mean_paired_difference': statistics.mean(differences),
            'scenario_cluster_percentile_ci_95': [lo, hi],
            'ci_scope': 'Illustrative bootstrap across sampled sensor-quality scenarios; no confirmatory LLM inference',
            'scenario_mean_differences': differences,
            'condition_means': {c: statistics.mean(o['score'] for o in outcomes if o['condition'] == c) for c in config['conditions']},
            'api_calls': 0, 'api_cost_usd': 0,
            'planning_example_only': {'independent_pairs_power': n_power, 'independent_pairs_precision': n_precision,
                                      'nested_standard_error': se, 'nested_half_width_95': 1.9599639845*se,
                                      'nested_approx_power': power}}


def run(config, out):
    validate_config(config)
    out.mkdir(parents=True, exist_ok=False)
    dump(out / 'config.resolved.json', config)
    plan = []
    for s in range(config['scenarios']):
        for r in range(config['replicates']):
            conditions = config['conditions'][:]
            rng(config, 'assignment', s, r).shuffle(conditions)
            for condition in conditions:
                plan.append({'schema_version':'1.0','study_id':config['study_id'],
                             'run_id':f's{s:03d}-r{r:03d}-{condition}', 'scenario_id':f's{s:03d}',
                             'replicate':r,'condition':condition})
    dump(out / 'planned-runs.json', plan)
    outcomes = []
    with (out / 'events.jsonl').open('w') as events_file:
        for item in plan:
            s = int(item['scenario_id'][1:])
            # New world on every condition; named stream ensures paired identity.
            world = initialize(config, s, item['replicate'])
            seq, previous = 0, '0'*64
            def emit(kind, payload, agent=None):
                nonlocal seq, previous
                event = {**item,'seq':seq,'type':kind,'agent_id':agent,
                         'parent_seq':seq-1 if seq else None,'payload':payload,'prev_hash':previous}
                event['event_hash'] = digest(event)
                events_file.write(canonical(event).decode()+'\n')
                previous = event['event_hash']
                seq += 1
            initial_hash = digest(world)
            emit('run_start', {'initial_sha256':initial_hash, 'policy_revision':'scripted-majority-v1'})
            decisions = []
            for agent in range(config['agents']):
                observed = observe(world, item['condition'], agent, config['repeated_source_copies'])
                emit('observation', {'evidence':observed, 'own_signal':world['signals'][agent]}, f'a{agent}')
                action = decide(observed, item['condition'], world['signals'][agent])
                decisions.append(action)
                emit('decision', {'value':action}, f'a{agent}')
            # Hidden truth is used only by the evaluator, after all decisions.
            score = sum(d == world['truth'] for d in decisions)/len(decisions)
            group_correct = int(sum(decisions)*2 > len(decisions)) == world['truth']
            emit('evaluation', {'truth':world['truth'],'score':score,'group_correct':group_correct})
            emit('run_end', {'status':'completed','decisions':len(decisions),'api_calls':0,'api_cost_usd':0})
            outcomes.append({**item,'initial_sha256':initial_hash,'status':'completed','score':score,
                             'group_correct':group_correct,'decisions':len(decisions),'api_calls':0,
                             'api_cost_usd':0.0,'final_event_hash':previous})
    (out / 'outcomes.jsonl').write_text(''.join(canonical(x).decode()+'\n' for x in outcomes))
    dump(out / 'summary.json', summarize(config, outcomes))
    sources = ['scripts/toy_harness.py','scripts/contracts.py','schemas/toy-config.schema.json',
               'schemas/event.schema.json','schemas/outcome.schema.json']
    dump(out / 'manifest.json', {'schema_version':'1.0','python':platform.python_version(),
         'configuration_sha256':digest(config), 'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
         'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file()},
         'security_boundary':'in-process scripted toy; no untrusted code isolation',
         'cost_scope':'zero provider calls; local CPU and human preparation time not metered'})
    return outcomes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text())
        results = run(config, args.out)
    except (ValueError, OSError):
        # Deliberately no raw exception or request dump.
        raise SystemExit('Preflight/execution failed; check config and use a new output directory.')
    print(f'Completed {len(results)} scripted runs; 0 provider calls; toy output only.')
