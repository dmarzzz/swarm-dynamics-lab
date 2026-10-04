"""D1 only: offline freeze, exactly 120 saved-input assignments, no retries.

No queue polling, swarm rerun, holdout generation, provisioning or automatic
successor. The owner controls credentials, hub run, claim and service lifecycle.
All files produced by this CLI are private run artifacts until sanitized.
"""
import argparse
import copy
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request

from tasks import digest, feasible
from bench_v3.contracts import SYSTEM, schema, strict_json, validate
from bench_v3.evidence import possible_decisions, reported_records, resolve, supported_parent
from bench_v3.journal import Journal, read_events
from bench_v3.policies import anthropic, Scripted
from bench_v3.scoring import parent_score, reference_winner, quorum_state
from bench_v3.worlds import make_case, memory_fixtures
from bench_v3.failures import safe_failure, REASONS
from plan_v3_diagnostic import build_receipt

ROOT = Path(__file__).resolve().parent
NOTES = ROOT.parent
DEFAULT_PLAN = NOTES / 'benchmark-v3/next-run-planning-evidence.json'
Q0_RECEIPT = NOTES / 'benchmark-v3/results/v3-q0-a1/analysis.json'
PLAN_DOC = NOTES / 'benchmark-v3/D1-PLAN.md'
SETUP_DOC = NOTES / 'benchmark-v3/SETUP.md'
PRE_DOC = NOTES / 'reviews/v3-d1-a1-pre.md'
MODELS = ('claude-haiku-4-5-20251001', 'claude-sonnet-4-6')
RATES = {MODELS[0]: (1, 5), MODELS[1]: (3, 15)}
ATTEMPT = 'v3-d1-a1'
EXPERIMENT = 'discussion-dose-v3'
VERSION = 'd1-saved-request-v1'
CHECKS = ('dedicated_claim_merged_exclusive', 'owner_account_verified', 'single_owner_state_writer',
          'worker_restart_disabled', 'watchdog_active', 'hub_single_dispatch_verified',
          'rehearsal_client_independence', 'rehearsal_progress', 'rehearsal_failure_capture',
          'rehearsal_durable_journal', 'rehearsal_upload', 'rehearsal_cloud_retrieval',
          'rehearsal_duplicate_refusal', 'owner_cleanup_path_verified', 'public_page_design_verified',
          'shared_budget_reservation_recorded', 'six_hour_claim_coverage_secured', 'rehearsal_operator_retrieval')


def read(path):
    return strict_json(Path(path).read_text(encoding='utf-8'))


