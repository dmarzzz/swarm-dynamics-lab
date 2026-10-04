"""Admission checks before any native engine is initialized or called."""

import datetime, hashlib, json, subprocess, urllib.request
from pathlib import Path

UTC = datetime.timezone.utc


def stamp(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def validate(receipt, stage, run, source, plan_hash, now=None):
    now = now or datetime.datetime.now(UTC)
    assert (
        receipt["experiment"] == "antsy-diversity-v7"
        and receipt["run"] == run
        and receipt["stage"] == stage
    )
    assert receipt["source"] == source and receipt["plan_sha256"] == plan_hash
    assert (
        stamp(receipt["expires_utc"]) > now
        and stamp(receipt["claim_expires_utc"]) > now
    )
    assert (
        datetime.timedelta(0)
        <= now - stamp(receipt["verified_utc"])
        < datetime.timedelta(minutes=30)
    )
    assert (
        receipt["public_page_verified"] is True
        and receipt["exclusive_claim_verified"] is True
    )
    assert (
        receipt["host"] == "sim-vishesh"
        and receipt["claim"] == "vishesh-antsy-diversity-v7"
    )
    assert receipt["max_model_calls"] == 0 and receipt["new_charge_cap_usd"] == 0
    assert receipt["max_ocr_calls"] == (250 if stage == "S1" else 100)
    expected = f"https://raw.githubusercontent.com/dmarzzz/swarm-lab/{source}/researchers/vishesh/notes/antsy-diversity-v7/PLAN.md"
    assert receipt["public_content_url"] == expected
    return True


def preflight(path, stage, run):
    source = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    subprocess.run(["git", "diff", "--quiet"], check=True)
    root = Path(__file__).resolve().parents[1]
    plan_hash = hashlib.sha256((root / "PLAN.md").read_bytes()).hexdigest()
    r = json.loads(path.read_text())
    validate(r, stage, run, source, plan_hash)
    with urllib.request.urlopen(r["public_content_url"], timeout=30) as response:
        public = response.read()
    assert hashlib.sha256(public).hexdigest() == plan_hash, (
        "public plan content mismatch"
    )
    return {
        "source": source,
        "plan_sha256": plan_hash,
        "public_content_verified": True,
        "verified_utc": datetime.datetime.now(UTC).isoformat(),
        "claim": r["claim"],
        "host": r["host"],
        "claim_expires_utc": r["claim_expires_utc"],
    }
