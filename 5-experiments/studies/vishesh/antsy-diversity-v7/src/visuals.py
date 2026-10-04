"""Deterministic charts from committed outcomes; no invented trajectories."""

import json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLORS = {
    "correct": "#32b78a",
    "wrong": "#ee786b",
    "refer": "#798ba5",
    "unknown": "#cbb77d",
}


def wilson(k, n):
    if not n:
        return None
    z = 1.96
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0, c - r), min(1, c + r)]


def intervals(outcomes, summary):
    rng = random.Random(71203)
    result = {
        "method": "Paired receipt bootstrap, 2000 replicates, seed 71203; exploratory percentile intervals. Wilson 95% accepted-error intervals. Receipt independence is an assumption; no multiplicity correction.",
        "arms": {},
        "contrasts": {},
    }
    for arm, s in summary["arms"].items():
        result["arms"][arm] = {
            "accepted_error_wilson95": wilson(s["wrong"], s["correct"] + s["wrong"])
        }
    for a, b in [
        ("mixed/majority", "related/majority"),
        ("mixed/provenance-dissent", "related/provenance-dissent"),
        ("mixed/provenance-dissent", "mixed/majority"),
    ]:
        aa = {o["id"]: o for o in outcomes if o["arm"] == a and o["scorable"]}
        bb = {o["id"]: o for o in outcomes if o["arm"] == b and o["scorable"]}
        ids = sorted(aa)
        n = len(ids)
        d = {}
        for metric in ["wrong", "coverage"]:
            vals = [
                float(aa[i]["wrong"]) - float(bb[i]["wrong"])
                if metric == "wrong"
                else float(not aa[i]["refer"]) - float(not bb[i]["refer"])
                for i in ids
            ]
            boot = (
                sorted(sum(rng.choices(vals, k=n)) / n for _ in range(2000))
                if n
                else []
            )
            d[metric] = {
                "difference": sum(vals) / n if n else None,
                "ci95": [boot[49], boot[1949]] if boot else None,
                "denominator": n,
            }
        result["contrasts"][a + " minus " + b] = d
    return result


def canvas(title, subtitle, h=1060):
    im = Image.new("RGB", (1800, h), "#0f1724")
    d = ImageDraw.Draw(im)
    for size, key in [(34, "title"), (22, "body"), (17, "small")]:
        try:
            f = ImageFont.truetype("DejaVuSans.ttf", size)
        except OSError:
            f = ImageFont.load_default(size=size)
        setattr(canvas, key, f)
    d.text((45, 25), title, font=canvas.title, fill="white")
    d.text((45, 78), subtitle, font=canvas.body, fill="#bfccdf")
    return im, d


def render(out, records, outcomes, summary, div):
    out = Path(out)
    (out / "uncertainty.json").write_text(
        json.dumps(intervals(outcomes, summary), indent=2)
    )
    im, d = canvas(
        "Antsy: does a different worker bring different evidence?",
        f"{summary['assigned']} assigned receipts | {summary['scorable']} scorable | 5 measured OCR workers | all arms paired on the same receipts",
    )
    for j, (arm, s) in enumerate(summary["arms"].items()):
        y = 150 + j * 66
        d.text((45, y), arm, font=canvas.body, fill="white")
        x = 520
        for key in ["correct", "wrong", "refer"]:
            w = 800 * s[key] / max(1, summary["scorable"])
            d.rectangle((x, y, x + w, y + 35), fill=COLORS[key])
            x += w
        d.text(
            (1350, y),
            f"{s['correct']} / {s['wrong']} / {s['refer']}   {s['tool_s']:.1f}s",
            font=canvas.body,
            fill="white",
        )
    d.text(
        (45, 915),
        "Green: correct | coral: wrong accepted | gray: refer. Right: counts and measured serial tool time.",
        font=canvas.body,
        fill="#bfccdf",
    )
    d.text(
        (45, 954),
        "Equal team size does not imply equal compute. Unknown-reference acceptance is reported separately in summary.json.",
        font=canvas.small,
        fill="#bfccdf",
    )
    im.save(out / "outcomes.png")
    im, d = canvas(
        "Agreement can conceal a shared mistake",
        "Cells: same wrong total / scorable receipts; below: answer agreement among co-answered receipts",
    )
    names = list(records[0]["workers"])
    for i, a in enumerate(names):
        d.text((70, 200 + i * 140), a, font=canvas.title, fill="white")
        d.text((270 + i * 270, 140), a, font=canvas.title, fill="white")
        for j, b in enumerate(names):
            x = 230 + j * 270
            y = 205 + i * 140
            if i == j:
                d.text((x, y), "same worker", font=canvas.body, fill="#798ba5")
                continue
            key = a + "--" + b if i < j else b + "--" + a
            p = div["pairs"][key]
            d.rectangle(
                (x - 12, y - 12, x + 238, y + 105),
                fill="#482e3b" if p["same_wrong"] else "#20384a",
            )
            d.text(
                (x, y),
                f"{p['same_wrong']} / {p['scorable']}",
                font=canvas.title,
                fill="white",
            )
            ag = p["answer_agreement"]
            d.text(
                (x, y + 50),
                f"agree {ag:.0%}, n={p['co_answered']}"
                if ag is not None
                else "no co-answers",
                font=canvas.small,
                fill="#bfccdf",
            )
    d.text(
        (45, 955),
        "Shared source pixels and extractor remain common failure paths. Pairwise correlation is not proof of independence.",
        font=canvas.small,
        fill="#bfccdf",
    )
    im.save(out / "same-wrong.png")
    arms = list(summary["arms"])
    h = max(650, 170 + len(records) * 27)
    im, d = canvas(
        "Every assigned receipt, every decision",
        "Green correct | coral wrong accepted | gray refer | gold unknown reference. Columns follow the numbered arm key.",
        h,
    )
    for j, arm in enumerate(arms):
        d.text((200 + j * 135, 122), str(j + 1), font=canvas.body, fill="white")
    lookup = {(o["id"], o["arm"]): o for o in outcomes}
    for i, r in enumerate(records):
        y = 165 + i * 27
        d.text((45, y), str(r["id"]), font=canvas.small, fill="white")
        for j, arm in enumerate(arms):
            o = lookup[r["id"], arm]
            key = (
                "unknown"
                if not o["scorable"]
                else "correct"
                if o["correct"]
                else "wrong"
                if o["wrong"]
                else "refer"
            )
            d.rectangle((195 + j * 135, y, 310 + j * 135, y + 20), fill=COLORS[key])
    im.save(out / "decision-map.png")
    (out / "arm-key.json").write_text(json.dumps(dict(enumerate(arms, 1)), indent=2))
    frames = []
    for r in records[:3]:
        for revealed in range(1, 7):
            im, d = canvas(
                f"Receipt {r['id']}: observed worker sequence",
                "Replay of measured candidates; timing normalized. Reference revealed only in the final frame.",
                720,
            )
            for j, (name, w) in enumerate(r["workers"].items()):
                shown = j < revealed
                value = str(w["candidate"]["value"]) if shown else "pending"
                d.text(
                    (80, 160 + j * 70),
                    f"{name}   {w['family']:<12}   {value}",
                    font=canvas.title,
                    fill="white" if shown else "#798ba5",
                )
            if revealed == 6:
                d.text(
                    (80, 575),
                    f"Reference: {r['gold']['value']} ({r['gold']['status']})",
                    font=canvas.title,
                    fill="#32b78a",
                )
            frames.append(im)
    frames[0].save(
        out / "observed-traces.gif",
        save_all=True,
        append_images=frames[1:],
        duration=850,
        loop=0,
    )
