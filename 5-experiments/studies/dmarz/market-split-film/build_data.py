"""Reduce the Sonnet market-split pilot (s1-002) to the numbers the film draws.

Reads the filed records archive and the study's report folder; writes one small JSON file. Nothing is estimated
here: every value is copied from a saved trace, or is a sum or a count over saved traces.

    python3 researchers/dmarz/notes/market-split-film/build_data.py \
      --records artifacts/market-split-sonnet-s1-002-records/market-split-sonnet-s1-002-records-v1.zip \
      --report researchers/dmarz/notes/market-split-api/report/s1-002 \
      --out data/market-split-film/film-data.json
"""
import argparse
import json
import zipfile
from pathlib import Path

LANES = ['none', 'firm', 'owner']          # no rule, per-firm rule, per-owner rule
ARM = 'neutral_dynamic'                    # the flexible arm: one to four firms allowed
WORKED = 36                                # first of the six task ids, chosen before looking at the traces


def reduce_round(t):
    own = [f['q'] for f in t['firms'] if f['owner'] == 'P']
    rivals = [f['q'] for f in t['firms'] if f['owner'] != 'P']
    return {'round': t['round'], 'op': t['operation'], 'firms': own, 'rivals': rivals, 'owner_q': t['owner_q'],
            'capacity_per_firm': t['capacity_per_firm'], 'firm_hhi': t['firm_hhi'], 'owner_hhi': t['owner_hhi'],
            'fine': t['fine'], 'net': t['net_profit'], 'note': t['action']['note']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', required=True); ap.add_argument('--report', required=True); ap.add_argument('--out', required=True)
    args = ap.parse_args()
    with zipfile.ZipFile(args.records) as z:
        eps = [json.loads(line) for line in z.read('episodes.jsonl').decode().splitlines() if line.strip()]
    report = Path(args.report)
    usage = json.loads((report / 'usage.json').read_text())
    analysis = json.loads((report / 'analysis.json').read_text())
    notes = json.loads((report / 'first-registration-notes.json').read_text())

    flex = {(e['task_id'], e['world']): e for e in eps if e['arm'] == ARM}
    tasks = sorted({k[0] for k in flex})
    if any((task, lane) not in flex for task in tasks for lane in LANES): raise SystemExit('a flexible-arm episode is missing')
    if not all(e['validity']['ok'] and len(e['trace']) == e['cfg']['rounds'] for e in eps): raise SystemExit('an episode is invalid or short')

    cfg = flex[(WORKED, 'firm')]['cfg']
    worked = {'task': WORKED, 'market': flex[(WORKED, 'firm')]['market'], 'lanes': {}}
    for lane in LANES:
        e = flex[(WORKED, lane)]
        worked['lanes'][lane] = {'run': e['run'], 'rounds': [reduce_round(t) for t in e['trace']],
                                 'profit': e['evaluation']['profit'], 'fines': e['evaluation']['fines'],
                                 'registered_round': e['evaluation']['first_registration_round'],
                                 'final_firms': e['evaluation']['final_firm_count']}

    markets = []
    for task in tasks:
        row = {'task': task, 'lanes': {}}
        for lane in LANES:
            e = flex[(task, lane)]; last = reduce_round(e['trace'][-1])
            row['lanes'][lane] = {'registered_round': e['evaluation']['first_registration_round'],
                                  'final_firms': e['evaluation']['final_firm_count'],
                                  'evasion': bool(e['evaluation']['behavioral_evasion']),
                                  'capacity': e['market']['capacity'], 'rival_capacities': e['market']['rival_capacities'],
                                  'last': {k: last[k] for k in ('firms', 'rivals', 'capacity_per_firm')},
                                  'profit': e['evaluation']['profit']}
        markets.append(row)

    data = {
        'run': {'attempt': usage['attempt'], 'model': usage['model'], 'episodes': analysis['episodes'], 'invalid': analysis['invalid'],
                'calls': usage['attempted_calls'], 'cost_usd': usage['api_cost_usd']},
        'rule': {'threshold': flex[(WORKED, 'firm')]['dose'], 'fine_rate': cfg['fine_rate'], 'registration_fee': cfg['registration_fee'],
                 'overhead': cfg['overhead'], 'rounds': cfg['rounds'], 'max_firms': cfg['max_firms']},
        'worked': worked,
        'markets': markets,
        'tally': {lane: sum(1 for m in markets if m['lanes'][lane]['registered_round'] is not None) for lane in LANES},
        'evasion': {lane: sum(1 for m in markets if m['lanes'][lane]['evasion']) for lane in LANES},
        'notes': [{'task': n['task_id'], 'round': n['round'], 'text': n['brief_action_note']} for n in notes],
    }
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, sort_keys=True))
    print(f'wrote {out}: {len(markets)} markets, tally {data["tally"]}')


if __name__ == '__main__':
    main()
