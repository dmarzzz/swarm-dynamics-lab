#!/usr/bin/env python3
"""Offline recovery auditor. No runner import, model calls, or credentials."""
import ast
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = '8c4ce07e1597e9be8316c940ff91027701efbe4f'
PREFIX = 'researchers/shadow/notes/capture-memory-mix/claude-pool/'


def load(name):
    return json.loads((ROOT / name).read_text())


def lines(name):
    return [json.loads(x) for x in (ROOT / name).read_text().splitlines() if x]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build():
    requests, responses = lines('requests.jsonl'), lines('responses.jsonl')
    req = {r['request_id']: r for r in requests}
    resp = {r['request_id']: r for r in responses}
    assert len(req) == len(requests) == len(resp) == len(responses) == 20
    assert set(req) == set(resp) == set(range(1, 21))
    assert all(req[i]['meta'] == resp[i]['meta'] for i in req)
    assert all(r['meta']['stage'] == 'qual' for r in requests)
    assert all(r['model'] == 'claude-sonnet-5-5' for r in requests)
    assert all(r['choice'] is None and r['model_returned'] is None and r['usage'] is None and not r['text'] for r in responses)
    tree = ast.parse((ROOT / 'run.py').read_text())
    histories = [q['history'] for q in load('qualification.json')['results']]
    # QHIST contains list repetition, which literal_eval deliberately does not execute.
    # Independently reconstruct the frozen fixtures instead of evaluating arbitrary source.
    expected = [[1]*8, [-1]*8, [1]*7+[-1], [-1]*7+[1],
                [1,1,1,-1,1,1,1,-1], [-1,-1,-1,1,-1,-1,-1,1],
                [1]*15+[-1], [-1]*15+[1], [1], [-1], [-1]*40+[1]*4, [1]*40+[-1]*4]
    assert histories == expected
    assert all(r['history_len'] == len(histories[r['meta']['k']]) for r in requests)
    q = load('qualification.json')
    assert q['n'] == 12 and q['valid'] == 0 and q['passed'] is False
    assert len(q['results']) == 12 and all(x['choice'] is None for x in q['results'])
    counts = Counter(r['meta']['k'] for r in requests)
    assert counts == {0:4, 1:4, 2:4, 3:4, 4:1, 5:1, 6:1, 7:1}
    statuses = Counter(str(r['status']) for r in responses)
    assert statuses == {'429':8, '503':12}
    assert load('STOP.json')['requests'] == 20
    prereg_before_calls = subprocess.run(['git','cat-file','-e',SOURCE+':'+PREFIX+'PREREG.md'], capture_output=True).returncode == 0
    assert not prereg_before_calls
    old_source = subprocess.check_output(['git','show',SOURCE+':'+PREFIX+'run.py'])
    assert old_source == (ROOT/'run.py').read_bytes()
    inputs_path = ROOT.parent.parent/'capture-memory'/'freeze-claude'/'inputs.json'
    roots = json.loads(inputs_path.read_text())['roots']
    scripted = load('scripted-reference.json')
    assignments = []
    for k in range(12):
        assignments.append({'stage':'qualification','unit':str(k),'arm':'','planned_decisions':1,
                            'http_attempts':counts[k], 'terminal_attempts':counts[k],
                            'valid_decisions':0,'status':'transport_failed' if counts[k] else 'unstarted'})
    per_root = []
    for root in roots:
        honest = sorted([i for i,a in root['agents'].items() if not a['committed']], key=int)
        assert len(root['agents']) == 12 and len(honest) == 6 and len(root['schedules']) == 20
        short = sorted(random.Random(f'mix:{root["task_id"]}').sample(honest, 2), key=int)
        ref = next(r for r in scripted['roots'] if r['task_id'] == root['task_id'])
        assert ref['short_ids_mix'] == short
        n = sum(2 for pairs in root['schedules'] for a,b in pairs if str(a) in honest and str(b) in honest)
        for arm in ['full','mix']:
            assert ref[arm]['calls'] == n
            assignments.append({'stage':'scientific_episode','unit':str(root['task_id']),'arm':arm,
                                'planned_decisions':n,'http_attempts':0,'terminal_attempts':0,
                                'valid_decisions':0,'status':'unstarted'})
        per_root.append({'task_id':root['task_id'],'short_ids':short,'decisions_per_arm':n})
    scientific = sum(a['planned_decisions'] for a in assignments if a['stage']=='scientific_episode')
    assert scientific == 456 and scripted['calls_planned'] == 468
    # Actual frozen admission only counts parseability. Copier is always an allowed name.
    fn = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='qualify')
    assert 'passed=valid >= 11' in ast.unparse(fn)
    copier = [h[-1] for h in histories]
    opposing = [k for k,h in enumerate(histories) if h[-1] != (1 if sum(h)>0 else -1)]
    assert len(opposing) == 8
    assert all(copier[k] != (1 if sum(histories[k])>0 else -1) for k in opposing)
    summary = {
      'assessment_date':'2026-10-04','assessor':'shadow/sol-mix-astra','disposition':'blocked',
      'source_commit':SOURCE,'prereg_present_at_source_commit':prereg_before_calls,
      'requested_model':'claude-sonnet-5-5','returned_models':[], 'provider_route':'historical local Anthropic pool',
      'time_first_request':min(r['started'] for r in requests),'time_last_response':max(r['finished'] for r in responses),
      'http_attempts':20,'terminal_attempts':20,'unresolved_transport_attempts':0,'statuses':dict(statuses),
      'qualification':{'assigned':12,'started_assignments':8,'failed_assignments':8,'unstarted':4,'valid':0,'passed':False},
      'scientific':{'planned_roots':4,'observed_roots':0,'planned_episodes':8,'started_episodes':0,
                    'unstarted_episodes':8,'planned_decisions':scientific,'valid_decisions':0,'paired_effect':None,'ci95':None,
                    'logical_missing_effect_bounds':[-1,1]},
      'recovery_new_model_calls':0,'recovery_openrouter_calls':0,
      'cost':{'actual_usd':None,'input_tokens':None,'output_tokens':None,'unreceipted_attempts':20,
              'historical_predispatch_reservation_ledger_present':False,'recovery_lane_cap_usd':5,
              'administrative_nonspendable_hold_usd':5,'admissible_remaining_usd':0,
              'hold_is_verified_billing_upper_bound':False,'recovery_incremental_model_spend_usd':0},
      'negative_control':{'label':'OFFLINE SOFTWARE CHECK, NOT MODEL EVIDENCE','last_item_copier_parseable':12,
                          'old_gate_would_pass':True,'opposing_majority_histories':8,'copier_majority_matches_on_conflicts':0},
      'roots':per_root,
      'native_hashes':{n:digest(ROOT/n) for n in ['PREREG.md','run.py','scripted-reference.json','requests.jsonl','responses.jsonl','qualification.json','STOP.json']},
      'input_sha256':digest(inputs_path),
      'limitations':['No qualified Claude outcome','No independent pre-review located','No prospective dollar ledger',
                     'Historical request log records metadata, not effective serialized payloads',
                     'Historical public-preregistration statement not supported by inspected source commit']
    }
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(assignments[0]))
    writer.writeheader(); writer.writerows(assignments)
    return summary, buf.getvalue()


if __name__ == '__main__':
    import sys
    summary, csv_text = build()
    if '--check' in sys.argv:
        assert load('recovery-summary.json') == summary
        assert (ROOT/'assignments.csv').read_text() == csv_text.replace('\r\n','\n')
        print('PASS: 20/20 terminals, 12 qualification assignments, 8 unstarted episodes, copy-gate defect, immutable native hashes')
    else:
        (ROOT/'recovery-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
        (ROOT/'assignments.csv').write_text(csv_text.replace('\r\n','\n'))
        print(json.dumps({k:summary[k] for k in ['http_attempts','statuses','qualification','scientific','negative_control','cost']},indent=2))
