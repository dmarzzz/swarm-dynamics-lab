"""Render all saved H5 decisions; no requests, sampling or model access."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p = argparse.ArgumentParser()
p.add_argument('results', type=Path)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
packet = json.loads((a.results/'packet.json').read_text())
summary = json.loads((a.results/'summary.json').read_text())
rows = json.loads((a.results/'records.json').read_text())
assert packet['stage'] == 'H5' and summary['origin'] == 'native-jev'
indexed = {(r['root'], r['arm'], r['tick']): r for r in rows}
assert len(indexed) == len(rows)
im = Image.new('RGB', (1500, 1320), '#101720')
draw = ImageDraw.Draw(im)
font_path = next((str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()), None)
font = lambda n: ImageFont.truetype(font_path, n) if font_path else ImageFont.load_default()
white, muted = '#e9eff6', '#b3c0ce'
draw.text((50, 32), 'When does saving a later check help?', font=font(40), fill=white)
draw.text((50, 91), 'RD5 H5 | Native Jev interpretations within three scripted allocation policies', font=font(23), fill=muted)
arms = summary['by_arm']
for i, arm in enumerate(('B0', 'B1', 'B2')):
    item = arms[arm]
    name = {'B0': 'Always check', 'B1': 'Remember attempts', 'B2': 'Memory + reserve'}[arm]
    x = 50 + i*480
    draw.rounded_rectangle((x, 141, x+450, 225), radius=10, fill='#1c2c3c')
    draw.text((x+18, 151), f"{arm} {name}: {item['correct']}/24 correct", font=font(23), fill=white)
    draw.text((x+18, 187), f"{item['physical_checks']} checks | {item['inference_attempts']} model calls", font=font(19), fill=muted)
draw.text((50, 256), 'SCENARIO / POLICY', font=font(18), fill=muted)
for i, tick in enumerate((0, 2, 4, 6)):
    draw.text((530+i*205, 256), f'TICK {tick}', font=font(18), fill=muted)
for group, root in enumerate(packet['definition']['roots']):
    y = 300+group*139
    label = root['mechanism'].replace('_', ' ') + ' / ' + root['direction']
    draw.text((50, y), label, font=font(21), fill=white)
    draw.text((50, y+30), f"Useful inspection at tick {root['critical_tick']}", font=font(17), fill=muted)
    for j, arm in enumerate(('B0', 'B1', 'B2')):
        row_y = y+j*39
        draw.text((445, row_y+7), arm, font=font(19), fill=muted)
        for i, tick in enumerate((0, 2, 4, 6)):
            r = indexed.get((root['id'], arm, tick))
            complete = r is not None and r['status'] == 'completed'
            action = r['action'] if complete else ('FAILED' if r else 'UNSTARTED')
            color = '#173e39' if complete and r['correct'] else '#522d34' if complete and action != 'DEFER' else '#27323f'
            x = 515+i*205
            draw.rounded_rectangle((x, row_y, x+185, row_y+33), radius=5, fill=color)
            draw.text((x+12, row_y+6), action, font=font(18), fill=white)
    draw.line((50, y+125, 1430, y+125), fill='#27323f', width=1)
delta = arms['B2']['correct']-arms['B1']['correct']
secondary = arms['B1']['correct']-arms['B0']['correct']
draw.text((50, 1158), f"Paired total: B2 minus B1 = {delta:+d} correct decisions; B1 minus B0 = {secondary:+d}.", font=font(25), fill=white)
draw.text((50, 1201), f"All assigned: {summary['terminal']}/{summary['assigned']} terminal. Green = correct; red = wrong commitment; gray = DEFER/missing.", font=font(19), fill=muted)
draw.text((50, 1236), 'DEFER counts as noncompletion. Inspect the urgent-early rows even when the aggregate reserve contrast improves.', font=font(19), fill=muted)
draw.text((50, 1271), 'Six fixed authored roots; dependent decisions, known timing, one domain and scripted ballots. No population inference.', font=font(19), fill=muted)
a.output.parent.mkdir(parents=True, exist_ok=True)
im.save(a.output)
print(json.dumps({'rendered': str(a.output), 'native_rows': len(rows), 'assigned': summary['assigned']}))
