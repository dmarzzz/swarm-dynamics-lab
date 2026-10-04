"""D1-Opus: one Opus 5.5 configuration of the D1 instrument. 72 assigned calls, no retries.

60 exact retained Q0 actor requests (the D1 development set, paired by request with the
Haiku/Sonnet D1 cohorts) plus 12 fresh clean full-evidence decisions on worlds 52001-52012,
built offline from the frozen v3 world generator. No swarm rerun, holdout, Q1 world,
queue polling, provisioning or automatic successor. Model identity AND request
configuration change relative to D1 (Opus 5.5 rejects temperature and cannot disable
thinking), so this is a new configuration, never pooled with D1.
"""
import argparse
import copy
from collections import Counter
from datetime import datetime, timezone, timedelta
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.request

import diagnostic_v3 as d1
from diagnostic_v3 import read, fingerprint, write_new, sync_dir, reject_gold, saved_inputs, group_metrics, DEFAULT_PLAN
from tasks import digest, feasible, rng_for
from providers import Anthropic, ProviderFailure
from bench_v3.contracts import SYSTEM, schema, strict_json, validate
from bench_v3.evidence import possible_decisions
from bench_v3.journal import Journal, read_events
from bench_v3.policies import Scripted
from bench_v3.scoring import reference_winner, quorum_state
from bench_v3.worlds import make_case, documents, validate_case, memory_fixtures
from bench_v3.failures import safe_failure, REASONS

ROOT = Path(__file__).resolve().parent
NOTES = ROOT.parent
REPO = ROOT.parents[4]
STUDY = NOTES / 'd1-opus'
PLAN_DOC = STUDY / 'README.md'
SETUP_DOC = STUDY / 'SETUP.md'
PRE_DOC = STUDY / 'reviews/d1o-a1-pre.md'
MODEL = 'claude-opus-5-5'
RATES = (4, 20)  # USD per million input/output tokens, Anthropic pricing table checked 2026-10-04
EXPERIMENT = 'discussion-v3-d1-opus'
ATTEMPT = 'd1o-a1'
VERSION = 'd1-opus-v1'
FRESH_WORLDS = tuple(range(52001, 52013))
EFFORT = 'high'
CONFIG = {'model': MODEL, 'temperature': 'omitted: rejected by claude-opus-5-5',
          'thinking': 'adaptive: cannot be disabled on claude-opus-5-5', 'effort': EFFORT,
          'thinking_display': 'omitted (API default)', 'max_output_tokens': 16000, 'max_input_bytes': 60000,
          'timeout': 600, 'transport_retries': 0, 'output_repair_retries': 0, 'server_fallbacks': 'disabled',
          'worker_count': 1, 'stage_deadline_seconds': 7200}
GATE = {'fresh_clean_full_evidence_justified_required': 10, 'fresh_assigned': 12, 'fresh_valid_required': 12}
ORDER_SEED = 'd1-opus-v1-schedule'


def fresh_stratum(world):
    return 'resolvable' if world <= 52006 else 'ambiguous'


def fresh_items():
    """Clean full-evidence diagnostic requests, built exactly as the v3 runner builds them."""
    items = {}
    for world in FRESH_WORLDS:
        case = make_case(world, fresh_stratum(world)); validate_case(case)
        corpus = documents(case, False)
        context = {'task': case['task'], 'documents': corpus, 'read_ledger': [d['id'] for d in corpus],
                   'reports': [], 'board': [], 'private_history': []}
        request = {'phase': 'diagnostic', 'context': context}
        reject_gold(request)
        if len(json.dumps(request, sort_keys=True).encode()) > CONFIG['max_input_bytes']: raise ValueError('fresh input exceeds byte limit')
        schema('diagnostic', context)
        key = f'fresh-{world}'
        items[key] = {'selected': {'group': 'fresh_diagnostic', 'label': f'{world}:0:diagnostic', 'phase': 'diagnostic',
                                   'agent': 'single', 'q0_call_id': None, 'request_sha256': digest(request)},
                      'request': request}
    return items


def all_inputs(q0, planning):
    plan, saved = saved_inputs(q0, planning)
    inputs = {cid: {'selected': {**row['selected']}, 'request': row['request']} for cid, row in saved.items()}
    inputs.update(fresh_items())
    return plan, inputs


