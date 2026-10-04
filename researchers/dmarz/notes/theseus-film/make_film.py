"""Assemble and finish the narrated Swarm of Theseus film.

    page   film.html + the pilot's reduced data + the narration timeline + the look, as one self-contained page
    mix    the narration clips laid on that timeline, levelled to -14 LUFS, and put on the recorded picture

The timeline, the audio mix, the fonts and the mark come from the market-split film's tools (../market-split-film);
the look itself is read at build time from a checkout of the brand kit and is not copied into this repo.

    D=data/theseus-film; M=researchers/dmarz/notes/market-split-film; F=researchers/dmarz/notes/theseus-film
    python3 $F/film_data.py --results researchers/vishesh/notes/swarm-of-theseus/results/S1-a1 \
      --evidence artifacts/theseus-pilot-evidence/theseus-pilot-evidence-v1.gz --out $D/film-data.json
    <venv>/bin/python $M/narrated/vo.py --script $F/script.json --out $D/vo
    python3 $F/make_film.py page --data $D/film-data.json --vo $D/vo --study researchers/vishesh/notes/swarm-of-theseus \
      --kit ~/dmarz-brand-and-content-kit/brand --out $D/theseus.html
    node researchers/dmarz/notes/discussion-dose/src/film_v3/record.mjs $D/theseus.html $D/picture.mp4 --kit ~/dmarz-brand-and-content-kit/brand
    python3 $F/make_film.py mix --vo $D/vo --picture $D/picture.mp4 --out $D/theseus.mp4
"""
import argparse
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = HERE / 'script.json'
MARKET = HERE.parent / 'market-split-film'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


narrated = load('market_split_narrated_build', MARKET / 'narrated' / 'build.py')     # timeline, mix; its `first` has fonts, mark, QR
first = narrated.first


