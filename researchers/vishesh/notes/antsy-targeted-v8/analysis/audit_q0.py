"""Offline closeout supplement. Never calls OCR or changes the frozen instrument."""

import argparse, hashlib, json, math
from pathlib import Path


def wilson(k, n):
    if not n:
        return None
    if not 0 <= k <= n:
        raise ValueError("invalid binomial denominator")
    z = 1.959963984540054
    p = k / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [max(0, center - half), min(1, center + half)]


def audit(records, journal, reported):
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)) or any(i not in range(60, 80) for i in ids):
        raise ValueError("invalid receipt identity")
    starts = [(e["id"], e["worker"]) for e in journal if e["status"] == "started"]
    terminals = [
        (e["id"], e["worker"]) for e in journal if e["status"] in ["valid", "error"]
    ]
    if len(starts) != len(set(starts)) or len(terminals) != len(set(terminals)):
        raise ValueError("duplicate call identity")
    expected = {(i, w) for i in range(60, 80) for w in ["P", "C"]}
    if not set(starts) <= expected or not set(terminals) <= set(starts):
        raise ValueError("orphan or out-of-scope call")
    valid = {(e["id"], e["worker"]) for e in journal if e["status"] == "valid"}
    if any((i, w) not in valid for i in ids for w in ["P", "C"]):
        raise ValueError("completed receipt lacks valid call")
    result = {
        "receipt_units": len(records),
        "vendor_layout_independence": "unknown",
        "planned_receipts": 20,
        "started": len(starts),
        "valid": len(valid),
        "unstarted": 40 - len(starts),
        "unresolved_started": len(set(starts) - set(terminals)),
        "readers": {},
        "conditional": {},
    }
    scorable = [r for r in records if r["gold"]["status"] == "ok"]

    def value(r, w):
        c = r["workers"][w]["candidate"]
        if c["status"] == "ok" and c["value"] is None:
            raise ValueError("ok candidate without amount")
        return c["value"] if c["status"] == "ok" else None

    for w, arm in [("P", "primary"), ("C", "checker")]:
        c = e = ref = u = 0
        for r in records:
            v = value(r, w)
            if r["gold"]["status"] != "ok":
                u += v is not None
            elif v is None:
                ref += 1
            elif v == r["gold"]["value"]:
                c += 1
            else:
                e += 1
        a = {"correct": c, "wrong": e, "refer": ref, "unknown_accepted": u}
        if any(reported["arms"][arm][k] != v for k, v in a.items()):
            raise ValueError("summary tally mismatch")
        result["readers"][w] = dict(
            a,
            correctness_wilson95=wilson(c, len(scorable)),
            accepted_error_wilson95=wilson(e, c + e),
        )
    missing = [r for r in scorable if value(r, "P") is None]
    wrong = [
        r
        for r in scorable
        if value(r, "P") is not None and value(r, "P") != r["gold"]["value"]
    ]
    correct = [r for r in scorable if value(r, "P") == r["gold"]["value"]]
    for name, rr in [
        ("checker_correct_given_primary_missing", missing),
        ("checker_correct_given_primary_wrong", wrong),
    ]:
        k = sum(value(r, "C") == r["gold"]["value"] for r in rr)
        result["conditional"][name] = {
            "numerator": k,
            "denominator": len(rr),
            "wilson95": wilson(k, len(rr)),
        }
    result["conditional"]["agreement_refers_correct_primary"] = {
        "numerator": sum(value(r, "C") != value(r, "P") for r in correct),
        "denominator": len(correct),
    }
    if any(reported[k] != result[k] for k in ["started", "valid", "unstarted"]):
        raise ValueError("journal count mismatch")
    # Independent qualification reconstruction, not an import of the production scorer.
    qualified = (
        set(ids) == set(range(60, 80))
        and set(starts) == expected
        and valid == expected
        and len(terminals) == 40
        and len(scorable) >= 16
        and all(
            a["correct"] >= 0.5 * len(scorable) and a["wrong"] <= 1
            for a in result["readers"].values()
        )
    )
    if qualified != reported["qualified"]:
        raise ValueError("qualification mismatch")
    result.update(
        qualified=qualified,
        same_author=True,
        scope="Descriptive qualification only. Receipt dependence and adaptive development limit population inference; intervals assume independent binomial receipt outcomes.",
    )
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if a.out.exists():
        raise ValueError("refuse to overwrite audit")
    paths = [a.results / n for n in ["records.jsonl", "calls.jsonl", "summary.json"]]
    records = (
        [json.loads(x) for x in paths[0].read_text().splitlines()]
        if paths[0].exists()
        else []
    )
    journal = (
        [json.loads(x) for x in paths[1].read_text().splitlines()]
        if paths[1].exists()
        else []
    )
    result = audit(records, journal, json.loads(paths[2].read_text()))
    result["input_sha256"] = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        for p in paths
    }
    a.out.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
