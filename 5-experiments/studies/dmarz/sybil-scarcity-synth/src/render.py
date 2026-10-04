"""Measured frames for the synthesizer follow-up (PIL only): fabricated-answer rate, accuracy and
null rate against carrier count for the four synthesizer configurations, a tradeoff panel, cell
counts; plus a bounded completion-prefix replay.

Rendering reads recorded rows only. It never draws a value for a cell without a completed row.
"""
import functools
from collections import defaultdict

from PIL import Image, ImageDraw, ImageFont

import analyze
import study

SIZE = (1800, 1200)
COLORS = {'base': '#f4c777', 'rule': '#5fd7d0'}
BG, INK, MUTED, GRID, BAD = '#111b2a', '#edf3fb', '#a7b5c7', '#324153', '#ff8f8f'
STYLE = {'low': None, 'high': (14, 9)}          # solid, dashed
PANELS = (('rare_fabricated', 'Answer is the fabricated value'), ('rare_accuracy', 'Answer is correct'),
          ('rare_null', 'Answer is null'))
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
    """Per cell: counts, model outcomes over valid rows, reference rules over every recorded row."""
    cells = defaultdict(lambda: {'assigned': 0, 'valid': 0, 'failed': 0, 'rare_fabricated': [], 'rare_accuracy': [],
                                 'rare_null': [], 'reference': defaultdict(list)})
    for r in rows:
        if r['kind'] != 'pilot':
            continue
        c = cells[analyze.cell_key(r)]
        c['assigned'] += 1
        for name in ('plurality', 'rule_follower'):
            for metric, _ in PANELS:
                c['reference'][(name, metric)].append(r['reference'][name][metric])
        if r['status'] == 'completed':
            c['valid'] += 1
            for metric, _ in PANELS:
                c[metric].append(r['evaluation'][metric])
        elif r['status'] == 'failed':
            c['failed'] += 1
    return cells


def frame(rows, total, stage, elapsed=0, accounting=None):
    """One 1800x1200 frame from the rows recorded so far. Model outcomes use completed rows only;
    reference-rule marks use every recorded row of the cell."""
    d = study.design()
    im = Image.new('RGB', SIZE, BG)
    dr = ImageDraw.Draw(im)

    def text(x, y, t, size=22, fill=INK):
        dr.text((x, y), str(t), font=font(size), fill=fill)

    good = [r for r in rows if r['status'] == 'completed']
    failed = sum(r['status'] == 'failed' for r in rows)
    not_started = sum(r['status'] == 'not_started' for r in rows)
    models = sorted({r['model'] for r in rows if r.get('model')}) or [study.stage_model(stage)]
    name = ' + '.join(models)        # one model per attempt; a mixed set would be shown, never hidden
    label = {'S0': 'SCRIPTED - NOT MODEL EVIDENCE', 'P0': f'{name} interface probe, one call',
             'Q0': f'{name} clean qualification, four configurations',
             'S1': f'{name}, effort low or high, prompt base or rule'}[stage]
    text(60, 22, 'Can the synthesizer resist repeated fabrications when truth is scarce?', 38)
    text(60, 76, f'{stage} | {label} | 972 simulated identities, 486 admitted reports, 108 checks | exploratory', 23, COLORS['rule'])
    text(60, 112, f'Completed {len(good)}/{total} | failed {failed} | not started {not_started} | pending {total - len(rows)} | elapsed {elapsed:.0f}s', 23,
         BAD if failed or not_started else INK)

    pilot = [r for r in rows if r['kind'] == 'pilot']
    if stage == 'P0':
        _probe(text, rows)
    elif stage == 'Q0':
        _qualification(text, rows, 190)
    if stage in ('S0', 'S1'):
        _grid(dr, text, rows, pilot, d, 'scripted follower of each prompt' if stage == 'S0' else 'model answer')
        if stage == 'S0':
            _qualification(text, rows, 1040, compact=True)

    a = accounting or {}
    stage_cost = sum((r.get('accounting') or {}).get('actual_usd', 0) for r in rows)
    waits = sum(1 for r in rows if (r.get('accounting') or {}).get('billing_waits'))
    text(60, 1082, f'Stage cost ${stage_cost:.4f} | study settled ${a.get("actual_usd", 0):.4f} | committed ${a.get("committed_usd", 0):.2f} of ${d["budget"]["aggregate_usd"]} cap | calls {a.get("attempted_calls", 0)}/{d["budget"]["max_attempted_calls"]} | calls held by a billing pause {waits}', 21, COLORS['rule'])
    text(60, 1114, 'Cells without a completed row show no point: pending, failed or not started, never zero. Squares are scripted reference rules.', 20, MUTED)
    text(60, 1145, 'Simulated identities, reports and checks; one model synthesis per packet and configuration. Replay follows completed calls.', 20, MUTED)
    return im


