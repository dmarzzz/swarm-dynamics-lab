"""Exact-total outcomes and real checker trace, no raw receipt content."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG = "#111a2b"
FG = "#eef4ff"
MUTED = "#a7b6d0"


def font(n):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, n)
    return ImageFont.load_default(size=n)


def text(d, xy, s, n=26, c=FG):
    d.text(xy, str(s), font=font(n), fill=c)


def canvas(title, subtitle):
    im = Image.new("RGB", (1800, 1100), BG)
    d = ImageDraw.Draw(im)
    text(d, (60, 40), title, 40)
    text(d, (60, 110), subtitle, 24, MUTED)
    return im, d


def render(out, records, outcomes, summary):
    im, d = canvas(
        "Antsy | accept, check, or refer?",
        f"{summary['assigned']} assigned receipts | {summary['scorable']} scorable | {summary['unscorable']} unscorable references | actual OCR tools",
    )
    colors = {"correct": "#57dca3", "wrong": "#fa777c", "refer": "#7488ac"}
    text(d, (60, 180), "Policy", 26)
    text(d, (460, 180), "Exact-total outcome counts", 26)
    text(d, (1270, 180), "Total / checker seconds", 24)
    for i, (arm, r) in enumerate(summary["arms"].items()):
        y = 250 + i * 122
        text(d, (60, y + 8), arm, 27)
        x = 460
        for label in ["correct", "wrong", "refer"]:
            w = 710 * r[label] / max(1, summary["scorable"])
            if w:
                d.rectangle((x, y, x + w, y + 48), fill=colors[label])
            x += w
        text(
            d,
            (460, y + 57),
            f"{r['correct']} correct / {r['wrong']} wrong / {r['refer']} refer",
            22,
            MUTED,
        )
        total = r.get("total_pipeline_wall_s")
        text(
            d,
            (1270, y + 8),
            f"{total:.1f}s / {r['checker_wall_s']:.1f}s"
            if total is not None
            else f"checks: {r['checker_wall_s']:.1f}s",
            25,
        )
        text(d, (1270, y + 52), f"{r['checks']} checker calls", 22, MUTED)
    text(
        d,
        (60, 910),
        "Green: correct acceptance     Red: wrong acceptance     Gray: referral (not correct)",
        26,
        MUTED,
    )
    text(
        d,
        (60, 970),
        "Tool seconds are summed measured pipeline costs, not online response time or human review time.",
        23,
        MUTED,
    )
    text(
        d,
        (60, 1020),
        "Exploratory tool pilot. Shared Tesseract errors; no model-committee or payment-safety claim.",
        23,
        MUTED,
    )
    im.save(out / "final_frame.png")
    # Every assigned receipt stays visible; missing references have their own color.
    im, d = canvas(
        "Antsy | where decisions change",
        "All assigned receipts, ordered by dataset ID. Blue outline: a checker was invoked.",
    )
    cell = min(27, 1400 / max(1, len(records)))
    for i, (arm, _) in enumerate(summary["arms"].items()):
        y = 270 + i * 120
        text(d, (40, y), arm, 23)
        for j, r in enumerate(records):
            o = next(x for x in outcomes if x["id"] == r["id"] and x["arm"] == arm)
            label = "correct" if o["correct"] else "wrong" if o["wrong"] else "refer"
            color = colors[label] if o["scorable"] else "#d0a753"
            x = 320 + j * cell
            d.rectangle(
                (x, y, x + cell - 3, y + 48),
                fill=color,
                outline="#68c4ff" if o["checks"] else BG,
                width=3,
            )
            if i == 0:
                text(d, (x, y - 35), r["id"], 14, MUTED)
    text(
        d,
        (60, 920),
        "Green correct | Red wrong | Gray refer | Yellow unknown reference",
        27,
        MUTED,
    )
    text(
        d,
        (60, 980),
        "Different policies replay the same measured tools. Agreement does not imply independent evidence.",
        24,
        MUTED,
    )
    im.save(out / "decision-map.png")
    examples = [
        (r, "First three assigned cases; no success-based example selection.")
        for r in records[:3]
    ]
    changed = next(
        (
            r
            for r in records
            if next(
                x
                for x in outcomes
                if x["id"] == r["id"] and x["arm"] == "selective-check"
            )["value"]
            != next(
                x for x in outcomes if x["id"] == r["id"] and x["arm"] == "agreement"
            )["value"]
        ),
        None,
    )
    if changed is not None and changed["id"] not in [r["id"] for r, _ in examples]:
        examples.append(
            (
                changed,
                "Post-hoc illustration: first decision changed by checking; not a representative sample.",
            )
        )
    for r, selection in examples:
        result = next(
            x for x in outcomes if x["id"] == r["id"] and x["arm"] == "selective-check"
        )
        visible = {k: r["pipelines"][k]["candidate"] for k in "ABC"}
        frames = []
        states = [("Initial candidates", dict(visible))]
        for ev in result["events"]:
            visible[ev["tool"]] = ev["response"]
            states.append(
                (
                    f"Checker {ev['tool']} returned after {r['pipelines'][ev['tool']]['wall_s']:.2f}s",
                    dict(visible),
                )
            )
        states.append(("Commit and evaluator reveal", dict(visible)))
        for i, (label, candidates) in enumerate(states):
            im, d = canvas(
                f"Antsy | receipt {r['id']} | {label}",
                "Actual candidate amounts and checker outputs. Ground truth hidden until commitment.",
            )
            for j, (tool, c) in enumerate(candidates.items()):
                text(
                    d,
                    (60, 220 + j * 105),
                    f"{tool}  {c['status']}  total={c['value']}  confidence={c['confidence']:.2f}",
                    29,
                )
            if i == len(states) - 1:
                text(
                    d,
                    (60, 830),
                    f"Decision: {result['action']} {result['value']} | reference: {r['gold']['status']} {r['gold']['value']}",
                    29,
                )
                text(
                    d,
                    (60, 910),
                    f"Correct={result['correct']}  wrong={result['wrong']}  refer={result['refer']}",
                    27,
                )
            else:
                text(d, (60, 910), "Evaluator reference: hidden", 28, MUTED)
            text(d, (60, 1010), selection, 22, MUTED)
            frames.append(im)
        frames[0].save(
            out / f"receipt-{r['id']:03}.gif",
            save_all=True,
            append_images=frames[1:],
            duration=1800,
            loop=0,
        )