def fingerprint(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def write_new(path, data):
    """Exclusive, fsynced creation including the directory entry."""
    path = Path(path)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    sync_dir(path.parent)


def sync_dir(path):
    fd = os.open(str(path), os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def source_hashes():
    paths = list((ROOT / 'bench_v3').glob('*.py'))
    paths += [ROOT / n for n in ('tasks.py', 'providers.py', 'plan_v3_diagnostic.py', 'diagnostic_v3.py')]
    return {p.relative_to(ROOT).as_posix(): fingerprint(p)['sha256'] for p in sorted(paths)}


def planning_documents():
    return {p.relative_to(ROOT.parents[4]).as_posix(): fingerprint(p) for p in (PLAN_DOC, SETUP_DOC, PRE_DOC)}


def source_commit():
    value = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}', value): raise ValueError('source commit required')
    # All executable dependencies must be committed, including new files.
    for name in source_hashes():
        rel = (ROOT / name).relative_to(ROOT.parents[4]).as_posix()
        saved = subprocess.check_output(['git', 'show', f'{value}:{rel}'], cwd=ROOT)
        if hashlib.sha256(saved).hexdigest() != fingerprint(ROOT / name)['sha256']:
            raise ValueError('commit executable source before freezing')
    for rel, expected in planning_documents().items():
        saved = subprocess.check_output(['git', 'show', f'{value}:{rel}'], cwd=ROOT)
        if hashlib.sha256(saved).hexdigest() != expected['sha256']:
            raise ValueError('commit current setup, D1 plan and pre-run assessment before freezing')
    return value


def reject_gold(value):
    forbidden = {'truth', 'truth_answer', 'expected', 'expected_supported', 'false_value', 'roles',
                 'target', 'stratum', 'allocation', 'attack_id', 'evidence_allowed_choices'}
    if type(value) is dict:
        if forbidden.intersection(value): raise ValueError('evaluator fields in actor request')
        for child in value.values(): reject_gold(child)
    elif type(value) is list:
        for child in value: reject_gold(child)


def saved_inputs(q0, planning):
    """Load exact retained Q0; no replacement requests are constructed here."""
    q0 = Path(q0)
    receipt = read(Q0_RECEIPT)
    for name in ('manifest.json', 'events.jsonl', 'episodes.json', 'summary.json'):
        if fingerprint(q0 / name) != receipt['verified_remote_files'][name]:
            raise ValueError('retained Q0 bytes differ from published audit receipt')
    plan = read(planning)
    if plan != read(DEFAULT_PLAN) or build_receipt(q0) != plan:
        raise ValueError('planning receipt differs from frozen Q0 selector/order')
    manifest = read(q0 / 'manifest.json')
    if manifest['system_hash'] != digest(SYSTEM): raise ValueError('actor system prompt changed')
    events = read_events(q0 / 'events.jsonl')
    starts = {e['call_id']: e for e in events if e['kind'] == 'call_start'}
    if len(starts) != 636 or len(events) != 1790 or events[-1]['kind'] != 'complete':
        raise ValueError('Q0 assignment/journal mismatch')
    rows = {}
    for selected in plan['selected']:
        start = starts[selected['q0_call_id']]
        request = start['request']
        if digest(request) != selected['request_sha256']: raise ValueError('saved request hash mismatch')
        if any(start.get(k) != selected[k] for k in ('label', 'agent')) or request['phase'] != selected['phase']:
            raise ValueError('saved request metadata mismatch')
        reject_gold(request)
        if len(json.dumps(request, sort_keys=True).encode()) > 60000: raise ValueError('saved input exceeds byte limit')
        schema(request['phase'], request['context'])
        rows[selected['q0_call_id']] = {'selected': selected, 'request': request}
    if len(rows) != 60: raise ValueError('expected 60 unique saved requests')
    return plan, rows


def body(request, model):
    # Byte-for-byte native Q0 serialization, except the model identity.
    return {'model': model, 'system': SYSTEM,
            'messages': [{'role': 'user', 'content': json.dumps(request, sort_keys=True)}],
            'temperature': 0, 'max_tokens': 2000,
            'output_config': {'format': {'type': 'json_schema', 'schema': schema(request['phase'], request['context'])}}}


def prepare(q0, planning, output, launch_owner):
    if not re.fullmatch('[a-z0-9-]+/[a-z0-9-]+', launch_owner): raise ValueError('nonsecret agent launch owner required')
    plan, inputs = saved_inputs(q0, planning)
    scheduled = []
    reservation = 0
    for index, assignment in enumerate(plan['proposed_schedule']):
        request = inputs[assignment['q0_call_id']]['request']
        payload = body(request, assignment['model'])
        rates = RATES[assignment['model']]
        allowance = (len(json.dumps(payload).encode()) + 512) * rates[0] + 2000 * rates[1]
        reservation += allowance
        scheduled.append({**assignment, 'call_id': f'd1-{index:03d}',
                          'provider_body_sha256': digest(payload), 'reservation_microusd': allowance})
    commit = source_commit()
    relative_plan = PLAN_DOC.relative_to(ROOT.parents[4]).as_posix()
    frozen = {'schema': VERSION, 'attempt': ATTEMPT, 'parent_attempt': 'v3-q0-a1',
              'status': 'frozen-diagnostic-only-owner-preflight-required', 'launch_owner': launch_owner,
              'source_commit': commit, 'source_hashes': source_hashes(),
              'planning_documents': planning_documents(),
              'public_plan': {'url': f'https://github.com/dmarzzz/swarm-lab/blob/{commit}/{relative_plan}',
                              'raw_url': f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{commit}/{relative_plan}',
                              'sha256': fingerprint(PLAN_DOC)['sha256']},
              'planning_receipt': fingerprint(planning), 'q0_manifest': fingerprint(Path(q0) / 'manifest.json'),
              'q0_events': fingerprint(Path(q0) / 'events.jsonl'), 'system_hash': digest(SYSTEM),
              'models': list(MODELS), 'planned_calls': 120, 'selected_requests': 60,
              'counts_per_model': {'diagnostic': 6, 'report_snapshot': 18, 'memory': 36},
              'configuration': {'temperature': 0, 'max_output_tokens': 2000, 'max_input_bytes': 60000,
                                'timeout': 120, 'transport_retries': 0, 'output_repair_retries': 0,
                                'thinking': 'disabled_by_omission', 'worker_count': 1},
              'rates_usd_per_million': {m: {'input': RATES[m][0], 'output': RATES[m][1]} for m in MODELS},
              'worst_case_reservation_microusd': reservation, 'shared_budget_usd': 500,
              'schedule': scheduled, 'holdout_opened': False, 'successor_dispatch_authorized': False}
    write_new(output, frozen)
    return {'status': frozen['status'], 'manifest_sha256': fingerprint(output)['sha256'],
            'calls': 120, 'reservation_usd': reservation / 1e6, 'model_calls_dispatched': 0}


def verify_manifest(manifest, q0, planning):
    frozen = read(manifest)
    if frozen['schema'] != VERSION or frozen['attempt'] != ATTEMPT or frozen['source_hashes'] != source_hashes():
        raise ValueError('manifest source/version mismatch')
    if frozen['source_commit'] != source_commit(): raise ValueError('use exact committed D1 source')
    plan, inputs = saved_inputs(q0, planning)
    # Rebuild all manifest fields, not just the submitted call count.
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
        rebuilt = Path(folder) / 'manifest.json'
        prepare(q0, planning, rebuilt, frozen['launch_owner'])
        if read(rebuilt) != frozen: raise ValueError('frozen manifest differs from bounded D1 plan')
    return frozen, inputs


def owner_evidence(evidence, manifest_hash, now=None):
    """Owner attestation is explicit evidence, not inferred cloud access."""
    now = now or datetime.now(timezone.utc)
    allowed = {'schema', 'manifest_sha256', 'launch_owner', 'server', 'claim_id', 'claim_until',
               'checks', 'evidence_sha256', 'shared_model_spend_usd', 'reserved_other_model_spend_usd',
               'model_availability', 'request_compatibility_verified', 'lifecycle_mode', 'hub_run'}
    if set(evidence) != allowed or evidence['schema'] != 'd1-owner-preflight-v1':
        raise ValueError('owner evidence schema mismatch')
    if evidence['manifest_sha256'] != manifest_hash: raise ValueError('preflight evidence is for another manifest')
    local = evidence['lifecycle_mode'] == 'owner-controlled-local-cleanup'
    required = set(CHECKS) - ({'rehearsal_cloud_retrieval'} if local else set())
    if set(evidence['checks']) != set(CHECKS) or any(type(evidence['checks'][k]) is not bool for k in CHECKS) or any(evidence['checks'][k] is not True for k in required):
        raise ValueError('owner readiness/rehearsal checks incomplete')
    if not re.fullmatch('[0-9a-f]{64}', evidence['evidence_sha256']): raise ValueError('private rehearsal evidence hash required')
    if evidence['server'] != 'sim-discussion-d1' or evidence['claim_id'] != 'dmarz-discussion-d1':
        raise ValueError('dedicated D1 allocation required; retired Q0 forbidden')
    until = datetime.fromisoformat(evidence['claim_until'].replace('Z', '+00:00'))
    if until.tzinfo is None or until - now < timedelta(minutes=90):
        raise ValueError('claim must cover one-hour D1 plus audit/upload allowance')
    if evidence['model_availability'] != list(MODELS) or evidence['request_compatibility_verified'] is not True:
        raise ValueError('exact account models and request compatibility must be verified')
    if evidence['lifecycle_mode'] not in ('owner-controlled-local-cleanup', 'owner-controlled-always-on'):
        raise ValueError('one owner-controlled lifecycle required')
    if evidence['hub_run'] != f'{EXPERIMENT}/{ATTEMPT}': raise ValueError('fixed D1 hub run required')
    for key in ('shared_model_spend_usd', 'reserved_other_model_spend_usd'):
        value = evidence[key]
        if type(value) not in (int, float) or not 0 <= value <= 500: raise ValueError('shared budget accounting invalid')
    return evidence


def check_models():
    """Authenticated metadata GET only, never an inference compatibility probe."""
    key = os.environ.get('SWARM_MODEL_API_KEY', '')
    if not key: raise ValueError('secure model environment absent')
    headers = {'x-api-key': key, 'anthropic-version': '2023-06-01'}
    workspace = os.environ.get('SWARM_MODEL_WORKSPACE_ID')
    if workspace: headers['anthropic-workspace-id'] = workspace
    for model in MODELS:
        req = urllib.request.Request('https://api.anthropic.com/v1/models/' + model, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as response:
            row = strict_json(response.read(100000).decode())
        if row.get('id') != model: raise ValueError('exact model unavailable; no fallback')


def preflight(manifest, q0, planning, evidence, output):
    frozen, inputs = verify_manifest(manifest, q0, planning)
    owner = owner_evidence(read(evidence), fingerprint(manifest)['sha256'])
    if owner['launch_owner'] != frozen['launch_owner']: raise ValueError('single launch owner mismatch')
    remaining = 500 - owner['shared_model_spend_usd'] - owner['reserved_other_model_spend_usd']
    if remaining * 1e6 < frozen['worst_case_reservation_microusd']: raise ValueError('shared model budget reservation unavailable')
    providers = {m: anthropic(config(m, remaining)) for m in MODELS}
    for row in frozen['schedule']:
        request = inputs[row['q0_call_id']]['request']
        if providers[row['model']].request_body(request) != body(request, row['model']):
            raise ValueError('native provider serialization changed')
    check_models()
    registration = public_plan(frozen)
    result = {'schema': 'd1-preflight-pass-v1', 'manifest_sha256': fingerprint(manifest)['sha256'],
              'owner_evidence': owner, 'checked_utc': datetime.now(timezone.utc).isoformat(),
              'available_models': list(MODELS), 'serialized_requests_verified': 120,
              'remaining_shared_budget_usd': remaining, 'model_calls_dispatched': 0}
    result['public_plan_verification'] = registration
    write_new(output, result)
    return {'status': 'preflight-passed', 'model_calls_dispatched': 0, 'preflight_sha256': fingerprint(output)['sha256']}


def config(model, remaining):
    return {'model': model, 'max_calls': 60, 'max_output_tokens': 2000, 'max_input_bytes': 60000,
            'timeout': 120, 'max_cost_usd': remaining, 'input_usd_per_million': RATES[model][0],
            'output_usd_per_million': RATES[model][1]}


def public_plan(frozen):
    """Unauthenticated immutable raw-content and rendered-page check before dispatch."""
    expected = frozen['public_plan']
    with urllib.request.urlopen(expected['raw_url'], timeout=120) as response:
        raw = response.read(1000000)
    if hashlib.sha256(raw).hexdigest() != expected['sha256']:
        raise ValueError('public immutable plan content mismatch')
    text = raw.decode('utf-8')
    for section in ('TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics'):
        if '\n## ' + section + '\n' not in text: raise ValueError('public plan section absent')
    with urllib.request.urlopen(expected['url'], timeout=120) as response:
        page = response.read(8000000).decode('utf-8')
    for marker in ('v3-d1-a1', 'claude-sonnet-4-6', '120'):
        if marker not in page: raise ValueError('public plan page does not display current design')
    return {'url': expected['url'], 'sha256': expected['sha256'], 'public_raw_hash_matches': True,
            'public_page_markers_verified': True, 'verified_utc': datetime.now(timezone.utc).isoformat()}


def score(selected, request, response):
    ctx = request['context']
    if selected['group'] == 'memory':
        fixture = next(f for f in memory_fixtures() if f['id'] == selected['label'])
        if fixture['context'] != ctx: raise ValueError('fixed memory fixture drift')
        result = parent_score(ctx, response, fixture['truth_answer'])
        support = supported_parent(ctx)
        extra = set(response['sources']) - set(support['sources']) if response is not None else set()
        records = reported_records(ctx)
        extra_agreeing = [s for s in extra if any(r['id'] == s and r['authority'] == 'secondary' and
                         r['facts'].get(ctx['key']) == (response['value'] - ctx['delta'] if response['value'] is not None else None)
                         for r in records)]
        result.update(extra_citations=len(extra), extra_agreeing_secondary_citations=len(extra_agreeing),
                      memory_coverage=int(any(r['key'] == ctx['key'] for r in ctx['memory'])),
                      memory_distinct_origins=len({r['origin'] for r in records if ctx['key'] in r['facts']}))
        return {'group': 'memory', 'state': fixture['state'], 'family': fixture['family'],
                'variant': fixture['variant'], 'evaluation': result}
    world = int(selected['label'].split(':')[0])
    case = make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')
    if case['task'] != ctx['task']: raise ValueError('Q0 world task drift')
    records = reported_records(ctx)
    choices = possible_decisions(ctx['task'], records)
    if len(choices) != 1: raise ValueError('saved request answerability drift')
    truth = case['truth']; winner = reference_winner(ctx['task'], truth)
    ev = {'invalid': int(response is None), 'truth_correct': None, 'truth_wrong_nonabstain': None,
          'abstain': None, 'evidence_justified': None,
          'constraint_violation': None, 'claim_extraction_correct': None, 'claim_extraction_observed': None,
          'all_values_extracted_correctly': None, 'choice_claim_consistent': None,
          'choice_claim_inconsistent': None, 'choice_claim_incomplete': None,
          'unnecessary_abstain': None, 'citation_mismatches': None}
    if response is not None:
        vote = response['vote']; claims = response['claims']
        extracted = {k: c['value'] for k, c in claims.items() if c is not None}
        endorsing = [{'id': k, 'origin': k, 'authority': 'primary', 'version': 1, 'facts': {k: v}} for k, v in extracted.items()]
        own_choices = possible_decisions(ctx['task'], endorsing)
        by_id = {d['id']: d for d in case['documents']}
        mismatch = sum(any(by_id[s]['facts'].get(k) != c['value'] for s in c['sources']) for k, c in claims.items() if c is not None)
        value_map = {k.split('.')[1]: v for k, v in truth.items() if k.startswith(vote + '.')}
        ev.update(truth_correct=int(vote == winner), evidence_justified=int(vote == choices[0]),
                  truth_wrong_nonabstain=int(vote != 'ABSTAIN' and vote != winner), abstain=int(vote == 'ABSTAIN'),
                  constraint_violation=int(vote != 'ABSTAIN' and not feasible(case['family'], value_map, ctx['task']['rules'])),
                  claim_extraction_correct=sum(v == truth[k] for k, v in extracted.items()),
                  claim_extraction_observed=len(extracted), all_values_extracted_correctly=int(extracted == truth),
                  choice_claim_consistent=int(len(own_choices) == 1 and vote == own_choices[0]),
                  choice_claim_inconsistent=int(len(own_choices) == 1 and vote != own_choices[0]),
                  choice_claim_incomplete=int(len(own_choices) != 1), unnecessary_abstain=int(vote == 'ABSTAIN'),
                  citation_mismatches=mismatch)
    return {'group': selected['group'], 'world': world, 'family': case['family'],
            'agent': selected['agent'], 'evaluation': ev}


def group_metrics(rows, assigned):
    names = sorted({m for r in rows for m in r['score']['evaluation']})
    return {'assigned': assigned, 'observed_responses': sum(r['status'] == 'valid' for r in rows),
            'terminal': len(rows), 'missing_terminal': assigned - len(rows),
            'metrics': {m: {'sum': sum(r['score']['evaluation'][m] for r in rows if r['score']['evaluation'].get(m) is not None),
                             'observed': sum(r['score']['evaluation'].get(m) is not None for r in rows),
                             'assigned': assigned} for m in names}}


class HubProgress:
    """Attach to the owner's already-started hub job; never enqueue/restart it.

    Reports only counters; actor inputs/outputs stay in private terminal artifacts.
    The same observer works for the independent zero-model rehearsal run.
    """
    def __init__(self, hub_run, manifest_sha256, scientific):
        expected = f'{EXPERIMENT}/{ATTEMPT}' + ('' if scientific else '-rehearsal')
        if hub_run != expected: raise ValueError('wrong bounded hub run')
        import swarm_report as sr
        current = sr.get_run(hub_run)
        if current.get('status') != 'running' or current.get('params', {}).get('manifest_sha256') != manifest_sha256:
            raise ValueError('owner must start one manifest-bound hub run before attachment')
        self.reporter = sr.Run(hub_run, EXPERIMENT, current['params'])
        self.started = self.terminal = self.invalid = self.physical = self.cost_micro = 0
        self.missing_usage = 0; self.scientific = scientific

    def metrics(self):
        return {'assigned_calls': 120, 'started_calls': self.started, 'terminal_calls': self.terminal,
                'physical_model_calls': self.physical, 'invalid_calls': self.invalid,
                'observed_usage_cost_usd': self.cost_micro / 1e6, 'usage_missing_calls': self.missing_usage,
                'qualification_passed': 0}

    def __call__(self, event):
        if event['kind'] == 'call_start': self.started += 1
        if event['kind'] == 'call_terminal':
            row = event['record']; self.terminal += 1
            self.invalid += row['status'] != 'valid'; self.physical += row['dispatched']
            complete = all(k in row['usage'] for k in ('input_tokens', 'output_tokens'))
            self.missing_usage += row['dispatched'] and not complete
            self.cost_micro += sum(row['usage'].get(k, 0) * rate for k, rate in zip(('input_tokens', 'output_tokens'), RATES[row['model']]))
        if event['kind'] in ('call_start', 'call_terminal', 'dispatch_stopped', 'complete'):
            self.reporter.progress(self.terminal, 120, message='D1 saved-input diagnostic; no fresh qualification.', **self.metrics())

    def finish(self, output, checked):
        from bench_v3.hub_worker import publish
        write_new(Path(output) / 'audit.json', {k: v for k, v in checked.items() if k != 'summary'})
        publish(self.reporter, Path(output))
        if self.terminal == 120 and not self.invalid and not self.missing_usage:
            self.reporter.done(message='D1 execution/audit complete; inspect diagnostic gates. No model qualification or successor.',
                               **self.metrics())
        else:
            self.reporter.fail(message='D1 bounded diagnostic retained failures/missingness; no retry or successor.', **self.metrics())


def summarize(frozen, events, rows):
    starts = [e for e in events if e['kind'] == 'call_start']
    ids = [e['call_id'] for e in starts]
    terminal = [r['call_id'] for r in rows]
    if len(ids) != len(set(ids)) or len(terminal) != len(set(terminal)) or set(terminal) - set(ids):
        raise ValueError('duplicate/unstarted records')
    models = {}
    for model in MODELS:
        own = [r for r in rows if r['model'] == model]
        start_ids = {e['call_id'] for e in starts if e['model'] == model}
        valid_usage = [r for r in own if all(type(r['usage'].get(k)) is int and r['usage'][k] >= 0 for k in ('input_tokens', 'output_tokens'))]
        missing_usage = [r['call_id'] for r in own if r['dispatched'] and r not in valid_usage]
        tokens = {k: sum(r['usage'][k] for r in valid_usage) for k in ('input_tokens', 'output_tokens')}
        cost_micro = tokens['input_tokens'] * RATES[model][0] + tokens['output_tokens'] * RATES[model][1]
        groups = {g: group_metrics([r for r in own if r['score']['group'] == g], n)
                  for g, n in frozen['counts_per_model'].items() if g != 'memory'}
        memory = {state: group_metrics([r for r in own if r['score'].get('state') == state], 6)
                  for state in ('complete', 'omitted', 'conflict', 'correlated_copies', 'superseded', 'inherited_false')}
        worlds = []
        for world in range(20001, 20007):
            votes = [next((r['response'] for r in own if r['score'].get('world') == world and
                          r['score']['group'] == 'report_snapshot' and r['score'].get('agent') == agent), None) for agent in range(3)]
            state = quorum_state(votes)
            winner = reference_winner(make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')['task'],
                                      make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')['truth'])
            worlds.append({'world': world, **state, 'truth_correct': int(state['decision'] == winner),
                           'correct_completion_lower': int(all(v == winner for v in state['completion_decisions'])),
                           'correct_completion_upper': int(any(v == winner for v in state['completion_decisions']))})
        full = sum(r['score']['evaluation'].get('truth_correct') == 1 for r in own if r['score']['group'] == 'diagnostic')
        report = sum(w['truth_correct'] for w in worlds)
        failures = Counter(r['reason'] for r in own if r['status'] != 'valid')
        complete = len(own) == len(start_ids) == 60 and all(r['status'] == 'valid' for r in own) and not missing_usage
        models[model] = {'assigned_calls': 60, 'started': len(start_ids), 'terminal': len(own),
                         'valid': sum(r['status'] == 'valid' for r in own),
                         'physical_calls_observed': sum(r['dispatched'] for r in own),
                         'unstarted': 60 - len(start_ids), 'unresolved': sorted(start_ids - set(terminal)),
                         'failures': dict(failures), 'usage_missing_calls': missing_usage, **tokens,
                         'observed_usage_cost_microusd': cost_micro,
                         'actual_cost_complete': not missing_usage and not (start_ids - set(terminal)) and
                                                 not any(r['reason'] == 'provider_accounting_error' for r in own),
                         'latency_seconds': [r['latency_seconds'] for r in own],
                         'groups': groups, 'memory': memory, 'report_quorums': worlds,
                         'diagnostic_gate': {'full_evidence_correct': full, 'saved_report_quorum_correct': report,
                                            'assigned_each': 6, 'required_each': 5,
                                            'eligible_for_separate_fresh_qualification': bool(frozen.get('scientific', True) and complete and full >= 5 and report >= 5),
                                            'model_qualified': False}}
    pairs = []
    by_id = {r['call_id']: r for r in rows}
    for pair in range(60):
        assignments = [a for a in frozen['schedule'] if a['pair'] == pair]
        observed = {a['model']: by_id.get(a['call_id']) for a in assignments}
        scores = {m: (r['score']['evaluation'] if r else None) for m, r in observed.items()}
        deltas = {k: scores[MODELS[1]][k] - scores[MODELS[0]][k]
                  for k in (set(scores[MODELS[0]] or {}) & set(scores[MODELS[1]] or {}))
                  if type(scores[MODELS[0]][k]) is int and type(scores[MODELS[1]][k]) is int}
        pairs.append({'pair': pair, 'q0_call_id': assignments[0]['q0_call_id'], 'scores': scores, 'sonnet_minus_haiku': deltas})
    return {'schema': VERSION, 'attempt': frozen['attempt'], 'assigned_calls': 120, 'started': len(starts),
            'terminal': len(rows), 'unresolved': sorted(set(ids) - set(terminal)),
            'models': models, 'paired_items': pairs, 'qualification': False,
            'holdout_opened': False, 'successors_dispatched': False,
            'limitations': ['Six development world clusters; descriptive diagnostics only.',
                            'Q0 report packets remain Haiku-generated; this is not an end-to-end Sonnet swarm.',
                            'Fixture and swarm parent wording differ; strict extra-citation labels remain frozen.',
                            'N=3 single-value majority merge structurally discards conflicts.',
                            'Ambiguous dispatched calls are never retried; absent usage is unknown cost, not zero.',
                            'Baseline reasoning and discussion effects remain confounded by failed Q0 qualification.']}


def validate_preflight(frozen, manifest_path, preflight_path):
    proof = read(preflight_path)
    if set(proof) != {'schema', 'manifest_sha256', 'owner_evidence', 'checked_utc', 'available_models',
                      'serialized_requests_verified', 'remaining_shared_budget_usd', 'model_calls_dispatched',
                      'public_plan_verification'}:
        raise ValueError('preflight receipt schema mismatch')
    if proof['schema'] != 'd1-preflight-pass-v1' or proof['available_models'] != list(MODELS) or proof['serialized_requests_verified'] != 120 or proof['model_calls_dispatched'] != 0:
        raise ValueError('passing exact-model zero-call preflight required')
    public = proof['public_plan_verification']
    if public.get('url') != frozen['public_plan']['url'] or public.get('sha256') != frozen['public_plan']['sha256'] or public.get('public_raw_hash_matches') is not True or public.get('public_page_markers_verified') is not True:
        raise ValueError('immutable public plan verification required')
    owner = owner_evidence(proof['owner_evidence'], fingerprint(manifest_path)['sha256'])
    checked = datetime.fromisoformat(proof['checked_utc'])
    elapsed = datetime.now(timezone.utc) - checked
    if elapsed < timedelta(0) or elapsed > timedelta(minutes=30): raise ValueError('preflight expired; recheck without inference calls')
    remaining = 500 - owner['shared_model_spend_usd'] - owner['reserved_other_model_spend_usd']
    if owner['launch_owner'] != frozen['launch_owner'] or proof['manifest_sha256'] != fingerprint(manifest_path)['sha256'] or remaining != proof['remaining_shared_budget_usd'] or remaining * 1e6 < frozen['worst_case_reservation_microusd']:
        raise ValueError('owner/manifest/shared-budget mismatch')
    return proof


def execute(frozen, inputs, output, ledger, providers, scientific, preflight_proof=None, observer=None):
    """Permanent attempt marker precedes dispatch; refusal survives alternate output paths."""
    output = Path(output); ledger = Path(ledger)
    if output.exists(): raise ValueError('output exists; audit instead of restarting')
    if not ledger.is_dir(): raise ValueError('owner-created persistent dispatch ledger required')
    prefix = frozen['attempt'] if scientific else frozen['attempt'] + '-zero-model-rehearsal'
    lock = (ledger / (prefix + '.lock')).open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        write_new(ledger / (prefix + '.started.json'), {'attempt': frozen['attempt'], 'manifest_hash': digest(frozen),
                                                      'scientific': scientific, 'automatic_restart_permitted': False})
        output.mkdir(parents=True, exist_ok=False); sync_dir(output.parent)
        run_manifest = {**frozen, 'scientific': scientific, 'preflight': preflight_proof}
        write_new(output / 'manifest.json', run_manifest)
        journal = Journal(output / 'events.jsonl', observer=observer)
        rows = []; begin_run = time.monotonic()
        try:
            journal.emit('manifest', manifest_hash=digest(run_manifest))
            for assignment in frozen['schedule']:
                if time.monotonic() - begin_run >= 3600 or (ledger / (prefix + '.stop')).exists():
                    journal.emit('dispatch_stopped', reason='deadline_or_owner_stop'); break
                model = assignment['model']; item = inputs[assignment['q0_call_id']]
                request = copy.deepcopy(item['request']); provider = providers[model]
                journal.emit('call_start', **assignment, request=request)
                start = time.monotonic(); before = provider.calls
                status = 'valid'; reason = None; http_class = None; response = None
                try:
                    answer = provider.complete(request)
                    if scientific and provider.last_model != model:
                        from providers import ProviderFailure
                        raise ProviderFailure('returned model mismatch', 'provider_model_mismatch')
                    try: response = validate(answer, request['phase'], request['context'])
                    except (ValueError, TypeError, KeyError):
                        status = 'invalid_output'; reason = 'provider_malformed_output'
                except Exception as exc:
                    failure = safe_failure(exc); status = 'provider_failure'
                    reason = failure['reason']; http_class = failure['http_status_class']
                usage = copy.deepcopy(getattr(provider, 'last_usage', {}))
                # Whitelist token fields and types at the journal boundary as well.
                usage = {k: v for k, v in usage.items() if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens') and type(v) is int and v >= 0}
                dispatched = bool(scientific and provider.calls > before)
                row = {**assignment, 'status': status, 'reason': reason, 'http_status_class': http_class,
                       'response': response, 'raw_text': getattr(provider, 'last_response_text', None),
                       'returned_model': getattr(provider, 'last_model', None), 'usage': usage, 'dispatched': dispatched,
                       'dispatch_state': 'outcome_unknown' if dispatched and reason in ('provider_timeout', 'provider_transport_error', 'provider_unknown') else 'terminal',
                       'latency_seconds': round(time.monotonic() - start, 6),
                       'score': score(item['selected'], request, response)}
                rows.append(row); journal.emit('call_terminal', record=row)
                if reason in ('provider_model_mismatch', 'provider_accounting_error', 'provider_local_limit'):
                    journal.emit('dispatch_stopped', reason=reason); break
            journal.emit('complete', terminal=len(rows), assigned=120)
            write_new(output / 'outcomes.json', rows)
            write_new(output / 'summary.json', summarize(run_manifest, journal.events, rows))
            write_new(output / 'reporting.json', {'observer_failures': journal.observer_failures})
        finally: journal.close()
        return {'status': 'bounded-execution-ended', 'assigned': 120, 'terminal': len(rows),
                'physical_calls': sum(r['dispatched'] for r in rows), 'qualification': False}
    finally: lock.close()


def run(manifest, q0, planning, preflight_path, output, ledger, hub_run=None):
    if hub_run is None: raise ValueError('paid run requires owner-started manifest-bound hub run')
    frozen, inputs = verify_manifest(manifest, q0, planning)
    proof = validate_preflight(frozen, manifest, preflight_path)
    providers = {m: anthropic(config(m, proof['remaining_shared_budget_usd'])) for m in MODELS}
    observer = HubProgress(hub_run, fingerprint(manifest)['sha256'], True) if hub_run else None
    result = execute(frozen, inputs, output, ledger, providers, True, proof, observer)
    if observer: observer.finish(output, audit(output, q0, planning))
    return result


def audit(directory, q0, planning, allow_interrupted=False):
    directory = Path(directory); frozen = read(directory / 'manifest.json')
    if frozen['source_hashes'] != source_hashes(): raise ValueError('audit with exact D1 source')
    # Validate the complete frozen protocol without treating saved preflight as a new authorization.
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
        manifest = Path(folder) / 'manifest.json'
        write_new(manifest, {k: v for k, v in frozen.items() if k not in ('scientific', 'preflight')})
        protocol, inputs = verify_manifest(manifest, q0, planning)
    events = read_events(directory / 'events.jsonl')
    if not events or events[0].get('manifest_hash') != digest(frozen): raise ValueError('journal manifest mismatch')
    complete = events[-1]['kind'] == 'complete'
    if not complete and not allow_interrupted: raise ValueError('interrupted run; use audit --allow-interrupted; never restart')
    starts = [e for e in events if e['kind'] == 'call_start']
    terminals = [e['record'] for e in events if e['kind'] == 'call_terminal']
    if len(starts) > 120: raise ValueError('unassigned starts')
    for start, assignment in zip(starts, protocol['schedule']):
        request = inputs[assignment['q0_call_id']]['request']
        if start != {**{k: start[k] for k in ('seq', 'previous', 'kind', 'hash')}, **assignment, 'request': request}:
            raise ValueError('saved schedule or request mismatch')
    by_start = {e['call_id']: e for e in starts}
    for row in terminals:
        start = by_start.get(row['call_id'])
        if start is None: raise ValueError('terminal without start')
        assignment = protocol['schedule'][int(row['call_id'][3:])]
        if any(row[k] != v for k, v in assignment.items()): raise ValueError('terminal assignment drift')
        item = inputs[row['q0_call_id']]
        response = row['response']
        if row['status'] == 'valid':
            validate(response, item['request']['phase'], item['request']['context'])
            if frozen['scientific']:
                if strict_json(row['raw_text']) != response or row['returned_model'] != row['model'] or not row['dispatched']:
                    raise ValueError('saved raw response/model mismatch')
        elif row['status'] not in ('invalid_output', 'provider_failure') or response is not None or row['reason'] not in REASONS:
            raise ValueError('invalid failure record')
        elif row['raw_text'] is not None and row['reason'] == 'provider_malformed_output':
            try:
                validate(strict_json(row['raw_text']), item['request']['phase'], item['request']['context'])
            except (ValueError, TypeError, KeyError): pass
            else: raise ValueError('valid raw response disguised as malformed failure')
        if score(item['selected'], item['request'], response) != row['score']: raise ValueError('saved outcome score mismatch')
    summary = summarize(frozen, events, terminals)
    if complete:
        if read(directory / 'outcomes.json') != terminals or read(directory / 'summary.json') != summary:
            raise ValueError('saved outcomes/summary mismatch')
        if events[-1] != {**{k: events[-1][k] for k in ('seq', 'previous', 'kind', 'hash')}, 'terminal': len(terminals), 'assigned': 120}:
            raise ValueError('final accounting mismatch')
    return {'ok': True, 'complete_journal': complete, 'requests_verified': len(starts),
            'outcomes_recomputed': len(terminals), 'summary': summary}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('prepare', 'preflight', 'run', 'rehearse', 'audit'):
        p = sub.add_parser(name)
        p.add_argument('--q0', type=Path, required=True)
        p.add_argument('--planning-receipt', type=Path, default=DEFAULT_PLAN)
        if name != 'audit': p.add_argument('--output', type=Path, required=True)
        if name in ('preflight', 'run', 'rehearse'): p.add_argument('--manifest', type=Path, required=True)
        if name == 'prepare': p.add_argument('--launch-owner', required=True)
        if name == 'preflight': p.add_argument('--owner-evidence', type=Path, required=True)
        if name == 'run': p.add_argument('--preflight', type=Path, required=True)
        if name in ('run', 'rehearse'):
            p.add_argument('--dispatch-ledger', type=Path, required=True)
            p.add_argument('--hub-run', required=name == 'run', help='Owner-started manifest-bound run; never enqueued by this CLI')
        if name == 'audit':
            p.add_argument('--directory', type=Path, required=True)
            p.add_argument('--allow-interrupted', action='store_true')
        if name == 'rehearse': p.add_argument('--scripted-failure-call', type=int, help='0-based deliberate software failure; no model call')
    args = parser.parse_args(argv)
    try:
        if args.command == 'prepare': result = prepare(args.q0, args.planning_receipt, args.output, args.launch_owner)
        elif args.command == 'preflight': result = preflight(args.manifest, args.q0, args.planning_receipt, args.owner_evidence, args.output)
        elif args.command == 'run': result = run(args.manifest, args.q0, args.planning_receipt, args.preflight, args.output, args.dispatch_ledger, args.hub_run)
        elif args.command == 'rehearse':
            frozen, inputs = verify_manifest(args.manifest, args.q0, args.planning_receipt)
            observer = HubProgress(args.hub_run, fingerprint(args.manifest)['sha256'], False) if args.hub_run else None
            providers = {m: Scripted() for m in MODELS}
            if args.scripted_failure_call is not None:
                if not 0 <= args.scripted_failure_call < 120: raise ValueError('scripted failure index must be 0..119')
                target = frozen['schedule'][args.scripted_failure_call]
                ordinal = sum(a['model'] == target['model'] for a in frozen['schedule'][:args.scripted_failure_call])
                class FailureFixture(Scripted):
                    def complete(self, request):
                        if self.calls == ordinal:
                            self.calls += 1; raise TimeoutError('scripted deliberate failure')
                        return super().complete(request)
                providers[target['model']] = FailureFixture()
            result = execute(frozen, inputs, args.output, args.dispatch_ledger, providers, False, observer=observer)
            if observer: observer.finish(args.output, audit(args.output, args.q0, args.planning_receipt))
        else:
            result = audit(args.directory, args.q0, args.planning_receipt, args.allow_interrupted)
            # Full diagnostics remain in the private output, not stdout/public logs.
            result = {k: v for k, v in result.items() if k != 'summary'}
        print(json.dumps(result, sort_keys=True)); return 0
    except Exception as exc:
        # No paths, credentials, provider bodies or arbitrary exception strings.
        detail = str(exc) if type(exc) is ValueError else 'See owner-private setup and audit evidence; no automatic retry.'
        print(json.dumps({'status': 'stopped', **safe_failure(exc), 'detail': detail}, sort_keys=True))
        return 2


if __name__ == '__main__': raise SystemExit(main())