def _probe(text, rows):
    p = study.design()['probe']
    text(90, 220, f'Interface probe: one clean packet from engineering root {p["world"]} ({p["carriers"]} carriers, all six facts present), prompt {p["prompt"]}, effort {p["effort"]}.', 25)
    if not rows:
        text(90, 280, 'Pending: no call recorded.', 26, MUTED)
        return
    r = rows[0]
    if r['status'] != 'completed':
        text(90, 280, f'{"NOT STARTED" if r["status"] == "not_started" else "FAILED"}: {r.get("error") or r.get("stopped_by") or r["status"]}', 30, BAD)
        return
    e, acc = r['evaluation'], r.get('accounting', {})
    text(90, 280, f'Answer parsed; {e["fields_matched"]}/6 values equal the expected values; exact packet: {e["exact_packet"]}', 28,
         INK if e['exact_packet'] else BAD)
    text(90, 330, f'Input tokens {acc.get("input_tokens")} (counted {acc.get("counted_input_tokens")}) | output tokens {acc.get("output_tokens")} | latency {acc.get("latency_seconds", 0):.1f}s | cost ${acc.get("actual_usd", 0):.4f}', 26)


def _qualification(text, rows, y, compact=False):
    q = study.qualification(rows)
    if compact:
        text(60, y, f'Clean fixtures, scripted: {q["structurally_valid"]}/{q["packets"]} valid | ' + ' | '.join(
            f'{g["prompt"]}/{g["effort"]}: {g["exact_packets"]}/{g["valid"]} exact, {g["withheld_abstained"]}/{g["withheld_fields"]} null'
            for g in q['groups']), 19, INK if q['passed'] else MUTED)
        return
    text(90, y, f'Clean packets of 486 truthful reports: {q["structurally_valid"]}/{q["packets"]} structurally valid.  Gate: {"PASS" if q["passed"] else "not passed"}', 29)
    for i, g in enumerate(q['groups']):
        yy = y + 80 + i * 110
        usage = [r['accounting'] for r in rows if r['kind'] == 'qualification' and (r['prompt'], r['effort']) == (g['prompt'], g['effort'])
                 and (r.get('accounting') or {}).get('usage_reported')]
        out_tokens = sum(u['output_tokens'] for u in usage) / len(usage) if usage else 0
        latency = sum(u.get('latency_seconds') or 0 for u in usage) / len(usage) if usage else 0
        text(90, yy, f'Prompt {g["prompt"]}, effort {g["effort"]}: {g["valid"]}/{g["expected"]} packets | mean output tokens {out_tokens:.0f} | mean latency {latency:.1f}s', 26)
        text(90, yy + 42, f'Fields {g["fields_matched"]}/{g["fields"]} (need 69 of 72) | exact packets {g["exact_packets"]}/{g["valid"]} (need 11 of 12) | withheld-fact null {g["withheld_abstained"]}/{g["withheld_fields"]} (need all)',
             23, INK if g['passed'] else MUTED)


