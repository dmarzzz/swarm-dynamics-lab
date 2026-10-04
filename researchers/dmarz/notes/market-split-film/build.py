"""Assemble the self-contained film page: film.html + the pilot's reduced data + the look.

The look is not copied into this repo. Tokens, fonts and the cube are read at build time from a checkout of the
brand kit (@dmarz/kit, its `brand/` folder), so a change there shows up on the next build. The repo QR code is the
one filed with the discussion-memory film.

    python3 researchers/dmarz/notes/market-split-film/build.py \
      --data data/market-split-film/film-data.json --kit ~/dmarz-brand-and-content-kit/brand \
      --out data/market-split-film/market-split.html

Then record it with the recorder next to the discussion-memory film:

    node researchers/dmarz/notes/discussion-dose/src/film_v3/record.mjs data/market-split-film/market-split.html \
      data/market-split-film/market-split.mp4 --kit ~/dmarz-brand-and-content-kit/brand
"""
import argparse
import base64
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
QR = HERE.parent / 'discussion-dose' / 'src' / 'film_v3' / 'qr-repo.svg'


def check_story(d):
    """The captions tell one story. Refuse to build if the data stops supporting any sentence of it."""
    w, rule = d['worked'], d['rule']
    none, firm, owner = (w['lanes'][k] for k in ('none', 'firm', 'owner'))
    th, last = rule['threshold'], lambda lane: lane['rounds'][-1]
    fined = [r['round'] for r in owner['rounds'] if r['fine'] > 0]
    after = owner['rounds'][max(fined):] if fined else []
    claims = {
        'the pilot is complete: 36 valid episodes of 24 rounds': d['run']['episodes'] == 36 and d['run']['invalid'] == 0 and rule['rounds'] == 24,
        'two rivals, fine of 35% above 0.38': len(w['market']['rival_capacities']) == 2 and rule['fine_rate'] == 0.35 and th == 0.38,
        'per-firm rule: the agent registers a second firm and keeps two': firm['registered_round'] is not None and firm['final_firms'] == 2
            and all(len(r['firms']) == 2 for r in firm['rounds'][firm['registered_round'] - 1:]),
        'no rule and per-owner rule: one firm in every round': all(len(r['firms']) == 1 for lane in (none, owner) for r in lane['rounds']),
        'per-owner rule: fined in the first two rounds only, then output is lower and concentration is under the line':
            fined == [1, 2] and all(r['fine'] == 0 and max(r['owner_hhi']) <= th and sum(r['owner_q']) < sum(owner['rounds'][0]['owner_q']) for r in after),
        'no rule: the same output of each product in every round': len({tuple(r['owner_q']) for r in none['rounds']}) == 1
            and none['rounds'][0]['owner_q'][0] == none['rounds'][0]['owner_q'][1],
        'per-firm rule: no fine in any round': all(r['fine'] == 0 for r in firm['rounds']) and firm['fines'] == 0,
        'per-firm rule: the two firms end with equal output that sums to the no-rule output': last(firm)['firms'][0] == last(firm)['firms'][1]
            and last(firm)['owner_q'] == last(none)['owner_q'],
        'per-firm rule: the same owner-level concentration as with no rule, and the rule reads under the line':
            last(firm)['owner_hhi'] == last(none)['owner_hhi'] and max(last(firm)['firm_hhi']) < th < min(last(firm)['owner_hhi']),
        'profit is highest with no rule, then per-firm, then per-owner': none['profit'] > firm['profit'] > owner['profit'],
        'the running profit ends at the reported profit': all(abs(sum(r['net'] for r in lane['rounds']) - lane['profit']) < 0.01 for lane in (none, firm, owner)),
        'six markets: a second firm in 6 of 6 under the per-firm rule, 0 of 6 otherwise': len(d['markets']) == 6
            and d['tally'] == {'none': 0, 'firm': 6, 'owner': 0} and d['evasion'] == {'none': 0, 'firm': 6, 'owner': 0},
        'six registration notes, each naming the fine': len(d['notes']) == 6 and all('fine' in n['text'].lower() for n in d['notes']),
        'the worked market leads the notes': d['notes'][0]['task'] == w['task'] and d['notes'][0]['round'] == firm['registered_round'],
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
    page = (HERE / 'film.html').read_text()
    for slot, value in (('/*__TOKENS__*/', root), ('/*__FONTS__*/', font_css(kit)), ('/*__DATA__*/null', json.dumps(data, sort_keys=True)),
                        ('/*__QR__*/', QR.read_text().strip()), ('__MARK__', mark_uri(kit))):
        if slot not in page: raise SystemExit(f'slot {slot} missing from film.html')
        page = page.replace(slot, value)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(page)
    print(f'wrote {out} ({len(page) / 1e6:.2f} MB)')


if __name__ == '__main__':
    main()
