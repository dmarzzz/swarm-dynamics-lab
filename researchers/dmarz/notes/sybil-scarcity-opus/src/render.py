"""Measured frames for the scarcity study (PIL only): accuracy against carrier count, truth
availability, cell counts and an invariance panel; plus a bounded completion-prefix replay.

Rendering reads recorded rows only. It never draws a value for a cell without a completed row.
"""
import functools
from collections import defaultdict

from PIL import Image, ImageDraw, ImageFont

import analyze
import study

SIZE = (1800, 1200)
COLORS = {'random': '#f4c777', 'coverage': '#5fd7d0'}
BG, INK, MUTED, GRID, BAD = '#111b2a', '#edf3fb', '#a7b5c7', '#324153', '#ff8f8f'
STYLE = {4: (3, 9), 64: (14, 9), 108: None}          # dotted, dashed, solid
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf',
              '/Library/Fonts/Arial.ttf',
              '/System/Library/Fonts/Helvetica.ttc')


@functools.lru_cache(maxsize=64)
def font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size)      # Pillow >= 10.1: scalable built-in font
    except TypeError:
        return ImageFont.load_default()


def _line(d, a, b, color, pattern, width=4):
    if pattern is None:
        d.line((*a, *b), fill=color, width=width)
        return
    dash, gap = pattern
    length = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** .5
    if length == 0:
        return
    t = 0.0
    while t < length:
        u = min(t + dash, length)
        d.line((a[0] + (b[0] - a[0]) * t / length, a[1] + (b[1] - a[1]) * t / length,
                a[0] + (b[0] - a[0]) * u / length, a[1] + (b[1] - a[1]) * u / length), fill=color, width=width)
        t += dash + gap


def _aggregate(rows):
    """Per cell: assigned and valid counts, model accuracy over valid rows, diagnostics over assigned rows."""
    cells = defaultdict(lambda: {'assigned': 0, 'valid': 0, 'failed': 0, 'accuracy': [], 'scripted': [],
                                 'truth': [], 'attacker': []})
    for r in rows:
        if r['kind'] != 'pilot':
            continue
        c = cells[analyze.cell_key(r)]
        c['assigned'] += 1
        c['truth'].append(r['diagnostics']['truth_available'])
        c['attacker'].append(r['diagnostics']['attacker_seat_share'])
        c['scripted'].append(r['scripted_evaluation']['rare_accuracy'])
        if r['status'] == 'completed':
            c['valid'] += 1
            c['accuracy'].append(r['evaluation']['rare_accuracy'])
        elif r['status'] == 'failed':
            c['failed'] += 1
    return cells


def frame(rows, total, stage, elapsed=0, accounting=None):
    """One 1800x1200 frame from the rows recorded so far. Model accuracy uses completed rows only;
    evaluator-side panels (truth availability, attacker share, plurality) use every recorded row."""
    d = study.design()
    im = Image.new('RGB', SIZE, BG)
    dr = ImageDraw.Draw(im)

    def text(x, y, t, size=22, fill=INK):
        dr.text((x, y), str(t), font=font(size), fill=fill)

    good = [r for r in rows if r['status'] == 'completed']
    failed = sum(r['status'] == 'failed' for r in rows)
    not_started = sum(r['status'] == 'not_started' for r in rows)
    label = {'S0': 'SCRIPTED - NOT MODEL EVIDENCE', 'P0': 'OPUS 5.5 interface probe, one call',
             'Q0': 'OPUS 5.5 clean qualification', 'S1': 'OPUS 5.5, effort low'}[stage]
    text(60, 22, 'Does Sybil-resistant accuracy depend on repeated knowledge?', 40)
    text(60, 78, f'{stage} | {label} | 972 simulated identities, 486 admitted reports | exploratory', 24, COLORS['coverage'])
    text(60, 114, f'Completed {len(good)}/{total} | failed {failed} | not started {not_started} | pending {total - len(rows)} | elapsed {elapsed:.0f}s', 23)

    pilot = [r for r in rows if r['kind'] == 'pilot']
    if stage == 'P0':
        _probe(text, rows)
    elif stage == 'Q0':
        _qualification(text, rows, 190)
    if stage in ('S0', 'S1'):
        _grid(dr, text, rows, pilot, d, 'scripted answer' if stage == 'S0' else 'model answer')
        if stage == 'S0':
            _qualification(text, rows, 1022, compact=True)

    a = accounting or {}
    stage_cost = sum(r.get('accounting', {}).get('actual_usd', 0) for r in rows)
    text(60, 1080, f'Stage cost ${stage_cost:.4f} | study settled ${a.get("actual_usd", 0):.4f} | committed ${a.get("committed_usd", 0):.2f} of ${d["budget"]["aggregate_usd"]} cap | calls {a.get("attempted_calls", 0)}/{d["budget"]["max_attempted_calls"]}', 21, COLORS['coverage'])
    text(60, 1113, 'Cells without a completed row show no point: pending or failed, never zero. Lower panels and seat share are evaluator-side.', 20, MUTED)
    text(60, 1144, 'Simulated identities, reports and checks; one model synthesis per packet. Replay follows completed calls, not agent conversations.', 20, MUTED)
    return im