class Opus(Anthropic):
    """Native Messages API for claude-opus-5-5: no temperature, adaptive thinking, explicit effort.

    Accepts thinking blocks before exactly one text block; the text is the only scored output.
    Thinking text is never stored (display is omitted by default).
    """
    def request_body(self, request):
        return {'model': self.model, 'system': self.system_prompt,
                'messages': [{'role': 'user', 'content': json.dumps(request, sort_keys=True)}],
                'max_tokens': self.max_output_tokens, 'thinking': {'type': 'adaptive'},
                'output_config': {'effort': EFFORT,
                                  'format': {'type': 'json_schema', 'schema': self.response_schema(request['phase'], request['context'])}}}

    def complete(self, request):
        self.last_usage = {}; self.last_response_text = None; self.last_model = None
        if self.calls >= self.max_calls: raise ProviderFailure('call budget exhausted', 'provider_local_limit')
        content = json.dumps(request, sort_keys=True)
        if len(content.encode()) > self.max_input_bytes: raise ProviderFailure('input byte budget exceeded', 'provider_local_limit')
        body = self.request_body(request)
        encoded = json.dumps(body).encode()
        reservation = ((len(encoded) + 512) * self.input_rate + self.max_output_tokens * self.output_rate) / 1_000_000
        if self.reserved_usd + reservation > self.max_cost_usd: raise ProviderFailure('dollar reservation exhausted', 'provider_local_limit')
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01'}
        if self.workspace: headers['anthropic-workspace-id'] = self.workspace
        req = urllib.request.Request(self.base + '/messages', data=encoded, headers=headers)
        self.reserved_usd += reservation; self.calls += 1; self.usage_missing_calls += 1
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r: raw = r.read(4_000_001)
            if len(raw) > 4_000_000: raise ProviderFailure('response too large')
            response = json.loads(raw); usage = response.get('usage', {})
            self.last_model = response.get('model')
            self.last_usage = {k: v for k, v in usage.items() if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens') and type(v) is int and v >= 0}
            if all(k in self.last_usage for k in ('input_tokens', 'output_tokens')):
                if any(self.last_usage.get(k, 0) for k in ('cache_creation_input_tokens', 'cache_read_input_tokens')):
                    raise ProviderFailure('unexpected cached usage; accounting requires review', 'provider_accounting_error')
                self.actual_cost_usd += (self.last_usage['input_tokens'] * self.input_rate + self.last_usage['output_tokens'] * self.output_rate) / 1_000_000
                self.input_tokens += self.last_usage['input_tokens']; self.output_tokens += self.last_usage['output_tokens']
                self.usage_missing_calls -= 1
            if response.get('stop_reason') != 'end_turn':
                raise ProviderFailure('incomplete response', 'provider_schema_refusal' if response.get('stop_reason') == 'refusal' else 'provider_incomplete')
            blocks = response['content']
            texts = [b for b in blocks if b.get('type') == 'text']
            if len(texts) != 1 or any(b.get('type') not in ('text', 'thinking', 'redacted_thinking') for b in blocks):
                raise ProviderFailure('unexpected response blocks', 'provider_schema_refusal')
            self.last_response_text = texts[0]['text']
            return self.response_decoder(self.last_response_text)
        except urllib.error.HTTPError as e:
            reason = 'provider_http_' + str(e.code)
            try:
                error = json.loads(e.read(16384)).get('error', {})
                if e.code == 400 and 'credit balance is too low' in error.get('message', '').lower(): reason = 'provider_credit_balance_low'
            except Exception: pass
            raise ProviderFailure(f'provider HTTP {e.code}', public_reason=reason, http_status=e.code) from None
        except ProviderFailure: raise
        except Exception as e:
            raise ProviderFailure('provider failure', **{'public_reason': safe_failure(e)['reason']}) from None


def provider(max_cost_usd):
    return Opus(system_prompt=SYSTEM, response_schema=schema, response_decoder=strict_json, model=MODEL,
                max_calls=72, max_output_tokens=CONFIG['max_output_tokens'], max_input_bytes=CONFIG['max_input_bytes'],
                timeout=CONFIG['timeout'], max_cost_usd=max_cost_usd, input_usd_per_million=RATES[0],
                output_usd_per_million=RATES[1])


def source_hashes():
    paths = list((ROOT / 'bench_v3').glob('*.py'))
    paths += [ROOT / n for n in ('tasks.py', 'providers.py', 'plan_v3_diagnostic.py', 'diagnostic_v3.py', 'diagnostic_v3_opus.py')]
    return {p.relative_to(ROOT).as_posix(): fingerprint(p)['sha256'] for p in sorted(paths)}


def planning_documents():
    return {p.relative_to(REPO).as_posix(): fingerprint(p) for p in (PLAN_DOC, SETUP_DOC, PRE_DOC)}


def source_commit():
    value = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}', value): raise ValueError('source commit required')
    for name, expected in source_hashes().items():
        rel = (ROOT / name).relative_to(REPO).as_posix()
        saved = subprocess.check_output(['git', 'show', f'{value}:{rel}'], cwd=ROOT)
        if hashlib.sha256(saved).hexdigest() != expected: raise ValueError('commit executable source before freezing')
    for rel, expected in planning_documents().items():
        saved = subprocess.check_output(['git', 'show', f'{value}:{rel}'], cwd=ROOT)
        if hashlib.sha256(saved).hexdigest() != expected['sha256']:
            raise ValueError('commit README, SETUP and pre-run assessment before freezing')
    return value


