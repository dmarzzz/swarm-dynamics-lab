"""Post-hoc error illustration from actual numeric records, not a new run."""

import argparse, json
from pathlib import Path
from render import canvas, text, MUTED


def render_error(root, ident):
    r = next(
        json.loads(x)
        for x in (root / "records.jsonl").read_text().splitlines()
        if json.loads(x)["id"] == ident
    )
    rows = [
        o for o in json.loads((root / "outcomes.json").read_text()) if o["id"] == ident
    ]
    im, d = canvas(
        f"Antsy | receipt {ident}: when agreement is wrong",
        "Post-hoc error analysis. Colors use evaluator truth after commitment, never policy input.",
    )
    for i, (tool, p) in enumerate(r["pipelines"].items()):
        x = 65 + i * 345
        c = p["candidate"]
        correct = r["gold"]["status"] == "ok" and c["value"] == r["gold"]["value"]
        color = "#57dca3" if correct else "#fa777c"
        d.rounded_rectangle((x, 225, x + 305, 460), radius=18, outline=color, width=4)
        text(d, (x + 25, 250), tool + (" initial" if tool in "ABC" else " checker"), 27)
        text(d, (x + 25, 320), c["value"], 30, color)
        text(d, (x + 25, 380), f"confidence {c['confidence']:.2f}", 23, MUTED)
    for j, arm in enumerate(["agreement", "always-check", "selective-check"]):
        o = next(o for o in rows if o["arm"] == arm)
        text(
            d,
            (65, 550 + j * 105),
            f"{arm}: {o['action']} {o['value']} | checks {','.join(o['checks']) or 'none'}",
            30,
        )
    text(
        d,
        (65, 900),
        f"Annotated total: {r['gold']['value']} | a correct minority can lose to correlated OCR errors.",
        28,
        "#57dca3",
    )
    text(
        d,
        (65, 985),
        "Illustrative observed failure, not a representative sample or an independent-agent experiment.",
        23,
        MUTED,
    )
    im.save(root / f"error-case-{ident:03}.png")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--id", type=int, required=True)
    a = p.parse_args()
    render_error(a.run, a.id)
