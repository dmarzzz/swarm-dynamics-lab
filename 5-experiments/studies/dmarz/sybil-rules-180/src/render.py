"""Frames, replay and plain counts for the 180-owner rule study (Pillow only, no network, no clock).

Rendering reads round records as returned by `sim.step` and nothing else. It never draws a value
for a round, market or episode that has no record. Every per-round number in a frame comes from
`summary_counts`; every per-owner mark comes from `owner_flags`, which `summary_counts` also uses.

Words used in frames: "entry into the other product" for a firm opened in the product the owner did
not start in, "same-product split" for two or more producing firms of one owner in one product, and
"split lowers a firm-level charge" for owner-rounds where the evaluator-only `mask` field is true. `sim`
defines that field on firm-level concentration in every regime, so under the owner-level charge and in the
warm-up the mark shows the same condition and no charge is saved. A new firm is never given any other label.

Text is fitted to its slot by shrinking, so a wider font (DejaVu on the servers, Arial on a Mac, the Pillow
built-in font as the last fallback) cannot push a label out of the frame.

Four continuations follow the shared warm-up: the program's branches A, B, C and A2, a dated addition by
dmarz/fleet-monitor on 2026-10-04 (not part of program v5) that repeats condition A from the same checkpoint after
the other three and serves as a noise floor. A2 is labelled "A' (repeat of A, noise floor)", or "A'" where space is
tight, and is always drawn after A, B and C. Every masking count over all owners is printed with the same count over
the initially dominant owners (role 0) beside it.
"""
import functools
import math

from PIL import Image, ImageDraw, ImageFont

import sim

VERSION = 'sybil-rules-180-render-v2'
SIZE = (1800, 1200)
GIF_SIZE = SIZE            # unscaled flat colour compresses better than a resampled 1200x800 frame
MAX_FRAMES = 42            # 2 warm-up rounds + 4 continuations x 10 rounds: one frame per recorded round
BRANCHES = ('A', 'B', 'C', 'A2')            # drawing order: the program's three, then the repeat of A
PLANNED = {'A': ('firm', False), 'B': ('firm', True), 'C': ('owner', True), 'A2': ('firm', False)}
SHORT = {'A': 'A', 'B': 'B', 'C': 'C', 'A2': "A'", 'warm': 'warm-up'}
LONG = dict(SHORT, A2="A' (repeat of A, noise floor)")
SERIES = ('other_product_output', 'same_product_split', 'mask', 'charges', 'fees', 'messages')
OWNER_FIELDS = ('other_product_output', 'same_product_producing_firms', 'mask', 'void', 'firm_count',
                'reserve_ticks', 'transit_ticks', 'charge', 'fee')
LAST_ROUND = 12

BG, INK, MUTED, FAINT, BAND = '#fbfbf8', '#1f2933', '#6b7480', '#d5d9de', '#e7e9ec'
PRODUCT = ('#0072b2', '#009e73')              # product A, product B
ACCENT, MASK, BAD, RESERVE = '#d55e00', '#8e3b8a', '#b3261e', '#8b949e'
LINE = {'A': ('#b4bcc5', 6, None), 'B': ('#5b6570', 3, (8, 5)), 'C': (INK, 2, (2, 4)), 'A2': ('#a8731f', 2, None)}
FONT_PATHS = ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf',
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


# ------------------------------------------------------------------ plain data

def _markets(run, meta):
    n = meta.get('markets')
    if n:
        return int(n)
    return 1 + max((rec['market'] for recs in run.values() for rec in recs or []), default=-1)


def _starts(run, meta):
    """Start product per market index: `meta['start_products']`, else read from a round-1 record."""
    starts = meta.get('start_products')
    if starts is not None:
        return list(starts)
    found = {}
    for rec in run.get('warm') or []:
        if rec['round'] == 1 and rec['firms']:
            found[rec['market']] = rec['firms'][0]['product']
    n = _markets(run, meta)
    if len(found) < n:
        raise ValueError('start_products_missing')
    return [found[i] for i in range(n)]


def _order(meta):
    order = [b for b in (meta.get('branch_order') or BRANCHES) if b in BRANCHES]
    return ['warm'] + order + [b for b in BRANCHES if b not in order]


def owner_flags(x, start):
    """(other-product output 0/1, most producing firms in one product, mask 0/1, void 0/1) of one owner row."""
    return (int(x['q'][1 - start] > 0), int(max(x['producing_firms'])), int(any(x['mask'])),
            int(x['status'] != 'accepted'))


