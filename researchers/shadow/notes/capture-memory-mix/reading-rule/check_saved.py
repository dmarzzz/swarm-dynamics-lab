#!/usr/bin/env python3
"""Independent same-author stdlib recomputation. No runner imports or network access."""
import csv
from collections import Counter
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import random
import statistics

ROOT = Path(__file__).resolve().parent
NAMES = ('Cedar', 'Raven')
ALLOWED_MODELS = {'openai/gpt-4o-mini', 'openai/gpt-4o-mini-2024-07-18',
                  'gpt-4o-mini', 'gpt-4o-mini-2024-07-18'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def reference_score(body, require_provider):
    try:
        if body['model'] not in ALLOWED_MODELS:
            return None
        if require_provider and (not isinstance(body.get('provider'), str) or not body['provider'].strip()):
            return None
        choice = body['choices'][0]['message']['content'].strip()
        if choice not in NAMES:
            return None
        mass = {name: 0.0 for name in NAMES}
        for token in body['choices'][0]['logprobs']['content'][0]['top_logprobs']:
            text = token['token'].strip().lower()
            if text:
                for name in NAMES:
                    if name.lower().startswith(text):
                        mass[name] += math.exp(float(token['logprob']))
        total = sum(mass.values())
        if not .8 <= total <= 1.00001:
            return None
        return {'choice': choice, 'mass': total, 'p': {k: v / total for k, v in mass.items()}}
    except (KeyError, IndexError, TypeError, ValueError, OverflowError):
        return None


def interval(values):
    if not values:
        return [None, None]
    rng = random.Random(20261004)
    means = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(10000))
    return [means[249], means[9749]]


