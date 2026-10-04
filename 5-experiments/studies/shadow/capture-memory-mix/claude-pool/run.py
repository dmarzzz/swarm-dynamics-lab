#!/usr/bin/env python3
"""Memory-mix rescue on Claude (pool). prepare = offline; run = calls.
Reuses freeze-claude roots (tasks 160-163, seed 1, N=12, 6 committed removed) and its prompt verbatim."""
from __future__ import annotations
import concurrent.futures as cf, copy, json, math, os, random, sys, threading, time
import urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FC = ROOT.parent.parent / 'capture-memory' / 'freeze-claude'
sys.path.insert(0, str(ROOT.parent / 'src'))
import sim  # noqa: E402  (round_draws only)

SYSTEM = ('You are one agent in a group agreeing on a name. Choose a name to coordinate with a randomly '
          'encountered group member. There is no objectively correct name. You will see only the names '
          'your previous partners used. Reply with exactly one of the two allowed names and nothing else.')
MODEL = 'claude-sonnet-5-5'
CONDS = ['full', 'mix']          # all-full vs 1/3 (2 of 6 honest survivors) memory1
CAP = 1000
CONC = 4
DEADLINE = datetime(2026, 10, 4, 23, 30, tzinfo=timezone.utc).timestamp()


def now(): return datetime.now(timezone.utc).isoformat()
def save(p, x): (ROOT / p).write_text(json.dumps(x, indent=1, sort_keys=True) + '\n')


def user_prompt(words, history):
    allowed = sorted(words.values())
    return (f'Allowed names: {allowed[0]}, {allowed[1]}.\n'
            f'Partner names, oldest first: {", ".join(words[str(x)] for x in history) or "(none)"}.\n'
            'Which name do you use now?')