def schedule(plan):
    keys = [s['q0_call_id'] for s in plan['selected']] + [f'fresh-{w}' for w in FRESH_WORLDS]
    order = keys.copy(); rng_for(ORDER_SEED, 'order').shuffle(order)
    return order


def prepare(q0, planning, output, launch_owner):
    if not re.fullmatch('[a-z0-9-]+/[a-z0-9-]+', launch_owner): raise ValueError('nonsecret agent launch owner required')
    plan, inputs = all_inputs(q0, planning)
    opus = Opus.__new__(Opus); opus.model = MODEL; opus.system_prompt = SYSTEM; opus.response_schema = schema
    opus.max_output_tokens = CONFIG['max_output_tokens']
    scheduled = []; reservation = 0
    for index, key in enumerate(schedule(plan)):
        item = inputs[key]; payload = opus.request_body(item['request'])
        allowance = (len(json.dumps(payload).encode()) + 512) * RATES[0] + CONFIG['max_output_tokens'] * RATES[1]
        reservation += allowance
        scheduled.append({'call_id': f'd1o-{index:03d}', 'key': key, 'group': item['selected']['group'],
                          'label': item['selected']['label'], 'request_sha256': item['selected']['request_sha256'],
                          'provider_body_sha256': digest(payload), 'reservation_microusd': allowance})
    commit = source_commit()
    rel = PLAN_DOC.relative_to(REPO).as_posix()
    counts = Counter(r['group'] for r in scheduled)
    frozen = {'schema': VERSION, 'attempt': ATTEMPT, 'experiment': EXPERIMENT, 'parent_attempts': ['v3-q0-a1', 'v3-d1-a1'],
              'status': 'frozen-opus-configuration-preflight-required', 'launch_owner': launch_owner,
              'source_commit': commit, 'source_hashes': source_hashes(), 'planning_documents': planning_documents(),
              'public_plan': {'url': f'https://github.com/dmarzzz/swarm-lab/blob/{commit}/{rel}',
                              'raw_url': f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{commit}/{rel}',
                              'sha256': fingerprint(PLAN_DOC)['sha256']},
              'planning_receipt': fingerprint(planning), 'q0_manifest': fingerprint(Path(q0) / 'manifest.json'),
              'q0_events': fingerprint(Path(q0) / 'events.jsonl'), 'system_hash': digest(SYSTEM),
              'model': MODEL, 'configuration': CONFIG, 'gate': GATE, 'fresh_worlds': list(FRESH_WORLDS),
              'fresh_strata': {str(w): fresh_stratum(w) for w in FRESH_WORLDS},
              'planned_calls': len(scheduled), 'counts': dict(sorted(counts.items())),
              'rates_usd_per_million': {'input': RATES[0], 'output': RATES[1]},
              'worst_case_reservation_microusd': reservation, 'schedule': scheduled,
              'holdout_opened': False, 'q1_ids_used': False, 'successor_dispatch_authorized': False}
    if len(scheduled) != 72 or counts != Counter({'memory': 36, 'report_snapshot': 18, 'diagnostic': 6, 'fresh_diagnostic': 12}):
        raise ValueError('unexpected assignment counts')
    write_new(output, frozen)
    return {'status': frozen['status'], 'manifest_sha256': fingerprint(output)['sha256'], 'calls': 72,
            'worst_case_reservation_usd': reservation / 1e6, 'model_calls_dispatched': 0}


