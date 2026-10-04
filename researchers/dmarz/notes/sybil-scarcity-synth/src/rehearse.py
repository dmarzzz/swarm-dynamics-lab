"""Offline rehearsal of the chain against throwaway hubs on 127.0.0.1 and a local model stub.

    python3 src/rehearse.py --hub-dir <dir with hub.py and swarm_report.py>

Four scenarios, each on its own throwaway hub with fresh temporary result and ledger directories,
run side by side as separate processes:
  a  S0, P0, Q0, S1 to completion on the default model with a stub that answers as a perfect
     follower of each prompt; then `chain verify`; a replay of a finished batch is refused.
  b  a stub that invents a value for a missing fact: Q0 fails, the chain stops with exit 3 and no
     S1 run exists on the hub.
  c  a billing outage that does not clear stops S1 of the default model
     (`provider_credit_balance_low`); then, on the same hub and source hash, P0, Q0 and S1 run on
     the second model of the ladder with its own batches, ledger and results directory; verify.
  d  S1 with one failed call (HTTP 500), a billing pause that clears, and a billing outage that
     does not; then `chain resume` completes the stage; verify; every unit is counted once.

It refuses any hub that is not on 127.0.0.1 and blocks every other network destination for the
process. A rehearsal answer is never a sample and never leaves the machine. No model call is made.
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

import chain
import coordinator
import provider
import study
import worker

LOCAL = '127.0.0.1'
SCENARIOS = ('a', 'b', 'c', 'd')
CREDIT_BODY = {'type': 'error', 'request_id': 'req_stub_credit',
               'error': {'type': 'invalid_request_error',
                         'message': 'Your credit balance is too low to access the Anthropic API. '
                                    'Please go to Plans & Billing to upgrade or purchase credits.'}}


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def http_error(url, code, body, request_id='req_stub'):
    return urllib.error.HTTPError(url, code, 'error', {'request-id': request_id}, io.BytesIO(json.dumps(body).encode()))


class Stub:
    """Stands in for the model endpoint. Answers count_tokens and messages requests in the real
    response shape: a thinking block before one text block, model id, stop reason and usage.

    mode 'reference': a perfect follower of the request's system prompt (row plurality for prompt
                      `base`, the scripted rule follower for prompt `rule`).
    mode 'invent':    the same, but never abstains: a missing fact gets an invented value.
    Faults are keyed by the ordinal of the messages request (1 = the probe, 2..49 = Q0, 50.. = S1):
    `fail_at` ordinals answer HTTP 500; `credit_at` starts a billing outage of `credit_times`
    requests that then clears; from `credit_from` on every request gets the credit-balance error.
    """
    def __init__(self, mode='reference', output_tokens=None, fail_at=(), credit_at=None, credit_times=0, credit_from=None):
        self.mode = mode
        self.output_tokens = output_tokens or {'low': 40, 'high': 1500}
        self.fail_at, self.credit_at, self.credit_left, self.credit_from = set(fail_at), credit_at, credit_times, credit_from
        self.lock = threading.Lock()
        self.count_calls = self.message_requests = self.answers = self.credit_errors = 0

    def __call__(self, request, timeout=None):
        url = request.full_url
        if url not in (provider.COUNT_URL, provider.MESSAGES_URL):
            raise AssertionError('stub_unexpected_url')
        headers = {k.lower(): v for k, v in request.header_items()}
        if not headers.get('x-api-key') or headers.get('anthropic-version') != '2023-06-01':
            raise AssertionError('stub_missing_headers')
        body = json.loads(request.data)
        tokens = len(request.data) // 2            # about the measured 2 characters per Opus token
        if url == provider.COUNT_URL:
            if tuple(body) != tuple(k for k in provider.REQUEST_KEYS if k != 'max_tokens'):
                raise AssertionError('stub_count_body_keys')
            with self.lock:
                self.count_calls += 1
            return _Response(json.dumps({'input_tokens': tokens}).encode())
        if (tuple(body) != provider.REQUEST_KEYS or set(body['output_config']) != {'effort', 'format'}
                or body['model'] not in study.design()['model_ladder'] or body['system'] not in provider.PROMPTS.values()):
            raise AssertionError('stub_message_body')
        with self.lock:
            self.message_requests += 1
            n = self.message_requests
            credit = self.credit_from is not None and n >= self.credit_from
            if not credit and self.credit_at is not None and n >= self.credit_at and self.credit_left > 0:
                self.credit_left -= 1
                credit = True
            if credit:
                self.credit_errors += 1
        if credit:
            raise http_error(url, 400, CREDIT_BODY, 'req_stub_credit')
        if n in self.fail_at:
            raise http_error(url, 500, {'type': 'error', 'error': {'type': 'api_error', 'message': 'stub internal error'}})
        packet = json.loads(body['messages'][0]['content'])
        prompt = 'rule' if body['system'] == provider.PROMPTS['rule'] else 'base'
        values = study.reference_answer(packet, prompt)['values']
        if self.mode == 'invent':
            values = {k: 55 if v is None else v for k, v in values.items()}
        with self.lock:
            self.answers += 1
        return _Response(json.dumps({
            'id': f'msg_stub_{n:06d}', 'type': 'message', 'role': 'assistant', 'model': body['model'],
            'content': [{'type': 'thinking', 'thinking': '', 'signature': 'stub'},
                        {'type': 'text', 'text': json.dumps({'values': values})}],
            'stop_reason': 'end_turn', 'stop_sequence': None,
            'usage': {'input_tokens': tokens, 'output_tokens': self.output_tokens[body['output_config']['effort']],
                      'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}}).encode())


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


def hub_runs(sr):
    return {(r.get('params') or {}).get('batch'): r for r in sr.runs(study.EXPERIMENT, limit=5000)}


def no_wait(seconds):
    """The billing schedule's waits take no time in a rehearsal."""


