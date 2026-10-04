"""Frames from recorded rows only: specialist accuracy against truthful carriers per rare fact, one
panel per auditing policy and check strength, one line per check count, with the parent's
(claude-opus-5-5) primary-cell curve on the same packets as a dashed reference; the qualification
table for P0 and Q0. PIL only; 1800x1200; a bounded completion-prefix replay."""
from collections import defaultdict
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

import analyze
import study

W, H = 1800, 1200
BG = '#101826'; INK = '#eef3fa'; MUTED = '#a3b1c4'; GRID = '#2e3b4e'; ACCENT = '#5fd7d0'; PARENT = '#f4c777'
CHECKS = {4: '#8796aa', 64: '#bb9df6', 108: '#5fd7d0'}
CARRIERS = (1, 3, 9, 27, 81)
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc')


@lru_cache(maxsize=32)
def font(size):
    for path in FONT_PATHS:
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    try: return ImageFont.load_default(size)
    except TypeError: return ImageFont.load_default()


def accuracy_by_cell(rows):
    g = defaultdict(list)
    for r in rows:
        if r.get('kind') == 'pilot' and r.get('status') == 'completed':
            g[(r['arm'], r['attacker_pass'], r['checks'], r['carriers'])].append(r['evaluation']['rare_accuracy'])
    return {k: (sum(v) / len(v), len(v)) for k, v in g.items()}


def grid_view(d, text, rows, stage, parent_curve):
    acc = accuracy_by_cell(rows)
    panels = [(arm, rate) for arm in ('random', 'coverage') for rate in (0.1, 0.9)]
    for i, (checks, color) in enumerate(CHECKS.items()):
        d.line((60 + i * 190, 182, 94 + i * 190, 182), fill=color, width=5); text(102 + i * 190, 170, f'{checks} checks', 20, color)
    if parent_curve:
        d.line((660, 182, 694, 182), fill=PARENT, width=3); text(702, 170, 'Opus 5.5 (parent), random, 108 checks, pass 10%, same packets', 20, PARENT)
    for p, (arm, rate) in enumerate(panels):
        x0 = 110 + p * 420; y0 = 260; w = 330; h = 420
        text(x0 - 20, 222, f'{arm} auditing | attacker passes {rate:.0%}', 20)
        for tick in (0, .25, .5, .75, 1):
            yy = y0 + h * (1 - tick); d.line((x0, yy, x0 + w, yy), fill=GRID, width=1); text(x0 - 56, yy - 10, f'{tick:.0%}', 16, MUTED)
        xs = {c: x0 + j * w / (len(CARRIERS) - 1) for j, c in enumerate(CARRIERS)}
        for c, x in xs.items(): text(x - 10, y0 + h + 8, c, 18)
        text(x0 + w / 2 - 110, y0 + h + 34, 'truthful carriers per rare fact', 16, MUTED)
        if (arm, rate) == ('random', 0.1) and parent_curve:
            pts = [(xs[c], y0 + h * (1 - parent_curve[c])) for c in CARRIERS if c in parent_curve]
            for a, b in zip(pts, pts[1:]):
                for s in range(0, 10, 2):
                    d.line((a[0] + (b[0] - a[0]) * s / 10, a[1] + (b[1] - a[1]) * s / 10,
                            a[0] + (b[0] - a[0]) * (s + 1) / 10, a[1] + (b[1] - a[1]) * (s + 1) / 10), fill=PARENT, width=3)
        for checks, color in CHECKS.items():
            pts = [(xs[c], y0 + h * (1 - acc[(arm, rate, checks, c)][0])) for c in CARRIERS if (arm, rate, checks, c) in acc]
            if len(pts) > 1: d.line([v for p_ in pts for v in p_], fill=color, width=4)
            for q in pts: d.ellipse((q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6), fill=color, outline=BG)
    a = analyze.analyze(rows) if any(r.get('kind') == 'pilot' for r in rows) else None
    pr = a['primary'] if a else None
    line = ('Primary (random, 108 checks, pass 10%, 1 minus 81 carriers): no root complete yet' if not pr or pr['estimate_pp'] is None else
            f'Primary (random, 108 checks, pass 10%, 1 minus 81 carriers): {pr["estimate_pp"]:+.1f} pp over {pr["complete_roots"]} of '
            f'{pr["assigned_roots"]} roots' + (f', 95% root bootstrap {pr["interval_pp"][0]:+.1f} to {pr["interval_pp"][1]:+.1f}' if pr['interval_pp'] else '')
            + (f'; bounds {pr["bounds_pp"][0]:+.1f} to {pr["bounds_pp"][1]:+.1f}' if pr['bounds_pp'] else ''))
    text(60, 760, line, 23, ACCENT)
    vp = (a or {}).get('versus_parent') or {}
    if vp.get('parent_primary_pp') is not None:
        text(60, 800, f'Parent on the same packets (claude-opus-5-5): {vp["parent_primary_pp"]:+.1f} pp. Models are compared root by root, never pooled.', 20, PARENT)
    text(60, 840, 'Specialist accuracy = rare facts answered exactly right / 3; null and wrong both count as incorrect. A cell with no completed call is not drawn.', 18, MUTED)


