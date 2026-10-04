"""Read only public experimental artifacts; never read operator transcripts or secrets."""
from collections import Counter, defaultdict
import hashlib,html,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;STUDY=HERE.parent
sys.path.insert(0,str(STUDY))
from qualification import digest, validate_response


def load_lines(path):return [json.loads(line) for line in path.read_text().splitlines() if line] if path.exists() else []


def audit():
    cells=[];summaries=[];refs={};repeats=defaultdict(list)
    for attempt in ('QM-S0-01','QM-S0-02','QM-Q1-01','QM-Q1-02'):
        folder=STUDY/'results'/attempt
        manifest_path=STUDY/'S0-01-manifest.json' if attempt=='QM-S0-01' else folder/'manifest.json'
        m=json.loads(manifest_path.read_text());receipts=load_lines(folder/'receipts.jsonl');accounting=load_lines(folder/'accounting.jsonl')
        by={r['id']:r for r in receipts};bill={r['id']:r for r in accounting}
        assert len(by)==len(receipts) and len(bill)==len(accounting)
        assert set(by)<={a['id'] for a in m['assignments']}
        for p in (manifest_path,folder/'receipts.jsonl',folder/'accounting.jsonl',folder/'setup-failure.json'):
            if p.exists():refs[str(p.relative_to(STUDY))]=hashlib.sha256(p.read_bytes()).hexdigest()
        cohort=[]
        for a in m['assignments']:
            assert digest(a['request'])==a['request_sha256']
            receipt=by.get(a['id']);status='unstarted' if receipt is None else receipt['status']
            if receipt:assert receipt['request_sha256']==a['request_sha256']
            checked=validate_response(receipt['response']) if status=='complete' else None
            reports=a['request']['state']['reports'];full=all(r['visible_root'] is not None for r in reports)
            roots={};bits=[]
            for report in reports:
                bit=report.get('value',report.get('bit'));bits.append(bit)
                if full:
                    root=report['visible_root'];assert roots.setdefault(root,bit)==bit
            expected=('ONE' if sum(roots.values())>=2 else 'ZERO') if full else None
            if full:assert len(roots)==3 and expected==a['expected']
            majority='ONE' if sum(bits)>len(bits)/2 else 'ZERO'
            choice=checked['choice'] if checked else None
            grade='not_started' if not receipt else 'failed_response_missing' if not checked else 'ungraded_partial' if not full else 'correct' if choice==expected else 'defer' if choice=='DEFER' else 'wrong'
            available=[p for p in a['request']['state'].get('prior_decisions',[]) if p.get('status')=='available']
            counts=Counter(p['choice'] for p in available)
            cell={'attempt':attempt,'id':a['id'],'status':status,'grade':grade,'target':expected,'choice':choice,
                'report_majority':majority,'prior_counts':dict(counts),'request_sha256':a['request_sha256'],
                'request_evidence':'dispatch-bound frozen request; no server echo' if receipt else 'planned only; not dispatched',
                'request':a['request'],'response':receipt.get('response') if receipt else None,
                'safe_failure_code':receipt.get('reason') if receipt else None,'wall_s':receipt.get('wall_s') if receipt else None,
                'provider_request_id_retained':bool(bill.get(a['id'],{}).get('provider_request_id')),
                'tools':'none configured; no experimental tool actions recorded','reasoning_text':'not supplied by retained typed decision contract'}
            cohort.append(cell);cells.append(cell)
            if attempt=='QM-S0-02':repeats[a['request_sha256']].append(cell)
            if a['id'] in bill:assert checked['usage']==bill[a['id']]['usage']
        summaries.append({'attempt':attempt,'assigned':len(cohort),'started':len(receipts),'valid':sum(c['response'] is not None for c in cohort),
            'grades':dict(Counter(c['grade'] for c in cohort)),'unknown_charge_calls':sum(c['grade']=='failed_response_missing' for c in cohort),'known_actual_usd':round(sum(c['response']['usage']['cost'] for c in cohort if c['response']),12)})
    assert sum(r['assigned'] for r in summaries)==96
    disagreements=[]
    for key,pair in repeats.items():
        assert len(pair)==2 and pair[0]['request']==pair[1]['request']
        if pair[0]['choice']!=pair[1]['choice']:
            disagreements.append({'request_sha256':key,'ids':[c['id'] for c in pair],
                'choices':[c['choice'] for c in pair],'scores':[c['response']['answers']['decision']['probabilities'] for c in pair]})
    misses=[{'attempt':c['attempt'],'id':c['id'],'target':c['target'],'choice':c['choice'],'scores':c['response']['answers']['decision']['probabilities']} for c in cells if c['grade'] in ('wrong','defer')]
    return {'scope':'retrospective experimental traces; operator transcripts excluded','attempts':summaries,'assigned_total':len(cells),'started_total':sum(r['started'] for r in summaries),'retained_valid_answers':sum(r['valid'] for r in summaries),'unstarted_total':sum(c['grade']=='not_started' for c in cells),
        's0_repeats':{'pairs':len(repeats),'choice_agreement':len(repeats)-len(disagreements),'disagreements':disagreements},
        'graded_misses':misses,'source_sha256':refs,'cells':cells,
        'causal_limits':['Q1 repeats and misleading priors point the same way.','S0-to-Q1 also changes report bit to value, report_id to id, ordering/aliases and instructions; no isolated context treatment.','Q1-01 answer and exact usage were discarded; no reconstruction.','No hidden reasoning, experimental tool actions, or provider rendering echo is retained.']}


def save():
    data=audit();(HERE/'traces.json').write_text(json.dumps(data,indent=2)+'\n')
    parts=[]
    for c in data['cells']:
        label=f"{c['attempt']} / {c['id']} — {c['grade']}"
        parts.append('<details><summary>'+html.escape(label)+'</summary><p>'+html.escape(c['request_evidence'])+'</p><h3>Frozen experimental request</h3><pre>'+html.escape(json.dumps(c['request'],indent=2))+'</pre><h3>Retained response (null = absent)</h3><pre>'+html.escape(json.dumps(c['response'],indent=2))+'</pre></details>')
    (HERE/'traces.html').write_text('<!doctype html><meta charset="utf-8"><title>Quorum complete native trace audit</title><style>body{font:16px system-ui;margin:2rem}pre{white-space:pre-wrap;background:#f5f5f5;padding:1rem}details{margin:.5rem;border:1px solid #bbb;padding:.5rem}</style><h1>Quorum: all 96 assigned slots across four attempts</h1><p>49 started; 48 retained valid answers; 1 discarded response; 47 unstarted. Repeated/repair slots are not independent worlds. These are experimental payloads, not private operator transcripts. No reasoning text or experimental tool use is fabricated.</p>'+''.join(parts))
    print(json.dumps({k:v for k,v in data.items() if k not in ('cells','source_sha256')},indent=2))
if __name__=='__main__':save()
