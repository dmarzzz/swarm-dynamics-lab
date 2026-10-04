"""Frames from recorded rows only: a compact trust-flow figure (attacker seats by rule and budget
with per-root paired lines), the per-root primary contrast, and the model's answers by cell.
PIL only; 1800x1200; a bounded completion-prefix replay."""
from collections import defaultdict
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

import analyze
import study

W, H = 1800, 1200
BG = '#111b2a'; INK = '#edf3fb'; MUTED = '#a7b5c7'; GRID = '#324153'; ACCENT = '#5fd7d0'
COLORS = {'propagated': '#bb9df6', 'direct': '#5fd7d0', 'anchors': '#f4c777'}
ANSWER = {'rare_correct': '#5fd7d0', 'rare_wrong': '#f08a8a', 'rare_abstain': '#8796aa'}
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc')


@lru_cache(maxsize=32)
def font(size):
    for path in FONT_PATHS:
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    try: return ImageFont.load_default(size)
    except TypeError: return ImageFont.load_default()


def seats_by_root(rows):
    """(attacker_pass, rule) -> task -> {checks: attacker seats}; every recorded attacked row."""
    out = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        if r.get('kind') == 'pilot': out[(r['attacker_pass'], r['rule'])][r['task']][r['checks']] = r['admission']['attacker_seats']
    return out


def answers_by_cell(rows):
    """(kind, attacker_pass, rule, checks) -> mean correct, wrong, abstain over completed rows, and n."""
    g = defaultdict(list)
    for r in rows:
        if r.get('kind') in ('pilot', 'clean') and r.get('status') == 'completed': g[(r['kind'], r['attacker_pass'], r['rule'], r['checks'])].append(r['evaluation'])
    return {k: dict({f: sum(e[f] for e in v) / len(v) for f in ANSWER}, n=len(v)) for k, v in g.items()}


