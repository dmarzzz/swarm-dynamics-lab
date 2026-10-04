"""Prospectively admitted real OCR collection and paired diversity evaluation."""

import argparse, datetime, gzip, hashlib, importlib.metadata, json, os, platform, subprocess, sys, time, urllib.request
from pathlib import Path
from PIL import Image, ImageOps
from core import digest, reference, evaluate, diversity, payload, decide
from admission import preflight

ROOT = Path(__file__).resolve().parents[1]
REV = "7f0115a4b758a71d6473b8d085751692da2fef98"
WORKERS = {
    "T0": ("tesseract", 3, False),
    "T1": ("tesseract", 6, False),
    "T2": ("tesseract", 11, False),
    "R0": ("rapidocr", 6, False),
    "R1": ("rapidocr", 6, True),
}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def fingerprint():
    paths = [
        ROOT / "PLAN.md",
        ROOT / "requirements.txt",
        ROOT / "spec/model-hashes.json",
        ROOT.parent / "antsy-receipt-v6/src/contract.py",
        *sorted((ROOT / "src").glob("*.py")),
    ]
    return digest({str(p.relative_to(ROOT.parent)): sha(p) for p in paths})


def runtime():
    import importlib.util
    import cv2
    from rapidocr import (
        RapidOCR,
    )  # Import-only dependency preflight, no engine constructed.

    pkg = Path(importlib.util.find_spec("rapidocr").origin).parent
    models = {p.name: sha(p) for p in sorted((pkg / "models").glob("*.onnx"))}
    assert models == json.loads((ROOT / "spec/model-hashes.json").read_text()), (
        "model hash drift"
    )
    tessdata = Path("/usr/share/tesseract-ocr/5/tessdata")
    tessmodels = {
        name: sha(tessdata / (name + ".traineddata")) for name in ["eng", "ind"]
    }
    return {
        "system_packages": subprocess.check_output(
            [
                "dpkg-query",
                "-W",
                "-f=${Package}=${Version}\n",
                "libgl1",
                "libglib2.0-0t64",
            ],
            text=True,
        ).splitlines(),
        "tesseract_model_hashes": tessmodels,
        "python": platform.python_version(),
        "packages": {
            p: importlib.metadata.version(p)
            for p in [
                "rapidocr",
                "onnxruntime",
                "pillow",
                "pyarrow",
                "numpy",
                "opencv-python",
            ]
        },
        "model_hashes": models,
        "rapid_config_sha256": sha(pkg / "config.yaml"),
        "tesseract": subprocess.check_output(
            ["tesseract", "--version"], text=True
        ).splitlines()[0],
    }


def load_dataset(split, private, cache):
    import pyarrow.parquet as pq

    if cache:
        # Reuse pinned public dataset bytes from a verified preceding measurement.
        manifest = json.loads((cache.parent.parent / "manifest.json").read_text())
        assert manifest["dataset_revision"] == REV and manifest["split"] == split
        assert sha(cache) == manifest["dataset_file"]["sha256"]
        return pq.read_table(cache).to_pylist(), manifest["dataset_file"]
    with urllib.request.urlopen(
        f"https://huggingface.co/api/datasets/naver-clova-ix/cord-v2/tree/{REV}/data",
        timeout=30,
    ) as f:
        tree = json.load(f)
    name = sorted(
        x["path"]
        for x in tree
        if x["path"].startswith("data/" + split + "-")
        and x["path"].endswith(".parquet")
    )[0]
    dest = private / (split + ".parquet")
    urllib.request.urlretrieve(
        f"https://huggingface.co/datasets/naver-clova-ix/cord-v2/resolve/{REV}/{name}",
        dest,
    )
    return pq.read_table(dest).to_pylist(), {"file": name, "sha256": sha(dest)}


def prior_hashes():
    old = ROOT.parent / "antsy-verification-v4/results/measured.jsonl.gz"
    hs = {
        json.loads(x)["image_sha256"]
        for x in gzip.decompress(old.read_bytes()).splitlines()
    }
    for run in ["E0-reparse-3", "S1-reparse-2"]:
        hs.update(
            json.loads(x)["image_sha256"]
            for x in (ROOT.parent / "antsy-receipt-v6/results" / run / "records.jsonl")
            .read_text()
            .splitlines()
        )
    return hs