def short_ids(root):
    hon = sorted((i for i, a in root['agents'].items() if not a['committed']), key=int)
    return sorted(random.Random(f"mix:{root['task_id']}").sample(hon, len(hon) // 3), key=int)


def start_agents(root, cond):
    ag = {i: copy.deepcopy(a) for i, a in root['agents'].items() if not a['committed']}
    s = short_ids(root) if cond == 'mix' else []
    for i, a in ag.items():
        a['short'] = i in s
        if a['short']:
            a['mem'] = a['mem'][-1:]
    return ag


def heard_at(agents, pairs):
    h = {}
    for a, b in pairs:
        a, b = str(a), str(b)
        if a in agents and b in agents:
            h[a] = agents[b]['word']
            h[b] = agents[a]['word']
    return h


def frac(agents): return sum(a['word'] == 1 for a in agents.values()) / len(agents)


def push_mem(a, w):
    a['mem'].append(w)
    if a['short']:
        a['mem'] = a['mem'][-1:]


def p_orig(mem, beta=2.5, h=0.1):
    m = sum(mem) / len(mem)
    return (math.tanh(beta * (m + h)) + 1) / 2


def scripted(root, cond, rng=None):
    ag = start_agents(root, cond)
    tr = [frac(ag)]
    for r, pairs in enumerate(root['schedules']):
        heard = heard_at(ag, pairs)
        draws = sim.round_draws(root['task_id'], 1, root['removal_round'] + r, 12)[1]
        for i, w in heard.items():
            push_mem(ag[i], w)
        for i in heard:
            u = rng.random() if rng else draws[int(i)]
            ag[i]['word'] = 1 if u < p_orig(ag[i]['mem']) else -1
        tr.append(frac(ag))
    return tr


def boot(diffs, B=10000, seed=7):
    r = random.Random(seed)
    n = len(diffs)
    bs = sorted(sum(r.choice(diffs) for _ in range(n)) / n for _ in range(B))
    return [bs[int(.025 * B)], bs[int(.975 * B) - 1]]


def roots():
    return json.loads((FC / 'inputs.json').read_text())['roots']


QHIST = [[1] * 8, [-1] * 8, [1] * 7 + [-1], [-1] * 7 + [1], [1, 1, 1, -1, 1, 1, 1, -1], [-1, -1, -1, 1, -1, -1, -1, 1],
         [1] * 15 + [-1], [-1] * 15 + [1], [1], [-1], [-1] * 40 + [1] * 4, [1] * 40 + [-1] * 4]


def prepare():
    assert not (ROOT / 'requests.jsonl').exists(), 'prepare refuses after calls'
    out = {'roots': [], 'calls_planned': 12}
    for root in roots():
        row = {'task_id': root['task_id'], 'short_ids_mix': short_ids(root)}
        for c in CONDS:
            tr = scripted(root, c)
            row[c] = {'trace_fixed_draws': tr, 'delta': tr[-1] - tr[0]}
            mc = [scripted(root, c, random.Random(f'mc:{root["task_id"]}:{c}:{k}')) for k in range(500)]
            row[c]['mc500_mean_delta'] = sum(t[-1] - t[0] for t in mc) / 500
            row[c]['calls'] = sum(len(heard_at(start_agents(root, c), p)) for p in root['schedules'])
            out['calls_planned'] += row[c]['calls']
        out['roots'].append(row)
    d = [r['mix']['delta'] - r['full']['delta'] for r in out['roots']]
    dmc = [r['mix']['mc500_mean_delta'] - r['full']['mc500_mean_delta'] for r in out['roots']]
    out['primary_fixed_draws'] = {'mean_diff': sum(d) / 4, 'ci95': boot(d), 'per_root': d}
    out['primary_mc500'] = {'mean_diff': sum(dmc) / 4, 'per_root': dmc}
    save('scripted-reference.json', out)
    print(json.dumps({k: out[k] for k in out if k != 'roots'}, indent=1))


class Stop(Exception):
    pass


class Pool:
    def __init__(self):
        cfg = json.loads(Path('/home/shad0w/.openclaw/openclaw.json').read_text())
        self.key = cfg['models']['providers']['anthropic-proxy']['apiKey']
        self.lock = threading.Lock()
        self.sem = threading.Semaphore(CONC)
        self.count = 0
        self.statuses = []
        self.cool = 0
        self.halted = None

    def rec(self, f, o):
        with (ROOT / f).open('a') as fh:
            fh.write(json.dumps(o, sort_keys=True) + '\n')
            fh.flush()
            os.fsync(fh.fileno())

    def call(self, words, history, meta):
        payload = dict(model=MODEL, max_tokens=16, system=SYSTEM,
                       messages=[dict(role='user', content=user_prompt(words, history))])
        data = json.dumps(payload).encode()
        for attempt in range(4):
            while True:
                with self.lock:
                    if self.halted:
                        raise Stop(self.halted)
                    d = self.cool - time.time()
                if d <= 0:
                    break
                time.sleep(min(d, 3))
            with self.sem:
                with self.lock:
                    if time.time() >= DEADLINE:
                        self.halted = 'deadline 23:30Z'
                        raise Stop(self.halted)
                    if self.count >= CAP:
                        self.halted = 'request cap'
                        raise Stop(self.halted)
                    self.count += 1
                    rid = self.count
                    self.rec('requests.jsonl', dict(request_id=rid, started=now(), attempt=attempt, meta=meta,
                                                    history_len=len(history), model=MODEL))
                st, resp, err, t0 = 0, None, None, time.monotonic()
                try:
                    req = urllib.request.Request('http://127.0.0.1:18811/v1/messages', data=data, headers={
                        'Content-Type': 'application/json', 'x-api-key': self.key,
                        'anthropic-version': '2023-06-01'})
                    with urllib.request.urlopen(req, timeout=120) as r:
                        st = r.status
                        resp = json.loads(r.read())
                except urllib.error.HTTPError as e:
                    st = e.code
                    raw = e.read().decode(errors='replace').replace(self.key, '[R]')[:500]
                    resp = {'raw_error': raw}
                except Exception as e:  # noqa: BLE001
                    err = type(e).__name__
            text = ''
            if st == 200 and resp:
                text = ''.join(x.get('text', '') for x in resp.get('content', []) if x.get('type') == 'text')
            cl = text.strip().strip(' .\n\t"\'`*').lower()
            choice = next((int(k) for k, v in words.items() if cl == v.lower()), None)
            with self.lock:
                self.rec('responses.jsonl', dict(
                    request_id=rid, finished=now(), elapsed_s=round(time.monotonic() - t0, 2), status=st,
                    error=err, text=text, choice=choice, meta=meta, model_returned=(resp or {}).get('model'),
                    usage=(resp or {}).get('usage'), err_body=(resp or {}).get('raw_error')))
                self.statuses.append(st)
                first = self.statuses[:20]
                if len(first) == 20 and sum(s in (429, 503, 529) for s in first) > 10 and not self.halted:
                    self.halted = 'blocked: >50% of first 20 attempts 429/503'
                if st in (400, 401, 403):
                    self.halted = f'fatal status {st}'
                if st != 200:
                    self.cool = max(self.cool, time.time() + random.uniform(20, 30))
            if st == 200:
                return dict(choice=choice, request_id=rid)  # choice None = parse failure
            if self.halted:
                raise Stop(self.halted)
        raise Stop('retries exhausted')


def qualify(pool):
    words = {'1': 'cedar', '-1': 'raven'}

    def one(k, h):
        try:
            return dict(k=k, history=h, **pool.call(words, h, dict(stage='qual', k=k)))
        except Stop as e:
            return dict(k=k, history=h, choice=None, error=str(e))
    with cf.ThreadPoolExecutor(CONC) as ex:
        res = list(ex.map(lambda kh: one(*kh), enumerate(QHIST)))
    valid = sum(r['choice'] is not None for r in res)
    out = dict(valid=valid, n=12, passed=valid >= 11, results=res)  # >=90% of 12 => 11
    save('qualification.json', out)
    print('qual', valid, '/12', flush=True)
    return out['passed']


def episode(pool, root, cond):
    dst = ROOT / 'episodes' / f'{root["task_id"]}-{cond}.json'
    dst.parent.mkdir(exist_ok=True)
    ag = start_agents(root, cond)
    res = dict(task_id=root['task_id'], cond=cond, trace=[frac(ag)], rounds=[],
               short_ids=[i for i in ag if ag[i]['short']], status='started')
    try:
        for rnd, pairs in enumerate(root['schedules'], 1):
            heard = heard_at(ag, pairs)
            for i, w in heard.items():
                push_mem(ag[i], w)
            with cf.ThreadPoolExecutor(CONC) as ex:
                fut = {i: ex.submit(pool.call, root['words'], list(ag[i]['mem']),
                                    dict(stage='episode', task=root['task_id'], cond=cond, round=rnd, agent=int(i)))
                       for i in sorted(heard)}
                new = {i: f.result() for i, f in fut.items()}
            bad = [i for i, r in new.items() if r['choice'] is None]
            if bad:
                raise Stop(f'parse failure agents {bad}')
            sw = sum(new[i]['choice'] != ag[i]['word'] for i in new)
            for i, r in new.items():
                ag[i]['word'] = r['choice']
            res['rounds'].append(dict(round=rnd, heard=heard, choices={i: r['choice'] for i, r in new.items()},
                                      switched=sw))
            res['trace'].append(frac(ag))
            save(dst.relative_to(ROOT), res)
        res['status'] = 'complete'
    except Stop as e:
        res['status'] = 'failed'
        res['error'] = str(e)
    save(dst.relative_to(ROOT), res)
    print(root['task_id'], cond, res['status'], res['trace'], pool.count, flush=True)


def run():
    pool = Pool()
    if not qualify(pool):
        save('STOP.json', dict(reason='qualification failed or blocked', halted=pool.halted,
                               requests=pool.count, time=now()))
        return
    jobs = [(r, c) for r in roots() for c in CONDS]
    with cf.ThreadPoolExecutor(4) as ex:  # global semaphore keeps HTTP concurrency at 4
        list(ex.map(lambda rc: episode(pool, *rc), jobs))
    save('completion.json', dict(time=now(), requests=pool.count, halted=pool.halted))


if __name__ == '__main__':
    prepare() if sys.argv[1] == 'prepare' else run()
