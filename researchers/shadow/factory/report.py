#!/usr/bin/env python3
"""Read-only result aggregation + labelled post-hoc cross-spec paired sensitivity."""
import html
import json
from pathlib import Path
import statistics
import factory as f

LABELS={
 'split-sonnet-linked-strong':'Linked, reliable, 12 checks',
 'split-sonnet-linked-weak':'Linked, unreliable, 12 checks',
 'split-sonnet-no-links-strong':'No links, reliable, 12 checks',
 'split-sonnet-no-links-weak':'No links, unreliable, 12 checks',
 'split-sonnet-four-checks':'Linked, reliable, 4 checks'}

def root_contrasts(name):
    p=f.ROOT/'results'/name/'records.jsonl'
    rows=[json.loads(l) for l in p.read_text().splitlines()]
    rows={(r['family'],r['task'],r['arm'],r['k']):r for r in rows if r['stage']=='M' and r['status']=='completed'}
    out={}
    for family,task,_,_ in rows:
        keys=[(family,task,'degree',27),(family,task,'degree',1),(family,task,'coverage',27),(family,task,'coverage',1)]
        if all(k in rows for k in keys):out[(family,task)]=sum(sign*rows[k]['metrics']['rare_wrong'] for sign,k in zip((1,-1,-1,1),keys))
    return out

