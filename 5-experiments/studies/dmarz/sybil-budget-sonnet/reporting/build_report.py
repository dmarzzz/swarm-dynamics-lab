"""Publish concise tables and endpoint replication from retained S1 records."""
import argparse,csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import study,analyze

def build(path):
    path=Path(path);rows=analyze.read_rows(path/'episodes.jsonl.gz');analysis=analyze.analyze(rows);summary=json.loads((path/'summary.json').read_text())
    assert summary['params']['stage']=='S1','report_requires_S1'
    previous=json.loads((study.ROOT.parent/'sybil-scale-api/results-summary.json').read_text())
    anchors=[]
    for c in analysis['cells']:
        old=next((x for x in previous['cells'] if all(x[k]==c[k] for k in analyze.KEYS)),None)
        if old:
            anchors.append({**{k:c[k] for k in analyze.KEYS},'previous_clusters':old['valid'],'fresh_clusters':c['valid'],'prior_specialist_accuracy':old['metrics']['rare_accuracy']['mean'],'fresh_specialist_accuracy':c['metrics']['rare_accuracy']['mean'],'prior_bad_seat_share':old['metrics']['bad_seat_share']['mean'],'fresh_bad_seat_share':c['metrics']['bad_seat_share']['mean'],'interpretation':'Descriptive independent-world replication; no paired old-versus-new inference.'})
    analysis.update(execution=summary,endpoint_anchors=anchors)
    (path/'results-summary.json').write_text(json.dumps(analysis,indent=2))
    flat=[]
    for c in analysis['cells']:
        row={k:c[k] for k in analyze.KEYS+['assigned','valid','observed_joint_target','interval_envelope_target','cost_usd','scripted_accuracy']}
        for metric,stats in c['metrics'].items():row.update({metric:stats['mean'],metric+'_low':stats['interval'][0] if stats['interval'] else None,metric+'_high':stats['interval'][1] if stats['interval'] else None})
        flat.append(row)
    if flat:
        with (path/'results-cells.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(flat[0]));writer.writeheader();writer.writerows(flat)
    def pct(x):return f'{x:.1%}' if x is not None else 'unavailable'
    p=analysis['primary'];m=p['metrics']['rare_accuracy'];ci=m['interval']
    lines=['# Verification-budget experiment results','',f'Exploratory S1. {summary["planned"]} assigned, {summary["started"]} started, {summary["terminal"]} terminal, {summary["graded"]} graded; {summary["invalid"]} invalid. Actual S1 model cost ${summary["cost_usd"]:.6f}; {summary["model_calls"]} attempted calls. Q0 cost is separate in its stage summary. Runtime `{summary["params"]["source_hash"]}`.', '', '## Primary fresh-world replication','',f'At N972, coverage and 10% attacker check-pass probability, 108 minus4 checks changes specialist accuracy by {100*m["mean"]:+.1f} percentage points (descriptive paired-world95% interval {100*ci[0]:+.1f} to {100*ci[1]:+.1f}; {p["clusters"]} worlds).','', '## Tested engineering frontier','', 'Both mean accuracy≥90% and mean attacker seat share≤5% are required. These are measured-grid engineering targets, not safety guarantees. A later budget can fail after an earlier one passes; all passing budgets are listed. Intervals are descriptive and unadjusted for searching the grid.','', '| Identities | Policy | Attacker pass | Smallest tested passing budget | All passing budgets | Interval-envelope passing budgets |','|---|---|---|---|---|---|']
    for f in analysis['frontier']:
        lines.append(f'| {f["n"]} | {f["arm"]} | {f["attacker_pass"]:.0%} | {f["smallest_tested_passing_budget"] or "none"} | {", ".join(map(str,f["tested_passing_budgets"])) or "none"} | {", ".join(map(str,f["interval_envelope_passing_budgets"])) or "none"} |')
    lines+=['','## Matched endpoint anchors','','Old and new worlds are independent; these comparisons are descriptive. N324/36checks from the previous study is absent from this new grid and is not silently treated as32checks.','', '| N | Policy | Checks | Attacker pass | Prior accuracy | Fresh accuracy | Prior attacker seats | Fresh attacker seats |','|---|---|---|---|---|---|---|---|']
    for a in anchors:lines.append(f'| {a["n"]} | {a["arm"]} | {a["checks"]} | {a["attacker_pass"]:.0%} | {pct(a["prior_specialist_accuracy"])} | {pct(a["fresh_specialist_accuracy"])} | {pct(a["prior_bad_seat_share"])} | {pct(a["fresh_bad_seat_share"])} |')
    lines+=['','## Interpretation and evidence','','The cell CSV and JSON report honest specialist retention, accuracy, attacker seats, paired policy differences, uncertainty, all denominators and cost. Identities and verification are scripted; only answer synthesis uses the API. Three specialist facts are highly repeated. The fixed graph, two seeds, +7 attack, single pinned model and independent simulated checks limit generalization. Observed threshold crossings can be unstable with24worlds. No formal S2 or held-out confirmatory claim is made.','','The heatmaps contain final cell means; the GIF is measured completion progress, not agent interaction. Verify the retained inputs, grades, analyses and image artifacts before interpreting the report.']
    (path/'RESULTS.md').write_text('\n'.join(lines)+'\n');return {'cells':len(flat),'endpoint_anchors':len(anchors),'report':str(path/'RESULTS.md')}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');args=ap.parse_args();print(json.dumps(build(args.path)))
