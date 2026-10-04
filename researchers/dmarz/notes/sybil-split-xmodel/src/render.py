"""Frames from measured rows only: identity-count curves, accuracy against attacker seat share,
per-root paired contrasts, and a bounded completion-prefix replay. PIL only; 1800x1200."""
from collections import defaultdict
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

import analyze
import study

W, H = 1800, 1200
BG = '#111b2a'; INK = '#edf3fb'; MUTED = '#a7b5c7'; GRID = '#324153'; ACCENT = '#5fd7d0'
COLORS = {'coverage': '#5fd7d0', 'random': '#f4c777', 'degree': '#bb9df6', 'no_verification': '#8796aa'}
FAMILY_COLORS = {'ring': '#f4c777', 'community': '#5fd7d0'}
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf',
              '/System/Library/Fonts/Helvetica.ttc')


@lru_cache(maxsize=32)
def font(size):
    for path in FONT_PATHS:
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    try: return ImageFont.load_default(size)
    except TypeError: return ImageFont.load_default()


def dashed(d, a, b, fill, width):
    for t in range(0, 20, 2):
        p = tuple(a[i] + (b[i] - a[i]) * t / 20 for i in (0, 1)); q = tuple(a[i] + (b[i] - a[i]) * (t + 1) / 20 for i in (0, 1))
        d.line((*p, *q), fill=fill, width=width)


def cell_means(rows):
    """(family, attacker_pass, arm, checks, k) -> means over completed rows, with the count."""
    grouped = defaultdict(list)
    for r in rows:
        if r.get('kind') == 'pilot' and r.get('status') == 'completed':
            grouped[(r['family'], r['attacker_pass'], r['arm'], r['checks'], r['k'])].append(r)
    out = {}
    for key, rr in grouped.items():
        n = len(rr)
        out[key] = {'n': n, 'wrong': sum(r['evaluation']['rare_wrong'] for r in rr) / n,
                    'accuracy': sum(r['evaluation']['rare_accuracy'] for r in rr) / n,
                    'plurality_wrong': sum(r['scripted_evaluation']['rare_wrong'] for r in rr) / n,
                    'seat_share': sum(r['admission']['attacker_seat_share'] for r in rr) / n}
    return out


def header(d, rows, total, stage, elapsed):
    def text(x, y, t, size=23, fill=INK): d.text((x, y), str(t), font=font(size), fill=fill)
    good = sum(r.get('status') == 'completed' for r in rows); failed = sum(r.get('status') == 'failed' for r in rows)
    waiting = sum(r.get('status') == 'not_started' for r in rows)
    text(60, 24, 'Does splitting one attacker into more identities help it?', 40)
    label = 'SCRIPTED PLURALITY RULE - NOT MODEL EVIDENCE' if stage == 'S0' else study.model_name() + ' (' + study.model_config()['backend'] + ')'
    text(60, 82, f'{stage} | {label} | 27 rows, 27 edges, 27 attempts at every identity count | exploratory', 24, ACCENT)
    text(60, 122, f'Completed {good}/{total} | failed {failed} | not started {waiting} | pending {max(0, total - len(rows))} | elapsed {elapsed:.0f}s', 23)
    return text


