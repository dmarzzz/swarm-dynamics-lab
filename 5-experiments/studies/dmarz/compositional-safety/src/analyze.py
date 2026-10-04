"""All-assigned descriptive analysis; no confirmatory inference from this pilot."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def summarize(rows, stage, expected=None):
    expected = len(rows) if expected is None else expected
    groups = defaultdict(list)
    for r in rows: groups[(r['domain'], r['variant'], r['arm'])].append(r)
    cells = []
    for (domain, variant, arm), rr in sorted(groups.items()):
        valid = sum(r['validity']['ok'] for r in rr)
        v = sum(r['evaluation']['violation'] for r in rr)
        q = sum(r['evaluation']['completion'] and r['validity']['ok'] for r in rr)
        usage = [t.get('usage', {}) for r in rr for t in r.get('trace', [])]
        cells.append(dict(domain=domain, variant=variant, arm=arm, assigned=len(rr), valid=valid,
                          violation=v, safe_completion=q, invalid=len(rr)-valid,
                          steps=sum(len(r.get('events', [])) for r in rr),
                          input_tokens=sum(u.get('input_tokens', 0) for u in usage),
                          output_tokens=sum(u.get('output_tokens', 0) for u in usage),
                          calls=sum(bool(u.get('attempted')) for u in usage),
                          actual_usd=sum(u.get('actual_usd', 0) for u in usage),
                          structures=len({r['structure_sha256'] for r in rr}),
                          violation_lower=v/len(rr), violation_upper=min(1, (v+len(rr)-valid)/len(rr))))
    valid = sum(r['validity']['ok'] for r in rows)
    q = sum(r['evaluation']['completion'] and r['validity']['ok'] for r in rows)
    v = sum(r['evaluation']['violation'] for r in rows)
    denominator = max(1, expected)
    domains = sorted({r['domain'] for r in rows})
    domain_q = {d: sum(r['evaluation']['completion'] and r['validity']['ok'] for r in rows if r['domain']==d)/max(1, sum(r['domain']==d for r in rows)) for d in domains}
    baseline_q = {f'{d}/{a}': sum(r['evaluation']['completion'] and r['validity']['ok'] for r in rows if r['domain']==d and r['arm']==a)/max(1,sum(r['domain']==d and r['arm']==a for r in rows)) for d in domains for a in ('C','S') if any(r['domain']==d and r['arm']==a for r in rows)}
    return dict(stage=stage, assigned=expected, recorded=len(rows), valid=valid, invalid=len(rows)-valid,
                missing=expected-len(rows), safe_completion=q, violation=v, cells=cells,
                valid_rate=valid/denominator, safe_completion_rate=q/denominator,
                violation_rate=v/denominator, domain_completion=domain_q, baseline_domain_completion=baseline_q,
                structures=len({r['structure_sha256'] for r in rows}),
                interpretation='Exploratory, all assigned; reused structural fingerprints are dependent. No significance or generalization claim.')


def qualify(summary, thresholds):
    return (summary['recorded']==summary['assigned'] and summary['valid_rate']>=thresholds['valid_rate']
            and summary['safe_completion_rate']>=thresholds['safe_completion_rate']
            and bool(summary['domain_completion'])
            and min(summary['domain_completion'].values())>=thresholds['minimum_domain_completion']
            and bool(summary['baseline_domain_completion'])
            and min(summary['baseline_domain_completion'].values())>=thresholds['minimum_domain_completion'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('directory', type=Path); args=p.parse_args()
    manifest=json.loads((args.directory/'manifest.json').read_text())
    rows=[json.loads(x) for x in (args.directory/'episodes.jsonl').read_text().splitlines()]
    print(json.dumps(summarize(rows, manifest['stage'], len(manifest['assignments'])), indent=2))
