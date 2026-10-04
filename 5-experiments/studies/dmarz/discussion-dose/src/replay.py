"""Backfill replay.json for a finished run from its saved event journal. No model calls; no outcome changes.

    python3 src/replay.py results/episodes/<run-dir> [--upload RUN_ID]
"""
import argparse
import json
from pathlib import Path
from frames import FrameTracker
from tasks import make_world, allocation
from tasks_v2 import make_world_v2

def build(run_dir):
    run_dir = Path(run_dir); manifest = json.loads((run_dir / 'manifest.json').read_text()); params = manifest['params']
    protocol = params.get('protocol', 'v1'); level = params.get('level')
    world_for = (lambda t: make_world_v2(t, level)) if protocol == 'v2' else \
        (lambda t: (lambda w: {**w, 'roles': {'exposed': allocation(w, params['n_agents'], params['seeds'][0])[1]}})(make_world(t)))
    tracker = FrameTracker(world_for, run_dir / 'frame.json', every=1e9, protocol=protocol, level=level)
    episodes = {}
    for line in (run_dir / 'episodes.jsonl').read_text().splitlines():
        r = json.loads(line); episodes[(r['task_id'], json.dumps(r['arm'], sort_keys=True))] = r
    finished = set()
    for line in (run_dir / 'events.jsonl').read_text().splitlines():
        x = json.loads(line); label, e = x['stream'], x['event']; tracker.event(label, e)
        if label.get('phase') == 'continuation' and e['kind'] in ('call_response', 'call_failure') and e.get('phase') == 'parent' or e['kind'] == 'call_failure':
            key = (label.get('task_id'), json.dumps(label.get('arm'), sort_keys=True))
            if key in episodes and key not in finished: finished.add(key); tracker.episode_done(episodes[key])
    for key, r in episodes.items():  # invalid episodes whose failure ended before a parent call
        if key not in finished: tracker.episode_done(r)
    out = run_dir / 'replay.json'; out.write_text(json.dumps(tracker.replay(), separators=(',', ':')))
    return out

def main():
    p = argparse.ArgumentParser(); p.add_argument('run_dir'); p.add_argument('--upload'); a = p.parse_args()
    out = build(a.run_dir); print(out, out.stat().st_size)
    if a.upload:
        import swarm_report as sr
        print(sr.upload(a.upload, out, 'replay.json'))

if __name__ == '__main__': main()
