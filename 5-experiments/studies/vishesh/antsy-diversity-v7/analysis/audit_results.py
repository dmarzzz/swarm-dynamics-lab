"""Separate-implementation read-only audit; same author, not independent review."""

import argparse, collections, json, math
from pathlib import Path


def audit(root):
    root = Path(root)
    m = json.loads((root / "manifest.json").read_text())
    records = [json.loads(x) for x in (root / "records.jsonl").read_text().splitlines()]
    out = json.loads((root / "outcomes.json").read_text())
    s = json.loads((root / "summary.json").read_text())
    d = json.loads((root / "diversity.json").read_text())
    events = [json.loads(x) for x in (root / "calls.jsonl").read_text().splitlines()]
    assert (
        m["complete"]
        and len(records) == len(m["ids"])
        and [r["id"] for r in records] == m["ids"]
    )
    assert len({r["image_sha256"] for r in records}) == len(records)
    starts = collections.Counter(
        (e["receipt"], e["worker"]) for e in events if e["status"] == "started"
    )
    ends = collections.Counter(
        (e["receipt"], e["worker"]) for e in events if e["status"] == "valid"
    )
    expected = {(r["id"], w): 1 for r in records for w in r["workers"]}
    assert starts == ends == expected and len(events) == 10 * len(records)
    assert (
        m["ocr_calls"] == 5 * len(records)
        and m["model_calls"] == 0
        and s["invalid"] == 0
    )
    arms = {
        "related": ["T0", "T1", "T2"],
        "mixed": ["T0", "T1", "R0"],
        "mixed-robustness": ["T0", "R0", "R1"],
    }
    lookup = {(o["id"], o["arm"]): o for o in out}
    assert len(lookup) == 11 * len(records)
    for r in records:

        def candidate(w):
            c = r["workers"][w]["candidate"]
            return c["value"] if c["status"] == "ok" else None

        for arm in s["arms"]:
            if arm.startswith("single/"):
                workers = [arm.split("/")[1]]
                value = candidate(workers[0])
            else:
                team, rule = arm.split("/")
                workers = arms[team]
                values = [candidate(w) for w in workers]
                voted = {v: values.count(v) for v in values if v is not None}
                wins = [v for v, n in voted.items() if n >= 2]
                value = wins[0] if len(wins) == 1 else None
                if rule == "provenance-dissent" and len(voted) > 1:
                    value = None
            o = lookup[r["id"], arm]
            assert o["value"] == value
            assert math.isclose(
                o["tool_s"],
                sum(r["workers"][w]["wall_s"] for w in workers),
                abs_tol=1e-8,
            )
            known = r["gold"]["status"] == "ok"
            assert o["scorable"] == known
            assert o["correct"] == (known and value == r["gold"]["value"])
            assert o["wrong"] == (
                known and value is not None and value != r["gold"]["value"]
            )
    for arm, ss in s["arms"].items():
        rr = [o for o in out if o["arm"] == arm and o["scorable"]]
        assert (
            ss["correct"] == sum(o["correct"] for o in rr)
            and ss["wrong"] == sum(o["wrong"] for o in rr)
            and ss["refer"] == sum(o["value"] is None for o in rr)
        )
    for pair, p in d["pairs"].items():
        a, b = pair.split("--")
        rr = [r for r in records if r["gold"]["status"] == "ok"]
        n = 0
        co = 0
        same = 0
        both = 0
        for r in rr:
            x = r["workers"][a]["candidate"]
            y = r["workers"][b]["candidate"]
            ok = x["status"] == y["status"] == "ok"
            co += ok
            same += ok and x["value"] == y["value"]
            bw = (
                ok
                and x["value"] != r["gold"]["value"]
                and y["value"] != r["gold"]["value"]
            )
            both += bw
            n += bw and x["value"] == y["value"]
        assert (
            p["scorable"],
            p["co_answered"],
            p["same_answer"],
            p["double_wrong"],
            p["same_wrong"],
        ) == (len(rr), co, same, both, n)
    return {
        "passed": True,
        "records": len(records),
        "started_and_valid_calls": len(starts),
        "policy_outcomes": len(out),
        "pair_checks": len(d["pairs"]),
        "implementation": "Separate reconstruction from saved candidates and gold; same-author review, no new inference.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("root", type=Path)
    a = p.parse_args()
    print(json.dumps(audit(a.root), indent=2))
