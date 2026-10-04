"""Reduce the Sonnet market-split pilot (s1-002) to what the narrated film draws.

Adds three things to the first film's data (../build_data.py): every one of the 36 episodes, round by round, for the
wall of runs; the round-1 message the agent was sent in the worked run and the reply it returned, copied from the
saved call record; and the mean profit of the free and the one-firm arm under the per-firm rule.

    python3 researchers/dmarz/notes/market-split-film/narrated/build_data.py \
      --records artifacts/market-split-sonnet-s1-002-records/market-split-sonnet-s1-002-records-v1.zip \
      --report researchers/dmarz/notes/market-split-api/report/s1-002 \
      --prompt researchers/dmarz/notes/market-split-api/src/prompt.txt \
      --out data/market-split-film/narrated/film-data.json
"""
import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from build_data import ARM, LANES, WORKED          # noqa: E402  (the first film's choices: flexible arm, market 36)

ARMS = [ARM, 'neutral_locked']                     # free to register, held to one firm
READS = {'none': 'owner_hhi', 'firm': 'firm_hhi', 'owner': 'owner_hhi'}   # what the rule scores (no rule: nothing is enforced)


def main():
    ap = argparse.ArgumentParser()
    for a in ('records', 'report', 'prompt', 'out'): ap.add_argument('--' + a, required=True)
    args = ap.parse_args()
    base = Path(args.out).with_name('base.json')
    base.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(HERE.parent / 'build_data.py'), '--records', args.records, '--report', args.report,
                    '--out', str(base)], check=True, stdout=subprocess.DEVNULL)
    data = json.loads(base.read_text()); base.unlink()

    with zipfile.ZipFile(args.records) as z:
        eps = [json.loads(line) for line in z.read('episodes.jsonl').decode().splitlines() if line.strip()]
        calls = {c['call_id']: c for c in (json.loads(line) for line in z.read('calls.jsonl').decode().splitlines() if line.strip())}
    by = {(e['task_id'], e['world'], e['arm']): e for e in eps}
    tasks = sorted({k[0] for k in by})
    if len(by) != len(tasks) * len(LANES) * len(ARMS): raise SystemExit('an episode is missing')

    # the wall: product A's output per firm, and the concentration the rule scores (the higher of the two products)
    wall = []
    for lane in LANES:
        for arm in ARMS:
            for task in tasks:
                e = by[(task, lane, arm)]
                rounds = [{'q': [f['q'][0] for f in t['firms'] if f['owner'] == 'P'], 'r': [f['q'][0] for f in t['firms'] if f['owner'] != 'P'],
                           'c': t['capacity_per_firm'][0], 'h': max(t[READS[lane]])} for t in e['trace']]
                wall.append({'task': task, 'lane': lane, 'free': arm == ARM, 'capacity': e['market']['capacity'][0],
                             'rival_capacities': [c[0] for c in e['market']['rival_capacities']], 'rounds': rounds,
                             'split': e['evaluation']['first_registration_round'], 'profit': e['evaluation']['profit']})
    data['wall'] = wall

    # the agent's view: the saved round-1 call of the worked run
    seed = by[(WORKED, 'firm', ARM)]['seed']
    call = calls[f"{data['run']['attempt']}:{WORKED}:{seed}:firm:{ARM}:r1"]
    prompt = Path(args.prompt).read_text()
    data['pov'] = {'call_id': call['call_id'], 'observation': call['observation'], 'response_text': call['accounting']['response_text'],
                   'latency_seconds': call['accounting']['latency_seconds'], 'instruction': '. '.join(prompt.split('. ')[:2]) + '.'}

    summary = {r['regulator']: r for r in json.loads((Path(args.report) / 'descriptive-summary.json').read_text())}
    data['means'] = {'free': summary['firm']['dynamic_profit'], 'held': summary['firm']['locked_profit'], 'markets': summary['firm']['paired_tasks']}

    Path(args.out).write_text(json.dumps(data, sort_keys=True))
    print(f'wrote {args.out}: {len(wall)} runs on the wall, call {call["call_id"]}')


if __name__ == '__main__':
    main()
