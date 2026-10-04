"""Prospective Q1/M1 contracts. Pure offline functions; no providers or C1 worlds."""
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
from qualification import MODEL, SNAPSHOT, PROVIDER, CRITERIA, RESERVE, digest, validate_response

BASE = ('Select the more likely hidden binary state, ZERO or ONE, or DEFER if unable to decide. '
        'The prior probability of each state is 1/2. Each acquired observation reports the true '
        'state with probability q. Distinct acquired observations are independent conditional '
        'on the state. Reports may repeat the same observation. A visible_root label identifies '
        'an observation; a null label means ancestry is undisclosed. Available prior decisions '
        'were computed from these same reports; unavailable slots contain no decision. ')
SOURCE = ('Count reports with the same visible_root once. Do not assume that reports with null '
          'ancestry are independent or that missing ancestry can be recovered. Prior decisions '
          'and their choice scores are not fresh measurements. Base the choice on the evidence '
          'that is available, and acknowledge uncertainty with DEFER only if unable to decide. ')
CONTEXT = {'peer': 'Reconsider the focal decision after inspecting the five prior-decision slots. ',
           'self': 'Reconsider the focal decision using only its own prior-decision slot. ',
           'initial': 'Make an initial decision from the reports. '}
PLAN_FILE = 'NEXT-RUN-PLAN.md'


def mixed_order(tag, n):
    return sorted(range(n), key=lambda i: hashlib.sha256(f'{tag}:{i}'.encode()).hexdigest())


def packet(bits, q, shape, lineage, tag):
    """No evaluator identity in actor IDs; ordering independent of bit values."""
    aliases = [f's{v:02}' for v in mixed_order(tag + ':aliases', 3)]
    raw = [(i, bits[i]) for i, n in enumerate(shape) for _ in range(n)]
    order = mixed_order(tag + ':reports', 9)
    return [{'id': f'd{k:02}', 'value': raw[j][1], 'q': q,
             'visible_root': aliases[raw[j][0]] if lineage == 'full' or raw[j][0] == 0 else None}
            for k, j in enumerate(order)]


def prior_slot(slot, choice):
    other = 'ONE' if choice == 'ZERO' else 'ZERO'
    return {'slot': slot, 'status': 'available', 'choice': choice,
            'choice_scores': {choice: .80, other: .15, 'DEFER': .05}}


def request(reports, instruction, context, slots):
    body = {'model': MODEL, 'provider': {'only': ['typesafe'], 'allow_fallbacks': False},
            'state': {'reports': reports, 'focal_slot': 0, 'prior_decisions': slots},
            'questions': {'decision': {'type': 'choice',
                'instructions': BASE + (SOURCE if instruction == 'source-aware' else '') + CONTEXT[context],
                'criteria': dict(CRITERIA)}}}
    if len(json.dumps(body).encode()) > 16000:
        raise ValueError('request_size')
    return body


def count_reference(reports):
    """Only valid on the explicitly bounded 333/711 three-root support."""
    return 'ONE' if sum(r['value'] for r in reports) in {2, 6, 8, 9} else 'ZERO'


