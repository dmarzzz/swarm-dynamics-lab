#!/usr/bin/env python3
"""Idea half-life: adoption curves for reused text units in two swarms.

Offline, no model calls. Implements PLAN.md (fixed 2026-10-04 before outcomes were computed).

  python3 halflife.py --wiki <collusion-wiki dir> --repo <swarm-lab checkout> --rev 66fa0aa6 \
      --out results/

Source rows are never written out; only aggregates and a few short unit examples.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import gzip
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np

SEED = 20261004
N_BOOT = 1000
BINS = [(1, 1), (2, 2), (3, 4), (5, 9), (10, 19), (20, 10**9)]
URL_RE = re.compile(r"https?://[^\s\]|\"'<>)]+", re.I)
LEAD_RE = re.compile(r"^[\s*\-#=>|]+")
WIKI_DEFAULT = "beschreibe hier die neue seite."
# POST-HOC (added after first results, 2026-10-04): the wiki's English default page text and template
# files outside templates/** (e.g. tooling/agent-experiments/templates/) surfaced among top units.
# Only used when --posthoc is passed; preregistered outputs never use these.
POSTHOC_WIKI_DEFAULTS = {"describe the new page here."}
POSTHOC_TEMPLATE_GLOB = ":(glob)**/templates/**"
POSTHOC = False
GIT_EXCLUDE = ["STATUS.md", "library/INDEX.md", "library/references.bib"]
AGENT_RE = re.compile(r"^\[([A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)\]")
MIN_LINE = 25


# ---------------------------------------------------------------- units

def url_units(text: str) -> set[str]:
    out = set()
    for m in URL_RE.findall(text):
        u = m.rstrip(".,;:").lower()
        if len(u) > len("https://"):
            out.add(u)
    return out


def norm_line(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = LEAD_RE.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def line_units(lines, exclude=frozenset()) -> set[str]:
    out = set()
    for l in lines:
        n = norm_line(l)
        if len(n) >= MIN_LINE and n != WIKI_DEFAULT and n not in exclude and not (
                POSTHOC and n in POSTHOC_WIKI_DEFAULTS):
            out.add(n)
    return out


def host_of(u: str) -> str:
    return u.split("://", 1)[1].split("/", 1)[0].split("?", 1)[0]


# ---------------------------------------------------------------- record model
# A record = one revision / commit: (time_epoch_s, identity_A, identity_B, cluster, {kind: set(units)})

def parse_time(s: str) -> float:
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()


def load_wiki(path: str):
    fn = os.path.join(path, "revisions.jsonl.gz")
    rows = [json.loads(l) for l in gzip.open(fn, "rt")]
    recs, empty_label = [], 0
    for r in rows:
        body = r["body"] or ""
        L = body.split("\n")
        ins = []
        for h in r["hunks"] or []:
            if h["op"] in ("insert", "replace"):
                ins += L[h["b0"]:h["b1"]]
        text = "\n".join(ins)
        urls = url_units(text)
        if not r["label"]:
            empty_label += 1
        recs.append(dict(
            t=parse_time(r["time"]), a=r["label"] or None, b=r["ip16"] or None, cluster=r["page_id"],
            units={"url": urls, "line": line_units(ins), "host": {host_of(u) for u in urls}},
            page=r["page_id"], full_urls=url_units(body), rev=r["rev_id"]))
    meta = dict(source="collusion.wiki revisions.jsonl.gz", sha256=sha256_file(fn), records=len(rows),
                records_empty_label=empty_label)
    return recs, meta


def git(repo, *args) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                          text=True, errors="replace").stdout


def load_git(repo: str, rev: str):
    rev = git(repo, "rev-parse", rev).strip()
    tmpl_spec = ["templates", POSTHOC_TEMPLATE_GLOB] if POSTHOC else ["templates"]
    tmpl = git(repo, "log", "--no-merges", "-p", "--format=", rev, "--", *tmpl_spec)
    tmpl_lines = {norm_line(l[1:]) for l in tmpl.split("\n") if l.startswith("+") and not l.startswith("+++")}
    pathspec = ["--", "."] + [f":(exclude){p}" for p in GIT_EXCLUDE] + [":(exclude)templates"]
    if POSTHOC:
        pathspec.append(":(exclude,glob)**/templates/**")
    out = subprocess.Popen(["git", "-C", repo, "log", "--no-merges", "-p", "--no-color",
                            "--format=@@@COMMIT %H %at %an%x09%s", rev, *pathspec],
                           stdout=subprocess.PIPE, text=True, errors="replace")
    recs, skipped = [], collections.Counter()
    cur, added = None, []

    def flush():
        if cur is None:
            return
        h, t, author, subj = cur
        if subj.startswith("[bot]") or "[bot]" in author or author.endswith("-bot"):
            skipped["bot"] += 1
            return
        m = AGENT_RE.match(subj)
        if not m:
            skipped["no_agent_id"] += 1
            return
        aid = m.group(1)
        text = "\n".join(added)
        urls = url_units(text)
        recs.append(dict(t=float(t), a=aid, b=aid.split("/")[0], cluster=h,
                         units={"url": urls, "line": line_units(added, tmpl_lines),
                                "host": {host_of(u) for u in urls}}))

    for line in out.stdout:
        line = line.rstrip("\n")
        if line.startswith("@@@COMMIT "):
            flush()
            h, t, rest = line[10:].split(" ", 2)
            author, _, subj = rest.partition("\t")
            cur, added = (h, t, author, subj), []
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    flush()
    out.wait()
    meta = dict(source="dmarzzz/swarm-lab git history (non-merge, origin/main)", rev=rev,
                records=len(recs), skipped=dict(skipped), template_lines_excluded=len(tmpl_lines))
    return recs, meta


def sha256_file(fn):
    h = hashlib.sha256()
    with open(fn, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- adoption extraction

def activity_clock(recs):
    """Activity time = number of in-scope records strictly earlier (ties share a value)."""
    ts = np.array(sorted(r["t"] for r in recs))
    return lambda t: float(np.searchsorted(ts, t, side="left")), ts


def adoption_table(recs, kind, ident):
    """unit -> sorted list of (t, act, identity, cluster) for each identity's first insertion."""
    act, ts = activity_clock(recs)
    first: dict[str, dict] = collections.defaultdict(dict)
    for r in recs:
        who = r[ident]
        if who is None:
            continue
        for u in r["units"][kind]:
            d = first[u]
            prev = d.get(who)
            if prev is None or r["t"] < prev[0]:
                d[who] = (r["t"], r["cluster"])
    t_end = float(ts[-1])
    a_end = float(len(ts))
    table = {}
    for u, d in first.items():
        ev = sorted((t, act(t), who, c) for who, (t, c) in d.items())
        table[u] = ev
    return table, t_end, a_end, act


