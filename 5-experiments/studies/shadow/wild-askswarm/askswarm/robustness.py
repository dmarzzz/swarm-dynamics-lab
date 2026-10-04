"""Importable, offline sensitivity transforms. No inferred people or invented clocks.

`variants(events)` returns (name -> Event list, name -> transformation receipt).
Root aggregation retains an actual earliest row per source root. It changes the estimand.
`robustness(events)` recomputes every answer and rank diagnostic, without exporting text.
"""
from collections import Counter, defaultdict
from hashlib import sha256
import math
import statistics
from .core import analyze, DISSENT, REVERT


def order(event):
    return (event.time is None, event.time if event.time is not None else 0, event.event_id)


def validate_ids(events):
    ids = [e.event_id for e in events]
    if any(not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Robustness requires nonempty unique event_id values')


def exact_deduplicate(events):
    """Global byte-identical nonempty text; retain earliest observed representative.

    Empty text rows remain independent missing-content observations. Distinct actors
    posting exactly the same text are removed too: this is NOT duplicate-event cleaning.
    """
    seen, kept = set(), []
    for event in sorted(events, key=order):
        key = sha256(event.text.encode('utf-8')).digest()
        if event.text and key in seen:
            continue
        if event.text:
            seen.add(key)
        kept.append(event)
    return kept


def root_ids(events):
    """Explicit root_id wins; else follow parent_id, retaining absent ancestor tokens.

    A missing root relation is a singleton, not a shared None bucket. Cycles fail
    closed because assigning an arbitrary cycle root would fabricate provenance.
    Thread alone is not presumed to mean derivation. Wiki adapter supplies page roots.
    """
    events = list(events)
    validate_ids(events)
    lookup = {e.event_id: e for e in events}
    roots = {}
    for eid in lookup:
        chain, seen, current = [], set(), eid
        while current not in roots:
            if current in seen:
                raise ValueError('Cycle in artifact parent chain')
            seen.add(current)
            chain.append(current)
            event = lookup.get(current)
            if event is None:
                root = 'external:' + current
                break
            explicit = event.metadata.get('root_id')
            if explicit is not None and str(explicit):
                root = 'root:' + str(explicit)
                break
            parent = event.metadata.get('parent_id')
            if parent is None or not str(parent):
                root = 'event:' + current
                break
            current = str(parent)
        else:
            root = roots[current]
        for node in chain:
            roots[node] = root
    return {eid: roots[eid] for eid in lookup}


def aggregate_roots(events, roots=None):
    """One earliest actual row per root, not concatenated text or a synthetic actor."""
    events = list(events)
    roots = root_ids(events) if roots is None else roots
    selected = {}
    for event in sorted(events, key=order):
        selected.setdefault(roots[event.event_id], event)
    return list(selected.values())


def time_exclusion_reason(event):
    value = event.metadata.get('time_imputed')
    if value is True or value == 1 or (isinstance(value, str) and value.lower() in ('true', '1', 'yes')):
        return 'explicitly_imputed'
    grade = str(event.metadata.get('time_grade') or '').lower()
    if grade in ('imputed', 'inferred', 'interpolated', 'synthetic'):
        return 'explicitly_imputed_grade'
    if event.time is not None and event.metadata.get('root_basis') == 'wiki_page' and grade != 'reqlog':
        return 'wiki_fallback_or_unknown_clock_grade'
    return None


def exclude_imputed(events):
    """Keep missing clocks. Wiki non-reqlog exclusion is conservative fallback sensitivity."""
    return [e for e in events if time_exclusion_reason(e) is None]


def variants(events):
    events = list(events)
    validate_ids(events)
    roots = root_ids(events)
    arms = {'baseline': sorted(events, key=order),
            'exact_dedup': exact_deduplicate(events),
            'root_aggregate': aggregate_roots(events, roots),
            'exclude_imputed': exclude_imputed(events)}
    # Roots must be resolved BEFORE filtering, or removing a parent splits a chain.
    arms['combined'] = aggregate_roots(exact_deduplicate(exclude_imputed(events)), roots)
    receipts = {}
    for name, rows in arms.items():
        receipts[name] = {
            'input_records': len(events), 'retained_records': len(rows), 'removed_records': len(events) - len(rows),
            'retained_root_count': len({roots[e.event_id] for e in rows}),
            'root_relation_known_records': sum('root_id' in e.metadata or 'parent_id' in e.metadata for e in rows),
            'clock_exclusion_candidates': dict(Counter(time_exclusion_reason(e) for e in events if time_exclusion_reason(e))),
            'clock_grade_counts': dict(Counter(str(e.metadata.get('time_grade', 'not_supplied')) for e in rows)),
            'retained_ids_sha256': sha256('\n'.join(sorted(e.event_id for e in rows)).encode()).hexdigest(),
        }
    return arms, receipts


def midranks(scores):
    groups = defaultdict(list)
    for key, score in scores.items():
        if score is not None:
            groups[score].append(key)
    ranks, start = {}, 1
    for value in sorted(groups, reverse=True):
        keys = groups[value]
        rank = start + (len(keys) - 1) / 2
        ranks.update({key: rank for key in keys})
        start += len(keys)
    return ranks


def rank_change(before, after, top_k=10):
    """Tie-aware ranks. Correlation restricted to common keys; loss shown separately.

    Top-k includes the full boundary tie. No artificial alphabetic tie breaking.
    """
    a, b = midranks(before), midranks(after)
    common = sorted(a.keys() & b.keys())
    shifts = [abs(a[k] - b[k]) for k in common]
    def top(scores):
        vals = sorted((v for v in scores.values() if v is not None), reverse=True)
        cutoff = vals[min(top_k, len(vals)) - 1] if vals else None
        return {k for k, v in scores.items() if v is not None and cutoff is not None and v >= cutoff}
    ta, tb = top(before), top(after)
    rho = None
    if len(common) > 1:
        # Re-rank on common support: Spearman, not Pearson of truncated full ranks.
        ca = midranks({k: before[k] for k in common})
        cb = midranks({k: after[k] for k in common})
        ma, mb = statistics.mean(ca.values()), statistics.mean(cb.values())
        den = math.sqrt(sum((ca[k] - ma) ** 2 for k in common) * sum((cb[k] - mb) ** 2 for k in common))
        rho = sum((ca[k] - ma) * (cb[k] - mb) for k in common) / den if den else None
    return {'before_ranked': len(a), 'after_ranked': len(b), 'common': len(common),
            'exited': len(a.keys() - b.keys()), 'entered': len(b.keys() - a.keys()),
            'common_spearman': rho, 'mean_absolute_rank_shift': statistics.mean(shifts) if shifts else None,
            'max_absolute_rank_shift': max(shifts) if shifts else None,
            'top_k': top_k, 'before_top_including_ties': len(ta), 'after_top_including_ties': len(tb),
            'top_overlap': len(ta & tb), 'top_jaccard': len(ta & tb) / len(ta | tb) if ta | tb else None}


def numeric_deltas(before, after, prefix=''):
    out = {}
    for key in before.keys() | after.keys():
        a, b = before.get(key), after.get(key)
        path = prefix + key
        if isinstance(a, dict) and isinstance(b, dict):
            out.update(numeric_deltas(a, b, path + '.'))
        elif a is None or b is None or (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            out[path] = {'before': a, 'after': b, 'delta': b - a if a is not None and b is not None else None}
    return out


def identity_scores(events, report):
    activity, dissent, revert, times, first = Counter(), Counter(), Counter(), defaultdict(list), Counter()
    for e in events:
        if e.agent_id is None:
            continue
        activity[e.agent_id] += 1
        dissent[e.agent_id] += bool(DISSENT.search(e.text))
        revert[e.agent_id] += bool(REVERT.search(e.text))
        if e.time is not None:
            times[e.agent_id].append(e.time)
    for c in report['clusters']:
        first.update(c['first_movers'])
    return {'participation': dict(activity), 'first_observed_cluster_count': dict(first),
            'reuse_credit': {r['identity']: r['fractional_new_adopter_credit'] for r in report['influence']},
            'reuse_credit_per_record': {r['identity']: r['credit_per_record'] for r in report['influence']},
            'observed_span_seconds': {a: max(ts) - min(ts) for a, ts in times.items()},
            'dissent_marker_count': dict(dissent), 'revert_marker_count': dict(revert)}


def compare_clusters(before, after):
    a, b = before['_membership'], after['_membership']
    overlap = Counter((a[e], b[e]) for e in a.keys() & b.keys())
    matched, used = {}, set()
    for (old, new), count in sorted(overlap.items(), key=lambda pair: (-pair[1], pair[0])):
        if new not in matched and old not in used:
            matched[new] = old
            used.add(old)
    ca = {c['cluster']: c for c in before['clusters']}
    cb = {c['cluster']: c for c in after['clusters']}
    changed = sum(set(ca[old]['first_movers']) != set(cb[new]['first_movers']) for new, old in matched.items())
    fields = ['records', 'identities', 'dated_identities']
    ranks = {}
    for field in fields:
        ranks[field] = rank_change({str(k): c[field] for k, c in ca.items()},
                                  {str(matched[k]) if k in matched else 'new:' + str(k): c[field] for k, c in cb.items()})
    for k in before['summary']['time_to_k']:
        # Negative time scores rank fastest first; unreached have no rank, not infinity/failure.
        ranks['time_to_' + k] = rank_change(
            {str(i): -c['time_to_k_seconds'][k] for i, c in ca.items() if c['time_to_k_seconds'][k] is not None},
            {str(matched[i]) if i in matched else 'new:' + str(i): -c['time_to_k_seconds'][k]
             for i, c in cb.items() if c['time_to_k_seconds'][k] is not None})
    retained = len(a.keys() & b.keys())
    matched_records = sum(count for (old, new), count in overlap.items() if matched.get(new) == old)
    return {'matching': 'greedy maximum shared-event overlap, one-to-one; not semantic identity',
            'before_clusters': len(ca), 'after_clusters': len(cb), 'matched_clusters': len(matched),
            'unmatched_before': len(ca) - len(matched), 'unmatched_after': len(cb) - len(matched),
            'common_text_records': retained, 'records_in_matched_correspondence': matched_records,
            'matched_record_fraction': matched_records / retained if retained else None,
            'first_observer_sets_changed': changed, 'rankings': ranks}


def robustness(events, name='swarm', **kwargs):
    arms, receipts = variants(events)
    reports, scores = {}, {}
    for arm, rows in arms.items():
        report = analyze(rows, name=name + ' / ' + arm, include_evidence=True, **kwargs)
        reports[arm] = report
        scores[arm] = identity_scores(rows, report)
    baseline = reports['baseline']
    comparisons = {}
    for arm, report in reports.items():
        if arm == 'baseline':
            continue
        comparisons[arm] = {'summary_deltas': numeric_deltas(baseline['summary'], report['summary']),
                            'record_kind_deltas': numeric_deltas(baseline['record_kinds'], report['record_kinds']),
                            'task_event_deltas': numeric_deltas(baseline['task_events'], report['task_events']),
                            'identity_rankings': {key: rank_change(scores['baseline'][key], value) for key, value in scores[arm].items()},
                            'cluster_comparison': compare_clusters(baseline, report)}
    # Evidence stays in memory for auditing; consumers decide whether to export derived IDs.
    return {'reports': reports, 'scores': scores, 'transformations': receipts, 'comparisons': comparisons}
