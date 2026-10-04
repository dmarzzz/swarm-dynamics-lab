"""Measured frames for verify-cost-qwen (PIL only): the regret and cost panel.

  top left      mean expected regret per case (4 error probabilities x 3 UNKNOWN costs), prose and table,
                with the optimal-choice count of each cell and the optimal action of the case
  top right     the 24 layout-level table-minus-prose values (the primary measure), their mean and interval
  bottom left   per case: regret with prose and with table against the offline comparators
  bottom right  calls, tokens, dollars, failures by category, billing pauses, qualification fixtures

Rendering reads recorded rows only. A cell or layout without a valid answer is drawn as missing; a
layout with missing units is drawn as its bounds, never as a point.
"""
import functools

from PIL import Image, ImageDraw, ImageFont

import analyze
import study

SIZE = (1800, 1200)
BG, INK, MUTED, GRID, BAD, GOOD, WARN = '#111b2a', '#edf3fb', '#a7b5c7', '#324153', '#ff8f8f', '#7fd6a2', '#f4c777'
REP = {'prose': '#f4c777', 'table': '#5fd7d0'}
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc')


@functools.lru_cache(maxsize=64)
def font(size):
    for path in FONT_PATHS:
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    try: return ImageFont.load_default(size)      # Pillow >= 10.1: scalable built-in font
    except TypeError: return ImageFont.load_default()


def shade(share):
    """0 (no regret) dark green to 1 (the worst action every time) red."""
    share = max(0.0, min(1.0, share)); lo, hi = (38, 92, 74), (176, 62, 62)
    return tuple(round(a + (b - a) * share) for a, b in zip(lo, hi))


def heatmaps(d, a, x0, y0):
    design = study.design(); es, us = design['error_probabilities'], design['unknown_costs']
    cw, ch = 118, 86
    d.text((x0, y0), 'Mean expected regret per case (optimal choices / valid)', font=font(24), fill=INK)
    cells = {(c['error'], c['unknown_cost'], c['representation']): c for c in a.get('cells', [])}
    strata = {(s['error'], s['unknown_cost']): s for s in a.get('strata', [])}
    for k, rep in enumerate(study.REPRESENTATIONS):
        gx = x0 + 96 + k * (3 * cw + 110); gy = y0 + 78
        d.text((gx, gy - 36), rep, font=font(24), fill=REP[rep])
        for j, u in enumerate(us): d.text((gx + j * cw + 14, gy + 4 * ch + 6), f'U {u:.2f}', font=font(18), fill=MUTED)
        for i, e in enumerate(es):
            if k == 0: d.text((x0, gy + i * ch + 30), f'e {e:.2f}', font=font(18), fill=MUTED)
            for j, u in enumerate(us):
                c = cells.get((e, u, rep)); s = strata.get((e, u)); box = (gx + j * cw, gy + i * ch, gx + (j + 1) * cw - 6, gy + (i + 1) * ch - 6)
                if not c or not c['valid']:
                    d.rectangle(box, fill='#1b2636', outline=GRID)
                    for t in range(0, cw + ch, 14): d.line((box[0] + t, box[1], box[0] + t - ch, box[3]), fill=GRID)
                    d.text((box[0] + 8, box[1] + 28), 'no valid answer' if c else 'not assigned', font=font(13), fill=MUTED)
                    continue
                d.rectangle(box, fill=shade(c['mean_regret'] / s['margin']), outline=GRID)
                d.text((box[0] + 8, box[1] + 8), f'{c["mean_regret"]:.3f}', font=font(22), fill=INK)
                d.text((box[0] + 8, box[1] + 38), f'{c["optimal"]}/{c["valid"]} {s["optimal_action"]}', font=font(15), fill=INK)
                missing = c['assigned'] - c['valid']
                if missing: d.text((box[0] + 8, box[1] + 58), f'{missing} missing', font=font(13), fill=BAD)


