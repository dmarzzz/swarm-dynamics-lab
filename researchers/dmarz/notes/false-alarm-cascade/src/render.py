"""Measured frames for the false-alarm study (PIL only).

Stage frame: use of X and of H by round and condition with the alarm and the correction marked,
spillover, signal detection, and a completion grid with missing cells shown as missing.
Replay: one frame per round for one prespecified root, showing how many of the five agents used
each resource and what the board held. Truth (honeypots, X, H, the planted author) is drawn only
here, in the viewer layer; it never enters an actor input.

Rendering reads recorded rows only. It never draws a value for a cell without a completed row.
"""
import functools
from collections import defaultdict

from PIL import Image, ImageDraw, ImageFont

import analyze
import sim
import study

SIZE = (1800, 1200)
BG, INK, MUTED, GRID, BAD, PANEL = '#111b2a', '#edf3fb', '#a7b5c7', '#324153', '#ff6b6b', '#182436'
COLORS = {'C0': '#dfe7f2', 'FA': '#ff9d5c', 'FA+C': '#f4d35e', 'TA': '#5fd7d0', 'TA+C': '#b39bff'}
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf',
              '/Library/Fonts/Arial.ttf',
              '/System/Library/Fonts/Helvetica.ttc')
LABEL = {'S0': 'SCRIPTED - NOT MODEL EVIDENCE', 'P0': 'OPUS 5.5 interface probe, one call',
         'Q0': 'OPUS 5.5 qualification, no planted claim', 'S1': 'OPUS 5.5, effort medium'}
TITLE = 'Does a false honeypot alarm outlive its correction?'


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


def _dash(d, a, b, color, width=2, dash=8, gap=7):
    length = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** .5
    t = 0.0
    while length and t < length:
        u = min(t + dash, length)
        d.line((a[0] + (b[0] - a[0]) * t / length, a[1] + (b[1] - a[1]) * t / length,
                a[0] + (b[0] - a[0]) * u / length, a[1] + (b[1] - a[1]) * u / length), fill=color, width=width)
        t += dash + gap


def _canvas():
    im = Image.new('RGB', SIZE, BG)
    dr = ImageDraw.Draw(im)

    def text(x, y, t, size=22, fill=INK):
        dr.text((x, y), str(t), font=font(size), fill=fill)
    return im, dr, text


def plot_actor(stage, rows):
    """The actor whose episodes the stage frame plots: the model, or in S0 the credulous script."""
    actors = {r['actor'] for r in rows if r['kind'] == 'episode'}
    return 'model' if stage != 'S0' else 'credulous' if 'credulous' in actors or not actors else sorted(actors)[0]


def round_rates(rows, actor, key, per=1):
    """{(condition, round): (used, observed decisions, planned decisions)} for one actor."""
    out = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        if r['kind'] == 'episode' and r['actor'] == actor:
            cell = out[(r['condition'], r['round'])]
            cell[2] += per
            if r['status'] == 'completed':
                cell[0] += r['evaluation'][key]
                cell[1] += per
    return out


def _lines(dr, text, box, title, rates, conditions, rounds, markers=True, upto=None):
    """Use rate by round, one line per condition. A round with no completed row has no point."""
    x0, y0, w, h = box
    text(x0 - 50, y0 - 46, title, 22)
    for tick in (0, .25, .5, .75, 1):
        yy = y0 + h * (1 - tick)
        dr.line((x0, yy, x0 + w, yy), fill=GRID, width=1)
        text(x0 - 56, yy - 11, f'{tick:.0%}', 18, MUTED)
    xs = lambda t: x0 + 30 + (t - 1) * (w - 60) / (rounds - 1)
    for t in range(1, rounds + 1):
        text(xs(t) - 6, y0 + h + 10, t, 20)
    text(x0 + w / 2 - 30, y0 + h + 38, 'round', 18, MUTED)
    if markers:
        d = study.design()['planted']
        for after, label in ((d['alarm_round'], 'alarm posted'), (d['correction_round'], 'correction posted')):
            xm = (xs(after) + xs(after + 1)) / 2
            _dash(dr, (xm, y0), (xm, y0 + h), MUTED)
            text(xm - 62, y0 - 22, label, 16, MUTED)
    for c in conditions:
        points = []
        for t in range(1, rounds + 1):
            used, n, _ = rates.get((c, t), (0, 0, 0))
            points.append((xs(t), y0 + h * (1 - used / n)) if n and (upto is None or t <= upto) else None)
        for a, b in zip(points, points[1:]):
            if a and b:
                dr.line((*a, *b), fill=COLORS[c], width=4)
        for pt in points:
            if pt:
                dr.ellipse((pt[0] - 6, pt[1] - 6, pt[0] + 6, pt[1] + 6), fill=COLORS[c])


