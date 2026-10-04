#!/usr/bin/env python3
"""Unified daily incident timeline across three public in-the-wild agent-swarm datasets.

Inputs (never committed; pass --data pointing at a directory that holds them):
  <data>/transluce/urlquery-agent-activity-2026-09-22-v5/{daily-counts.csv,daily-source-counts.csv,methods.json,report-sources.csv}
  <data>/collusion-wiki/{revisions,events,pages}.jsonl.gz, shortener-logs.json.gz, other-wikis.json.gz
  <data>/swarmtraces/redacted.jsonl.gz

Outputs (derived aggregates only, committed):
  daily.csv            one row per UTC day, one column per series
  shared_sources.csv   Transluce source buckets that also leave traces in the wiki dump
  summary.json         headline numbers used in FINDING.md
  timeline.png/.svg    figure 1, the stacked daily timeline
  shared.png/.svg      figure 2, per-source daily series for the shared sources

Descriptive only. No model calls. Counts are counts of records in each publisher's selection,
not counts of agents or of successful actions.
"""
import argparse, collections, csv, gzip, json, math, os, re
from urllib.parse import urlsplit
from datetime import date, datetime, timedelta

HOST_RE = re.compile(r"https?://([^/\s\"'<>\]\)|]+)", re.I)

# Hand-entered overlays. Every row cites the library entry or dataset file it was read from.
OVERLAYS = [
    # (date, label, kind, source)
    ("2026-03-06", "First Transluce tunnelling day (Thai ONCB, 29 reports)", "data", "transluce daily-source-counts.csv"),
    ("2026-05-11", "Wiki swarm start per collusion.wiki report; first other-wiki sandbox edit in dump", "report", "[[collusion-wiki-2026-discovery]], other-wikis.json.gz"),
    ("2026-05-24", "First held revision in the collusion.wiki dump (first successful write per report)", "data", "collusion-wiki manifest.json.gz, [[collusion-wiki-2026-discovery]]"),
    ("2026-06-22", "Wiki swarm end per collusion.wiki report (burst again 07-01, 07-02)", "report", "[[collusion-wiki-2026-discovery]]"),
    ("2026-07-08", "First message on the package-cache board (METR scope 07-07 to 07-13)", "report", "[[metr-2026-brief]]"),
    ("2026-07-13", "Last logged attacker event at Hugging Face", "report", "[[huggingface-2026-security]]"),
    ("2026-07-16", "Hugging Face security disclosure", "report", "[[huggingface-2026-security]]"),
    ("2026-08-26", "OpenAI technical report and METR investigation published", "publication", "[[openai-2026-hugging]], [[metr-2026-brief]]"),
    ("2026-09-04", "collusion.wiki report published", "publication", "[[collusion-wiki-2026-discovery]]"),
    ("2026-09-05", "OpenAI statement on the wiki incident", "publication", "[[x-openai-2096133504417616165]]"),
    ("2026-09-08", "arXiv 2609.09150 submitted (copying on the wiki)", "publication", "[[de-marzo-2026-copying]], https://arxiv.org/abs/2609.09150 (submission date checked)"),
    ("2026-09-22", "Transluce urlquery dataset v5 / agent-activity post", "publication", "[[transluce-2026-early]], dataset README"),
    ("2026-09-25", "SwarmTraces report", "publication", "[[swarmtraces-2026-revealing]], [[x-jeffladish-2103584701357437133]]"),
    ("2026-10-01", "Transluce: agents vs government sites", "publication", "[[x-transluceai-2105725928357937410]]"),
]
WINDOWS = [
    ("2026-05-11", "2026-06-22", "wiki swarm (per report)"),
    ("2026-07-08", "2026-07-13", "HF board + attack (METR window)"),
]


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)


