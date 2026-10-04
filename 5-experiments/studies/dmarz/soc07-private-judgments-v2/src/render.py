"""Progress frames and the completion replay (visualization mapping v1, reviews/chain-001-pre.md).

Every bar is a measured count over assigned episodes. A cell with no terminal episode yet is
drawn as 'pending', never as zero. Rendering reads episode records only; it has no access to
agent contexts and makes no model call. Time in the replay is the count of completed blocks.
"""
from PIL import Image, ImageDraw, ImageFont

import config

W, H = 1800, 1200
BG, INK, MUTED, GRID = '#111b2a', '#edf3fb', '#a7b5c7', '#324153'
COLORS = {'private': '#5fd7d0', 'public': '#f4c777', 'never': '#bb9df6', 'prepare': '#7fb2f0', 'vote': '#8796aa',
          'single': '#5fd7d0'}
REGIME_LABEL = {'clean': 'Clean: everyone has current records',
                'informed_minority': 'Informed minority: 1 of 5 has the audits',
                'correctable_minority': 'Correctable minority: 4 of 5 have the audits'}
MODE_LABEL = {'live': 'five-agent teams', 'replay': 'one focal agent, four scripted peers',
              'qualification': 'single solver with every record'}


def font(size):
    for path in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def cells(episodes):
    """{(regime, arm): {'n': terminal assigned episodes, 'k': correct decisions}}"""
    out = {}
    for e in episodes:
        if not e.get('regime'):
            continue
        cell = out.setdefault((e['regime'], e['arm']), {'n': 0, 'k': 0})
        cell['n'] += 1
        cell['k'] += e['decision'] == 'correct'
    return out


def revisions(episodes):
    out = {}
    for e in episodes:
        for a in e.get('agents', []):
            row = out.setdefault(e['arm'], {'useful': 0, 'eligible_useful': 0, 'harmful': 0, 'eligible_harmful': 0})
            t = a['transition_public']
            for key in row:
                row[key] += t[key]
    return out


