#!/usr/bin/env python3
"""Generate prospective specs before any calls. Never overwrite an existing spec."""
import json
from pathlib import Path
import factory as f

def main():
    rows=[
      ('split-sonnet-linked-strong','Does Sonnet reproduce the informative-check identity-splitting contrast?', 'ring2',.1,12,'positive'),
      ('split-sonnet-linked-weak','Does unreliable verification reverse the Sonnet identity-splitting contrast?', 'ring2',.9,12,'negative'),
      ('split-sonnet-no-links-strong','Does the informative-check result survive removing free attacker-internal links?', 'none',.1,12,'positive'),
      ('split-sonnet-no-links-weak','Does the unreliable-check reversal survive removing free attacker-internal links?', 'none',.9,12,'negative'),
      ('split-sonnet-four-checks','Does the informative-check contrast survive a four-check verification budget?', 'ring2',.1,4,'positive')]
    paths=[f.ROOT/'factory.py', f.PARENT/'src/sim.py',f.PARENT/'src/study.py',f.PARENT/'src/provider.py',f.PARENT/'design.yaml']
    hashes={str(p.relative_to(f.REPO)):f.sha(p) for p in paths}
    for ident,title,links,rate,checks,direction in rows:
        p=f.ROOT/'specs'/f'{ident}.json'
        if p.exists(): raise SystemExit('Refusing to overwrite '+str(p))
        s=dict(id=ident,title=title,question=title,owner='shadow/sol-factory',created_at=f.now(),
            authority='Shadow Wave 4 item 16: exploratory extensions, not accepted hypotheses; no independent review claimed.',
            source_sha256=hashes,route='anthropic-pool',model='claude-sonnet-4-6',max_paid_usd=0,
            max_calls=204,concurrency=4,failure_stop=3,deadline_utc='2026-10-04T22:00:00Z',
            internal_links=links,attacker_pass=rate,checks=checks,expected_direction=direction,
            roots={'ring':list(range(8233,8257)),'community':list(range(8351,8375))},
            dispatch_seed=20261004,bootstrap_draws=10000,
            prior='Dmarz sybil-split-opus, primary +41.0 pp; unreliable-check reversal -52.8 pp. Same-family Sonnet follow-up, not a second-family replication.',
            protocol='12 clean fixtures (one root/family x six shapes), all exact required; then 48 parent comparison roots x k={1,27} x policy={degree,coverage}. No retries, no optional sample-size extension, no outcome replacement. Distinct-packet calls are not deduplicated.',
            metric='Mean over graph-family means of paired root difference-in-differences in rare_wrong. 10000 within-family root bootstrap draws, seed 20261004, percentile 95% interval. Missing outcomes bounded [0,1] before signed contrasts.',
            classification='finding only if all 204 calls valid, Q passed, and entire directional CI exceeds useful magnitude 0.10; otherwise complete run negative, incomplete lead. Five exploratory, unadjusted tests, not confirmatory claims.',
            interpretation='This small synthetic robustness check extends the parent result without claiming a novel Sybil defense. Removing internal links addresses an explicit confound in the parent review.' if links=='none' else 'A directional replication strengthens only the scoped synthetic mechanism; reversal or nonreplication is reported equally. No universal superiority of coverage is implied.',
            novelty='Incremental replication/sensitivity analysis; the parent pre-run review already notes a scripted no-links attenuation. No novelty claim.',
            limits=['Parent root reuse and synthetic worlds','Model and request configuration change together','Reduced 12-fixture competence screen','Graph families are equally weighted, not random real swarms','No formal prior-art/hypothesis gate approval','No paid fallback, even if pool unavailable'])
        f.dump(p,s)
    f.dump(f.ROOT/'queue.json',dict(specs=[r[0] for r in rows],hard_paid_cap_usd=20,paid_routes_enabled=False))
if __name__=='__main__':main()