def layout_panel(d, a, x0, y0, w, h):
    p = a.get('primary'); d.text((x0, y0), 'Table minus prose expected regret, per layout', font=font(24), fill=INK)
    top, bottom, left = y0 + 60, y0 + h - 70, x0 + 70
    span = max(0.05, (p or {}).get('largest_possible') or 0.32)
    y = lambda v: (top + bottom) / 2 - v / span * (bottom - top) / 2
    d.rectangle((left, top, x0 + w, bottom), outline=GRID)
    for v in (-span, 0, span):
        d.line((left, y(v), x0 + w, y(v)), fill=GRID if v else MUTED); d.text((x0, y(v) - 10), f'{v:+.2f}', font=font(16), fill=MUTED)
    rows = a.get('layouts') or []
    if not rows:
        d.text((left + 20, top + 20), 'no grid units in this stage', font=font(18), fill=MUTED); return
    step = (w - 90) / max(1, len(rows))
    for i, r in enumerate(rows):
        x = left + 16 + i * step
        if r['complete']:
            d.ellipse((x - 6, y(r['value']) - 6, x + 6, y(r['value']) + 6), fill=REP['table'] if r['value'] < 0 else REP['prose'] if r['value'] > 0 else MUTED)
        elif r['assigned']:
            d.line((x, y(r['bounds'][0]), x, y(r['bounds'][1])), fill=BAD, width=3)
    if p and p['estimate'] is not None:
        d.line((left, y(p['estimate']), x0 + w, y(p['estimate'])), fill=INK, width=2)
        text = f'mean {p["estimate"]:+.4f} over {p["layouts"]} of {p["assigned_layouts"]} layouts'
        if p['interval95']: text += f'; 95% interval {p["interval95"][0]:+.4f} to {p["interval95"][1]:+.4f}'
        d.text((left, bottom + 10), text, font=font(18), fill=INK)
    if p:
        d.text((left, bottom + 36), f'bounds over all assigned layouts {p["bounds_all_assigned"][0]:+.4f} to {p["bounds_all_assigned"][1]:+.4f}; '
                                    f'below zero favours the table; red bar: missing units', font=font(15), fill=MUTED)


def strata_panel(d, a, x0, y0, w, h):
    d.text((x0, y0), 'Regret per case: prose, table and the offline comparators', font=font(24), fill=INK)
    strata = a.get('strata') or []
    top, bottom, left = y0 + 54, y0 + h - 64, x0 + 60
    d.rectangle((left, top, x0 + w, bottom), outline=GRID)
    scale = 0.75; y = lambda v: bottom - min(v, scale) / scale * (bottom - top)
    for v in (0.25, 0.5, 0.75):
        d.line((left, y(v), x0 + w, y(v)), fill=GRID); d.text((x0, y(v) - 10), f'{v:.2f}', font=font(16), fill=MUTED)
    step = (w - 70) / max(1, len(strata))
    for i, s in enumerate(strata):
        x = left + 10 + i * step
        for k, rep in enumerate(study.REPRESENTATIONS):
            v = s[rep]['mean_regret']
            if v is None:
                d.text((x + k * 24, bottom - 22), '?', font=font(18), fill=BAD); continue
            d.rectangle((x + k * 24, y(v), x + k * 24 + 20, bottom), fill=REP[rep])
        for key, colour in (('always_check_regret', INK), ('always_explore_regret', BAD)):
            if s[key] > 0: d.line((x - 4, y(s[key]), x + 50, y(s[key])), fill=colour, width=3)
        d.text((x - 4, bottom + 6), f'e{s["error"]:.2f}', font=font(13), fill=MUTED)
        d.text((x - 4, bottom + 22), f'U{s["unknown_cost"]:.2f}', font=font(13), fill=MUTED)
        if s['regression']: d.text((x, top + 4), 'R', font=font(18), fill=BAD)
    d.text((left, bottom + 42), 'bars: prose (amber), table (teal). lines: regret of always-check (white) and always-explore (red) where it is wrong. '
                                'R: reliable-source regression flag', font=font(14), fill=MUTED)