def frame(episodes, state):
    """state: stage, mode, backend, planned_episodes, blocks_done, blocks, elapsed, calls, cost_usd,
    input_tokens, output_tokens, failures, note (optional), series (optional label for S0)."""
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)

    def text(x, y, t, size=23, fill=INK):
        d.text((x, y), str(t), font=font(size), fill=fill)
    mode = state['mode']
    arms = ['single'] if mode == 'qualification' else [a for a in config.ARMS
                                                       if mode == 'live' or a in ('private', 'public', 'never', 'prepare')]
    terminal = [e for e in episodes if e.get('regime')]
    unfinished = sum(e['execution'] != 'completed' for e in episodes)
    text(60, 28, 'Keep the first judgment private, but allow revision', 42)
    who = 'SCRIPTED POLICY, NO MODEL' if state['backend'] == 'scripted' else 'HAIKU 4.5'
    text(60, 90, '%s | %s | %s | exploratory' % (config.STAGE_LABELS[state['stage']], MODE_LABEL[mode], who), 25, COLORS['private'])
    text(60, 132, 'Blocks %d/%d | episodes recorded %d/%d | not completed %d | failed calls %d | elapsed %.0fs' % (
        state['blocks_done'], state['blocks'], len(episodes), state['planned_episodes'], unfinished,
        state['failures'], state['elapsed']), 23)
    if state.get('series'):
        text(60, 168, state['series'], 21, MUTED)
    # legend
    x = 60
    for arm in arms:
        d.rectangle((x, 212, x + 26, 232), fill=COLORS[arm])
        label = 'full information' if arm == 'single' else arm.upper()
        text(x + 36, 208, label, 21, COLORS[arm])
        x += 60 + 14 * len(label) + 30
    measured = cells(terminal)
    title = {'live': 'Correct team decision (3 of 5 public final votes), share of assigned episodes',
             'replay': 'Focal agent\'s public final answer correct, share of assigned episodes',
             'qualification': 'Single solver correct, share of assigned worlds'}[mode]
    text(60, 262, title, 24)
    top, height, left, group = 330, 380, 110, 550
    for tick in (0, .25, .5, .75, 1):
        y = top + height * (1 - tick)
        d.line((left, y, left + 3 * group + 20, y), fill=GRID, width=1)
        text(left - 72, y - 12, '%d%%' % (tick * 100), 19, MUTED)
    for g, regime in enumerate(config.REGIMES):
        gx = left + g * group + 30
        text(gx, top + height + 52, REGIME_LABEL[regime], 20)
        bar = min(84, (group - 90) // len(arms))
        for i, arm in enumerate(arms):
            bx = gx + i * (bar + 10)
            cell = measured.get((regime, arm))
            if not cell:
                d.rectangle((bx, top + height - 3, bx + bar, top + height), fill=GRID)
                text(bx + 4, top + height + 8, 'pending', 15, MUTED)
                continue
            rate = cell['k'] / cell['n']
            d.rectangle((bx, top + height * (1 - rate), bx + bar, top + height), fill=COLORS[arm])
            d.rectangle((bx, top, bx + bar, top + height), outline=GRID, width=1)
            text(bx + 4, top + height + 8, '%d/%d' % (cell['k'], cell['n']), 18, INK)
    y = 820
    if mode != 'qualification':
        text(60, y, 'Revisions between the first answer and the public final answer (all agents, pooled)', 24)
        rev = revisions(terminal)
        text(60, y + 44, 'arm', 20, MUTED)
        text(260, y + 44, 'wrong -> correct (useful) / first answers wrong', 20, MUTED)
        text(930, y + 44, 'correct -> wrong (harmful) / first answers correct', 20, MUTED)
        for i, arm in enumerate(arms):
            row = rev.get(arm)
            yy = y + 80 + i * 34
            text(60, yy, arm.upper(), 21, COLORS[arm])
            if arm == 'prepare':
                text(260, yy, 'no first answer by design: revision undefined', 21, MUTED)
            elif row:
                text(260, yy, '%d / %d' % (row['useful'], row['eligible_useful']), 21)
                text(930, yy, '%d / %d' % (row['harmful'], row['eligible_harmful']), 21)
            else:
                text(260, yy, 'pending', 21, MUTED)
    else:
        valid = sum(bool(e.get('valid')) for e in terminal)
        correct = sum(e['decision'] == 'correct' for e in terminal)
        text(60, y, 'Qualification gate: at least 10 of 12 correct and at least 11 of 12 valid', 24)
        text(60, y + 50, 'So far: %d correct, %d valid, of %d recorded' % (correct, valid, len(terminal)), 24, COLORS['private'])
    if state['backend'] == 'scripted':
        text(60, 1082, 'Scripted calls %d | model calls 0 | cost $0' % state['calls'], 22, COLORS['private'])
    else:
        text(60, 1082, 'Model calls %d | input tokens %d | output tokens %d | stage cost $%.4f' % (
            state['calls'], state['input_tokens'], state['output_tokens'], state['cost_usd']), 22, COLORS['private'])
    text(60, 1122, state.get('note') or 'Counts are assigned episodes; an unfinished episode is a failed decision. '
         'Pending cells have no terminal episode yet.', 20, MUTED)
    text(60, 1156, 'Fictional supplier tasks with a known answer. One generator, one model. Development study, not a confirmation.'
         if state['backend'] != 'scripted' else 'Fictional supplier tasks with a known answer. Bars show a scripted policy, not a model.', 20, MUTED)
    return im


def replay(snapshots, out):
    """snapshots: list of (episodes_prefix, state) in completion order. Writes initial_frame.png,
    final_frame.png and replay.gif (at most 25 frames). Returns the frame count of the saved GIF
    (the encoder merges consecutive identical frames)."""
    if len(snapshots) > 25:
        last = len(snapshots) - 1
        keep = sorted({round(last * i / 24) for i in range(25)})
        snapshots = [snapshots[i] for i in keep]
    images = [frame(e, s) for e, s in snapshots]
    images[0].save(out / 'initial_frame.png')
    images[-1].save(out / 'final_frame.png')
    images[0].save(out / 'replay.gif', save_all=True, append_images=images[1:],
                   duration=[500] * (len(images) - 1) + [2500], loop=0)
    with Image.open(out / 'replay.gif') as saved:
        return getattr(saved, 'n_frames', 1)