def _probe(text, rows):
    text(90, 220, 'Interface probe: one clean packet from engineering root 7790 (81 carriers, all six facts present).', 26)
    if not rows:
        text(90, 280, 'Pending: no call recorded.', 26, MUTED)
        return
    r = rows[0]
    if r['status'] != 'completed':
        text(90, 280, f'FAILED: {r.get("error", r["status"])}', 30, BAD)
        return
    e, acc = r['evaluation'], r.get('accounting', {})
    text(90, 280, f'Answer parsed; {e["fields_matched"]}/6 values equal the expected values; exact packet: {e["exact_packet"]}', 28,
         INK if e['exact_packet'] else BAD)
    text(90, 330, f'Input tokens {acc.get("input_tokens")} (counted {acc.get("counted_input_tokens")}) | output tokens {acc.get("output_tokens")} | latency {acc.get("latency_seconds", 0):.1f}s | cost ${acc.get("actual_usd", 0):.4f}', 26)


def _qualification(text, rows, y, compact=False):
    q = study.qualification(rows)
    size = 20 if compact else 27
    step = 26 if compact else 120
    if compact:
        text(60, y, f'Clean fixtures, scripted plurality: {q["structurally_valid"]}/{q["packets"]} valid | ' + ' | '.join(
            f'c={g["carriers"]}: {g["exact_packets"]}/{g["valid"]} exact, {g["withheld_abstained"]}/{g["withheld_fields"]} abstain'
            for g in q['groups']), size, INK if q['passed'] else MUTED)
        return
    text(90, y, f'Clean packets of 486 truthful reports: {q["structurally_valid"]}/{q["packets"]} structurally valid.  Gate: {"PASS" if q["passed"] else "not passed"}', size + 2)
    for i, g in enumerate(q['groups']):
        yy = y + 80 + i * step
        text(90, yy, f'{g["carriers"]} carrier(s) per rare fact: {g["valid"]}/{g["expected"]} packets', size)
        text(90, yy + 44, f'Fields {g["fields_matched"]}/{g["fields"]} ({g["fact_accuracy"]:.1%}, need 95%) | exact packets {g["exact_packets"]}/{g["valid"]} ({g["exact_packet_rate"]:.1%}, need 90%) | withheld-fact abstention {g["withheld_abstained"]}/{g["withheld_fields"]} (need all)',
             size - 4, INK if g['passed'] else MUTED)


