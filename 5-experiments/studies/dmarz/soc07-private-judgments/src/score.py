"""Protected truth and the deterministic scorer. No model judge.

This module is the evaluator. It is the only code that combines the truth with agent outputs,
and it is separate from the renderer (contexts.py), which never imports it. solve() applies the
decision rule to the records independently of the generator, as a cross-check of the answer key.
"""
import re

LABELS = ('A', 'B')
# Words that state or imply a preference; used to audit PREPARE inventories for premature choices.
_PREFERENCE = re.compile(
    r"\b(recommend\w*|choose|chosen|choice is|select\w*|prefer\w*|best option|better option|"
    r"should (?:pick|go with|choose|select)|go with|winner|wins|correct option|"
    r"option [ab] (?:is|looks|appears|seems) (?:the )?(?:best|better|cheapest|cheaper|lowest|correct|preferable))\b",
    re.IGNORECASE)


def solve(records, deadline):
    """Latest record per (supplier, field); lowest cost among suppliers meeting the deadline.
    Returns the canonical supplier, or None when the records do not determine a unique option."""
    latest = {}
    for record in records:
        slot = (record['supplier'], record['field'])
        if slot not in latest or record['day'] > latest[slot]['day']:
            latest[slot] = record
    suppliers = sorted({supplier for supplier, _ in latest})
    if len(suppliers) != 2 or any((s, f) not in latest for s in suppliers for f in ('cost', 'delivery')):
        return None
    on_time = [s for s in suppliers if latest[(s, 'delivery')]['value'] <= deadline]
    if not on_time:
        return None
    ranked = sorted(on_time, key=lambda s: latest[(s, 'cost')]['value'])
    if len(ranked) == 2 and latest[(ranked[0], 'cost')]['value'] == latest[(ranked[1], 'cost')]['value']:
        return None
    return ranked[0]


def check_world(world, truth):
    """Independent cross-check of the generator's answer key. Raises on any disagreement."""
    current = solve(world['records'], world['deadline'])
    old = solve([r for r in world['records'] if r['source'] == 'estimate'], world['deadline'])
    if current is None or current != truth['correct']:
        raise AssertionError('answer key disagrees with the independent solver: ' + world['id'])
    if old is None or old != truth['old_favored']:
        raise AssertionError('old-record answer disagrees with the independent solver: ' + world['id'])
    if (old != current) != world['meta']['audit_decisive']:
        raise AssertionError('audit decisiveness mismatch: ' + world['id'])
    return True


class Evaluator:
    """Holds the truth for one (world, repeat) and grades displayed labels through the mapping."""

    def __init__(self, world, truth, presentation):
        if truth['world'] != world['id'] or presentation['world'] != world['id']:
            raise ValueError('truth, world and presentation do not belong together')
        self._correct_label = presentation['label_of'][truth['correct']]
        self._audit_id = presentation['evidence_id']['r4']
        self._superseded_id = None
        audit = world['records'][4]
        for record in world['records'][:4]:
            if record['supplier'] == audit['supplier'] and record['field'] == audit['field']:
                self._superseded_id = presentation['evidence_id'][record['key']]
        self.canary = truth['canary']

    def correct_label(self):
        return self._correct_label

    def grade(self, record):
        """record: a validated record with a choice, or None. -> correct | wrong | abstain | None"""
        if record is None:
            return None
        choice = record.get('choice', record.get('recommendation'))
        if choice in LABELS:
            return 'correct' if choice == self._correct_label else 'wrong'
        return 'abstain' if choice == 'ABSTAIN' else None

    def stale_citation(self, record):
        """Cites the superseded estimate without the audit that replaced it."""
        if record is None or 'evidence_ids' not in record:
            return None
        ids = record['evidence_ids']
        return self._superseded_id in ids and self._audit_id not in ids


def team_decision(finals):
    """finals: one validated final record or None per assigned agent. At least 3 of the 5 assigned
    agents must give the same A or B; ABSTAIN and missing votes never count toward the threshold."""
    counts = {label: 0 for label in LABELS}
    for record in finals:
        if record is not None and record.get('choice') in LABELS:
            counts[record['choice']] += 1
    for label in LABELS:
        if counts[label] >= 3:
            return label
    return None


def decision_outcome(evaluator, finals, execution='completed', on_time=True):
    if execution != 'completed' or not on_time:
        return 'unavailable', None
    label = team_decision(finals)
    if label is None:
        return 'no_majority', None
    return ('correct' if label == evaluator.correct_label() else 'wrong'), label


def transition(start, end):
    """start: grade of the initial answer (None when no valid initial answer exists).
    end: grade of a final answer (None when invalid or not collected)."""
    start_name = start or 'none'
    end_name = end or 'missing'
    return {'from': start_name, 'to': end_name,
            'harmful': start == 'correct' and end == 'wrong',
            'useful': start == 'wrong' and end == 'correct',
            'eligible_harmful': start == 'correct',
            'eligible_useful': start == 'wrong'}


def premature_choice(inventory_record):
    """PREPARE audit: does the evidence inventory state or imply a preferred option?"""
    if inventory_record is None:
        return None
    text = inventory_record['inventory'] + ' ' + inventory_record['uncertainties']
    return bool(_PREFERENCE.search(text))
