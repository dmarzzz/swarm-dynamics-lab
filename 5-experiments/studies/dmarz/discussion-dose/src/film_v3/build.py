"""Assemble the self-contained film page: film.html + the run's reduced data + the look.

The look is not copied into this repo. Tokens, fonts and the cube are read at build time from a checkout of the
brand kit (@dmarz/kit, its `brand/` folder), so a change there shows up on the next build.

    python3 researchers/dmarz/notes/discussion-dose/src/film_v3/build.py \
      --data data/discussion-v3/v3-q0-a1/film-data.json --kit ~/dmarz-brand-and-content-kit/brand \
      --out data/discussion-v3/v3-q0-a1/film/discussion-memory-v3.html
"""
import argparse
import base64
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent


def check_story(d):
    """The captions tell one story. Refuse to build if the data stops supporting any sentence of it."""
    w, a, q = d['worked'], d['attacked'], d['qualification']
    exposed, witness = w['roles']['exposed'], w['roles']['witness']
    claims = {
        'one agent holds the planted value before sharing, another the true one':
            w['initial']['beliefs'].count('false') == 1 and w['initial']['beliefs'][exposed] == 'false'
            and w['initial']['beliefs'][witness] == 'true',
        'after one exchange all three endorse the planted value': w['reports']['beliefs'] == ['false'] * 3,
        'reports-only memory records the planted value and the parent repeats it':
            w['arms']['reports']['memory']['target'] == 'false' and w['arms']['reports']['parent']['outcome'] == 'wrong'
            and w['arms']['reports']['parent']['value'] == w['false'] + w['delta'],
        'with no sharing the parent has nothing to go on':
            w['arms']['independent']['memory']['records'] == 0 and w['arms']['independent']['parent']['outcome'] == 'abstain',
        'alone: one agent recovers, no majority, the fact drops, the parent abstains':
            w['arms']['private']['final']['beliefs'].count('true') == 1 and w['arms']['private']['memory']['target'] is None
            and w['arms']['private']['parent']['outcome'] == 'abstain',
        'together: all hold the true value by round 3 and vote the winner':
            w['arms']['board']['rounds'][2]['beliefs'] == ['true'] * 3
            and w['arms']['board']['rounds'][2]['votes'] == [w['winner']] * 3
            and w['arms']['board']['rounds'][0]['beliefs'][witness] == 'true',
        'board memory records the true value and the parent answers the truth':
            w['arms']['board']['memory']['target'] == 'true' and w['arms']['board']['parent']['value'] == w['truth_answer'],
        'the quote is the witness in board round 1': w['quote']['agent'] == witness and w['quote']['turn'] == 1,
        'six worlds, no invalid ballots or parents': len(d['worlds']) == 6 and d['invalid_ballots'] == 0
            and all(v['invalid'] == 0 for v in a.values()),
        'early merge misleads more parents than either three-round arm':
            a['reports']['wrong'] > a['private']['wrong'] >= a['board']['wrong'],
        'board parents right at least as often as private': a['board']['correct'] >= a['private']['correct'],
        'primary contrast is identified and zero in every resolvable world':
            d['primary']['mean'] == 0 and all(p['contrast'] == 0 for p in d['primary']['per_world']),
        'no clean parent is wrong': all(v['parent_wrong'] == 0 for v in d['clean'].values()),
        'the model did not qualify, on the clean reports-only floor':
            not q['model_qualified'] and q['clean_reports_correct'] < q['required_each'],
        'run complete and audited': d['run']['audit_ok'] and q['execution_complete'],
    }
    failed = [k for k, ok in claims.items() if not ok]
    if failed: raise SystemExit('the data no longer supports: ' + '; '.join(failed))


def font_css(kit):
    faces = json.loads((kit / 'fonts' / 'fonts.json').read_text())['faces']
    css = []
    for f in faces:
        if f['style'] != 'normal': continue
        b64 = base64.b64encode((kit / 'fonts' / f['file']).read_bytes()).decode()
        css.append(f"@font-face {{ font-family: '{f['family']}'; font-weight: {f['weight']}; font-style: normal; "
                   f"src: url(data:font/ttf;base64,{b64}) format('truetype'); }}")
    return '\n'.join(css)


def mark_uri(kit):
    """One frame of the kit's cube loop, cropped to the cube, for the page that plays alone. The recorder hides it
    and lays the moving loop over the same spot."""
    png = subprocess.run(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-ss', '3', '-i', str(kit / 'marks/cube/cube-loop-alpha.webm'),
                          '-frames:v', '1', '-vf', 'crop=380:380:0:0', '-f', 'image2pipe', '-c:v', 'png', '-'],
                         check=True, capture_output=True).stdout
    return 'data:image/png;base64,' + base64.b64encode(png).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True); ap.add_argument('--kit', required=True); ap.add_argument('--out', required=True)
    args = ap.parse_args()
    kit = Path(args.kit).expanduser()
    data = json.loads(Path(args.data).read_text())
    check_story(data)
    tokens = (kit / 'dist' / 'tokens.css').read_text()
    root = re.search(r':root\s*\{.*?\n\}', tokens, re.S).group(0)      # the sys roles only; format scopes are not used here
    qr = (HERE / 'qr-repo.svg').read_text().strip()
    page = (HERE / 'film.html').read_text()
    for slot, value in (('/*__TOKENS__*/', root), ('/*__FONTS__*/', font_css(kit)), ('/*__DATA__*/null', json.dumps(data, sort_keys=True)),
                        ('/*__QR__*/', qr), ('__MARK__', mark_uri(kit))):
        if slot not in page: raise SystemExit(f'slot {slot} missing from film.html')
        page = page.replace(slot, value)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(page)
    print(f'wrote {out} ({len(page) / 1e6:.2f} MB)')


if __name__ == '__main__':
    main()
