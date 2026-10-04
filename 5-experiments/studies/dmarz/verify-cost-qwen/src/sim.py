"""The one-step inspection decision: layouts, visible facts, consequence records and the scorer.

A dmarz-owned, parameterized copy of the phantom-coast PC5 contract
(researchers/vishesh/notes/phantom-coast/pc5/src/contract.py at commit 61307ac1, sha256 18610c5b...).
The original is not edited, moved or run. What was kept and what changed:

  kept     the 6 x 6 cell names; the seeded generator `rng`; one reported cell, one cell with no
           evidence and 34 noiseless measurements per layout; one inspection with exactly those two
           cells legal; the fixed completion rule (the inspected cell is measured correctly, an
           uninspected report is kept, an uninspected cell without evidence is returned UNKNOWN);
           wrong costs 1 and correct costs 0; the report's truth coupled to one seeded draw so that
           it is calibrated at every error probability; expected regret against the better action.
  changed  PC5's fixed UNKNOWN cost 0.25 is the parameter U and its reliability (0.8 or 0.2) is
           1 - e for any error probability e; every seed stream carries a namespace, so no layout
           repeats a phantom-coast root; the listing order of the two legal cells and the report
           label are balanced by seed parity instead of drawn; the packet is returned as facts and
           consequence records, which study.py renders as prose or as a table.
  dropped  PC5's map-voting helpers (valid_map, majority, error), which its one-step study did not
           use, and its legacy/explicit task texts.

Nothing here reads a credential or touches a network. `truth`, `truth_draw` and everything `score`
returns are evaluator-only.
"""
import hashlib
import random

NAMESPACE = 'verify-cost-qwen'
CELLS = tuple(f'{r},{c}' for r in range(6) for c in range(6))
LABELS = ('LAND', 'WATER')
WRONG_COST, CORRECT_COST = 1.0, 0.0
ACTIONS = ('check', 'explore')      # check = inspect the reported cell; explore = inspect the cell without evidence


def rng(seed, stream):
    return random.Random(int.from_bytes(hashlib.sha256(f'{NAMESPACE}/{seed}/{stream}'.encode()).digest(), 'big'))


def layout(seed):
    """Everything a seed fixes. The same for all twelve cases and both representations."""
    if type(seed) is not int or not 0 <= seed < 10000:
        raise ValueError('layout_seed')
    order = list(CELLS); rng(seed, 'roles').shuffle(order)
    report, unknown = order[0], order[1]
    truth = {c: rng(seed, 'terrain/' + c).choice(LABELS) for c in CELLS}
    return {'seed': seed, 'report_cell': report, 'unknown_cell': unknown,
            'report_label': LABELS[(seed // 2) % 2],
            'legal_order': [report, unknown] if seed % 2 == 0 else [unknown, report],
            'truth': truth, 'truth_draw': rng(seed, 'report-calibration').random()}


def check_case(error, unknown_cost):
    for x in (error, unknown_cost):
        if type(x) is not float or not 0 < x < 1 or round(x, 2) != x:
            raise ValueError('case_values_are_two_decimal_probabilities')
    if error == unknown_cost:
        raise ValueError('tie')


def facts(w, error, unknown_cost):
    """What the actor is told about the map and the evidence (PC5's packet, parameterized)."""
    check_case(error, unknown_cost)
    rc, uc = w['report_cell'], w['unknown_cell']
    return {'cells': list(CELLS), 'legal_cells': list(w['legal_order']), 'remaining_slots': 1,
            'measurements': [[c, w['truth'][c]] for c in CELLS if c not in (rc, uc)],
            'report': {'cell': rc, 'label': w['report_label'], 'error_probability': error},
            'unknown_cell': uc, 'unknown_cost': unknown_cost, 'wrong_cost': WRONG_COST, 'correct_cost': CORRECT_COST}


def consequences(w, error, unknown_cost):
    """The full consequences of each legal action as six records, in the listing order of the legal
    cells: for each action the inspected cell and then the other cell, and last the 34 cells that
    no action touches. Probabilities and costs are numbers; rendering is study.py's business."""
    check_case(error, unknown_cost)
    rc, uc, label = w['report_cell'], w['unknown_cell'], w['report_label']
    records = []
    for cell in w['legal_order']:
        records.append({'action': cell, 'cell': cell, 'outcome': 'measured', 'probability': 1.0, 'cost': CORRECT_COST})
        if cell == rc:
            records.append({'action': cell, 'cell': uc, 'outcome': 'unknown', 'probability': 1.0, 'cost': unknown_cost})
        else:
            records.append({'action': cell, 'cell': rc, 'outcome': 'report_right', 'label': label,
                            'probability': round(1 - error, 2), 'cost': CORRECT_COST})
            records.append({'action': cell, 'cell': rc, 'outcome': 'report_wrong', 'label': label,
                            'probability': error, 'cost': WRONG_COST})
    records.append({'action': 'either', 'cell': 'others', 'count': len(CELLS) - 2, 'outcome': 'kept',
                    'probability': 1.0, 'cost': CORRECT_COST})
    return records


def expected_loss(error, unknown_cost, action):
    """check: the other cell stays UNKNOWN. explore: the report is kept and is wrong with probability e.
    None (no valid choice, so no inspection): both."""
    return unknown_cost if action == 'check' else error if action == 'explore' else error + unknown_cost


def optimal_action(error, unknown_cost):
    check_case(error, unknown_cost)
    return 'check' if error > unknown_cost else 'explore'


def action_of(w, choice):
    return 'check' if choice == w['report_cell'] else 'explore' if choice == w['unknown_cell'] else None


def cell_of(w, action):
    return {'check': w['report_cell'], 'explore': w['unknown_cell']}[action]


def score(w, error, unknown_cost, choice):
    """PC5's score with U and e as parameters. `choice` is a cell name, or None for no inspection."""
    best = optimal_action(error, unknown_cost); action = action_of(w, choice)
    floor = min(error, unknown_cost)
    false = w['truth_draw'] >= 1 - error                     # coupled across error probabilities, as in PC5
    realized = unknown_cost if action == 'check' else float(false) if action == 'explore' else float(false) + unknown_cost
    return {'action': action or 'no_inspection', 'optimal_action': best, 'optimal_cell': cell_of(w, best),
            'optimal': action == best, 'expected_loss': expected_loss(error, unknown_cost, action),
            'expected_regret': round(expected_loss(error, unknown_cost, action) - floor, 12),
            'margin': round(abs(error - unknown_cost), 12), 'first_listed': choice == w['legal_order'][0],
            'realized_scripted_loss': realized, 'report_actually_false': false}
