"""Strict Q0 accounting and fixed policy diagnostics; no model dependencies."""

from fields import policy

MODES = ["primary", "checker", "targeted-fallback", "always-fallback", "agreement"]


def summarize(records, journal):
    scorable = sum(r["gold"]["status"] == "ok" for r in records)
    arms = {}
    for mode in MODES:
        a = dict(
            correct=0,
            wrong=0,
            refer=0,
            unknown_accepted=0,
            checker_uses=0,
            replayed_worker_seconds=0.0,
        )
        for r in records:
            d = policy(
                r["workers"]["P"]["candidate"], r["workers"]["C"]["candidate"], mode
            )
            v = d["value"]
            g = r["gold"]
            a["checker_uses"] += "C" in d["used"]
            a["replayed_worker_seconds"] += sum(
                r["workers"][x]["wall_s"] for x in d["used"]
            )
            if g["status"] != "ok":
                a["unknown_accepted"] += v is not None
            elif v is None:
                a["refer"] += 1
            elif v == g["value"]:
                a["correct"] += 1
            else:
                a["wrong"] += 1
        arms[mode] = a
    starts = [(e["id"], e["worker"]) for e in journal if e["status"] == "started"]
    terminals = [
        (e["id"], e["worker"]) for e in journal if e["status"] in ["valid", "error"]
    ]
    expected = [(i, w) for i in range(60, 80) for w in ["P", "C"]]
    valid = sum(e["status"] == "valid" for e in journal)
    checks = {
        "all_assigned": [r["id"] for r in records] == list(range(60, 80)),
        "unique_journal": starts == expected and terminals == expected,
        "no_execution_errors": valid == 40
        and all(w["valid"] for r in records for w in r["workers"].values()),
        "reference_coverage": scorable >= 16,
        "primary_competence": scorable > 0
        and arms["primary"]["correct"] >= 0.5 * scorable
        and arms["primary"]["wrong"] <= 1,
        "checker_competence": scorable > 0
        and arms["checker"]["correct"] >= 0.5 * scorable
        and arms["checker"]["wrong"] <= 1,
    }
    both = [r for r in records if r["gold"]["status"] == "ok"]

    def val(r, w):
        c = r["workers"][w]["candidate"]
        return c["value"] if c["status"] == "ok" else None

    paired = {
        "scorable": len(both),
        "same_wrong": sum(
            val(r, "P") is not None and val(r, "P") == val(r, "C") != r["gold"]["value"]
            for r in both
        ),
        "checker_rescue_primary_missing": sum(
            val(r, "P") is None and val(r, "C") == r["gold"]["value"] for r in both
        ),
        "checker_correct_primary_wrong": sum(
            val(r, "P") is not None and val(r, "P") != r["gold"]["value"] == val(r, "C")
            for r in both
        ),
        "shared_missing": sum(
            val(r, "P") is None and val(r, "C") is None for r in both
        ),
    }
    return dict(
        assigned=20,
        completed=len(records),
        scorable=scorable,
        started=len(starts),
        valid=valid,
        unstarted=40 - len(starts),
        qualified=all(checks.values()),
        checks=checks,
        arms=arms,
        paired=paired,
    )
