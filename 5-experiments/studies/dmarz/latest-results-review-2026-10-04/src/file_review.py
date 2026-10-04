"""File this review through fd.py add, preserving existing immutable provenance."""
from pathlib import Path
import copy, hashlib, json, os, sys
base=Path(__file__).resolve().parents[1]
repo=base.parents[3]
sys.path.insert(0,str(repo/'.flightdeck'))
import fd, artifacts_check as ac
artifact_id='latest-experiment-results-2026-10-04'
os.chdir(repo)
old=copy.deepcopy(ac.load_lock(str(repo)))
assert artifact_id+'@1' not in old['entries'], 'Already filed; do not create an accidental new version.'
attestations={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'attestations').glob('*.intoto.json')}
fill=ac.fill_lock
def preserve_history(folder,data,previous=None,host=None):
    result=fill(folder,data,previous,host)
    for key,entry in old['entries'].items():
        assert key in result['entries'], key
        result['entries'][key]=entry
    return result
# The stock refresh rehashes historical, mutable ingredients. Keep recorded
# facts for every pre-existing artifact; only the new artifact gets new facts.
ac.fill_lock=preserve_history
inputs=[base/'src/build_review.py',Path(__file__),base/'evidence.json',base/'inputs/sources.json']
inputs += [repo/x['local'] for x in json.loads((base/'inputs/sources.json').read_text())]
args=['add','/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/latest-experiment-results.canvas.tsx',
      '--id',artifact_id,'--type','doc','--title','Latest experiment results — 4 October 2026',
      '--prompt','can u review the latest results from our experiments?','--copy','--strict',
      '--note','Frozen evidence review through 08:11:40 UTC. Source reports and public hub state retained; selected arithmetic checked. No new experiments.']
for path in inputs: args += ['--ingredient',str(path.relative_to(repo))]
assert fd.main(args)==0
new=ac.load_lock(str(repo))
assert all(new['entries'][k]==v for k,v in old['entries'].items())
assert all(hashlib.sha256((repo/'attestations'/p).read_bytes()).hexdigest()==h for p,h in attestations.items())
print('Preserved',len(old['entries']),'existing provenance entries and all historical attestations.')

