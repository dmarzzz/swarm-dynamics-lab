"""QM-2 offline evidence contracts. No provider, network, sampling or run entry point."""
from dataclasses import dataclass
from math import exp, isfinite, log


@dataclass(frozen=True)
class Report:
    report_id: str
    true_root: str
    visible_root: str | None
    bit: int
    q: float


def validate(reports):
    if not reports:
        raise ValueError('empty evidence')
    ids, roots, visible = set(), {}, {}
    for r in reports:
        if not isinstance(r.report_id, str) or not r.report_id or r.report_id in ids:
            raise ValueError('invalid or duplicate transport ID')
        ids.add(r.report_id)
        if not isinstance(r.true_root, str) or not r.true_root:
            raise ValueError('invalid root ID')
        if type(r.bit) is not int or r.bit not in (0, 1):
            raise ValueError('invalid observation')
        if type(r.q) not in (int, float) or not isfinite(r.q) or not .5 < r.q < 1:
            raise ValueError('invalid reliability')
        identity = (r.bit, r.q, r.visible_root)
        if r.true_root in roots and roots[r.true_root] != identity:
            raise ValueError('inconsistent descendants or lineage mask')
        roots[r.true_root] = identity
        if r.visible_root is not None:
            if not isinstance(r.visible_root, str) or not r.visible_root:
                raise ValueError('invalid visible lineage')
            if r.visible_root in visible and visible[r.visible_root] != r.true_root:
                raise ValueError('visible lineage collision')
            visible[r.visible_root] = r.true_root
    if len({r.q for r in reports}) != 1:
        raise ValueError('QM-2 requires common reliability within a world')


def actor_packet(reports):
    """Explicit allowlist; no evaluator truth or hidden ancestry crosses boundary."""
    validate(reports)
    return [dict(report_id=r.report_id, visible_root=r.visible_root, bit=r.bit, q=r.q)
            for r in reports]


def _term(bit, q):
    return (2 * bit - 1) * log(q / (1 - q))


def _prob(score):
    if score >= 0:
        return 1 / (1 + exp(-score))
    e = exp(score)
    return e / (1 + e)


def oracle_posterior(reports):
    """Evaluator-only, exact under the PLAN's independent-root generator."""
    validate(reports)
    roots = {r.true_root: r for r in reports}
    return _prob(sum(_term(r.bit, r.q) for r in roots.values()))


def evidence_score(packet, policy):
    """Consumes only actor fields; partial-lineage outputs are not calibrated probabilities."""
    if policy not in ('naive', 'visible', 'capped'):
        raise ValueError('unknown policy')
    if not packet:
        raise ValueError('empty packet')
    seen, known, opaque = {}, 0., 0.
    ids, qualities = set(), set()
    for r in packet:
        if set(r) != {'report_id', 'visible_root', 'bit', 'q'}:
            raise ValueError('non-actor fields')
        if not isinstance(r['report_id'], str) or not r['report_id'] or r['report_id'] in ids:
            raise ValueError('invalid transport ID')
        ids.add(r['report_id'])
        bit, q, root = r['bit'], r['q'], r['visible_root']
        if type(bit) is not int or bit not in (0, 1):
            raise ValueError('invalid observation')
        if type(q) not in (int, float) or not isfinite(q) or not .5 < q < 1:
            raise ValueError('invalid reliability')
        qualities.add(q)
        if root is not None and (not isinstance(root, str) or not root):
            raise ValueError('invalid visible lineage')
        if root is not None and root in seen and seen[root] != (bit, q):
            raise ValueError('inconsistent visible descendants')
        value = _term(bit, q)
        if policy == 'naive':
            known += value
        elif root is None:
            opaque += value
        elif root not in seen:
            known += value
        if root is not None:
            seen[root] = (bit, q)
    if len(qualities) != 1:
        raise ValueError('QM-2 requires common reliability')
    if policy == 'capped':
        q = next(iter(qualities))
        bound = log(q / (1 - q))
        opaque = max(-bound, min(bound, opaque))
    return _prob(known + opaque)


def valid_response(response):
    return (isinstance(response, dict) and set(response) == {'choice', 'p_one'}
            and response['choice'] in ('ZERO', 'ONE', 'DEFER')
            and type(response['p_one']) in (int, float)
            and isfinite(response['p_one']) and 0 <= response['p_one'] <= 1)


def committee(slots):
    if len(slots) != 5:
        raise ValueError('must retain all five scheduled slots')
    choices = [r['choice'] if valid_response(r) else None for r in slots]
    for choice in ('ZERO', 'ONE'):
        if choices.count(choice) >= 3:
            return choice
    return 'DEFER'


def summarize(assigned, outcomes):
    """Outcomes map each started world to (truth_bit, five response slots).

    Missing keys are unstarted assignments. Never infer or discard missing worlds.
    """
    if not assigned or len(set(assigned)) != len(assigned):
        raise ValueError('nonempty unique assignment IDs required')
    if set(outcomes) - set(assigned):
        raise ValueError('unassigned outcome')
    result = dict(assigned=len(assigned), recorded=len(outcomes), correct=0, wrong=0,
                  defer=0, unstarted=len(assigned)-len(outcomes), invalid_slots=0,
                  wrong_unanimous=0, valid_probabilities=0, brier_sum=0.)
    for truth, slots in outcomes.values():
        if type(truth) is not int or truth not in (0, 1):
            raise ValueError('invalid evaluator truth')
        decision = committee(slots)
        answer = 'ONE' if truth else 'ZERO'
        result['defer' if decision == 'DEFER' else 'correct' if decision == answer else 'wrong'] += 1
        valid = [r for r in slots if valid_response(r)]
        result['invalid_slots'] += 5 - len(valid)
        result['valid_probabilities'] += len(valid)
        result['brier_sum'] += sum((r['p_one']-truth)**2 for r in valid)
        result['wrong_unanimous'] += int(len(valid) == 5 and all(r['choice'] == decision for r in valid)
                                          and decision not in ('DEFER', answer))
    result['accuracy_all_assigned'] = result['correct'] / len(assigned)
    result['brier_valid'] = (result['brier_sum'] / result['valid_probabilities']
                             if result['valid_probabilities'] else None)
    return result
