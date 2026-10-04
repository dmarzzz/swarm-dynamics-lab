#!/usr/bin/env python3
"""Small, prospectively specified paired experiments. Standard library + parent's PyYAML.
No dynamic code in specs. Pool only: paid fallback is deliberately disabled ($0 <= $20).
"""
from __future__ import annotations
import argparse
import concurrent.futures
import csv
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
PARENT = REPO / 'researchers/dmarz/notes/sybil-split-opus'
DEADLINE = datetime.fromisoformat('2026-10-04T22:00:00+00:00').timestamp()
TOTAL_PAID_CAP_USD = 20

def require(condition, message="validation failed"):
    """Operational guard that remains active under python -O/PYTHONOPTIMIZE."""
    if not condition:
        raise AssertionError(message)

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n'); tmp.replace(path)

def append(path, data):
    with Path(path).open('a') as f:
        f.write(json.dumps(data, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno())

def load_parent():
    sys.path.insert(0, str(PARENT / 'src'))
    import study
    import sim
    import provider
    return study, sim, provider

def read_spec(name, frozen=True):
    p = ROOT / 'specs' / (name if name.endswith('.json') else name + '.json')
    s = json.loads(p.read_text())
    require(s['route'] == 'anthropic-pool', 'Paid routes disabled, no automatic fallback')
    require(s['max_paid_usd'] == 0 and s['max_calls'] == 204, 'validation failed')
    require(s['model'] == 'claude-sonnet-4-6', 'validation failed')
    require(1 <= s['concurrency'] <= 4, 'validation failed')
    if frozen:
        relative = str(p.relative_to(REPO))
        committed = subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=REPO)
        require(committed == p.read_bytes(), 'Spec must be committed before dispatch')
        for path, digest in s['source_sha256'].items():
            require(sha(REPO / path) == digest, 'Pinned source changed: ' + path)
    return s

def assignments(s):
    study, sim, provider = load_parent()
    out = []
    # Two roots (one per graph family) x six clean shapes. This is deliberately
    # smaller than the parent's 60-call Q0 and cannot inherit its qualification.
    for family, task in [('ring', 5139), ('community', 5144)]:
        for shape in study.design()['qualification']['shapes']:
            w, admitted, passed = study.fixture(family, task, shape)
            pack = study.packet(w, admitted, passed)
            present = {r['skill'] for r in pack['reports']}
            expected = {str(i): w['answers'][i] if i in present else None for i in range(6)}
            out.append(dict(id=f'Q-{family}-{task}-{shape}', stage='Q', family=family, task=task,
                            shape=shape, packet=pack, answers=w['answers'], fabricated=[None]*6,
                            expected=expected))
    mains = []
    for family in ('ring', 'community'):
        for task in s['roots'][family]:
            for k in (1, 27):
                attacker = dict(study.design()['attacker'], internal_links=s['internal_links'])
                w = study.world(family, task, k, s['attacker_pass'], attacker=attacker)
                for rec in sim.checkpoints(w, [s['checks']], ['degree', 'coverage'], study.cfg()):
                    mains.append(dict(id=f'M-{family}-{task}-{k}-{rec["arm"]}', stage='M',
                        family=family, task=task, k=k, arm=rec['arm'], packet=study.packet(w, rec['admitted'], rec['passed']),
                        answers=w['answers'], fabricated=w['fabricated'], admission=rec['admission']))
    random.Random(s['dispatch_seed']).shuffle(mains)
    out.extend(mains)
    require(len(out) == s['max_calls'] and len({a['id'] for a in out}) == len(out), 'validation failed')
    for a in out:
        a['packet_hash'] = study.digest(a['packet'])
    return out

def parse_answer(text):
    # Exact schema; no fences/answer salvage. Permit JSON-schema integer 12.0,
    # reject booleans, missing/extra fields, nonfinite values and strings.
    d = json.loads(text)
    require(isinstance(d, dict) and set(d) == {'values'}, 'validation failed')
    v = d['values']; require(isinstance(v, dict) and set(v) == {str(i) for i in range(6)}, 'validation failed')
    for k, x in v.items():
        require(x is None or (type(x) in (int, float) and float(x).is_integer()), 'validation failed')
        if x is not None: v[k] = int(x)
    return d