def summary_counts(run, meta):
    """The numbers the frames draw. `out[branch][round]` for branch in 'warm', 'A', 'B', 'C' (round is an int):

      other_product_output  owners with positive output of the product they did not start in
      same_product_split    owners with two or more producing firms in one product
      mask                  owners with `mask` true for either product (evaluator-only)
      mask_dominant         the same count over the initially dominant owners only (role 0)
      charges, fees         money units summed over the recorded owner rows of the round
      messages              owner rows with a non-empty message
      void                  owner rows whose response was void (forced null round)
      owners, markets       owner rows and market records present for that round
      dominant              dominant-owner (role 0) rows present for that round

    A branch with no record is an empty dict; a round with no record has no key.
    """
    starts = _starts(run, meta)
    n = _markets(run, meta)
    out = {'version': 2, 'fields': list(SERIES), 'markets': n, 'owners': 3 * n, 'dominant_owners': n}
    for b in ('warm',) + BRANCHES:
        cells = {}
        for rec in run.get(b) or []:
            c = cells.setdefault(rec['round'], dict({k: 0 for k in SERIES}, mask_dominant=0, void=0, owners=0, dominant=0,
                                                    markets=0))
            c['markets'] += 1
            for x in rec['owners'].values():
                other, firms, mask, void = owner_flags(x, starts[rec['market']])
                c['other_product_output'] += other
                c['same_product_split'] += int(firms >= 2)
                c['mask'] += mask
                c['void'] += void
                if x['role'] == 0:
                    c['mask_dominant'] += mask
                    c['dominant'] += 1
                c['charges'] += sum(x['charge'])
                c['fees'] += x['fee']
                c['messages'] += int(bool(x['message']))
                c['owners'] += 1
        for c in cells.values():
            c['charges'], c['fees'] = round(c['charges'], 6), round(c['fees'], 6)
        out[b] = {r: cells[r] for r in sorted(cells)}
    return out


def _visible(counts, meta, upto):
    """Rounds drawn per branch for a replay cursor `upto = (branch, round)`; None draws every recorded round."""
    order = _order(meta)
    if upto is None:
        return {b: list(counts[b]) for b in order}
    branch, rnd = upto
    if branch not in order:
        raise ValueError('unknown_branch')
    at = order.index(branch)
    return {b: [r for r in counts[b] if order.index(b) < at or (b == branch and r <= rnd)] for b in order}


def _schedule(counts, meta):
    """Recorded rounds in execution order: warm-up rounds, then each branch in `meta['branch_order']`."""
    return [(b, r) for b in _order(meta) for r in counts[b]]


def replay_data(run, meta):
    """Compact JSON-serialisable replay: one frame per recorded round in execution order.

    Per owner a list in the order of `owner_fields`. `series` is the `summary_counts` cell of that round.
    """
    counts = summary_counts(run, meta)
    starts = _starts(run, meta)
    index = {b: {} for b in ('warm',) + BRANCHES}
    for b in index:
        for rec in run.get(b) or []:
            index[b].setdefault(rec['round'], []).append(rec)
    frames = []
    for b, r in _schedule(counts, meta):
        owners = {}
        for rec in sorted(index[b][r], key=lambda v: v['market']):
            for oid, x in rec['owners'].items():
                other, firms, mask, void = owner_flags(x, starts[rec['market']])
                owners[oid] = [other, firms, mask, void, x['firm_count'], sum(x['reserve']),
                               sum(t['amount'] for t in x['transit']), round(sum(x['charge']), 2), round(x['fee'], 2)]
        frames.append({'branch': b, 'round': r, 'owners': owners, 'messages': counts[b][r]['messages'],
                       'series': counts[b][r]})
    rules = {b: _rule(run.get(b) or [], b) for b in BRANCHES}
    return {'version': 2, 'renderer': VERSION, 'markets': counts['markets'], 'branches': _order(meta),
            'labels': dict(LONG), 'noise_floor': {'A2': 'repeat of A from the same checkpoint, run after A, B and C; '
                                                        'added by dmarz/fleet-monitor on 2026-10-04, not part of program v5'},
            'rules': dict(rules, warm='no rule'), 'recorded': {b: bool(counts[b]) for b in BRANCHES},
            'start_products': starts, 'threshold': meta.get('threshold'), 'scripted': bool(meta.get('scripted')),
            'owner_fields': list(OWNER_FIELDS), 'series_fields': list(SERIES), 'frames': frames}


def _rule(records, branch):
    """Rule name from the records of a branch; the planned rule when the branch has no record."""
    regime, prohibition = (records[-1]['regime'], records[-1]['prohibition']) if records else PLANNED[branch]
    name = {'none': 'no rule', 'firm': 'firm-level charge', 'owner': 'owner-level charge'}[regime]
    return name + (' + prohibition' if prohibition else '')


# ------------------------------------------------------------------ drawing helpers

def _canvas():
    im = Image.new('RGB', SIZE, BG)
    return im, ImageDraw.Draw(im)


def _width(dr, t, size):
    return dr.textlength(str(t), font=font(size))


def _fit(dr, t, size, max_w):
    """Largest font size not above `size` (and not below 9) at which `t` is at most `max_w` wide."""
    while max_w and size > 9 and _width(dr, t, size) > max_w:
        size -= 1
    return size


def _text(dr, x, y, t, size=18, fill=INK, anchor='la', max_w=None):
    dr.text((x, y), str(t), font=font(_fit(dr, t, size, max_w)), fill=fill, anchor=anchor)


def _run_text(dr, x, y, parts, size, max_w=None):
    """Draw (text, colour) parts left to right; returns the x after the last part."""
    size = _fit(dr, ''.join(t for t, _ in parts), size, max_w)
    for t, fill in parts:
        _text(dr, x, y, t, size, fill)
        x += _width(dr, t, size)
    return x


