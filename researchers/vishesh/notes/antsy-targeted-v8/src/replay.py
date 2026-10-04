"""Analyze saved development observations; never invoke OCR or open fresh data."""

import argparse, hashlib, json
from pathlib import Path
from fields import extract, policy


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def analyze(raw, records):
    produced = []
    input_hashes = {}
    # All candidate generation completes before the evaluator consumes gold values.
    for r in records:
        candidates = {}
        for w in r["workers"]:
            p = raw / f"train-{r['id']}-{w}.json"
            input_hashes[p.name] = sha(p)
            candidates[w] = extract(json.loads(p.read_text())["raw_words"])
        produced.append({"id": r["id"], "candidates": candidates})
    summary = {
        "kind": "development replay, not fresh qualification",
        "assigned": len(records),
        "scorable": sum(r["gold"]["status"] == "ok" for r in records),
        "new_ocr_calls": 0,
        "new_hosted_model_calls": 0,
        "workers": {},
        "policies": {},
    }
    for w in records[0]["workers"]:
        summary["workers"][w] = {}
        for version in ["old", "new"]:
            c = wrong = ref = unknown = 0
            for r, new in zip(records, produced):
                x = (
                    r["workers"][w]["candidate"]
                    if version == "old"
                    else new["candidates"][w]
                )
                v = x["value"] if x["status"] == "ok" else None
                g = r["gold"]
                if g["status"] != "ok":
                    unknown += v is not None
                    continue
                c += v == g["value"]
                wrong += v is not None and v != g["value"]
                ref += v is None
            summary["workers"][w][version] = {
                "correct": c,
                "wrong": wrong,
                "refer": ref,
                "unknown_accepted": unknown,
            }
    for mode in [
        "primary",
        "checker",
        "targeted-fallback",
        "always-fallback",
        "agreement",
    ]:
        c = wrong = ref = unknown = 0
        cost = 0
        checker_uses = 0
        for r, new in zip(records, produced):
            d = policy(new["candidates"]["R0"], new["candidates"]["T1"], mode)
            new.setdefault("policies", {})[mode] = d
            v = d["value"]
            cost += sum(
                r["workers"]["R0" if x == "P" else "T1"]["wall_s"] for x in d["used"]
            )
            checker_uses += "C" in d["used"]
            g = r["gold"]
            if g["status"] != "ok":
                unknown += v is not None
                continue
            c += v == g["value"]
            wrong += v is not None and v != g["value"]
            ref += v is None
        summary["policies"][mode] = {
            "correct": c,
            "wrong": wrong,
            "refer": ref,
            "unknown_accepted": unknown,
            "checker_uses": checker_uses,
            "replayed_worker_seconds": cost,
        }
    return {
        "summary": summary,
        "records": produced,
        "input_sha256": input_hashes,
        "source_sha256": {p.name: sha(p) for p in Path(__file__).parent.glob("*.py")},
        "limits": "Used train40–59; developer saw prior outcomes; no held-out inference. Cost reuses v7 worker durations, excludes new parser time, and is not measured v8 latency.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--raw", type=Path, required=True)
    p.add_argument("--records", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    assert not a.out.exists(), "preserve earlier report"
    rr = [json.loads(x) for x in a.records.read_text().splitlines()]
    assert [r["id"] for r in rr] == list(range(40, 60)), "development-only allowlist"
    result = analyze(a.raw, rr)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))
