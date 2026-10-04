"""One explicit S0 batch. Append assignments, then record all results; never retry."""
import argparse
import hashlib
import itertools
import json
import platform
import subprocess
from pathlib import Path
import sim

ROOT = Path(__file__).resolve().parents[1]


def run(backend, out, progress=None):
    design = json.loads((ROOT / 'design.yaml').read_text())
    out.mkdir(parents=True, exist_ok=False)
    assignments = list(itertools.product(design['tasks'], design['worlds'], design['deadlines']))
    metadata = {'backend': backend, 'platform': platform.system(), 'machine': platform.machine(),
                'python': platform.python_version(), 'stage': 'S0',
                'code': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'design_hash': hashlib.sha256((ROOT / 'design.yaml').read_bytes()).hexdigest(),
                'assigned_blocks': len(assignments), 'complete': False}
    (out / 'assignments.json').write_text(json.dumps(assignments))
    (out / 'manifest.json').write_text(json.dumps(metadata, indent=2))
    decide = sim.scripted
    if backend == 'laya':
        from backend import Laya
        decide = Laya()
        metadata.update(decide.metadata)
    records = []
    with (out / 'episodes.jsonl').open('x') as f:
        for n, (task, world, deadline) in enumerate(assignments, 1):
            rows = sim.run_episode(task, 1, world, deadline, list(sim.ARMS), {'decide': decide})
            for row in rows:
                row.update(metadata)
                f.write(json.dumps(row) + '\n')
                f.flush()
            records += rows
            if progress:
                progress(n, len(assignments))
    cells = []
    for arm, world, deadline in itertools.product(sim.ARMS, design['worlds'], design['deadlines']):
        rows = [r for r in records if (r['arm'], r['world'], r['dose']) == (arm, world, deadline)]
        cells.append({'arm': arm, 'world': world, 'deadline': deadline, 'assigned': len(rows),
                      'correct': sum(r['evaluation']['correct'] for r in rows),
                      'committed': sum(r['evaluation']['committed'] for r in rows),
                      'false_commit': sum(r['evaluation']['false_commit'] for r in rows),
                      'invalid': sum(not r['validity']['ok'] for r in rows),
                      'mean_loss': sum(r['evaluation']['loss'] for r in rows) / len(rows)})
    invalid = sum(not r['validity']['ok'] for r in records)
    qualified = not invalid and all(c['correct'] / c['assigned'] >= .8 for c in cells if c['world'] == 'clean')
    summary = {'backend': backend, 'episodes': len(records), 'invalid': invalid,
               'clean_qualification_pass': qualified, 'cells': cells,
               'physical_calls': sum(r['cost_actual']['shared_tape_calls'] for r in records if r['arm'] == 'central'),
               'physical_inference_s': sum(r['cost_actual']['shared_tape_wall_s'] for r in records if r['arm'] == 'central')}
    metadata['complete'] = True
    (out / 'manifest.json').write_text(json.dumps(metadata, indent=2))
    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    from replay import render
    render(records, out / 'replay.html')
    return summary


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--backend', choices=['scripted', 'laya'], required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    result = run(args.backend, args.out)
    print(json.dumps({k: v for k, v in result.items() if k != 'cells'}))