def check():
    data = json.loads((ROOT / 'input.json').read_text())
    assert digest((ROOT / 'input.json').read_bytes()) == 'c9d24c92ff32abbdd3c961bb4446f07edf60ba9aff330417b5436b4cc71f2639'
    assignments = {a['id']: a for a in data['assignments']}
    histories = {h['id']: h for h in data['histories']}
    totals = Counter()
    stage_rows = []
    all_rows = []
    selected = {}
    known_cost = Decimal('0')
    unknown_bound = Decimal('0')
    reserved = Decimal('0')
    providers = Counter()
    for attempt, directory in [('v1', 'results'), ('R2', 'results-r2')]:
        rows = [json.loads(line) for line in (ROOT / directory / 'journal.jsonl').read_text().splitlines() if line.strip()]
        starts = {x['id']: x for x in rows if x['event'] == 'start'}
        terminals = {x['id']: x for x in rows if x['event'] == 'terminal'}
        assert len(starts) == sum(x['event'] == 'start' for x in rows)
        assert len(terminals) == sum(x['event'] == 'terminal' for x in rows)
        assert terminals.keys() <= starts.keys() <= assignments.keys()
        for start in starts.values():
            encoded = json.dumps(assignments[start['id']]['body'], sort_keys=True, separators=(',', ':')).encode()
            assert digest(encoded) == start['request_sha256']
            assert Decimal(str(start['reservation_usd'])) == Decimal('.05')
        for stage in ['S0', 'S1']:
            ids = [a['id'] for a in data['assignments'] if a['stage'] == stage]
            counts = Counter(assigned=len(ids))
            for identity in ids:
                start = starts.get(identity)
                terminal = terminals.get(identity)
                response = (terminal or {}).get('response', {})
                score = reference_score(response, attempt == 'R2')
                counts['started'] += bool(start)
                counts['terminal'] += bool(terminal)
                counts['valid'] += score is not None
                counts['invalid_terminal'] += bool(terminal) and score is None
                counts['unstarted'] += start is None
                counts['ambiguous_started'] += bool(start) and terminal is None
                if start:
                    reservation = Decimal(str(start['reservation_usd']))
                    reserved += reservation
                    cost = (response.get('usage') or {}).get('cost')
                    if cost is None:
                        counts['cost_unknown_started'] += 1
                        unknown_bound += reservation
                    else:
                        value = Decimal(str(cost))
                        assert value.is_finite() and 0 <= value <= reservation
                        known_cost += value
                if attempt == 'R2' and score:
                    selected[identity] = score
                    providers[response['provider']] += 1
                    stored = terminal['score']
                    assert stored['valid'] and stored['choice'] == score['choice']
                    assert all(abs(stored['p'][k] - score['p'][k]) < 1e-12 for k in NAMES)
                all_rows.append({'attempt': attempt, 'id': identity, 'stage': stage, 'started': bool(start),
                                 'terminal': bool(terminal), 'valid': score is not None,
                                 'status': 'valid' if score else ('invalid' if terminal else ('ambiguous' if start else 'unstarted'))})
            stage_rows.append({'attempt': attempt, 'stage': stage, **counts})
            totals.update(counts)
    assert reserved <= Decimal('8')
    assert totals['started'] <= 157
    summary = json.loads((ROOT / 'results-r2/summary.json').read_text())
    r2 = [x for x in stage_rows if x['attempt'] == 'R2']
    for field in ('started', 'terminal', 'valid', 'assigned'):
        assert summary[field] == sum(x[field] for x in r2), field
    scientific = [h for h in data['histories'] if h['stage'] == 'S1']
    contrasts = {}
    for name, suffix, absolute in [
        ('primary_abs_raw_reverse_minus_chrono', 'raw-reversed', True),
        ('abs_raw_shuffle_minus_chrono', 'raw-shuffled', True),
        ('signed_summary_chrono_minus_raw_chrono', 'summary-chronological', False)]:
        values = []
        for history in scientific:
            baseline = selected.get(history['id'] + '-raw-chronological')
            treatment = selected.get(history['id'] + '-' + suffix)
            if baseline and treatment:
                difference = treatment['p'][history['majority']] - baseline['p'][history['majority']]
                values.append(abs(difference) if absolute else difference)
        checked = {'n_histories': len(values), 'mean': statistics.mean(values) if values else None,
                   'ci95': interval(values)}
        if absolute:
            checked['all_assigned_missingness_bounds'] = [sum(values) / 24, (sum(values) + (24 - len(values))) / 24]
        assert summary['contrasts'][name] == checked, name
        contrasts[name] = checked
    csv_rows = list(csv.DictReader((ROOT / 'results-r2/scored.csv').open()))
    assert len(csv_rows) == 156
    svg = (ROOT / 'results-r2/paired-history.svg').read_text()
    for row in csv_rows:
        score = selected.get(row['id'])
        assert (row['valid'] == 'True') == bool(score)
        if score:
            probability = score['p'][histories[row['history']]['majority']]
            assert abs(float(row['p_majority']) - probability) < 1e-12
            if row['stage'] == 'S1':
                assert f'{row["id"]}: {probability:.9f}</title>' in svg
    assert svg.count('<circle ') == sum(x['stage'] == 'S1' and x['valid'] == 'True' for x in csv_rows)
    for condition in summary['conditions']:
        cells = [x for x in csv_rows if x['stage'] == 'S1' and x['representation'] == condition['representation']
                 and x['order'] == condition['order'] and x['valid'] == 'True']
        assert condition['valid_histories'] == len(cells)
        assert condition['majority_choices'] == sum(x['choice'] == x['majority'] for x in cells)
        assert condition['last_choices'] == sum(x['choice'] == x['last'] for x in cells)
        if cells:
            assert condition['mean_p_majority'] == statistics.mean(float(x['p_majority']) for x in cells)
            assert condition['mean_p_last'] == statistics.mean(float(x['p_last']) for x in cells)
    for group in summary['strata']:
        cells = [x for x in csv_rows if x['stage'] == 'S1' and int(x['length']) == group['length']
                 and (x['conflict'] == 'True') == group['conflict'] and x['representation'] == group['representation']
                 and x['order'] == group['order'] and x['valid'] == 'True']
        assert group['valid_histories'] == len(cells)
        assert group['majority_choices'] == sum(x['choice'] == x['majority'] for x in cells)
        assert group['last_choices'] == sum(x['choice'] == x['last'] for x in cells)
        if cells:
            assert group['mean_p_majority'] == statistics.mean(float(x['p_majority']) for x in cells)
            assert group['mean_p_last'] == statistics.mean(float(x['p_last']) for x in cells)
    accounting = {'scope': 'reading-rule diagnostic only; historical swarm pilots remain separate',
                  'totals': dict(totals), 'stages': stage_rows, 'cap_usd': 8,
                  'actual_reported_usd': str(known_cost), 'unknown_cost_reserved_usd': str(unknown_bound),
                  'conservative_actual_cost_upper_bound_usd': str(known_cost + unknown_bound),
                  'actual_total_usd': str(known_cost) if not unknown_bound else None,
                  'retained_reservations_usd': str(reserved), 'r2_valid_providers': dict(providers),
                  'scientific_histories': 24, 'contrasts': contrasts,
                  'checker': 'same-author independent stdlib implementation; no runner imports',
                  'journal_sha256': {d: digest((ROOT / d / 'journal.jsonl').read_bytes()) for d in ['results', 'results-r2']}}
    (ROOT / 'accounting.json').write_text(json.dumps(accounting, indent=2) + '\n')
    with (ROOT / 'all-attempts.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)
    print(json.dumps(accounting, indent=2))
    print('PASS: raw scores, root accounting, paired contrasts, bootstrap intervals, CSV and figure match.')


if __name__ == '__main__':
    check()
