"""Targeted extractor repair from preserved OCR; no new OCR or model calls.

The original measured pipeline wall times are inherited, not re-measured.
Parser-only repair wall time is separate; this is not an online latency run.
"""

import argparse, hashlib, json, subprocess, time
from pathlib import Path
from contract import extract
from measure import lines_from_tsv
from study import evaluate
from render import render
from audit import audit
from analyze import analyze


def reparse(parent, out):
    pm = json.loads((parent / "manifest.json").read_text())
    assert pm["complete"] and pm["invalid_ocr"] == 0
    out.mkdir(parents=True, exist_ok=False)
    source = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    raw = (parent / "records.jsonl").read_bytes()
    m = {
        **pm,
        "source": source,
        "complete": False,
        "measurement_source": pm["source"],
        "parent_run": parent.name,
        "parent_records_sha256": hashlib.sha256(raw).hexdigest(),
        "new_ocr_calls": 0,
        "model_calls": 0,
        "kind": "targeted-parser-repair",
        "utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "latency_semantics": "Inherited original pipeline wall measurements; repair parser wall separately measured. Not online end-to-end latency.",
    }
    (out / "manifest.json").write_text(json.dumps(m, indent=2))
    records = [json.loads(x) for x in raw.splitlines()]
    changes = []
    started = time.monotonic()
    for r in records:
        for tool, p in r["pipelines"].items():
            tsv = parent / "private" / f"{r['split']}-{r['id']}-{tool}.tsv"
            new = extract(lines_from_tsv(tsv.read_text()))
            if new != p["candidate"]:
                changes.append(
                    {
                        "id": r["id"],
                        "tool": tool,
                        "before": p["candidate"],
                        "after": new,
                    }
                )
            p["candidate"] = new
    m["repair_parser_wall_s"] = time.monotonic() - started
    outcomes, summary = evaluate(records)
    # Carry the existing development-overlap diagnostic; image assignment did not change.
    old = json.loads((parent / "summary.json").read_text())
    if "exact_header_fingerprint_overlap" in old:
        summary["exact_header_fingerprint_overlap"] = old[
            "exact_header_fingerprint_overlap"
        ]
    (out / "records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
    for name, value in [
        ("outcomes.json", outcomes),
        ("summary.json", summary),
        ("candidate-changes.json", changes),
    ]:
        (out / name).write_text(json.dumps(value, indent=2))
    render(out, records, outcomes, summary)
    m.update(complete=True, wall_s=time.monotonic() - started)
    (out / "manifest.json").write_text(json.dumps(m, indent=2))
    (out / "audit.json").write_text(json.dumps(audit(out), indent=2))
    (out / "analysis.json").write_text(json.dumps(analyze(out), indent=2))
    return {
        "assigned": len(records),
        "candidate_changes": len(changes),
        "new_ocr_calls": 0,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--parent", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--report", action="store_true")
    a = p.parse_args()
    exp = "antsy-receipt-v6"
    rid = exp + "/" + a.out.name
    if a.report:
        import swarm_report as sr

        sr.report(
            "start",
            exp,
            rid,
            message="Targeted hyphenated-subtotal repair. Replay preserved real OCR; zero new OCR/model calls. Original measured tool cost inherited, parser repair time separate.",
            strict=True,
        )
    try:
        metrics = reparse(a.parent, a.out)
        if a.report:
            for f in a.out.iterdir():
                if f.is_file():
                    sr.upload(rid, f, f.name)
            sr.report(
                "done",
                exp,
                rid,
                metrics=metrics,
                message="Targeted parser repair replay complete and audited. No efficacy or independent model claim.",
                strict=True,
            )
        print(json.dumps(metrics))
    except Exception as e:
        if a.report:
            sr.report(
                "fail",
                exp,
                rid,
                message=type(e).__name__ + " in parser repair; preserve parent",
                strict=True,
            )
        raise


if __name__ == "__main__":
    main()