def measure(row, ident, split, private, versions):
    raw = row["image"]["bytes"]
    image = private / f"{split}-{ident}.png"
    image.write_bytes(raw)
    image_sha = sha(image)
    with Image.open(image) as im:
        width, height = im.size
    result = {
        "id": ident,
        "split": split,
        "image_sha256": image_sha,
        "pixel_count": width * height,
        "workers": {},
    }
    for name, (family, psm, transform) in WORKERS.items():
        start = time.monotonic()
        path = image
        if transform:
            with Image.open(image) as im:
                im = ImageOps.autocontrast(im.convert("L"))
                im = im.resize((im.width * 2, im.height * 2))
                path = private / f"{split}-{ident}-{name}.png"
                im.save(path)
        config = {
            "family": family,
            "psm": psm if family == "tesseract" else None,
            "transform": "gray-autocontrast-2x" if transform else "original",
            "model_bundle": digest(versions["model_hashes"])
            if family == "rapidocr"
            else digest(versions["tesseract_model_hashes"]),
            "extractor_sha": sha(ROOT / "src/core.py"),
        }
        origin = digest({"config": config, "input_sha256": sha(path)})
        entry = {
            "id": name,
            "family": family,
            "origin": origin,
            "configuration": config,
            "input_sha256": sha(path),
            "evidence_roots": [image_sha],
            "valid": False,
        }
        dest = private / f"{split}-{ident}-{name}.json"
        ledger = private.parent / "calls.jsonl"

        def event(status, **extra):
            with ledger.open("a") as f:
                f.write(
                    json.dumps(
                        {
                            "receipt": ident,
                            "worker": name,
                            "status": status,
                            "utc": datetime.datetime.now(
                                datetime.timezone.utc
                            ).isoformat(),
                            **extra,
                        }
                    )
                    + "\n"
                )
                f.flush()

        event("started")
        try:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "src/worker.py"),
                    "--image",
                    str(path),
                    "--engine",
                    family,
                    "--psm",
                    str(psm),
                    "--out",
                    str(dest),
                ],
                capture_output=True,
                timeout=45,
                check=True,
                env=dict(os.environ, OMP_THREAD_LIMIT="1", OPENBLAS_NUM_THREADS="1"),
            )
            w = json.loads(dest.read_text())
            entry.update(
                candidate=w["candidate"],
                valid=True,
                observation_sha256=digest(w["raw_words"]),
            )
        except Exception as e:
            entry.update(
                candidate={
                    "status": "error",
                    "value": None,
                    "confidence": 0.0,
                    "regions": [],
                },
                error=type(e).__name__,
            )
        event("valid" if entry["valid"] else "error", error=entry.get("error"))
        entry["wall_s"] = time.monotonic() - start
        result["workers"][name] = entry
    result["gold"] = reference(json.loads(row["ground_truth"]))
    return result


