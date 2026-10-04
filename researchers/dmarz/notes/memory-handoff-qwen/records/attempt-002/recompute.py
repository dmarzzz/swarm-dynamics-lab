"""Independent recomputation of attempt 002 from the saved rows. Uses only the rows' answers and
evaluator labels for the outcome classes (no call into analyze.py), then compares with the pinned
package's analyze.py and scorer and with the saved analysis.json."""
import gzip, json, math, random, sys, collections, hashlib
from pathlib import Path
# usage: python3 recompute.py <package directory at commit 5831e534> [output.json]
#   the package: git archive 5831e534 researchers/dmarz/notes/memory-handoff-qwen | tar -x -C <dir>
R = Path(__file__).resolve().parent; PIN = Path(sys.argv[1])
status = json.load(open(R / 'chain-status.json'))
def rows_of(stage):
    return [json.loads(l) for l in gzip.open(R / f'{stage.lower()}-episodes.jsonl.gz', 'rt')], stage.lower()
STATES = ('clean', 'misquote', 'stale', 'copies', 'contradiction', 'false_original'); POLICIES = ('raw', 'metadata', 'content', 'reset')
def outcome(r):
    v = r['answer']['value']; e = r['evaluator']
    if v is None: return 'abstain'
    if v == e['truth_answer']: return 'correct'
    if e['false_answer'] is not None and v == e['false_answer']: return 'inherited_error'
    return 'other_wrong'
s1, s1dir = rows_of('S1'); q0, q0dir = rows_of('Q0'); p0, p0dir = rows_of('P0')
assert len(s1) == 576 and all(r['status'] == 'completed' for r in s1) and len({r['id'] for r in s1}) == 576
by = {(r['root'], r['state'], r['policy']): r for r in s1}; roots = sorted({r['root'] for r in s1}); assert len(roots) == 24 and len(by) == 576
ie = lambda root, s, p: int(outcome(by[(root, s, p)]) == 'inherited_error')
d = [((ie(r, 'misquote', 'content') - ie(r, 'misquote', 'metadata')) + (ie(r, 'stale', 'content') - ie(r, 'stale', 'metadata'))) / 2 for r in roots]
rng = random.Random(20261004); means = sorted(math.fsum(d[rng.randrange(24)] for _ in range(24)) / 24 for _ in range(10000))
out = {'primary': {'mean': math.fsum(d) / 24, 'root_values': dict(zip(roots, d)), 'interval95': [means[250], means[9750]],
                   'distinct_values': sorted(set(d)), 'by_state': {s: math.fsum(ie(r, s, 'content') - ie(r, s, 'metadata') for r in roots) / 24 for s in ('misquote', 'stale')}}}
table = {}
for s in STATES:
    for p in POLICIES:
        c = collections.Counter(outcome(by[(r, s, p)]) for r in roots)
        sup = sum(by[(r, s, p)]['evaluation']['supported'] for r in roots)
        table[f'{s}/{p}'] = {'correct': c['correct'], 'inherited_error': c['inherited_error'], 'abstain': c['abstain'], 'other_wrong': c['other_wrong'], 'supported': sup,
                             'expected': by[(roots[0], s, p)]['evaluator']['expected_code']}
out['table'] = table
out['unsupported_rows'] = [{'id': r['id'], 'answer': r['answer'], 'reference': r['reference'], 'truth': r['evaluator']['truth_answer'], 'false': r['evaluator']['false_answer'],
                            'outcome': outcome(r), 'work_report': r['work_report'], 'raw': r['raw']} for r in s1 if r['evaluation']['supported'] != 1]
out['supported_total'] = sum(r['evaluation']['supported'] for r in s1)
def wilson(k, n, z=1.959963984540054):
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [max(0, c - h), min(1, c + h)]
out['clean'] = {p: {'correct': table[f'clean/{p}']['correct'], 'wilson95': wilson(table[f'clean/{p}']['correct'], 24)} for p in POLICIES}
out['qualification'] = {'rows': len(p0 + q0), 'valid': sum(r['status'] == 'completed' for r in p0 + q0), 'supported': sum(r['evaluation']['supported'] for r in p0 + q0),
                        'by_cell': {f"{r['state']}/{r['policy']}": [r['answer']['value'], r['reference']['value'], r['evaluation']['supported']] for r in p0 + q0}}
wr = collections.Counter()
for r in s1:
    for k, v in r['work_report'].items(): wr[k] += int(v == 1)
    for k, v in r['tolerated'].items(): wr['tol_' + k] += int(bool(v))
out['work'] = dict(wr)
out['work_by_policy'] = {p: {k: sum(int(r['work_report'][k] == 1) for r in s1 if r['policy'] == p) for k in ('listing_matches_message', 'follows_from_own_listing', 'counting_values_consistent', 'distinct_origins_consistent')} for p in POLICIES}
out['listing_mismatch_rows'] = [{'id': r['id'], 'supported': r['evaluation']['supported'], 'work_report': r['work_report'], 'records': r['raw'].get('records')} for r in s1 if r['work_report']['listing_matches_message'] != 1]
acc = [r['accounting'] for r in s1]
out['usage'] = {'input_tokens': sum(a['input_tokens'] for a in acc), 'output_tokens': sum(a['output_tokens'] for a in acc), 'cost_usd': math.fsum(a['actual_usd'] for a in acc),
                'attempts': sum(a['attempts'] for a in acc), 'max_output_tokens': max(a['output_tokens'] for a in acc), 'max_input_tokens': max(a['input_tokens'] for a in acc),
                'latency_mean': math.fsum(a['latency_seconds'] for a in acc) / 576, 'latency_max': max(a['latency_seconds'] for a in acc),
                'models': sorted({a['response_model'] for a in acc}), 'providers': sorted({a['response_provider'] for a in acc}), 'reasoning_tokens': sum(a.get('reasoning_tokens') or 0 for a in acc),
                'reported_cost_rows': sum(a.get('provider_reported_usd') is not None for a in acc), 'earlier_http': sum('earlier_http_status' in a for a in acc)}