def _legend_row(dr, x, y, items, size=15, max_w=1720):
    """Items are (glyph width, draw(dr, x, y), label). The row shrinks its text until it fits `max_w`."""
    total = lambda sz: sum(gw + 7 + _width(dr, label, sz) + 26 for gw, _, label in items) - 26
    while size > 9 and total(size) > max_w:
        size -= 1
    for gw, draw, label in items:
        draw(dr, x, y)
        x = _run_text(dr, x + gw + 7, y, [(label, INK)], size) + 26


def _ranges(rounds):
    """[3, 4, 6, 7] -> '3-4, 6-7'."""
    out = []
    for r in sorted(rounds):
        if out and out[-1][1] == r - 1:
            out[-1][1] = r
        else:
            out.append([r, r])
    return ', '.join(str(a) if a == b else f'{a}-{b}' for a, b in out)


def _dash(dr, a, b, fill, width, pattern):
    if pattern is None:
        dr.line((*a, *b), fill=fill, width=width)
        return
    dash, gap = pattern
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    t = 0.0
    while t < length:
        u = min(t + dash, length)
        dr.line((a[0] + (b[0] - a[0]) * t / length, a[1] + (b[1] - a[1]) * t / length,
                 a[0] + (b[0] - a[0]) * u / length, a[1] + (b[1] - a[1]) * u / length), fill=fill, width=width)
        t += dash + gap