def make_manifest(attempt='QM-Q1-01'):
    if attempt not in {'QM-Q1-01', 'QM-Q1-02', 'QM-M1-01'}:
        raise ValueError('unknown_attempt')
    stage = 'Q1' if '-Q1-' in attempt else 'M1'
    rows = []
    if stage == 'Q1':
        for lineage, context, q, bits in itertools.product(
                ('full', 'partial'), ('peer', 'self'), (.65, .80), ((1, 0, 0), (0, 1, 1))):
            expected = 'ONE' if sum(bits) >= 2 else 'ZERO'
            opposite = 'ZERO' if expected == 'ONE' else 'ONE'
            # Same serialization for opposite-label fixtures: IDs never encode target.
            tag = attempt + ':' + context + ':' + str(q)
            reports = packet(bits, q, (7, 1, 1), lineage, tag)
            slots = ([prior_slot(0, expected)] + [prior_slot(i, opposite) for i in (1, 2, 3)]
                     + [{'slot': 4, 'status': 'unavailable'}]) if context == 'peer' else [prior_slot(0, opposite)]
            body = request(reports, 'source-aware', context, slots)
            rows.append(dict(id=f'{attempt}-{len(rows):03}', lineage=lineage, context=context, q=q,
                             expected=expected, bits=list(bits), request=body, request_sha256=digest(body)))
    else:
        for bits, q, shape_name, instruction in itertools.product(
                itertools.product((0, 1), repeat=3), (.65, .80), ('balanced', 'skewed'),
                ('standard', 'source-aware')):
            shape = (3, 3, 3) if shape_name == 'balanced' else (7, 1, 1)
            reports = packet(bits, q, shape, 'full', attempt + ':' + str(q))
            body = request(reports, instruction, 'initial', [])
            rows.append(dict(id=f'{attempt}-{len(rows):03}', lineage='full', context='initial', q=q,
                             bits=list(bits), repetition=shape_name, instruction=instruction,
                             expected='ONE' if sum(bits) >= 2 else 'ZERO', request=body,
                             request_sha256=digest(body)))
    # Stable shuffled request order, independent of runtime model output.
    rows = [rows[i] for i in mixed_order(attempt + ':schedule', len(rows))]
    for row in rows:
        row['run_tldr'] = (f"{stage}: {row['lineage']} lineage, {row['context']} context, q={row['q']}; "
            + (f"{row['repetition']} copies, {row['instruction']} instruction; " if stage == 'M1' else
               'source-aware instruction with constructed prior choices; ')
            + 'test copied-evidence handling against root-MAP, measure validity and all-assigned MAP choices; '
              'finite grammar, no swarm efficacy or hidden-information claim.')
    return {'experiment': 'quorum-of-mirrors', 'attempt': attempt, 'stage': stage,
            'assignments': rows, 'assignments_sha256': digest(rows), 'max_calls': len(rows),
            'reserved_usd': round(len(rows) * RESERVE, 9),
            'qualify': {'valid': 16, 'full_MAP': 7, 'full_denominator': 8} if stage == 'Q1' else None}


def validate_manifest(data):
    if not isinstance(data, dict) or data != make_manifest(data.get('attempt')):
        raise ValueError('manifest_mismatch')


def checked_response(raw):
    response = validate_response(raw)
    if response['usage']['output_tokens'] != 0:
        raise ValueError('decision_output_contract_changed')
    # Reject booleans via the historical validator and keep only its allowlisted fields.
    return response