def _grid(dr, text, rows, pilot, d, answer_label):
    cells = _aggregate(rows)
    carriers, checks_list, rates, arms = d['carriers'], d['audit_checks'], d['attacker_pass'], d['arms']
    p = d['primary_contrast']

    # Primary contrast line.
    grouped = defaultdict(list)
    for r in pilot:
        grouped[analyze.cell_key(r)].append(r)
    primary = analyze.combo(grouped, [(1, (min(carriers), p['checks'], p['attacker_pass'], p['arm'])),
                                      (-1, (max(carriers), p['checks'], p['attacker_pass'], p['arm']))]) if pilot else None
    head = f'Primary ({p["arm"]}, {p["checks"]} checks, pass {p["attacker_pass"]:.0%}): 1 carrier minus 81 carriers = '
    if not primary or not primary['roots']:
        text(60, 150, head + 'pending', 23, MUTED)
    elif primary['mean'] is not None:
        lo, hi = primary['interval']
        text(60, 150, head + f'{primary["mean"] * 100:+.1f} pp, root bootstrap 95% [{lo * 100:+.1f}, {hi * 100:+.1f}], {primary["roots"]} roots', 23)
    else:
        lo, hi = primary['all_assigned_bounds']
        text(60, 150, head + f'incomplete: {primary["complete_roots"]}/{primary["roots"]} roots; all-assigned bounds [{lo * 100:+.1f}, {hi * 100:+.1f}] pp', 23, MUTED)

    # Legend.
    x = 60
    for arm in arms:
        dr.line((x, 205, x + 40, 205), fill=COLORS[arm], width=5)
        text(x + 50, 192, arm, 21, COLORS[arm])
        x += 190
    for checks in checks_list:
        _line(dr, (x, 205), (x + 60, 205), INK, STYLE[checks])
        text(x + 70, 192, f'{checks} checks', 21)
        x += 215
    dr.rectangle((x, 198, x + 13, 211), outline=INK, width=2)
    text(x + 24, 192, 'squares: plurality on the same packets (108 checks)', 21, MUTED)

    width, height = 520, 260
    xs = lambda x0, j: x0 + 30 + j * (width - 60) / (len(carriers) - 1)
    for col, rate in enumerate(rates):
        x0 = 110 + col * 620
        for row, (title, field) in enumerate(((f'Specialist accuracy ({answer_label})', 'accuracy'),
                                              ('Rare facts with a truthful carrier admitted', 'truth'))):
            y0 = 290 + row * 384
            text(x0 - 50, y0 - 44, f'{title} | check-pass {rate:.0%}', 20)
            for tick in (0, .25, .5, .75, 1):
                yy = y0 + height * (1 - tick)
                dr.line((x0, yy, x0 + width, yy), fill=GRID, width=1)
                text(x0 - 58, yy - 11, f'{tick:.0%}', 17, MUTED)
            for j, c in enumerate(carriers):
                text(xs(x0, j) - 9, y0 + height + 10, c, 19)
            text(x0, y0 + height + 38, 'truthful carriers per rare fact (log-spaced)', 17, MUTED)
            for arm in arms:
                for checks in checks_list:
                    points = []
                    for j, c in enumerate(carriers):
                        cell = cells.get((c, checks, rate, arm))
                        values = cell[field] if cell else []
                        points.append((xs(x0, j), y0 + height * (1 - sum(values) / len(values))) if values else None)
                    for a, b in zip(points, points[1:]):
                        if a and b:
                            _line(dr, a, b, COLORS[arm], STYLE[checks])
                    for pt in points:
                        if pt:
                            dr.ellipse((pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5), fill=COLORS[arm])
                if field == 'accuracy':
                    for j, c in enumerate(carriers):
                        cell = cells.get((c, max(checks_list), rate, arm))
                        if cell and cell['valid'] == cell['assigned'] >= 8:
                            lo, hi = analyze.interval(cell['accuracy'])
                            xx = xs(x0, j) + (-7 if arm == arms[0] else 7)
                            dr.line((xx, y0 + height * (1 - lo), xx, y0 + height * (1 - hi)), fill=COLORS[arm], width=2)
                        if cell and cell['valid']:
                            v = sum(cell['scripted']) / len(cell['scripted'])
                            dr.rectangle((xs(x0, j) - 7, y0 + height * (1 - v) - 7, xs(x0, j) + 7, y0 + height * (1 - v) + 7),
                                         outline=COLORS[arm], width=2)

    # Cell counts: valid / assigned roots for all 60 cells.
    tx, ty = 1350, 246
    text(tx, ty, 'Valid / assigned roots per cell', 20)
    text(tx, ty + 30, 'policy checks pass', 16, MUTED)
    for j, c in enumerate(carriers):
        text(tx + 190 + j * 50, ty + 30, f'c={c}', 16, MUTED)
    line = 0
    for arm in arms:
        for checks in checks_list:
            for rate in rates:
                yy = ty + 56 + line * 23
                text(tx, yy, f'{arm[:4]} {checks:>3} {rate:.0%}', 16, COLORS[arm])
                for j, c in enumerate(carriers):
                    cell = cells.get((c, checks, rate, arm))
                    if not cell:
                        text(tx + 190 + j * 50, yy, '-', 16, MUTED)
                    else:
                        color = BAD if cell['failed'] else INK if cell['valid'] == cell['assigned'] else MUTED
                        text(tx + 190 + j * 50, yy, f'{cell["valid"]}/{cell["assigned"]}', 16, color)
                line += 1

    # Invariance: attacker seat share must not move with the carrier count.
    ix, iy, iw, ih = 1390, 674, 350, 260
    text(ix - 40, iy - 44, 'Attacker seat share (must be flat)', 20)
    for tick in (0, .1, .2, .3):
        yy = iy + ih * (1 - tick / .3)
        dr.line((ix, yy, ix + iw, yy), fill=GRID, width=1)
        text(ix - 50, yy - 11, f'{tick:.0%}', 17, MUTED)
    for j, c in enumerate(carriers):
        text(ix + 20 + j * (iw - 40) / (len(carriers) - 1) - 9, iy + ih + 10, c, 19)
    for arm in arms:
        for checks in checks_list:
            for rate in rates:
                points = []
                for j, c in enumerate(carriers):
                    cell = cells.get((c, checks, rate, arm))
                    if cell and cell['attacker']:
                        v = min(.3, sum(cell['attacker']) / len(cell['attacker']))
                        points.append((ix + 20 + j * (iw - 40) / (len(carriers) - 1), iy + ih * (1 - v / .3)))
                    else:
                        points.append(None)
                for a, b in zip(points, points[1:]):
                    if a and b:
                        _line(dr, a, b, COLORS[arm], STYLE[checks], 2)
    matched = defaultdict(set)
    for r in pilot:
        matched[(r['task'], r['attacker_pass'], r['arm'], r['checks'])].add((r['admitted_hash'], r['audit_hash'], r['order_hash']))
    bad = sum(len(v) != 1 for v in matched.values())
    text(ix - 40, iy + ih + 38, f'mismatches across carrier counts: {bad} in {len(matched)} cells', 17,
         BAD if bad else MUTED)


def replay(rows, out, stage, total, initial_accounting=None):
    """Initial and final frames and a GIF of at most 33 completion prefixes (measured rows only)."""
    terminal = [r for r in rows if r['status'] != 'not_started']
    count = len(terminal)
    counts = sorted(set([0, count, *[round(count * i / 32) for i in range(1, 32)]]))
    images = []
    for n in counts:
        prefix = terminal[:n]
        last = prefix[-1] if prefix else {}
        images.append(frame(rows if n == count else prefix, total, stage, last.get('elapsed_seconds', 0),
                            last.get('study_accounting') or initial_accounting))
    images[0].save(out / 'initial_frame.png')
    images[-1].save(out / 'final_frame.png')
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:],
                   duration=[550] * (len(images) - 1) + [2500], loop=0)
    return len(images)
