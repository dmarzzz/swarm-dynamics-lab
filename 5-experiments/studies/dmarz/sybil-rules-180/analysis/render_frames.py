"""Re-draw the S1 final frame, the S1 replay and the D1 frame of the gpt-6-sol run from the committed records with the
study's own renderer (src/render.py at the run's source hash). No model call.

    STUDY_MODEL=gpt-6-sol python3 analysis/render_frames.py records/gpt-6-sol <output dir>
"""
import gzip
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'src'))
import analyze  # noqa: E402
import render  # noqa: E402
import study  # noqa: E402


def rows(path):
    with gzip.open(path, 'rt') as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    s1 = next(p for p in root.glob('*s1-*') if p.is_dir())
    d1 = next(p for p in root.glob('*d1-*') if p.is_dir())
    run = {}
    for r in rows(s1 / 'rounds.jsonl.gz'):
        run.setdefault(r['label'], []).append(r)
    d = study.design()
    e = d['economy']
    meta = {'markets': e['markets'], 'start_products': study.main_start_products(), 'threshold': d['cfg']['threshold'],
            'stage': 'S1', 'scripted': False, 'branch_order': study.branch_order(), 'cfg': d['cfg']}
    s = json.loads((s1 / 'summary.json').read_text())
    acc = {k: s[k] for k in ('model_calls', 'input_tokens', 'output_tokens', 'cost_usd')}
    acc.update(void_rounds=s['void'], rejected_commands=s['rejected_commands'])
    render.economy_frame(run, meta, accounting=acc).save(out / 'sybil-rules-180-final-frame.png')
    render.economy_replay(run, meta, out / 'sybil-rules-180-replay.gif', accounting=acc)
    an = analyze.analyze_diagnostic(rows(d1 / 'rounds.jsonl.gz'))
    render.diagnostic_frame(an['episodes'], {'stage': 'D1', 'scripted': False}).save(out / 'sybil-rules-180-d1-frame.png')


if __name__ == '__main__':
    main()