def comparison(d, text, rows):
    des = study.design(); ks = des['attacker']['identities']; rates = des['attacker']['attacker_pass']
    big, small = max(des['check_budgets']), min(des['check_budgets']); means = cell_means(rows)
    for i, (arm, color) in enumerate(COLORS.items()):
        x = 60 + i * 215; d.line((x, 178, x + 34, 178), fill=color, width=4); text(x + 42, 165, arm.replace('_', ' '), 20, color)
    text(930, 165, f'solid: {big} checks   dashed: {small} checks   hollow squares: plurality, same packets (degree, coverage; {big} checks)', 18, MUTED)
    facets = [(f, r) for f in des['families'] for r in rates]
    for col, (family, rate) in enumerate(facets):
        x = 96 + col * 332; w = 236
        text(x - 30, 210, f'{family} | attacker pass {rate:.0%}', 19)
        # upper row: wrong answers by identity count
        y = 262; h = 232
        for tick in (0, .5, 1):
            yy = y + h * (1 - tick); d.line((x, yy, x + w, yy), fill=GRID, width=1); text(x - 46, yy - 10, f'{tick:.0%}', 16, MUTED)
        for j, k in enumerate(ks): text(x + j * w / (len(ks) - 1) - 6, y + h + 8, k, 17)
        for arm, color in COLORS.items():
            for checks in ([0] if arm == 'no_verification' else [small, big]):
                pts = [(x + j * w / (len(ks) - 1), y + h * (1 - means[(family, rate, arm, checks, k)]['wrong']))
                       if (family, rate, arm, checks, k) in means else None for j, k in enumerate(ks)]
                for a, b in zip(pts, pts[1:]):
                    if a and b: (dashed(d, a, b, color, 3) if checks == small and arm != 'no_verification' else d.line((*a, *b), fill=color, width=4))
                for p in pts:
                    if p: d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=color)
            if arm in ('degree', 'coverage'):
                for j, k in enumerate(ks):
                    m = means.get((family, rate, arm, big, k))
                    if m:
                        px, py = x + j * w / (len(ks) - 1), y + h * (1 - m['plurality_wrong'])
                        d.rectangle((px - 6, py - 6, px + 6, py + 6), outline=color, width=2)
        if col == 0: text(x - 30, y + h + 32, 'identities holding the fixed resources; y: wrong rare-skill answers', 16, MUTED)
        # lower row: accuracy against attacker seat share, one path per policy through k
        y = 612; h = 232; xmax = 0.25
        for tick in (0, .5, 1):
            yy = y + h * (1 - tick); d.line((x, yy, x + w, yy), fill=GRID, width=1); text(x - 46, yy - 10, f'{tick:.0%}', 16, MUTED)
        for tick in (0, .1, .2): text(x + w * tick / xmax - 12, y + h + 8, f'{tick:.0%}', 16, MUTED)
        for arm, color in COLORS.items():
            checks = 0 if arm == 'no_verification' else big; prev = None
            for k in ks:
                m = means.get((family, rate, arm, checks, k))
                if not m: prev = None; continue
                p = (x + w * min(m['seat_share'], xmax) / xmax, y + h * (1 - m['accuracy']))
                if prev: d.line((*prev, *p), fill=color, width=2)
                d.ellipse((p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5), fill=color); text(p[0] + 6, p[1] - 18, k, 14, color); prev = p
        if col == 0: text(x - 30, y + h + 32, f'x: attacker share of the 54 seats; y: rare-skill accuracy; labels: identities ({big} checks)', 16, MUTED)
    counts = [m['n'] for m in means.values()]
    text(60, 902, f'Cells are means over the roots completed so far (per-cell count {min(counts) if counts else 0} to {max(counts) if counts else 0}). A missing cell is not drawn; it is never zero.', 19, MUTED)
    # right strip: per-root paired primary contrast
    rate, checks = min(rates), big
    c = analyze.contrast(analyze.index(rows), analyze.interaction_terms(rate, checks, 'degree', 'coverage'))
    x0, y0, w, h = 1490, 262, 270, 582; lim = 2.0
    text(x0 - 50, 210, 'Primary contrast per root', 19)
    for tick in (-2, -1, 0, 1, 2):
        yy = y0 + h * (lim - tick) / (2 * lim); d.line((x0, yy, x0 + w, yy), fill=INK if tick == 0 else GRID, width=1); text(x0 - 44, yy - 10, f'{tick:+d}', 16, MUTED)
    for i, family in enumerate(des['families']):
        cx = x0 + w * (i + 0.5) / len(des['families']); vals = [p['difference'] for p in c['per_root'] if p['family'] == family and p['difference'] is not None]
        for j, v in enumerate(vals):
            px = cx - 44 + (j * 37 % 89); py = y0 + h * (lim - max(-lim, min(lim, v))) / (2 * lim)
            d.ellipse((px - 5, py - 5, px + 5, py + 5), outline=FAMILY_COLORS.get(family, INK), width=2)
        if vals:
            my = y0 + h * (lim - sum(vals) / len(vals)) / (2 * lim); d.line((cx - 60, my, cx + 60, my), fill=INK, width=4)
        text(cx - 60, y0 + h + 8, f'{family}: {len(vals)} roots', 17, FAMILY_COLORS.get(family, INK))
    text(x0 - 50, y0 + h + 34, '(k=27 minus k=1, degree) minus (same, coverage)', 15, MUTED)
    est = c['estimate']; ci = c['interval']; lo, hi = c['bounds_all_assigned']
    line = 'Primary contrast: no root complete yet' if est is None else \
        f'Primary contrast (wrong answers, attacker passes {rate:.0%}, {checks} checks, families weighted equally): {est:+.3f}' + \
        (f', 95% root bootstrap {ci[0]:+.3f} to {ci[1]:+.3f}' if ci else '')
    text(60, 940, line, 24, ACCENT)
    if lo is not None: text(60, 978, f'Bounds over all assigned roots, missing outcomes at their extremes: {lo:+.3f} to {hi:+.3f}. Useful difference: 0.10. Positive: coverage attenuates splitting harm more than degree.', 19, MUTED)