def run(sr, stages, base, name, stub, resume=False):
    started = time.monotonic()
    code = chain.run_chain(stages, sr, base / name / 'results', base / name / 'ledger' / 'ledger.jsonl',
                           opener=stub, sleep=no_wait, resume=resume)
    return {'exit': code, 'seconds': round(time.monotonic() - started, 1),
            'status': chain.read_status(base / name / 'results'),
            'ledger': provider.Ledger(base / name / 'ledger' / 'ledger.jsonl').transact()
            if (base / name / 'ledger' / 'ledger.jsonl').exists() else None}


def brief(result):
    status = result['status'] or {}
    stages = {}
    for s, e in (status.get('stages') or {}).items():
        stages[s] = {k: e.get(k) for k in ('batch', 'status', 'stage_status', 'reason', 'calls', 'cost_usd', 'planned',
                                           'valid', 'failed', 'not_started', 'elapsed_seconds') if e.get(k) is not None}
        if e.get('continuations'):
            stages[s]['continuations'] = [{k: c.get(k) for k in ('batch', 'status', 'calls', 'part_units', 'valid', 'failed',
                                                                 'not_started', 'elapsed_seconds')} for c in e['continuations']]
    return {'exit': result['exit'], 'seconds': result['seconds'], 'model': status.get('model'), 'state': status.get('state'),
            'stopped_stage': status.get('stopped_stage'), 'reason': status.get('reason'), 'stages': stages,
            'ledger_calls': (result['ledger'] or {}).get('attempted_calls'),
            'stub_cost_usd_not_real': (result['ledger'] or {}).get('actual_usd')}


