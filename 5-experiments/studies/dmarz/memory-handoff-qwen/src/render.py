"""Frames of a stage: the memory-state by handoff-policy grid filling in, plus the source-to-successor
trace of the most recent assignment. Mapping v1 (VISUALIZATION.md). Uses recorded rows only;
evaluator labels appear in frames and never in a successor's message. Rendering reads no random
stream and changes nothing the successor sees.
"""
from PIL import Image, ImageDraw, ImageFont

import sim

W, H = 1420, 800
BG, INK, MUTED, LINE = (245, 244, 239), (29, 33, 38), (96, 102, 110), (208, 208, 200)
COLORS = {'correct': (47, 111, 143), 'abstain': (190, 190, 182), 'inherited_error': (200, 85, 61), 'other_wrong': (107, 76, 122)}
LEGEND = (('correct', 'correct (hidden truth)'), ('abstain', 'null (unresolved)'), ('inherited_error', 'inherited error'),
          ('other_wrong', 'other wrong value'), ('failed', 'no valid answer'), ('not_started', 'not started'))
POLICY_TITLES = {'raw': 'raw inheritance', 'metadata': 'metadata only', 'content': 'content-bound', 'reset': 'reset'}
STATE_TITLES = {'clean': 'clean', 'misquote': 'misquoted source', 'stale': 'stale version', 'copies': 'copies as independent',
                'contradiction': 'equal contradiction', 'false_original': 'false original'}


def font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:               # older Pillow: fixed bitmap font
        return ImageFont.load_default()


def square(draw, x, y, s, row):
    box = [x, y, x + s, y + s]
    status = row['status'] if row else 'not_started'
    if status == 'completed':
        draw.rectangle(box, fill=COLORS[row['evaluation']['outcome']])
        if row['evaluation']['supported']:
            draw.line([x, y + s + 3, x + s, y + s + 3], fill=INK, width=2)     # underline: supported by the message
    elif status == 'failed':
        draw.rectangle(box, fill=(255, 255, 255), outline=INK, width=2)
        draw.line([x, y, x + s, y + s], fill=INK, width=2); draw.line([x, y + s, x + s, y], fill=INK, width=2)
    else:
        draw.rectangle(box, outline=LINE, width=1)


def trace(row):
    """Source-to-successor lines for one recorded row."""
    if not row:
        return ['No assignment has finished yet.']
    p = row.get('packet_summary') or {}
    lines = [f'{row["id"]}   root {row["root"]} ({row["family"]})   memory: {STATE_TITLES[row["state"]]}   handoff: {POLICY_TITLES[row["policy"]]}',
             f'source store: {p.get("source", "-")}',
             f'predecessor note: {p.get("note", "-")}',
             f'handoff added: {p.get("added", "-")}']
    if row['status'] == 'completed':
        value = row['answer']['value']
        lines.append(f'successor: {"null" if value is None else value}   reference: {p.get("reference", "-")}   hidden truth: {p.get("truth_answer", "-")}'
                     f'   -> {row["evaluation"]["outcome"].replace("_", " ")}{", supported" if row["evaluation"]["supported"] else ", not supported"}')
    else:
        lines.append(f'successor: no outcome ({row.get("error") or row["status"]}); the cell keeps this assignment with unknown outcome')
    return lines


def frame(rows, assigned, stage, elapsed=None, accounting=None, scripted=False, headline=None):
    """`assigned`: every assignment of the stage (id, state, policy, root); `rows`: recorded rows so far."""
    img = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(img)
    f_title, f_text, f_small = font(26), font(16), font(13)
    by_id = {r['id']: r for r in rows}
    done = sum(r['status'] == 'completed' for r in rows); failed = sum(r['status'] == 'failed' for r in rows)
    d.text((32, 22), f'memory-handoff-qwen  {stage}', font=f_title, fill=INK)
    label = 'SCRIPTED - NOT MODEL EVIDENCE' if scripted else 'model answers as recorded'
    bits = [label, f'{done} of {len(assigned)} answered', f'{failed} without a valid answer']
    if accounting:
        bits.append(f'{accounting.get("attempted_calls", 0)} calls in the study ledger, USD {accounting.get("actual_usd", 0):.4f}')
    if elapsed is not None:
        bits.append(f'{elapsed:.0f} s')
    d.text((32, 60), '   |   '.join(bits), font=f_text, fill=MUTED)

    left, top, cell_w, cell_h = 232, 128, 236, 72
    for j, policy in enumerate(sim.POLICIES):
        d.text((left + j * cell_w + 8, top - 28), POLICY_TITLES[policy], font=f_text, fill=INK)
    for i, state in enumerate(sim.STATES):
        y = top + i * cell_h
        d.text((32, y + 22), STATE_TITLES[state], font=f_text, fill=INK)
        d.line([32, y, left + 4 * cell_w, y], fill=LINE, width=1)
        for j, policy in enumerate(sim.POLICIES):
            group = [a for a in assigned if a['state'] == state and a['policy'] == policy]
            group.sort(key=lambda a: (a['root'], a['id']))
            per_line = 12; s = 14
            for k, a in enumerate(group):
                square(d, left + j * cell_w + 8 + (k % per_line) * (s + 4), y + 10 + (k // per_line) * (s + 10), s, by_id.get(a['id']))
    d.line([32, top + 6 * cell_h, left + 4 * cell_w, top + 6 * cell_h], fill=LINE, width=1)

    x0 = left + 4 * cell_w + 16; y = top - 28
    d.text((x0, y), 'one square = one', font=f_small, fill=MUTED); y += 16
    d.text((x0, y), 'assignment', font=f_small, fill=MUTED); y += 26
    for key, text in LEGEND:
        probe = {'status': 'completed', 'evaluation': {'outcome': key, 'supported': 0}} if key in COLORS else {'status': key}
        square(d, x0, y, 12, probe); d.text((x0 + 20, y - 2), text, font=f_small, fill=INK); y += 22
    d.line([x0, y + 8, x0 + 12, y + 8], fill=INK, width=2); d.text((x0 + 20, y), 'underline: supported', font=f_small, fill=INK); y += 30
    if headline:
        for text in headline:
            d.text((x0, y), text, font=f_small, fill=INK); y += 18

    y = top + 6 * cell_h + 24
    d.text((32, y), 'Source to successor, most recent assignment', font=f_text, fill=INK); y += 26
    latest = max(rows, key=lambda r: r.get('completion_index', 0)) if rows else None
    for text in trace(latest):
        d.text((32, y), text[:150], font=f_small, fill=INK if text.startswith('successor') else MUTED); y += 20
    return img


def replay(rows, assigned, out, stage, scripted=False, headline=None, max_frames=24):
    """Time-ordered replay of the stage as an animated GIF; returns the number of frames."""
    ordered = sorted(rows, key=lambda r: r.get('completion_index', 0))
    n = len(ordered)
    steps = sorted({max(1, round(n * k / max_frames)) for k in range(1, max_frames + 1)}) if n else []
    frames = [frame([], assigned, stage, scripted=scripted)]
    for k in steps:
        last = k == n
        frames.append(frame(ordered[:k], assigned, stage, elapsed=ordered[k - 1].get('elapsed_seconds'),
                            accounting=ordered[k - 1].get('study_accounting') or None, scripted=scripted,
                            headline=headline if last else None))
    palette = [f.convert('P', palette=Image.ADAPTIVE, colors=32) for f in frames]
    palette[0].save(out / 'replay.gif', save_all=True, append_images=palette[1:], duration=[500] * (len(palette) - 1) + [2500], loop=0)
    return len(frames)