def main():
    names=json.loads((f.ROOT/'queue-structured.json').read_text())['specs']
    summaries=[]
    for name in names:
        p=f.ROOT/'results'/name/'summary.json'
        if p.exists():summaries.append(json.loads(p.read_text()))
    allsum=[json.loads(p.read_text()) for p in (f.ROOT/'results').glob('*/summary.json')]
    lines=['# Factory results: the attacker link assumption is a testable condition','',
      'Exploratory synthetic Sonnet 4.6 sensitivity checks, not a claim about real-world swarms or a new Sybil defense. Reuses Dmarz’s frozen split-policy worlds and credits that study as the source. Each completed comparison has 48 paired roots; the five cohorts share those roots. Source-reported, not independently reviewed.','',
      '## Current results','',
      '| Specification | Main valid / assigned | Paired roots | Primary pp [95% CI] | Status | Accounted USD |',
      '|---|---:|---:|---:|---|---:|']
    for s in summaries:
        name=s['spec'];label=LABELS[name.removesuffix('-or-json')]
        effect='unavailable' if s['primary'] is None else (f"{100*s['primary']:+.1f}, CI not interpreted (<10 roots)" if s['paired_roots']<10 else f"{100*s['primary']:+.1f} [{100*s['ci95'][0]:+.1f}, {100*s['ci95'][1]:+.1f}]")
        lines.append(f"| [{label}](results/{name}/FINDING.md) | {s['main_valid']}/192 | {s['paired_roots']}/48 | {effect} | {s['status']} | {s['paid_usd']:.4f} |")
    lines += ['', '**Primary definition:** (rare-skill wrong fraction at 27 identities minus one identity under degree checks) minus the same difference under coverage checks. Positive means splitting increased wrong answers more under degree; it does not establish that coverage always wins. Intervals are 10,000 within-family root-bootstrap draws, equally weighted families, unadjusted across five dependent tests.', '',
       '![Primary contrast with root-bootstrap intervals](results/contrasts.svg)','',
       '## Attempt lineage and costs','',
       f"All saved cohorts currently account for {sum(s['attempted'] for s in allsum)} attempted calls, {sum(s['valid'] for s in allsum)} valid, {sum(s['failed'] for s in allsum)} failed. Historical transport/schema failures remain separate, never last-valid-selected into repaired cohorts.",
       '', 'The initial pool attempts: 20 HTTP429 failures, $0 external-paid spend. The first OpenRouter attempts: 20 schema-invalid answers (prose/fences), stopped before treatment calls. Both are interface/transport diagnostics, not negative evidence about the scientific contrast. The current attempt prospectively added native strict JSON-schema output and fresh clean qualification roots. See [route amendment](AMENDMENT-PAID.md) and [schema amendment](AMENDMENT-STRUCTURED.md).', '',
       'All paid attempts share one locked USD20 reservation ledger; each spec is capped at USD4. Reported costs and conservative outstanding reservations are in [the ledger](results/paid-ledger.jsonl). No retry or cap expansion. A failed competence screen stops the current queue.']
    contrasts=[]
    for reliability in ('strong','weak'):
        linked='split-sonnet-linked-'+reliability+'-or-json'
        none='split-sonnet-no-links-'+reliability+'-or-json'
        if not all((f.ROOT/'results'/n/'terminal.json').exists() for n in (linked,none)):continue
        a,b=root_contrasts(linked),root_contrasts(none);keys=sorted(a.keys()&b.keys())
        vals={family:[a[k]-b[k] for k in keys if k[0]==family] for family in ('ring','community')}
        if not all(vals.values()):continue
        est=statistics.mean(statistics.mean(v) for v in vals.values());ci=f.bootstrap(vals)
        contrasts.append(dict(condition=reliability,paired_roots=len(keys),linked_minus_no_links=est,ci95=ci,status='post-hoc descriptive'))
    if contrasts:
        lines+=['','## Post-hoc descriptive link sensitivity','',
          'The following cross-spec difference was added after initial calls began, so it is explicitly **post-hoc**, not one of the five preregistered primaries. Pair by the shared root, then subtract no-links from linked before bootstrapping; do not subtract marginal CI endpoints.']
        for c in contrasts:
            lines.append(f"- {c['condition']} checks: linked minus no-links primary = {100*c['linked_minus_no_links']:+.1f} pp, CI [{100*c['ci95'][0]:+.1f}, {100*c['ci95'][1]:+.1f}], {c['paired_roots']} paired roots.")
    f.dump(f.ROOT/'results'/'cross_spec_posthoc.json',contrasts)
    lines+=['','## Provider stop and precision warning','',
      'The first structured paid run stopped at a shared OpenRouter key limit (read-only metadata: USD5 daily cap, zero remaining). No key limit or credential was changed. It has only 2/48 complete roots despite 88 valid main calls: its narrow complete-case bootstrap is not meaningful precision. All-assigned bounds are -93.1 to +123.6 pp, so no directional finding is established. New native-schema pool specs, separately preregistered, use root-first dispatch and bounded429 backoff. See [native amendment](AMENDMENT-NATIVE.md).', '',
      '## Scope and interpretation','',
      '“Finding” is a within-spec, complete-data directional signal whose entire CI exceeds 10 points. “Negative” means the preregistered useful-direction criterion was not met, not equivalence or an absence of any effect. “Lead” includes partial data and failed qualification. None is formal hypothesis acceptance.', '',
      'The link ablation does not identify an arbitrary graph-only causal mechanism: changing attacker-internal links also changes admission and can put split identities at an admission floor. It asks whether the original setup-dependent result survives removing one explicit modeling assumption. The parent already anticipated scripted attenuation; this is a native-model sensitivity check.', '',
      'Only synthetic reports are used, no incident-dataset row or private user text. One synthesizer per packet, not 108 independently running LLM agents. Model and inference configuration differ from the parent. Twelve clean fixtures are a reduced screen, and no published Sybil-defense comparator is evaluated.', '',
      '## Reproduce','',
      '`python3 researchers/shadow/factory/structured.py analyze --spec <id>` regenerates per-spec estimates from saved terminal records and the pinned generator. `python3 researchers/shadow/factory/report.py` regenerates this report and figure. See [README](README.md), [source specs](specs/), and [Dmarz parent](../../dmarz/notes/sybil-split-opus/RESULTS.md).','']
    (f.ROOT/'FINDING.md').write_text('\n'.join(lines))
    # Original vector figure, 1600px wide, unit-correct percentage point axis.
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="660" viewBox="0 0 1600 660">',
       '<rect width="1600" height="660" fill="#11151c"/><g font-family="monospace" fill="#e6edf3">',
       '<text x="45" y="55" font-size="29">Identity splitting: sensitivity to attacker links and check reliability</text>',
       '<text x="45" y="93" font-size="20">Sonnet 4.6 | 48 paired roots per complete row | exploratory, shared synthetic worlds</text>']
    def x(v):return 970+v*510
    for tick in (-1,-.5,0,.5,1):
        xx=x(tick);svg.append(f'<line x1="{xx}" x2="{xx}" y1="140" y2="570" stroke="#384353"/><text x="{xx-23}" y="605" font-size="20">{tick*100:+.0f}</text>')
    for i,s in enumerate(summaries):
        yy=180+i*80;label=LABELS[s['spec'].removesuffix('-or-json')]
        svg.append(f'<text x="45" y="{yy+7}" font-size="21">{html.escape(label)}</text>')
        if s['primary'] is None or s['paired_roots']<10:continue
        lo,hi=s['ci95'];color='#8ddd9a' if s['status']=='finding' else '#e9bc69'
        svg.append(f'<line x1="{x(lo)}" x2="{x(hi)}" y1="{yy}" y2="{yy}" stroke="{color}" stroke-width="5"/><circle cx="{x(s["primary"])}" cy="{yy}" r="8" fill="{color}"/>')
    svg+=['<text x="620" y="644" font-size="19">Degree-minus-coverage splitting effect (percentage points), 95% root-bootstrap CI</text>','</g></svg>']
    (f.ROOT/'results'/'contrasts.svg').write_text('\n'.join(svg))
    print('report cohorts:',len(summaries),'posthoc contrasts:',len(contrasts))
if __name__=='__main__':main()