def verify_manifest(manifest, q0, planning):
    frozen = read(manifest)
    if frozen['schema'] != VERSION or frozen['attempt'] != ATTEMPT or frozen['source_hashes'] != source_hashes():
        raise ValueError('manifest source/version mismatch')
    if frozen['source_commit'] != source_commit(): raise ValueError('use exact committed source')
    _, inputs = all_inputs(q0, planning)
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
        rebuilt = Path(folder) / 'manifest.json'
        prepare(q0, planning, rebuilt, frozen['launch_owner'])
        if read(rebuilt) != frozen: raise ValueError('frozen manifest differs from the committed plan')
    return frozen, inputs


def score_fresh(world, request, response):
    case = make_case(world, fresh_stratum(world)); ctx = request['context']
    if case['task'] != ctx['task'] or documents(case, False) != ctx['documents']: raise ValueError('fresh world drift')
    choices = possible_decisions(ctx['task'], ctx['documents'])
    if len(choices) != 1: raise ValueError('fresh answerability drift')
    truth = case['truth']; winner = reference_winner(ctx['task'], truth)
    ev = {'invalid': int(response is None), 'evidence_justified': None, 'truth_correct': None, 'abstain': None,
          'truth_wrong_nonabstain': None, 'constraint_violation': None, 'all_values_extracted_correctly': None,
          'claim_extraction_correct': None, 'claim_extraction_observed': None, 'choice_claim_consistent': None,
          'choice_claim_inconsistent': None, 'citation_mismatches': None}
    if response is not None:
        vote = response['vote']; claims = response['claims']
        extracted = {k: c['value'] for k, c in claims.items() if c is not None}
        endorsing = [{'id': k, 'origin': k, 'authority': 'primary', 'version': 1, 'facts': {k: v}} for k, v in extracted.items()]
        own = possible_decisions(ctx['task'], endorsing)
        by_id = {d['id']: d for d in case['documents']}
        values = {k.split('.')[1]: v for k, v in truth.items() if k.startswith(vote + '.')}
        ev.update(evidence_justified=int(vote == choices[0]), truth_correct=int(vote == winner), abstain=int(vote == 'ABSTAIN'),
                  truth_wrong_nonabstain=int(vote != 'ABSTAIN' and vote != winner),
                  constraint_violation=int(vote != 'ABSTAIN' and not feasible(case['family'], values, ctx['task']['rules'])),
                  all_values_extracted_correctly=int(extracted == truth),
                  claim_extraction_correct=sum(v == truth[k] for k, v in extracted.items()), claim_extraction_observed=len(extracted),
                  choice_claim_consistent=int(len(own) == 1 and vote == own[0]),
                  choice_claim_inconsistent=int(len(own) == 1 and vote != own[0]),
                  citation_mismatches=sum(any(by_id[s]['facts'].get(k) != c['value'] for s in c['sources']) for k, c in claims.items() if c is not None))
    return {'group': 'fresh_diagnostic', 'world': world, 'family': case['family'], 'stratum': fresh_stratum(world), 'evaluation': ev}


def score(item, request, response):
    if item['selected']['group'] == 'fresh_diagnostic':
        return score_fresh(int(item['selected']['label'].split(':')[0]), request, response)
    return d1.score(item['selected'], request, response)


