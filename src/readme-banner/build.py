#!/usr/bin/env python3
"""Build assets/banner.svg, the README banner, from the repo's own records.

Run from anywhere:  python3 src/readme-banner/build.py

What each mark encodes
- Outer swarm: one dot per library entry (1-library/<type>/<id>.md).
  angle     = the entry's topics (each topic in 1-library/topics.yaml owns a direction, in file order;
              an entry with several topics sits at their circular mean)
  distance  = `relevance` 1 to 5 (5 is nearest the core)
  brightness and size = `read_depth` (abstract, skim, full, ran)
- Core: one dot per cohort in 5-experiments/evidence-metadata.json, highest evidence score at the centre.
  hollow ring = 0/4 or unassessed, filled violet = 1/4, filled white = 2/4. No cohort scores higher.
- Amber path: the order the lab enforces, five nodes from the edge to the core:
  scan, survey, synthesis, hypothesis, experiment. It is the one mark that is not a record.

The scatter inside each band is a hash of the entry id, so the output is deterministic.
Stdlib only. No text, fonts, scripts or external references in the SVG (GitHub serves it through <img>).
"""
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "banner.svg"
LIBRARY = ROOT / "1-library"
TOPICS = LIBRARY / "topics.yaml"
REGISTRY = ROOT / "5-experiments" / "evidence-metadata.json"
TYPES = ["papers", "blogs", "threads", "code", "datasets", "talks"]

W, H = 1600, 520
CX, CY = 800.0, 260.0
RX, RY = 742.0, 232.0            # the swarm's extent; an ellipse because the banner is wide
HUE = 274                        # project hue, as on the lab's run site

VOID = "#040306"
INK = "#e9e7e1"
AMBER = "#fbc35a"                # hsl(40 95% 66%)
VIOLET = "#b76bf9"               # hsl(274 92% 70%)

# normalised distance from the centre for relevance 5..1, and the scatter around it
BAND = {5: 0.30, 4: 0.46, 3: 0.62, 2: 0.78, 1: 0.92}
BAND_SIGMA = 0.062
ANGLE_SIGMA = 0.20               # radians
# read depth -> (dot diameter px, opacity, colour)
DEPTH = {
    "abstract": (2.7, 0.42, VIOLET),
    "skim": (3.1, 0.66, VIOLET),
    "full": (3.6, 1.0, VIOLET),
    "ran": (5.2, 1.0, INK),
}
CORE_STEP = 5.3                  # spacing of the cohort dots
CORE_DOT = 2.5


def unit(key, salt):
    """Deterministic float in (0, 1) from a string."""
    h = hashlib.sha256(f"{salt}:{key}".encode()).digest()
    return (int.from_bytes(h[:8], "big") + 1) / (2**64 + 2)


def gauss(key, salt):
    return math.sqrt(-2 * math.log(unit(key, salt + "a"))) * math.cos(2 * math.pi * unit(key, salt + "b"))


def frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    block = text.split("\n---", 1)[0]
    out, key = {}, None
    for line in block.splitlines()[1:]:
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).split(" #")[0].strip()
            out[key] = val
        elif key and re.match(r"^\s+-\s+", line):
            out[key] = (out[key] + "," + line.split("-", 1)[1].strip()).lstrip(",")
    return out


def read_library():
    slugs = re.findall(r"^- slug:\s*([a-z0-9-]+)", TOPICS.read_text(encoding="utf-8"), flags=re.M)
    angle_of = {s: 2 * math.pi * i / len(slugs) - math.pi / 2 for i, s in enumerate(slugs)}
    entries = []
    for t in TYPES:
        for p in sorted((LIBRARY / t).glob("*.md")):
            fm = frontmatter(p)
            if not fm:
                continue
            topics = [s for s in re.findall(r"[a-z0-9-]+", fm.get("topics", "")) if s in angle_of]
            depth = fm.get("read_depth", "").strip("\"'")
            try:
                rel = int(fm.get("relevance", "").strip("\"'"))
            except ValueError:
                rel = 1
            entries.append({
                "id": p.stem,
                "angles": [angle_of[s] for s in topics],
                "depth": depth if depth in DEPTH else "abstract",
                "rel": min(5, max(1, rel)),
            })
    return entries, len(slugs)


def place(e):
    sx = sum(math.cos(a) for a in e["angles"])
    sy = sum(math.sin(a) for a in e["angles"])
    if math.hypot(sx, sy) < 1e-6:                      # no topic, or topics that cancel: hash the direction
        theta = 2 * math.pi * unit(e["id"], "theta")
    else:
        theta = math.atan2(sy, sx)
    theta += ANGLE_SIGMA * gauss(e["id"], "ang")
    r = BAND[e["rel"]] + BAND_SIGMA * gauss(e["id"], "rad")
    r = min(1.02, max(0.20, r))
    return CX + RX * r * math.cos(theta), CY + RY * r * math.sin(theta)