def check_story(d, study):
    """The narration states facts about the pilot. Refuse to build if the records stop supporting any of them."""
    both, neither, wall = d['inside']['both'], d['inside']['neither'], d['wall']
    phrase = both[0]['members'][0]['convention']
    founders_left = lambda run: [sum(s['founder']) for s in run['steps']]
    new = lambda run, s, name: next(m for m in run[s]['members'] if m['id'] == name)
    n1, n3, h1, h3 = new(both, 1, 'new-1'), new(both, 3, 'new-3'), both[1]['handover'], both[3]['handover']
    obs = d['by_scenario']['observatory']
    readme, v2, d2 = ((study / p).read_text() for p in ('README.md', 'v2/RESULTS.md', 'execution-diagnostic/RESULTS-D2.md'))
    claims = {
        'W1: 36 complete runs, 864 calls': d['run']['runs'] == 36 and len(wall) == 36 and d['run']['calls'] == d['run']['calls_reported'] == 864,
        'W2: three members and four cases at every step': all(len(s['founder']) == 3 and len(s['right']) == 4 for r in wall for s in r['steps']),
        'W3: one member replaced at each of steps 1 to 3, none of the original crew after': all(founders_left(r) == [3, 2, 1, 0, 0, 0] for r in wall if r['arm'] != 'founders'),
        'W6: the control crew is never replaced': all(founders_left(r) == [3] * 6 for r in wall if r['arm'] == 'founders'),
        'P1: the seeded notebook says match -> dax, differ -> wug': 'XOR of the two assay bits (0 if equal, 1 if different)' in both[0]['members'][0]['notebook_in']
            and 'Map result 0 to dax and result 1 to wug' in both[0]['members'][0]['notebook_in'],
        'P2: the receipt phrase is amber reed': phrase == 'amber reed' and 'amber reed' in both[0]['members'][0]['notebook_in'],
        'P3: new-1 arrives at step one with an empty notebook': both[1]['members'][0]['id'] == 'new-1' and n1['notebook_in'] == '',
        'P4: its question asks for the procedure and the receipt phrase': 'standard procedure' in h1['question']['message'] and 'receipt phrases' in h1['question']['message'],
        'P5: it is handed the answer and all three notebooks': all(k in n1['onboarding'] for k in ('founder-0:', 'founder-1:', 'founder-2:', 'Departing mentor:'))
            and h1['answer']['actor'] == 'founder-0',
        'P6: four correct bins, the phrase, a notebook in its own words': both[1]['accuracy'] == 1 and n1['labels'] == both[1]['collective'] == both[1]['expected']
            and n1['convention'] == phrase and all(n1['notebook_out'] != m['notebook_out'] for m in both[0]['members']),
        'S1 and S2: all new by step three, every case right at steps four and five': all(not m['id'].startswith('founder') for m in both[3]['members'])
            and both[4]['accuracy'] == both[5]['accuracy'] == 1,
        'S3: the last founder had dropped the phrase and said to sign dax or wug': h3['answer']['actor'] == 'founder-2' and phrase not in h3['answer_notebook']
            and "Use 'dax' or 'wug'" in h3['answer']['message'] and "Use 'dax' or 'wug'" in n3['onboarding'],
        'S4: the other two notebooks kept the phrase and new-3 signed it': n3['onboarding'].count('Receipt: ' + phrase) == 2 and n3['convention'] == phrase,
        'N1: the neighbour has the same cases': all(a['expected'] == b['expected'] for a, b in zip(both, neither)),
        'N2: each newcomer wrote its own rule and phrase; new-1 any bit -> dax, new-2 any bit -> wug': '(dax) if assay[0]=1 OR assay[1]=1' in new(neither, 1, 'new-1')['notebook_out']
            and 'if any element is 1, result=1 (wug)' in new(neither, 2, 'new-2')['notebook_out']
            and all(m['convention'] != phrase and m['onboarding'] == '' for s in (1, 2, 3) for m in [new(neither, s, f'new-{s}')]),
        'N3: right while a founder remains, one in four after': [s['accuracy'] for s in neither] == [1, 1, 1, .25, .25, .25],
        'R2: notes and both 100%, question 92%, nothing 52%': d['after']['notes'] == d['after']['both'] == 1 and round(d['after']['mentor'] * 100) == 92 and round(d['after']['neither'] * 100) == 52,
        'R3: never replaced 90%, all misses at the repair dock': round(d['after']['founders'] * 100) == 90 and d['by_scenario']['seed-bank']['founders']['accuracy'] == 1
            and obs['founders']['accuracy'] == 1 and d['by_scenario']['repair-dock']['founders']['accuracy'] < 1,
        'R4: observatory crews with notes right on every case, phrase kept by nobody': all(obs[a]['accuracy'] == 1 and obs[a]['convention'] == 0 for a in ('notes', 'both')),
        'the tiles agree with the run the film enters': all(next(r for r in wall if (r['scenario'], r['seed'], r['arm']) == (d['worked']['scenario'], d['worked']['seed'], arm))['steps'][s]['receipt']
            == sum(m['convention'] == phrase for m in run[s]['members']) / 3 for arm, run in d['inside'].items() for s in range(6)),
        'C1: the study rates its evidence 1 of 4 and its review says the rule was supplied': '**evidence_confidence:** **1/4**' in readme and 'largely explained by preserving a supplied rule' in readme,
        'C4: the follow-up failed qualification and its diagnostics have not qualified': 'joint competence gate failed' in v2 and 'both predeclared executor gates fail' in d2,
    }
    failed = [k for k, ok in claims.items() if not ok]
    if failed: raise SystemExit('the records no longer support: ' + '; '.join(failed))


def page(args):
    kit, study = Path(args.kit).expanduser(), Path(args.study)
    data = json.loads(Path(args.data).read_text())
    check_story(data, study)
    data['timeline'] = narrated.timeline(args.vo, SCRIPT)
    data['evidence_confidence'] = '1 of 4'
    root = re.search(r':root\s*\{.*?\n\}', (kit / 'dist' / 'tokens.css').read_text(), re.S).group(0)
    html = (HERE / 'film.html').read_text()
    for slot, value in (('/*__TOKENS__*/', root), ('/*__FONTS__*/', first.font_css(kit)), ('/*__DATA__*/null', json.dumps(data, sort_keys=True)),
                        ('/*__QR__*/', first.QR.read_text().strip()), ('__MARK__', first.mark_uri(kit))):
        if slot not in html: raise SystemExit(f'slot {slot} missing from film.html')
        html = html.replace(slot, value)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)
    end = data['timeline'][-1]
    print(f'wrote {out} ({len(html) / 1e6:.2f} MB), {end["start"] + end["dur"]:.1f} s')


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('page')
    for a in ('data', 'vo', 'study', 'kit', 'out'): p.add_argument('--' + a, required=True)
    m = sub.add_parser('mix')
    for a in ('vo', 'picture', 'out'): m.add_argument('--' + a, required=True)
    args = ap.parse_args()
    if args.cmd == 'page': page(args)
    else: args.script = SCRIPT; narrated.mix(args)


if __name__ == '__main__':
    main()
