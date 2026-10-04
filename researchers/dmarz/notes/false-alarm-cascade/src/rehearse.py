"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

    python3 src/rehearse.py --hub-dir <dir with hub.py and swarm_report.py>

Runs the chain six times, each on a fresh hub, in fresh temporary result and ledger directories:
  (a) S0, P0, Q0, S1 to completion with a stub that answers every call by the private-evidence
      reference policy (and posts claims by the scripted rule), then `chain verify`;
  (b) with a stub that skips on any suspicious inspection, which must fail Q0, stop the chain with
      exit 3, and leave no S1 run on the hub;
  (c) with the reference stub and one HTTP 500 during S1: that episode ends, dispatch continues,
      S1 ends done with one failed episode and the primary contrast reported as bounds;
  (d) with an HTTP 500 in every 40th S1 call: the fourth failed episode exceeds the limit of 3,
      dispatch stops and S1 ends failed;
  (e) with a credit-balance error three times and then a healthy provider: one pause, no failed
      row, S1 done;
  (f) with a credit-balance error that does not end: S1 stops with provider_credit_balance_low and
      the unfinished rows not started; then `chain resume` with a healthy stub completes S1, and
      the analysis and `verify` see every row exactly once.

The stub reads the request exactly as the provider sends it, so each later round's answer depends
on the board that earlier stub answers produced. It refuses any hub that is not on 127.0.0.1 and
blocks every other network destination for the process. The provider's waits are replaced by a
no-op, so nothing sleeps. A rehearsal answer is never a sample and never leaves the machine. No
model call is made.
"""
import argparse
import io
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze
import chain
import coordinator
import provider
import study
import worker

LOCAL = '127.0.0.1'


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


CREDIT_BODY = json.dumps({'type': 'error', 'error': {
    'type': 'invalid_request_error',
    'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}}).encode()


class Stub:
    """Stands in for the model endpoint. Answers count_tokens and messages requests in the real
    response shape: a thinking block before one text block, model id, stop reason and usage.

    mode 'private': the private-evidence reference decision for the packet in the request, with
                    claims by the scripted rule.
    mode 'jumpy':   skip on any suspicious inspection (an over-cautious agent); fails Q0.
    `fail`:   a function of the messages request's ordinal; True answers it with HTTP 500.
    `credit`: a function of the ordinal; True answers it with the HTTP 400 credit-balance error.
    """
    def __init__(self, mode='private', output_tokens=600, fail=None, credit=None, hold=0.002):
        self.mode, self.output_tokens, self.fail, self.credit, self.hold = mode, output_tokens, fail, credit, hold
        self.lock = threading.Lock()
        self.count_calls = self.message_calls = self.in_flight = self.max_in_flight = 0
        self.credit_errors = self.answered = 0
        self.models = set()                         # model ids seen in messages requests

    def __call__(self, request, timeout=None):
        url = request.full_url
        if url not in (provider.COUNT_URL, provider.MESSAGES_URL):
            raise AssertionError('stub_unexpected_url')
        headers = {k.lower(): v for k, v in request.header_items()}
        if not headers.get('x-api-key') or headers.get('anthropic-version') != '2023-06-01':
            raise AssertionError('stub_missing_headers')
        body = json.loads(request.data)
        tokens = len(request.data) // 3            # rough: about 3 characters per token for this JSON
        if url == provider.COUNT_URL:
            if tuple(body) != tuple(k for k in provider.REQUEST_KEYS if k != 'max_tokens'):
                raise AssertionError('stub_count_body_keys')
            with self.lock:
                self.count_calls += 1
            return _Response(json.dumps({'input_tokens': tokens}).encode())
        if tuple(body) != provider.REQUEST_KEYS or set(body['output_config']) != {'effort', 'format'}:
            raise AssertionError('stub_message_body_keys')
        if body['system'] != study.SYSTEM or body['output_config']['format']['schema'] != study.schema():
            raise AssertionError('stub_prompt_or_schema')
        packet = json.loads(body['messages'][0]['content'])
        with self.lock:
            self.models.add(body['model'])
            self.message_calls += 1
            n = self.message_calls
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
        try:
            time.sleep(self.hold)                   # long enough for concurrent requests to overlap
            if self.credit and self.credit(n):
                with self.lock:
                    self.credit_errors += 1
                raise urllib.error.HTTPError(url, 400, 'Bad Request', {'request-id': f'req_stub_{n:06d}'}, io.BytesIO(CREDIT_BODY))
            if self.fail and self.fail(n):
                raise urllib.error.HTTPError(url, 500, 'stub failure', {'request-id': f'req_stub_{n:06d}'},
                                             io.BytesIO(b'{"type": "error", "error": {"type": "api_error", "message": "stub failure"}}'))
            answer = study.jumpy_answer(packet) if self.mode == 'jumpy' else study.scripted_answer(packet, 'private', True)
            answer['rationale'] = 'Stub answer from own inspection counts.'
        finally:
            with self.lock:
                self.in_flight -= 1
        with self.lock:
            self.answered += 1
        return _Response(json.dumps({
            'id': f'msg_stub_{n:06d}', 'type': 'message', 'role': 'assistant', 'model': body['model'],
            'content': [{'type': 'thinking', 'thinking': '', 'signature': 'stub'},
                        {'type': 'text', 'text': json.dumps(answer)}],
            'stop_reason': 'end_turn', 'stop_sequence': None,
            'usage': {'input_tokens': tokens, 'output_tokens': self.output_tokens,
                      'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}}).encode())


def no_wait(seconds):
    """Replaces the provider's sleep in the rehearsal: backoffs and billing waits take no time."""


