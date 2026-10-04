"""File the proposal through fd.py add without rewriting historical provenance."""
from pathlib import Path
import copy,hashlib,json,os,sys
base=Path(__file__).resolve().parents[1];repo=base.parents[3]
sys.path.insert(0,str(repo/'.flightdeck'))
import fd,artifacts_check as ac
os.chdir(repo)
aid='large-swarm-experiment-proposal-2026-10-04'
old=copy.deepcopy(ac.load_lock(str(repo)))
assert not any(k.startswith(aid+'@') for k in old['entries'])
old_statements={p:p.read_bytes() for p in (repo/'attestations').glob('*.intoto.json')}
original_fill=ac.fill_lock
def keep_history(folder,data,previous=None,host=None):
    result=original_fill(folder,data,previous,host)
    for key,value in old['entries'].items():
        assert key in result['entries']
        result['entries'][key]=value
    return result
ac.fill_lock=keep_history
original_write=fd.write_statements
def write_new_only(folder,data,lock):
    scoped=dict(data,artifacts=[a for a in data['artifacts'] if a['id']==aid])
    return original_write(folder,scoped,lock)
fd.write_statements=write_new_only
inputs=[base/'proposal.json',base/'SETUP.md',base/'src/build_review.py',Path(__file__),*sorted((base/'inputs').glob('*'))]
args=['add',"/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/large-swarm-experiment.canvas.tsx",'--id',aid,'--type','doc',
      '--title','A larger active-evidence swarm experiment',
      '--prompt','can u think of what experiment we could run from all of these on a much larger scale, potentially even using multiple simulation servers.',
      '--note','Exploratory proposal and conditional cost calculator. Credential excluded from the quoted request excerpt; no experimental calls or resources launched.',
      '--copy','--strict']
for p in inputs:args += ['--ingredient',str(p.relative_to(repo))]
for source in json.loads((base/'proposal.json').read_text())['plan']['sources']:
    if source['url'].startswith('https://'):args += ['--ingredient',source['url']]
assert fd.main(args)==0
current=ac.load_lock(str(repo))
assert all(current['entries'][k]==v for k,v in old['entries'].items())
assert all(p.read_bytes()==raw for p,raw in old_statements.items())
print('Historical provenance and attestations preserved.')

