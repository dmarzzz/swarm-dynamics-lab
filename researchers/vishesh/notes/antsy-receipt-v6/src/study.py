"""Real receipt-total application pilot with protected observations and full accounting."""

import argparse, gzip, hashlib, json, subprocess, time, platform, importlib.metadata
from pathlib import Path
from contract import ARMS, actor, run_policy, grade, reference
from measure import dataset, measure, REV


def evaluate(records):
    outcomes = []
    for r in records:
        for arm in ARMS:
            # Only numeric candidate records cross this boundary; no gold access.
            result = run_policy(
                actor(r), lambda tool: dict(r["pipelines"][tool]["candidate"]), arm
            )
            score = grade(result, r["gold"])
            outcomes.append(
                {
                    "id": r["id"],
                    "arm": arm,
                    **result,
                    **score,
                    "initial_ocr_calls": 1 if arm == "fixed-B" else 3,
                    "initial_wall_s": sum(
                        r["pipelines"][t]["wall_s"]
                        for t in ("B" if arm == "fixed-B" else "ABC")
                    ),
                    "checker_wall_s": sum(
                        r["pipelines"][t]["wall_s"] for t in result["checks"]
                    ),
                    "execution_valid": all(p["valid"] for p in r["pipelines"].values()),
                }
            )
    summary = {
        "assigned": len(records),
        "scorable": sum(r["gold"]["status"] == "ok" for r in records),
        "unscorable": sum(r["gold"]["status"] != "ok" for r in records),
        "invalid_ocr": sum(
            not p["valid"] for r in records for p in r["pipelines"].values()
        ),
        "arms": {},
    }
    for arm in ARMS:
        rows = [r for r in outcomes if r["arm"] == arm]
        sc = [r for r in rows if r["scorable"]]
        accept = sum(not r["refer"] for r in sc)
        wrong = sum(r["wrong"] for r in sc)
        summary["arms"][arm] = {
            "assigned": len(rows),
            "scorable": len(sc),
            "correct": sum(r["correct"] for r in sc),
            "wrong": wrong,
            "refer": sum(r["refer"] for r in sc),
            "unscorable_accept": sum(
                not r["refer"] and not r["scorable"] for r in rows
            ),
            "conditional_error": wrong / accept if accept else None,
            "coverage": accept / len(sc) if sc else None,
            "checks": sum(len(r["checks"]) for r in rows),
            "initial_ocr_calls": sum(r["initial_ocr_calls"] for r in rows),
            "total_pipeline_wall_s": sum(
                r["initial_wall_s"] + r["checker_wall_s"] for r in rows
            ),
            "checker_wall_s": sum(r["checker_wall_s"] for r in rows),
            "assumed_loss": {
                str(p): sum(r["wrong"] + p * r["refer"] for r in sc) / len(sc)
                if sc
                else None
                for p in [0.1, 0.25, 0.5]
            },
        }
    summary["candidate_oracle_correct"] = sum(
        r["gold"]["status"] == "ok"
        and any(
            p["candidate"]["status"] == "ok"
            and p["candidate"]["value"] == r["gold"]["value"]
            for p in r["pipelines"].values()
        )
        for r in records
    )
    summary["checker_new_correct"] = sum(
        r["gold"]["status"] == "ok"
        and not any(
            r["pipelines"][k]["candidate"]["value"] == r["gold"]["value"] for k in "ABC"
        )
        and any(
            r["pipelines"][k]["candidate"]["value"] == r["gold"]["value"] for k in "DE"
        )
        for r in records
    )
    return outcomes, summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stage", choices=["E0", "S1"], required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--development", type=Path)
    p.add_argument("--report", action="store_true")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    private = a.out / "private"
    private.mkdir()
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    split, n = ("train", 20) if a.stage == "E0" else ("test", 50)
    exp = "antsy-receipt-v6"
    rid = exp + "/" + a.out.name
    manifest = {
        "source": sha,
        "stage": a.stage,
        "split": split,
        "ids": list(range(n)),
        "dataset_revision": REV,
        "complete": False,
        "model_calls": 0,
        "utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tesseract": subprocess.check_output(
            ["tesseract", "--version"], text=True
        ).splitlines()[0],
    }
    start = time.monotonic()
    manifest["runtime"] = {
        "python": platform.python_version(),
        **{p: importlib.metadata.version(p) for p in ["pillow", "pyarrow"]},
    }

    def save():
        (a.out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    save()
    if a.report:
        import swarm_report as sr

        sr.report(
            "start",
            exp,
            rid,
            params={"stage": a.stage, "kind": "application-pilot"},
            url=f"https://github.com/dmarzzz/swarm-lab/tree/{sha}/researchers/vishesh/notes/antsy-receipt-v6",
            message=f"{a.stage}: {n} fresh {split} receipts; measured OCR total extraction and two fallible pixel-only checkers. Correct/wrong/refer and latency, zero model calls. Exploratory, not payment safety.",
            strict=True,
        )
    try:
        rows, meta = dataset(split, private)
        assert len(rows) >= n
        manifest["dataset_file"] = meta
        save()
        old = (
            Path(__file__).resolve().parents[2]
            / "antsy-verification-v4/results/measured.jsonl.gz"
        )
        oldhashes = {
            r["image_sha256"]
            for r in [
                json.loads(l) for l in gzip.decompress(old.read_bytes()).splitlines()
            ]
        }
        dev = []
        if a.stage == "S1":
            if not a.development:
                raise ValueError("development required")
            dm = json.loads((a.development / "manifest.json").read_text())
            assert dm["complete"] and dm["invalid_ocr"] == 0
            dev = [
                json.loads(l)
                for l in (a.development / "records.jsonl").read_text().splitlines()
            ]
            oldhashes.update(r["image_sha256"] for r in dev)
        # Fail closed on image overlap before invoking any OCR on this stage.
        hashes = [hashlib.sha256(row["image"]["bytes"]).hexdigest() for row in rows[:n]]
        assert len(set(hashes)) == n and not set(hashes) & oldhashes
        references = [reference(json.loads(row["ground_truth"])) for row in rows[:n]]
        if not any(g["status"] == "ok" for g in references):
            raise ValueError("zero_scorable_references")
        records = []
        with (a.out / "records.jsonl").open("x") as f:
            for i, row in enumerate(rows[:n]):
                r = measure(row, i, split, private)
                records.append(r)
                f.write(json.dumps(r) + "\n")
                f.flush()
                if a.report:
                    sr.report(
                        "progress",
                        exp,
                        rid,
                        step=i + 1,
                        total=n,
                        metrics={"completed": i + 1},
                        strict=True,
                    )
        outcomes, summary = evaluate(records)
        if dev:
            families = {r.get("header_fingerprint") for r in dev} - {None}
            summary["exact_header_fingerprint_overlap"] = sum(
                r.get("header_fingerprint") in families for r in records
            )
        for name, obj in [("outcomes.json", outcomes), ("summary.json", summary)]:
            (a.out / name).write_text(json.dumps(obj, indent=2))
        from render import render

        render(a.out, records, outcomes, summary)
        manifest.update(
            complete=True,
            assigned=n,
            ocr_calls=n * 5,
            invalid_ocr=summary["invalid_ocr"],
            wall_s=time.monotonic() - start,
        )
        save()
        from audit import audit

        (a.out / "audit.json").write_text(json.dumps(audit(a.out), indent=2))
        if a.report:
            for path in a.out.iterdir():
                if path.is_file():
                    sr.upload(rid, path, path.name)
            sr.report(
                "done" if not summary["invalid_ocr"] else "fail",
                exp,
                rid,
                metrics={
                    "assigned": n,
                    "invalid_ocr": summary["invalid_ocr"],
                    "model_calls": 0,
                },
                message="Real checker measurement complete. Inspect exact-field errors, abstentions and post-mortem; completion is not an efficacy claim.",
                strict=True,
            )
        print(json.dumps({"manifest": manifest, "summary": summary}))
    except Exception as e:
        manifest.update(error=type(e).__name__, wall_s=time.monotonic() - start)
        save()
        if a.report:
            sr.upload(rid, a.out / "manifest.json", "manifest.json")
            sr.report(
                "fail",
                exp,
                rid,
                message=type(e).__name__ + "; no automatic outcome retries",
                strict=True,
            )
        raise


if __name__ == "__main__":
    main()