def read_cohorts():
    studies = json.loads(REGISTRY.read_text(encoding="utf-8"))["studies"]
    scores = []
    for s in studies:
        ec = s.get("evidence_confidence")
        score = ec.get("score") if isinstance(ec, dict) else ec
        scores.append(score if isinstance(score, int) else -1)
    return sorted(scores, reverse=True)


def spiral(n_points=160):
    """The amber path: from the edge of the swarm to the edge of the core, a little under one turn."""
    pts = []
    core_r = CORE_STEP * math.sqrt(150) + 16
    for i in range(n_points + 1):
        u = i / n_points
        theta = math.radians(292) + u * math.radians(282)
        ex, ey = RX * 0.93, RY * 0.93
        k = (1 - u) ** 1.25
        rx = core_r + (ex - core_r) * k
        ry = core_r + (ey - core_r) * k
        pts.append((CX + rx * math.cos(theta), CY + ry * math.sin(theta)))
    return pts


def main():
    entries, n_topics = read_library()
    cohorts = read_cohorts()

    by_depth = {d: [] for d in DEPTH}
    for e in entries:
        x, y = place(e)
        by_depth[e["depth"]].append(f"M{x:.1f} {y:.1f}h0")

    s = []
    s.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="A swarm of {len(entries)} dots, one per library source, around a core of {len(cohorts)} '
        f'experiment cohorts, with an amber path running from the edge to the core through five nodes">'
    )
    s.append(
        "<defs>"
        f'<radialGradient id="a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="hsl({HUE},85%,42%)" stop-opacity=".34"/>'
        f'<stop offset=".5" stop-color="hsl({HUE},80%,30%)" stop-opacity=".12"/><stop offset="1" stop-color="hsl({HUE},80%,30%)" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="b" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="hsl({HUE},90%,72%)" stop-opacity=".42"/>'
        f'<stop offset="1" stop-color="hsl({HUE},90%,60%)" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        "</defs>"
    )
    s.append(f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{VOID}"/>')
    s.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{RX * 1.02:.0f}" ry="{RY * 1.2:.0f}" fill="url(#a)"/>')

    # outer swarm, one path per read depth; a zero-length segment with a round cap is a dot
    for d, (size, op, col) in DEPTH.items():
        if by_depth[d]:
            s.append(
                f'<path d="{"".join(by_depth[d])}" fill="none" stroke="{col}" stroke-opacity="{op}" '
                f'stroke-width="{size}" stroke-linecap="round"/>'
            )

    # amber path and its five nodes
    pts = spiral()
    core_r = CORE_STEP * math.sqrt(len(cohorts)) + 16
    s.append(
        '<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f'" fill="none" stroke="{AMBER}" '
        'stroke-width="2.2" stroke-opacity=".9" stroke-linecap="butt" stroke-dasharray="7 7"/>'
    )
    for k, i in enumerate([0, 40, 80, 120, 160]):
        x, y = pts[i]
        if k < 4:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{VOID}" stroke="{AMBER}" stroke-width="2.2"/>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{AMBER}"/>')

    # core: experiment cohorts, phyllotaxis, highest score at the centre
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{core_r + 46:.0f}" fill="url(#b)"/>')
    golden = math.pi * (3 - math.sqrt(5))
    rings, ones, twos = [], [], []
    for i, score in enumerate(cohorts):
        r = CORE_STEP * math.sqrt(i + 0.5)
        x, y = CX + r * math.cos(i * golden), CY + r * math.sin(i * golden)
        if score >= 2:
            twos.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{CORE_DOT}"/>')
        elif score == 1:
            ones.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{CORE_DOT}"/>')
        else:
            rings.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{CORE_DOT - 0.5}"/>')
    s.append(f'<g fill="#ffffff">{"".join(twos)}</g>')
    s.append(f'<g fill="hsl({HUE},95%,74%)">{"".join(ones)}</g>')
    s.append(f'<g fill="none" stroke="hsl({HUE},60%,74%)" stroke-opacity=".7" stroke-width="1">{"".join(rings)}</g>')

    s.append("</g>")
    s.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#ffffff" stroke-opacity=".12"/>')
    s.append("</svg>\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(s), encoding="utf-8")
    depth_n = {d: len(v) for d, v in by_depth.items()}
    score_n = {k: cohorts.count(k) for k in sorted(set(cohorts), reverse=True)}
    print(f"{OUT.relative_to(ROOT)}: {W}x{H}, {OUT.stat().st_size} bytes")
    print(f"library entries {len(entries)} over {n_topics} topics, by read depth {depth_n}")
    print(f"cohorts {len(cohorts)}, by evidence score (-1 = unassessed) {score_n}")


if __name__ == "__main__":
    main()