def unit_intervals(ev, t_end, a_end, clock):
    """Yield (j, exposure, event) intervals; j = distinct identities so far.

    clock: 0 = wall hours, 1 = activity records. Ties at origin all count as originators.
    """
    idx = 1 if clock else 0
    scale = 1.0 if clock else 1 / 3600.0
    end = a_end if clock else t_end
    t0 = ev[0][idx]
    j = sum(1 for e in ev if e[idx] == t0)
    last = t0
    out = []
    for e in ev[j:]:
        out.append((j, (e[idx] - last) * scale, 1))
        last = e[idx]
        j += 1
    out.append((j, max(end - last, 0.0) * scale, 0))
    return out


def bin_of(j):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= j <= hi:
            return i
    raise ValueError(j)


# ---------------------------------------------------------------- statistics

def weighted_km(dur, obs, w, points):
    """Kaplan-Meier adoption fraction F(t)=1-S(t) at points, with unit weights w."""
    order = np.argsort(dur, kind="stable")
    d, o, ww = dur[order], obs[order], w[order]
    times, start = np.unique(d, return_index=True)
    wsum = np.add.reduceat(ww, start)
    esum = np.add.reduceat(ww * o, start)
    at_risk = ww.sum() - np.concatenate([[0], np.cumsum(wsum)[:-1]])
    with np.errstate(divide="ignore", invalid="ignore"):
        haz = np.where(at_risk > 0, esum / np.where(at_risk > 0, at_risk, 1), 0.0)
    surv = np.cumprod(1 - haz)
    res = []
    for p in points:
        k = np.searchsorted(times, p, side="right") - 1
        res.append(1 - (surv[k] if k >= 0 else 1.0))
    return np.array(res), times, 1 - surv


