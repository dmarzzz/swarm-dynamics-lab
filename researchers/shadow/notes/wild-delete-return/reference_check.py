#!/usr/bin/env python3
"""Independent scan-based recomputation from raw sources; no analyzer imports.

Same author, separate implementation, not independent researcher review.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import random


def parse_time(row):
    value=row.get('time')
    return datetime.fromisoformat(value.replace('Z','+00:00')).timestamp() if value else None


def clock_error(row):
    if parse_time(row) is None:
        return 'missing_time'
    if row.get('time_grade') not in ['reqlog','rclog']:
        return 'ineligible_time_grade'
    uncertainty=row.get('uncertainty_seconds')
    if type(uncertainty) not in [int,float] or not (0<=uncertainty<=1):
        return 'ineligible_uncertainty'
    return None


def date_text(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat().replace('+00:00','Z') if t is not None else None


def read(path):
    with gzip.open(path,'rt') as stream:
        return [json.loads(line) for line in stream]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',type=Path,required=True)
    ap.add_argument('--results',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    if args.out.exists():
        raise SystemExit('Refusing to replace a reference receipt')
    events=read(args.data/'events.jsonl.gz')
    revisions=read(args.data/'revisions.jsonl.gz')
    assert len({r['event_id'] for r in events})==len(events)
    assert len({r['rev_id'] for r in revisions})==len(revisions)
    deletes=defaultdict(list)
    for e in events:
        if e.get('event_type')=='delete' and e.get('success_observed') is True and e.get('page_key'):
            deletes[e['page_key']].append(e)
    saved=defaultdict(list)
    for r in revisions:
        if r.get('page_key') and clock_error(r) is None:
            saved[r['page_key']].append(parse_time(r))
    all_times=[t for group in saved.values() for t in group]
    low,high=min(all_times),max(all_times)
    actual=[]
    for page, history in deletes.items():
        if any(parse_time(e) is None for e in history):
            t=None
            reason='unknown_first_deletion_missing_time'
        else:
            first=sorted(history,key=lambda e:(parse_time(e),e['event_id']))[0]
            t=parse_time(first)
            reason=clock_error(first)
        if reason is None and (t-1800<low or t+1800>high):
            reason='primary_release_edge'
        a={'page_sha256':hashlib.sha256(page.encode()).hexdigest(),
           'first_delete_time':date_text(t),'deletion_day':date_text(t)[:10] if t is not None else None,
           'successful_delete_events_for_page':len(history),'eligible':reason is None,
           'exclusion':reason,'windows':{}}
        if reason is None:
            for horizon in [300,1800,3600]:
                if t-horizon<low or t+horizon>high:
                    a['windows'][str(horizon)]={'eligible':False,'exclusion':'secondary_release_edge'}
                else:
                    before=[s for s in saved[page] if t-horizon<=s<t-60]
                    after=[s for s in saved[page] if t+60<s<=t+horizon]
                    a['windows'][str(horizon)]={'eligible':True,'before':len(before),'after':len(after),
                       'difference':len(after)-len(before),'any_return':bool(after),
                       'first_return_latency_seconds':min(after)-t if after else None}
        actual.append(a)
    actual.sort(key=lambda a:a['page_sha256'])
    expected=json.loads((args.results/'assignments.json').read_text())
    assert actual==expected, 'Full assignment/eligibility/window table mismatch'
    summary=json.loads((args.results/'summary.json').read_text())
    primary=[a for a in actual if a['eligible']]
    total_before=sum(a['windows']['1800']['before'] for a in primary)
    total_after=sum(a['windows']['1800']['after'] for a in primary)
    metrics=summary['window_results']['1800']
    assert (len(primary),total_before,total_after)==(metrics['pages'],metrics['before'],metrics['after'])
    # Recompute cluster bootstrap via cluster-index draws, rather than analyzer's group draws.
    dates=sorted({a['deletion_day'] for a in primary})
    ci=None
    if len(dates)>=5 and len(primary)>=10:
        ns=[sum(a['deletion_day']==d for a in primary) for d in dates]
        ds=[sum(a['windows']['1800']['difference'] for a in primary if a['deletion_day']==d) for d in dates]
        rng=random.Random(20261004)
        bootstrap=[]
        for _ in range(5000):
            indices=[rng.randrange(len(dates)) for _ in dates]
            bootstrap.append(sum(ds[i] for i in indices)/sum(ns[i] for i in indices))
        bootstrap.sort()
        ci=[]
        for p in [.025,.975]:
            x=(len(bootstrap)-1)*p
            k=int(x)
            ci.append(bootstrap[k]*(1-(x-k))+bootstrap[min(k+1,len(bootstrap)-1)]*(x-k))
        assert all(abs(a-b)<1e-12 for a,b in zip(ci,metrics['day_cluster_bootstrap_95_interval']))
    else:
        assert metrics['day_cluster_bootstrap_95_interval'] is None
    hashes={name:hashlib.sha256((args.data/name).read_bytes()).hexdigest() for name in ('events.jsonl.gz','revisions.jsonl.gz')}
    assert hashes==summary['provenance']['input_sha256']
    receipt={'status':'pass','scope':'Full raw-to-assignment recomputation plus primary arithmetic and bootstrap',
      'review_independence':'Separate implementation, same author; not independent peer review',
      'selected_page_records_matched':len(actual),'eligible_pages':len(primary),
      'before':total_before,'after':total_after,'day_cluster_bootstrap_95_interval':ci,
      'input_sha256':hashes,'reference_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