def block_network():
    """Every urllib request of this process must go to 127.0.0.1."""
    original = urllib.request.urlopen

    def guarded(target, *args, **kwargs):
        url = target.full_url if isinstance(target, urllib.request.Request) else target
        if urllib.parse.urlparse(url).hostname != LOCAL:
            raise RuntimeError('rehearsal_network_blocked')
        return original(target, *args, **kwargs)
    urllib.request.urlopen = guarded


def free_port():
    with socket.socket() as s:
        s.bind((LOCAL, 0))
        return s.getsockname()[1]


def start_hub(hub_dir, data_dir, log):
    port, token = free_port(), secrets.token_hex(16)
    proc = subprocess.Popen([sys.executable, str(hub_dir / 'hub.py'), '--data', str(data_dir), '--bind', LOCAL,
                             '--port', str(port)], env={**os.environ, 'SWARM_HUB_TOKEN': token},
                            stdout=log, stderr=subprocess.STDOUT)
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:{port}', SWARM_HUB_TOKEN=token)
    return proc


def require_local(sr):
    urls = [os.environ.get('SWARM_HUB_URL', '')]
    if hasattr(sr, '_config'):
        urls.append(sr._config().get('SWARM_HUB_URL', ''))
    if any(urllib.parse.urlparse(u).hostname != LOCAL for u in urls):
        raise SystemExit('rehearse: refusing to run: the hub is not on 127.0.0.1')


def wait_for_hub(sr, proc):
    for _ in range(100):
        if proc.poll() is not None:
            raise SystemExit('rehearse: the throwaway hub exited')
        try:
            sr.runs(study.EXPERIMENT, limit=1)
            return
        except Exception:
            time.sleep(0.1)
    raise SystemExit('rehearse: the throwaway hub did not answer')


def stage_runs(sr):
    return {(r.get('params') or {}).get('stage'): r for r in sr.runs(study.EXPERIMENT, limit=5000)}


