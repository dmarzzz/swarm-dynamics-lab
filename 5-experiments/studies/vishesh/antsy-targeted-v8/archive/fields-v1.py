"""Localized total-field extraction; no labels, case IDs or evaluator inputs."""

import hashlib, importlib.util, json, re
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "antsy-diversity-v7/src/core.py"
spec = importlib.util.spec_from_file_location("v7_core", p)
v7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v7)
ANCHOR = v7.ANCHOR
EXCLUDE = re.compile(
    v7.EXCLUDE.pattern + r"|\b(?:void|cancelled|canceled|discount)\b", re.I
)
# Spaces following a decimal/grouping mark are normalized, never arbitrary digit gaps.
NUM = re.compile(r"(?<![\w.,-])\d+(?:[.,]\s*\d+)*(?![\w.,])")
PREFIX = re.compile(r"^[\s:.*©»|]*(?:(?:Rp\.?|IDR)\s*)?$", re.I)


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


def rows(words):
    """Anchor-centered baseline, not a cluster tied to the first tiny word."""
    seen = set()
    for anchor in words:
        if not ANCHOR.search(anchor["text"]):
            continue
        row = sorted(
            [
                w
                for w in words
                if abs(w["y"] - anchor["y"]) <= 0.45 * max(w["h"], anchor["h"])
            ],
            key=lambda w: w["x"],
        )
        key = tuple(tuple(w["box"]) for w in row)
        if key in seen:
            continue
        seen.add(key)
        yield row


def extract(words):
    found = []
    reasons = []
    for row in rows(words):
        text = " ".join(w["text"] for w in row)
        anchor = ANCHOR.search(text)
        if not anchor:
            continue
        if EXCLUDE.search(text):
            reasons.append("excluded_context")
            continue
        tail = text[anchor.end() :]
        nums = list(NUM.finditer(tail))
        if len(nums) != 1:
            reasons.append("missing_or_multiple_amounts")
            continue
        n = nums[0]
        if not PREFIX.fullmatch(tail[: n.start()]):
            reasons.append("unrecognized_label_value_gap")
            continue
        raw = re.sub(r"([.,])\s+", r"\1", n.group())
        value = v7.amount(raw)
        if value is None:
            reasons.append("invalid_amount_grammar")
            continue
        # Keep only spans that actually contain a recognized label and one numeric field.
        found.append(
            {
                "value": value,
                "region_hash": digest([w["box"] for w in row]),
                "observation_hash": digest(row),
            }
        )
    values = {f["value"] for f in found}
    status = "ok" if len(values) == 1 else "ambiguous" if values else "missing"
    return {
        "status": status,
        "value": next(iter(values)) if status == "ok" else None,
        "evidence": found,
        "reasons": sorted(set(reasons)),
        "contract": "anchor-row-v1",
    }


def policy(primary, checker, mode):
    """A fallback is one-source acceptance, never reported as corroboration."""
    p = primary["value"] if primary["status"] == "ok" else None
    c = checker["value"] if checker["status"] == "ok" else None
    if mode == "primary":
        value = p
        used = ["P"]
    elif mode == "checker":
        value = c
        used = ["C"]
    elif mode == "targeted-fallback":
        value = p if p is not None else c
        used = ["P"] if p is not None else ["P", "C"]
    elif mode == "always-fallback":
        value = p if p is not None else c
        used = ["P", "C"]
    elif mode == "agreement":
        value = p if p is not None and p == c else None
        used = ["P", "C"]
    else:
        raise ValueError("unknown policy")
    return {
        "value": value,
        "action": "accept" if value is not None else "refer",
        "used": used,
        "corroborated": mode == "agreement" and value is not None,
    }
