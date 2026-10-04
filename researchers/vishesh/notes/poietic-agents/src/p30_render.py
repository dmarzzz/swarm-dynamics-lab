"""Dependency-free SVG progress and HTML event replay from recorded values only."""
import html
import json
from pathlib import Path


def diagnostic_png(summary, path, scripted=False):
    from PIL import Image, ImageDraw, ImageFont
    canvas=Image.new('RGB',(1600,720),'#101923');draw=ImageDraw.Draw(canvas)
    title=ImageFont.load_default(size=40);body=ImageFont.load_default(size=24)
    draw.text((55,42),'Poietic Agents | contract qualification',fill='#eff4f7',font=title)
    label='SCRIPTED - NOT MODEL EVIDENCE' if scripted else 'Q30 qualification - not a swarm efficacy result'
    draw.text((55,105),label,fill='#b5c8d8',font=body)
    for i,(role,g) in enumerate(summary['contracts'].items()):
        y=190+i*140
        draw.text((55,y),role,fill='#eff4f7',font=body)
        draw.rectangle((395,y,1450,y+40),fill='#374453')
        if g['correct']:draw.rectangle((395,y,395+1055*g['correct']/48,y+40),fill='#54b5a7')
        draw.text((395,y+52),f"Correct {g['correct']}/48 | valid {g['schema_valid']}/48 | started {g['started']}/48 | unstarted {48-g['started']}",fill='#eff4f7',font=body)
    draw.text((55,650),'Per contract: At least 44 correct, 48 valid, zero protected-access violations. All assignments retained.',fill='#b5c8d8',font=ImageFont.load_default(size=22))
    canvas.save(path)


def diagnostic_frame(summary, path, scripted=False):
    label='SCRIPTED — NOT MODEL EVIDENCE' if scripted else 'Q30 qualification — not a swarm efficacy result'
    chunks=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="720" viewBox="0 0 1600 720">',
            '<rect width="1600" height="720" fill="#101923"/>',
            '<g fill="#eff4f7" font-family="sans-serif">',
            '<text x="60" y="75" font-size="40">Poietic Agents · contract qualification</text>',
            f'<text x="60" y="120" font-size="23">{html.escape(label)}</text>']
    for i,(role,group) in enumerate(summary['contracts'].items()):
        y=205+i*145; correct=group['correct']; valid=group['schema_valid']
        chunks.extend([f'<text x="60" y="{y}" font-size="26">{html.escape(role)}</text>',
                       f'<rect x="400" y="{y-30}" width="1000" height="44" fill="#374453"/>',
                       f'<rect x="400" y="{y-30}" width="{1000*correct/48}" height="44" fill="#54b5a7"/>',
                       f'<text x="400" y="{y+50}" font-size="23">Correct {correct}/48 · valid {valid}/48 · started {group["started"]}/48 · unstarted {48-group["started"]}</text>'])
    chunks+=['<text x="60" y="680" font-size="21">Threshold per contract: At least 44 correct, 48 valid, zero protected-access violations. All assignments retained.</text>','</g></svg>']
    Path(path).write_text(''.join(chunks))