def scenario(sr, hub_dir, tmp, name, stub, stages, verify=False, resume_with=None):
    """One chain on a fresh hub, fresh results directory and fresh ledger. With `resume_with`, a
    second stub then drives `chain resume` on the same hub, results and ledger."""
    base = tmp / name
    base.mkdir()
    with (base / 'hub.log').open('w') as log:
        proc = start_hub(hub_dir, base / 'hubdata', log)
        try:
            require_local(sr)
            wait_for_hub(sr, proc)
            ledger_path = base / 'ledger' / 'ledger.jsonl'
            started = time.monotonic()
            code = chain.run_chain(stages, sr, base / 'results', ledger_path, opener=stub, sleep=no_wait)
            elapsed = time.monotonic() - started
            status = chain.read_status(base / 'results')
            out = {'exit': code, 'seconds': elapsed, 'status': status, 'runs': stage_runs(sr),
                   'stub_messages': stub.message_calls, 'stub_counts': stub.count_calls,
                   'max_in_flight': stub.max_in_flight, 'credit_errors': stub.credit_errors,
                   'ledger': provider.Ledger(ledger_path).transact(), 'replay_refused': None, 'verify': None}
            entries = chain.stage_entries(status or {}, 'S1')
            if entries and all((Path(e.get('results_dir', '')) / 'episodes.jsonl.gz').exists() for e in entries):
                out['s1_rows'] = analyze.read_rows(Path(entries[0]['results_dir']) / 'episodes.jsonl.gz')
            else:
                out['s1_rows'] = None
            if resume_with is not None:
                # A resume that is not allowed is refused and queues nothing.
                started = time.monotonic()
                code = chain.resume_chain(sr, base / 'results', ledger_path, opener=resume_with, sleep=no_wait)
                status = chain.read_status(base / 'results')
                entries = chain.stage_entries(status or {}, 'S1')
                out['resume'] = {'exit': code, 'seconds': time.monotonic() - started, 'status': status,
                                 'runs': sr.runs(study.EXPERIMENT, limit=5000),
                                 'rows': analyze.read_rows(Path(entries[-1]['results_dir']) / 'episodes.jsonl.gz') if len(entries) > 1 else None,
                                 'merged': chain.saved_rows(entries) if len(entries) > 1 else None,
                                 'stub_messages': resume_with.message_calls,
                                 'ledger': provider.Ledger(ledger_path).transact(),
                                 'again': chain.resume_chain(sr, base / 'results', ledger_path, opener=resume_with, sleep=no_wait)}
                out['status'] = status
            if verify:
                started_verify = time.monotonic()
                out['verify'] = chain.verify(sr, base / 'results')
                out['verify']['seconds'] = time.monotonic() - started_verify
            if name == 'a':
                try:
                    coordinator.enqueue(sr, 'S0')
                    out['replay_refused'] = False
                except ValueError as exc:
                    out['replay_refused'] = str(exc) == 'batch_exists_no_replay'
                out['resume_refused'] = chain.resume_chain(sr, base / 'results', ledger_path, opener=stub, sleep=no_wait) == chain.EXIT_STOPPED
            return out
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


