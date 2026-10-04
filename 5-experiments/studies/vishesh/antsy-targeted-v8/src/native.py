"""Q0 only. Orchestrator admission required; no automatic repair, resume or S1."""

import argparse, datetime, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
from fields import digest, v7
from qualification import summarize

ROOT = Path(__file__).resolve().parents[1]
EXP = "antsy-targeted-v8"
ATTEMPT = "Q0-attempt-1"
RUN = EXP + "/" + ATTEMPT
DOCS = ["PLAN.md", "AMENDMENT-01.md", "reviews/Q0-pre.md", "NATIVE-Q0.md"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def require(x, why):
    if not x:
        raise ValueError(why)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def source(repo):
    require(
        not subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain"]),
        "dirty_source",
    )
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()


def validate(r, revision, runtime_hash, ts=None):
    ts = time.time() if ts is None else ts
    require(r["experiment"] == EXP and r["attempt"] == ATTEMPT, "wrong_attempt")
    require(
        r["source"] == revision and re.fullmatch("[a-f0-9]{40}", revision),
        "wrong_revision",
    )
    require(r["runtime_sha256"] == runtime_hash, "runtime_drift")
    require(
        0 <= ts - r["verified_at"] < 1800 and ts + 1800 < r["claim_expires_at"],
        "stale_admission",
    )
    require(
        r["exclusive_claim_verified"] is True
        and r["approved_team_verified"] is True
        and r["host_idle_verified"] is True,
        "allocation_missing",
    )
    require(
        r["public_page_verified"] is True and r["budget_reconciled"] is True,
        "page_or_budget_missing",
    )
    require(
        r["max_ocr_calls"] == 40
        and r["max_model_calls"] == 0
        and r["new_charge_cap_usd"] == 0,
        "wrong_cap",
    )
    require(
        r["claim"] == "vishesh-antsy-targeted-v8" and bool(r["host"]), "wrong_claim"
    )
    require(r["documents"] == {p: sha(ROOT / p) for p in DOCS}, "plan_drift")
    return True


ENV = dict(
    os.environ,
    OMP_NUM_THREADS="1",
    OMP_THREAD_LIMIT="1",
    OPENBLAS_NUM_THREADS="1",
    MKL_NUM_THREADS="1",
    PYTHONHASHSEED="0",
)


def runtimes(args):
    result = {}
    for w, python in [("P", args.primary_python), ("C", args.checker_python)]:
        proc = subprocess.run(
            [
                str(python),
                str(ROOT / "src/native_worker.py"),
                "--engine",
                w,
                "--models",
                str(args.models),
                "--inspect",
            ],
            capture_output=True,
            text=True,
            env=ENV,
            timeout=90,
        )
        require(proc.returncode == 0, "runtime_inspection_failed_" + w)
        result[w] = json.loads(proc.stdout)
    return result


def prior_hashes():
    sys.path.append(str(ROOT.parent / "antsy-diversity-v7/src"))
    spec = importlib.util.spec_from_file_location(
        "v7_study", ROOT.parent / "antsy-diversity-v7/src/study.py"
    )
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    hashes = s.prior_hashes()
    for p in (ROOT.parent / "antsy-diversity-v7/results").glob("*/records.jsonl"):
        hashes.update(json.loads(x)["image_sha256"] for x in p.read_text().splitlines())
    return s, hashes


def execute(a):
    revision = source(a.repo)
    runtime = runtimes(a)
    receipt = json.loads(a.admission.read_text())
    validate(receipt, revision, digest(runtime))
    for doc in DOCS:
        url = f"https://raw.githubusercontent.com/dmarzzz/swarm-lab/{revision}/researchers/vishesh/notes/{EXP}/{doc}"
        with urllib.request.urlopen(url, timeout=30) as f:
            body = f.read()
        require(
            hashlib.sha256(body).hexdigest() == sha(ROOT / doc), "public_plan_mismatch"
        )
    import swarm_report as sr

    require(
        not any(r["run"] == RUN for r in sr.runs(EXP, limit=5000)), "hub_attempt_exists"
    )
    require(
        a.out.name == ATTEMPT and not a.out.exists(), "attempt_exists_or_wrong_name"
    )
    os.umask(0o077)
    a.out.mkdir(parents=True, exist_ok=False)
    private = a.out / "private"
    private.mkdir()
    manifest = dict(
        experiment=EXP,
        attempt=ATTEMPT,
        source=revision,
        runtime=runtime,
        runtime_sha256=digest(runtime),
        assigned=20,
        max_ocr_calls=40,
        model_calls=0,
        new_charge_usd=0,
        started_utc=now(),
        complete=False,
        qualified=False,
    )
    records = []
    journal = []
    started = time.monotonic()

    def save():
        (a.out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    def event(ident, w, status, **extra):
        e = dict(id=ident, worker=w, status=status, utc=now(), **extra)
        journal.append(e)
        with (a.out / "calls.jsonl").open("a") as f:
            f.write(json.dumps(e) + "\n")
            f.flush()
            os.fsync(f.fileno())

    (a.out / "admission-public.json").write_text(
        json.dumps(
            {
                k: receipt[k]
                for k in [
                    "claim",
                    "host",
                    "source",
                    "runtime_sha256",
                    "verified_at",
                    "claim_expires_at",
                    "max_ocr_calls",
                    "max_model_calls",
                    "new_charge_cap_usd",
                ]
            },
            indent=2,
        )
    )
    save()
    try:
        sr.report(
            "start",
            EXP,
            RUN,
            params={"stage": "Q0", "attempt": ATTEMPT},
            message="Fresh competence qualification: 20 receipts, RapidOCR and EasyOCR, at most 40 OCR calls; zero paid model calls.",
            url=f"https://github.com/dmarzzz/swarm-lab/blob/{revision}/researchers/vishesh/notes/{EXP}/reviews/Q0-pre.md",
            strict=True,
        )
        old, prior = prior_hashes()
        rows, meta = old.load_dataset("train", private, None)
        images = [
            hashlib.sha256(rows[i]["image"]["bytes"]).hexdigest() for i in range(60, 80)
        ]
        require(len(set(images)) == 20 and not set(images) & prior, "image_overlap")
        manifest.update(
            dataset_revision=old.REV, dataset_file=meta, ids=list(range(60, 80))
        )
        save()
        for i in range(60, 80):
            image = private / f"train-{i}.png"
            image.write_bytes(rows[i]["image"]["bytes"])
            r = {"id": i, "split": "train", "image_sha256": sha(image), "workers": {}}
            for w, python in [("P", a.primary_python), ("C", a.checker_python)]:
                require(time.monotonic() - started < 1500, "stage_deadline")
                require(
                    time.time() + 90 < receipt["claim_expires_at"], "claim_expiring"
                )
                require(
                    len([e for e in journal if e["status"] == "started"]) < 40,
                    "call_cap",
                )
                output = private / f"{i}-{w}.json"
                event(i, w, "started")
                begin = time.monotonic()
                entry = {
                    "valid": False,
                    "candidate": {"status": "error", "value": None},
                    "input_sha256": sha(image),
                    "runtime_sha256": digest(runtime[w]),
                }
                try:
                    proc = subprocess.run(
                        [
                            str(python),
                            str(ROOT / "src/native_worker.py"),
                            "--engine",
                            w,
                            "--models",
                            str(a.models),
                            "--image",
                            str(image),
                            "--out",
                            str(output),
                        ],
                        capture_output=True,
                        timeout=45,
                        env=ENV,
                    )
                    (private / f"{i}-{w}.stderr").write_bytes(proc.stderr)
                    require(proc.returncode == 0, "worker_process_error")
                    data = json.loads(output.read_text())
                    c = data["candidate"]
                    require(
                        c["status"] in ["ok", "missing", "ambiguous"],
                        "candidate_invalid",
                    )
                    entry.update(
                        valid=True,
                        candidate=c,
                        observation_sha256=digest(data["raw_words"]),
                    )
                except Exception as e:
                    entry["error"] = type(e).__name__
                entry["wall_s"] = time.monotonic() - begin
                r["workers"][w] = entry
                event(
                    i, w, "valid" if entry["valid"] else "error", wall_s=entry["wall_s"]
                )
                if not entry["valid"]:
                    (a.out / "partial-record.json").write_text(json.dumps(r, indent=2))
                    raise ValueError("worker_failed_no_retry")
            r["gold"] = v7.reference(json.loads(rows[i]["ground_truth"]))
            records.append(r)
            with (a.out / "records.jsonl").open("a") as f:
                f.write(json.dumps(r) + "\n")
                f.flush()
                os.fsync(f.fileno())
            sr.report(
                "progress",
                EXP,
                RUN,
                step=len(records),
                total=20,
                metrics={"completed": len(records), "valid_calls": len(records) * 2},
                strict=True,
            )
        manifest["complete"] = True
    except Exception as e:
        manifest["error"] = type(e).__name__
    summary = summarize(records, journal)
    manifest.update(
        qualified=summary["qualified"],
        wall_s=time.monotonic() - started,
        ocr_started=summary["started"],
        valid=summary["valid"],
        unstarted=summary["unstarted"],
    )
    save()
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2))
    from native_visuals import render

    render(a.out, records, journal)
    for p in sorted(a.out.iterdir()):
        if p.is_file():
            sr.upload(RUN, p, p.name)
    sr.report(
        "done" if summary["qualified"] else "fail",
        EXP,
        RUN,
        metrics={
            "completed": summary["completed"],
            "valid_calls": summary["valid"],
            "qualified": int(summary["qualified"]),
        },
        message="Qualification passed; S1 needs separate admission."
        if summary["qualified"]
        else "Qualification failed or incomplete; stop and diagnose. No automatic repair or S1.",
        strict=True,
    )
    print(json.dumps(summary))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--primary-python", type=Path, required=True)
    p.add_argument("--checker-python", type=Path, required=True)
    p.add_argument("--models", type=Path, required=True)
    p.add_argument("--runtime-out", type=Path)
    p.add_argument("--admission", type=Path)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    if a.runtime_out:
        require(not a.runtime_out.exists(), "runtime_file_exists")
        runtime = runtimes(a)
        a.runtime_out.write_text(json.dumps(runtime, indent=2))
        print(json.dumps({"runtime_sha256": digest(runtime), "native_calls": 0}))
        return
    require(
        a.admission is not None and a.out is not None, "admission_and_output_required"
    )
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with (a.out.parent / "Q0.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        execute(a)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Antsy qualification blocked: " + type(e).__name__)
        raise SystemExit(1)