def comparison(d, text, rows, stage):
    des = study.design(); budgets = sorted(des['check_budgets']); rates = sorted(des['attacker_pass']); seats = seats_by_root(rows)
    for i, (rule, color) in enumerate(COLORS.items()):
        x = 60 + i * 230; d.line((x, 178, x + 34, 178), fill=color, width=5); text(x + 42, 165, rule, 21, color)
    text(760, 165, 'thin lines: one root; thick line: mean over recorded roots. Seats come from scripted admission.', 19, MUTED)
    top = 60
    for col, rate in enumerate(rates):
        x0 = 100 + col * 560; y0 = 250; w = 430; h = 330
        text(x0 - 40, 208, f'Attacker seats of 162 | controller passes a check {rate:.0%}', 20)
        for tick in range(0, top + 1, 20):
            yy = y0 + h * (1 - tick / top); d.line((x0, yy, x0 + w, yy), fill=GRID, width=1); text(x0 - 40, yy - 10, tick, 16, MUTED)
        for j, b in enumerate(budgets): text(x0 + j * w / (len(budgets) - 1) - 14, y0 + h + 8, b, 18)
        text(x0 + w / 2 - 60, y0 + h + 34, 'coverage checks', 16, MUTED)
        for rule, color in COLORS.items():
            per = seats[(rate, rule)]
            for task, by in per.items():
                pts = [(x0 + j * w / (len(budgets) - 1), y0 + h * (1 - min(by[b], top) / top)) for j, b in enumerate(budgets) if b in by]
                if len(pts) > 1: d.line([c for p in pts for c in p], fill=color + '', width=1)
            means = [(x0 + j * w / (len(budgets) - 1), y0 + h * (1 - min(m, top) / top)) for j, b in enumerate(budgets)
                     for m in [analyze.mean(by[b] for by in per.values() if b in by)] if m is not None]
            if len(means) > 1: d.line([c for p in means for c in p], fill=color, width=6)
            for p in means: d.ellipse((p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7), fill=color, outline=BG)
    # per-root primary
    x0, y0, w, h = 1290, 250, 440, 330; lim = 60
    p = analyze.analyze(rows)['primary'] if any(r.get('kind') == 'pilot' for r in rows) else {'per_root': [], 'estimate': None, 'interval': None, 'roots': 0, 'positive_roots': 0}
    text(x0 - 50, 208, 'Primary contrast per root (seats)', 20)
    for tick in (-60, -30, 0, 30, 60):
        yy = y0 + h * (lim - tick) / (2 * lim); d.line((x0, yy, x0 + w, yy), fill=INK if tick == 0 else GRID, width=1); text(x0 - 48, yy - 10, f'{tick:+d}', 16, MUTED)
    for j, item in enumerate(p['per_root']):
        px = x0 + 14 + j * (w - 28) / max(1, 23); v = max(-lim, min(lim, item['difference'])); py = y0 + h * (lim - v) / (2 * lim)
        d.line((px, y0 + h / 2, px, py), fill=GRID, width=2); d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=ACCENT)
    if p['estimate'] is not None:
        my = y0 + h * (lim - max(-lim, min(lim, p['estimate']))) / (2 * lim); d.line((x0, my, x0 + w, my), fill=INK, width=3)
    text(x0 - 50, y0 + h + 8, '(propagated 108 - 32) - (direct 108 - 32), strong checks', 16, MUTED)
    line = 'Primary contrast: no root recorded yet' if p['estimate'] is None else (
        f'Primary contrast: {p["estimate"]:+.2f} attacker seats over {p["roots"]} roots'
        + (f', 95% root bootstrap {p["interval"][0]:+.2f} to {p["interval"][1]:+.2f}' if p['interval'] else '')
        + f'; positive in {p["positive_roots"]} roots. Positive: direct credit attenuates the rise with budget.')
    text(60, 650, line, 23, ACCENT)
    # model answers: stacked bars per cell
    ans = answers_by_cell(rows); y0 = 760; h = 190; bw = 26
    text(60, 700, ('Reference-policy answers' if stage == 'S0' else 'Model answers') + ' on the three rare skills (completed rows only): correct / wrong / abstained', 20)
    for i, (f, color) in enumerate(ANSWER.items()):
        d.rectangle((1100 + i * 180, 704, 1120 + i * 180, 724), fill=color); text(1128 + i * 180, 702, f.replace('rare_', ''), 18, color)
    groups = [('pilot', rate) for rate in rates] + [('clean', None)]
    for gi, (kind, rate) in enumerate(groups):
        gx = 100 + gi * 590
        text(gx - 40, y0 - 28, f'controller passes {rate:.0%}' if kind == 'pilot' else f'clean endpoint ({max(budgets)} checks)', 18, MUTED)
        for tick in (0, .5, 1):
            yy = y0 + h * (1 - tick); d.line((gx, yy, gx + 470, yy), fill=GRID, width=1); text(gx - 44, yy - 10, f'{tick:.0%}', 15, MUTED)
        for ri, rule in enumerate(des['rules']):
            for bi, b in enumerate(budgets if kind == 'pilot' else [max(budgets)]):
                x = gx + 14 + ri * 155 + bi * (bw + 14); cell = ans.get((kind, rate, rule, b))
                if cell:
                    y = y0 + h
                    for f, color in ANSWER.items():
                        seg = h * cell[f]; d.rectangle((x, y - seg, x + bw, y), fill=color); y -= seg
                else:
                    d.rectangle((x, y0, x + bw, y0 + h), outline=GRID, width=1)       # nothing completed yet: empty outline, never zero
                text(x - 2, y0 + h + 6, b, 14, MUTED)
            text(gx + 14 + ri * 155, y0 + h + 26, rule, 16, COLORS[rule])