def cost_panel(d, rows, a, total, stage, elapsed, accounting, x0, y0):
    count = lambda s: sum(r['status'] == s for r in rows)
    acct = [r.get('accounting') or {} for r in rows]
    lines = [(f'{stage}: {count("completed")} valid of {total} assigned; {count("failed")} failed; {count("not_started")} not started;'
              f' {total - len(rows)} pending', INK),
             (f'calls {sum(bool(x.get("attempted")) for x in acct)}; transport attempts {sum(x.get("attempts", 0) for x in acct)}; '
              f'input tokens {sum(x.get("input_tokens", 0) for x in acct):,}; output tokens {sum(x.get("output_tokens", 0) for x in acct):,}', INK),
             (f'stage cost USD {sum(x.get("actual_usd", 0) for x in acct):.6f}; study committed USD {(accounting or {}).get("committed_usd", 0):.6f} '
              f'of cap {(accounting or {}).get("cap_usd", study.design()["budget"]["aggregate_usd"])}; elapsed {elapsed:.0f} s', INK)]
    comp = a.get('comparators') or {}; reps = a.get('representations') or {}
    if reps:
        lines.append(('mean regret: ' + ', '.join(f'{rep} {reps[rep]["mean_regret"]:.4f}' if reps[rep]['mean_regret'] is not None else f'{rep} n/a'
                                                 for rep in study.REPRESENTATIONS)
                      + f'; always-check {comp["always_check"]:.4f}; always-explore {comp["always_explore"]:.4f}; analytic 0', INK))
        rs = a['reliable_source']
        lines.append((f'reliable-source strata (e <= 0.20): worst optimal-count change table minus prose {rs["worst_optimal_table_minus_prose"]}; '
                      f'flagged {len(rs["flagged"])}', BAD if rs['flagged'] else MUTED))
    wk = (a.get('work') or {}).get('all')
    if wk and wk['checked']:
        lines.append((f'written costs: both present {wk["both_written"]}/{wk["checked"]}, both correct {wk["both_correct"]}; '
                      f'choice against own numbers {wk["choice_contradicts_own_costs"]}; malformed {wk["work_malformed"]} (reported, not graded)', MUTED))
    f = a.get('failures') or {}
    if f.get('units_without_a_valid_answer'):
        lines.append(('without a valid answer: ' + ', '.join(f'{k} {v}' for k, v in f['by_category'].items()), BAD))
    for i, (text, colour) in enumerate(lines): d.text((x0, y0 + i * 30), text[:150], font=font(18), fill=colour)
    # qualification fixtures: one square per fixture and representation
    q = [r for r in rows if r['kind'] == 'qualification']
    if q:
        y = y0 + len(lines) * 30 + 14
        d.text((x0, y), 'qualification fixtures (green optimal, red not optimal, grey no valid answer)', font=font(16), fill=MUTED)
        for i, r in enumerate(sorted(q, key=lambda r: (str(r['set']), r['representation'], r['layout']))):
            colour = GRID if r['status'] != 'completed' else GOOD if r['evaluation']['optimal'] else BAD
            d.rectangle((x0 + (i % 24) * 30, y + 28 + (i // 24) * 30, x0 + (i % 24) * 30 + 24, y + 52 + (i // 24) * 30), fill=colour)


def frame(rows, total, stage, elapsed=0, accounting=None):
    """One 1800x1200 frame from the rows recorded so far."""
    a = analyze.analyze(rows) if rows else {'cells': []}
    im = Image.new('RGB', SIZE, BG); d = ImageDraw.Draw(im)
    d.text((40, 24), f'verify-cost-qwen  {stage}: when is verification worth its cost? One-step choice, prose against table',
           font=font(28), fill=INK)
    d.text((40, 62), f'model {study.model()} (answer: {study.schema().replace("_", " ")}). check = inspect the reported cell (loss U); '
                     'explore = inspect the cell without evidence (expected loss e). Scripted consequences; exploratory.', font=font(17), fill=MUTED)
    heatmaps(d, a, 40, 110)
    layout_panel(d, a, 960, 110, 800, 500)
    strata_panel(d, a, 40, 640, 860, 380)
    cost_panel(d, rows, a, total, stage, elapsed, accounting, 960, 640)
    return im


def replay(rows, total, out, stage, frames=8):
    """A bounded completion-prefix replay: the frame after each eighth of the recorded units."""
    ordered = sorted(rows, key=lambda r: (r.get('batch', ''), r.get('completion_index', 0)))
    cuts = sorted({max(1, round(len(ordered) * k / frames)) for k in range(1, frames + 1)}) if ordered else []
    images = [frame(ordered[:n], total, stage).resize((900, 600)).convert('P', palette=Image.ADAPTIVE, colors=64) for n in cuts]
    if not images: images = [frame([], total, stage).resize((900, 600)).convert('P', palette=Image.ADAPTIVE, colors=64)]
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:], duration=700, loop=0, optimize=True)
    return len(images)
