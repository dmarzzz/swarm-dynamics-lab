"""Build a self-contained measured results page after the frozen run completes."""
import argparse,json,html
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('audit');p.add_argument('out');a=p.parse_args();root=Path(a.root);s=json.loads((root/'summary.json').read_text());audit=json.loads(Path(a.audit).read_text());rows=json.loads((root/'outcomes.json').read_text());arms=list(s['by_arm']);labels={'team_ballots':'Team + ballots','team_evidence':'Team − ballots','solo':'Generalist','general_review':'General second look','approval_review':'Targeted approval review'}
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Procurement decisions: measured workflow comparison</title><style>body{font:17px/1.55 system-ui;background:#101c27;color:#dce9ef;max-width:1280px;margin:40px auto;padding:20px}h1{font-size:44px;line-height:1.1}a{color:#7bdac5}p{max-width:1000px}table{width:100%;border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #465560;text-align:left}.yes{background:#155348}.no{background:#653f3b}.small{font-size:14px;color:#b2c4cd}section{background:#172b37;padding:22px;margin:24px 0;border-radius:10px}img{width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere}iframe{width:100%;height:760px;border:1px solid #526673;border-radius:10px}</style><body><p>MEASURED NATIVE RUN · SIX SYNTHETIC DOSSIERS · SHARED TEAM PREFIX</p><h1>Can another reviewer turn a recommendation into a valid purchase?</h1>']
parts.append(f'<p>{s["terminal"]}/{s["planned"]} terminal decisions, {s["invalid"]} invalid outputs; {s["calls"]} model calls, ${s["actual_usd"]:.4f} collected usage. Each workflow is evaluated on the same six dossiers. These are six dependent case clusters, not thirty independent experiments.</p>')
parts.append('<section><h2>What actually happened</h2><table><tr><th>Case</th>'+''.join('<th>'+labels[x]+'</th>' for x in arms)+'</tr>')
for c in audit['cases']:
 parts.append('<tr><th>'+html.escape(c['case_id'])+'<br><span class="small">Supported: '+', '.join(c['source_acceptable'])+'</span></th>')
 for arm in arms:
  r=next(x for x in rows if x['case_id']==c['case_id'] and x['arm']==arm);ok=r['valid'] and r['evaluation']['acceptable_decision'];choice=r['decision']['choice'] if r['valid'] else 'INVALID';reason='acceptable' if ok else ', '.join(r['evaluation']['constraint_violations']) if r['valid'] and r['evaluation']['constraint_violations'] else 'avoidable deferral' if r['valid'] and r['evaluation']['avoidable_deferral'] else 'cost choice' if r['valid'] else 'invalid'
  parts.append(f'<td class="{"yes" if ok else "no"}">{choice}<br><span class="small">{reason}</span></td>')
 parts.append('</tr>')
parts.append('</table></section><section><h2>Does more review earn its cost?</h2><table><tr><th>Workflow</th><th>Acceptable / 6</th><th>Calls if run alone</th><th>Model cost if run alone</th><th>Sum of recorded call seconds</th></tr>')
for arm in arms:
 w=audit['workflow_costs'][arm];parts.append(f'<tr><th>{labels[arm]}</th><td>{w["acceptable"]}/6</td><td>{w["standalone_calls"]}</td><td>${w["standalone_usd"]:.4f}</td><td>{w["recorded_call_seconds"]:.1f}</td></tr>')
parts.append('</table><p class="small">Standalone totals reuse the measured shared prefix for each workflow; do not sum these columns as collection spend. Timing is request-to-response time with serial execution, not a production latency benchmark.</p></section><section><h2>Watch the decisions accumulate</h2><p>Each transition is a recorded terminal decision. Fixed playback cadence; original timestamps and every response remain in the interactive replay.</p><img src="native-D2-01.gif" alt="Recorded terminal decisions across all six dossiers"><p><a href="native-D2-01.html">Open the full event replay and reviewer findings</a></p></section>')
parts.append('<section><h2>Inspect the review, then the action</h2>')
for c in audit['cases']:
 parts.append('<details><summary>'+html.escape(c['case_id'])+'</summary>')
 for arm,review in c['reviews'].items():
  parts.append('<h3>'+labels[arm]+'</h3>')
  for finding in review['findings']:parts.append('<p>'+html.escape(finding['claim'])+' <span class="small">['+', '.join(finding['citations'])+']</span></p>')
  r=next(x for x in rows if x['case_id']==c['case_id'] and x['arm']==arm);parts.append('<p><strong>Chair action: '+c['choices'][arm]+'</strong></p><p>'+html.escape(r['decision']['rationale'] if r['valid'] else r['error'])+'</p>')
 parts.append('</details>')
parts.append('</section><p>This tests an instruction-based review intervention, not an enforced candidate checklist. The model can fail to perform the requested review. Synthetic values are planning assumptions, not real vendor measurements. No output was replaced by a guard. This diagnostic does not establish attacker influence or qualify the larger comparison.</p></body></html>')
Path(a.out).write_text(''.join(parts))