def load_transluce(root):
    d = os.path.join(root, "transluce", "urlquery-agent-activity-2026-09-22-v5")
    daily = {}
    for r in csv.DictReader(open(os.path.join(d, "daily-counts.csv"))):
        daily[r["date_utc"]] = {k: int(r[k]) for k in ("significant", "suggestive", "total")}
    src_daily = collections.defaultdict(collections.Counter)
    for r in csv.DictReader(open(os.path.join(d, "daily-source-counts.csv"))):
        src_daily[r["data_source"]][r["date_utc"]] += int(r["reports"])
    methods = json.load(open(os.path.join(d, "methods.json")))
    markers = collections.defaultdict(set)
    for m in methods:
        if m.get("markers") and m.get("label"):
            for mk in m["markers"]:
                markers[m["label"]].add(mk.lower())
    # normalise method labels to the display buckets used in daily-source-counts
    alias = {
        "IHME health data": "IHME", "IHME proxy references": "IHME",
        "Mapillary API": "Mapillary", "Mapillary API proxy references": "Mapillary",
        "Drivelah research": "Drivelah", "Drivelah proxy references": "Drivelah",
        "GBBC Canada 2024": "GBBC", "SND Airtable view": "SND Airtable", "SND Airtable share": "SND Airtable",
        "SND Airtable base": "SND Airtable", "SEC county statistics": "SEC county data",
        "UNM Valmora archive": "UNM digital library", "UNM proxy references": "UNM digital library",
        "IEA charts": "IEA", "IEA statistical pages and tools": "IEA", "School history": "Woodlands House School",
        "Woodlands House School history": "Woodlands House School", "MAX exact PDF Q2": "MAX budget documents",
        "MAX exact PDF Q3": "MAX budget documents", "Thai NSO proxy references": "Thai NSO",
        "Thrill proxy references": "Thrill Data", "UNCTAD proxy references": "UNCTAD",
        "AIHW proxy references": "AIHW", "DataUSA proxy references": "DataUSA",
        "Maryland school-query proxy references": "Maryland school report cards",
        "Data for India chart assets": "Data for India", "NZ vegetation API": "NZ vegetation API",
        "NYSED enrollment institution": "NYSED", "Yahoo CYBR archived history": "Yahoo CYBR",
    }
    bucket_markers = collections.defaultdict(set)
    for lab, mks in markers.items():
        bucket_markers[alias.get(lab, lab)] |= mks
    # Normalize path-bearing markers to hosts; PDF filenames and bare ids are not domains.
    host_markers = {b: {m.split("/")[0] for m in mks if "." in m and not m.split("/")[0].endswith(".pdf")}
                    for b, mks in bucket_markers.items()}
    host_markers = {b: m for b, m in host_markers.items() if m}
    return daily, src_daily, host_markers


def load_wiki(root):
    d = os.path.join(root, "collusion-wiki")
    revs = [json.loads(l) for l in gzip.open(os.path.join(d, "revisions.jsonl.gz"), "rt")]
    events = [json.loads(l) for l in gzip.open(os.path.join(d, "events.jsonl.gz"), "rt")]
    pages = [json.loads(l) for l in gzip.open(os.path.join(d, "pages.jsonl.gz"), "rt")]
    sh = json.load(gzip.open(os.path.join(d, "shortener-logs.json.gz"), "rt"))
    ow = json.load(gzip.open(os.path.join(d, "other-wikis.json.gz"), "rt"))
    series = collections.defaultdict(collections.Counter)
    for e in events:
        series["wiki_" + e["event_type"]][e["time"][:10]] += 1
    for s in sh["sites"]:
        for l in s["links"]:
            if l.get("time"):
                series["wiki_shortener"][l["time"][:10]] += 1
    for p in ow["pages"]:
        for r in p["revisions"]:
            series["wiki_other_sandbox"][r["time"][:10]] += 1
    return revs, pages, series, events