def _legend(dr, text, x, y, conditions, size=20):
    for c in conditions:
        dr.line((x, y + 12, x + 36, y + 12), fill=COLORS[c], width=5)
        text(x + 44, y, c, size, COLORS[c])
        x += 70 + 14 * len(c)
    return x


def frame(rows, total, stage, elapsed=0, accounting=None):
    """One 1800x1200 frame from the rows recorded so far."""
    d = study.design()
    im, dr, text = _canvas()
    good = [r for r in rows if r['status'] == 'completed']
    failed = sum(r['status'] == 'failed' for r in rows)
    not_started = sum(r['status'] == 'not_started' for r in rows)
    text(60, 22, TITLE, 40)
    text(60, 78, f'{stage} | {LABEL[stage]} | 6 members, 12 synthetic resources, 6 rounds | exploratory', 24, COLORS['TA'])
    text(60, 114, f'Call rows completed {len(good)}/{total} | failed {failed} | not started {not_started} | pending {total - len(rows)} | elapsed {elapsed:.0f}s', 23)
    if stage == 'P0':
        _probe(text, rows)
    elif stage == 'Q0':
        _qualification(text, rows, 200)
    else:
        _grid(dr, text, rows, d, stage)
    a = accounting or {}
    stage_cost = sum((r.get('accounting') or {}).get('actual_usd', 0) for r in rows)
    text(60, 1100, f'Stage cost ${stage_cost:.4f} | study settled ${a.get("actual_usd", 0):.4f} | committed ${a.get("committed_usd", 0):.2f} of ${d["budget"]["aggregate_usd"]} cap | calls {a.get("attempted_calls", 0)}/{d["budget"]["max_attempted_calls"]}', 21, COLORS['TA'])
    text(60, 1134, 'A point is drawn only where completed rows exist: pending, failed and not-started calls are never shown as zero. Truth is used by the evaluator only.', 19, MUTED)
    text(60, 1162, 'Synthetic resources; the sixth member posts by design. Roots are the units; agents, rounds and calls are not independent samples.', 19, MUTED)
    return im


def _probe(text, rows):
    p = study.design()['probe']
    text(90, 220, f'Interface probe: one round-{p["round"]} packet of engineering root {p["world"]} with a clean board.', 26)
    rows = [r for r in rows if r['kind'] == 'probe']
    if not rows:
        text(90, 280, 'Pending: no call recorded.', 26, MUTED)
        return
    r = rows[0]
    if r['status'] != 'completed':
        text(90, 280, f'FAILED: {r.get("error", r["status"])}', 30, BAD)
        return
    e, acc = r['evaluation'], r.get('accounting', {})
    u = e['unanimous']
    text(90, 280, f'Answer parsed; {u["matched"]}/{u["total"]} decisions on unanimous resources equal the reference.', 28,
         INK if u['matched'] == u['total'] else BAD)
    text(90, 330, f'Input tokens {acc.get("input_tokens")} (counted {acc.get("counted_input_tokens")}) | output tokens {acc.get("output_tokens")} | latency {acc.get("latency_seconds") or 0:.1f}s | cost ${acc.get("actual_usd", 0):.4f}', 26)
    text(90, 380, f'All 12 decisions: {e["agree"]["private"]}/12 equal the private-evidence reference; claims posted: {len(e["claims"])}.', 24, MUTED)


def _qualification(text, rows, y, compact=False):
    q = study.qualification(rows)
    need = study.design()['qualification']['match_rate']
    if compact:
        text(60, y, f'Qualification fixtures, scripted: {q["structurally_valid"]}/{q["packets"]} valid | ' + ' | '.join(
            f'depth {g["depth"]}: {g["matched"]}/{g["gated"]} gated' for g in q['groups']), 20, INK if q['passed'] else MUTED)
        return
    text(90, y, f'Packets without any planted claim: {q["structurally_valid"]}/{q["packets"]} structurally valid.  Gate: {"PASS" if q["passed"] else "not passed"}', 29)
    text(90, y + 50, f'Gated decisions (private posterior at most 0.10 or at least 0.80, no opposing board claim): {q["matched"]}/{q["gated"]} equal the reference ({q["match_rate"]:.1%}, need {need:.0%})', 23,
         INK if q['gated'] and q['matched'] >= need * q['gated'] else MUTED)
    for i, g in enumerate(q['groups']):
        yy = y + 130 + i * 110
        text(90, yy, f'Round depth {g["depth"]}: {g["valid"]}/{g["expected_packets"]} packets', 27)
        text(90, yy + 42, f'gated {g["matched"]}/{g["gated"]} of {g["expected_gated"]} planned ({g["match_rate"]:.1%}, need {need:.0%}) | use-gated {g["use_matched"]}/{g["use_gated"]} | skip-gated {g["skip_matched"]}/{g["skip_gated"]} | contested, not gated: {g["contested"]}',
             22, INK if g['passed'] else MUTED)


