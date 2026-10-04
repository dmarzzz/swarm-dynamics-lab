#!/usr/bin/env python3
"""Saved-data closeout and one static measured-dose figure, never dispatch."""
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import zipfile
import analyze
import recompute

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'results'


def figure(rows,source):
    main=[r for r in rows if r['stage']=='M' and r['status']=='completed']
    if not main:return None
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1080" viewBox="0 0 1800 1080">',
         '<rect width="1800" height="1080" fill="white"/>',
         '<g font-family="sans-serif" fill="#182330">',
         '<text x="70" y="48" font-size="29">Provenance attempt 2: measured root-level copy-dose responses</text>',
         f'<text x="70" y="82" font-size="19">OpenRouter / Anthropic sonnet-4.6 | source {html.escape(source[:12])} | 12 assigned numeric roots</text>']
    colors=['#a23328','#186a80','#42712d','#694c91']
    for i,arm in enumerate(('raw','ancestry','dedup','padding')):
        ox=95+(i%2)*865;oy=150+(i//2)*405
        cells=[r for r in main if r['arm']==arm]
        lookup={(r['root'],r['copies']):r['metrics']['accuracy'] for r in cells}
        full=sum(all((root,dose) in lookup for dose in (1,4,16)) for root in range(12))
        out += [f'<text x="{ox}" y="{oy}" font-size="24">{arm}: {len(cells)}/36 valid cells, {full}/12 full dose series</text>']
        xs={1:ox+70,4:ox+345,16:ox+620}
        for score in (0,1):
            y=oy+260-score*185
            out += [f'<line x1="{ox+70}" y1="{y}" x2="{ox+620}" y2="{y}" stroke="#d8dce1"/>',
                    f'<text x="{ox+40}" y="{y+6}" font-size="19">{score}</text>']
        for root in range(12):
            for lo,hi in ((1,4),(4,16)):
                if (root,lo) in lookup and (root,hi) in lookup:
                    y1=oy+260-lookup[(root,lo)]*185;y2=oy+260-lookup[(root,hi)]*185
                    out.append(f'<line x1="{xs[lo]}" y1="{y1}" x2="{xs[hi]}" y2="{y2}" stroke="{colors[i]}" stroke-width="2" opacity="0.3"/>')
            for dose in (1,4,16):
                if (root,dose) in lookup:
                    y=oy+260-lookup[(root,dose)]*185
                    out.append(f'<circle cx="{xs[dose]}" cy="{y}" r="5" fill="{colors[i]}" opacity="0.35"/>')
        for dose in (1,4,16):
            n=sum((root,dose) in lookup for root in range(12))
            out.append(f'<text x="{xs[dose]-30}" y="{oy+295}" font-size="18">{dose} copies</text>')
            out.append(f'<text x="{xs[dose]-30}" y="{oy+320}" font-size="16">n={n}/12</text>')
    out += ['<text x="70" y="1000" font-size="19">Y: exact decision-rule accuracy (0 or 1). Each translucent series is one root; identical observations overlap.</text>',
            '<text x="70" y="1032" font-size="19">Gaps are missing observations, not failures. Calls and copies are not independent worlds. Static doses, not time.</text>',
            '</g></svg>']
    path=BASE/'dose-trajectories.svg';path.write_text('\n'.join(out)+'\n');return path.name


def main():
    summary=analyze.report(BASE);check=recompute.check(BASE)
    c=summary['cohorts'][0];rows=[json.loads(p.read_text()) for p in sorted((BASE/'openrouter/outcomes').glob('*.json'))]
    valid=[r for r in rows if r['status']=='completed'];mainrows=[r for r in valid if r['stage']=='M']
    calls=sum(r.get('network_attempted') is True for r in rows)
    spent=sum(r.get('paid_usd',0) for r in rows if not r.get('cost_unknown'))
    unknown=sum(r.get('paid_usd',0) for r in rows if r.get('cost_unknown'))
    primary=c['contrasts']['raw-16-minus-1-accuracy'];full=c['complete_roots']
    fig=figure(rows,summary['source_revision'])
    if mainrows:
        accuracy=sum(r['metrics']['accuracy'] for r in mainrows)
        sentence=f'In this synthetic fixed-evidence pilot, {accuracy}/{len(mainrows)} main answers followed the unique-acquisition rule; raw16-minus1 accuracy difference was {primary["mean_complete"]} across {primary["complete_roots"]} paired roots.'
        confidence=1
    elif c['terminal']['qualification_passed']:
        sentence='The clean qualification passed, but no main comparison was observed.';confidence=0
    else:
        sentence=f'Qualification stopped at {c["qualification_correct"]}/6 correct clean answers; no treatment comparison was admitted.';confidence=0
    errors=Counter((r.get('error','unknown'),r.get('error_class','local_or_validation')) for r in rows if r['status']=='failed')
    lines=['# Provenance / duplication invariance: attempt 2','',sentence,'',
        '## Evidence metadata','',
        f'- **evidence_confidence: {confidence}/4.** Small exploratory synthetic instrument under one grammar; no independent scientific-result review or broad provenance claim. A failed gate supports no treatment conclusion.',
        f'- **sample_size_summary:** {calls} new HTTP attempts, {len(valid)} valid answers ({c["qualification_correct"]} correct qualification, {len(mainrows)} main), {full}/12 completely observed main roots. Planned150 assignments:6 clean qualification plus144 main cells. Original cap permits at most149 new HTTP attempts after2 historical requests. Calls and copies are not independent worlds.',
        '- Assessor: shadow/sol-factory,2026-10-04. This is same-author closeout and computational verification, not independent human/researcher review.',
        f'- Frozen implementation: `{summary["source_revision"]}`. [Plan](../SPEC.md), [admission](admission.json), [summary](summary.json), [recomputation](recomputation.json).','',
        '## Qualification, execution and missing outcomes','',
        f'- Qualification: {c["qualification_correct"]}/6 correct; passed={c["terminal"]["qualification_passed"]}. Gate unchanged; no prompt tuning or replacement calls.',
        f'- Terminal reason: `{c["terminal"]["reason"]}`. Categories: `{json.dumps(c["statuses"],sort_keys=True)}`.',
        '- Attempt1 remains frozen:2 HTTP refusals,0 answers,0 complete roots. Its missing cells are not imputed or pooled with attempt2.',
        '- Attempt2 uses fresh qualification seed202610040604 and the originally planned12 main numeric roots. No pool use, HTTP retries, provider fallback, key rotation or limit changes.',
        '- The original151 cumulative HTTP allowance is not reset. If the gate and subsequent calls succeed, the final main cell remains not-run because only149 calls remain.',
        f'- Provider input-token range: `{c["actual_input_tokens_range"]}`. Proxy budget is exactly1800 cl100k tokens; provider-token equality is not claimed.','',
        '## Error table','',
        '| Error | Class | Attempted assignments |','|---|---|---|']
    lines += [f'| `{e}` | {kind} | {n} |' for (e,kind),n in sorted(errors.items())] or ['| None observed | n/a | 0 |']
    lines += ['', 'Failed requests are missing model responses, not known incorrect scientific answers. HTTP400 is contract failure;429/503 are availability failures. Neither is retried or triggers fallback. Unstarted cells remain explicit in immutable outcomes.','',
        '## Costs and validation','',
        f'- New settled/known cost: **USD{spent:.6f}**. New unresolved reservations: **USD{unknown:.6f}**. New liability: **USD{spent+unknown:.6f}**, hard capUSD9.',
        f'- Original factory ledger cumulative liability: **USD{check["factory_paid_liability"]:.6f}**, including priorUSD1.851345. Unknown reservations are carried, not released on refusal.',
        f'- Stdlib checker: **{check["checks"]} checks pass**, recomputing from saved assignment/outcome data without importing the runner or scorer.16 offline fault tests pass normal/-O.','',
        '## Root-level results','',
        f'Primary raw16-minus1 accuracy: `{json.dumps(primary,sort_keys=True)}`. All12 assigned-root worst-case bounds remain explicit. Bootstrap intervals are exploratory and withheld below10 paired roots.',
        'Full root-by-root accuracy, false-confidence, decision-flip and intervention contrasts are in summary.json. These endpoints are dependent and not multiplicity-adjusted confirmatory tests.','']
    if fig:lines += [f'![Measured root-level copy-dose trajectories]({fig})','', 'One measured static figure. It is not a temporal animation: each call is fresh/stateless. Coincident root trajectories overlap. Missing points are not imputed.','']
    else:lines += ['No figure: no main trajectories exist. An empty effect chart would falsely suggest a null result.','']
    lines += ['## Scope and decision','',
        'The normative outcome is the sign of five unique signed integer contributions, not a sampled latent real-world truth. Ancestry is trusted harness metadata, raw text has exact-copy cues, and dedup is deterministic preprocessing. This cannot establish semantic source authentication, real-world independence, swarm advantage or general confidence calibration. Twelve numeric roots share one task grammar.',
        'Stop this attempt. A valid null or adverse result is not permission to rerun for a preferred effect. Independent saved-result inspection remains required before any scaling; independently checked completed contrasts/hour remains0 until that happens.']
    (BASE/'FINDING.md').write_text('\n'.join(lines)+'\n')
    paths=[BASE/'admission.json',BASE/'assignments.json',BASE/'calls.jsonl']+sorted((BASE/'openrouter').rglob('*.json'))
    inventory={'source_revision':summary['source_revision'],'files':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    ip=BASE/'numeric-inventory.json'
    if not ip.exists():ip.write_text(json.dumps(inventory,indent=2)+'\n')
    elif json.loads(ip.read_text())!=inventory:raise ValueError('immutable_inventory_mismatch')
    zp=BASE/'numeric-evidence.zip'
    if not zp.exists():
        with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for p in paths+[ip]:z.write(p,str(p.relative_to(BASE)))
    with zipfile.ZipFile(zp) as z:
        if z.testzip() is not None:raise ValueError('archive_crc')
        for name,digest in inventory['files'].items():
            if hashlib.sha256(z.read(name)).hexdigest()!=digest:raise ValueError('archive_hash')
    (BASE/'archive-checksum.json').write_text(json.dumps({'file':zp.name,'sha256':hashlib.sha256(zp.read_bytes()).hexdigest(),'bytes':zp.stat().st_size},indent=2)+'\n')
    print(json.dumps({'http_attempts':calls,'valid':len(valid),'complete_roots':full,'spent':spent,'unknown':unknown,'result':sentence}))

if __name__=='__main__':main()