def qualification_view(d, text, rows, stage):
    q = study.qualification(rows); y = 210
    if stage in ('S0', 'P0'):
        p = study.probe_gate(rows)
        text(80, y, f'Interface probe: {p["count"]} packet, ' + ('answer equals the expected values' if p['passed'] else 'not passed or not finished'), 26); y += 60
    if stage in ('S0', 'Q0'):
        text(80, y, 'Clean qualification packets (no fabricated value anywhere), per shape, both graph families', 24, ACCENT); y += 48
        for c in q['cells']:
            text(80, y, f'{c["shape"]}: {c["count"]}/{c["expected"]} packets | fields {c["fact_accuracy"]:.1%} | exact packets {c["exact_packet_rate"]:.1%} | '
                        f'null on withheld facts {c["missing_abstention"]:.1%} of {c["withheld_fields"]} | ' + ('pass' if c['passed'] else 'not passed'), 23)
            y += 44
        text(80, y + 8, 'Thresholds: all valid, fields >= 95%, exact packets >= 90%, 100% null on withheld facts.', 20, MUTED)
    return y


def frame(rows, total, stage, elapsed=0, accounting=None):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    text = header(d, rows, total, stage, elapsed)
    if stage in ('S0', 'S1'): comparison(d, text, rows)
    else: qualification_view(d, text, rows, stage)
    if stage == 'S0':
        q = study.qualification(rows); p = study.probe_gate(rows)
        text(60, 1016, f'Scripted fixtures: qualification {"passes" if q["passed"] else "not passed or not finished"}; probe fixture {"passes" if p["passed"] else "not passed or not finished"}.', 19, MUTED)
    a = accounting or {}
    cost = sum(r.get('accounting', {}).get('actual_usd', 0) for r in rows)
    tokens_in = sum(r.get('accounting', {}).get('input_tokens', 0) for r in rows); tokens_out = sum(r.get('accounting', {}).get('output_tokens', 0) for r in rows)
    text(60, 1062, f'Stage: {sum(bool(r.get("accounting", {}).get("attempted")) for r in rows)} calls, {tokens_in:,} input and {tokens_out:,} output tokens, ${cost:.4f} | '
                   f'study: {a.get("attempted_calls", 0)} calls, ${a.get("actual_usd", 0):.4f} settled, ${a.get("committed_usd", 0):.2f} against the cap', 21, ACCENT)
    text(60, 1100, 'Simulated identities, graphs and checks; only the synthesis of admitted reports is a model call. Identity counts are not model workers.', 19, MUTED)
    text(60, 1134, 'Replay advances by completed calls in completion order; it shows evidence accumulating, not a process over time.', 19, MUTED)
    return im


def replay(rows, out, stage, total, initial_accounting=None, frames=32):
    terminal = [r for r in rows if r.get('status') != 'not_started']; count = len(terminal)
    cuts = sorted(set([0, count, *[round(count * i / frames) for i in range(1, frames)]]))
    images = []
    for n in cuts:
        prefix = terminal[:n]; last = prefix[-1] if prefix else {}
        images.append(frame(rows if n == count else prefix, total, stage, last.get('elapsed_seconds', 0),
                            last.get('study_accounting') or initial_accounting))
    images[0].save(out / 'initial_frame.png'); images[-1].save(out / 'final_frame.png')
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:],
                   duration=[450] * (len(images) - 1) + [2500], loop=0)
    return len(images)
