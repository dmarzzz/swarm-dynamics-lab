"""Receipt-paired descriptive analysis; no policy tuning or causal mind-reading."""
import argparse,collections,csv,json,random,statistics
from pathlib import Path
from policies import ARMS

def avg(xs):return sum(xs)/len(xs)
def interval(values):
    rng=random.Random(2026);draws=sorted(avg(rng.choices(values,k=len(values))) for _ in range(2000));return [draws[49],draws[1949]]
def analyze(blocks):
    result={'n_receipts':len(blocks),'interpretation':'Exploratory receipt-paired descriptive bootstrap; one validation corpus, not independent agent votes','arms':{},'contrasts':{}}
    for a in ARMS:
        vals=[b['arms'][a] for b in blocks]
        result['arms'][a]={'quality':avg([v['metrics']['quality'] for v in vals]),'regret':avg([v['metrics']['regret'] for v in vals]),'checks':avg([v['metrics']['checks'] for v in vals]),'bad_over_2pp':sum(v['metrics']['regret']>.02 for v in vals),'qa_helps_vs_confidence':sum(v['metrics']['quality']>b['arms']['confidence-only']['metrics']['quality']+1e-9 for v,b in zip(vals,blocks)),'qa_hurts_vs_confidence':sum(v['metrics']['quality']<b['arms']['confidence-only']['metrics']['quality']-1e-9 for v,b in zip(vals,blocks)),'utility':{str(c):avg([v['metrics']['quality']-c*v['metrics']['checks'] for v in vals]) for c in [0,.01,.02,.05]}}
    for a,b in [('swarm-adaptive','best-fixed'),('swarm-adaptive','decision-focused'),('swarm-adaptive','single-agent'),('swarm-adaptive','swarm-fixed'),('single-agent','best-fixed'),('decision-focused','best-fixed')]:
        diffs=[r['arms'][a]['metrics']['quality']-r['arms'][b]['metrics']['quality'] for r in blocks]
        result['contrasts'][f'{a} minus {b}']={'mean_quality_difference':avg(diffs),'bootstrap_95':interval(diffs),'better':sum(v>1e-9 for v in diffs),'worse':sum(v< -1e-9 for v in diffs),'tied':sum(abs(v)<=1e-9 for v in diffs)}
    result['oracle_quality']=avg([max(b['mode_scores'].values()) for b in blocks]);result['optimistic_budget_oracle']=avg([b['budget_oracle'] for b in blocks])
    result['adaptive_stopping']={'stopped_before_budget':sum(b['arms']['swarm-adaptive']['metrics']['checks']<2 for b in blocks),'saved_checks':sum(2-b['arms']['swarm-adaptive']['metrics']['checks'] for b in blocks),'worse_than_fixed':sum(b['arms']['swarm-adaptive']['metrics']['quality']<b['arms']['swarm-fixed']['metrics']['quality']-1e-9 for b in blocks),'better_than_fixed':sum(b['arms']['swarm-adaptive']['metrics']['quality']>b['arms']['swarm-fixed']['metrics']['quality']+1e-9 for b in blocks)}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args();blocks=[json.loads(s) for s in (a.run/'episodes.jsonl').read_text().splitlines()]
    assert len({b['id'] for b in blocks})==len(blocks)
    for b in blocks:
        assert set(b['arms'])==set(ARMS)
        for arm,r in b['arms'].items():
            assert r['valid'] and len(r['checks'])<=2
            assert len({(c['mode'],c['region']) for c in r['checks']})==len(r['checks'])
            assert abs(r['metrics']['quality']-b['mode_scores'][r['choice']])<1e-10
    result=analyze(blocks);receipts=json.loads((a.run/'receipts.json').read_text())
    result['runtime']={'physical_calls':len(receipts),'invalid':sum(not r['valid'] for r in receipts),'encoded_tokens':sum(r['encoded_tokens'] for r in receipts),'inference_s':sum(r['wall_s'] for r in receipts),'max_encoded_tokens':max(r['encoded_tokens'] for r in receipts),'logical_calls':{arm:sum(b['arms'][arm]['logical_calls'] for b in blocks) for arm in ARMS},'action_counts':dict(collections.Counter(r.get('choice') for r in receipts))}
    (a.run/'analysis.json').write_text(json.dumps(result,indent=2))
    with (a.run/'outcomes.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['receipt','arm','choice','quality','regret','checks','total_field_exact','logical_calls'])
        for b in blocks:
            for arm,r in b['arms'].items():w.writerow([b['id'],arm,r['choice'],*[r['metrics'][k] for k in ['quality','regret','checks','total_field_exact']],r['logical_calls']])
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
