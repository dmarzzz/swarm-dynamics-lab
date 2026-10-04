"""Frozen operational policies and truth-separated diversity measurements."""

import collections, hashlib, importlib.util, json, math, re
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "antsy-receipt-v6/src/contract.py"
spec = importlib.util.spec_from_file_location("antsy6_contract", p)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
amount = old.amount
reference = old.reference
ANCHOR = re.compile(
    r"\b(?:grand\s*total|total\s+bayar|jumlah\s+bayar|amount\s+due|total|due)\b", re.I
)
EXCLUDE = old.EXCLUDE
TEAMS = {
    "related": ["T0", "T1", "T2"],
    "mixed": ["T0", "T1", "R0"],
    "mixed-robustness": ["T0", "R0", "R1"],
}


def digest(x):
    return hashlib.sha256(
        json.dumps(x, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def extract(lines):
    found = []
    for line in lines:
        s = line["text"]
        a = ANCHOR.search(s)
        if not a or EXCLUDE.search(s):
            continue
        left = s[: a.start()].strip(" \t")
        right = s[a.end() :].strip(" \t")
        if left and not left.strip("*"):
            left = ""
        right = re.sub(r"^\.(?:\s+|$)", "", right).lstrip(": \t")
        if right == ".":
            right = ""
        # Accept exactly one value adjacent to a legitimate label, not arbitrary salvage.
        raw = right if not left else left if not right else None
        value = amount(raw) if raw is not None else None
        if value is not None:
            found.append((value, line.get("confidence", 0.0), line.get("region_hash")))
    values = {x[0] for x in found}
    if len(values) != 1:
        return {
            "status": "ambiguous" if values else "missing",
            "value": None,
            "confidence": 0.0,
            "regions": [],
        }
    value = next(iter(values))
    return {
        "status": "ok",
        "value": value,
        "confidence": max(x[1] for x in found),
        "regions": sorted({x[2] for x in found if x[2]}),
    }


def spatial_lines(words):
    groups = []
    for w in sorted(words, key=lambda w: (w["y"], w["x"])):
        candidates = [
            g
            for g in groups
            if abs(w["y"] - g["y"]) <= max(3, min(w["h"], g["h"]) * 0.5)
        ]
        if candidates:
            min(candidates, key=lambda g: abs(w["y"] - g["y"]))["words"].append(w)
        else:
            groups.append({"y": w["y"], "h": w["h"], "words": [w]})
    return [
        {
            "text": " ".join(
                w["text"] for w in sorted(g["words"], key=lambda w: w["x"])
            ),
            "confidence": sum(w["confidence"] for w in g["words"]) / len(g["words"]),
            "region_hash": digest(sorted(w["box"] for w in g["words"])),
        }
        for g in groups
    ]


def payload(record, ids):
    return [
        {k: record["workers"][i][k] for k in ["id", "family", "origin", "candidate"]}
        for i in ids
    ]


def decide(items, rule):
    if rule == "provenance-dissent":
        unique = {}
        for item in items:
            root = item["origin"]
            if root in unique and unique[root]["candidate"] != item["candidate"]:
                raise ValueError("conflicting duplicate provenance")
            unique[root] = item
        items = list(unique.values())
    elif rule != "majority":
        raise ValueError("rule")
    valid = [x for x in items if x["candidate"]["status"] == "ok"]
    counts = collections.Counter(x["candidate"]["value"] for x in valid)
    ranked = counts.most_common()
    value = None
    if (
        ranked
        and ranked[0][1] >= 2
        and (len(ranked) == 1 or ranked[0][1] > ranked[1][1])
    ):
        if rule == "majority" or len(ranked) == 1:
            value = ranked[0][0]
    support = (
        [x for x in valid if x["candidate"]["value"] == value]
        if value is not None
        else []
    )
    return {
        "action": "accept" if value is not None else "refer",
        "value": value,
        "support_origins": sorted({x["origin"] for x in support}),
        "support_families": sorted({x["family"] for x in support}),
        "dissent": len(counts) > 1,
    }


def grade(value, gold):
    known = gold["status"] == "ok"
    return {
        "scorable": known,
        "correct": known and value == gold["value"],
        "wrong": known and value is not None and value != gold["value"],
        "refer": value is None,
    }


def evaluate(records):
    out = []
    for r in records:
        for team, ids in TEAMS.items():
            for rule in ["majority", "provenance-dissent"]:
                d = decide(payload(r, ids), rule)
                out.append(
                    {
                        "id": r["id"],
                        "arm": team + "/" + rule,
                        **d,
                        **grade(d["value"], r["gold"]),
                        "tool_s": sum(r["workers"][i]["wall_s"] for i in ids),
                    }
                )
        for i, w in r["workers"].items():
            v = w["candidate"]["value"] if w["candidate"]["status"] == "ok" else None
            out.append(
                {
                    "id": r["id"],
                    "arm": "single/" + i,
                    "action": "accept" if v is not None else "refer",
                    "value": v,
                    **grade(v, r["gold"]),
                    "tool_s": w["wall_s"],
                }
            )
    summary = {
        "assigned": len(records),
        "scorable": sum(r["gold"]["status"] == "ok" for r in records),
        "invalid": sum(not w["valid"] for r in records for w in r["workers"].values()),
        "arms": {},
    }
    for arm in sorted({o["arm"] for o in out}):
        rr = [o for o in out if o["arm"] == arm]
        sc = [o for o in rr if o["scorable"]]
        correct = sum(o["correct"] for o in sc)
        wrong = sum(o["wrong"] for o in sc)
        n = len(sc)
        summary["arms"][arm] = {
            "correct": correct,
            "wrong": wrong,
            "refer": sum(o["refer"] for o in sc),
            "unknown_accepted": sum(not o["scorable"] and not o["refer"] for o in rr),
            "coverage": (correct + wrong) / n if n else None,
            "accepted_error": wrong / (correct + wrong) if correct + wrong else None,
            "tool_s": sum(o["tool_s"] for o in rr),
        }
    return out, summary


def pair_stats(records, a, b):
    sc = [r for r in records if r["gold"]["status"] == "ok"]
    n = len(sc)
    answer = same = bothwrong = samewrong = jointnoncorrect = rescuea = rescueb = 0
    ca = []
    cb = []
    for r in sc:
        x = r["workers"][a]["candidate"]
        y = r["workers"][b]["candidate"]
        g = r["gold"]["value"]
        xa = x["status"] == "ok"
        ya = y["status"] == "ok"
        xc = xa and x["value"] == g
        yc = ya and y["value"] == g
        ca.append(int(xc))
        cb.append(int(yc))
        answer += xa and ya
        same += xa and ya and x["value"] == y["value"]
        bothwrong += xa and ya and not xc and not yc
        samewrong += xa and ya and not xc and not yc and x["value"] == y["value"]
        jointnoncorrect += not xc and not yc
        rescuea += xc and not yc
        rescueb += yc and not xc
    ma = sum(ca) / n if n else 0
    mb = sum(cb) / n if n else 0
    den = math.sqrt(sum((x - ma) ** 2 for x in ca) * sum((y - mb) ** 2 for y in cb))
    phi = sum((x - ma) * (y - mb) for x, y in zip(ca, cb)) / den if den else None
    missing_same = sum(
        (r["workers"][a]["candidate"]["status"] != "ok")
        == (r["workers"][b]["candidate"]["status"] != "ok")
        for r in records
    )
    return {
        "assigned": len(records),
        "scorable": n,
        "co_answered": answer,
        "same_answer": same,
        "answer_agreement": same / answer if answer else None,
        "double_wrong": bothwrong,
        "same_wrong": samewrong,
        "same_wrong_per_scorable": samewrong / n if n else None,
        "joint_noncorrect": jointnoncorrect,
        "a_correct_b_not": rescuea,
        "b_correct_a_not": rescueb,
        "correctness_phi": phi,
        "missingness_agreement": missing_same / len(records) if records else None,
    }


def diversity(records):
    ids = list(records[0]["workers"]) if records else []
    result = {"pairs": {}, "workers": {}}
    for j, a in enumerate(ids):
        for b in ids[j + 1 :]:
            result["pairs"][a + "--" + b] = pair_stats(records, a, b)
    for i in ids:
        rr = [r for r in records if r["gold"]["status"] == "ok"]
        result["workers"][i] = {
            "correct": sum(
                r["workers"][i]["candidate"]["value"] == r["gold"]["value"] for r in rr
            ),
            "unique_correct": sum(
                r["workers"][i]["candidate"]["value"] == r["gold"]["value"]
                and all(
                    w["candidate"]["value"] != r["gold"]["value"]
                    for k, w in r["workers"].items()
                    if k != i
                )
                for r in rr
            ),
            "valid_outputs": sum(
                r["workers"][i]["candidate"]["status"] == "ok" for r in records
            ),
        }
    result["candidate_oracle"] = sum(
        r["gold"]["status"] == "ok"
        and any(
            w["candidate"]["value"] == r["gold"]["value"] for w in r["workers"].values()
        )
        for r in records
    )
    return result