def wmedian(x, w):
    if w.sum() <= 0:
        return float("nan")
    o = np.argsort(x)
    x, w = x[o], w[o]
    c = np.cumsum(w)
    return float(x[np.searchsorted(c, 0.5 * c[-1])])


def wls_slope(E, X, mids):
    r = np.divide(E, X, out=np.zeros_like(E), where=X > 0)
    m = (E > 0) & (X > 0)
    if m.sum() < 2:
        return float("nan")
    x, y, w = np.log(mids[m]), np.log(r[m]), E[m]
    xm, ym = (w * x).sum() / w.sum(), (w * y).sum() / w.sum()
    den = (w * (x - xm) ** 2).sum()
    return float((w * (x - xm) * (y - ym)).sum() / den) if den > 0 else float("nan")


def ci(a):
    a = np.asarray(a, float)
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return [None, None]
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def analyse(table, t_end, a_end, rng, label):
    units = list(table)
    nU = len(units)
    nid = np.array([len(table[u]) for u in units])
    clus_names = sorted({table[u][0][3] for u in units})
    cidx = {c: i for i, c in enumerate(clus_names)}
    ucl = np.array([cidx[table[u][0][3]] for u in units])
    nC = len(clus_names)
    boot_w = rng.multinomial(nC, np.ones(nC) / nC, size=N_BOOT).astype(float)  # cluster counts
    res = dict(units=nU, clusters=nC, reach_ge2=float((nid >= 2).mean()), reach_ge5=float((nid >= 5).mean()),
               reach_ge10=float((nid >= 10).mean()), units_ge2=int((nid >= 2).sum()),
               units_ge5=int((nid >= 5).sum()), max_identities=int(nid.max()) if nU else 0)
    mids = np.array([1, 2, 3.5, 7, 14.5, 30.0])
    for clock, cname, pts in ((1, "activity", [10, 100, 1000]), (0, "wall_h", [1, 24, 24 * 7])):
        # time to second identity
        dur, obs = np.zeros(nU), np.zeros(nU)
        E = np.zeros((nC, len(BINS)))
        X = np.zeros((nC, len(BINS)))
        Ew = np.zeros((nC, 4))
        Xw = np.zeros((nC, 4))
        t50, t50c = [], []
        for i, u in enumerate(units):
            iv = unit_intervals(table[u], t_end, a_end, clock)
            dur[i], obs[i] = iv[0][1], iv[0][2]
            if iv[0][0] >= 2:  # tie at origin: adopted at time 0
                dur[i], obs[i] = 0.0, 1
            for j, x, e in iv:
                b = bin_of(j)
                E[ucl[i], b] += e
                X[ucl[i], b] += x
                if nid[i] >= 5 and j <= 4:
                    Ew[ucl[i], j - 1] += e
                    Xw[ucl[i], j - 1] += x
            if nid[i] >= 5:
                idx = 1 if clock else 0
                scale = 1.0 if clock else 1 / 3600.0
                half = math.ceil(nid[i] / 2)
                t50.append((table[u][half - 1][idx] - table[u][0][idx]) * scale)
                t50c.append(ucl[i])
        t50, t50c = np.array(t50), np.array(t50c, int)
        w1 = np.ones(nU)
        F, kt, kF = weighted_km(dur, obs, w1, pts)
        adopted = obs == 1
        cond_med = float(np.median(dur[adopted])) if adopted.any() else None
        Et, Xt = E.sum(0), X.sum(0)
        rate = np.divide(Et, Xt, out=np.full(len(BINS), np.nan), where=Xt > 0)
        beta = wls_slope(Et, Xt, mids)
        Ewt, Xwt = Ew.sum(0), Xw.sum(0)
        rate_w = np.divide(Ewt, Xwt, out=np.full(4, np.nan), where=Xwt > 0)
        beta_w = wls_slope(Ewt, Xwt, np.array([1, 2, 3, 4.0]))
        bF, bmed, bbeta, bbw, bt50, brate = [], [], [], [], [], []
        for w in boot_w:
            uw = w[ucl]
            bF.append(weighted_km(dur, obs, uw, pts)[0])
            bmed.append(wmedian(dur[adopted], uw[adopted]) if adopted.any() else np.nan)
            bE, bX = w @ E, w @ X
            bbeta.append(wls_slope(bE, bX, mids))
            brate.append(np.divide(bE, bX, out=np.full(len(BINS), np.nan), where=bX > 0))
            bbw.append(wls_slope(w @ Ew, w @ Xw, np.array([1, 2, 3, 4.0])))
            bt50.append(wmedian(t50, w[t50c]) if len(t50) else np.nan)
        bF = np.array(bF)
        brate = np.array(brate)
        res[cname] = dict(
            km_points=pts, km_adopted_frac=[float(f) for f in F],
            km_adopted_frac_ci=[ci(bF[:, k]) for k in range(len(pts))],
            km_curve=downsample(kt, kF),
            cond_median_time_to_2nd=cond_med, cond_median_time_to_2nd_ci=ci(bmed),
            t50_median_units_ge5=float(np.median(t50)) if len(t50) else None, t50_ci=ci(bt50),
            rate_bins=[f"{lo}-{hi}" if hi < 10**9 else f"{lo}+" for lo, hi in BINS],
            rate_events=[int(e) for e in Et], rate_exposure=[float(x) for x in Xt],
            rate=[None if not np.isfinite(r) else float(r) for r in rate],
            rate_ci=[ci(brate[:, k]) for k in range(len(BINS))],
            beta=beta, beta_ci=ci(bbeta),
            within_ge5_rate_j1to4=[None if not np.isfinite(r) else float(r) for r in rate_w],
            within_ge5_events=[int(e) for e in Ewt],
            within_ge5_beta=beta_w, within_ge5_beta_ci=ci(bbw))
    top = sorted(units, key=lambda u: (-len(table[u]), u))[:5]
    res["top_units"] = [dict(unit=u[:90], identities=len(table[u])) for u in top]
    print(f"  {label}: {nU} units, {res['units_ge2']} >=2 ids, beta act={res['activity']['beta']:.2f} "
          f"within={res['activity']['within_ge5_beta']:.2f}", file=sys.stderr)
    return res


