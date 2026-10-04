"""QM-S0-01 request contract, provider validation and all-assigned analysis.

No credentials, provider calls, infrastructure or scientific sampling in this module.
"""
import hashlib
import itertools
import json
import math
from reference import Report, actor_packet

MODEL = 'typesafe/jev-1.13'
SNAPSHOT = 'typesafe/jev-1.13-20260917'
PROVIDER = 'TypeSafe'
RESERVE = .001344
CRITERIA = {'ZERO': 'The hidden binary state is more likely zero.',
            'ONE': 'The hidden binary state is more likely one.',
            'DEFER': 'Unable to determine which state is more likely.'}
INSTRUCTIONS = ('Select the more likely hidden binary state. The prior probability of each state is 1/2. '
                'Distinct observation roots are independent conditional on the state. Each root reports '
                'the true state with its stated probability q. Reports with the same visible_root are '
                'copies of one observation and add no independent evidence. Count each observation '
                'root once. Select DEFER only if unable to determine the more likely state.')


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def assignments():
    result = []
    for repeat in (1, 2):
        for q in (.65, .80):
            for bits in itertools.product((0, 1), repeat=3):
                reports = [Report(f'p{i}-{j}', f'r{i}', f'r{i}', bits[i], q)
                           for i, n in enumerate((7, 1, 1)) for j in range(n)]
                body = {'model': MODEL, 'provider': {'only': ['typesafe'], 'allow_fallbacks': False},
                        'state': {'reports': actor_packet(reports)},
                        'questions': {'decision': {'type': 'choice', 'instructions': INSTRUCTIONS,
                                                   'criteria': dict(CRITERIA)}}}
                case = f'q{int(q*100)}-' + ''.join(map(str, bits))
                result.append({'id': f'{case}-r{repeat}', 'case': case, 'repeat': repeat, 'q': q,
                               'expected': 'ONE' if sum(bits) >= 2 else 'ZERO',
                               'request': body, 'request_sha256': digest(body)})
    return result


def manifest(attempt="QM-S0-01"):
    if attempt not in ("QM-S0-01", "QM-S0-02"):
        raise ValueError("unknown_attempt")
    rows = assignments()
    return {'experiment': 'quorum-of-mirrors', 'attempt': attempt,
            'stage': 'exploratory competence', 'assignments': rows,
            'assignments_sha256': digest(rows), 'max_calls': 32, 'max_reserved_usd': 32*RESERVE}


def validate_manifest(data):
    # Exact frozen matrix: arbitrary payloads or target edits cannot ride along.
    if data != manifest(data.get("attempt")):
        raise ValueError('manifest_mismatch')


def validate_response(data):
    """Return safe allowlisted fields only; never raw response/error data."""
    if not isinstance(data, dict) or data.get('model') != SNAPSHOT or data.get('provider') != PROVIDER:
        raise ValueError('route_changed')
    usage = data.get('usage', {})
    if not isinstance(usage, dict):
        raise ValueError('usage_invalid')
    cost, tokens, output = (usage.get(k) for k in ('cost','input_tokens','output_tokens'))
    if (type(cost) not in (int,float) or not math.isfinite(cost) or not 0 <= cost <= RESERVE + 1e-10
            or type(tokens) is not int or not 0 < tokens <= 32000
            or type(output) is not int or output < 0):
        raise ValueError('usage_invalid')
    answers = data.get('answers')
    if not isinstance(answers, dict) or set(answers) != {'decision'}:
        raise ValueError('choice_invalid')
    answer = answers['decision']
    if not isinstance(answer, dict):
        raise ValueError('choice_invalid')
    p, choice = answer.get('probabilities'), answer.get('choice')
    if (not isinstance(p,dict) or set(p) != set(CRITERIA) or choice not in CRITERIA
            or any(type(v) not in (int,float) or not math.isfinite(v) or not 0 <= v <= 1 for v in p.values())):
        raise ValueError('choice_invalid')
    on_grid = all(abs(v*100-round(v*100)) < 1e-8 for v in p.values())
    tolerance = .005*len(p)+1e-9 if on_grid else .001
    if abs(sum(p.values())-1) > tolerance or p[choice] < max(p.values())-1e-5:
        raise ValueError('choice_invalid')
    return {'choice': choice, 'probabilities': dict(p), 'model': SNAPSHOT, 'provider': PROVIDER,
            'usage': {'cost': cost, 'input_tokens': tokens, 'output_tokens': output}}


def analyze(data, receipts):
    validate_manifest(data)
    by_id = {r['id']: r for r in data['assignments']}
    if len({r['id'] for r in receipts}) != len(receipts) or any(r['id'] not in by_id for r in receipts):
        raise ValueError('duplicate_or_unassigned_receipt')
    totals = dict(assigned=32, valid=0, correct=0, wrong=0, defer=0, failed=0,
                  unstarted=32-len(receipts), complete_pairs=0, agreeing_pairs=0)
    cells = {f'{q}-{label}': dict(assigned=8, correct=0) for q in (.65,.80) for label in ('ZERO','ONE')}
    pairs = {}
    for receipt in receipts:
        row = by_id[receipt['id']]
        if receipt.get('request_sha256') != row['request_sha256']:
            raise ValueError('receipt_request_mismatch')
        if receipt.get('status') == 'failed':
            totals['failed'] += 1
            continue
        if receipt.get('status') != 'complete':
            raise ValueError('nonterminal_receipt')
        response = validate_response(receipt['response'])
        choice = response['choice']
        totals['valid'] += 1
        totals['correct' if choice == row['expected'] else 'defer' if choice == 'DEFER' else 'wrong'] += 1
        cells[f"{row['q']}-{row['expected']}"]['correct'] += int(choice == row['expected'])
        pairs.setdefault(row['case'], []).append(choice)
    for choices in pairs.values():
        if len(choices) == 2:
            totals['complete_pairs'] += 1
            totals['agreeing_pairs'] += int(choices[0] == choices[1])
    totals['cells'] = cells
    totals['accuracy_all_assigned'] = totals['correct']/32
    # Stop-on-failure means all 32 must finish before advancing even if the count floor could pass.
    totals['qualified'] = (totals['unstarted'] == 0 and totals['failed'] == 0 and totals['valid'] >= 31
                            and totals['correct'] >= 28 and all(c['correct'] >= 6 for c in cells.values()))
    return totals


def main():
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', type=Path)
    parser.add_argument('--analyze', type=Path)
    parser.add_argument('--receipts', type=Path)
    args = parser.parse_args()
    if args.prepare and not args.analyze:
        with args.prepare.open('x') as f:
            json.dump(manifest(), f, indent=2)
        print('Prepared 32 assignments; zero model calls.')
    elif args.analyze and args.receipts:
        data = json.loads(args.analyze.read_text())
        receipts = [json.loads(line) for line in args.receipts.read_text().splitlines() if line.strip()]
        print(json.dumps(analyze(data, receipts), indent=2))
    else:
        parser.error('choose --prepare PATH or --analyze MANIFEST --receipts JOURNAL')


if __name__ == '__main__':
    main()
