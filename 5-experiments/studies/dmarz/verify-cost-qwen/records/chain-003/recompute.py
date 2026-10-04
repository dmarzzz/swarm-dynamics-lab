"""Independent recomputation of chain 003 from the saved rows and request texts (no use of sim.score or analyze)."""
import gzip, json, math, re, sys, statistics
from pathlib import Path
base = Path(sys.argv[1]) / 'results'; status = json.loads((base / 'chain-status.json').read_text())
def rows(stage, name='episodes.jsonl.gz'):
    d = base / Path(status['stages'][stage]['directory']).name
    return [json.loads(l) for l in gzip.open(d / name, 'rt') if l.strip()]
def graded(stage):
    req = {r['id']: r for r in rows(stage, 'requests.jsonl.gz')}; out = []
    for r in rows(stage):
        user = req[r['id']]['user']; report = re.search(r'Report, older \(1 cell\): cell (\d,\d) is', user).group(1)
        e = float(re.search(r'wrong with probability (\d\.\d\d)\.', user).group(1)); first, second = re.search(r'in this order: (\d,\d); (\d,\d)\.', user).groups()
        u = float(re.search(r'returned as UNKNOWN(?: with probability 1\.00, at cost| \| 1\.00 \|) (\d\.\d\d)', user).group(1))
        assert (e, u) == (r['error'], r['unknown_cost']) and r['status'] == 'completed'
        pick = r['answer']['inspect']; action = 'check' if pick == report else 'explore'; loss = u if action == 'check' else e
        out.append(dict(id=r['id'], layout=r['layout'], e=e, u=u, rep=r['representation'], action=action, regret=round(loss - min(e, u), 12),
                        optimal=loss == min(e, u), first=pick == first, acc=r['accounting'], work=r['answer'].get('work'), raw=r['answer'].get('raw'),
                        saved_regret=r['evaluation']['expected_regret'], saved_optimal=r['evaluation']['optimal'], realized=r['evaluation']['realized_scripted_loss']))
    return out
s1 = graded('S1'); q = graded('P0') + graded('Q0')
assert all(abs(x['regret'] - x['saved_regret']) < 1e-12 and x['optimal'] == x['saved_optimal'] for x in s1 + q)
out = {'s1_rows': len(s1), 'q_rows': len(q)}
out['qualification'] = {rep: {'optimal': sum(x['optimal'] for x in q if x['rep'] == rep), 'of': sum(x['rep'] == rep for x in q)} for rep in ('prose', 'table')}
cases = sorted({(x['e'], x['u']) for x in s1}); layouts = sorted({x['layout'] for x in s1}); by = {(x['layout'], x['e'], x['u'], x['rep']): x for x in s1}
strata = []
for e, u in cases:
    line = {'e': e, 'u': u, 'optimal_action': 'check' if e > u else 'explore', 'margin': round(abs(e - u), 2), 'always_check': round(max(0, u - e), 2), 'always_explore': round(max(0, e - u), 2)}
    for rep in ('prose', 'table'):
        mine = [by[(l, e, u, rep)] for l in layouts]
        line[rep] = {'optimal': sum(x['optimal'] for x in mine), 'check': sum(x['action'] == 'check' for x in mine), 'explore': sum(x['action'] == 'explore' for x in mine),
                     'mean_regret': sum(x['regret'] for x in mine) / 24}
    line['table_minus_prose'] = line['table']['mean_regret'] - line['prose']['mean_regret']; strata.append(line)
out['strata'] = strata
values = [sum(by[(l, e, u, 'table')]['regret'] - by[(l, e, u, 'prose')]['regret'] for e, u in cases) / 12 for l in layouts]
m = statistics.mean(values); sd = statistics.stdev(values); se = sd / math.sqrt(24)
out['primary'] = {'values': dict(zip(layouts, values)), 'mean': m, 'sd': sd, 'se': se, 'interval95_t23': [m - 2.0687 * se, m + 2.0687 * se], 'min': min(values), 'max': max(values),
                  'negative': sum(v < 0 for v in values), 'zero': sum(v == 0 for v in values), 'positive': sum(v > 0 for v in values),
                  'leave_one_out': [min((sum(values) - v) / 23 for v in values), max((sum(values) - v) / 23 for v in values)]}
for rep in ('prose', 'table'):
    mine = [x for x in s1 if x['rep'] == rep]
    out[rep] = {'mean_regret': sum(x['regret'] for x in mine) / len(mine), 'optimal': sum(x['optimal'] for x in mine), 'n': len(mine), 'first_listed': sum(x['first'] for x in mine),
                'check': sum(x['action'] == 'check' for x in mine), 'mean_realized_loss': sum(x['realized'] for x in mine) / len(mine)}
out['comparators'] = {'always_check': sum(max(0, u - e) for e, u in cases) / 12, 'always_explore': sum(max(0, e - u) for e, u in cases) / 12}
out['misses'] = [{k: x[k] for k in ('id', 'e', 'u', 'rep', 'action', 'regret', 'first')} for x in s1 if not x['optimal']]
allrows = s1 + q
def stat(key, xs): v = [x['acc'].get(key) for x in xs if x['acc'].get(key) is not None]; return {'n': len(v), 'sum': sum(v), 'mean': sum(v) / len(v), 'min': min(v), 'max': max(v)} if v else None
out['usage'] = {k: stat(k, allrows) for k in ('input_tokens', 'output_tokens', 'reasoning_tokens', 'visible_output_tokens', 'latency_seconds', 'actual_usd', 'attempts', 'cached_tokens')}
out['s1_usage'] = {k: stat(k, s1) for k in ('input_tokens', 'output_tokens', 'reasoning_tokens', 'latency_seconds', 'actual_usd')}
out['response_models'] = sorted({str(x['acc'].get('response_model')) for x in allrows}); out['finish'] = sorted({str(x['acc'].get('finish_reason')) for x in allrows})
out['input_pricing'] = sorted({str(x['acc'].get('input_pricing')) for x in allrows}); out['fingerprints'] = sorted({str(x['acc'].get('system_fingerprint')) for x in allrows})[:5]
out['tolerated'] = {'extra_keys': sum(bool(x['work'] and x['work'].get('extra_keys')) for x in allrows), 'inspect_respaced': sum(bool(x['work'] and x['work'].get('inspect_respaced')) for x in allrows)}
out['raw_examples'] = sorted({x['raw'] for x in allrows})[:3]; out['raw_lengths'] = sorted({len(x['raw']) for x in allrows})
out['qualification_rows'] = [{k: x[k] for k in ('id', 'e', 'u', 'rep', 'action', 'optimal', 'first')} for x in q]
print(json.dumps(out, indent=1))
