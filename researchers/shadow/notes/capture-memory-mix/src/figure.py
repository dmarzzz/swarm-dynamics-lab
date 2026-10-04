#!/usr/bin/env python3
"""Figure: post-purge return vs short-memory fraction f, scripted (M1) vs real models (MP, MP2). SVG, stdlib only.

    python3 src/figure.py   -> results/rescue-vs-f.svg
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def series_from_cells(csv_path: Path, arm: str, metric: str, dose: float, fam: str):
    out = {}
    for r in csv.DictReader(csv_path.open()):
        if r["arm"] != arm or float(r["dose"]) != dose or r["world"] != "W1_INSIDE":
            continue
        m = r["memory"]
        if m.startswith(f"mix:{fam}@"):
            f = float(m.split("@")[1])
        elif m == fam.split("/")[1]:
            f = 0.0
        elif m == fam.split("/")[0]:
            f = 1.0
        else:
            continue
        v = r[metric]
        if v and v != "nan":
            out[f] = float(v)
    return dict(sorted(out.items()))


def svg(curves, title, path):
    W, H, L, B = 640, 400, 70, 50
    def X(f): return L + f * (W - L - 30)
    def Y(v): return H - B - v * (H - B - 40)
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b"]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="20" text-anchor="middle" font-size="14">{title}</text>']
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        s.append(f'<line x1="{L}" y1="{Y(v)}" x2="{W-30}" y2="{Y(v)}" stroke="#ddd"/>')
        s.append(f'<text x="{L-8}" y="{Y(v)+4}" text-anchor="end">{v:.2f}</text>')
    for f in (0, 0.25, 0.5, 0.75, 1.0):
        s.append(f'<text x="{X(f)}" y="{H-B+18}" text-anchor="middle">{f:g}</text>')
    s.append(f'<text x="{(L+W-30)/2}" y="{H-12}" text-anchor="middle">fraction f of honest agents with a 1-slot memory (rest: full running mean)</text>')
    s.append(f'<text transform="translate(16,{(H-B+40)/2}) rotate(-90)" text-anchor="middle">honest fraction on the original, 30 to 50 rounds after the purge</text>')
    for i, (name, pts, style) in enumerate(curves):
        c = colors[i % len(colors)]
        if not pts:
            continue
        d = " ".join(f"{'M' if j == 0 else 'L'}{X(f):.1f},{Y(v):.1f}" for j, (f, v) in enumerate(pts.items()))
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" {style}/>')
        for f, v in pts.items():
            s.append(f'<circle cx="{X(f):.1f}" cy="{Y(v):.1f}" r="4" fill="{c}"/>')
        s.append(f'<rect x="{L+10}" y="{32+i*16}" width="12" height="3" fill="{c}"/><text x="{L+28}" y="{38+i*16}">{name}</text>')
    s.append("</svg>")
    path.write_text("\n".join(s))


def main():
    R = ROOT / "results"
    curves = []
    if (R / "M1_cells.csv").exists():
        curves.append(("scripted tanh rule (beta 2.5, h 0.1), N=24, dose 0.54, round 50, A1 purge", series_from_cells(R / "M1_cells.csv", "A1_purge", "frac_T_c", 0.54, "1/full"), 'stroke-dasharray="6,4"'))
        curves.append(("scripted, A2 purge + wipe", series_from_cells(R / "M1_cells.csv", "A2_purge_wipe", "frac_T_c", 0.54, "1/full"), 'stroke-dasharray="2,3"'))
    if (R / "MP_cells.csv").exists():
        curves.append(("gpt-4o-mini, N=16, dose 0.5, round 30, A1 purge", series_from_cells(R / "MP_cells.csv", "A1_purge", "frac_T_c", 0.5, "1/full"), ""))
        curves.append(("gpt-4o-mini, A2 purge + wipe", series_from_cells(R / "MP_cells.csv", "A2_purge_wipe", "frac_T_c", 0.5, "1/full"), ""))
    if (R / "MP2_cells.csv").exists():
        curves.append(("gemma-3-27b-it (sample mode), A1 purge", series_from_cells(R / "MP2_cells.csv", "A1_purge", "frac_T_c", 0.5, "1/full"), ""))
    if (R / "MP3_cells.csv").exists():
        curves.append(("qwen3-235b-a22b, A1 purge", series_from_cells(R / "MP3_cells.csv", "A1_purge", "frac_T_c", 0.5, "1/full"), ""))
    svg(curves, "Return after a perfect purge vs short-memory fraction (captured episodes)", R / "rescue-vs-f.svg")
    print("wrote", R / "rescue-vs-f.svg", [(n, len(p)) for n, p, _ in curves])


if __name__ == "__main__":
    main()
