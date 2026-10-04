"""Run Q0 then P1 in one finite process; P1 starts only if Q0's own summary reports qualification_pass."""
import argparse
import json
import time
import common


def chain(q0, p1, execute=None, register=None, log=print):
    if execute is None: from worker import execute
    if register is None: from register import register
    register(q0)
    summary = execute('Q0', q0)
    gate = summary.get('qualification_pass') is True and summary['recorded'] == summary['assigned']
    log(json.dumps(dict(event='gate', attempt=q0, qualification_pass=summary.get('qualification_pass'), recorded=summary['recorded'],
                        assigned=summary['assigned'], next=p1 if gate else None, time=time.time()), sort_keys=True))
    if not gate: return dict(q0=summary, p1=None, stopped='q0_gate_failed')
    register(p1)
    return dict(q0=summary, p1=execute('P1', p1, str(common.ROOT/'results'/q0)), stopped=None)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('q0'); a.add_argument('p1'); args = a.parse_args()
    out = chain(args.q0, args.p1)
    print(json.dumps(dict(event='chain_end', stopped=out['stopped'], p1_ran=out['p1'] is not None, time=time.time()), sort_keys=True), flush=True)