def qualification_view(d, text, rows, stage):
    y = 220
    if stage == 'P0':
        p = study.probe_gate(rows)
        text(80, y, f'Interface probe: {p["count"]} call, ' + ('interface checks passed' if p['passed'] else 'not passed or not finished')
             + (', answer exactly right' if p['exact'] else ''), 26); y += 50
        if p['tokens_per_byte']: text(80, y, f'{p["input_tokens"]:,} input tokens for a {p["request_bytes"]:,}-byte request: {p["tokens_per_byte"]:.3f} tokens per byte', 24)
        return
    q = study.qualification(rows)
    text(80, y, f'Clean qualification: {sum(r.get("kind") == "qualification" for r in rows)} of {q["packets"]} packets recorded, {q["structurally_valid"]} valid', 24, ACCENT); y += 50
    for g in q['groups']:
        text(80, y, f'{g["carriers"]} carrier(s): {g["valid"]}/{g["expected"]} valid | field accuracy {g["fact_accuracy"]:.3f} (>= 0.95) | exact {g["exact_packet_rate"]:.3f} (>= 0.90) | '
                    f'null on withheld {g["withheld_abstained"]}/{g["withheld_fields"]} | ' + ('passes' if g['passed'] else 'not passed'), 22); y += 40
    text(80, y + 20, "The parent's thresholds, unchanged. A failed qualification ends this model's chain and is reported.", 20, MUTED)


def frame(rows, total, stage, elapsed=0, accounting=None, parent_curve=None):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    def text(x, y, t, size=23, fill=INK): d.text((x, y), str(t), font=font(size), fill=fill)
    good = sum(r.get('status') == 'completed' for r in rows); failed = sum(r.get('status') == 'failed' for r in rows)
    waiting = sum(r.get('status') == 'not_started' for r in rows)
    text(60, 24, 'Does Sybil-resistant accuracy depend on repeated knowledge? Cross-model replication', 34)
    label = 'SCRIPTED PLURALITY RULE - NOT MODEL EVIDENCE' if stage == 'S0' else f'{study.model()} ({study.spec()["api"]})'
    text(60, 76, f'{stage} | {label} | packets identical to sybil-scarcity-opus | 972 simulated identities | exploratory', 22, ACCENT)
    text(60, 116, f'Completed {good}/{total} | failed {failed} | not started {waiting} | pending {max(0, total - len(rows))} | elapsed {elapsed:.0f}s', 22)
    if stage in ('S0', 'S1'): grid_view(d, text, rows, stage, parent_curve if stage == 'S1' else None)
    else: qualification_view(d, text, rows, stage)
    a = accounting or {}
    cost = sum((r.get('accounting') or {}).get('actual_usd', 0) for r in rows)
    tin = sum((r.get('accounting') or {}).get('input_tokens', 0) for r in rows); tout = sum((r.get('accounting') or {}).get('output_tokens', 0) for r in rows)
    text(60, 1062, f'Stage: {sum(bool((r.get("accounting") or {}).get("attempted")) for r in rows)} calls, {tin:,} input and {tout:,} output tokens, ${cost:.4f} | '
                   f'study ({study.tag()}): {a.get("attempted_calls", 0)} calls, ${a.get("actual_usd", 0):.4f} settled, ${a.get("committed_usd", 0):.4f} against the cap', 20, ACCENT)
    text(60, 1100, 'Identities, graph, audits and admission are scripted; only the synthesis of the admitted packet is a model call.', 19, MUTED)
    text(60, 1134, 'Replay advances by recorded calls in completion order; it shows evidence accumulating, not a process over time.', 19, MUTED)
    return im


def parent_primary_curve():
    """Opus 5.5's specialist accuracy in the primary cell by carriers, from the pinned parent rows."""
    parent = analyze.parent_rows()
    if not parent: return None
    pc = study.design()['primary_contrast']; g = defaultdict(list)
    for r in parent.values():
        if (r.get('status') == 'completed' and r['arm'] == pc['arm'] and r['checks'] == pc['checks']
                and r['attacker_pass'] == pc['attacker_pass']):
            g[r['carriers']].append(r['evaluation']['rare_accuracy'])
    return {c: sum(v) / len(v) for c, v in g.items()}


def replay(rows, out, stage, total, initial_accounting=None, frames=10):
    terminal = sorted((r for r in rows if r.get('status') != 'not_started'), key=lambda r: (r.get('run', ''), r.get('completion_index', 0)))
    count = len(terminal); curve = parent_primary_curve() if stage == 'S1' else None
    cuts = sorted(set([0, count, *[round(count * i / frames) for i in range(1, frames)]]))
    images = []
    for n in cuts:
        prefix = terminal[:n]; last = prefix[-1] if prefix else {}
        images.append(frame(rows if n == count else prefix, total, stage, last.get('elapsed_seconds', 0),
                            last.get('study_accounting') or initial_accounting, curve))
    images[0].save(out / 'initial_frame.png'); images[-1].save(out / 'final_frame.png')
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:], duration=[500] * (len(images) - 1) + [2500], loop=0)
    return len(images)