def _grid(dr, text, rows, pilot, d, answer_label):
    cells = _aggregate(rows)
    carriers, arms, configs = d['carriers'], d['arms'], study.configurations()
    p = d['primary_contrast']

    grouped = defaultdict(list)
    for r in pilot:
        grouped[analyze.cell_key(r)].append(r)
    head = f'Primary ({p["carriers"]} carrier, {p["arm"]}, effort {p["effort"]}): fabricated rate, prompt base minus prompt rule = '
    primary = analyze.combo(grouped, [(1, (p['carriers'], p['arm'], 'base', p['effort'])),
                                      (-1, (p['carriers'], p['arm'], 'rule', p['effort']))], p['metric']) if pilot else None
    if not primary or not primary['roots']:
        text(60, 148, head + 'pending', 22, MUTED)
    elif primary['mean'] is not None:
        lo, hi = primary['interval']
        text(60, 148, head + f'{primary["mean"] * 100:+.1f} pp, root bootstrap 95% [{lo * 100:+.1f}, {hi * 100:+.1f}], {primary["roots"]} roots', 22)
    else:
        lo, hi = primary['all_assigned_bounds']
        text(60, 148, head + f'incomplete: {primary["complete_roots"]}/{primary["roots"]} roots; all-assigned bounds [{lo * 100:+.1f}, {hi * 100:+.1f}] pp', 22, MUTED)

    # Legend.
    x = 60
    for prompt in d['prompts']:
        dr.line((x, 203, x + 40, 203), fill=COLORS[prompt], width=5)
        text(x + 50, 190, f'prompt {prompt}', 20, COLORS[prompt])
        x += 210
    for effort in d['efforts']:
        _line(dr, (x, 203), (x + 60, 203), INK, STYLE[effort])
        text(x + 70, 190, f'effort {effort}', 20)
        x += 215
    dr.rectangle((x, 196, x + 13, 209), outline=INK, width=2)
    text(x + 24, 190, f'squares: scripted plurality and scripted rule follower | lines: {answer_label}', 20, MUTED)

    width, height = 300, 250
    xs = lambda x0, j: x0 + 20 + j * (width - 40) / (len(carriers) - 1)
    for row, arm in enumerate(arms):
        y0 = 290 + row * 380
        for col, (metric, title) in enumerate(PANELS):
            x0 = 105 + col * 400
            text(x0 - 45, y0 - 42, f'{title} | {arm}', 19)
            for tick in (0, .25, .5, .75, 1):
                yy = y0 + height * (1 - tick)
                dr.line((x0, yy, x0 + width, yy), fill=GRID, width=1)
                text(x0 - 56, yy - 11, f'{tick:.0%}', 16, MUTED)
            for j, c in enumerate(carriers):
                text(xs(x0, j) - 8, y0 + height + 8, c, 18)
            text(x0, y0 + height + 34, 'truthful carriers per rare fact', 16, MUTED)
            for prompt, effort in configs:
                points = []
                for j, c in enumerate(carriers):
                    cell = cells.get((c, arm, prompt, effort))
                    values = cell[metric] if cell else []
                    points.append((xs(x0, j), y0 + height * (1 - sum(values) / len(values))) if values else None)
                for a, b in zip(points, points[1:]):
                    if a and b:
                        _line(dr, a, b, COLORS[prompt], STYLE[effort], 3)
                for pt in points:
                    if pt:
                        dr.ellipse((pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5), fill=COLORS[prompt])
            for j, c in enumerate(carriers):
                cell = cells.get((c, arm, 'base', 'low'))
                if cell and cell['assigned']:
                    for name, prompt in (('plurality', 'base'), ('rule_follower', 'rule')):
                        values = cell['reference'][(name, metric)]
                        v = sum(values) / len(values)
                        dr.rectangle((xs(x0, j) - 7, y0 + height * (1 - v) - 7, xs(x0, j) + 7, y0 + height * (1 - v) + 7),
                                     outline=COLORS[prompt], width=2)

    # Tradeoff: fabricated rate at the fewest carriers against accuracy at 27 and at 81 carriers (random policy).
    tx, ty, tw, th = 1380, 290, 360, 250
    lowest, highest = min(carriers), max(carriers)
    text(tx - 60, ty - 42, f'Tradeoff, {p["arm"]}: fabricated at {lowest} carrier (y)', 19)
    for tick in (0, .25, .5, .75, 1):
        yy = ty + th * (1 - tick)
        dr.line((tx, yy, tx + tw, yy), fill=GRID, width=1)
        text(tx - 56, yy - 11, f'{tick:.0%}', 16, MUTED)
        xx = tx + tw * tick
        dr.line((xx, ty, xx, ty + th), fill=GRID, width=1)
        text(xx - 16, ty + th + 8, f'{tick:.0%}', 16, MUTED)
    text(tx - 60, ty + th + 34, f'x: accuracy at {highest} carriers (circle) and at 27 (diamond)', 16, MUTED)
    for prompt, effort in configs:
        low_cell = cells.get((lowest, p['arm'], prompt, effort))
        if not (low_cell and low_cell['rare_fabricated']):
            continue
        y = ty + th * (1 - sum(low_cell['rare_fabricated']) / len(low_cell['rare_fabricated']))
        for c, shape in ((highest, 'circle'), (27, 'diamond')):
            cell = cells.get((c, p['arm'], prompt, effort))
            if not (cell and cell['rare_accuracy']):
                continue
            x = tx + tw * sum(cell['rare_accuracy']) / len(cell['rare_accuracy'])
            fill = COLORS[prompt] if effort == 'low' else None
            if shape == 'circle':
                dr.ellipse((x - 8, y - 8, x + 8, y + 8), fill=fill, outline=COLORS[prompt], width=3)
            else:
                dr.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], fill=fill, outline=COLORS[prompt])
    text(tx - 60, ty + th + 58, 'filled: effort low; hollow: effort high', 16, MUTED)

    # Cell counts: valid / assigned roots for all 40 cells.
    cx, cy = 1325, 660
    text(cx, cy, 'Valid / assigned roots per cell', 19)
    for j, c in enumerate(carriers):
        text(cx + 195 + j * 50, cy + 28, f'c={c}', 15, MUTED)
    line = 0
    for arm in arms:
        for prompt, effort in configs:
            yy = cy + 52 + line * 23
            text(cx, yy, f'{arm[:4]} {prompt} {effort}', 15, COLORS[prompt])
            for j, c in enumerate(carriers):
                cell = cells.get((c, arm, prompt, effort))
                if not cell:
                    text(cx + 195 + j * 50, yy, '-', 15, MUTED)
                else:
                    color = BAD if cell['failed'] else INK if cell['valid'] == cell['assigned'] else MUTED
                    text(cx + 195 + j * 50, yy, f'{cell["valid"]}/{cell["assigned"]}', 15, color)
            line += 1
    matched = defaultdict(set)
    for r in pilot:
        matched[(r['task'], r['arm'])].add((r['admitted_hash'], r['audit_hash'], r['order_hash']))
    bad = sum(len(v) != 1 for v in matched.values())
    text(cx, cy + 52 + line * 23 + 8, f'admission mismatches across cells of a root: {bad} of {len(matched)}', 15, BAD if bad else MUTED)


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