def load_swarmtraces(root):
    kinds = collections.Counter(); dated = 0; n = 0
    for l in gzip.open(os.path.join(root, "swarmtraces", "redacted.jsonl.gz"), "rt"):
        r = json.loads(l); n += 1
        kinds[r["kind"]] += 1
        if r.get("time_utc"):
            dated += 1
    return n, dated, kinds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--no-fig", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    t_daily, t_src, host_markers = load_transluce(a.data)
    # Only buckets actually represented in daily-source-counts enter the overlap census.
    host_markers = {b: m for b, m in host_markers.items() if b in t_src}
    revs, pages, w_series, events = load_wiki(a.data)
    st_n, st_dated, st_kinds = load_swarmtraces(a.data)

    # ---- daily table -------------------------------------------------------
    all_days = set(t_daily) | {d for s in w_series.values() for d in s}
    d0 = min(date.fromisoformat(x) for x in all_days)
    d1 = max(date.fromisoformat(x) for x in all_days)
    cols = ["transluce_total", "transluce_significant", "transluce_suggestive",
            "wiki_save", "wiki_delete", "wiki_probe", "wiki_revert", "wiki_shortener", "wiki_other_sandbox"]
    rows = []
    for d in daterange(d0, d1):
        k = d.isoformat()
        t = t_daily.get(k, {"total": 0, "significant": 0, "suggestive": 0})
        row = {"date_utc": k, "transluce_total": t["total"], "transluce_significant": t["significant"],
               "transluce_suggestive": t["suggestive"]}
        for c in cols[3:]:
            row[c] = w_series[c].get(k, 0)
        rows.append(row)
    with open(os.path.join(a.out, "daily.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date_utc"] + cols); w.writeheader(); w.writerows(rows)

    # ---- shared sources ----------------------------------------------------
    # wiki side: revisions whose body links a host containing a Transluce marker; pages whose family prefix matches
    fam_alias = {"datausa": "DataUSA", "ihme": "IHME", "aihw": "AIHW", "oecd": "OECD", "unaids": "UNAIDS"}
    wiki_rev_by_bucket = collections.defaultdict(collections.Counter)
    wiki_pages_by_bucket = collections.Counter()
    rev_hit_any = 0
    for r in revs:
        hosts = {urlsplit("https://" + h.rstrip(".,;")).hostname for h in HOST_RE.findall(r.get("body") or "")}
        hosts.discard(None)
        hit = False
        for b, mks in host_markers.items():
            if any(h == m or h.endswith("." + m) for h in hosts for m in mks):
                wiki_rev_by_bucket[b][r["time"][:10]] += 1; hit = True
        rev_hit_any += hit
    for p in pages:
        pref = p["page_family"].split("-")[0]
        if pref in fam_alias:
            wiki_pages_by_bucket[fam_alias[pref]] += 1
    shared = []
    for b in sorted(t_src, key=lambda x: -sum(t_src[x].values())):
        tr = t_src[b]; wr = wiki_rev_by_bucket.get(b, collections.Counter())
        if not wr and not wiki_pages_by_bucket.get(b):
            continue
        t_days = {d for d in tr if "2026-05-11" <= d <= "2026-07-02"}
        w_days = set(wr)
        jac = len(t_days & w_days) / len(t_days | w_days) if (t_days | w_days) else float("nan")
        shared.append({
            "source": b,
            "transluce_reports": sum(tr.values()),
            "transluce_first": min(tr), "transluce_last": max(tr),
            "transluce_peak_day": min(tr, key=lambda d: (-tr[d], d)), "transluce_peak_n": tr.most_common(1)[0][1],
            "wiki_revisions_linking": sum(wr.values()),
            "wiki_pages_in_family": wiki_pages_by_bucket.get(b, 0),
            "wiki_first": min(wr) if wr else "", "wiki_last": max(wr) if wr else "",
            "wiki_peak_day": min(wr, key=lambda d: (-wr[d], d)) if wr else "",
            "wiki_peak_n": wr.most_common(1)[0][1] if wr else 0,
            "peak_lag_days": ((date.fromisoformat(min(wr, key=lambda d: (-wr[d], d))) - date.fromisoformat(min(tr, key=lambda d: (-tr[d], d)))).days if wr else ""),
            "active_day_jaccard_wiki_window": round(jac, 3) if jac == jac else "",
        })
    # wiki-only families with no Transluce bucket (for the table footer)
    wiki_only = {fam_alias[k]: v for k, v in collections.Counter(p["page_family"].split("-")[0] for p in pages).items()
                 if k in fam_alias and fam_alias[k] not in t_src}
    with open(os.path.join(a.out, "shared_sources.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(shared[0].keys())); w.writeheader(); w.writerows(shared)

    # ---- exact cross-reference: wiki revisions that link a urlquery report ------
    uq = [(r["time"], r.get("label") or "<anon>", m) for r in revs for m in re.findall(r"urlquery\.net/report/([0-9a-f-]{36})", r.get("body") or "")]
    uq_ids = sorted({m for _, _, m in uq})
    rs = {}
    for r in csv.DictReader(open(os.path.join(a.data, "transluce", "urlquery-agent-activity-2026-09-22-v5", "report-sources.csv"))):
        if r["report_id"] in uq_ids:
            rs[r["report_id"]] = (r["report_date_utc"], r["data_source"])

    # ---- co-movement inside the wiki window (descriptive, post-hoc) -----------
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r

    def spearman(x, y):
        rx, ry = rank(x), rank(y); n = len(x)
        mx, my = sum(rx) / n, sum(ry) / n
        num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
        den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
        return num / den if den else float("nan")

    win = [r for r in rows if "2026-05-24" <= r["date_utc"] <= "2026-06-22"]
    tx = [r["transluce_total"] for r in win]; wy = [r["wiki_save"] for r in win]
    rho = spearman(tx, wy)
    # last day with any Transluce report before the long gap, and last wiki save day in the main run
    t_days_nonzero = sorted(k for k, v in t_daily.items() if v["total"])
    t_last_before_gap = max(d for d in t_days_nonzero if d < "2026-07-01")
    w_last_main = max(d for d, n in w_series["wiki_save"].items() if n and d < "2026-07-01")
    comove = {"window": "2026-05-24..2026-06-22", "days": len(win), "days_both_nonzero": sum(1 for a, b in zip(tx, wy) if a and b),
              "spearman_rho_daily_transluce_total_vs_wiki_save": round(rho, 3),
              "transluce_last_nonzero_day_before_july": t_last_before_gap, "wiki_last_save_day_before_july": w_last_main,
              "transluce_reports_2026-06-22_to_07-13": sum(v["total"] for k, v in t_daily.items() if "2026-06-22" <= k <= "2026-07-13"),
              "transluce_reports_in_HF_window_07-08_to_07-13": sum(v["total"] for k, v in t_daily.items() if "2026-07-08" <= k <= "2026-07-13")}

    # ---- summary -----------------------------------------------------------
    t_total = sum(v["total"] for v in t_daily.values())
    t_in_wiki_window = sum(v["total"] for k, v in t_daily.items() if "2026-05-11" <= k <= "2026-06-22")
    t_before_wiki = sum(v["total"] for k, v in t_daily.items() if k < "2026-05-11")
    t_after_july = sum(v["total"] for k, v in t_daily.items() if k >= "2026-07-14")
    shared_buckets = {s["source"] for s in shared}
    t_in_shared = sum(sum(t_src[b].values()) for b in shared_buckets)
    t_src_total = sum(sum(c.values()) for c in t_src.values())
    saves = w_series["wiki_save"]; dels = w_series["wiki_delete"]
    summary = {
        "transluce": {"included_reports_in_chart": t_total, "days": len(t_daily),
                      "first_nonzero_day": min(k for k, v in t_daily.items() if v["total"]),
                      "last_nonzero_day": max(k for k, v in t_daily.items() if v["total"]),
                      "peak_day": max(t_daily, key=lambda k: t_daily[k]["total"]),
                      "peak_n": max(v["total"] for v in t_daily.values()),
                      "in_wiki_window_2026-05-11_to_06-22": t_in_wiki_window,
                      "before_2026-05-11": t_before_wiki, "on_or_after_2026-07-14": t_after_july,
                      "source_buckets": len(t_src), "source_buckets_with_wiki_trace": len(shared_buckets),
                      "reports_in_shared_buckets": t_in_shared, "reports_with_source_row": t_src_total,
                      "share_in_shared_buckets": round(t_in_shared / t_src_total, 4)},
        "wiki": {"held_revisions": len(revs), "first": min(saves), "last": max(saves),
                 "peak_day": saves.most_common(1)[0][0], "peak_n": saves.most_common(1)[0][1],
                 "admin_deletions": sum(dels.values()), "deletions_first": min(dels), "deletions_last": max(dels),
                 "probes": sum(w_series["wiki_probe"].values()), "shortener_links": sum(w_series["wiki_shortener"].values()),
                 "other_sandbox_revisions": sum(w_series["wiki_other_sandbox"].values()),
                 "other_sandbox_first": min(w_series["wiki_other_sandbox"]),
                 "revisions_linking_transluce_tracked_host": rev_hit_any,
                 "share_linking": round(rev_hit_any / len(revs), 4),
                 "page_families_no_transluce_bucket": wiki_only,
                 "urlquery_report_links": [{"wiki_reference_count": sum(m == i for _, _, m in uq),
                                            "transluce_report_time": rs.get(i, ("", ""))[0],
                                            "transluce_source": rs.get(i, ("", ""))[1]} for i in uq_ids]},
        "swarmtraces": {"records": st_n, "records_with_time_utc": st_dated, "by_kind": dict(st_kinds)},
        "comovement": comove,
        "overlays": [dict(zip(("date", "label", "kind", "source"), o)) for o in OVERLAYS],
        "windows": [dict(zip(("start", "end", "label"), w)) for w in WINDOWS],
    }
    json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1)[:4000])
    if a.no_fig:
        return

    # ---- figures -----------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams.update({"font.family": "monospace", "font.size": 8, "axes.edgecolor": "#888", "axes.labelcolor": "#ddd",
                         "xtick.color": "#ccc", "ytick.color": "#ccc", "text.color": "#eee", "figure.facecolor": "#111",
                         "axes.facecolor": "#161616", "grid.color": "#2a2a2a", "legend.facecolor": "#1b1b1b", "legend.edgecolor": "#333"})
    xs = [date.fromisoformat(r["date_utc"]) for r in rows]
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(13, 9.5), gridspec_kw={"height_ratios": [3, 3, 1.4, 1.55], "hspace": 0.08})
    ax2.sharex(ax1); ax3.sharex(ax1)
    ax1.tick_params(labelbottom=False); ax2.tick_params(labelbottom=False)
    C = {"sig": "#ff7b54", "sug": "#ffd166", "save": "#4cc9f0", "del": "#f72585", "probe": "#b5e48c", "short": "#c77dff", "other": "#80ed99"}
    ax1.bar(xs, [r["transluce_suggestive"] for r in rows], color=C["sug"], width=1, label="Transluce urlquery reports, suggestive")
    ax1.bar(xs, [r["transluce_significant"] for r in rows], bottom=[r["transluce_suggestive"] for r in rows], color=C["sig"], width=1, label="Transluce urlquery reports, significant")
    ax1.set_yscale("symlog", linthresh=10); ax1.set_ylabel("reports / day"); ax1.grid(True, axis="y", lw=0.4)
    ax1.legend(loc="upper left", fontsize=7, frameon=True)
    ax1.set_title("Incident timeline (UTC): Transluce and wiki daily counts; SwarmTraces undated inset. Records, not agents.", fontsize=9, loc="left")
    for k, col, lab in [("wiki_save", C["save"], "collusion.wiki saves (held revisions)"), ("wiki_delete", C["del"], "admin deletions (dse)"),
                        ("wiki_probe", C["probe"], "script probes"), ("wiki_shortener", C["short"], "rmn.re shortener links"),
                        ("wiki_other_sandbox", C["other"], "sandbox edits on 3 other wikis")]:
        ys = [r[k] for r in rows]
        ax2.plot(xs, ys, color=col, lw=1.1, label=lab, drawstyle="steps-mid")
    ax2.set_yscale("symlog", linthresh=10); ax2.set_ylabel("events / day"); ax2.grid(True, axis="y", lw=0.4)
    ax2.legend(loc="upper left", fontsize=7, ncol=2)
    for ax in (ax1, ax2, ax3):
        for s, e, lab in WINDOWS:
            ax.axvspan(date.fromisoformat(s), date.fromisoformat(e) + timedelta(days=1), color="#ffffff", alpha=0.06, lw=0)
    # overlay strip
    ax3.set_ylim(0, 1); ax3.set_yticks([]); ax3.set_ylabel("key events")
    kinds_y = {"data": 0.22, "report": 0.5, "publication": 0.78}
    kc = {"data": "#9aa", "report": "#4cc9f0", "publication": "#ffd166"}
    for i, (d, lab, kind, src) in enumerate(OVERLAYS):
        x = date.fromisoformat(d); y = kinds_y[kind]
        # stagger numbers so same-row neighbours within ~10 days do not sit on top of each other
        prev_same = [j for j, o in enumerate(OVERLAYS[:i]) if o[2] == kind and abs((x - date.fromisoformat(o[0])).days) <= 20]
        off = [3, 17, -12, 31][len(prev_same) % 4]
        ax3.plot([x], [y], marker="o", ms=3.5, color=kc[kind])
        ax3.annotate(str(i + 1), (x, y), xytext=(4, off), textcoords="offset points", fontsize=6.5, color=kc[kind], fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color=kc[kind], lw=0.4, alpha=0.6) if prev_same else None)
    for s, e, lab in WINDOWS:
        ax3.annotate(lab, (date.fromisoformat(s), 0.03), fontsize=6, color="#ccc", xytext=(2, 2), textcoords="offset points")
    for kind, yy in kinds_y.items():
        ax3.text(date(2025, 11, 3), yy, kind, fontsize=6, color=kc[kind], va="center")
    # numbered key for the overlay strip, two columns
    ax4.axis("off")
    half = math.ceil(len(OVERLAYS) / 2)
    for col, chunk in enumerate((OVERLAYS[:half], OVERLAYS[half:])):
        lines = [f"{col * half + j + 1:>2}. {d}  {lab}" for j, (d, lab, kind, src) in enumerate(chunk)]
        ax4.text(0.0 if col == 0 else 0.5, 0.98, "\n".join(lines), transform=ax4.transAxes, fontsize=6.3, va="top", ha="left", color="#ddd", linespacing=1.45)
    ax4.text(0.0, 0.02, "Overlay dates are hand-entered from the cited library entries (see summary.json 'overlays' for the source of each row). Grey bands: windows named by the publishers, not by this analysis.", transform=ax4.transAxes, fontsize=6, color="#999", va="bottom")
    ax3.xaxis.set_major_locator(mdates.MonthLocator()); ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax3.set_xlim(date(2025, 11, 1), date(2026, 10, 10))
    # SwarmTraces inset (undated)
    # placed over the empty right third of the top panel (after 2026-07-14 the Transluce series is near zero)
    ins = ax1.inset_axes([0.765, 0.40, 0.225, 0.42])
    ks = ["payload", "recovered_text", "response"]
    ins.barh(range(len(ks)), [st_kinds[k] for k in ks], color=["#f72585", "#c77dff", "#4cc9f0"])
    ins.set_yticks(range(len(ks))); ins.set_yticklabels(ks)
    for i, k in enumerate(ks):
        ins.text(st_kinds[k], i, f" {st_kinds[k]:,}", va="center", fontsize=6.5)
    ins.set_title(f"SwarmTraces records by kind\n(n={st_n:,}; {st_dated} carry time_utc, so undated)", fontsize=6.3, loc="left")
    ins.set_facecolor("#161616")
    ins.set_xticks([]); ins.tick_params(axis="y", labelsize=6.5); ins.set_xlim(0, max(st_kinds.values()) * 1.35)
    for sp in ins.spines.values(): sp.set_visible(False)
    fig.text(0.01, 0.003, "Sources: Transluce urlquery-agent-activity v5 daily-counts.csv; collusion.wiki dump (events, shortener-logs, other-wikis); SwarmTraces redacted.jsonl.gz. "
             "Overlays hand-entered from the cited library entries. shadow/sol-timeline, swarm-lab, 2026-10-04.", fontsize=6, color="#888")
    fig.savefig(os.path.join(a.out, "timeline.png"), dpi=160, bbox_inches="tight")
    fig.savefig(os.path.join(a.out, "timeline.svg"), bbox_inches="tight")

    # figure 2: shared sources
    sh = [s for s in shared if s["wiki_revisions_linking"] > 0]
    n = len(sh); ncol = 2; nrow = math.ceil(n / ncol)
    fig2, axes = plt.subplots(nrow, ncol, figsize=(13, 2.5 * nrow), sharex=True, squeeze=False)
    lo_d, hi_d = date(2026, 5, 1), date(2026, 7, 5)
    span = list(daterange(lo_d, hi_d))
    for ax, s in zip(axes.flat, sh):
        b = s["source"]
        tr = [t_src[b].get(d.isoformat(), 0) for d in span]
        wr = [wiki_rev_by_bucket[b].get(d.isoformat(), 0) for d in span]
        ax.bar(span, tr, width=1, color=C["sig"], alpha=0.85, label="Transluce reports")
        ax.plot(span, wr, color=C["save"], lw=1.2, drawstyle="steps-mid", label="wiki revisions linking host")
        ax.set_xlim(lo_d, hi_d)
        ax.set_yscale("symlog", linthresh=5); ax.grid(True, axis="y", lw=0.3)
        ax.set_title(f"{b}\nTransluce {s['transluce_reports']:,} reports, all dates (peak {s['transluce_peak_day'][5:]}); wiki {s['wiki_revisions_linking']:,} revisions (peak {s['wiki_peak_day'][5:]}); peak lag {s['peak_lag_days']:+d} d", fontsize=7, loc="left")
        for st, en, _ in WINDOWS:
            ax.axvspan(date.fromisoformat(st), date.fromisoformat(en) + timedelta(days=1), color="#fff", alpha=0.05, lw=0)
    for ax in axes.flat[n:]:
        ax.axis("off")
    h, l = axes.flat[0].get_legend_handles_labels()
    fig2.legend(h, l, fontsize=7, loc="upper right", ncol=2, frameon=False, bbox_to_anchor=(0.99, 0.963))
    for ax in axes.flat:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    # make sure the last visible panel in each column carries x tick labels
    for c in range(ncol):
        vis = [axes[r][c] for r in range(nrow) if r * ncol + c < n]
        if vis:
            vis[-1].tick_params(labelbottom=True)
    fig2.suptitle("Shared target domains: May to early July 2026 (UTC days)\nTransluce reports per source bucket vs wiki revisions linking a matching host. Titles give whole-dump totals.", fontsize=8.5, x=0.01, ha="left")
    fig2.tight_layout(rect=(0, 0, 1, 0.935))
    fig2.savefig(os.path.join(a.out, "shared.png"), dpi=160, bbox_inches="tight")
    fig2.savefig(os.path.join(a.out, "shared.svg"), bbox_inches="tight")
    print("figures written")


if __name__ == "__main__":
    main()