def scenario(sr, name, base):
    """One scenario on the hub that is already running. Returns (checks, details)."""
    d = study.design()
    budget = d['budget']
    stages = list(study.STAGES)
    required = set(worker.REQUIRED_METRICS)
    stop = budget['billing_outage']['stop_category']
    checks, details = {}, {}
    if name == 'a':
        stub = Stub()
        r = run(sr, stages, base, 'default', stub)
        runs = hub_runs(sr)
        batches = [study.base_batch(s) for s in stages]
        checks['a_exit_zero'] = r['exit'] == 0
        checks['a_state_completed'] = (r['status'] or {}).get('state') == 'completed'
        checks['a_all_stages_done'] = all(runs.get(b, {}).get('status') == 'done' for b in batches)
        checks['a_metrics_reported'] = all(required <= set(runs.get(b, {}).get('metrics') or {}) for b in batches)
        checks['a_calls_per_stage'] = {s: (runs.get(b, {}).get('metrics') or {}).get('model_calls')
                                       for s, b in zip(stages, batches)} == budget['max_calls']
        checks['a_gates_passed'] = all((runs.get(b, {}).get('metrics') or {}).get('qualification_passed') == 1 for b in batches[:3])
        checks['a_ledger_total_calls'] = r['ledger']['attempted_calls'] == budget['max_attempted_calls'] == stub.answers
        started = time.monotonic()
        report = chain.verify(sr, base / 'default' / 'results')
        details['verify_seconds'] = round(time.monotonic() - started, 1)
        details['verify_stages'] = {s: v.get('ok') for s, v in report.get('stages', {}).items()}
        checks['a_verify_ok'] = bool(report['ok']) and set(report['stages']) == set(stages)
        try:
            coordinator.enqueue(sr, 'S0')
            checks['a_replay_refused'] = False
        except ValueError as exc:
            checks['a_replay_refused'] = str(exc) == 'batch_exists_no_replay'
        details['full_chain'] = brief(r)
        details['s1_primary'] = (report.get('stages', {}).get('S1') or {}).get('primary')
    elif name == 'b':
        stub = Stub('invent')
        r = run(sr, stages, base, 'default', stub)
        runs, status = hub_runs(sr), r['status'] or {}
        q0 = runs.get(study.base_batch('Q0'), {})
        checks['b_exit_three'] = r['exit'] == chain.EXIT_STOPPED
        checks['b_state_stopped_at_gate'] = status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'Q0'
        checks['b_no_s1_run_on_hub'] = study.base_batch('S1') not in runs and 'S1' not in (status.get('stages') or {})
        checks['b_q0_failed_with_metrics'] = (q0.get('status') == 'failed' and required <= set(q0.get('metrics') or {})
                                              and (q0.get('metrics') or {}).get('qualification_passed') == 0)
        checks['b_s0_p0_done'] = all(runs.get(study.base_batch(s), {}).get('status') == 'done' for s in ('S0', 'P0'))
        checks['b_calls_stopped_at_49'] = r['ledger']['attempted_calls'] == 49 == stub.answers
        details['failed_qualification_chain'] = brief(r)
    elif name == 'c':
        first, second = d['model_ladder']
        r = run(sr, stages, base, 'default', Stub(credit_from=80))
        runs, status = hub_runs(sr), r['status'] or {}
        s1 = runs.get(study.base_batch('S1'), {})
        checks['c_first_model_stopped_on_billing'] = (r['exit'] == chain.EXIT_STOPPED and status.get('reason') == stop
                                                      and status.get('stopped_stage') == 'S1' and status.get('model') == first)
        checks['c_billing_stop_reported'] = (s1.get('status') == 'failed' and (s1.get('metrics') or {}).get('billing_stop') == 1
                                             and (s1.get('metrics') or {}).get('failed') == 0
                                             and (s1.get('metrics') or {}).get('billing_pauses', 0) >= 1
                                             and required <= set(s1.get('metrics') or {}))
        details['first_model_billing_stop'] = brief(r)
        # Relaunch on the second model: own batches, ledger and results directory; S0 is not rerun.
        os.environ['STUDY_MODEL'] = second
        stub = Stub()
        r2 = run(sr, stages[1:], base, 'second-model', stub)
        runs = hub_runs(sr)
        batches = {s: study.base_batch(s) for s in stages[1:]}
        prices = d['models'][second]
        checks['c_second_model_done'] = r2['exit'] == 0 and (r2['status'] or {}).get('model') == second
        checks['c_second_model_batches'] = (list(batches.values()) == [f'{s.lower()}-{d["attempt"]}-{second[len("claude-"):]}' for s in stages[1:]]
                                            and all(runs.get(b, {}).get('status') == 'done' for b in batches.values())
                                            and all((runs[b].get('params') or {}).get('model') == second for b in batches.values()))
        checks['c_second_model_calls'] = {s: (runs[b].get('metrics') or {}).get('model_calls') for s, b in batches.items()} == \
            {s: budget['max_calls'][s] for s in stages[1:]}
        checks['c_one_s0_serves_both_models'] = sum((x.get('params') or {}).get('stage') == 'S0' for x in runs.values()) == 1
        ledger = r2['ledger']
        checks['c_second_model_own_ledger_and_prices'] = (
            ledger['models'] == [second] and ledger['attempted_calls'] == budget['max_attempted_calls']
            and abs(ledger['actual_usd'] - (ledger['input_tokens'] * prices['input_usd_per_million']
                                            + ledger['output_tokens'] * prices['output_usd_per_million']) / 1e6) < 1e-6)
        report = chain.verify(sr, base / 'second-model' / 'results')
        checks['c_second_model_verify_ok'] = bool(report['ok']) and report.get('model') == second and set(report['stages']) == set(stages[1:])
        os.environ['STUDY_MODEL'] = first
        report_first = chain.verify(sr, base / 'default' / 'results')
        checks['c_first_model_records_verify'] = bool(report_first['ok']) and report_first.get('model') == first
        os.environ.pop('STUDY_MODEL')
        details['second_model_chain'] = brief(r2)
    elif name == 'd':
        r = run(sr, stages, base, 'default', Stub(fail_at={55}, credit_at=60, credit_times=2, credit_from=100))
        runs, status = hub_runs(sr), r['status'] or {}
        s1 = runs.get(study.base_batch('S1'), {})
        metrics = s1.get('metrics') or {}
        checks['d_stopped_on_billing'] = (r['exit'] == chain.EXIT_STOPPED and status.get('reason') == stop
                                          and s1.get('status') == 'failed' and metrics.get('billing_stop') == 1)
        checks['d_one_failed_call_recorded'] = metrics.get('failed') == 1 and metrics.get('not_started', 0) > 0
        details['billing_stop'] = brief(r)
        first_ledger = r['ledger']
        stub = Stub()
        r2 = run(sr, [], base, 'default', stub, resume=True)
        runs, status = hub_runs(sr), r2['status'] or {}
        cont = runs.get(study.params('S1', 1)['batch'], {})
        cm = cont.get('metrics') or {}
        checks['d_resume_completed'] = r2['exit'] == 0 and status.get('state') == 'completed' and cont.get('status') == 'done'
        checks['d_continuation_holds_only_unstarted_units'] = (
            cm.get('model_calls') == metrics.get('not_started') == stub.answers
            and cm.get('episodes') == budget['max_calls']['S1'] and cm.get('invalid') == 1 and cm.get('failed') == 1
            and cm.get('not_started') == 0)
        checks['d_same_ledger_and_caps'] = (r2['ledger']['calls_by_stage'].get('S1') == budget['max_calls']['S1']
                                            and r2['ledger']['released_calls'] == first_ledger['released_calls'] >= 1)
        report = chain.verify(sr, base / 'default' / 'results')
        s1_report = report.get('stages', {}).get('S1') or {}
        checks['d_verify_ok_units_once'] = (bool(report['ok']) and s1_report.get('parts') == 2
                                            and (s1_report.get('checks') or {}).get('no_unit_counted_twice') is True
                                            and s1_report.get('stage_valid') == budget['max_calls']['S1'] - 1)
        analysis = json.loads((Path(status['stages']['S1']['continuations'][0]['results_dir']) / 'analysis.json').read_text())
        checks['d_analysis_keeps_failed_unit_with_bounds'] = (
            sum(c['assigned'] for c in analysis['cells']) == budget['max_calls']['S1']
            and sum(c['missing'] for c in analysis['cells']) == 1 == analysis['missing']['failed']
            and all(c['rare_fabricated']['all_assigned_bounds'][1] - c['rare_fabricated']['all_assigned_bounds'][0] > 0
                    for c in analysis['cells'] if c['missing']))
        refused = run(sr, [], base, 'default', Stub(), resume=True)
        checks['d_second_resume_refused'] = refused['exit'] == chain.EXIT_STOPPED and len(hub_runs(sr)) == len(runs)
        details['resumed_chain'] = brief(r2)
    return checks, details