def summarize(frozen, events, rows):
    starts = [e for e in events if e['kind'] == 'call_start']
    ids = [e['call_id'] for e in starts]; terminal = [r['call_id'] for r in rows]
    if len(ids) != len(set(ids)) or len(terminal) != len(set(terminal)) or set(terminal) - set(ids):
        raise ValueError('duplicate/unstarted records')
    valid_usage = [r for r in rows if all(type(r['usage'].get(k)) is int and r['usage'][k] >= 0 for k in ('input_tokens', 'output_tokens'))]
    missing_usage = [r['call_id'] for r in rows if r['dispatched'] and r not in valid_usage]
    tokens = {k: sum(r['usage'][k] for r in valid_usage) for k in ('input_tokens', 'output_tokens')}
    counts = frozen['counts']
    groups = {g: group_metrics([r for r in rows if r['score']['group'] == g], counts[g]) for g in ('diagnostic', 'report_snapshot', 'fresh_diagnostic')}
    memory = {s: group_metrics([r for r in rows if r['score'].get('state') == s], 6)
              for s in ('complete', 'omitted', 'conflict', 'correlated_copies', 'superseded', 'inherited_false')}
    worlds = []
    for world in range(20001, 20007):
        votes = [next((r['response'] for r in rows if r['score'].get('world') == world and r['score']['group'] == 'report_snapshot'
                       and r['score'].get('agent') == agent), None) for agent in range(3)]
        state = quorum_state(votes)
        case = make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')
        winner = reference_winner(case['task'], case['truth'])
        worlds.append({'world': world, **state, 'truth_correct': int(state['decision'] == winner)})
    fresh = [r for r in rows if r['score']['group'] == 'fresh_diagnostic']
    fresh_ok = sum(r['score']['evaluation'].get('evidence_justified') == 1 for r in fresh)
    fresh_valid = sum(r['status'] == 'valid' for r in fresh)
    complete = len(rows) == len(starts) == 72 and not missing_usage
    full = sum(r['score']['evaluation'].get('truth_correct') == 1 for r in rows if r['score']['group'] == 'diagnostic')
    report = sum(w['truth_correct'] for w in worlds)
    return {'schema': VERSION, 'attempt': frozen['attempt'], 'model': MODEL, 'assigned_calls': 72, 'started': len(starts),
            'terminal': len(rows), 'valid': sum(r['status'] == 'valid' for r in rows),
            'unresolved': sorted(set(ids) - set(terminal)), 'failures': dict(Counter(r['reason'] for r in rows if r['status'] != 'valid')),
            'usage_missing_calls': missing_usage, **tokens,
            'observed_usage_cost_microusd': tokens['input_tokens'] * RATES[0] + tokens['output_tokens'] * RATES[1],
            'latency_seconds': [r['latency_seconds'] for r in rows], 'groups': groups, 'memory': memory, 'report_quorums': worlds,
            'development_comparison': {'full_evidence_correct': full, 'saved_report_quorum_correct': report, 'assigned_each': 6,
                                       'd1_haiku': {'full_evidence_correct': 2, 'saved_report_quorum_correct': 1},
                                       'd1_sonnet': {'full_evidence_correct': 3, 'saved_report_quorum_correct': 3}},
            'fresh_gate': {'evidence_justified': fresh_ok, 'valid': fresh_valid, **GATE,
                           'passed': bool(frozen.get('scientific', True) and complete and fresh_valid == 12 and fresh_ok >= 10)},
            'model_qualified_for_swarm': False, 'holdout_opened': False, 'successors_dispatched': False,
            'limitations': ['Opus 5.5 rejects temperature and cannot disable thinking: model AND configuration changed versus D1.',
                            'The 60 saved requests are reused development items; the 12 fresh worlds are clean full-evidence decisions only.',
                            'Q0 report packets remain Haiku-generated; no fresh report or swarm stage is included.',
                            'N=3 single-value majority merge structurally discards conflicts.',
                            'Ambiguous dispatched calls are never retried; absent usage is unknown cost, not zero.']}


class HubProgress:
    def __init__(self, hub_run, manifest_sha256, scientific):
        expected = f'{EXPERIMENT}/{ATTEMPT}' + ('' if scientific else '-rehearsal')
        if hub_run != expected: raise ValueError('wrong bounded hub run')
        import swarm_report as sr
        current = sr.get_run(hub_run)
        if current.get('status') != 'running' or current.get('params', {}).get('manifest_sha256') != manifest_sha256:
            raise ValueError('owner must start one manifest-bound hub run before attachment')
        self.reporter = sr.Run(hub_run, EXPERIMENT, current['params'])
        self.started = self.terminal = self.invalid = self.physical = self.cost_micro = self.missing_usage = 0

    def metrics(self):
        return {'assigned_calls': 72, 'started_calls': self.started, 'terminal_calls': self.terminal,
                'physical_model_calls': self.physical, 'invalid_calls': self.invalid,
                'observed_usage_cost_usd': self.cost_micro / 1e6, 'usage_missing_calls': self.missing_usage}

    def __call__(self, event):
        if event['kind'] == 'call_start': self.started += 1
        if event['kind'] == 'call_terminal':
            row = event['record']; self.terminal += 1
            self.invalid += row['status'] != 'valid'; self.physical += row['dispatched']
            self.missing_usage += row['dispatched'] and not all(k in row['usage'] for k in ('input_tokens', 'output_tokens'))
            self.cost_micro += row['usage'].get('input_tokens', 0) * RATES[0] + row['usage'].get('output_tokens', 0) * RATES[1]
        if event['kind'] in ('call_start', 'call_terminal', 'dispatch_stopped', 'complete'):
            self.reporter.progress(self.terminal, 72, message='D1-Opus: 60 saved + 12 fresh clean decisions.', **self.metrics())

    def finish(self, output, checked):
        from bench_v3.hub_worker import publish
        summary = checked['summary']
        write_new(Path(output) / 'audit.json', {k: v for k, v in checked.items() if k != 'summary'})
        publish(self.reporter, Path(output))
        extra = {'fresh_justified': summary['fresh_gate']['evidence_justified'], 'qualification_passed': int(summary['fresh_gate']['passed'])}
        if self.terminal == 72 and not self.invalid and not self.missing_usage:
            self.reporter.done(message='D1-Opus execution/audit complete; see fresh gate and development comparison.', **self.metrics(), **extra)
        else:
            self.reporter.fail(message='D1-Opus retained failures/missingness; no retry or successor.', **self.metrics(), **extra)


