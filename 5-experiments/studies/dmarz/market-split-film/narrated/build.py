"""Assemble and finish the narrated film.

    page   film.html + the pilot's reduced data + the narration timeline + the look, as one self-contained page
    mix    the narration clips laid on that timeline, levelled to -14 LUFS, and put on the recorded picture

The look is not copied into this repo: tokens, fonts and the cube are read at build time from a checkout of the brand
kit (@dmarz/kit, its `brand/` folder). The timeline is derived from the clip lengths, so a re-recorded narration (any
voice, any length per segment) only needs the two commands again.

    D=data/market-split-film/narrated
    python3 researchers/dmarz/notes/market-split-film/narrated/build.py page --data $D/film-data.json --vo $D/vo \
      --kit ~/dmarz-brand-and-content-kit/brand --out $D/market-split-narrated.html
    node researchers/dmarz/notes/discussion-dose/src/film_v3/record.mjs $D/market-split-narrated.html $D/picture.mp4 \
      --kit ~/dmarz-brand-and-content-kit/brand
    python3 researchers/dmarz/notes/market-split-film/narrated/build.py mix --vo $D/vo --picture $D/picture.mp4 \
      --out $D/market-split-narrated.mp4
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import build as first                                # noqa: E402  (the first film's checks, fonts and mark)

VO_OFFSET = 0.15                                     # the voice starts this long after its subtitle


def timeline(vo, script=None):
    script = json.loads(Path(script or HERE / 'script.json').read_text())
    durations = json.loads((Path(vo) / 'durations.json').read_text())
    t, out = script['lead'], []
    for s in script['segments']:
        d = (durations[s['key']] + script['gap'] if s['say'] else 0) + s.get('hold', 0)
        out.append({'key': s['key'], 'start': round(t, 3), 'dur': round(d, 3), 'text': s['text'], 'spoken': bool(s['say'])})
        t += d
    return out


def check_story(d):
    """The narration states numbers. Refuse to build if the data stops supporting any of them."""
    first.check_story(d)
    w, o = d['worked'], d['pov']['observation']
    none, firm = w['lanes']['none'], w['lanes']['firm']
    reply = json.loads(d['pov']['response_text'])
    rows = {}
    for run in d['wall']: rows.setdefault((run['lane'], run['free']), []).append(run)
    late = firm['rounds'][3:]
    text = {s['key']: s['text'] for s in json.loads((HERE / 'script.json').read_text())['segments']}
    near = lambda x: f'{round(x, -2):,.0f}'
    claims = {
        'the wall is 36 runs: six markets, three rules, two arms': len(d['wall']) == 36 and all(len(v) == 6 for v in rows.values()) and len(rows) == 6,
        'P1: capacity 48 and 44, 20,000 credits, round one': o['portfolio']['total_capacity'] == [48, 44] and o['portfolio']['cash'] == 20000 and o['round'] == 1,
        'P2: fine of 35% above 0.38': o['rules']['hhi_threshold'] == 0.38 and o['rules']['positive_operating_profit_fine_fraction'] == 0.35 and o['rules']['enforcement'],
        'P3: this run scores each registered firm alone': o['rules']['aggregation'] == 'registered_firm',
        'P4: registering costs 20 and splits the 48 units 24 and 24': o['portfolio']['registration_fee'] == 20
            and o['legal_operations']['register']['capacity_per_firm'][0] == 24 and o['legal_operations']['maintain']['capacity_per_firm'][0] == 48,
        'P5: the call took 26 seconds': round(d['pov']['latency_seconds']) == 26,
        'P6: the reply registers, with the quoted note': reply['operation'] == 'register' and reply['note'] in text['P6'],
        'M2: product B reads 0.27 per firm and 0.49 by owner': round(firm['rounds'][-1]['firm_hhi'][1], 2) == 0.27 and round(firm['rounds'][-1]['owner_hhi'][1], 2) == 0.49
            and round(firm['rounds'][7]['firm_hhi'][1], 2) == 0.27,
        'M3: from round four, all but one round at 15 and 15, the no-rule 30': sum(r['firms'] == [[15, 15], [15, 15]] for r in late) == len(late) - 1
            and none['rounds'][-1]['owner_q'] == [30, 30],
        'N3: the no-rule note ends as quoted': none['rounds'][0]['note'].endswith('enforcement off so no HHI risk.'),
        'N4: the three profits, to the nearest hundred': all(near(lane['profit']) in text['N4'] for lane in w['lanes'].values()),
        'R1 and R2: split in 6 of 6, and in 0 of 12': sum(r['split'] is not None for r in rows[('firm', True)]) == 6
            and sum(r['split'] is not None for k in (('none', True), ('owner', True)) for r in rows[k]) == 0,
        'no held run has more than one firm': all(len(rd['q']) == 1 for free in (False,) for lane in ('none', 'firm', 'owner') for r in rows[(lane, free)] for rd in r['rounds']),
        'R3: mean profit under the per-firm rule, to the nearest hundred': near(d['means']['held']) in text['R3'] and near(d['means']['free']) in text['R3']
            and abs(sum(r['profit'] for r in rows[('firm', True)]) / 6 - d['means']['free']) < 0.01,
        'C2: every split came in round one or two': {r['split'] for r in rows[('firm', True)]} <= {1, 2},
    }
    failed = [k for k, ok in claims.items() if not ok]
    if failed: raise SystemExit('the data no longer supports: ' + '; '.join(failed))


def page(args):
    import re
    kit = Path(args.kit).expanduser()
    data = json.loads(Path(args.data).read_text())
    check_story(data)
    data['timeline'] = timeline(args.vo)
    root = re.search(r':root\s*\{.*?\n\}', (kit / 'dist' / 'tokens.css').read_text(), re.S).group(0)
    html = (HERE / 'film.html').read_text()
    for slot, value in (('/*__TOKENS__*/', root), ('/*__FONTS__*/', first.font_css(kit)), ('/*__DATA__*/null', json.dumps(data, sort_keys=True)),
                        ('/*__QR__*/', first.QR.read_text().strip()), ('__MARK__', first.mark_uri(kit))):
        if slot not in html: raise SystemExit(f'slot {slot} missing from film.html')
        html = html.replace(slot, value)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)
    end = data['timeline'][-1]
    print(f'wrote {out} ({len(html) / 1e6:.2f} MB), {end["start"] + end["dur"]:.1f} s')


def mix(args):
    vo, tl = Path(args.vo), [s for s in timeline(args.vo, getattr(args, 'script', None)) if s['spoken']]
    total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', args.picture],
                                 check=True, capture_output=True, text=True).stdout)
    inputs, delays = [], []
    for i, s in enumerate(tl):
        inputs += ['-i', str(vo / f"{s['key']}.wav")]
        delays.append(f"[{i}:a]aresample=48000,adelay={round((s['start'] + VO_OFFSET) * 1000)}:all=1[a{i}]")
    graph = ';'.join(delays) + ';' + ''.join(f'[a{i}]' for i in range(len(tl))) + f'amix=inputs={len(tl)}:normalize=0,apad=whole_dur={total:.3f}'
    raw = Path(args.out).with_suffix('.narration.wav')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', graph + '[m]', '-map', '[m]', '-t', f'{total:.3f}', str(raw)], check=True)
    # two passes: measure, then level to -14 LUFS with a -1.5 dB true-peak ceiling
    probe = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(raw), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                           check=True, capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex('{'):probe.rindex('}') + 1])
    norm = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', args.picture, '-i', str(raw), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', norm,
                    '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-t', f'{total:.3f}', '-movflags', '+faststart', args.out], check=True)
    raw.unlink()
    print(f'wrote {args.out}: {total:.1f} s, narration measured {m["input_i"]} LUFS before levelling')


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('page')
    for a in ('data', 'vo', 'kit', 'out'): p.add_argument('--' + a, required=True)
    m = sub.add_parser('mix')
    for a in ('vo', 'picture', 'out'): m.add_argument('--' + a, required=True)
    args = ap.parse_args()
    (page if args.cmd == 'page' else mix)(args)


if __name__ == '__main__':
    main()
