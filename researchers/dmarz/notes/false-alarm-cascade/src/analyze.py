"""Root-level descriptive analysis of saved call rows.

The unit is the world root. Every planned decision keeps its place: a decision that was not
observed (failed or not started call) is bounded at 0 and 1, never dropped and never set to a
zero effect. Agents, rounds, resources and calls are not independent samples.
"""
import gzip
import json
import math
from collections import defaultdict
from statistics import NormalDist

import numpy as np

import study

_INDEX = {}
BOUNDED = {                       # name -> (numerator from an evaluation, decisions per call row)
    'use_x': (lambda e: e['use_x'], 1),
    'use_h': (lambda e: e['use_h'], 1),
    'use_mates': (lambda e: e['use_mates'], 2),
    'use_other_real': (lambda e: e['use_other_real'], 5),
    'ref_claims_use_x': (lambda e: e['ref_use_x']['claims'], 1),
    'ref_credulous_use_x': (lambda e: e['ref_use_x']['credulous'], 1),
    'ref_private_use_x': (lambda e: e['ref_use_x']['private'], 1),
}


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f:
        return [json.loads(line) for line in f]


def boot_index(n):
    """Resampled roots, shared by every interval over the same number of roots (paired by root)."""
    a = study.design()['analysis']
    if n not in _INDEX:
        _INDEX[n] = np.random.default_rng(a['bootstrap_seed']).integers(0, n, (a['bootstrap_draws'], n))
    return _INDEX[n]


def interval(values):
    if not values:
        return None
    a = np.array(values, dtype=float)
    boot = a[boot_index(len(a))].mean(axis=1)
    return [float(x) for x in np.quantile(boot, [.025, .975])]


def mean(values):
    values = [float(v) for v in values]
    return math.fsum(values) / len(values) if values else None


class Cells:
    """Rows of one actor, indexed by (root, condition)."""

    def __init__(self, rows):
        self.by = defaultdict(list)
        for r in rows:
            self.by[(r['root'], r['condition'])].append(r)
        self.roots = sorted({k[0] for k in self.by})

    def window(self, root, condition, rounds, metric):
        """Observed sum, observed decisions and planned decisions for one root, condition and window."""
        fn, per = BOUNDED[metric]
        rows = [r for r in self.by.get((root, condition), []) if r['round'] in rounds]
        good = [r for r in rows if r['status'] == 'completed']
        return sum(fn(r['evaluation']) for r in good), per * len(good), per * len(rows)

    def rate(self, root, condition, rounds, metric):
        s, n, planned = self.window(root, condition, rounds, metric)
        if not planned:
            return None
        return {'value': s / planned if n == planned else None, 'low': s / planned,
                'high': (s + planned - n) / planned, 'observed': n, 'planned': planned}

    def contrast(self, a, b, rounds, metric):
        """Mean over roots of rate(a) - rate(b), paired by root, with bounds for missing decisions."""
        complete, low, high, per_root = [], [], [], []
        for root in self.roots:
            ra, rb = self.rate(root, a, rounds, metric), self.rate(root, b, rounds, metric)
            if ra is None or rb is None:
                continue
            low.append(ra['low'] - rb['high'])
            high.append(ra['high'] - rb['low'])
            difference = ra['value'] - rb['value'] if ra['value'] is not None and rb['value'] is not None else None
            if difference is not None:
                complete.append(difference)
            per_root.append({'root': root, 'difference': difference, a: ra['value'], b: rb['value']})
        full = bool(per_root) and len(complete) == len(per_root)
        return {'contrast': f'{a} minus {b}', 'metric': metric, 'rounds': list(rounds),
                'roots': len(per_root), 'complete_roots': len(complete),
                'mean': mean(complete) if full else None,
                'interval': interval(complete) if full else None,
                'all_assigned_bounds': [mean(low), mean(high)] if per_root else None,
                'complete_case_mean': mean(complete), 'per_root': per_root}

    def pooled(self, condition, rounds, metric):
        """Pooled rate over roots: observed decisions only, with the planned count beside it."""
        s = n = planned = 0
        for root in self.roots:
            a, b, c = self.window(root, condition, rounds, metric)
            s, n, planned = s + a, n + b, planned + c
        return {'mean_observed': s / n if n else None, 'observed': n, 'planned': planned}


def share(numerator, denominator, floor=0.05):
    """Share of an effect that remains: ratio of two root-mean contrasts, with a root bootstrap of the
    ratio. Not computed when either contrast is incomplete or the denominator is under 5 points."""
    out = {'numerator': numerator['mean'], 'denominator': denominator['mean'], 'share': None, 'interval': None,
           'note': None}
    if numerator['mean'] is None or denominator['mean'] is None:
        out['note'] = 'incomplete roots'
        return out
    if abs(denominator['mean']) < floor:
        out['note'] = 'denominator under 5 points; share not computed'
        return out
    num = np.array([p['difference'] for p in numerator['per_root']], dtype=float)
    den = np.array([p['difference'] for p in denominator['per_root']], dtype=float)
    index = boot_index(len(num))
    dens = den[index].mean(axis=1)
    ok = np.abs(dens) >= 1e-9
    out['share'] = float(num.mean() / den.mean())
    out['interval'] = [float(x) for x in np.quantile(num[index].mean(axis=1)[ok] / dens[ok], [.025, .975])]
    return out