def execute(frozen, inputs, output, ledger, prov, scientific, observer=None):
    output = Path(output); ledger = Path(ledger)
    if output.exists(): raise ValueError('output exists; audit instead of restarting')
    if not ledger.is_dir(): raise ValueError('persistent dispatch ledger required')
    prefix = frozen['attempt'] if scientific else frozen['attempt'] + '-zero-model-rehearsal'
    lock = (ledger / (prefix + '.lock')).open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        write_new(ledger / (prefix + '.started.json'), {'attempt': frozen['attempt'], 'manifest_hash': digest(frozen),
                                                      'scientific': scientific, 'automatic_restart_permitted': False})
        output.mkdir(parents=True, exist_ok=False); sync_dir(output.parent)
        run_manifest = {**frozen, 'scientific': scientific}
        write_new(output / 'manifest.json', run_manifest)
        journal = Journal(output / 'events.jsonl', observer=observer)
        rows = []; begin = time.monotonic()
        try:
            journal.emit('manifest', manifest_hash=digest(run_manifest))
            for assignment in frozen['schedule']:
                if time.monotonic() - begin >= CONFIG['stage_deadline_seconds'] or (ledger / (prefix + '.stop')).exists():
                    journal.emit('dispatch_stopped', reason='deadline_or_owner_stop'); break
                item = inputs[assignment['key']]; request = copy.deepcopy(item['request'])
                journal.emit('call_start', **assignment, request=request)
                start = time.monotonic(); before = prov.calls
                status = 'valid'; reason = None; http_class = None; response = None
                try:
                    answer = prov.complete(request)
                    if scientific and prov.last_model != MODEL:
                        raise ProviderFailure('returned model mismatch', 'provider_model_mismatch')
                    try: response = validate(answer, request['phase'], request['context'])
                    except (ValueError, TypeError, KeyError):
                        status = 'invalid_output'; reason = 'provider_malformed_output'
                except Exception as exc:
                    failure = safe_failure(exc); status = 'provider_failure'
                    reason = failure['reason']; http_class = failure['http_status_class']
                usage = {k: v for k, v in copy.deepcopy(getattr(prov, 'last_usage', {})).items()
                         if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens') and type(v) is int and v >= 0}
                dispatched = bool(scientific and prov.calls > before)
                row = {**assignment, 'status': status, 'reason': reason, 'http_status_class': http_class, 'response': response,
                       'raw_text': getattr(prov, 'last_response_text', None), 'returned_model': getattr(prov, 'last_model', None),
                       'usage': usage, 'dispatched': dispatched,
                       'dispatch_state': 'outcome_unknown' if dispatched and reason in ('provider_timeout', 'provider_transport_error', 'provider_unknown') else 'terminal',
                       'latency_seconds': round(time.monotonic() - start, 6), 'score': score(item, request, response)}
                rows.append(row); journal.emit('call_terminal', record=row)
                if reason in ('provider_model_mismatch', 'provider_accounting_error', 'provider_local_limit', 'provider_credit_balance_low'):
                    journal.emit('dispatch_stopped', reason=reason); break
            journal.emit('complete', terminal=len(rows), assigned=72)
            write_new(output / 'outcomes.json', rows)
            write_new(output / 'summary.json', summarize(run_manifest, journal.events, rows))
            write_new(output / 'reporting.json', {'observer_failures': journal.observer_failures})
        finally: journal.close()
        return {'status': 'bounded-execution-ended', 'assigned': 72, 'terminal': len(rows),
                'physical_calls': sum(r['dispatched'] for r in rows)}
    finally: lock.close()


def check_model():
    """Authenticated metadata GET only; never an inference probe."""
    key = os.environ.get('SWARM_MODEL_API_KEY', '')
    if not key: raise ValueError('secure model environment absent')
    headers = {'x-api-key': key, 'anthropic-version': '2023-06-01'}
    if os.environ.get('SWARM_MODEL_WORKSPACE_ID'): headers['anthropic-workspace-id'] = os.environ['SWARM_MODEL_WORKSPACE_ID']
    with urllib.request.urlopen(urllib.request.Request('https://api.anthropic.com/v1/models/' + MODEL, headers=headers), timeout=120) as r:
        row = strict_json(r.read(200000).decode())
    caps = row.get('capabilities', {})
    if row.get('id') != MODEL or not caps.get('structured_outputs', {}).get('supported') or not caps.get('effort', {}).get(EFFORT, {}).get('supported'):
        raise ValueError('exact model or required capability unavailable; no fallback')
    return {'id': row['id'], 'structured_outputs': True, 'effort_' + EFFORT: True}


def public_plan(frozen):
    expected = frozen['public_plan']
    with urllib.request.urlopen(expected['raw_url'], timeout=120) as r: raw = r.read(1000000)
    if hashlib.sha256(raw).hexdigest() != expected['sha256']: raise ValueError('public immutable plan content mismatch')
    text = raw.decode('utf-8')
    for section in ('TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics'):
        if '\n## ' + section + '\n' not in text: raise ValueError('public plan section absent')
    return {'url': expected['url'], 'sha256': expected['sha256'], 'public_raw_hash_matches': True}


def preflight(manifest, q0, planning, output, max_cost_usd):
    frozen, inputs = verify_manifest(manifest, q0, planning)
    if max_cost_usd * 1e6 < frozen['worst_case_reservation_microusd']: raise ValueError('reservation exceeds authorized cap')
    prov = provider(max_cost_usd)
    for row in frozen['schedule']:
        if digest(prov.request_body(inputs[row['key']]['request'])) != row['provider_body_sha256']:
            raise ValueError('native provider serialization changed')
    result = {'schema': 'd1-opus-preflight-v1', 'manifest_sha256': fingerprint(manifest)['sha256'],
              'checked_utc': datetime.now(timezone.utc).isoformat(), 'model': check_model(),
              'serialized_requests_verified': 72, 'max_cost_usd': max_cost_usd, 'model_calls_dispatched': 0,
              'public_plan_verification': public_plan(frozen)}
    write_new(output, result)
    return {'status': 'preflight-passed', 'model_calls_dispatched': 0, 'preflight_sha256': fingerprint(output)['sha256']}


def validate_preflight(frozen, manifest, path):
    proof = read(path)
    if proof.get('schema') != 'd1-opus-preflight-v1' or proof['manifest_sha256'] != fingerprint(manifest)['sha256'] \
            or proof['serialized_requests_verified'] != 72 or proof['model_calls_dispatched'] != 0 \
            or proof['public_plan_verification'].get('sha256') != frozen['public_plan']['sha256']:
        raise ValueError('passing zero-call preflight required')
    elapsed = datetime.now(timezone.utc) - datetime.fromisoformat(proof['checked_utc'])
    if elapsed < timedelta(0) or elapsed > timedelta(minutes=30): raise ValueError('preflight expired; recheck without inference calls')
    if proof['max_cost_usd'] * 1e6 < frozen['worst_case_reservation_microusd']: raise ValueError('reservation exceeds authorized cap')
    return proof


def run(manifest, q0, planning, preflight_path, output, ledger, hub_run):
    frozen, inputs = verify_manifest(manifest, q0, planning)
    proof = validate_preflight(frozen, manifest, preflight_path)
    observer = HubProgress(hub_run, fingerprint(manifest)['sha256'], True)
    result = execute(frozen, inputs, output, ledger, provider(proof['max_cost_usd']), True, observer)
    observer.finish(output, audit(output, q0, planning))
    return result


def audit(directory, q0, planning, allow_interrupted=False):
    directory = Path(directory); frozen = read(directory / 'manifest.json')
    if frozen['source_hashes'] != source_hashes(): raise ValueError('audit with exact source')
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
        manifest = Path(folder) / 'manifest.json'
        write_new(manifest, {k: v for k, v in frozen.items() if k != 'scientific'})
        protocol, inputs = verify_manifest(manifest, q0, planning)
    events = read_events(directory / 'events.jsonl')
    if not events or events[0].get('manifest_hash') != digest(frozen): raise ValueError('journal manifest mismatch')
    complete = events[-1]['kind'] == 'complete'
    if not complete and not allow_interrupted: raise ValueError('interrupted run; use --allow-interrupted; never restart')
    starts = [e for e in events if e['kind'] == 'call_start']
    terminals = [e['record'] for e in events if e['kind'] == 'call_terminal']
    if len(starts) > 72: raise ValueError('unassigned starts')
    for start, assignment in zip(starts, protocol['schedule']):
        if start != {**{k: start[k] for k in ('seq', 'previous', 'kind', 'hash')}, **assignment, 'request': inputs[assignment['key']]['request']}:
            raise ValueError('schedule or request mismatch')
    for row in terminals:
        assignment = protocol['schedule'][int(row['call_id'][4:])]
        if any(row[k] != v for k, v in assignment.items()): raise ValueError('terminal assignment drift')
        item = inputs[row['key']]; response = row['response']
        if row['status'] == 'valid':
            validate(response, item['request']['phase'], item['request']['context'])
            if frozen['scientific'] and (strict_json(row['raw_text']) != response or row['returned_model'] != MODEL or not row['dispatched']):
                raise ValueError('saved raw response/model mismatch')
        elif row['status'] not in ('invalid_output', 'provider_failure') or response is not None or row['reason'] not in REASONS:
            raise ValueError('invalid failure record')
        if score(item, item['request'], response) != row['score']: raise ValueError('saved outcome score mismatch')
    summary = summarize(frozen, events, terminals)
    if complete and (read(directory / 'outcomes.json') != terminals or read(directory / 'summary.json') != summary):
        raise ValueError('saved outcomes/summary mismatch')
    return {'ok': True, 'complete_journal': complete, 'requests_verified': len(starts), 'outcomes_recomputed': len(terminals), 'summary': summary}


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
        if name == 'preflight': p.add_argument('--max-cost-usd', type=float, required=True)
        if name == 'run': p.add_argument('--preflight', type=Path, required=True)
        if name in ('run', 'rehearse'):
            p.add_argument('--dispatch-ledger', type=Path, required=True)
            p.add_argument('--hub-run', required=name == 'run')
        if name == 'audit':
            p.add_argument('--directory', type=Path, required=True)
            p.add_argument('--allow-interrupted', action='store_true')
        if name == 'rehearse': p.add_argument('--scripted-failure-call', type=int)
    args = parser.parse_args(argv)
    try:
        if args.command == 'prepare': result = prepare(args.q0, args.planning_receipt, args.output, args.launch_owner)
        elif args.command == 'preflight': result = preflight(args.manifest, args.q0, args.planning_receipt, args.output, args.max_cost_usd)
        elif args.command == 'run': result = run(args.manifest, args.q0, args.planning_receipt, args.preflight, args.output, args.dispatch_ledger, args.hub_run)
        elif args.command == 'rehearse':
            frozen, inputs = verify_manifest(args.manifest, args.q0, args.planning_receipt)
            observer = HubProgress(args.hub_run, fingerprint(args.manifest)['sha256'], False) if args.hub_run else None
            prov = Scripted()
            if args.scripted_failure_call is not None:
                if not 0 <= args.scripted_failure_call < 72: raise ValueError('scripted failure index must be 0..71')
                target = args.scripted_failure_call
                class FailureFixture(Scripted):
                    def complete(self, request):
                        if self.calls == target:
                            self.calls += 1; raise TimeoutError('scripted deliberate failure')
                        return super().complete(request)
                prov = FailureFixture()
            result = execute(frozen, inputs, args.output, args.dispatch_ledger, prov, False, observer=observer)
            if observer: observer.finish(args.output, audit(args.output, args.q0, args.planning_receipt))
        else:
            result = {k: v for k, v in audit(args.directory, args.q0, args.planning_receipt, args.allow_interrupted).items() if k != 'summary'}
        print(json.dumps(result, sort_keys=True)); return 0
    except Exception as exc:
        detail = str(exc) if type(exc) is ValueError else 'See private evidence; no automatic retry.'
        print(json.dumps({'status': 'stopped', **safe_failure(exc), 'detail': detail}, sort_keys=True))
        return 2


if __name__ == '__main__': raise SystemExit(main())