def pool_key():
    path = Path(os.environ.get('FACTORY_POOL_KEY_FILE', '~/.moltbot/secrets/pool-keys.json')).expanduser()
    keys = json.loads(path.read_text())['keys']
    return next(k['key'] for k in keys if k.get('enabled') and k.get('label') == 'default')

def call(s, a, key):
    study, sim, provider = load_parent()
    system = provider.SYSTEM + '\nReturn exactly {"values":{"0":integer_or_null,"1":integer_or_null,"2":integer_or_null,"3":integer_or_null,"4":integer_or_null,"5":integer_or_null}}.'
    body = dict(model=s['model'], max_tokens=500, temperature=0, system=system,
                messages=[{'role': 'user', 'content': json.dumps(a['packet'], sort_keys=True)}])
    row = {k: v for k, v in a.items() if k != 'packet'}
    row.update(started_at=now(), model=s['model'], route=s['route'], status='failed', paid_usd=0,
               request_hash=hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest())
    # No network-configurable destination: credentials only ever go to the approved local pool.
    req = urllib.request.Request('http://127.0.0.1:18811/v1/messages', data=json.dumps(body).encode(),
            headers={'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
    t0 = time.monotonic()
    try:
        if time.time() >= DEADLINE: raise RuntimeError('deadline_before_dispatch')
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read(200000))
        row.update(returned_model=data.get('model'), usage=data.get('usage'), stop_reason=data.get('stop_reason'),
                   response_id=data.get('id'))
        texts = [b['text'] for b in data.get('content', []) if b.get('type') == 'text']
        row['raw_text'] = '\n'.join(texts)
        require(data.get('model') == s['model'], 'model_mismatch')
        require(isinstance(data.get('usage'), dict), 'missing_usage')
        require(data.get('stop_reason') == 'end_turn', 'stop_reason')
        require(len(texts) == 1, 'text_blocks')
        ans = parse_answer(texts[0]); row['answer'] = ans
        row['metrics'] = sim.grade(ans['values'], a['answers'], a['fabricated'])
        if a['stage'] == 'Q': row['exact'] = ans['values'] == a['expected']
        row['status'] = 'completed'
    except urllib.error.HTTPError as e:
        # No raw provider exception/body, which could echo credentials. No answer or transport retry.
        row['error'] = 'http_' + str(e.code)
    except Exception as e:
        row['error'] = type(e).__name__ + (':' + str(e) if isinstance(e, AssertionError) else '')
    row.update(ended_at=now(), elapsed_seconds=round(time.monotonic()-t0, 3))
    return row

def bootstrap(values_by_family, draws=10000):
    rng = random.Random(20261004)
    means = []
    for _ in range(draws):
        means.append(statistics.mean(statistics.mean(rng.choices(v, k=len(v))) for v in values_by_family.values()))
    means.sort()
    return [means[int(.025*draws)], means[int(.975*draws)]]

def analyze(s, aa, rows, out):
    byid = {r['id']: r for r in rows}
    require(len(byid) == len(rows), 'duplicate terminal outcome')
    q = [byid.get(a['id']) for a in aa if a['stage'] == 'Q']
    gate = len(q) == 12 and all(r and r['status'] == 'completed' and r.get('exact') for r in q)
    main = [a for a in aa if a['stage'] == 'M']
    valid = [byid[a['id']] for a in main if a['id'] in byid and byid[a['id']]['status'] == 'completed']
    allby = {(r['family'], r['task'], r['arm'], r['k']): r for r in valid}
    complete = {'ring': [], 'community': []}; bounds = {'ring': [], 'community': []}
    for family in complete:
        for task in s['roots'][family]:
            lo = hi = 0.; full = True
            for arm, k, sign in [('degree',27,1), ('degree',1,-1), ('coverage',27,-1), ('coverage',1,1)]:
                r = allby.get((family, task, arm, k))
                if r:
                    x = r['metrics']['rare_wrong']; lo += sign*x; hi += sign*x
                else:
                    full = False; lo += min(0,sign); hi += max(0,sign)
            bounds[family].append((lo,hi))
            if full: complete[family].append(lo)
    enough = all(complete.values())
    estimate = statistics.mean(statistics.mean(v) for v in complete.values()) if enough else None
    ci = bootstrap(complete, s['bootstrap_draws']) if enough else None
    ncomplete = sum(map(len, complete.values()))
    finished = len(rows) == len(aa) and len(valid) == len(main) and gate
    # Five exploratory tests, no multiple-comparison correction. 'finding' is a narrow
    # within-spec descriptive label, NOT a formal hypothesis acceptance.
    direction = s['expected_direction']
    finding = finished and ci and ((direction == 'positive' and ci[0] > .1) or (direction == 'negative' and ci[1] < -.1))
    status = 'finding' if finding else ('negative' if finished else 'lead')
    summary = dict(spec=s['id'], status=status, exploratory=True, qualification_passed=gate,
        planned=len(aa), attempted=len(rows), valid=sum(r['status']=='completed' for r in rows),
        failed=sum(r['status']!='completed' for r in rows), unstarted=len(aa)-len(rows),
        main_planned=len(main), main_valid=len(valid), paired_roots=ncomplete, roots_planned=48,
        primary=estimate, ci95=ci, all_assigned_bounds=[statistics.mean(statistics.mean(x[j] for x in v) for v in bounds.values()) for j in (0,1)],
        family_means={f: statistics.mean(v) if v else None for f,v in complete.items()}, paid_usd=0,
        input_tokens=sum((r.get('usage') or {}).get('input_tokens',0) for r in rows),
        output_tokens=sum((r.get('usage') or {}).get('output_tokens',0) for r in rows), generated_at=now())
    dump(out/'summary.json', summary)
    with (out/'cells.csv').open('w') as f:
        w = csv.writer(f); w.writerow(['family','arm','k','assigned','valid','rare_wrong','rare_accuracy','rare_abstain'])
        for family in ('ring','community'):
            for arm in ('degree','coverage'):
                for k in (1,27):
                    v = [r for r in valid if r['family']==family and r['arm']==arm and r['k']==k]
                    w.writerow([family,arm,k,24,len(v)]+[statistics.mean(r['metrics'][m] for r in v) if v else '' for m in ('rare_wrong','rare_accuracy','rare_abstain')])
    primary = 'unavailable' if estimate is None else f'{estimate*100:+.1f} pp (descriptive 95% root-bootstrap CI {ci[0]*100:+.1f} to {ci[1]*100:+.1f})'
    (out/'FINDING.md').write_text(f'''# {s['title']}

Status: **{status}**, exploratory, not independently reviewed. No accepted hypothesis or multiplicity-adjusted inference.

## Question

{s['question']}

## Method and results

Frozen one-file [spec](../../specs/{s['id']}.json), parent simulator and prompt from [Dmarz's split study](../../../../dmarz/notes/sybil-split-opus/README.md). Model: `{s['model']}`, temperature 0, local Anthropic pool, no paid fallback. Internal links: `{s['internal_links']}`; attacker pass probability {s['attacker_pass']}; {s['checks']} checks.

Primary: (k=27 minus k=1 rare-skill wrong fraction under degree) minus the same under coverage. **{primary}**. Complete paired roots: {ncomplete}/48, equally weighted graph-family means. All-assigned worst-case bounds: {summary['all_assigned_bounds']}. Bounds cover missing calls, not sampling uncertainty.

Calls: {len(rows)}/{len(aa)} attempted; {summary['valid']} valid; {summary['failed']} failed; {summary['unstarted']} unstarted. Main: {len(valid)}/192 valid. Qualification: {sum(bool(r and r.get('exact')) for r in q)}/12 exact, gate {'passed' if gate else 'not passed'}. No retries or outcome replacements. External paid spend $0; pool usage {summary['input_tokens']} input / {summary['output_tokens']} output tokens (not a claim of zero compute cost).

[Cell table](cells.csv), [summary](summary.json), [all outcomes](records.jsonl), [execution provenance](provenance.json).

## Interpretation and limits

{s['interpretation']}

The 48 synthetic roots are reused from the parent, not new independent evidence about real swarms. Four calls within a root are paired; skills and identities are not sample units. The five queue specs share roots and are not five independent replications. The 12 clean fixtures are a reduced capability screen, not the parent's 60-fixture qualification. This changes the model and request configuration together: Sonnet uses temperature 0 and an explicit JSON instruction instead of Opus effort-low schema-constrained output. All comparisons remain exploratory. A negative label means the prespecified directional/useful-size criterion was not met, not equivalence or absence of an effect. No published Sybil defense or in-the-wild claim is tested.
''')
    return summary

def run(s):
    out = ROOT/'results'/s['id']; out.mkdir(parents=True, exist_ok=True)
    with (out/'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
        aa = assignments(s)
        provenance = dict(spec_sha256=sha(ROOT/'specs'/f"{s['id']}.json"), source_sha256=s['source_sha256'],
                          commit=subprocess.check_output(['git','rev-parse','HEAD'], cwd=REPO,text=True).strip(),
                          python=sys.version, host=os.uname().nodename, created_at=now(), command='python3 researchers/shadow/factory/factory.py queue',
                          assignment_digest=hashlib.sha256(json.dumps(aa,sort_keys=True).encode()).hexdigest())
        if (out/'provenance.json').exists():
            old = json.loads((out/'provenance.json').read_text())
            for k in ('spec_sha256','source_sha256','assignment_digest'): require(old[k] == provenance[k], 'resume pin mismatch')
        else: dump(out/'provenance.json', provenance)
        record = out/'records.jsonl'; journal = out/'dispatch.jsonl'
        rows = [json.loads(l) for l in record.read_text().splitlines()] if record.exists() else []
        dispatches = [json.loads(l) for l in journal.read_text().splitlines()] if journal.exists() else []
        finished = {r['id'] for r in rows}; dispatched = {r['id'] for r in dispatches}
        # An interrupted in-flight call is unknown, never repeated. This makes resumes
        # at-most-once and includes uncertain calls in denominators.
        for d in dispatches:
            if d['id'] not in finished:
                a = next(a for a in aa if a['id']==d['id'])
                r = {k:v for k,v in a.items() if k!='packet'}
                r.update(status='failed', error='interrupted_unknown', paid_usd=0)
                append(record,r); rows.append(r)
        key = None
        for stage in ('Q','M'):
            if stage == 'M' and not analyze(s, aa, rows, out)['qualification_passed']: break
            pending = [a for a in aa if a['stage']==stage and a['id'] not in dispatched]
            # Bounded batches: no executor backlog can run beyond cutoff or after a failure stop.
            for i in range(0,len(pending),s['concurrency']):
                if time.time() >= DEADLINE: break
                if sum(r['status']=='failed' for r in rows) >= s['failure_stop']: break
                if key is None: key = pool_key()
                batch = pending[i:i+s['concurrency']]
                for a in batch:
                    require(len(dispatched)<s['max_calls'], 'call_cap')
                    append(journal,dict(id=a['id'], time=now(), reserved_paid_usd=0)); dispatched.add(a['id'])
                with concurrent.futures.ThreadPoolExecutor(max_workers=s['concurrency']) as pool:
                    futures = [pool.submit(call,s,a,key) for a in batch]
                    for f in concurrent.futures.as_completed(futures):
                        r=f.result(); append(record,r); rows.append(r)
                summary=analyze(s,aa,rows,out)
                print(json.dumps({k:summary[k] for k in ('spec','status','attempted','failed','main_valid')}), flush=True)
        summary=analyze(s,aa,rows,out)
        dump(out/'terminal.json',dict(time=now(), qualification_passed=summary['qualification_passed'], status=summary['status']))
        return summary

def main():
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['queue','run','analyze','manifest']); p.add_argument('--spec'); p.add_argument('--watch',action='store_true'); args=p.parse_args()
    if args.command=='queue':
        while True:
            for name in json.loads((ROOT/'queue.json').read_text())['specs']:
                if time.time()>=DEADLINE: return
                if not (ROOT/'results'/name/'terminal.json').exists(): run(read_spec(name))
            if not args.watch: return
            time.sleep(min(60,max(0,DEADLINE-time.time())))
            if time.time()>=DEADLINE: return
    else:
        s=read_spec(args.spec)
        if args.command=='run': run(s)
        elif args.command=='manifest':
            aa=assignments(s); print(json.dumps({'assigned':len(aa),'packet_digest':hashlib.sha256(json.dumps(aa,sort_keys=True).encode()).hexdigest()}))
        else:
            out=ROOT/'results'/s['id']; rows=[json.loads(l) for l in (out/'records.jsonl').read_text().splitlines()]
            print(json.dumps(analyze(s,assignments(s),rows,out),indent=2))
if __name__=='__main__': main()
