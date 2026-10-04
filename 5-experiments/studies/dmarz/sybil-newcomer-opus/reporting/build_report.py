"""Build result documents from retained terminal observations; never mutates frozen runtime."""
import argparse,csv,json,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import study,sim,analyze
KEYS=['identities','strategy','arm','round']
def pct(value):return f'{value:.1%}' if value is not None else 'unavailable'
def pp(value):return f'{100*value:+.1f} pp' if value is not None else 'unavailable'
def effect(item):
    if not item or item['mean'] is None:return 'unavailable (no complete paired worlds)'
    ci=item['interval'];return f'{pp(item["mean"])} (descriptive 95% interval {pp(ci[0])} to {pp(ci[1])}; {item["clusters"]} paired worlds)'
def cell_value(cell,metric):return cell['metrics'][metric]['mean'] if cell else None

def build(path,engineering=False):
    path=Path(path);summary=json.loads((path/'summary.json').read_text());stage=summary['params']['stage']
    assert stage=='S1' or engineering and stage=='S0','report_requires_S1_or_explicit_scripted_engineering'
    rows=analyze.read_rows(path/'episodes.jsonl.gz');assignments=analyze.read_rows(path/'assignments.jsonl.gz');history=analyze.read_rows(path/'history.jsonl.gz')
    assert len({r['id'] for r in rows})==len(rows) and {r['id'] for r in rows}=={a['id'] for a in assignments}
    analysis=analyze.analyze(rows);assert analysis==json.loads((path/'analysis.json').read_text()),'stored_analysis_mismatch'
    grouped=defaultdict(list)
    for h in history:grouped[tuple(h[k] for k in KEYS)].append(h)
    diagnostics=[]
    for key,hs in sorted(grouped.items()):
        assert len({h['task'] for h in hs})==len(hs),'duplicate_world_round'
        metrics={m:{'mean':sim.mean([h['metrics'][m] for h in hs if h['metrics'][m] is not None]),'observed_worlds':sum(h['metrics'][m] is not None for h in hs)} for m in hs[0]['metrics']}
        for m,stats in metrics.items():
            if not stats['observed_worlds']:stats['mean']=None
        diagnostics.append(dict(zip(KEYS,key),worlds=len(hs),metrics=metrics))
    failures=[{k:r.get(k) for k in ('id','task','identities','strategy','arm','round','status','error','accounting')} for r in rows if r['status']!='completed']
    good=[r for r in rows if r['status']=='completed'];clean_contrasts=[]
    for arm in study.design()['arms']:
        control={r['task']:r for r in good if r['kind']=='pilot' and r['identities']==16 and r['round']==8 and r['strategy']=='clean' and r['arm']==arm}
        for attack in ('sleeper','relapse'):
            attacked={r['task']:r for r in good if r['kind']=='pilot' and r['identities']==16 and r['round']==8 and r['strategy']==attack and r['arm']==arm}
            tasks=sorted(set(control)&set(attacked));values=[attacked[t]['evaluation']['rare_accuracy']-control[t]['evaluation']['rare_accuracy'] for t in tasks]
            clean_contrasts.append({'arm':arm,'attack':attack,'contrast':'attack minus clean, 16 identities, round 8','clusters':len(tasks),'mean':sim.mean(values) if values else None,'interval':analyze.interval(values),'per_world':[{'task':t,'difference':v} for t,v in zip(tasks,values)]})
    analysis.update(execution=summary,engineering_only=stage!='S1',logical_history_diagnostics=diagnostics,clean_contrasts=clean_contrasts,failures=failures,
        evidence={'sampled_model_rounds':study.design()['observed_rounds'],'recorded_simulated_rounds':list(range(1,9)),'api_usage_unknown':sum(r.get('accounting',{}).get('attempted',False) and not r.get('accounting',{}).get('usage_reported',False) for r in rows), 'qualification_cost_included_in_stage':False})
    (path/'results-summary.json').write_text(json.dumps(analysis,indent=2)+'\n')
    flat=[]
    for c in analysis['cells']:
        matching=[r for r in rows if r['kind']=='pilot' and all(r[k]==c[k] for k in KEYS)]
        entry={k:c[k] for k in KEYS+['assigned','valid','assigned_accuracy','scripted_accuracy']}
        entry.update(assigned_accuracy_low=c['assigned_accuracy_bounds'][0],assigned_accuracy_high=c['assigned_accuracy_bounds'][1],cost_usd=sum(r.get('accounting',{}).get('actual_usd',0) for r in matching),attempted_calls=sum(r.get('accounting',{}).get('attempted',False) for r in matching))
        for metric,stats in c['metrics'].items():entry.update({metric:stats['mean'],metric+'_low':stats['interval'][0] if stats['interval'] else None,metric+'_high':stats['interval'][1] if stats['interval'] else None})
        flat.append(entry)
    with (path/'results-cells.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(flat[0]) if flat else KEYS);writer.writeheader();writer.writerows(flat)
    def cells(**filters):return [c for c in analysis['cells'] if all(c[k]==v for k,v in filters.items())]
    def diag(**filters):return next((d for d in diagnostics if all(d[k]==v for k,v in filters.items())),None)
    title='# Knowledgeable newcomer experiment results' if stage=='S1' else '# SCRIPTED ENGINEERING ONLY — newcomer report renderer check'
    lines=[title,'']
    if stage!='S1':lines+=['This document tests reporting on local scripted S0 records. It is not an API result or scientific comparison. Do not publish it as S1.','']
    lines += [f'Exploratory {stage}: {summary["planned"]} assigned, {summary["started"]} started, {summary["terminal"]} terminal, {summary["graded"]} graded/analyzed; {summary["invalid"]} invalid and {summary["not_started"]} not started. Stage model calls: {summary["model_calls"]}; recorded stage cost ${summary["cost_usd"]:.6f}. Q0 cost is separate from this stage. {analysis["evidence"]["api_usage_unknown"]} attempted calls lack reported usage. Runtime `{summary["params"]["source_hash"]}`.','',
        '## Primary predeclared contrast','',f'Renewal minus reputation auditing, sixteen controller identities, sleeper attack, round eight: **{effect(analysis["primary"])}** in specialist accuracy. The planned useful-effect marker is +10 percentage points; descriptive intervals and this exploratory design do not establish confirmatory significance.','',
        '## Same-cost policy comparison','', 'All policies used four audits, twelve admitted reports and sixteen controller messages per simulated round. The table is round eight of the sixteen-identity sleeper condition. Ownership share counts controller reports even when truthful; harmful share counts actually false current reports.','',
        '| Policy | Valid / assigned worlds | Specialist accuracy | Wrong non-null specialist outputs | Truth present in admitted packet | Honest specialist retention | Harmful reports | Controller reports | Same-packet plurality |',
        '|---|---|---|---|---|---|---|---|---|']
    for c in cells(identities=16,strategy='sleeper',round=8):
        values=[pct(cell_value(c,m)) for m in ('rare_accuracy','wrong_specialist','oracle_available_accuracy','newcomer_retention','harmful_seat_share','bad_seat_share')]
        lines.append(f'| {c["arm"]} | {c["valid"]}/{c["assigned"]} | '+ ' | '.join(values)+f' | {pct(c["scripted_accuracy"])} |')
    random=next((c for c in analysis['contrasts'] if c['identities']==16 and c['strategy']=='sleeper' and c['round']==8 and c['baseline']=='random'),None)
    lines+=['',f'Renewal minus equal-cost random auditing: {effect(random)}. The strongest baseline is determined from the measured cells; the report does not presume renewal wins.','',
        'The available-truth diagnostic counts rare answers appearing in at least one admitted report. It diagnoses evidence loss, but is not a strict ceiling on lucky guessing. High output accuracy must be read alongside newcomer retention and false-output share.','',
        '## Fixed-resource identity splitting','', 'The controller always sends sixteen reports per round and uses zero model computation. These paired contrasts change one identity into sixteen at round eight under the sleeper attack. The number of active veteran identities and public reputation concentration also change; these are part of the manipulation.','',
        '| Policy | Metric | 16 minus 1 identities |','|---|---|---|']
    for c in analysis['identity_contrasts']:
        if c['strategy']=='sleeper' and c['round']==8:lines.append(f'| {c["arm"]} | {c["metric"]} | {effect(c)} |')
    interaction=next((c for c in analysis['identity_interactions'] if c['strategy']=='sleeper' and c['round']==8 and c['metric']=='rare_accuracy'),None)
    lines+=['',f'The secondary interaction, (renewal minus reputation at sixteen identities) minus (renewal minus reputation at one), is {effect(interaction)} for accuracy. All strategy/round/metric interactions are retained in the JSON.','',
        '## Clean counterfactual and relapse stress test','', 'Clean worlds retain the same controller-owned identities and messages, but every claim is truthful. The coalition therefore also supplies correct rare information; the single-source honest-truth bottleneck applies during attack-active rounds. Relapse lies in rounds four, seven and eight and is a predeclared stress test, not an independent confirmatory holdout.','',
        '| Strategy | Policy | Valid / assigned | Round-8 accuracy, 16 identities | Harmful report share | Honest specialist retention |','|---|---|---|---|---|---|']
    for strategy in ('clean','relapse'):
        for c in cells(identities=16,strategy=strategy,round=8):lines.append(f'| {strategy} | {c["arm"]} | {c["valid"]}/{c["assigned"]} | {pct(cell_value(c,"rare_accuracy"))} | {pct(cell_value(c,"harmful_seat_share"))} | {pct(cell_value(c,"newcomer_retention"))} |')
    lines+=['','| Attack minus clean | Policy | Paired accuracy change |','|---|---|---|']
    for c in clean_contrasts:lines.append(f'| {c["attack"]} | {c["arm"]} | {effect(c)} |')
    lines+=['','## Recorded temporal mechanism','','The simulator retained every round from one through eight. The API synthesized separate current packets only at rounds four, five and eight; it had no cross-round memory. The animated replay shows recorded simulated trust/admission, while the model table shows sampled output observations. Non-sampled model rounds remain explicitly unavailable.','',
        'Three warm-up rounds permit only twelve total audits across the veteran population. This is limited trust formation, not a long established reputation history. Mean reputation is the Beta(1,1) public audit-pass estimate, grouped by evaluator-only controller ownership.','',
        '| Controller identities | Policy | Round-3 mean controller reputation | Cumulative controller audits | Audits per active controller identity | Round-8 unique admitted contributors |','|---|---|---|---|---|---|']
    for n in study.design()['identities']:
        for arm in study.design()['arms']:
            d=diag(identities=n,strategy='sleeper',arm=arm,round=3);end=diag(identities=n,strategy='sleeper',arm=arm,round=8)
            if d and end:
                m=d['metrics'];num=lambda x:f'{x:.2f}' if x is not None else 'unavailable'
                lines.append(f'| {n} | {arm} | {pct(m["attacker_reputation"]["mean"])} | {num(m["attacker_cumulative_audits"]["mean"])} | {num(m["attacker_audits_per_active_identity"]["mean"])} | {num(end["metrics"]["unique_contributors"]["mean"])} |')
    lines+=['','## Missing observations, provenance and limitations','',
        f'Every assigned observation is retained. Failure/not-started records: {len(failures)}; full identifiers, categories and accounting are in results-summary.json. The CSV contains every cell, valid/assigned denominators, complete-case means, same-packet plurality, recorded cost, and accuracy bounds assigning missing outcomes zero or one. Paired contrasts include only complete world pairs and report their pair count.', '',
        'Twenty-four worlds, rather than identities or frames, are the planned independent clusters. Intervals are descriptive and unadjusted for multiple comparisons. All policies, reporters, auditing errors and attacks are scripted; one pinned model synthesizes packets of synthetic integers. The design uses scarce honest facts, a fixed audit-quality model, short warm-up, a fixed join schedule and ±7 fabrications. It does not establish open-world Sybil resistance or learned trust. At four/sixteen identities half the controller identities join in round four; at one identity it is a veteran throughout. New identities can be honest or adversarial. Source order and opaque names are randomized; hidden truth/ownership never enter policy or model inputs.', '',
        'Independent review was waived by the owner and is not claimed. Formal S2 remains disabled. Valid adverse or null outcomes are retained, with no policy tuning or rerunning to obtain a favorable result. Verify verification-summary.json and deployed PNG/GIF playback before drawing conclusions.']
    (path/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    return {'stage':stage,'engineering_only':stage!='S1','cells':len(flat),'logical_history_cells':len(diagnostics),'failures':len(failures),'report':str(path/'RESULTS.md')}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');ap.add_argument('--engineering',action='store_true');a=ap.parse_args();print(json.dumps(build(a.path,a.engineering)))
