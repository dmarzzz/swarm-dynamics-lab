"""Discussion v3 swarm qualification on claude-opus-5-5, chained into a 24-world S1 comparison.

Reuses the frozen bench_v3 instrument (runner, worlds, contracts, scoring, analysis, journal,
replay) unchanged and adds only: an Opus 5.5 request path (no temperature, adaptive thinking,
explicit effort, 16,000-token ceiling, thinking blocks filtered, refusal counted), fresh world
namespaces, and a chain that runs probe -> Q0 -> S1 and stops at the first failed software gate.
Model AND request configuration differ from v3-q0-a1 (Haiku, temperature 0, 2,000 tokens), so
this is a new configuration under its own hub experiment, never pooled with Haiku results.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import urllib.error
import urllib.request

from tasks import digest
from providers import Anthropic, ProviderFailure
from bench_v3 import VERSION as BENCH_VERSION
from bench_v3.contracts import SYSTEM, schema, strict_json, validate
from bench_v3.worlds import make_case, memory_fixtures, SPLITS, validate_case
from bench_v3.scoring import parent_score
from bench_v3.runner import Runner, allocation, ARMS
from bench_v3.evidence import possible_decisions
from bench_v3.worlds import documents
from tasks import rng_for
from bench_v3.journal import Journal, Replay, read_events
from bench_v3.policies import Scripted
from bench_v3.analysis import summarize
from bench_v3.replay_view import render
from bench_v3.portable_audit import summary_equal
from bench_v3.failures import safe_failure

ROOT = Path(__file__).resolve().parent
VERSION = 'v3-opus-chain-v1'
EXPERIMENT = 'discussion-v3-opus'
MODEL = 'claude-opus-5-5'
RATES = (4, 20)  # USD per million input/output tokens (Anthropic list price, checked 2026-10-04)
EFFORT = 'high'  # same as the passed D1-Opus configuration
MAX_OUTPUT_TOKENS = 16000  # thinking tokens bill as output and count against this ceiling
VISIBLE_ANSWER_MAX_CHARS = 8000  # about the old 2,000-token visible ceiling, enforced on the text block
ROUNDS = 3
STAGES = {
    # Fresh namespaces, disjoint from dev 10002-10007, tests 10101-10160, Q0 20001-20006,
    # holdout 30000-30023 (closed), sidecar 40001-40012, Q1 50001-50006, D1-Opus 52001-52012.
    'q0': {'worlds': list(range(54001, 54007)), 'resolvable': 3},
    's1': {'worlds': list(range(54101, 54125)), 'resolvable': 12},
}
CONFIG = {'model': MODEL, 'temperature': 'omitted: rejected by claude-opus-5-5',
          'thinking': 'adaptive (cannot be disabled on claude-opus-5-5)', 'effort': EFFORT,
          'max_output_tokens': MAX_OUTPUT_TOKENS, 'visible_answer_max_chars': VISIBLE_ANSWER_MAX_CHARS,
          'max_input_bytes': 60000, 'timeout': 600,
          'transport_retries': 'at most 2 per logical call, only HTTP 429/529 (model not run), within the 600 s request timeout; every attempt reserved and counted against the attempt cap; model answers never retried',
          'attempt_cap': 'planned calls + max(10, planned calls // 10)',
          'dispatch_order': 'clean-first: per world clean acquisition, report snapshot, reports-only arm and clean full-evidence diagnostic; early gate after those 66 calls; then remaining clean arms, attacked exposures, memory fixtures',
          'server_fallbacks': 'disabled',
          'refusal': 'stop_reason refusal counted separately (public reason provider_schema_refusal)',
          'input_usd_per_million': RATES[0], 'output_usd_per_million': RATES[1]}


def stage_cases(stage):
    spec = STAGES[stage]
    reserved = set(SPLITS['holdout']) | set(range(50001, 50007)) | set(range(52001, 52013)) | set(range(40001, 40013))
    if reserved & set(spec['worlds']): raise ValueError('reserved world namespace')
    return [make_case(w, 'resolvable' if i < spec['resolvable'] else 'ambiguous') for i, w in enumerate(spec['worlds'])]


def planned_calls(stage):
    return allocation(stage_cases(stage), ROUNDS)[1]


def source_hashes():
    paths = sorted((ROOT / 'bench_v3').glob('*.py')) + [ROOT / 'tasks.py', ROOT / 'providers.py', ROOT / 'bench_v3_opus.py']
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


class Opus(Anthropic):
    """Native Messages API for claude-opus-5-5, ported from the passed D1-Opus adapter."""
    def __init__(self, max_calls, max_cost_usd):
        super().__init__(system_prompt=SYSTEM, response_schema=schema, response_decoder=strict_json, model=MODEL,
                         max_calls=max_calls, max_output_tokens=MAX_OUTPUT_TOKENS, max_input_bytes=CONFIG['max_input_bytes'],
                         timeout=CONFIG['timeout'], max_cost_usd=max_cost_usd,
                         input_usd_per_million=RATES[0], output_usd_per_million=RATES[1])
        self.refusals = 0; self.model_mismatches = 0; self.last_stop_reason = None
        self.attempts = 0; self.max_attempts = max_calls + max(10, max_calls // 10); self.transport_retries = 0
        self.sleep = time.sleep

    RETRYABLE = (429, 529)
    MAX_RETRIES = 2

    def send(self, encoded, reservation, headers):
        """Dispatch with at most two retries, only for HTTP 429/529 (the provider did not run the model)."""
        started = time.monotonic(); retries = 0
        while True:
            if self.attempts >= self.max_attempts: raise ProviderFailure('attempt cap exhausted', 'provider_local_limit')
            if self.reserved_usd + reservation > self.max_cost_usd: raise ProviderFailure('dollar reservation exhausted', 'provider_local_limit')
            remaining = self.timeout - (time.monotonic() - started)
            if remaining <= 1: raise ProviderFailure('request timeout window exhausted', 'provider_timeout')
            self.reserved_usd += reservation; self.attempts += 1
            req = urllib.request.Request(self.base + '/messages', data=encoded, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=remaining) as r: return r.read(4_000_001)
            except urllib.error.HTTPError as e:
                if e.code in self.RETRYABLE and retries < self.MAX_RETRIES:
                    wait = min(2.0 * (2 ** retries), 20.0)
                    try:
                        after = float(e.headers.get('retry-after')) if e.headers and e.headers.get('retry-after') else None
                        if after is not None: wait = min(max(after, 0.5), 30.0)
                    except Exception: pass
                    if time.monotonic() - started + wait < self.timeout - 1:
                        retries += 1; self.transport_retries += 1; self.sleep(wait); continue
                raise

    def request_body(self, request):
        return {'model': self.model, 'system': self.system_prompt,
                'messages': [{'role': 'user', 'content': json.dumps(request, sort_keys=True)}],
                'max_tokens': self.max_output_tokens, 'thinking': {'type': 'adaptive'},
                'output_config': {'effort': EFFORT,
                                  'format': {'type': 'json_schema', 'schema': self.response_schema(request['phase'], request['context'])}}}

    def complete(self, request):
        self.last_usage = {}; self.last_response_text = None; self.last_model = None; self.last_stop_reason = None
        if self.calls >= self.max_calls: raise ProviderFailure('call budget exhausted', 'provider_local_limit')
        if len(json.dumps(request, sort_keys=True).encode()) > self.max_input_bytes:
            raise ProviderFailure('input byte budget exceeded', 'provider_local_limit')
        encoded = json.dumps(self.request_body(request)).encode()
        reservation = ((len(encoded) + 512) * self.input_rate + self.max_output_tokens * self.output_rate) / 1_000_000
        if self.reserved_usd + reservation > self.max_cost_usd: raise ProviderFailure('dollar reservation exhausted', 'provider_local_limit')
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01'}
        if self.workspace: headers['anthropic-workspace-id'] = self.workspace
        self.calls += 1; self.usage_missing_calls += 1
        try:
            raw = self.send(encoded, reservation, headers)
            if len(raw) > 4_000_000: raise ProviderFailure('response too large', 'provider_incomplete')
            response = json.loads(raw); usage = response.get('usage', {})
            self.last_model = response.get('model'); self.last_stop_reason = response.get('stop_reason')
            self.last_usage = {k: v for k, v in usage.items() if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens') and type(v) is int and v >= 0}
            if all(k in self.last_usage for k in ('input_tokens', 'output_tokens')):
                if any(self.last_usage.get(k, 0) for k in ('cache_creation_input_tokens', 'cache_read_input_tokens')):
                    raise ProviderFailure('unexpected cached usage', 'provider_accounting_error')
                self.actual_cost_usd += (self.last_usage['input_tokens'] * self.input_rate + self.last_usage['output_tokens'] * self.output_rate) / 1_000_000
                self.input_tokens += self.last_usage['input_tokens']; self.output_tokens += self.last_usage['output_tokens']
                self.usage_missing_calls -= 1
            if self.last_model != self.model:
                self.model_mismatches += 1
                raise ProviderFailure('returned model differs', 'provider_model_mismatch')
            if self.last_stop_reason != 'end_turn':
                if self.last_stop_reason == 'refusal': self.refusals += 1
                raise ProviderFailure('incomplete response', 'provider_schema_refusal' if self.last_stop_reason == 'refusal' else 'provider_incomplete')
            blocks = response['content']
            texts = [b for b in blocks if b.get('type') == 'text']
            if len(texts) != 1 or any(b.get('type') not in ('text', 'thinking', 'redacted_thinking') for b in blocks):
                raise ProviderFailure('unexpected response blocks', 'provider_schema_refusal')
            self.last_response_text = texts[0]['text']  # thinking text is never stored
            if len(self.last_response_text) > VISIBLE_ANSWER_MAX_CHARS:
                raise ProviderFailure('visible answer exceeds ceiling', 'provider_incomplete')
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
            raise ProviderFailure('provider failure', public_reason=safe_failure(e)['reason']) from None

    def accounting(self):
        return {'calls': self.calls, 'input_tokens': self.input_tokens, 'output_tokens': self.output_tokens,
                'cost_usd': round(self.actual_cost_usd, 6), 'reserved_usd': round(self.reserved_usd, 6),
                'usage_missing_calls': self.usage_missing_calls, 'refusals': self.refusals,
                'model_mismatches': self.model_mismatches, 'attempts': self.attempts,
                'max_attempts': self.max_attempts, 'transport_retries': self.transport_retries}


class GateStop(Exception):
    """The clean-first early gate failed; the remaining assignments are deliberately not dispatched."""
    def __init__(self, rows, gate):
        super().__init__('early gate failed'); self.rows = rows; self.gate = gate


def early_gate(rows, failures):
    clean_full = [r for r in rows if r['kind'] == 'diagnostic' and not r['attack']]
    clean_reports = [r for r in rows if r['kind'] == 'swarm' and r['arm'] == 'reports' and not r['attack']]
    diag = sum(r['evaluation']['justified'] for r in clean_full)
    rep = sum(r['evaluation']['vote_correct'] for r in clean_reports)
    return {'clean_full_evidence_correct': diag, 'clean_reports_correct': rep, 'assigned_each': len(clean_full),
            'call_failures_so_far': failures, 'passed': len(clean_full) == len(clean_reports) == 6 and diag >= 5 and rep >= 5 and failures == 0}


class CleanFirstRunner(Runner):
    """bench_v3 Runner with clean-first dispatch (same calls and records, different order).

    Phase 1, per world: clean acquisition, clean report snapshot, clean reports-only arm, clean full-evidence
    diagnostic (11 calls/world). With early_gate=True the Q0 competence gate is decided after phase 1 and a failure
    stops dispatch. Phase 2: remaining clean arms. Phase 3: attacked exposures (all arms + diagnostic). Phase 4:
    memory fixtures. The order is deterministic, so exact-source replay reproduces it.
    """
    def __init__(self, provider, journal, rounds=3, early=False):
        super().__init__(provider, journal, rounds); self.early = early

    def execute(self, cases, assignments):
        if len({case['id'] for case in cases}) != len(cases): raise ValueError('duplicate world identifiers')
        planned, _ = allocation(cases, self.rounds)
        if digest(sorted(assignments, key=lambda a: a['id'])) != digest(sorted(planned, key=lambda a: a['id'])):
            raise ValueError('assignments differ from frozen allocation')
        for case in cases: validate_case(case)
        rows = []; expected = {r['id'] for r in assignments}
        def terminal(row):
            if row['id'] not in expected: raise ValueError('unassigned terminal record')
            expected.remove(row['id']); rows.append(row); self.journal.emit('terminal', record=row)
        def diagnostic(case, attack):
            label = f'{case["id"]}:{int(attack)}:diagnostic'
            corpus = documents(case, attack)
            context = {'task': case['task'], 'documents': corpus, 'read_ledger': [d['id'] for d in corpus],
                       'reports': [], 'board': [], 'private_history': []}
            answer = self.call('diagnostic', context, label, 'single')
            possibilities = possible_decisions(case['task'], corpus)
            expected_answer = possibilities[0] if len(possibilities) == 1 else 'ABSTAIN'
            terminal({'id': label, 'kind': 'diagnostic', 'world': case['id'], 'family': case['family'],
                      'stratum': case['stratum'], 'attack': attack, 'status': 'completed', 'answer': answer,
                      'evaluation': {'invalid': int(answer is None), 'justified': int(answer is not None and answer['vote'] == expected_answer)}})
        def arm_order(case, attack):
            arms = [a for a in ARMS if a != 'reports']; rng_for(BENCH_VERSION, case['id'], attack, 'arm-order').shuffle(arms)
            return arms
        clean = {}
        for case in cases:
            clean[case['id']] = self.prepare_reports(case, False, self.acquire(case, False))
            terminal(self.continue_arm(case, False, 'reports', clean[case['id']]))
            diagnostic(case, False)
        gate = early_gate(rows, self.failures)
        self.journal.emit('early_gate', **gate)
        if self.early and not gate['passed']: raise GateStop(rows, gate)
        for case in cases:
            for arm in arm_order(case, False): terminal(self.continue_arm(case, False, arm, clean[case['id']]))
        for case in cases:
            snapshot = self.prepare_reports(case, True, self.acquire(case, True))
            for arm in ['reports'] + arm_order(case, True): terminal(self.continue_arm(case, True, arm, snapshot))
            diagnostic(case, True)
        for fixture in memory_fixtures():
            answer = self.call('parent', fixture['context'], fixture['id'], 'parent')
            score = parent_score(fixture['context'], answer, fixture['truth_answer'])
            terminal({'id': fixture['id'], 'kind': 'memory', 'family': fixture['family'], 'state': fixture['state'],
                      'variant': fixture['variant'], 'status': 'completed', 'answer': answer, 'evaluation': score})
        if expected: raise ValueError('missing terminal assignments')
        return rows


def write_json(path, value):
    with open(path, 'x', encoding='utf-8') as stream:
        json.dump(value, stream, sort_keys=True, indent=2); stream.write('\n')


def manifest(stage, provider, launch_record=None):
    worlds = stage_cases(stage)
    assigned, calls = allocation(worlds, ROUNDS)
    frozen = {'schema': BENCH_VERSION, 'chain_version': VERSION, 'stage': stage, 'split': 'opus-' + stage,
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'runtime': {'python': platform.python_version(), 'system': platform.system(), 'machine': platform.machine()},
              'rounds': ROUNDS, 'n_agents': 3, 'worlds': [c['id'] for c in worlds],
              'strata': {str(c['id']): c['stratum'] for c in worlds},
              'world_hashes': {str(c['id']): digest(c) for c in worlds},
              'source_hashes': source_hashes(), 'system_hash': digest(SYSTEM), 'provider': provider.name,
              'scientific': provider.scientific, 'model_config': CONFIG if provider.scientific else None,
              'assignments': assigned, 'planned_calls': calls, 'retry_policy': 'none',
              'reserved_holdout': SPLITS['holdout']}
    if launch_record is not None: frozen['launch_record'] = launch_record
    return frozen, worlds


def run_stage(destination, stage, provider, observer=None, launch_record=None):
    frozen, worlds = manifest(stage, provider, launch_record)
    destination.mkdir(parents=True, exist_ok=False)
    write_json(destination / 'manifest.json', frozen)
    journal = Journal(destination / 'events.jsonl', observer=observer)
    try:
        journal.emit('manifest', manifest_hash=digest(frozen))
        try:
            rows = CleanFirstRunner(provider, journal, ROUNDS, early=(stage == 'q0')).execute(worlds, frozen['assignments'])
        except GateStop as stop:
            journal.emit('early_stop', **stop.gate, terminal_rows=len(stop.rows))
            write_json(destination / 'episodes-partial.json', stop.rows)
            summary = {'schema': frozen['schema'], 'scientific': frozen['scientific'], 'early_stop': True,
                       'qualification': {'execution_complete': False, 'early_stop': True, 'model_qualified': False,
                                         'competence_screen_pass': False, 'required_each': 5, **stop.gate},
                       'reconciliation': {'planned_calls': frozen['planned_calls'], 'terminal_rows': len(stop.rows),
                                          'assigned_rows': len(frozen['assignments'])}}
            write_json(destination / 'summary.json', summary)
            render(journal.events, stop.rows, destination / 'replay.html')
            return summary
        journal.emit('complete', episodes=len(rows))
        write_json(destination / 'episodes.json', rows)
        summary = summarize(frozen, rows, journal.events)
        write_json(destination / 'summary.json', summary)
        render(journal.events, rows, destination / 'replay.html')
        return summary
    finally:
        journal.close()


def audit(directory):
    frozen = strict_json((directory / 'manifest.json').read_text())
    if frozen['source_hashes'] != source_hashes(): raise ValueError('source hashes changed; audit at the recorded revision')
    events = read_events(directory / 'events.jsonl')
    if not events or events[0].get('manifest_hash') != digest(frozen): raise ValueError('manifest hash mismatch')
    if events[-1]['kind'] != 'complete': raise ValueError('interrupted run; assignments remain unresolved')
    saved = strict_json((directory / 'episodes.json').read_text())
    if [e['record'] for e in events if e['kind'] == 'terminal'] != saved: raise ValueError('terminal records differ from saved episodes')
    playback = Replay(events)
    regenerated = CleanFirstRunner(playback, Journal(), frozen['rounds'], early=False).execute(stage_cases(frozen['stage']), frozen['assignments'])
    playback.finish()
    if regenerated != saved: raise ValueError('saved-response outcome replay mismatch')
    summary = summarize(frozen, regenerated, events)
    if not summary_equal(strict_json((directory / 'summary.json').read_text()), summary): raise ValueError('summary mismatch')
    rec = summary['reconciliation']
    if rec['missing'] or rec['unresolved_calls'] or rec['started_calls'] != frozen['planned_calls']:
        raise ValueError('assignment or call accounting mismatch')
    return {'ok': True, 'episodes': len(saved), 'requests_replayed': playback.calls, 'journal_events': len(events)}


def load_launch(path):
    """Owner-authorized launch record: exact source, stage caps and the waiver evidence file digest."""
    launch = strict_json(Path(path).read_text())
    required = {'status', 'experiment', 'model', 'configuration', 'source_hashes', 'stages', 'owner_authorization'}
    if set(launch) != required or launch['status'] != 'owner-waived-opus-chain' or launch['experiment'] != EXPERIMENT:
        raise ValueError('launch record is not an owner-authorized Opus chain')
    if launch['model'] != MODEL or launch['configuration'] != CONFIG: raise ValueError('configuration differs from source')
    if launch['source_hashes'] != source_hashes(): raise ValueError('launch record does not match this source')
    for stage in STAGES:
        caps = launch['stages'][stage]
        if caps['max_calls'] != planned_calls(stage): raise ValueError('call allowance must equal the planned allocation')
        if not 0 < caps['max_cost_usd'] <= 2000: raise ValueError('bad reservation ceiling')
    proof = launch['owner_authorization']
    evidence = (Path(path).parent / proof['path']).resolve()
    if hashlib.sha256(evidence.read_bytes()).hexdigest() != proof['sha256']: raise ValueError('authorization evidence hash mismatch')
    return launch


class Reporter:
    """Forwards to the hub reporter with an accurate message (review waived, not pending)."""
    def __init__(self, inner, stage, cases_total):
        self.inner = inner; self.stage = stage; self.cases_total = cases_total
    def progress(self, step, total, message=None, **metrics):
        if 'model_cost_usd' in metrics: metrics['cost_usd'] = metrics['model_cost_usd']
        episodes = metrics.get('episodes', 0)
        self.inner.progress(step, total, message=f'{self.stage.upper()} Opus: {episodes}/{self.cases_total} cases; {step}/{total} calls; review waived by owner', **metrics)
    def artifact(self, *a, **k): return self.inner.artifact(*a, **k)
    def done(self, **k): return self.inner.done(**k)
    def fail(self, **k): return self.inner.fail(**k)


SPEC = {'title': 'Discussion and memory v3 on Opus 5.5',
        'description': 'Exploratory three-agent swarm benchmark on claude-opus-5-5 (adaptive thinking, effort high, no temperature): independent votes, reports only, private work and public discussion; paired clean/contaminated evidence and fresh-parent memory probes. Q0 qualification on 6 fresh worlds, then S1 on 24 fresh worlds if Q0 passes. Owner waived cross-researcher review. New configuration; not pooled with the Haiku v3-q0-a1 run.',
        'owner': 'dmarz',
        'params': {'stage': {'type': 'str', 'role': 'stage'}, 'batch': {'type': 'str', 'role': 'replicate'},
                   'rounds': {'type': 'int'}, 'n_agents': {'type': 'int'}, 'model': {'type': 'str'}, 'effort': {'type': 'str'}},
        'metrics': ['model_calls', 'cost_usd', 'model_cost_usd', 'usage_missing_calls', 'episodes', 'invalid_calls',
                    'parent_unsupported', 'parent_inherited_error', 'clean_accuracy', 'qualification_passed', 'execution_complete', 'refusals'],
        'primary_metric': 'model_calls',
        'url': 'https://github.com/dmarzzz/swarm-lab/tree/main/researchers/dmarz/notes/discussion-dose/v3-opus'}


def execute_stage(sr, stage, launch, destination, batch, provider):
    from bench_v3.hub_worker import Progress, publish
    run_id = f'{EXPERIMENT}/{batch}'
    if destination.exists(): raise ValueError('output already exists; no automatic restart')
    if any(r['run'] == run_id for r in sr.runs(EXPERIMENT, limit=5000)): raise ValueError('batch already on hub')
    worlds = stage_cases(stage); calls = planned_calls(stage)
    sr.register(EXPERIMENT, **SPEC)
    inner = sr.start(EXPERIMENT, run=run_id, params={'batch': batch, 'stage': stage.upper(), 'rounds': ROUNDS, 'n_agents': 3,
                     'model': MODEL if provider.scientific else provider.name, 'effort': EFFORT, 'planned_calls': calls,
                     'review': 'waived by owner'}, message=f'{stage.upper()} Opus chain stage started')
    reporter = Reporter(inner, stage, len(allocation(worlds, ROUNDS)[0]))
    tracker = Progress(destination, worlds, reporter, ROUNDS, calls, RATES)
    try:
        summary = run_stage(destination, stage, provider, observer=tracker, launch_record=launch)
        tracker.finish()
        if summary.get('early_stop'):
            acct = provider.accounting() if hasattr(provider, 'accounting') else {'calls': provider.calls}
            write_json(destination / 'accounting.json', acct)
            publish(inner, destination)
            q = summary['qualification']
            metrics = tracker.metrics(); metrics['cost_usd'] = metrics['model_cost_usd']
            inner.done(message=(f'{stage.upper()} stopped early at the clean-first gate: clean diagnostic {q["clean_full_evidence_correct"]}/6, '
                                f'clean reports {q["clean_reports_correct"]}/6, call failures {q["call_failures_so_far"]}; remaining assignments not dispatched by design. Review waived by owner.'),
                       **metrics, refusals=acct.get('refusals', 0), qualification_passed=0, execution_complete=0)
            return summary
        checked = audit(destination); write_json(destination / 'audit.json', checked)
        acct = provider.accounting() if hasattr(provider, 'accounting') else {'calls': provider.calls}
        write_json(destination / 'accounting.json', acct)
        write_json(destination / 'reporting.json', {'reporting_errors': tracker.reporting_errors})
        publish(inner, destination)
        q = summary['qualification']
        metrics = tracker.metrics(); metrics['cost_usd'] = metrics['model_cost_usd']
        message = (f'{stage.upper()} complete and replay-audited. ' + (('Qualification ' + ('passed' if q['model_qualified'] else 'did not pass') +
                   f'; clean diagnostic {q["clean_full_evidence_correct"]}/6, clean reports {q["clean_reports_correct"]}/6.') if stage == 'q0'
                   else 'Exploratory comparison; no gate.') + ' Review waived by owner.')
        inner.done(message=message, **metrics, refusals=acct.get('refusals', 0),
                   qualification_passed=int(q['model_qualified']), execution_complete=int(q['execution_complete']))
        return summary
    except BaseException as exc:
        if destination.exists():
            tracker.finish()
            try: publish(inner, destination)
            except Exception: pass
        metrics = tracker.metrics(); metrics['cost_usd'] = metrics['model_cost_usd']
        inner.fail(message=f'{stage.upper()} incomplete: {type(exc).__name__}; ledger preserved', **metrics)
        raise


def probe_request():
    """One parent-phase memory fixture: exercises the full Opus contract, scored nowhere."""
    fixture = memory_fixtures()[0]
    return {'phase': 'parent', 'context': copy.deepcopy(fixture['context'])}, fixture['expected_supported']


def run_probe(provider, outdir):
    request, expected = probe_request()
    record = {'kind': 'interface-probe', 'model': MODEL, 'created_utc': datetime.now(timezone.utc).isoformat()}
    try:
        answer = provider.complete(request)
        record.update(status='valid', answer=answer, expected_supported=expected, model_returned=provider.last_model,
                      stop_reason=provider.last_stop_reason, usage=provider.last_usage)
        try:
            validate(answer, 'parent', request['context']); ok = True  # same contract the runner applies
        except (ValueError, TypeError, KeyError):
            ok = False; record['status'] = 'invalid_contract'
    except ProviderFailure as exc:
        record.update(status='failed', **safe_failure(exc), usage=provider.last_usage, stop_reason=getattr(provider, 'last_stop_reason', None))
        ok = False
    record['accounting'] = provider.accounting() if hasattr(provider, 'accounting') else {}
    write_json(outdir / 'probe.json', record)
    return ok, record


def chain(sr, launch_path, outdir, prefix, scripted=False):
    """probe -> Q0 -> (gate) -> S1. Stops at the first failed software gate; never retries."""
    launch = load_launch(launch_path)
    outdir.mkdir(parents=True, exist_ok=True)
    state = {'started_utc': datetime.now(timezone.utc).isoformat(), 'prefix': prefix, 'stages': {}}
    def save():
        (outdir / 'chain-state.json').write_text(json.dumps(state, sort_keys=True, indent=2))
    if not scripted:
        ok, record = run_probe(Opus(1, 1.0), outdir)
        state['probe'] = {'ok': ok, 'status': record['status'], 'cost_usd': record['accounting'].get('cost_usd')}; save()
        if not ok:
            state['stopped'] = 'probe failed'; save(); return state
    for stage in ('q0', 's1'):
        caps = launch['stages'][stage]
        provider = Scripted() if scripted else Opus(caps['max_calls'], caps['max_cost_usd'])
        batch = f'{prefix}-{stage}'
        summary = execute_stage(sr, stage, launch, outdir / batch, batch, provider)
        q = summary['qualification']
        state['stages'][stage] = {'batch': batch, 'execution_complete': q['execution_complete'],
                                  'model_qualified': q['model_qualified'], 'clean_full_evidence_correct': q['clean_full_evidence_correct'],
                                  'clean_reports_correct': q['clean_reports_correct'],
                                  'accounting': provider.accounting() if hasattr(provider, 'accounting') else {'calls': provider.calls}}
        save()
        if stage == 'q0' and not (q['model_qualified'] or (scripted and q['execution_complete'])):
            state['stopped'] = 'Q0 gate failed; S1 not started'; save(); return state
        if not q['execution_complete']:
            state['stopped'] = f'{stage} execution incomplete'; save(); return state
    state['finished_utc'] = datetime.now(timezone.utc).isoformat(); save()
    return state


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('chain'); p.add_argument('--launch', type=Path, required=True); p.add_argument('--outdir', type=Path, required=True)
    p.add_argument('--prefix', required=True); p.add_argument('--scripted', action='store_true')
    p = sub.add_parser('audit'); p.add_argument('directory', type=Path)
    p = sub.add_parser('plan')
    args = parser.parse_args(argv)
    if args.command == 'plan':
        out = {s: {'worlds': STAGES[s]['worlds'], 'planned_calls': planned_calls(s)} for s in STAGES}
        out['source_hashes'] = source_hashes(); out['configuration'] = CONFIG
        print(json.dumps(out, indent=2, sort_keys=True)); return 0
    if args.command == 'audit':
        print(json.dumps(audit(args.directory), indent=2)); return 0
    import swarm_report as sr
    print(json.dumps(chain(sr, args.launch, args.outdir, args.prefix, scripted=args.scripted), indent=2, sort_keys=True))
    return 0


if __name__ == '__main__': sys.exit(main())