def ladder_scenario(sr, hub_dir, tmp, stages, credit_from):
    """The model ladder on one hub and source hash: the first rung's chain stops on a billing
    outage that does not end; then P0, Q0 and S1 run on the second rung with its own results
    directory and ledger, as the launcher's --model does. S0 is not repeated."""
    base = tmp / 'g'
    base.mkdir()
    ladder = study.design()['model_ladder']
    with (base / 'hub.log').open('w') as log:
        proc = start_hub(hub_dir, base / 'hubdata', log)
        try:
            require_local(sr)
            wait_for_hub(sr, proc)
            first_stub = Stub('private', credit=lambda n: n >= credit_from)
            first = chain.run_chain(stages, sr, base / 'results', base / 'accounting' / 'ledger.jsonl',
                                    opener=first_stub, sleep=no_wait)
            os.environ['STUDY_MODEL'] = ladder[1]
            try:
                # Before P0 on the second rung exists, its Q0 must be refused even though the first
                # rung's Q0 passed at this source hash.
                try:
                    coordinator.enqueue(sr, 'Q0')
                    cross_refused = False
                except ValueError as exc:
                    cross_refused = str(exc).startswith('exact_runtime_qualification_required')
                second_stub = Stub('private')
                second = chain.run_chain(stages[1:], sr, base / 'results-opus-5',
                                         base / 'accounting' / 'ledger-opus-5.jsonl', opener=second_stub, sleep=no_wait)
                status = chain.read_status(base / 'results-opus-5')
                entries = chain.stage_entries(status or {}, 'S1')
                rows = analyze.read_rows(Path(entries[0]['results_dir']) / 'episodes.jsonl.gz') if entries else []
                ledger2 = provider.Ledger(base / 'accounting' / 'ledger-opus-5.jsonl').transact()
            finally:
                os.environ.pop('STUDY_MODEL', None)
            ledger1 = provider.Ledger(base / 'accounting' / 'ledger.jsonl').transact()
            return {'first_exit': first, 'second_exit': second, 'cross_refused': cross_refused,
                    'runs': sr.runs(study.EXPERIMENT, limit=5000), 'rows': rows, 'status': status,
                    'first_models': first_stub.models, 'second_models': second_stub.models,
                    'second_messages': second_stub.message_calls, 'ledger1': ledger1, 'ledger2': ledger2}
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True, help='directory with hub.py and swarm_report.py (not part of this repo)')
    ap.add_argument('--keep', action='store_true', help='keep the temporary directory and print its path')
    a = ap.parse_args(argv)
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('rehearse: --hub-dir needs hub.py and swarm_report.py')
    tmp = Path(tempfile.mkdtemp(prefix='false-alarm-rehearsal-'))
    if study.ROOT in tmp.resolve().parents:
        raise SystemExit('rehearse: temporary directory is inside the study tree')
    # The client reads these; nothing points outside this machine and the model key is a dummy.
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:1', SWARM_HUB_TOKEN='unset-until-hub-starts',
                      SWARM_SOURCE='rehearsal/local', SWARM_SPOOL=str(tmp / 'spool'), SWARM_NO_AUTO_REFRESH='1',
                      SWARM_MODEL_API_KEY='rehearsal-stub-not-a-key', SWARM_MODEL_WORKSPACE_ID='rehearsal-stub')
    os.environ.pop(provider.LEDGER_ENV, None)
    os.environ.pop('STUDY_RESULTS_DIR', None)
    block_network()
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    require_local(sr)

    stages = list(study.STAGES)
    d = study.design()
    budget = d['budget']
    required = set(worker.REQUIRED_METRICS)
    paid_before_s1 = budget['max_calls']['P0'] + budget['max_calls']['Q0']
    per_round = len(d['world']['members']) - 1
    s1_rows = budget['max_calls']['S1']
    after = d['windows']['after_correction']
    checks = {}

    def metrics(run, stage):
        return run['runs'].get(stage, {}).get('metrics') or {}

    def count(rows, status):
        return sum(r['status'] == status for r in rows)
    try:
        a_run = scenario(sr, hub_dir, tmp, 'a', Stub('private'), stages, verify=True)
        runs = a_run['runs']
        checks['a_exit_zero'] = a_run['exit'] == 0
        checks['a_state_completed'] = (a_run['status'] or {}).get('state') == 'completed'
        checks['a_all_stages_done'] = all(runs.get(s, {}).get('status') == 'done' for s in stages)
        checks['a_metrics_reported'] = all(required <= set(metrics(a_run, s)) for s in stages)
        checks['a_calls_per_stage'] = {s: metrics(a_run, s).get('model_calls') for s in stages} == budget['max_calls']
        checks['a_gates_passed'] = all(metrics(a_run, s).get('qualification_passed') == 1 for s in stages[:3])
        checks['a_ledger_total_calls'] = a_run['ledger']['attempted_calls'] == budget['max_attempted_calls'] == a_run['stub_messages']
        checks['a_verify_ok'] = bool(a_run['verify'] and a_run['verify']['ok'])
        checks['a_replay_refused'] = a_run['replay_refused'] is True
        checks['a_resume_refused_without_credit_stop'] = a_run['resume_refused'] is True
        s1 = metrics(a_run, 'S1')
        checks['a_team_episodes_complete'] = s1.get('team_episodes') == s1.get('team_episodes_complete') == d['stages']['S1']['episodes']
        checks['a_requests_in_flight_within_limit'] = 1 < a_run['max_in_flight'] <= budget['workers']
        checks['a_no_failure_no_fallback_no_pause'] = (s1.get('failed') == 0 and s1.get('failed_episodes') == 0
                                                       and s1.get('count_fallbacks') == 0 and s1.get('billing_pauses') == 0)
        # The stub is the private-evidence policy, so the paired contrast must be exactly zero.
        checks['a_reference_stub_shows_zero_effect'] = s1.get('residual_avoidance_pp') == 0 and s1.get('cascade_size_pp') == 0
        rows = a_run['s1_rows'] or []
        boards = [len(r['packet']['board']) for r in rows if r.get('packet') and r['round'] == d['world']['rounds']]
        checks['a_later_rounds_carry_earlier_answers'] = bool(boards) and min(boards) > 0 and all(
            len(r['packet']['your_decisions']['r01']) == r['round'] - 1 for r in rows)

        b_run = scenario(sr, hub_dir, tmp, 'b', Stub('jumpy'), stages)
        runs = b_run['runs']
        status = b_run['status'] or {}
        checks['b_exit_stopped'] = b_run['exit'] == chain.EXIT_STOPPED
        checks['b_state_stopped_at_gate'] = status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'Q0'
        checks['b_no_s1_run_on_hub'] = 'S1' not in runs and 'S1' not in (status.get('stages') or {})
        checks['b_q0_failed_with_metrics'] = (runs.get('Q0', {}).get('status') == 'failed'
                                              and required <= set(metrics(b_run, 'Q0'))
                                              and metrics(b_run, 'Q0').get('qualification_passed') == 0)
        checks['b_s0_p0_done'] = all(runs.get(s, {}).get('status') == 'done' for s in ('S0', 'P0'))
        checks['b_calls_stopped_before_s1'] = b_run['ledger']['attempted_calls'] == paid_before_s1 == b_run['stub_messages']

        # (c) One failed call. The first two episodes dispatched are a C0 and an FA+C episode, so the
        # failure lands in a cell of the primary contrast and the contrast must be reported as bounds.
        one = paid_before_s1 + 2 * per_round + 3
        c_run = scenario(sr, hub_dir, tmp, 'c', Stub('private', fail=lambda n: n == one), stages, verify=True)
        rows = c_run['s1_rows'] or []
        failed = [r for r in rows if r['status'] == 'failed']
        s1 = metrics(c_run, 'S1')
        checks['c_exit_zero_and_s1_done'] = c_run['exit'] == 0 and c_run['runs'].get('S1', {}).get('status') == 'done'
        checks['c_one_failed_call_with_evidence'] = (len(failed) == 1 and failed[0].get('error') == 'http_500'
                                                     and failed[0]['accounting'].get('http_status') == 500
                                                     and 'stub failure' in failed[0]['accounting'].get('error_body', '')
                                                     and failed[0]['accounting'].get('request_id', '').startswith('req_stub_'))
        episode = failed[0]['episode'] if failed else None
        later = [r for r in rows if r['episode'] == episode and r['round'] > failed[0]['round']] if failed else []
        checks['c_failed_episode_ends_there'] = bool(later) and all(r['status'] == 'not_started' and 'packet' not in r for r in later)
        checks['c_dispatch_continued'] = (len(rows) == s1_rows and count(rows, 'not_started') == len(later)
                                          and count(rows, 'completed') == s1_rows - len(later) - 1)
        checks['c_metrics_truthful'] = (s1.get('failed') == 1 and s1.get('failed_episodes') == 1
                                        and s1.get('invalid') == len(later) + 1 and s1.get('team_episodes_complete') == 119
                                        and s1.get('model_calls') == s1_rows - len(later))
        primary = None
        entry = ((c_run['status'] or {}).get('stages') or {}).get('S1') or {}
        if entry.get('results_dir'):
            primary = json.loads((Path(entry['results_dir']) / 'analysis.json').read_text())['primary']
        checks['c_primary_reported_as_bounds'] = bool(
            primary and primary['mean'] is None and primary['roots'] == 24 and primary['complete_roots'] == 23
            and primary['all_assigned_bounds'][0] < primary['all_assigned_bounds'][1] and primary['complete_case_mean'] == 0
            and 'residual_avoidance_pp' not in s1)
        checks['c_verify_ok'] = bool(c_run['verify'] and c_run['verify']['ok'])

        # (d) A failure in every 40th S1 call: the fourth failed episode exceeds max_failed = 3.
        d_run = scenario(sr, hub_dir, tmp, 'd', Stub('private', fail=lambda n: n > paid_before_s1 and (n - paid_before_s1) % 40 == 3),
                         stages, verify=True)
        rows = d_run['s1_rows'] or []
        status = d_run['status'] or {}
        s1 = metrics(d_run, 'S1')
        started = len(rows) - count(rows, 'not_started')
        checks['d_exit_stopped'] = d_run['exit'] == chain.EXIT_STOPPED
        checks['d_stopped_over_the_limit'] = (status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'S1'
                                              and status.get('reason') == 'failed_units_exceed_limit')
        checks['d_s1_failed_with_metrics'] = (d_run['runs'].get('S1', {}).get('status') == 'failed' and required <= set(s1)
                                              and s1.get('failed_episodes') == budget['max_failed'] + 1 == len({r['episode'] for r in rows if r['status'] == 'failed'}))
        checks['d_dispatch_stopped'] = (len(rows) == s1_rows and started == d_run['stub_messages'] - paid_before_s1
                                        and started <= 40 * (budget['max_failed'] + 1) + budget['workers'] and s1.get('model_calls') == started)
        checks['d_verify_ok'] = bool(d_run['verify'] and d_run['verify']['ok'])

        # (e) A billing outage that ends: three credit-balance errors, then a healthy provider.
        first = paid_before_s1 + 4 * per_round + 2
        e_run = scenario(sr, hub_dir, tmp, 'e', Stub('private', credit=lambda n: first <= n < first + 3), stages, verify=True)
        rows = e_run['s1_rows'] or []
        s1 = metrics(e_run, 'S1')
        checks['e_exit_zero_and_s1_done'] = e_run['exit'] == 0 and e_run['runs'].get('S1', {}).get('status') == 'done'
        checks['e_no_row_failed'] = len(rows) == s1_rows and count(rows, 'completed') == s1_rows and s1.get('invalid') == 0
        checks['e_pause_reported'] = (e_run['credit_errors'] == 3 and s1.get('billing_pauses', 0) >= 1 and s1.get('billing_pause_seconds', 0) >= 60
                                      and 1 <= s1.get('billing_affected_calls', 0) <= 3)
        checks['e_resends_recorded_in_ledger'] = (e_run['ledger']['transport_attempts'] == budget['max_attempted_calls'] + 3
                                                  and e_run['ledger']['attempted_calls'] == budget['max_attempted_calls'])
        checks['e_reference_stub_shows_zero_effect'] = s1.get('residual_avoidance_pp') == 0
        checks['e_verify_ok'] = bool(e_run['verify'] and e_run['verify']['ok'])

        # (f) A billing outage that does not end, then a resume with a healthy provider.
        f_run = scenario(sr, hub_dir, tmp, 'f', Stub('private', credit=lambda n: n >= paid_before_s1 + 200), stages,
                         verify=True, resume_with=Stub('private'))
        rows = f_run['s1_rows'] or []
        interrupted = [r for r in rows if r.get('interrupted')]
        runs = {(r.get('params') or {}).get('batch'): r for r in f_run['resume']['runs']}
        first_run, second_run = runs.get('s1-001', {}), runs.get('s1-001-r1', {})
        merged = f_run['resume']['merged'] or []
        checks['f_stage_stopped_for_credit'] = (f_run['exit'] == chain.EXIT_STOPPED and first_run.get('status') == 'failed'
                                                and (first_run.get('metrics') or {}).get('billing_stop') == 1
                                                and 'provider_credit_balance_low' in (first_run.get('message') or ''))
        checks['f_rows_not_started_not_failed'] = (len(rows) == s1_rows and count(rows, 'failed') == 0 and len(interrupted) >= 1
                                                   and all(r['status'] == 'not_started' and r['accounting'].get('voided') for r in interrupted if r['accounting'].get('attempts'))
                                                   and (first_run.get('metrics') or {}).get('failed_episodes') == 0)
        checks['f_slow_schedule_followed'] = any(r['accounting'].get('billing_wait_seconds') == budget['billing_outage']['max_wait_seconds'] for r in interrupted)
        checks['f_resume_completes'] = (f_run['resume']['exit'] == 0 and second_run.get('status') == 'done'
                                        and (f_run['resume']['status'] or {}).get('state') == 'completed')
        checks['f_continuation_holds_exactly_the_not_started_rows'] = (
            f_run['resume']['rows'] is not None
            and sorted(r['id'] for r in f_run['resume']['rows']) == sorted(r['id'] for r in rows if r['status'] == 'not_started')
            and f_run['resume']['stub_messages'] == count(rows, 'not_started'))
        checks['f_every_row_exactly_once'] = (len(merged) == s1_rows == len({r['id'] for r in merged}) and count(merged, 'completed') == s1_rows)
        checks['f_same_ledger_and_caps'] = (f_run['resume']['ledger']['attempted_calls'] == budget['max_attempted_calls']
                                            and f_run['resume']['ledger']['voided_calls'] == sum(bool(r['accounting'].get('voided')) for r in interrupted))
        checks['f_analysis_complete_after_resume'] = ((second_run.get('metrics') or {}).get('residual_avoidance_pp') == 0
                                                      and (second_run.get('metrics') or {}).get('team_episodes_complete') == 120)
        checks['f_second_resume_refused'] = f_run['resume']['again'] == chain.EXIT_STOPPED
        checks['f_verify_ok_with_continuation'] = bool(f_run['verify'] and f_run['verify']['ok']
                                                       and set(f_run['verify']['stages']) == {'S0', 'P0', 'Q0', 'S1', 'S1-r1'})

        # (g) The model ladder: a billing stop on the first rung, then P0 -> Q0 -> S1 on the second.
        ladder = d['model_ladder']
        g_run = ladder_scenario(sr, hub_dir, tmp, stages, paid_before_s1 + 200)
        by_batch = {(r.get('params') or {}).get('batch'): r for r in g_run['runs']}
        tag = study.model_tag(ladder[1])
        second = [by_batch.get(f'{s.lower()}-{d["attempt"]}{tag}', {}) for s in stages[1:]]
        checks['g_first_rung_stopped_for_credit'] = (g_run['first_exit'] == chain.EXIT_STOPPED
                                                     and (by_batch.get('s1-001', {}).get('metrics') or {}).get('billing_stop') == 1
                                                     and g_run['first_models'] == {ladder[0]})
        checks['g_cross_model_qualification_refused'] = g_run['cross_refused'] is True
        checks['g_second_rung_completes'] = (g_run['second_exit'] == 0 and all(r.get('status') == 'done' for r in second)
                                             and all((r.get('params') or {}).get('model') == ladder[1] for r in second))
        checks['g_second_rung_own_batches_and_ledger'] = (tag == '-opus-5' and g_run['ledger2']['attempted_calls'] == budget['max_attempted_calls']
                                                          and g_run['second_messages'] == budget['max_attempted_calls']
                                                          and g_run['second_models'] == {ladder[1]})
        checks['g_rows_name_their_model'] = (len(g_run['rows']) == s1_rows and all(r.get('model') == ladder[1] for r in g_run['rows']))
        prices = d['models'][ladder[1]]
        expected = g_run['second_messages'] and g_run['ledger2']['actual_usd'] > 0 and abs(
            g_run['ledger2']['actual_usd'] - (g_run['ledger2']['input_tokens'] * prices['input_usd_per_million']
                                             + g_run['ledger2']['output_tokens'] * prices['output_usd_per_million']) / 1e6) < 1e-6
        checks['g_second_rung_priced_at_its_own_rates'] = bool(expected)

        checks['nothing_spooled'] = not list((tmp / 'spool').glob('*.json')) if (tmp / 'spool').exists() else True
        checks['committed_tree_untouched'] = not (study.ROOT / 'results').exists() or not any((study.ROOT / 'results').iterdir())

        def brief(run):
            stages_out = {}
            for s, e in ((run['status'] or {}).get('stages') or {}).items():
                stages_out[s] = {k: e.get(k) for k in ('status', 'reason', 'calls', 'input_tokens', 'output_tokens', 'cost_usd',
                                                      'planned', 'valid', 'failed', 'not_started', 'failed_units', 'elapsed_seconds') if e.get(k) is not None}
                if e.get('continuations'):
                    stages_out[s]['continuations'] = [{k: c.get(k) for k in ('batch', 'status', 'calls', 'planned', 'valid', 'elapsed_seconds')} for c in e['continuations']]
            return {'exit': run['exit'], 'seconds': round(run['seconds'], 1), 'state': (run['status'] or {}).get('state'),
                    'stopped_stage': (run['status'] or {}).get('stopped_stage'), 'reason': (run['status'] or {}).get('reason'),
                    'stages': stages_out, 'ledger_calls': run['ledger']['attempted_calls'],
                    'max_requests_in_flight': run['max_in_flight'], 'credit_errors': run['credit_errors'],
                    'stub_cost_usd_not_real': run['ledger']['actual_usd']}
        result = {'rehearsal': 'passed' if all(checks.values()) else 'FAILED', 'checks': checks,
                  'source_hash': study.source_hash(), 'model_calls_made': 0,
                  'full_chain': brief(a_run), 'verify_seconds': round(a_run['verify']['seconds'], 1) if a_run['verify'] else None,
                  'verify_stages': {s: v.get('ok') for s, v in (a_run['verify'] or {}).get('stages', {}).items()},
                  'failed_qualification_chain': brief(b_run), 'one_failed_call_chain': brief(c_run),
                  'over_the_failure_limit_chain': brief(d_run), 'billing_pause_chain': brief(e_run),
                  'model_ladder_chain': {'first_exit': g_run['first_exit'], 'second_exit': g_run['second_exit'],
                                         'second_rung': ladder[1], 'second_calls': g_run['second_messages'],
                                         'second_stub_cost_usd_not_real': g_run['ledger2']['actual_usd']},
                  'billing_stop_and_resume_chain': dict(brief(f_run), first_exit=f_run['exit'], resume_exit=f_run['resume']['exit'],
                                                        resume_seconds=round(f_run['resume']['seconds'], 1),
                                                        interrupted_rows=len(interrupted), resumed_rows=len(f_run['resume']['rows'] or []))}
    finally:
        if a.keep:
            print(f'rehearsal files kept in {tmp}', file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps(result, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