def downsample(t, F, n=200):
    if len(t) <= n:
        return [[float(a), float(b)] for a, b in zip(t, F)]
    idx = np.unique(np.linspace(0, len(t) - 1, n).astype(int))
    return [[float(t[i]), float(F[i])] for i in idx]


# ---------------------------------------------------------------- wiki visible copies

def visible_copies(recs, table_url, t_end, n_boot=0):
    """Rate of new label adoption vs number of pages currently showing the URL (wiki only).

    A page shows a URL if its latest revision body contains it. Deletions are ignored (stated limit).
    Exposure on the activity clock.
    """
    act, _ = activity_clock(recs)
    a_end = float(len(recs))
    # per URL: list of (act, page, present_bool) state changes
    changes = collections.defaultdict(list)
    last_state = {}
    for r in sorted(recs, key=lambda r: r["t"]):
        a = act(r["t"])
        prev = last_state.get(r["page"], set())
        cur = r["full_urls"]
        for u in cur - prev:
            changes[u].append((a, r["page"], 1))
        for u in prev - cur:
            changes[u].append((a, r["page"], -1))
        last_state[r["page"]] = cur
    vb = [(0, 0), (1, 1), (2, 2), (3, 4), (5, 9), (10, 10**9)]
    clusters = sorted({ev[0][3] for ev in table_url.values()})
    cluster_idx = {c: i for i, c in enumerate(clusters)}
    Ec = np.zeros((len(clusters), len(vb)))
    Xc = np.zeros_like(Ec)
    for u, ev in table_url.items():
        c = cluster_idx[ev[0][3]]
        arrivals = sorted(e[1] for e in ev)
        a0 = arrivals[0]
        arr = collections.Counter(arrivals[1:]) if len(ev) > 1 else collections.Counter()
        # first arrivals at a0 are originators
        arr = collections.Counter({k: v for k, v in arr.items() if k > a0})
        pts = sorted(set([a0, a_end] + [c[0] for c in changes.get(u, []) if c[0] > a0] + list(arr)))
        ch = sorted(changes.get(u, []))
        vis, ci_ = collections.Counter(), 0
        # apply changes up to and including a0 (the origin revision itself writes the URL)
        while ci_ < len(ch) and ch[ci_][0] <= a0:
            vis[ch[ci_][1]] += ch[ci_][2]; ci_ += 1
        for k in range(len(pts) - 1):
            lo, hi = pts[k], pts[k + 1]
            n_vis = sum(1 for v in vis.values() if v > 0)
            # adoptions at hi are attributed to the state just before hi
            b = next(i for i, (l, h) in enumerate(vb) if l <= n_vis <= h)
            Xc[c, b] += hi - lo
            Ec[c, b] += arr.get(hi, 0)
            while ci_ < len(ch) and ch[ci_][0] <= hi:
                vis[ch[ci_][1]] += ch[ci_][2]; ci_ += 1
    E, X = Ec.sum(0), Xc.sum(0)
    rate = np.divide(E, X, out=np.full(len(vb), np.nan), where=X > 0)
    result = dict(bins=[f"{l}-{h}" if h < 10**9 else f"{l}+" for l, h in vb], events=[int(e) for e in E],
                  exposure_records=[float(x) for x in X],
                  rate_per_1k_records=[None if not np.isfinite(r) else float(r * 1000) for r in rate],
                  note="Adoptions by new labels of URLs; visibility = pages whose latest revision contains the URL; "
                       "moderator page-deletion events ignored, revision removals included; activity clock. "
                       "Tied-origin identities excluded from subsequent-arrival counts.")
    if n_boot:
        rng = np.random.default_rng(SEED)
        weights = rng.multinomial(len(clusters), np.ones(len(clusters)) / len(clusters), size=n_boot)
        be, bx = weights @ Ec, weights @ Xc
        br = np.divide(be * 1000, bx, out=np.full_like(bx, np.nan), where=bx > 0)
        result.update(n_boot=n_boot, seed=SEED, clusters=len(clusters),
                      rate_per_1k_records_ci=[ci(br[:, i]) for i in range(len(vb))],
                      uncertainty="Post-draft supplement: origin-page percentile cluster bootstrap, not independent pages.")
    return result