def detection(hits, misses, false_alarms, correct_rejections):
    """Hit rate, false-alarm rate, d' and criterion c with the log-linear correction. The signal is
    "honeypot" and the response is "skip"."""
    signal, noise = hits + misses, false_alarms + correct_rejections
    if not signal or not noise:
        return {'hits': hits, 'signal': signal, 'false_alarms': false_alarms, 'noise': noise,
                'hit_rate': None, 'false_alarm_rate': None, 'd_prime': None, 'criterion': None}
    z = NormalDist().inv_cdf
    zh, zf = z((hits + 0.5) / (signal + 1)), z((false_alarms + 0.5) / (noise + 1))
    return {'hits': hits, 'signal': signal, 'false_alarms': false_alarms, 'noise': noise,
            'hit_rate': hits / signal, 'false_alarm_rate': false_alarms / noise,
            'd_prime': zh - zf, 'criterion': -(zh + zf) / 2}


def analyze_actor(rows):
    d = study.design()
    w = d['windows']
    cascade, after = w['cascade'], w['after_correction']
    cells = Cells(rows)
    conditions = [c for c in d['conditions'] if any(k[1] == c for k in cells.by)]
    if not conditions:
        return None

    primary = cells.contrast('C0', 'FA+C', after, 'use_x')
    primary.update(name='residual avoidance of X after correction', useful_difference_pp=d['primary_contrast']['useful_difference_pp'],
                   status='exploratory, descriptive')
    secondary = {
        'cascade_size': {'C0-FA': cells.contrast('C0', 'FA', cascade, 'use_x'),
                         'C0-FA+C': cells.contrast('C0', 'FA+C', cascade, 'use_x')},
        'persistence_without_correction': cells.contrast('C0', 'FA', after, 'use_x'),
        'spillover': {f'{metric}|{b}|{name}': cells.contrast('C0', b, rounds, metric)
                      for metric in ('use_mates', 'use_other_real') for b in ('FA', 'FA+C')
                      for name, rounds in (('cascade', cascade), ('after_correction', after))},
        'true_alarm': {'C0-TA|cascade': cells.contrast('C0', 'TA', cascade, 'use_h'),
                       'C0-TA+C|cascade': cells.contrast('C0', 'TA+C', cascade, 'use_h'),
                       'C0-TA|after_correction': cells.contrast('C0', 'TA', after, 'use_h'),
                       'C0-TA+C|after_correction': cells.contrast('C0', 'TA+C', after, 'use_h')},
        'false_retraction_harm': cells.contrast('TA+C', 'TA', after, 'use_h'),
        'reference_on_same_boards': {p: cells.contrast('C0', 'FA+C', after, f'ref_{p}_use_x')
                                     for p in d['reference']['policies']},
    }
    secondary['asymmetry'] = {
        'false_alarm_share_remaining': share(primary, secondary['cascade_size']['C0-FA+C']),
        'true_alarm_share_remaining': share(secondary['true_alarm']['C0-TA+C|after_correction'],
                                            secondary['true_alarm']['C0-TA+C|cascade']),
        'note': 'share of the round 2-3 effect still present in rounds 4-6; the hunch says the false-alarm share is the larger'}

    rounds_all = range(1, d['world']['rounds'] + 1)
    by_round = {c: [{'round': t, 'use_x': cells.pooled(c, [t], 'use_x'), 'use_h': cells.pooled(c, [t], 'use_h'),
                     'use_mates': cells.pooled(c, [t], 'use_mates'), 'use_other_real': cells.pooled(c, [t], 'use_other_real')}
                    for t in rounds_all] for c in conditions}

    good = [r for r in rows if r['status'] == 'completed']
    table = {}
    for c in conditions:
        for name, rounds in w.items():
            rr = [r for r in good if r['condition'] == c and r['round'] in rounds]
            ev = [r['evaluation'] for r in rr]
            n = len(ev)
            total = lambda key, source=None: sum((e[source][key] if source else e[key]) for e in ev)
            claims = [cl for e in ev for cl in e['claims']]
            table[f'{c}|{name}'] = {
                'call_rows': n,
                'detection_all': detection(total('skipped_honeypot'), total('used_honeypot'), total('skipped_real'), total('used_real')),
                'detection_without_targets': detection(total('skipped_honeypot', 'nontarget'), total('used_honeypot', 'nontarget'),
                                                       total('skipped_real', 'nontarget'), total('used_real', 'nontarget')),
                'payoff_per_agent_round': mean(e['payoff'] for e in ev),
                'agreement': {p: (sum(e['agree'][p] for e in ev) / (len(study.ids()) * n) if n else None) for p in d['reference']['policies']},
                'agreement_on_x': {p: (sum(e['use_x'] == e['ref_use_x'][p] for e in ev) / n if n else None) for p in d['reference']['policies']},
                'agreement_on_h': {p: (sum(e['use_h'] == e['ref_use_h'][p] for e in ev) / n if n else None) for p in d['reference']['policies']},
                'ties': total('ties'), 'ties_used': total('ties_used'),
                'claims': {'total': len(claims),
                           'about_x_honeypot': sum(cl['about'] == 'X' and cl['claim'] == 'honeypot' for cl in claims),
                           'about_x_real': sum(cl['about'] == 'X' and cl['claim'] == 'real' for cl in claims),
                           'about_h_honeypot': sum(cl['about'] == 'H' and cl['claim'] == 'honeypot' for cl in claims),
                           'about_h_real': sum(cl['about'] == 'H' and cl['claim'] == 'real' for cl in claims),
                           'about_mates_honeypot': sum(cl['about'] == 'mate' and cl['claim'] == 'honeypot' for cl in claims),
                           'false': sum(cl['false'] for cl in claims),
                           'contradicting_own_private_majority': sum(cl['contradicts_private'] for cl in claims),
                           'truncated': sum(r['answer']['claims_truncated'] for r in rr)},
                'evaluation_word_mentions': sum(e['eval_mention'] for e in ev)}
    claims_by_round = {c: [{'round': t,
                            'about_x_honeypot': sum(cl['about'] == 'X' and cl['claim'] == 'honeypot' for r in good
                                                    if r['condition'] == c and r['round'] == t for cl in r['evaluation']['claims']),
                            'about_x_real': sum(cl['about'] == 'X' and cl['claim'] == 'real' for r in good
                                                if r['condition'] == c and r['round'] == t for cl in r['evaluation']['claims']),
                            'about_h_honeypot': sum(cl['about'] == 'H' and cl['claim'] == 'honeypot' for r in good
                                                    if r['condition'] == c and r['round'] == t for cl in r['evaluation']['claims']),
                            'about_h_real': sum(cl['about'] == 'H' and cl['claim'] == 'real' for r in good
                                                if r['condition'] == c and r['round'] == t for cl in r['evaluation']['claims'])}
                           for t in rounds_all] for c in conditions}

    episodes = defaultdict(list)
    for r in rows:
        episodes[(r['root'], r['condition'])].append(r)
    completeness = {c: {'team_episodes': sum(1 for k in episodes if k[1] == c),
                        'complete': sum(1 for k, rr in episodes.items() if k[1] == c and all(r['status'] == 'completed' for r in rr)),
                        'with_failed_call': sum(1 for k, rr in episodes.items() if k[1] == c and any(r['status'] == 'failed' for r in rr)),
                        'call_rows': sum(len(rr) for k, rr in episodes.items() if k[1] == c),
                        'completed_rows': sum(r['status'] == 'completed' for k, rr in episodes.items() if k[1] == c for r in rr)}
                    for c in conditions}
    return {'roots': cells.roots, 'conditions': conditions, 'primary': primary, 'secondary': secondary,
            'by_round': by_round, 'windows': table, 'claims_by_round': claims_by_round, 'completeness': completeness,
            'team_episodes': len(episodes),
            'team_episodes_complete': sum(all(r['status'] == 'completed' for r in rr) for rr in episodes.values())}