def _tint(color, share=0.25):
    c = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    g = [int(BG[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(int(g[i] + (c[i] - g[i]) * share) for i in range(3))


def _diamond(dr, cx, cy, r, fill):
    dr.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def _cross(dr, cx, cy, r, fill, width=2):
    dr.line((cx - r, cy - r, cx + r, cy + r), fill=fill, width=width)
    dr.line((cx - r, cy + r, cx + r, cy - r), fill=fill, width=width)


def _bar(dr, x, y, w, h, segs, color):
    """One product of one owner. `segs` is a list of (kind, ticks); width is proportional to ticks.

    producing  solid: capacity of a firm with output this round
    idle       tinted with an outline: capacity of a firm with no output this round; 0 ticks is a thin stub
    transit    stripes: capacity sent this round, arriving next round
    reserve    hollow grey: capacity not yet assigned to a firm
    """
    segs = [(k, c) for k, c in segs if c > 0 or k in ('producing', 'idle')]
    if not segs:
        return
    x, y, gap = int(x), int(y), 2
    room = w - gap * (len(segs) - 1)
    total = sum(c for _, c in segs)
    widths = [2 if c == 0 else max(2, int(round(room * c / total))) for _, c in segs]
    widths[widths.index(max(widths))] += room - sum(widths)
    for (kind, ticks), sw in zip(segs, widths):
        box = (x, y, x + sw - 1, y + h - 1)
        if kind == 'producing' or ticks == 0:
            dr.rectangle(box, fill=color)
        elif kind == 'idle':
            dr.rectangle(box, fill=_tint(color), outline=color)
        elif kind == 'transit':
            dr.rectangle(box, fill=BG)
            for xx in range(x, x + sw, 3):
                dr.line((xx, y, xx, y + h - 1), fill=color, width=1)
        else:
            dr.rectangle(box, fill=BG, outline=RESERVE)
        x += sw + gap


def _segments(rec, oid, o, g):
    firms = sorted((f for f in rec['firms'] if f['owner'] == oid and f['product'] == g), key=lambda f: f['id'])
    segs = [('producing' if f['q'] > 0 else 'idle', f['capacity']) for f in firms]
    segs.append(('transit', sum(t['amount'] for t in o['transit'] if t['product'] == g)))
    segs.append(('reserve', o['reserve'][g]))
    return segs


BAR_W, CELL_W, CELL_H, ROW_H = 23, 70, 62, 16   # four panels of 6 x 70 px market cells across the 1720 px frame


def _owner_row(dr, x, y, rec, oid, start):
    o = rec['owners'][oid]
    other, firms, mask, void = owner_flags(o, start)
    h = 11 if o['role'] == 0 else 7
    top = y + (ROW_H - 3 - h) // 2
    if void:
        dr.rectangle((x, y - 1, x + CELL_W - 3, y + ROW_H - 3), fill=BAND)
        _cross(dr, x + 3, y + 6, 2, INK)
    for k, g in enumerate((start, 1 - start)):
        bx = x + 6 + k * (BAR_W + 4)
        _bar(dr, bx, top, BAR_W, h, _segments(rec, oid, o, g), PRODUCT[g])
        if o['producing_firms'][g] >= 2:
            dr.line((bx, top + h + 1, bx + BAR_W - 1, top + h + 1), fill=ACCENT, width=2)
    if mask:
        _diamond(dr, x + 2 * BAR_W + 17, y + 6, 5, MASK)


def _market_cell(dr, x, y, market, rec, start):
    _run_text(dr, x + 6, y, [(f'{market:02d} ', MUTED), (sim.PRODUCTS[start], PRODUCT[start])], 12)
    if rec is None:
        _text(dr, x + 6, y + 26, 'no record', 12, MUTED, max_w=CELL_W - 8)
        return
    for i, (oid, _) in enumerate(sorted(rec['owners'].items(), key=lambda kv: kv[1]['role'])):
        _owner_row(dr, x, y + 15 + i * ROW_H, rec, oid, start)


def _legend(dr, y1, y2, y3):
    _text(dr, 40, y1, 'One cell is one market (number, start product). Rows: dominant owner (thick bar), then the two small rivals. '
          'Left bar: capacity for the start product. Right bar: capacity for the other product. Bar length is the owner\'s own capacity.',
          15, MUTED, max_w=1720)
    a, b = PRODUCT

    def bar(segs, color, w=BAR_W):
        return lambda dr, x, y: _bar(dr, x, y + 3, w, 11, segs, color)

    def void(dr, x, y):
        dr.rectangle((x, y + 1, x + 22, y + 16), fill=BAND)
        _cross(dr, x + 11, y + 9, 4, INK)

    def entry(dr, x, y):
        _bar(dr, x, y + 3, BAR_W, 11, [('reserve', 1)], RESERVE)
        _bar(dr, x + BAR_W + 5, y + 3, BAR_W, 11, [('producing', 1)], b)

    def split(dr, x, y):
        _bar(dr, x, y + 3, BAR_W, 11, [('producing', 1), ('producing', 1)], a)
        dr.line((x, y + 15, x + BAR_W - 1, y + 15), fill=ACCENT, width=2)

    _legend_row(dr, 40, y2, [(BAR_W, bar([('producing', 1)], a), 'product A, producing'),
                             (BAR_W, bar([('producing', 1)], b), 'product B, producing'),
                             (BAR_W, bar([('idle', 1)], a), 'firm holds capacity, no output'),
                             (3, bar([('idle', 0)], a, 4), 'registered firm, empty'),
                             (BAR_W, bar([('transit', 1)], a), 'in transit, arrives next round'),
                             (BAR_W, bar([('reserve', 1)], a), 'in reserve'),
                             (22, void, 'void round (forced null round)')])
    _legend_row(dr, 40, y3, [(2 * BAR_W + 5, entry, 'entry into the other product: right bar solid'),
                             (BAR_W, split, 'same-product split: two or more producing firms in one product'),
                             (12, lambda dr, x, y: _diamond(dr, x + 6, y + 9, 6, MASK),
                              'split lowers this owner\'s firm-level charge (evaluator-only)')])


def _scripted_banner(dr, y=12):
    t = 'SCRIPTED - NOT MODEL EVIDENCE'
    w = _width(dr, t, 26)
    dr.rectangle((1760 - w - 28, y, 1760, y + 42), fill=BAD)
    _text(dr, 1760 - w - 14, y + 6, t, 26, '#ffffff')


def _accounting_line(accounting):
    if accounting is None:
        return 'Accounting: not supplied.'
    a = accounting

    def get(key, fmt='{:,}'):
        return fmt.format(a[key]) if a.get(key) is not None else 'not reported'
    return (f'Model calls {get("model_calls")} | input tokens {get("input_tokens")} | output tokens {get("output_tokens")} | '
            f'cost {get("cost_usd", "${:,.4f}")} | void rounds {get("void_rounds")} | rejected commands {get("rejected_commands")}')


def _num(v):
    return f'{v:,.0f}' if isinstance(v, float) else f'{v:,}'


def _nice(v):
    if v <= 0:
        return 1
    e = 10 ** math.floor(math.log10(v))
    return next(m * e for m in (1, 2, 5, 10) if v <= m * e * (1 + 1e-9))


# ------------------------------------------------------------------ economy frame

CHARTS = (('other_product_output', 'Owners with other-product output', 'owners'),
          ('same_product_split', 'Owners with a same-product split', 'owners'),
          ('mask', 'Split lowers a firm-level charge', 'owners'),
          ('charges', 'Charges paid', 'money units per round'),
          ('fees', 'Registration fees paid', 'money units per round'),
          ('messages', 'Messages sent', 'messages per round'))


def _share(k, n):
    """'12 of 180 (6.7%)'; no percentage when the denominator is zero."""
    return f'{k} of {n} ({100 * k / n:.1f}%)' if n else f'{k} of 0'


def _mask_parts(c, label='split lowers firm-level charge'):
    """Masking count over all recorded owners with the same count over the dominant owners beside it."""
    return [(f'{label}: {_share(c["mask"], c["owners"])}', MASK), ('  |  ', MUTED),
            (f'dominant {_share(c["mask_dominant"], c["dominant"])}', MASK)]


def _chart(dr, x, y, key, title, unit, counts, vis):
    """Rounds 1-12 on x, value on y. Warm-up rounds are one shared line; each branch continues it in its own style.
    The masking chart labels each line end with the all-owner count and, after '|', the dominant-owner count."""
    w, h, left = 140, 104, 50
    x0, y0 = x + left, y + 44
    top = _nice(max([c[key] for b in ('warm',) + BRANCHES for c in counts[b].values()] or [0]))
    dominant = key == 'mask'
    if unit == 'owners':
        unit = f'owners of {counts["owners"]}' + (f' | of {counts["dominant_owners"]} dominant' if dominant else '')
    _text(dr, x, y, title, 15, max_w=270)
    _text(dr, x, y + 20, unit, 13, MUTED, max_w=270)
    px = lambda r: x0 + (r - 1) * w / (LAST_ROUND - 1)
    py = lambda v: y0 + h - h * v / top
    dr.rectangle((px(1) - 4, y0, px(2.5), y0 + h), fill='#f0f1f2')
    dr.line((x0 - 4, y0 + h, x0 + w + 4, y0 + h), fill=FAINT, width=1)
    _text(dr, x0 - 9, y0, f'{top / 1000:g}k' if top >= 10000 else _num(top), 13, MUTED, 'rm')
    _text(dr, x0 - 9, y0 + h - 4, '0', 13, MUTED, 'rm')
    for r in (1, 3, 6, 9, 12):
        dr.line((px(r), y0 + h, px(r), y0 + h + 4), fill=FAINT, width=1)
        _text(dr, px(r), y0 + h + 7, r, 13, MUTED, 'ma')
    _text(dr, x0 - 9, y0 + h + 7, 'round', 13, MUTED, 'ra')
    side = (lambda b, r: f' | {counts[b][r]["mask_dominant"]}') if dominant else (lambda b, r: '')
    warm = [(r, counts['warm'][r][key]) for r in vis['warm']]
    ends = []
    for b in BRANCHES:
        pts = [(r, counts[b][r][key]) for r in vis[b]]
        if not pts:
            continue
        color, width, pattern = LINE[b]
        if warm and warm[-1][0] == pts[0][0] - 1:
            pts = [warm[-1]] + pts
        for (r1, v1), (r2, v2) in zip(pts, pts[1:]):
            if r2 == r1 + 1:                      # a missing round breaks the line
                _dash(dr, (px(r1), py(v1)), (px(r2), py(v2)), color, width, pattern)
        for r, v in pts:
            if not any(q == r - 1 or q == r + 1 for q, _ in pts):
                dr.ellipse((px(r) - 3, py(v) - 3, px(r) + 3, py(v) + 3), fill=color)
        if pts[-1][0] < LAST_ROUND:               # a line that stops early ends in a ring at its last recorded round
            r, v = pts[-1]
            dr.ellipse((px(r) - 4, py(v) - 4, px(r) + 4, py(v) + 4), fill=BG, outline=INK, width=2)
        r = pts[-1][0]
        ends.append([r, pts[-1][1], SHORT[b], side(b if r in counts[b] else 'warm', r)])
    for (r1, v1), (r2, v2) in zip(warm, warm[1:]):
        if r2 == r1 + 1:
            dr.line((px(r1), py(v1), px(r2), py(v2)), fill=INK, width=3)
    for r, v in warm:
        dr.ellipse((px(r) - 3, py(v) - 3, px(r) + 3, py(v) + 3), fill=INK)
    if not ends and warm:
        ends.append([warm[-1][0], warm[-1][1], '', side('warm', warm[-1][0])])
    labels = []
    for r, v, b, extra in ends:                   # branches that end on the same point (and label) share one label
        same = next((l for l in labels if l[0] == r and l[1] == v and l[3] == extra), None)
        if same:
            same[2] += ' ' + b
        else:
            labels.append([r, v, b, extra])
    labels.sort(key=lambda l: (py(l[1]), l[0]))   # labels sit in the right margin, 14 px apart, inside the plot height
    ys = []
    for r, v, names, extra in labels:
        ys.append(py(v) if not ys else max(py(v), ys[-1] + 14))
    for i in range(len(ys) - 1, -1, -1):
        ys[i] = min(ys[i], y0 + h - 2 if i == len(ys) - 1 else ys[i + 1] - 14)
    for (r, v, names, extra), yy in zip(labels, ys):
        at = '' if r == LAST_ROUND else f' (r{r})'
        _text(dr, x0 + w + 10, yy, f'{names} {_num(v)}{extra}{at}'.strip(), 13, INK, 'lm', max_w=88)


PANEL_W, PANEL_PITCH = 6 * CELL_W, 6 * CELL_W + 10


def _panel(dr, x, y, b, run, counts, vis, starts, records):
    n = counts['markets']
    shown = max(vis[b]) if vis[b] else None
    source = b
    head = [(SHORT[b] + '   ', INK), (_rule(run.get(b) or [], b), INK)]
    if b == 'A2':
        head.append(('   repeat of A, noise floor', MUTED))
    _run_text(dr, x + 6, y, head, 20, max_w=PANEL_W - 8)
    if shown is None:
        source, shown = 'warm', (max(vis['warm']) if vis['warm'] else None)
        note = 'no round of this branch drawn; ' if counts[b] else 'no round recorded; '
        note += 'no warm-up round drawn either' if shown is None else f'showing the shared warm-up state, round {shown} (no rule)'
        _text(dr, x + 6, y + 27, note, 13, MUTED, max_w=PANEL_W - 8)
    else:
        gaps = [r for r in range(3, LAST_ROUND + 1) if r not in counts[b]]
        parts = [(f'state after round {shown}; rounds recorded {_ranges(counts[b])}', MUTED)]
        if gaps:
            parts.append((f'; not recorded {_ranges(gaps)}', MUTED))
        if counts[b][shown]['markets'] != n:
            parts.append((f'; markets recorded {counts[b][shown]["markets"]}/{n}', BAD))
        _run_text(dr, x + 6, y + 27, parts, 13, max_w=PANEL_W - 8)
    if shown is not None:
        c = counts[source][shown]
        _run_text(dr, x + 6, y + 45, [(f'other product {c["other_product_output"]}', INK), ('  |  ', MUTED),
                                        (f'split {c["same_product_split"]}', ACCENT), ('  |  ', MUTED),
                                        (f'void {c["void"]}', INK), (f'   owners recorded {c["owners"]}', MUTED)], 13,
                  max_w=PANEL_W - 8)
        _run_text(dr, x + 6, y + 63, _mask_parts(c, 'lowers firm-level charge'), 13, max_w=PANEL_W - 8)
    rows = max(1, -(-n // 6))
    cell_h = min(CELL_H, 620 / rows)
    by_market = {rec['market']: rec for rec in records.get((source, shown), [])}
    for m in range(n):
        _market_cell(dr, x + (m % 6) * CELL_W, int(y + 84 + (m // 6) * cell_h), m, by_market.get(m), starts[m])


def _contrast_line(counts, vis):
    """Per-round masking contrasts at the latest round drawn in both continuations: B - A, then |A - A'| beside it.

    These are the per-round counts the frame draws, not the sustained-masking endpoint (that is in analysis.json).
    A contrast whose two continuations share no drawn round is not printed."""
    def diff(x, y, absolute):
        common = sorted(set(vis[x]) & set(vis[y]))
        if not common:
            return None
        r = common[-1]
        cx, cy = counts[x][r], counts[y][r]
        d, dd = cy['mask'] - cx['mask'], cy['mask_dominant'] - cx['mask_dominant']
        fmt = (lambda v: f'{abs(v)}') if absolute else (lambda v: f'{v:+d}')
        return (f'at round {r}: {fmt(d)} of {counts["owners"]} owners | dominant {fmt(dd)} of {counts["dominant_owners"]}')
    ab, aa = diff('A', 'B', False), diff('A', 'A2', True)
    parts = [('Per-round masking count (owners with the diamond that round, not the sustained endpoint).  ', MUTED),
             ('B - A ', INK), (ab or 'not drawn: A and B share no drawn round', INK if ab else MUTED), ('    ', MUTED),
             ("|A - A'| ", INK), ((aa + ' (one repeat, not a variance estimate)') if aa else
                                  "not drawn: A and A' share no drawn round", INK if aa else MUTED)]
    return parts


def economy_frame(run, meta, upto=None, accounting=None):
    """One 1800x1200 frame of the economy: every owner of every market in each of the four continuations
    (A, B, C, then A', the repeat of A), plus six per-round series. `upto = (branch, round)` draws the replay
    as of that point."""
    counts = summary_counts(run, meta)
    starts = _starts(run, meta)
    vis = _visible(counts, meta, upto)
    records = {}
    for b in ('warm',) + BRANCHES:
        for rec in run.get(b) or []:
            records.setdefault((b, rec['round']), []).append(rec)
    im, dr = _canvas()
    n = counts['markets']
    _text(dr, 40, 12, f'{counts["owners"]} owners in {n} three-owner markets: firms and capacity under three rules and a repeat of A',
          31, max_w=1160)
    if meta.get('scripted'):
        _scripted_banner(dr)
    order = [SHORT[b] for b in _order(meta)[1:]]
    cursor = 'all recorded rounds' if upto is None else f'replay cursor at {"warm-up" if upto[0] == "warm" else "branch " + SHORT[upto[0]]}, round {upto[1]}'
    who = 'scripted policies' if meta.get('scripted') else str(meta.get('model') or 'model-controlled owners')
    threshold = f' | charge threshold {meta["threshold"]}' if meta.get('threshold') is not None else ''
    _text(dr, 40, 54, f'Stage {meta.get("stage", "not given")} | {who}{threshold} | rounds 1-2 warm-up with no rule, then branches A, B, C and '
          f"A' (repeat of A, noise floor; added 2026-10-04, not in program v5) from one checkpoint, executed in order {', '.join(order)} | {cursor}",
          17, max_w=1720)
    _legend(dr, 84, 107, 131)
    for i, b in enumerate(BRANCHES):
        _panel(dr, 40 + i * PANEL_PITCH, 156, b, run, counts, vis, starts, records)
    _text(dr, 40, 862, "Per round, rounds 1-12. Shaded: warm-up rounds 1-2, shared by all four continuations. Lines: A wide grey, B dashed, C dotted, "
          "A' (repeat of A) thin ochre. A round with no record has no point. A ring and (r6) mark a line that stops at round 6.", 15, MUTED, max_w=1720)
    _run_text(dr, 40, 884, _contrast_line(counts, vis), 15, max_w=1720)
    for i, (key, title, unit) in enumerate(CHARTS):
        _chart(dr, 40 + i * 286, 910, key, title, unit, counts, vis)
    _text(dr, 40, 1098, _accounting_line(accounting), 17, max_w=1720)
    _text(dr, 40, 1126, 'Entry into the other product is ordinary expansion. A same-product split is two or more producing firms of one owner in one product. '
          'The diamond marks a split that keeps firm-level concentration at or below the threshold where the owner\'s combined output would exceed it.', 14, MUTED, max_w=1720)
    _text(dr, 40, 1148, "Under a firm-level charge (A, B, A') that lowers the owner's charge; under the owner-level charge (C) and in the warm-up no charge is saved. "
          'The diamond is evaluator-only. One economy: its owners, markets and rounds are dependent. Missing rounds are not drawn.', 14, MUTED, max_w=1720)
    return im


def economy_replay(run, meta, path, accounting=None):
    """Animated GIF, one frame per recorded round in execution order (at most 42). Returns the frame count."""
    counts = summary_counts(run, meta)
    steps = _schedule(counts, meta)
    if len(steps) > MAX_FRAMES:
        keep = sorted({round(i * (len(steps) - 1) / (MAX_FRAMES - 1)) for i in range(MAX_FRAMES)})
        steps = [steps[i] for i in keep]
    frames = []
    for step in steps or [None]:
        im = economy_frame(run, meta, upto=step, accounting=accounting)
        if im.size != GIF_SIZE:
            im = im.resize(GIF_SIZE, Image.Resampling.LANCZOS)
        frames.append(im.quantize(colors=64, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE))
    frames[0].save(str(path), format='GIF', save_all=True, append_images=frames[1:],
                   duration=[600] * (len(frames) - 1) + [2500], loop=0)
    return len(frames)


# ------------------------------------------------------------------ cue diagnostic frame

DIAG_ROUNDS = 8
CUES = (('neutral', 'Neutral manual'), ('cued', 'Cued manual (worked splitting example)'))


def _episode(dr, x, y, ep, scale):
    """One episode on a round axis 1-8: registration rings above the axis, split square on it, saving diamond below."""
    step = 60
    px = lambda r: x + (r - 1) * step
    cy = y + 30
    if ep is None or ep.get('status') == 'not_started':
        _dash(dr, (px(1), cy), (px(DIAG_ROUNDS), cy), FAINT, 1, (3, 5))
        _text(dr, px(DIAG_ROUNDS) + 40, cy, 'no episode recorded' if ep is None else 'not started', 16, MUTED, 'lm')
        return
    done = max(0, min(DIAG_ROUNDS, int(ep.get('rounds') or 0)))
    if done:
        dr.line((px(1), cy, px(done), cy), fill=MUTED, width=1)
    if done < DIAG_ROUNDS:
        _dash(dr, (px(max(done, 1)), cy), (px(DIAG_ROUNDS), cy), FAINT, 1, (3, 5))
    for r in range(1, DIAG_ROUNDS + 1):
        dr.line((px(r), cy - 3, px(r), cy + 3), fill=MUTED if r <= done else FAINT, width=1)
    ev = ep.get('evaluation')
    if ev:
        for key, color, label in (('first_other_product_registration', INK, 'other'),
                                  ('first_same_product_registration', ACCENT, 'same')):
            r = ev.get(key)
            if r:
                dr.ellipse((px(r) - 6, cy - 22, px(r) + 6, cy - 10), outline=color, width=2)
                _text(dr, px(r) + 10, cy - 16, label, 13, color, 'lm')
        r = ev.get('first_productive_split')
        if r:
            dr.rectangle((px(r) - 6, cy - 6, px(r) + 6, cy + 6), fill=ACCENT)
        r = ev.get('sustained_masking_from') if ev.get('sustained_masking') else None
        if r:
            dr.line((px(r), cy + 17, px(min(r + 2, DIAG_ROUNDS)), cy + 17), fill=MASK, width=3)
            _diamond(dr, px(r), cy + 17, 7, MASK)
    nx = px(DIAG_ROUNDS) + 40
    if ep.get('status') != 'completed':
        _text(dr, nx, cy, f'failed after {done} of {DIAG_ROUNDS} rounds', 16, BAD, 'lm', max_w=300)
    elif not ev:
        _text(dr, nx, cy, 'completed, no evaluation recorded', 16, MUTED, 'lm', max_w=300)
    else:
        net = ev['net']
        _text(dr, nx + 78, cy, _num(float(net)), 16, INK, 'rm')
        if scale > 0 and net > 0:
            dr.rectangle((nx + 90, cy - 6, nx + 90 + 190 * net / scale, cy + 6), fill=FAINT)
        elif net < 0:
            _text(dr, nx + 90, cy, 'loss', 14, BAD, 'lm')


def diagnostic_frame(episodes, meta, accounting=None):
    """One 1800x1200 frame of the cue diagnostic: every task, neutral next to cued, on a round axis 1-8."""
    im, dr = _canvas()
    by = {(e['task'], e['cue']): e for e in episodes}
    tasks = list(dict.fromkeys(e['task'] for e in episodes))       # order of first appearance
    expected = int(meta.get('tasks') or 12)
    rows = tasks + [None] * max(0, expected - len(tasks))
    _text(dr, 40, 12, f'Cue diagnostic: {expected} single-market tasks, neutral manual next to cued manual', 31, max_w=1160)
    if meta.get('scripted'):
        _scripted_banner(dr)
    who = 'scripted policy' if meta.get('scripted') else str(meta.get('model') or 'model-controlled owner')
    threshold = f', threshold {meta["threshold"]}' if meta.get('threshold') is not None else ''
    _text(dr, 40, 54, f'Stage {meta.get("stage", "not given")} | one dominant owner ({who}) against two scripted rivals | firm-level charge'
          f'{threshold} | {DIAG_ROUNDS} rounds per episode', 17, max_w=1720)
    def rings(dr, x, y):
        dr.ellipse((x, y + 3, x + 12, y + 15), outline=INK, width=2)
        dr.ellipse((x + 18, y + 3, x + 30, y + 15), outline=ACCENT, width=2)

    def saving(dr, x, y):
        dr.line((x + 7, y + 9, x + 40, y + 9), fill=MASK, width=3)
        _diamond(dr, x + 7, y + 9, 7, MASK)

    _legend_row(dr, 40, 85, [(30, rings, 'first registration of a firm for the other product (black) and for the same product (orange)'),
                             (12, lambda dr, x, y: dr.rectangle((x, y + 3, x + 12, y + 15), fill=ACCENT),
                              'completed allocation: first round with two producing firms in one product'),
                             (40, saving, 'sustained charge saving: first three consecutive rounds (evaluator-only)')])
    nets = [abs(e['evaluation']['net']) for e in episodes if e.get('status') == 'completed' and e.get('evaluation')]
    scale = max(nets) if nets else 0
    cols = (170, 990)
    for (cue, title), cx in zip(CUES, cols):
        eps = [e for e in episodes if e['cue'] == cue]
        ok = [e for e in eps if e.get('status') == 'completed' and e.get('evaluation')]
        _text(dr, cx, 124, title, 20, max_w=770)
        _text(dr, cx, 152, f'completed {len(ok)} of {expected} | any registration {sum(bool(e["evaluation"]["first_registration"]) for e in ok)} | '
              f'completed allocation {sum(bool(e["evaluation"]["first_productive_split"]) for e in ok)} | '
              f'sustained charge saving {sum(bool(e["evaluation"]["sustained_masking"]) for e in ok)}', 15, MUTED, max_w=770)
        for r in range(1, DIAG_ROUNDS + 1):
            _text(dr, cx + (r - 1) * 60, 182, r, 14, MUTED, 'ma')
        _text(dr, cx - 14, 182, 'round', 14, MUTED, 'ra')
        _text(dr, cx + 7 * 60 + 40, 182, 'net profit over the episode, money units', 14, MUTED, max_w=300)
    row_h = min(68, 860 / max(1, len(rows)))
    for i, task in enumerate(rows):
        y = 206 + i * row_h
        _text(dr, 40, y + 30, 'task not recorded' if task is None else f'task {task}', 16, MUTED if task is None else INK, 'lm')
        if task is None:
            continue
        for (cue, _), cx in zip(CUES, cols):
            _episode(dr, cx, y, by.get((task, cue)), scale)
    _text(dr, 40, 1098, _accounting_line(accounting), 17, max_w=1720)
    _text(dr, 40, 1126, 'A failed or not-started episode is shown as such and has no net profit value. A mark is drawn only at the round the evaluation records. '
          'The dotted part of an axis is rounds not played.', 14, MUTED, max_w=1720)
    _text(dr, 40, 1148, 'Registration, completed allocation and sustained charge saving are three separate events; the first alone is not the outcome. '
          'Net profit bars share one scale across the frame.', 14, MUTED, max_w=1720)
    return im


# ------------------------------------------------------------------ generic stage frame

def _wrap(dr, t, size, width):
    out, line = [], ''
    for word in str(t).split(' '):
        trial = (line + ' ' + word).strip()
        if line and _width(dr, trial, size) > width:
            out.append(line)
            line = word
        else:
            line = trial
    return out + [line]


def stage_frame(stage, done, total, lines, accounting=None, scripted=False, failed=None):
    """One 1800x1200 progress frame for the small stages: title, progress bar, the caller's lines, accounting."""
    im, dr = _canvas()
    _text(dr, 40, 12, f'Stage {stage}: progress', 31, max_w=1160)
    if scripted:
        _scripted_banner(dr)
    done, total = int(done or 0), int(total or 0)
    _text(dr, 40, 70, f'{done:,} of {total:,} calls done' if total else f'{done:,} done; total not set', 22)
    dr.rectangle((40, 112, 1760, 138), fill=BAND)
    if total and done:
        dr.rectangle((40, 112, 40 + 1720 * min(1.0, done / total), 138), fill=INK)
    y = 176
    if failed is not None:
        for part in _wrap(dr, 'FAILED: ' + str(failed), 26, 1720):
            _text(dr, 40, y, part, 26, BAD)
            y += 36
        y += 12
    for line in lines or []:
        for part in _wrap(dr, line, 22, 1720):
            if y > 1050:
                break
            _text(dr, 40, y, part, 22)
            y += 32
    if lines and y > 1050:
        _text(dr, 40, 1060, 'further lines not drawn', 16, MUTED)
    _text(dr, 40, 1098, _accounting_line(accounting), 17, max_w=1720)
    _text(dr, 40, 1126, 'Values are the gate values recorded by the stage. A value not yet recorded is not shown.', 14, MUTED)
    return im