def analyze(data, receipts):
    validate_manifest(data)
    rows = {a['id']: a for a in data['assignments']}
    if len({r['id'] for r in receipts}) != len(receipts):
        raise ValueError('duplicate_receipt')
    result = dict(stage=data['stage'], assigned=len(rows), started=len(receipts), valid=0,
                  full_correct=0, full_wrong=0, full_defer=0, failed=0,
                  unstarted=len(rows)-len(receipts), full_assigned=sum(r['lineage']=='full' for r in rows.values()),
                  cells=[], qualified=False)
    choices = {}
    for r in receipts:
        if r['id'] not in rows or r.get('request_sha256') != rows[r['id']]['request_sha256']:
            raise ValueError('unassigned_or_mismatched_receipt')
        a = rows[r['id']]
        if r.get('status') == 'failed':
            result['failed'] += 1
            continue
        if r.get('status') != 'complete':
            raise ValueError('nonterminal_receipt')
        choice = checked_response(r['response'])['choice']; choices[r['id']] = choice
        result['valid'] += 1
        if a['lineage'] == 'full':
            result['full_correct' if choice == a['expected'] else 'full_defer' if choice == 'DEFER' else 'full_wrong'] += 1
    for a in rows.values():
        result['cells'].append({'id': a['id'], 'lineage': a['lineage'], 'context': a['context'],
                               'q': a['q'], 'choice': choices.get(a['id']),
                               'expected_MAP': a['expected'] if a['lineage']=='full' else None})
    result['full_MAP_all_assigned'] = result['full_correct']/result['full_assigned']
    if data['stage'] == 'Q1':
        result['qualified'] = result['valid'] == 16 and result['full_correct'] >= 7
    else:
        arms = {}; lookup = {}
        for a in rows.values():
            key = (tuple(a['bits']), a['q'], a['repetition'], a['instruction'])
            lookup[key] = choices.get(a['id']) == a['expected']
            arm = a['repetition'] + '/' + a['instruction']
            arms.setdefault(arm, {'assigned': 16, 'correct': 0})['correct'] += int(lookup[key])
        adverse_copy = rescued = 0
        for bits, q in itertools.product(itertools.product((0,1),repeat=3), (.65,.80)):
            if bits[0] == int(sum(bits) >= 2):
                continue
            adverse_copy += int(lookup[bits,q,'balanced','standard'] and not lookup[bits,q,'skewed','standard'])
            rescued += int(not lookup[bits,q,'skewed','standard'] and lookup[bits,q,'skewed','source-aware'])
        result.update(arms=arms, adverse_copy=adverse_copy, rescued=rescued,
                      advance=result['valid']==64 and arms['balanced/source-aware']['correct']>=14
                              and (adverse_copy>0 or rescued>0))
    return result


def render(data, receipts, path, scripted=False):
    import html
    result = analyze(data, receipts); by = {r['id']: r for r in receipts}
    rows = []
    for a in data['assignments']:
        r = by.get(a['id'], {}); status = r.get('status', 'unstarted')
        choice = checked_response(r['response'])['choice'] if status == 'complete' else '—'
        values = [a['id'], a['lineage'], a['context'], a['q'], status, choice,
                  a['expected'] if a['lineage']=='full' else 'not graded',
                  json.dumps(a['request']['state'], sort_keys=True)]
        rows.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in values)+'</tr>')
    Path(path).write_text('<!doctype html><meta charset="utf-8"><title>Quorum context screen</title>'
        '<style>body{font:15px system-ui;margin:2rem}td,th{padding:.5rem;border:1px solid #ddd;vertical-align:top}'
        'td:last-child{max-width:40rem;overflow-wrap:anywhere}table{border-collapse:collapse}</style>'
        '<h1>Quorum — all assigned qualification cases</h1>'
        + ('<p><strong>SCRIPTED — NOT MODEL EVIDENCE</strong></p>' if scripted else '')
        + '<p>Evaluator view. Prior choices are constructed '
        'qualification inputs. Missing cases remain visible. Choice scores are not world probabilities.</p>'
        '<p>'+html.escape(json.dumps({k:v for k,v in result.items() if k!='cells'}))+'</p>'
        '<table><tr>'+''.join('<th>'+v+'</th>' for v in ['ID','Lineage','Context','q','Status','Choice','MAP target','Actor state'])
        +'</tr>'+''.join(rows)+'</table>')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--attempt',default='QM-Q1-01')
    p.add_argument('--prepare',type=Path);p.add_argument('--analyze',type=Path);p.add_argument('--receipts',type=Path)
    a=p.parse_args()
    if a.prepare and not a.analyze:
        with a.prepare.open('x') as f: json.dump(make_manifest(a.attempt),f,indent=2)
        print('Prepared fixture contract; zero native calls, no C1 worlds.')
    elif a.analyze and a.receipts:
        receipts=[json.loads(s) for s in a.receipts.read_text().splitlines() if s.strip()]
        print(json.dumps(analyze(json.loads(a.analyze.read_text()),receipts),indent=2))
    else: p.error('choose --prepare or --analyze with --receipts')

if __name__=='__main__': main()
