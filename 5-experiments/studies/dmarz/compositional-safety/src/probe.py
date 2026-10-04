"""One explicitly registered diagnostic call; never a qualification retry."""
import argparse
import json
import time
import common
from provider import Anthropic, CallFailure, Ledger


def execute(attempt):
    if common.design().get('diagnostics',{}).get(attempt,{}).get('mode')=='closed-loop':
        from worker import execute as closed_loop
        return closed_loop('I0',attempt)
    if common.design().get('diagnostics',{}).get(attempt,{}).get('mode')=='interface':
        from diagnose import execute as diagnose
        return diagnose(attempt)
    import swarm_report as sr
    commit = common.frozen(attempt)
    out = common.ROOT/'results'/attempt
    out.mkdir(parents=True, exist_ok=False)
    lineage = common.design().get('diagnostics',{}).get(attempt,{'parent_attempt':'q0-003','source_attempt':'q0-003'})
    parent = common.ROOT/'results'/lineage['source_attempt']
    rows = [json.loads(l) for l in (parent/'episodes.jsonl').read_text().splitlines()]
    failed = next(r for r in rows if r['validity']['reason']=='nonterminal_output')
    packet = failed['trace'][-1]['observation']
    manifest = dict(attempt=attempt, stage='I0', **lineage,
                    source_episode=failed['episode_id'], commit=commit,
                    hashes=common.hashes(), created=time.time(), assigned=1)
    common.dump(out/'manifest.json', manifest)
    common.dump(out/'packet.json', packet)
    ledger = Ledger(common.ROOT/'accounting/study.jsonl')
    before = ledger.transact()
    with sr.start(common.EXP, params=dict(stage='I0', kind='diagnostic', attempt=attempt),
                  run=f'{common.EXP}/{attempt}-diagnostic') as run:
        try:
            answer, usage = Anthropic(ledger).call(packet, f'{attempt}/termination-probe')
            result = dict(valid=True, answer=answer, usage=usage)
        except CallFailure as e:
            result = dict(valid=False, reason=e.category, usage=e.accounting)
        after = ledger.transact()
        result['accounting'] = {k:after[k]-before[k] for k in after}
        result['qualification_pass'] = False
        common.dump(out/'summary.json', result)
        for name in ('manifest.json', 'packet.json', 'summary.json'): run.artifact(out/name, name)
        run.done(model_calls=result['accounting']['attempted_calls'],
                 api_cost_usd=result['accounting']['actual_usd'],
                 message='One-call provider termination diagnostic; not qualification evidence.')
    print(json.dumps(result), flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('attempt'); execute(p.parse_args().attempt)
