#!/usr/bin/env python3
"""Build assets/architecture.svg, the README system architecture figure, from the repo's own records.

Run from anywhere:  python3 src/readme-architecture/build.py

What the figure shows
- Top left: the three researchers (principals) and their agents with the session loop.
- Centre: the one git repository as the only shared state between agents: the coordination files under
  lab/, and the research record in the numbered folders with the gates drawn on the path between them.
- Top right: the CI verifier (.github/workflows/lab.yml).
- Bottom: the experiment plane (agentops/): admission, server claim, workers, run hub, model APIs, live site.

Encoding (also drawn as a legend inside the figure)
- amber  = a gate or verifier, and nothing else
- violet = agents and control flow (who starts or hands work to whom)
- ink    = data flow and structure
- box styles: human (pill), agent (violet), state in git (plain), gate/verifier (amber), compute (left bar),
  external service (dashed)

Counts and thresholds are read from the repo (see read_counts); the script prints what it used.
The layout is declarative: NODES places boxes on a small grid, EDGES connects them by side.
Stdlib only, deterministic. The SVG uses real <text> in a system monospace stack and has no scripts,
web fonts, foreignObject or external references (GitHub serves it through <img>).
Text is drawn at twice the README size: 22 px is the smallest label (11 px on the page).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "architecture.svg"

W = 1760
VOID = "#040306"
INK = "#e9e7e1"
AMBER = "#fbc35a"                # gates and verifiers only
VIOLET = "#b76bf9"               # project hue 274: agents and control flow
FONT = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
EM = 0.62                        # assumed advance per character, in em; boxes are sized with this much slack
S_MIN, S_NAME, S_BIG = 22, 24, 28

WARNINGS = []


# ---------------------------------------------------------------------------------------------- repo facts
def _const(text, name, cast=float):
    m = re.search(rf'^\s*"?{name}"?\s*[:=]\s*(?:int\(os\.environ\.get\("[A-Z_]+",\s*)?([0-9.]+)', text, flags=re.M)
    if not m:
        raise SystemExit(f"could not read {name}")
    return cast(m.group(1))


def _front(path, key):
    m = re.search(rf"^{key}:\s*([A-Za-z-]+)", path.read_text(encoding="utf-8", errors="replace"), flags=re.M)
    return m.group(1) if m else ""


def read_counts():
    lab_py = (ROOT / "scripts/lab.py").read_text(encoding="utf-8")
    hub_py = (ROOT / "agentops/hub/hub.py").read_text(encoding="utf-8")
    researchers = sorted(p.name for p in (ROOT / "lab/researchers").iterdir() if p.is_dir())
    surveys = [p for p in sorted((ROOT / "2-surveys").glob("*.md")) if p.name != "README.md"]
    reviews = [p for p in sorted((ROOT / "2-surveys/reviews").glob("*.md")) if p.name != "README.md"]
    hyps = [p for p in sorted((ROOT / "4-hypotheses").glob("*.md")) if p.name != "README.md"]
    atlas = (ROOT / "3-synthesis/research-question-atlas.md").read_text(encoding="utf-8")
    m = re.search(r"([0-9,]+) candidates supported", atlas)
    c = {
        "researchers": len(researchers),
        "agents": sum(len(list((ROOT / "lab/researchers" / r / "agents").glob("*.md"))) for r in researchers),
        "tasks": len(list((ROOT / "lab/tasks").glob("*.md"))),
        "library": sum(len(list((ROOT / "1-library" / t).glob("*.md")))
                       for t in ("papers", "blogs", "threads", "code", "datasets", "talks")),
        "surveys": len(surveys),
        "surveys_complete": sum(_front(p, "status") == "complete" for p in surveys),
        "reviews": len(reviews),
        "reviews_pass": sum(_front(p, "verdict") == "pass" for p in reviews),
        "reviews_revise": sum(_front(p, "verdict") == "revise" for p in reviews),
        "hyp_proposed": sum(_front(p, "status") == "proposed" for p in hyps),
        "hyp_accepted": sum(_front(p, "status") in {"accepted", "testing", "supported", "refuted"} for p in hyps),
        "questions": int(m.group(1).replace(",", "")) if m else 0,
        "studies": sum(1 for r in researchers for p in (ROOT / "5-experiments/studies" / r).iterdir() if p.is_dir()),
        "cohorts": len(json.loads((ROOT / "5-experiments/evidence-metadata.json").read_text(encoding="utf-8"))["studies"]),
        # this figure is itself filed as an artifact; count it before it is filed so a rebuild does not change it
        "artifacts": len(re.findall(r"^  - id:", (ROOT / "artifacts.yaml").read_text(encoding="utf-8"), flags=re.M))
        + (0 if re.search(r"^  - id: readme-architecture$", (ROOT / "artifacts.yaml").read_text(encoding="utf-8"), flags=re.M) else 1),
        # thresholds, from the code that enforces them
        "claim_ttl_h": _const(lab_py, "CLAIM_TTL_HOURS", int),
        "min_cited": _const(lab_py, "min_cited", int),
        "min_papers": _const(lab_py, "min_papers", int),
        "min_code": _const(lab_py, "min_code", int),
        "min_informal": _const(lab_py, "min_informal", int),
        "min_full_reads": _const(lab_py, "min_full_reads", int),
        "min_seminal": _const(lab_py, "min_seminal", int),
        "min_search_rounds": _const(lab_py, "min_search_rounds", int),
        "saturation_rounds": _const(lab_py, "saturation_rounds", int),
        "saturation_pct": round(_const(lab_py, "saturation_max_new") * 100),
        "hub_lease_min": _const(hub_py, "LEASE", int) // 60,
        "hub_max_attempts": _const(hub_py, "MAX_ATTEMPTS", int),
    }
    c["sync_min"] = 10               # AGENTS.md: `lab.py sync --every 600`
    return c


# ---------------------------------------------------------------------------------------------- svg helpers
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def width_of(s, size, track=0.0):
    return len(s) * size * (EM + track)


def text(x, y, s, size=S_MIN, fill=INK, op=1.0, weight=400, anchor="start", track=0.0, fit=None):
    """One line of text. `fit` is the widest it may be; a line estimated wider is reported."""
    if size < S_MIN:
        WARNINGS.append(f"text below {S_MIN}px: {s!r}")
    if fit is not None and width_of(s, size, track) > fit + 0.5:
        WARNINGS.append(f"too wide by {width_of(s, size, track) - fit:.0f}px (fit {fit:.0f}): {s!r}")
    a = [f'x="{f(x)}"', f'y="{f(y)}"', f'font-size="{size}"', f'fill="{fill}"']
    if op < 1:
        a.append(f'fill-opacity="{op}"')
    if weight != 400:
        a.append(f'font-weight="{weight}"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if track:
        a.append(f'letter-spacing="{f(size * track)}"')
    return f"<text {' '.join(a)}>{esc(s)}</text>"


# one style per kind of thing
KIND = {
    "human":     dict(stroke=INK, sw=1.6, so=0.95, fill=INK, fo=0.03, rx=26),
    "agent":     dict(stroke=VIOLET, sw=1.6, so=1.0, fill=VIOLET, fo=0.08, rx=10),
    "state":     dict(stroke=INK, sw=1.2, so=0.55, fill=INK, fo=0.045, rx=3),
    "verifier":  dict(stroke=AMBER, sw=1.6, so=1.0, fill=AMBER, fo=0.06, rx=3),
    "compute":   dict(stroke=INK, sw=1.2, so=0.55, fill=INK, fo=0.045, rx=3, bar=True),
    "external":  dict(stroke=INK, sw=1.4, so=0.7, fill=INK, fo=0.0, rx=18, dash="7 6"),
    "container": dict(stroke=INK, sw=1.0, so=0.30, fill=INK, fo=0.018, rx=10),
}


def rect(kind, x, y, w, h):
    k = KIND[kind]
    a = (f'x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{min(k["rx"], h / 2):g}" fill="{k["fill"]}" '
         f'fill-opacity="{k["fo"]}" stroke="{k["stroke"]}" stroke-opacity="{k["so"]}" stroke-width="{k["sw"]}"')
    if k.get("dash"):
        a += f' stroke-dasharray="{k["dash"]}"'
    out = [f"<rect {a}/>"]
    if k.get("bar"):
        out.append(f'<rect x="{f(x)}" y="{f(y)}" width="5" height="{f(h)}" fill="{INK}" fill-opacity="0.8"/>')
    return "".join(out)


EDGE = {
    "control": dict(stroke=VIOLET, sw=2.2, op=1.0),
    "data":    dict(stroke=INK, sw=1.6, op=0.85),
    "ungated": dict(stroke=INK, sw=1.6, op=0.85, dash="7 6"),
}


def arrow(points, kind="data", head=True):
    """Orthogonal polyline through `points` with a small filled head at the last point."""
    k = EDGE[kind]
    (x1, y1), (x2, y2) = points[-2], points[-1]
    L = 11.0
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5 or 1.0
    ux, uy = dx / n, dy / n
    pts = list(points)
    out = []
    if head:
        bx, by = x2 - ux * L, y2 - uy * L
        pts[-1] = (x2 - ux * (L - 1), y2 - uy * (L - 1))
        out.append(f'<polygon points="{f(x2)},{f(y2)} {f(bx - uy * 5.5)},{f(by + ux * 5.5)} {f(bx + uy * 5.5)},{f(by - ux * 5.5)}" '
                   f'fill="{k["stroke"]}" fill-opacity="{k["op"]}"/>')
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
    a = f'd="{d}" fill="none" stroke="{k["stroke"]}" stroke-opacity="{k["op"]}" stroke-width="{k["sw"]}" stroke-linejoin="round"'
    if k.get("dash"):
        a += f' stroke-dasharray="{k["dash"]}"'
    return f"<path {a}/>" + "".join(out)


def diamond(x, y, r=10):
    return (f'<polygon points="{f(x)},{f(y - r)} {f(x + r)},{f(y)} {f(x)},{f(y + r)} {f(x - r)},{f(y)}" '
            f'fill="{VOID}" stroke="{AMBER}" stroke-width="2"/>'
            f'<polygon points="{f(x)},{f(y - r + 5)} {f(x + r - 5)},{f(y)} {f(x)},{f(y + r - 5)} {f(x - r + 5)},{f(y)}" fill="{AMBER}"/>')


def callout(n, x, y):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="17" fill="{VOID}" stroke="{INK}" stroke-width="1.6"/>'
            + text(x, y + 7.5, str(n), size=S_MIN, weight=700, anchor="middle"))


def person(x, y):
    return (f'<circle cx="{f(x)}" cy="{f(y - 9)}" r="6.5" fill="none" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{f(x - 11)},{f(y + 12)} a11,12 0 0 1 22,0" fill="none" stroke="{INK}" stroke-width="1.6"/>')


# ---------------------------------------------------------------------------------------------- layout grid
PAD = 12                                   # text inset inside a box
LX, LW = 40, 380                           # left column: principals and agents
RX, RR = 500, 1720                         # right region: verifier, repository
TOP_Y, TOP_H = 40, 140                     # top row
REPO_Y = 236                               # repository container
COORD_Y, COORD_H = 292, 120                # coordination files
RULE_Y = 448
PIPE_Y = 540                               # first phase row
ROW_H = 66
GAP_PLAIN, GAP_GATES, GAP_GATE = 30, 104, 46
SUB_X, SUB_W = 524, 215                    # side column inside the repository (3-synthesis)
MAIN_X, MAIN_R = 774, 1696                 # phase rows
SPINE_X = 846                              # the path the phases are read along
DESC_X = 1000
Y_LIB = PIPE_Y
Y_SUR = Y_LIB + ROW_H + GAP_PLAIN
Y_HYP = Y_SUR + ROW_H + GAP_GATES
Y_EXP = Y_HYP + ROW_H + GAP_GATE
REPO_B = Y_EXP + ROW_H + 24
BAND_Y = REPO_B + 38                       # experiment plane
BAND_R1, BAND_R1H = BAND_Y + 54, 130
BAND_R2, BAND_R2H = BAND_Y + 54 + 130 + 30, 66
BAND_B = BAND_R2 + BAND_R2H + 20
LEGEND_Y = BAND_B + 42
H = LEGEND_Y + 30


def nodes(c):
    """Every box: id -> (kind, x, y, w, h, title, [lines]). Titles are component names, lines are facts."""
    all_revise = c["reviews"] and c["reviews_revise"] == c["reviews"]
    review_line = (f'{c["reviews"]} reviews, all returned revise' if all_revise
                   else f'{c["reviews"]} reviews, {c["reviews_pass"]} pass')
    return {
        "humans":   ("human", LX, TOP_Y, LW, TOP_H, f'{c["researchers"]} researchers',
                     ["write directives,", "authorize budget, scope"]),
        "agents":   ("agent", LX, REPO_Y, LW, REPO_B - REPO_Y, f'{c["agents"]} agents',
                     ["id: researcher/agent", "harnesses: claude code,", "codex and others"]),
        "ci":       ("verifier", 620, TOP_Y, RR - 620, TOP_H, "", []),
        "repo":     ("container", RX, REPO_Y, RR - RX, REPO_B - REPO_Y, "", []),
        "directives": ("state", 524, COORD_Y, 240, COORD_H, "directives",
                       ["human to agents", "override board"]),
        "board":    ("state", 784, COORD_Y, 352, COORD_H, f'task board · {c["tasks"]}',
                     ["only broadcast channel", f'claim = lease, {c["claim_ttl_h"]} h ttl']),
        "inbox":    ("state", 1156, COORD_Y, 270, COORD_H, "inbox.md, for:",
                     ["directed messages", "cross-researcher"]),
        "status":   ("state", 1446, COORD_Y, 250, COORD_H, "agent status",
                     [f'{c["agents"]} registered', "the heartbeat"]),
        "library":  ("state", MAIN_X, Y_LIB, MAIN_R - MAIN_X, ROW_H, "1-library",
                     [f'{c["library"]:,} sources · one file each, stated read depth',
                      "deterministic ids: duplicates collide at push"]),
        "surveys":  ("state", MAIN_X, Y_SUR, MAIN_R - MAIN_X, ROW_H, "2-surveys",
                     [f'{c["surveys"]} surveys · {c["surveys_complete"]} pass the gate, '
                      f'{c["surveys"] - c["surveys_complete"]} in progress', review_line]),
        "synthesis": ("state", SUB_X, Y_SUR, SUB_W, ROW_H, "3-synthesis", [f'{c["questions"]} questions']),
        "hypotheses": ("state", MAIN_X, Y_HYP, MAIN_R - MAIN_X, ROW_H, "4-hypotheses",
                       [f'{c["hyp_proposed"]} proposed · {c["hyp_accepted"]} accepted',
                        "each cites a complete survey + 3 closest priors"]),
        "experiments": ("state", MAIN_X, Y_EXP, 1350 - MAIN_X, ROW_H, "5-experiments",
                        [f'{c["studies"]} study folders', f'{c["cohorts"]} cohorts, scored 0-4']),
        "artifacts": ("state", 1410, Y_EXP, MAIN_R - 1410, ROW_H, f'artifacts/ · {c["artifacts"]}',
                      ["with provenance"]),
        "band":     ("container", LX, BAND_Y, RR - LX, BAND_B - BAND_Y, "", []),
        "admission": ("verifier", 64, BAND_R1, 360, BAND_R1H, "pre-run admission",
                      ["plan + pre-registration", "committed before run 1", "pre-run assessment"]),
        "claim":    ("state", 464, BAND_R1, 260, BAND_R1H, "server claim",
                     ["exclusive,", "expiring,", "recorded in git"]),
        "workers":  ("compute", 774, BAND_R1, 340, BAND_R1H, "workers",
                     ["short-lived servers", "opentofu + ansible", "reports spool offline"]),
        "hub":      ("compute", 1244, BAND_R1, MAIN_R - 1244, BAND_R1H, "run hub · stdlib + sqlite",
                     [f'run queue: {c["hub_lease_min"]} min lease,',
                      f'{c["hub_max_attempts"]} attempts, idempotent take', "events · metrics · backups"]),
        "authorize": ("human", 64, BAND_R2, 660, BAND_R2H, "", []),
        "models":   ("external", 774, BAND_R2, 340, BAND_R2H, "model apis", ["per-study budget ledger"]),
        "site":     ("external", 1244, BAND_R2, MAIN_R - 1244, BAND_R2H, "public live run site",
                     ["swarm-live.pages.dev"]),
    }


def side(n, s, off=0.0):
    """A point on a box side: l, r, t, b, with an offset along the side from its middle."""
    _, x, y, w, h = n[:5]
    return {"l": (x, y + h / 2 + off), "r": (x + w, y + h / 2 + off),
            "t": (x + w / 2 + off, y), "b": (x + w / 2 + off, y + h)}[s]


def edges(N):
    """Every connector: (kind, [points]). Points come from box sides, so moving a box moves its edges."""
    spine = lambda a, b: [(SPINE_X, N[a][2] + N[a][4]), (SPINE_X, N[b][2])]
    hx = N["humans"]
    dx = N["directives"][1] + 36
    sx = N["synthesis"][1] + 36
    ey = N["experiments"][2] + N["experiments"][4] / 2
    wk, hb = N["workers"], N["hub"]
    return [
        ("control", [(130, hx[2] + hx[4]), (130, REPO_Y)]),                                # humans start agents
        ("data", [(hx[1] + hx[3], 104), (dx, 104), (dx, COORD_Y)]),                        # humans write directives
        ("data", [(RX, 330), (LX + LW, 330)]),                                             # pull
        ("data", [(LX + LW, 386), (RX, 386)]),                                             # push
        ("data", [(700, REPO_Y), (700, TOP_Y + TOP_H)]),                                   # each push runs ci
        ("data", [(1400, TOP_Y + TOP_H), (1400, REPO_Y)]),                                 # ci writes generated files
        ("data", spine("library", "surveys")),
        ("data", spine("surveys", "hypotheses")),
        ("data", spine("hypotheses", "experiments")),
        ("data", [side(N["surveys"], "l"), side(N["synthesis"], "r")]),
        ("ungated", [(sx, N["synthesis"][2] + ROW_H), (sx, ey), (MAIN_X, ey)]),            # exploratory studies
        ("data", [side(N["experiments"], "r"), side(N["artifacts"], "l")]),
        ("control", [(230, REPO_B), (230, BAND_Y)]),                                       # agents launch
        ("control", [side(N["authorize"], "t", -150), side(N["admission"], "b", 0)]),    # human authorizes
        ("control", [side(N["admission"], "r"), side(N["claim"], "l")]),
        ("control", [side(N["claim"], "r"), side(wk, "l")]),
        ("control", [side(hb, "l", -24), side(wk, "r", -24)]),                             # hub hands out a run
        ("data", [side(wk, "r", 22), side(hb, "l", 22)]),                                  # workers report
        ("data", [side(wk, "b"), side(N["models"], "t")]),
        ("data", [side(hb, "b"), side(N["site"], "t")]),
        ("data", [(wk[1] + wk[3] / 2, wk[2]), (wk[1] + wk[3] / 2, N["experiments"][2] + ROW_H)]),  # records
    ]


# ---------------------------------------------------------------------------------------------- drawing
def draw_box(n, phase=False):
    kind, x, y, w, h, title, lines = n
    out = [rect(kind, x, y, w, h)]
    inner = w - 2 * PAD - (6 if kind == "compute" else 0)
    tx = x + PAD + (8 if kind == "compute" else 0) + (6 if kind in ("external", "human") else 0)
    if phase:                                       # folder name on the left, facts on the right
        out.append(text(x + 16, y + h / 2 + 8, title, size=S_NAME, weight=600, fit=DESC_X - x - 28))
        for i, s in enumerate(lines):
            out.append(text(DESC_X, y + 27 + 27 * i, s, op=0.8, fit=x + w - DESC_X - 8))
        return "".join(out)
    if h <= ROW_H:                                  # short box: name and one line
        out.append(text(tx, y + 28, title, size=S_NAME, weight=600, fit=inner))
        for i, s in enumerate(lines):
            out.append(text(tx, y + 54 + 26 * i, s, op=0.8, fit=inner))
        return "".join(out)
    big = kind in ("human", "agent")
    out.append(text(tx + (10 if kind == "human" else 12 if big else 0), y + (46 if big else 34), title,
                    size=S_BIG if big else S_NAME, weight=600, fit=inner - (70 if big else 0)))
    for i, s in enumerate(lines):
        out.append(text(tx + (10 if kind == "human" else 12 if big else 0), y + (80 if big else 64) + 28 * i, s,
                        op=0.8, fit=inner))
    return "".join(out)


def build(c):
    N = nodes(c)
    o = []
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{VOID}" stroke="{INK}" stroke-opacity="0.14"/>')
    o.append(f'<g font-family=\'{FONT}\'>')

    # containers first, then edges, then boxes, so a line never draws over a label
    for k in ("repo", "band"):
        o.append(draw_box(N[k]))
    for kind, pts in edges(N):
        o.append(arrow(pts, kind))
    for k, n in N.items():
        if k in ("repo", "band"):
            continue
        o.append(draw_box(n, phase=k in ("library", "surveys", "hypotheses", "experiments")))

    # --- principals
    hx = N["humans"]
    for i in range(c["researchers"]):
        o.append(person(hx[1] + hx[3] - 44 - 34 * i, hx[2] + 42))
    o.append(text(146, 216, "start, steer", fill=VIOLET))
    o.append(text(432, 94, "directives", op=0.9))

    # --- agents: identity, session loop, sync timer
    ax, ay = N["agents"][1], N["agents"][2]
    o.append(text(ax + LW - 30, ay + 46, ">_", size=S_BIG, fill=VIOLET, weight=700, anchor="end"))
    y0 = ay + 182
    o.append(f'<line x1="{ax + 24}" y1="{y0 - 34}" x2="{ax + LW - 24}" y2="{y0 - 34}" stroke="{VIOLET}" stroke-opacity="0.35"/>')
    o.append(text(ax + 24, y0, "SESSION LOOP", fill=VIOLET, track=0.14, weight=600))
    steps = [("sync", "pull rebase"), ("orient", "directives"), ("pick", "by priority"), ("claim", "task lease"),
             ("work", "own files"), ("heartbeat", "status file"), ("finish", "done/release"), ("log", "session log")]
    ys = [y0 + 46 + 48 * i for i in range(len(steps))]
    for (name, note), y in zip(steps, ys):
        o.append(text(ax + 64, y, name, fill=VIOLET, weight=600))
        o.append(text(ax + 204, y, note, op=0.8, fit=LW - 204 - 10))
    lx = ax + 34                                    # the loop closes: log back to sync
    o.append(arrow([(ax + 54, ys[-1] - 7), (lx, ys[-1] - 7), (lx, ys[0] - 7), (ax + 56, ys[0] - 7)], "control"))
    y1 = ys[-1] + 60
    o.append(f'<line x1="{ax + 24}" y1="{y1 - 34}" x2="{ax + LW - 24}" y2="{y1 - 34}" stroke="{VIOLET}" stroke-opacity="0.35"/>')
    o.append(text(ax + 24, y1, "SYNC TIMER", fill=VIOLET, track=0.14, weight=600))
    for i, s in enumerate([f'every {c["sync_min"]} min: push only', "files that pass check,",
                           "re-checked on a clean", "checkout; renew lease"]):
        o.append(text(ax + 24, y1 + 32 + 28 * i, s, op=0.8, fit=LW - 40))
    o.append(text((LX + LW + RX) / 2, 320, "pull", anchor="middle", op=0.9))
    o.append(text((LX + LW + RX) / 2, 376, "push", anchor="middle", op=0.9))

    # --- ci verifier: its three jobs
    jobs = [("check", ["schema · links · duplicates", "prior-art gate · tests"]),
            ("verify", ["new paper ids resolve", "on datacite, crossref"]),
            ("index", ["rebuilds lab/STATUS.md,", "1-library/INDEX.md"])]
    for (name, lines), jx in zip(jobs, (648, 1044, 1384)):
        o.append(text(jx, TOP_Y + 80, name, fill=AMBER, weight=600))
        for j, s in enumerate(lines):
            o.append(text(jx, TOP_Y + 106 + 26 * j, s, op=0.8, fit=(376 if jx < 1000 else 322)))
    o.append(text(648, TOP_Y + 44, "ci verifier · every push to main", size=S_NAME + 2, weight=600))
    o.append(text(716, 216, "each push", op=0.9))
    o.append(text(1416, 216, "generated files", op=0.9))

    # --- repository: header, write rule, phase path with its gates
    o.append(text(596, REPO_Y + 36, "SHARED STATE (BLACKBOARD) · ONE GIT REPOSITORY, BRANCH MAIN", track=0.14, weight=600,
                  fit=RR - 596 - 20))
    o.append(text(524, RULE_Y, "no orchestrator · no agent-to-agent messages · writes partitioned by owner",
                  fit=MAIN_R - 524))
    o.append(text(524, RULE_Y + 28, "optimistic concurrency: a conflicting push is rejected, the agent rebases",
                  op=0.8, fit=MAIN_R - 524))
    o.append(f'<line x1="524" y1="{RULE_Y + 46}" x2="{MAIN_R}" y2="{RULE_Y + 46}" stroke="{INK}" stroke-opacity="0.22"/>')
    o.append(text(580, RULE_Y + 76, "RESEARCH RECORD · PHASES IN ORDER", track=0.14, weight=600, op=0.9))
    gx = SPINE_X + 34
    gfit = RR - 14 - gx
    ya = Y_SUR + ROW_H
    o.append(diamond(SPINE_X, ya + 23))
    o.append(text(gx, ya + 30, f'prior-art gate (ci) ≥{c["min_cited"]} cited: {c["min_papers"]} papers, '
                  f'{c["min_code"]} code, {c["min_informal"]} informal', fill=AMBER, fit=gfit))
    o.append(text(gx, ya + 57, f'{c["min_full_reads"]} read in full · {c["min_seminal"]} seminal · '
                  f'{c["min_search_rounds"]} rounds, last {c["saturation_rounds"]} ≤{c["saturation_pct"]}% new',
                  fill=AMBER, fit=gfit))
    o.append(diamond(SPINE_X, ya + 78))
    o.append(text(gx, ya + 85, "review by a different researcher's agent, verdict pass", fill=AMBER, fit=gfit))
    yb = Y_HYP + ROW_H
    o.append(diamond(SPINE_X, yb + 21))
    o.append(text(gx, yb + 29, "accepted after review · plan committed before first run", fill=AMBER, fit=gfit))
    sx = N["synthesis"][1] + 36
    for i, s in enumerate(["exploratory", "studies,", "no gate"]):
        o.append(text(sx + 16, Y_SUR + ROW_H + 58 + 27 * i, s, op=0.9, fit=MAIN_X - sx - 30))

    # --- experiment plane
    o.append(text(LX + 44, BAND_Y + 36, "EXPERIMENT PLANE · ONE PASS PER ATTEMPT", track=0.14, weight=600))
    o.append(text(246, REPO_B + 29, "launch", fill=VIOLET))
    wk, hb = N["workers"], N["hub"]
    o.append(text(wk[1] + wk[3] / 2 + 18, REPO_B + 29, "saved records, post-mortem per attempt", op=0.9))
    mid = (wk[1] + wk[3] + hb[1]) / 2
    o.append(text(mid, wk[2] + wk[4] / 2 - 34, "next run", fill=VIOLET, anchor="middle", fit=hb[1] - wk[1] - wk[3] - 8))
    o.append(text(mid, wk[2] + wk[4] / 2 + 50, "report", anchor="middle", op=0.9))
    au = N["authorize"]
    o.append(person(au[1] + 36, au[2] + au[4] / 2 + 2))
    o.append(text(au[1] + 64, au[2] + au[4] / 2 + 8, "researcher authorizes budget and scope",
                  fit=au[3] - 64 - 16))

    # --- numbered callouts, referred to by the caption
    for n, (x, y) in enumerate([(LX, TOP_Y), (LX, REPO_Y), (RX, REPO_Y), (620, TOP_Y), (546, RULE_Y + 69),
                                (LX, BAND_Y), (N["site"][1] + N["site"][3], N["site"][2])], start=1):
        o.append(callout(n, x, y))

    # --- legend: the encoding, stated once
    x, y = LX + 4, LEGEND_Y
    for kind, label in [("human", "human"), ("agent", "agent"), ("state", "state in git"),
                        ("verifier", "gate, verifier"), ("compute", "compute"), ("external", "external")]:
        o.append(rect(kind, x, y - 19, 38, 24))
        if kind == "verifier":
            o.append(diamond(x + 19, y - 7, 8))
        o.append(text(x + 48, y, label, op=0.9))
        x += 48 + width_of(label, S_MIN) + 26
    for kind, label in [("control", "control"), ("data", "data"), ("ungated", "ungated")]:
        o.append(arrow([(x, y - 7), (x + 44, y - 7)], kind))
        o.append(text(x + 54, y, label, op=0.9))
        x += 54 + width_of(label, S_MIN) + 26
    if x > W - 70:
        WARNINGS.append(f"legend runs to x={x:.0f}")

    # --- the mark, low right: a plain solid at one fixed angle
    mx, my, r = W - 62, LEGEND_Y - 8, 15
    hx_, hy_ = r * 0.866, r * 0.5
    top = f"{f(mx)},{f(my - r)} {f(mx + hx_)},{f(my - hy_)} {f(mx)},{f(my)} {f(mx - hx_)},{f(my - hy_)}"
    left = f"{f(mx - hx_)},{f(my - hy_)} {f(mx)},{f(my)} {f(mx)},{f(my + r)} {f(mx - hx_)},{f(my + hy_)}"
    right = f"{f(mx + hx_)},{f(my - hy_)} {f(mx)},{f(my)} {f(mx)},{f(my + r)} {f(mx + hx_)},{f(my + hy_)}"
    o.append(f'<polygon points="{top}" fill="{INK}" fill-opacity="0.9"/><polygon points="{left}" fill="{INK}" '
             f'fill-opacity="0.5"/><polygon points="{right}" fill="{INK}" fill-opacity="0.25"/>')
    o.append("</g>")

    title = "Swarm Dynamics Lab: system architecture"
    desc = (f'{c["researchers"]} researchers steer {c["agents"]} agents. The agents share no orchestrator and send each '
            f'other no messages: they read and write one git repository, which holds the task board of {c["tasks"]} tasks, '
            "inboxes, agent status files and the research record in five numbered folders. A CI verifier checks every push. "
            "Amber marks the gates between surveys, hypotheses and experiments. Below, the experiment plane: pre-run "
            "admission, an exclusive server claim, workers on short-lived servers, a run hub with a leased run queue, "
            "model APIs under a budget ledger and a public live run site.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-labelledby="t d">\n<title id="t">{esc(title)}</title>\n<desc id="d">{esc(desc)}</desc>\n'
            + "\n".join(o) + "\n</svg>\n")


def main():
    c = read_counts()
    svg = build(c)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print("counts and thresholds used:")
    for k, v in c.items():
        print(f"  {k:18s} {v}")
    for w in WARNINGS:
        print("WARN", w)
    print(f"wrote {OUT.relative_to(ROOT)}  {W}x{H}  {len(svg.encode('utf-8')):,} bytes")


if __name__ == "__main__":
    main()