def qualification_view(d, text, rows, stage):
    y = 220
    if stage == 'P0':
        p = study.probe_gate(rows)
        text(80, y, f'Interface probe: {p["count"]} call, ' + ('interface checks passed' if p['passed'] else 'not passed or not finished'), 26); y += 50
        if p['tokens_per_byte']: text(80, y, f'{p["input_tokens"]:,} input tokens for a {p["request_bytes"]:,}-byte request: {p["tokens_per_byte"]:.3f} tokens per byte', 24)
        return
    sets = ('a', 'b') if stage == 'S0' else (study.qualification_set(),)
    for which in sets:
        mine = [r for r in rows if r.get('kind') == 'qualification' and r.get('set') == which]
        q = study.qualification(mine, which)
        text(80, y, f'Qualification set {which}: {len(mine)} fixtures recorded in this run' + (' (the probe row is added to the gate)' if stage == 'Q0' else ''), 24, ACCENT); y += 44
        for shape, c in q['cells'].items():
            text(80, y, f'{shape}: {c["valid"]}/{c["assigned"]} valid | exactly right {c["exact"]} | null on the withheld fact {c["abstained"]}', 23); y += 38
        y += 20
    text(80, y, 'Gate over all 24 fixtures: every structure valid; at least 7 of 8 exactly right in full and in sparse; 8 of 8 null in missing.', 20, MUTED)


def frame(rows, total, stage, elapsed=0, accounting=None):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    def text(x, y, t, size=23, fill=INK): d.text((x, y), str(t), font=font(size), fill=fill)
    good = sum(r.get('status') == 'completed' for r in rows); failed = sum(r.get('status') == 'failed' for r in rows)
    waiting = sum(r.get('status') == 'not_started' for r in rows)
    text(60, 24, 'When verification amplifies capture', 40)
    label = 'SCRIPTED REFERENCE POLICY - NOT MODEL EVIDENCE' if stage == 'S0' else 'qwen/qwen3.7-flash, reasoning disabled'
    text(60, 82, f'{stage} | {label} | 324 scripted identities, one frozen audit, three admission rules | exploratory', 24, ACCENT)
    text(60, 122, f'Completed {good}/{total} | failed {failed} | not started {waiting} | pending {max(0, total - len(rows))} | elapsed {elapsed:.0f}s', 23)
    if stage in ('S0', 'S1'): comparison(d, text, rows, stage)
    else: qualification_view(d, text, rows, stage)
    if stage == 'S0':
        qa, qb = (study.qualification(rows, w)['passed'] for w in ('a', 'b'))
        text(60, 1010, f'Scripted fixtures: set a {"passes" if qa else "not passed or not finished"}; set b {"passes" if qb else "not passed or not finished"}.', 19, MUTED)
    a = accounting or {}
    cost = sum((r.get('accounting') or {}).get('actual_usd', 0) for r in rows)
    tin = sum((r.get('accounting') or {}).get('input_tokens', 0) for r in rows); tout = sum((r.get('accounting') or {}).get('output_tokens', 0) for r in rows)
    text(60, 1062, f'Stage: {sum(bool((r.get("accounting") or {}).get("attempted")) for r in rows)} calls, {tin:,} input and {tout:,} output tokens, ${cost:.4f} | '
                   f'study: {a.get("attempted_calls", 0)} calls, ${a.get("actual_usd", 0):.4f} settled, ${a.get("committed_usd", 0):.4f} against the cap', 21, ACCENT)
    text(60, 1100, 'Identities, graph and checks are scripted; only the synthesis of the admitted packet is a model call. A missing cell is drawn empty, never as zero.', 19, MUTED)
    text(60, 1134, 'Replay advances by recorded calls in completion order; it shows evidence accumulating, not a process over time.', 19, MUTED)
    return im


def replay(rows, out, stage, total, initial_accounting=None, frames=10):
    terminal = sorted((r for r in rows if r.get('status') != 'not_started'), key=lambda r: (r.get('run', ''), r.get('completion_index', 0)))
    count = len(terminal)
    cuts = sorted(set([0, count, *[round(count * i / frames) for i in range(1, frames)]]))
    images = []
    for n in cuts:
        prefix = terminal[:n]; last = prefix[-1] if prefix else {}
        images.append(frame(rows if n == count else prefix, total, stage, last.get('elapsed_seconds', 0), last.get('study_accounting') or initial_accounting))
    images[0].save(out / 'initial_frame.png'); images[-1].save(out / 'final_frame.png')
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:], duration=[500] * (len(images) - 1) + [2500], loop=0)
    return len(images)