def run_scenario(hub_dir, name, tmp):
    """One scenario in this process, on its own throwaway hub."""
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:1', SWARM_HUB_TOKEN='unset-until-hub-starts',
                      SWARM_SOURCE='rehearsal/local', SWARM_SPOOL=str(tmp / 'spool'), SWARM_NO_AUTO_REFRESH='1',
                      SWARM_MODEL_API_KEY='rehearsal-stub-not-a-key', SWARM_MODEL_WORKSPACE_ID='rehearsal-stub')
    for key in (provider.LEDGER_ENV, 'STUDY_RESULTS_DIR', 'STUDY_MODEL'):
        os.environ.pop(key, None)
    block_network()
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    require_local(sr)
    (tmp / name).mkdir(parents=True)
    with (tmp / name / 'hub.log').open('w') as log:
        proc = start_hub(hub_dir, tmp / name / 'hubdata', log)
        try:
            require_local(sr)
            wait_for_hub(sr, proc)
            started = time.monotonic()
            checks, details = scenario(sr, name, tmp / name)
            details['seconds'] = round(time.monotonic() - started, 1)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
    checks[name + '_nothing_spooled'] = not list((tmp / 'spool').glob('*.json')) if (tmp / 'spool').exists() else True
    return checks, details


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True, help='directory with hub.py and swarm_report.py (not part of this repo)')
    ap.add_argument('--scenario', choices=SCENARIOS, help='run one scenario in this process (used internally)')
    ap.add_argument('--tmp', help=argparse.SUPPRESS)
    ap.add_argument('--keep', action='store_true', help='keep the temporary directory and print its path')
    a = ap.parse_args(argv)
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('rehearse: --hub-dir needs hub.py and swarm_report.py')
    if a.scenario:
        checks, details = run_scenario(hub_dir, a.scenario, Path(a.tmp))
        print(json.dumps({'checks': checks, 'details': details}, sort_keys=True))
        return 0 if all(checks.values()) else 1
    tmp = Path(tempfile.mkdtemp(prefix='scarcity-synth-rehearsal-'))
    if study.ROOT in tmp.resolve().parents:
        raise SystemExit('rehearse: temporary directory is inside the study tree')
    started = time.monotonic()
    env = {k: v for k, v in os.environ.items() if k not in ('SWARM_MODEL_API_KEY', 'SWARM_MODEL_WORKSPACE_ID', 'STUDY_MODEL')}
    procs = {name: subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--hub-dir', str(hub_dir),
                                     '--scenario', name, '--tmp', str(tmp)], env=env, stdout=subprocess.PIPE,
                                    stderr=(tmp / f'{name}.stderr').open('w'), text=True) for name in SCENARIOS}
    checks, details, logs_clean = {}, {}, {}
    try:
        for name, proc in procs.items():
            out, _ = proc.communicate()
            lines = [line for line in out.splitlines() if line.startswith('{')]
            if proc.returncode not in (0, 1) or not lines:
                checks[name + '_scenario_ran'] = False
                continue
            result = json.loads(lines[-1])
            checks.update(result['checks'])
            details[name] = result['details']
            # A run's log must not end in a traceback (the earlier run's pool workers printed one).
            logs_clean[name] = 'Traceback' not in (tmp / f'{name}.stderr').read_text()
        checks['no_traceback_in_any_scenario_log'] = bool(logs_clean) and all(logs_clean.values())
        checks['committed_tree_untouched'] = not (study.ROOT / 'results').exists() or not any((study.ROOT / 'results').iterdir())
        result = {'rehearsal': 'passed' if checks and all(checks.values()) else 'FAILED', 'checks': checks,
                  'source_hash': study.source_hash(), 'model_calls_made': 0, 'scenarios': details,
                  'wall_seconds': round(time.monotonic() - started, 1)}
    finally:
        if a.keep:
            print(f'rehearsal files kept in {tmp}', file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['rehearsal'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