# ---------------------------------------------------------------- figure

def figure(summary, path, visibility=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3 if visibility else 2, figsize=(15.5 if visibility else 11, 4.2))
    styles = {("wiki", "url"): ("#d62728", "-"), ("wiki", "line"): ("#d62728", "--"),
              ("git", "url"): ("#1f77b4", "-"), ("git", "line"): ("#1f77b4", "--")}
    names = {"wiki": "collusion.wiki (label)", "git": "swarm-lab git (agent id)"}
    for (sw, kind), (col, ls) in styles.items():
        r = summary[sw]["A"][kind]["activity"]
        c = np.array(r["km_curve"])
        if len(c):
            ax[0].step(np.maximum(c[:, 0], 0.5), c[:, 1], where="post", color=col, ls=ls,
                       label=f"{names[sw]}, {kind} units")
        # Pointwise uncertainty only, not a simultaneous confidence band.
        ax[0].vlines(r['km_points'], [x[0] for x in r['km_adopted_frac_ci']],
                     [x[1] for x in r['km_adopted_frac_ci']], color=col, alpha=.5, lw=1.4)
        ax[0].plot(r['km_points'], r['km_adopted_frac'], color=col, ls='none',
                   marker='o' if kind == 'url' else 'x', ms=3)
        rates = r["rate"]
        xs = [1, 2, 3.5, 7, 14.5, 30.0]
        pts = [(x, y, lo_hi) for x, y, lo_hi in zip(xs, rates, r["rate_ci"]) if y]
        if pts:
            x, y, l = zip(*pts)
            yerr = [[yy - (li[0] or yy) for yy, li in zip(y, l)], [(li[1] or yy) - yy for yy, li in zip(y, l)]]
            ax[1].errorbar(np.array(x) * (1.04 if sw == "git" else 1), np.array(y) * 1000, yerr=np.array(yerr) * 1000,
                           color=col, ls=ls, marker="o", ms=4, capsize=2,
                           label=f"{names[sw]}, {kind}: beta={r['beta']:.2f}")
    ax[0].set_xscale("log"); ax[0].set_xlabel("activity time since first appearance (swarm records)")
    ax[0].set_ylabel("fraction of units with a 2nd identity (KM)")
    ax[0].set_title("A. time to first adoption by another identity")
    ax[0].legend(fontsize=7)
    xx = np.array([1, 30.0])
    ax[1].plot(xx, xx * 0 + 1, alpha=0)  # keep log axes sane
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("identities that already wrote the unit (j)")
    ax[1].set_ylabel("new-identity adoptions per 1k swarm records")
    ax[1].set_title("B. adoption rate vs prior adopters (95% cluster bootstrap)")
    ax[1].legend(fontsize=7)
    if visibility:
        yy = np.array(visibility['rate_per_1k_records'])
        cc = np.array(visibility['rate_per_1k_records_ci'])
        xx = np.arange(len(yy))
        ax[2].plot(xx, yy, color='#d62728', marker='o', ms=4)
        ax[2].vlines(xx, cc[:, 0], cc[:, 1], color='#d62728', lw=1.4)
        ax[2].set_xticks(xx, ['0', '1', '2', '3–4', '5–9', '10+'])
        ax[2].set_yscale('log')
        ax[2].set_xlabel('pages showing URL in latest known revision')
        ax[2].set_ylabel('new-label adoptions per 1k wiki records')
        ax[2].set_title('C. wiki visibility proxy (95% cluster bootstrap)')
        ax[2].text(.03, .97, 'Not actual views; page deletion events ignored',
                   transform=ax[2].transAxes, va='top', fontsize=7)
    fig.tight_layout()
    fig.savefig(path, dpi=170)


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", required=True, help="collusion-wiki data dir (revisions.jsonl.gz)")
    ap.add_argument("--repo", required=True, help="swarm-lab git checkout")
    ap.add_argument("--rev", default="66fa0aa6")
    ap.add_argument("--out", required=True)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--posthoc", action="store_true",
                    help="POST-HOC sensitivity: extra boilerplate exclusions, identity A only, writes posthoc.json")
    a = ap.parse_args(argv)
    globals()["N_BOOT"] = a.boot
    globals()["POSTHOC"] = a.posthoc
    os.makedirs(a.out, exist_ok=True)
    summary = dict(plan="PLAN.md", seed=SEED, n_boot=a.boot, generated_by="halflife.py",
                   note="Aggregates only. Intervals: 95% percentile cluster bootstrap over origin page (wiki) "
                        "or origin commit (git); describe these corpora only.")
    print("loading wiki", file=sys.stderr)
    wrecs, wmeta = load_wiki(a.wiki)
    print("loading git", file=sys.stderr)
    grecs, gmeta = load_git(a.repo, a.rev)
    summary["inputs"] = dict(wiki=wmeta, git=gmeta)
    for sw, recs in (("wiki", wrecs), ("git", grecs)):
        ts = sorted(r["t"] for r in recs)
        summary[sw] = dict(records=len(recs), span_hours=(ts[-1] - ts[0]) / 3600,
                           identities_A=len({r["a"] for r in recs if r["a"]}),
                           identities_B=len({r["b"] for r in recs if r["b"]}))
        for ident in (("a",) if a.posthoc else ("a", "b")):
            key = ident.upper()
            summary[sw][key] = {}
            for kind in ("url", "line", "host"):
                rng = np.random.default_rng(SEED)
                table, t_end, a_end, _ = adoption_table(recs, kind, ident)
                summary[sw][key][kind] = analyse(table, t_end, a_end, rng, f"{sw}/{key}/{kind}")
                if sw == "wiki" and ident == "a" and kind == "url" and not a.posthoc:
                    summary[sw]["visible_copies_url"] = visible_copies(recs, table, t_end)
    if a.posthoc:
        summary["posthoc"] = ("POST-HOC sensitivity, not preregistered: excludes the wiki English default page "
                              "line and git lines from any **/templates/** path. Identity A only.")
        with open(os.path.join(a.out, "posthoc.json"), "w") as f:
            json.dump(summary, f, indent=1)
        print("done", file=sys.stderr)
        return
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    figure(summary, os.path.join(a.out, "fig-adoption.png"))
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
