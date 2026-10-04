#!/usr/bin/env python3
"""Render predeclared daily aggregates from frozen A1 summary; no new analysis."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
summary=json.loads((ROOT/'results/A1/summary.json').read_text())
days=summary['window_results']['1800']['daily']
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1150" viewBox="0 0 1600 1150">',
 '<rect width="1600" height="1150" fill="#10161e"/><g font-family="monospace" fill="#edf3f7">',
 '<text x="60" y="70" font-size="30">The aggregate null combines different deletion-day contrasts</text>',
 '<text x="60" y="120" font-size="20">30-minute horizon, 60-second guard; observed saves, not estimated treatment effects</text>',
 '<text xml:space="preserve" x="60" y="170" font-size="20">UTC day        pages    before   after   difference</text>']
for i,(day,d) in enumerate(days.items()):
    y=225+i*53
    delta=d['after']-d['before']
    parts.append(f'<text xml:space="preserve" x="60" y="{y}" font-size="21">{day}   {d["pages"]:5d}      {d["before"]:3d}     {d["after"]:3d}       {delta:+3d}</text>')
    x=1160+min(delta,0)*12
    parts.append(f'<rect x="{x}" y="{y-20}" width="{max(abs(delta)*12,2)}" height="27" fill="{("#77d9b5" if delta>0 else "#f0bf70" if delta<0 else "#8999aa")}"/>')
parts+=['<line x1="1160" x2="1160" y1="195" y2="950" stroke="#526171"/>',
 '<text x="60" y="1040" font-size="22">Only June 18–20 contribute any saves inside these windows.</text>',
 '<text x="60" y="1085" font-size="20">Moderation targeting, quiet pages and collection gaps prevent a causal containment claim.</text></g></svg>']
(ROOT/'results/A1/daily-contrast.svg').write_text('\n'.join(parts))
print('Rendered frozen per-day counts; no new sample or outcome collected.')
