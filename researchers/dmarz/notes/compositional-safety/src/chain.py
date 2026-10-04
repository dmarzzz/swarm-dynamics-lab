"""Run Q0 then P1 in one finite process; P1 starts only if Q0's own summary reports qualification_pass."""
import argparse
import json
import time
import common

STATE = 'https://swarm-live.pages.dev/api/state'


def wait_public(receipt, getter=None, timeout=120, pause=5, clock=time.monotonic, sleep=time.sleep):
    """Block until the public site shows this registration (its read path is cached); admission checks the same record."""
    if getter is None:
        from admission import fetch as getter
    deadline = clock() + timeout
    while True:
        try:
            state = json.loads(getter(STATE))
            exp = next((e for e in state['experiments'] if e['id'] == common.EXP), {})
            if exp.get('url') == receipt['url'] and exp.get('description') == receipt['registered_tldr']: return True
        except Exception:
            pass
        if clock() >= deadline: raise ValueError('public_registration_not_visible')
        sleep(pause)


def chain(q0, p1, execute=None, register=None, wait=None, log=print):
    if execute is None: from worker import execute
    if register is None: from register import register
    if wait is None: wait = wait_public
    wait(register(q0))
    summary = execute('Q0', q0)
    gate = summary.get('qualification_pass') is True and summary['recorded'] == summary['assigned']
    log(json.dumps(dict(event='gate', attempt=q0, qualification_pass=summary.get('qualification_pass'), recorded=summary['recorded'],
                        assigned=summary['assigned'], next=p1 if gate else None, time=time.time()), sort_keys=True))
    if not gate: return dict(q0=summary, p1=None, stopped='q0_gate_failed')
    wait(register(p1))
    return dict(q0=summary, p1=execute('P1', p1, str(common.ROOT/'results'/q0)), stopped=None)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('q0'); a.add_argument('p1'); args = a.parse_args()
    out = chain(args.q0, args.p1)
    print(json.dumps(dict(event='chain_end', stopped=out['stopped'], p1_ran=out['p1'] is not None, time=time.time()), sort_keys=True), flush=True)