def audit(records, outcomes, summary, ids):
    assert [r["id"] for r in records] == ids and len(
        {r["image_sha256"] for r in records}
    ) == len(ids)
    assert len(outcomes) == len(ids) * 11 and len(
        {(o["id"], o["arm"]) for o in outcomes}
    ) == len(outcomes)
    for arm, a in summary["arms"].items():
        rr = [o for o in outcomes if o["arm"] == arm]
        correct = wrong = refer = 0
        for o in rr:
            r = next(r for r in records if r["id"] == o["id"])
            if r["gold"]["status"] != "ok":
                continue
            if o["value"] is None:
                refer += 1
            elif o["value"] == r["gold"]["value"]:
                correct += 1
            else:
                wrong += 1
        assert (a["correct"], a["wrong"], a["refer"]) == (correct, wrong, refer)
    controls = 0
    for r in records:
        xs = payload(r, ["T0", "T1", "R0"])
        expected = decide(xs, "provenance-dissent")
        assert (
            decide(xs + [dict(xs[0], id="duplicate")] * 3, "provenance-dissent")
            == expected
        )
        assert decide(list(reversed(xs)), "provenance-dissent") == expected
        controls += 2
    return {
        "passed": True,
        "assigned": len(ids),
        "policy_outcomes": len(outcomes),
        "invariance_checks": controls,
        "scoring": "separate numeric tally; same-author audit",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stage", choices=["S0", "S0-repair", "S1"], required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--admission", type=Path, required=True)
    p.add_argument("--cache", type=Path)
    p.add_argument("--qualification", type=Path)
    p.add_argument("--report", action="store_true")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    private = a.out / "private"
    private.mkdir()
    exp = "antsy-diversity-v7"
    rid = exp + "/" + a.out.name
    start = time.monotonic()
    split = "test" if a.stage == "S1" else "train"
    ids = (
        list(range(50, 100))
        if a.stage == "S1"
        else list(range(40, 60))
        if a.stage == "S0-repair"
        else list(range(20, 40))
    )
    manifest = {
        "stage": a.stage,
        "split": split,
        "ids": ids,
        "dataset_revision": REV,
        "complete": False,
        "qualified": False,
        "model_calls": 0,
        "assigned": len(ids),
        "utc_start": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    def save():
        (a.out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    save()
    try:
        receipt = preflight(a.admission, a.stage, a.out.name)
        (a.out / "admission-public.json").write_text(json.dumps(receipt, indent=2))
        versions = runtime()
        manifest.update(
            source=receipt["source"], instrument_sha256=fingerprint(), runtime=versions
        )
        save()
        if a.report:
            import swarm_report as sr

            sr.report(
                "start",
                exp,
                rid,
                params={"stage": a.stage},
                message=f"{len(ids)} assigned {split} receipts; five native OCR workers; paired evidence-family and aggregation factors; zero hosted-model calls.",
                strict=True,
            )
        qualification = None
        if a.stage == "S1":
            assert a.qualification is not None
            qualification = json.loads((a.qualification / "manifest.json").read_text())
            assert (
                qualification["qualified"]
                and qualification["instrument_sha256"] == manifest["instrument_sha256"]
                and qualification["runtime"] == versions
            )
        rows, meta = load_dataset(split, private, a.cache)
        manifest["dataset_file"] = meta
        save()
        assert max(ids) < len(rows)
        hs = [hashlib.sha256(rows[i]["image"]["bytes"]).hexdigest() for i in ids]
        prior = prior_hashes()
        if a.qualification:
            prior.update(
                json.loads(x)["image_sha256"]
                for x in (a.qualification / "records.jsonl").read_text().splitlines()
            )
        assert len(set(hs)) == len(ids) and not set(hs) & prior, "image overlap"
        records = []
        with (a.out / "records.jsonl").open("x") as f:
            for step, i in enumerate(ids, 1):
                assert time.monotonic() - start < 1500, (
                    "stage time budget exhausted before next receipt"
                )
                r = measure(rows[i], i, split, private, versions)
                records.append(r)
                f.write(json.dumps(r) + "\n")
                f.flush()
                assert all(w["valid"] for w in r["workers"].values()), (
                    "worker failure: stop before next receipt"
                )
                if a.report:
                    sr.report(
                        "progress",
                        exp,
                        rid,
                        step=step,
                        total=len(ids),
                        metrics={"completed": step},
                        strict=True,
                    )
        outcomes, summary = evaluate(records)
        d = diversity(records)
        audit_result = audit(records, outcomes, summary, ids)
        sizes = sorted(r["pixel_count"] for r in records)
        thresholds = (
            qualification["size_thresholds"]
            if qualification
            else [sizes[len(sizes) // 3], sizes[2 * len(sizes) // 3]]
        )
        d["size_strata"] = {
            str(i): diversity(
                [
                    r
                    for r in records
                    if sum(r["pixel_count"] > x for x in thresholds) == i
                ]
            )
            for i in range(3)
        }
        d["declared_pair_differences"] = {}
        for j, aa in enumerate(WORKERS):
            for bb in list(WORKERS)[j + 1 :]:
                ca = records[0]["workers"][aa]["configuration"]
                cb = records[0]["workers"][bb]["configuration"]
                d["declared_pair_differences"][aa + "--" + bb] = [
                    k for k in ca if ca[k] != cb[k]
                ]
        d["shared_pixel_source_jaccard"] = 1.0
        d["interpretation"] = (
            "Same receipt pixels and shared extractor; different engines are not proven independent."
        )
        checks = {
            "complete": len(records) == len(ids),
            "no_execution_errors": summary["invalid"] == 0,
            "reference_coverage": summary["scorable"] >= 16
            if a.stage != "S1"
            else summary["scorable"] > 0,
            "best_worker_competence": max(x["correct"] for x in d["workers"].values())
            >= 0.5 * summary["scorable"],
            "both_families_useful": max(
                d["workers"][k]["correct"] for k in ["T0", "T1", "T2"]
            )
            >= 2
            and max(d["workers"][k]["correct"] for k in ["R0", "R1"]) >= 2,
        }
        manifest.update(
            complete=True,
            qualified=all(checks.values()) if a.stage != "S1" else False,
            checks=checks,
            ocr_calls=len(ids) * 5,
            invalid=summary["invalid"],
            size_thresholds=thresholds,
            wall_s=time.monotonic() - start,
        )
        for name, value in [
            ("outcomes.json", outcomes),
            ("summary.json", summary),
            ("diversity.json", d),
            ("audit.json", audit_result),
        ]:
            (a.out / name).write_text(json.dumps(value, indent=2))
        from visuals import render

        render(a.out, records, outcomes, summary, d)
        save()
        if a.report:
            for file in a.out.iterdir():
                if file.is_file():
                    sr.upload(rid, file, file.name)
            passed = (
                manifest["qualified"] if a.stage != "S1" else summary["invalid"] == 0
            )
            sr.report(
                "done" if passed else "fail",
                exp,
                rid,
                metrics={
                    "assigned": len(ids),
                    "scorable": summary["scorable"],
                    "invalid": summary["invalid"],
                },
                message="Native qualification passed"
                if manifest["qualified"]
                else "Comparison complete; examine wrong acceptance, coverage and diversity separately."
                if passed
                else "Qualification failed; no escalation. Preserve and diagnose.",
                strict=True,
            )
        print(
            json.dumps(
                {
                    "complete": True,
                    "qualified": manifest["qualified"],
                    "checks": checks,
                    "summary": summary,
                }
            )
        )
    except BaseException as e:
        manifest.update(error=type(e).__name__, wall_s=time.monotonic() - start)
        save()
        if a.report:
            import swarm_report as sr

            sr.report(
                "fail",
                exp,
                rid,
                message=type(e).__name__ + "; preserved attempt, no hidden retries",
                strict=True,
            )
        raise


if __name__ == "__main__":
    main()