out['per_policy_usage'] = {p: {'input_tokens': sum(r['accounting']['input_tokens'] for r in s1 if r['policy'] == p), 'output_tokens': sum(r['accounting']['output_tokens'] for r in s1 if r['policy'] == p),
                               'cost_usd': round(math.fsum(r['accounting']['actual_usd'] for r in s1 if r['policy'] == p), 6),
                               'registry_lookups': sum(r['retrieval']['registry_lookups'] for r in s1 if r['policy'] == p), 'records_retrieved': sum(r['retrieval']['records_retrieved'] for r in s1 if r['policy'] == p),
                               'bytes': sum(r['retrieval']['bytes'] for r in s1 if r['policy'] == p), 'seconds': math.fsum(r['retrieval'].get('seconds', 0) for r in s1 if r['policy'] == p)} for p in POLICIES}
out['distinct_packets'] = len({r['packet_hash'] for r in s1})
# identical packets answered differently?
groups = collections.defaultdict(list)
for r in s1: groups[r['packet_hash']].append(json.dumps(r['answer'], sort_keys=True))
out['identical_packets'] = {'groups_with_repeats': sum(len(v) > 1 for v in groups.values()), 'groups_with_differing_answers': sum(len(set(v)) > 1 for v in groups.values())}
# pinned code: analyze and regrade
sys.path.insert(0, str(PIN / 'src'))
import study, sim, analyze, journal, manifest as man
assert study.source_hash() == status['source_hash'] == '10f51d2c5d2023fc82df57b2c26173c32aceae1fca4e443971b2686d9a019689'
saved = json.load(open(R / 's1-analysis.json')); again = json.loads(json.dumps(analyze.analyze(s1)))
def close(a, b):
    if isinstance(a, bool) or isinstance(b, bool): return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(a, dict) and isinstance(b, dict): return set(a) == set(b) and all(close(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list): return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    return a == b
ref = man.load(); checks = {}
checks['analysis_recomputed_equals_saved'] = close(saved, again)
checks['independent_primary_equals_analysis'] = close(out['primary']['mean'], saved['primary']['estimate']) and close(out['primary']['interval95'], saved['primary']['interval95']) \
    and close([x['value'] for x in saved['primary']['root_values']], d)
for stage, (rows, directory) in (('S1', (s1, s1dir)), ('Q0', (q0, q0dir)), ('P0', (p0, p0dir))):
    assigned = [json.loads(l) for l in gzip.open(R / f'{directory}-assignments.jsonl.gz', 'rt')]; by_id = {a['id']: a for a in assigned}
    checks[stage + '_manifest_digest'] = man.stage_entry(assigned)['digest'] == ref['stages'][stage]['digest']
    checks[stage + '_packets_regenerate'] = all(study.rebuild(a) == a for a in assigned)
    ok = True
    for r in rows:
        full = study.revalidate(r); a = by_id[r['id']]
        ok = ok and study.stored(full)['answer'] == r['answer'] and study.stored(full)['tolerated'] == r['tolerated'] and close(study.evaluate(a, full), r['evaluation']) \
            and sim.reference(a['packet']) == r['reference'] and sim.work_report(a['packet'], full) == r['work_report'] and outcome(r) == r['evaluation']['outcome']
    checks[stage + '_rows_regraded'] = ok
    with gzip.open(R / f'{directory}-events.jsonl.gz', 'rt') as f: events = journal.read_events(f)
    checks[stage + '_journal_intact'] = journal.call_ledger_complete(events) and {e['id']: e['status'] for e in events if e['kind'] == 'terminal'} == {r['id']: r['status'] for r in rows}
q = study.qualification(p0 + q0); checks['qualification_gate_recomputed'] = q['passed'] and q['supported'] == 24
out['checks'] = checks; out['saved_guard'] = saved['utility_guard']['by_policy']; out['saved_forgetting'] = saved['forgetting']; out['saved_secondary'] = {k: {x: v[x] for x in ('estimate', 'interval95', 'roots')} for k, v in saved['secondary_contrasts'].items()}
out['guard_diffs'] = {k: {x: saved['utility_guard'][k][x] for x in ('estimate', 'interval95', 'roots')} for k in ('content_minus_raw', 'content_minus_metadata')}
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else R / 'recomputed.json', 'w'), indent=1, sort_keys=True)
print(json.dumps({k: out[k] for k in ('checks', 'supported_total', 'distinct_packets', 'identical_packets', 'work', 'usage')}, indent=1))
print(json.dumps(out['primary']['mean']), out['primary']['interval95'], out['primary']['distinct_values'], out['primary']['by_state'])
for k, v in table.items(): print(k, v)
print(json.dumps(out['qualification']['supported']), out['clean'])
print('UNSUPPORTED', json.dumps(out['unsupported_rows'])[:6000])