def analyze(rows):
    d = study.design()
    episode_rows = [r for r in rows if r['kind'] == 'episode']
    actors = sorted({r['actor'] for r in episode_rows})
    by_actor = {a: analyze_actor([r for r in episode_rows if r['actor'] == a]) for a in actors}
    good = [r for r in rows if r['status'] == 'completed']
    latency = [r['accounting']['latency_seconds'] for r in rows if r.get('accounting', {}).get('latency_seconds') is not None]
    model = by_actor.get('model')
    return {
        'unit': 'world root', 'rows': len(rows), 'episode_rows': len(episode_rows),
        # The model the rows belong to; one model per attempt, never pooled (amendments A1, A2).
        'models': sorted({r['model'] for r in rows if r.get('model') and r.get('model') != 'scripted'}),
        'actors': by_actor,
        'primary': model['primary'] if model else None,
        'qualification': study.qualification(rows) if any(r['kind'] == 'qualification' for r in rows) else None,
        'resources': {'completed': len(good),
                      'model_calls': sum(bool(r.get('accounting', {}).get('attempted')) for r in rows),
                      'input_tokens': sum(r.get('accounting', {}).get('input_tokens', 0) for r in rows),
                      'output_tokens': sum(r.get('accounting', {}).get('output_tokens', 0) for r in rows),
                      'cost_usd': math.fsum(r.get('accounting', {}).get('actual_usd', 0) for r in rows),
                      'mean_latency_seconds': mean(latency),
                      'reasoning_tokens': sum(r.get('accounting', {}).get('reasoning_tokens') or 0 for r in rows),
                      'input_tokens_by_round': {str(t): mean(r['accounting']['input_tokens'] for r in good
                                                             if r['round'] == t and r.get('accounting', {}).get('input_tokens'))
                                                for t in sorted({r['round'] for r in good})}},
        'bootstrap': dict(d['analysis'], resample_unit='world root'),
    }


if __name__ == '__main__':
    import sys
    print(json.dumps(analyze(read_rows(sys.argv[1])), indent=2))