def _grid(dr, text, rows, d, stage):
    actor = plot_actor(stage, rows)
    mine = [r for r in rows if r['kind'] == 'episode' and r['actor'] == actor]
    rounds = d['world']['rounds']
    w = d['windows']
    cells = analyze.Cells(mine)

    # Primary contrast line. Roots that have no recorded row yet are unknown, not absent.
    head = 'Primary: use of X in rounds 4-6, C0 minus FA+C = '
    primary = cells.contrast('C0', 'FA+C', w['after_correction'], 'use_x') if mine else None
    who = '' if stage == 'S1' else f' ({actor} script)'
    planned = len(d['worlds'] if stage == 'S1' else d['engineering_worlds'])
    if not primary or not primary['roots']:
        text(60, 150, head + 'pending', 23, MUTED)
    elif primary['mean'] is not None and primary['roots'] == planned:
        lo, hi = primary['interval']
        text(60, 150, head + f'{primary["mean"] * 100:+.1f} pp, root bootstrap 95% [{lo * 100:+.1f}, {hi * 100:+.1f}], {primary["roots"]} roots{who}', 23)
    else:
        unknown = planned - primary['roots']
        lo = (primary['all_assigned_bounds'][0] * primary['roots'] - unknown) / planned
        hi = (primary['all_assigned_bounds'][1] * primary['roots'] + unknown) / planned
        text(60, 150, head + f'incomplete: {primary["complete_roots"]}/{planned} roots complete; all-assigned bounds [{lo * 100:+.1f}, {hi * 100:+.1f}] pp{who}', 23, MUTED)

    x = _legend(dr, text, 60, 192, d['conditions'])
    text(x + 10, 192, 'X: real resource falsely accused in FA, FA+C.  H: honeypot truly accused in TA, TA+C.', 19, MUTED)

    label = 'model agents' if stage == 'S1' else f'{actor} script'
    _lines(dr, text, (110, 290, 600, 270), f'Use of X by round ({label})', round_rates(rows, actor, 'use_x'), ('C0', 'FA', 'FA+C'), rounds)
    _lines(dr, text, (830, 290, 600, 270), f'Use of H by round ({label})', round_rates(rows, actor, 'use_h'), ('C0', 'TA', 'TA+C'), rounds)

    # Spillover: C0 minus alarm condition, family-mates of X and other real resources.
    sx, sy, sw, sh = 110, 720, 600, 250
    text(sx - 50, sy - 46, 'Spillover: use rate, C0 minus condition (points)', 22)
    zero = sy + sh / 2
    for tick in (-.5, -.25, 0, .25, .5):
        yy = zero - tick * sh
        dr.line((sx, yy, sx + sw, yy), fill=INK if tick == 0 else GRID, width=1)
        text(sx - 56, yy - 11, f'{tick * 100:+.0f}', 18, MUTED)
    bars = [(metric, b, name, rr) for metric in ('use_mates', 'use_other_real') for b in ('FA', 'FA+C')
            for name, rr in (('2-3', w['cascade']), ('4-6', w['after_correction']))]
    for i, (metric, b, name, rr) in enumerate(bars):
        c = cells.contrast('C0', b, rr, metric) if mine else None
        bx = sx + 18 + i * (sw - 36) / len(bars)
        bw = (sw - 36) / len(bars) - 14
        value = c['complete_case_mean'] if c else None
        if value is not None:
            top = zero - max(-.5, min(.5, value)) * sh
            dr.rectangle((bx, min(top, zero), bx + bw, max(top, zero)), fill=COLORS[b],
                         outline=None if c['mean'] is not None else MUTED)
            text(bx, min(top, zero) - 22, f'{value * 100:+.0f}', 17)
        text(bx, sy + sh + 8, name, 17, COLORS[b])
    text(sx + 18, sy + sh + 32, "X's two family-mates", 18, MUTED)
    text(sx + 18 + (sw - 36) / 2, sy + sh + 32, 'five other real resources', 18, MUTED)
    text(sx + 18, sy + sh + 56, 'bar labels: rounds 2-3 and 4-6; complete roots only', 16, MUTED)

    # Signal detection by condition and window.
    table = defaultdict(lambda: [0, 0, 0, 0])
    for r in mine:
        if r['status'] == 'completed':
            for name, rr in w.items():
                if r['round'] in rr:
                    e, t = r['evaluation'], table[(r['condition'], name)]
                    t[0] += e['skipped_honeypot']; t[1] += e['used_honeypot']; t[2] += e['skipped_real']; t[3] += e['used_real']
    names = list(w)
    for k, (title, key, lo, hi) in enumerate((("d' (discrimination)", 'd_prime', 0, 3), ('criterion c (below 0: skips more)', 'criterion', -1.5, 1.5))):
        px, py, pw, ph = 830 + k * 330, 720, 250, 250
        text(px - 40, py - 46, title, 20)
        for tick in (lo, (lo + hi) / 2, hi):
            yy = py + ph * (1 - (tick - lo) / (hi - lo))
            dr.line((px, yy, px + pw, yy), fill=GRID, width=1)
            text(px - 44, yy - 10, f'{tick:g}', 17, MUTED)
        for j, name in enumerate(names):
            text(px + 14 + j * (pw - 40) / (len(names) - 1) - 12, py + ph + 8, ('1', '2-3', '4-6')[j], 18)
        for c in d['conditions']:
            points = []
            for j, name in enumerate(names):
                s = analyze.detection(*table[(c, name)]) if (c, name) in table else None
                v = s[key] if s else None
                points.append((px + 14 + j * (pw - 40) / (len(names) - 1),
                               py + ph * (1 - (max(lo, min(hi, v)) - lo) / (hi - lo))) if v is not None else None)
            for a, b in zip(points, points[1:]):
                if a and b:
                    dr.line((*a, *b), fill=COLORS[c], width=3)
            for pt in points:
                if pt:
                    dr.ellipse((pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5), fill=COLORS[c])
    text(790, 720 + 250 + 34, 'round windows; all 12 resources; log-linear correction', 16, MUTED)

    # Completion grid: one row per root (and actor in S0), one column per condition.
    gx, gy = 1500, 250
    text(gx, gy - 44, 'Rounds completed per episode', 20)
    episodes = defaultdict(lambda: {'done': 0, 'failed': 0, 'rows': 0})
    for r in rows:
        if r['kind'] == 'episode':
            e = episodes[(r['actor'], r['root'], r['condition'])]
            e['rows'] += 1
            e['done'] += r['status'] == 'completed'
            e['failed'] += r['status'] == 'failed'
    keys = sorted({(a, root) for a, root, _ in episodes})
    for j, c in enumerate(d['conditions']):
        text(gx + 96 + j * 40, gy - 16, c, 13, COLORS[c])
    step = min(30, 760 // max(1, len(keys)))
    per_round = len(d['world']['members']) - 1
    for i, (a, root) in enumerate(keys):
        yy = gy + 6 + i * step
        text(gx, yy, f'{root}' if stage == 'S1' else f'{root} {a[:9]}', 13, MUTED)
        for j, c in enumerate(d['conditions']):
            e = episodes.get((a, root, c))
            box = (gx + 96 + j * 40, yy, gx + 96 + j * 40 + 34, yy + step - 4)
            if not e:
                dr.rectangle(box, outline=GRID)
                continue
            done = e['done'] // per_round
            shade = int(40 + 200 * done / rounds)
            dr.rectangle(box, fill=BAD if e['failed'] else (shade // 3, shade // 2 + 30, shade), outline=GRID)
            text(box[0] + 12, yy + max(0, (step - 22) // 2), done, 14, INK)
    text(gx, gy + 12 + len(keys) * step, 'red: a call failed', 15, MUTED)
    if stage == 'S0':
        _qualification(text, rows, 1060, compact=True)


def representative(rows, stage):
    """The prespecified episode set of the replay: lowest root; the model, or in S0 the credulous script."""
    d = study.design()
    actor = plot_actor(stage, rows)
    root = d['analysis']['representative_root'] if stage == 'S1' else min(d['engineering_worlds'])
    return actor, root


def replay_frame(rows, stage, round_, actor, root):
    """Round `round_` of the representative root in all five conditions. round_ 0: nothing played yet."""
    d = study.design()
    im, dr, text = _canvas()
    world = sim.make_world(root, d['world'])
    truth = world['truth']
    order = sorted(world['public']['resources'], key=lambda x: (x['family'], x['id']))
    mine = [r for r in rows if r['kind'] == 'episode' and r['actor'] == actor and r['root'] == root]
    text(60, 22, TITLE, 40)
    text(60, 78, f'{stage} | {LABEL[stage]} | replay of recorded rows, root {root}' + ('' if stage == 'S1' else f', {actor} script'), 24, COLORS['TA'])
    text(60, 114, f'Round {round_} of {d["world"]["rounds"]}' if round_ else 'Before round 1', 30)
    text(420, 122, 'Cell: how many of the 5 agents used the resource this round. Red outline: honeypot. X, H: alarm subjects. Viewer layer only; agents never see this.', 18, MUTED)
    cw = 84
    for j, x in enumerate(order):
        text(250 + j * cw + 12, 166, x['id'], 19)
        text(250 + j * cw + 12, 190, x['family'][:6], 15, MUTED)
    text(1290, 166, 'Board seen this round: entries on the alarm subject', 16, MUTED)
    text(1290, 188, '(* = planted author)', 15, MUTED)
    for i, c in enumerate(d['conditions']):
        y = 226 + i * 172
        text(60, y + 20, c, 30, COLORS[c])
        now = [r for r in mine if r['condition'] == c and r['round'] == round_]
        good = [r for r in now if r['status'] == 'completed']
        subject = truth['X'] if c in ('C0', 'FA', 'FA+C') else truth['H']
        if round_ and now:
            text(60, y + 62, f'{len(good)}/{len(now)} calls', 17, MUTED if len(good) == len(now) else BAD)
        for j, x in enumerate(order):
            ident = x['id']
            box = (250 + j * cw, y, 250 + j * cw + cw - 8, y + 108)
            used = sum(r['answer']['decisions'][ident] == 'use' for r in good)
            if good:
                shade = int(40 + 200 * used / len(good))
                dr.rectangle(box, fill=(shade // 3, shade // 2 + 30, shade))
                text(box[0] + 18, y + 34, f'{used}/{len(good)}', 24)
            else:
                dr.rectangle(box, fill=PANEL)
                text(box[0] + 30, y + 34, '-', 24, MUTED)
            if ident in truth['honeypots']:
                dr.rectangle(box, outline=BAD, width=4)
            if ident in (truth['X'], truth['H']):
                text(box[0] + 6, y + 4, 'X' if ident == truth['X'] else 'H', 20, COLORS['FA+C'] if ident == truth['X'] else COLORS['TA'])
        board = good[0]['packet']['board'] if good else []
        about = [e for e in board if e['resource'] == subject]
        text(1290, y, f'{len(board)} entries; {len(about)} about {"X" if subject == truth["X"] else "H"} ({subject})', 17)
        for k, e in enumerate(about[-5:]):
            star = '*' if e['author'] == truth['planted'] else ''
            tail = f' (retracts r{e["retracts"]})' if 'retracts' in e else ''
            text(1290, y + 26 + k * 24, f'r{e["round"]} {e["author"]}{star}: {e["claim"]}{tail}', 17,
                 COLORS[c] if star else INK)
    rates = round_rates(rows, actor, 'use_x')
    text(60, 1100, 'All recorded roots, use of X in this round: ' + '   '.join(
        f'{c} {rates[(c, round_)][0] / rates[(c, round_)][1]:.0%}' if round_ and rates.get((c, round_), (0, 0, 0))[1] else f'{c} -'
        for c in ('C0', 'FA', 'FA+C')), 21, COLORS['TA'])
    text(60, 1134, 'Each frame is one logical round of recorded calls; nothing is interpolated. A dash means no completed call for that cell.', 19, MUTED)
    text(60, 1162, 'Synthetic resources; the sixth member posts by design. Truth and the planted author are drawn by the viewer, never sent to an agent.', 19, MUTED)
    return im


def replay(rows, out, stage, total, initial_accounting=None):
    """Initial and final stage frames, and a GIF: one frame per round of the representative root for
    stages with episodes, otherwise the initial and final frames."""
    terminal = [r for r in rows if r['status'] != 'not_started']
    last = terminal[-1] if terminal else {}
    first = frame([], total, stage, 0, initial_accounting)
    final = frame(rows, total, stage, last.get('elapsed_seconds', 0), last.get('study_accounting') or initial_accounting)
    first.save(out / 'initial_frame.png')
    final.save(out / 'final_frame.png')
    if any(r['kind'] == 'episode' for r in rows):
        actor, root = representative(rows, stage)
        images = [replay_frame(rows, stage, t, actor, root) for t in range(0, study.design()['world']['rounds'] + 1)] + [final]
        durations = [900] + [1400] * (len(images) - 2) + [3000]
    else:
        images, durations = [first, final], [900, 3000]
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:], duration=durations, loop=0)
    return len(images)
