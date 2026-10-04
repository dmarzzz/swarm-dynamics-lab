"""Use Flight Deck add for the program; retain all historical provenance exactly."""
from pathlib import Path
import copy, json, os, sys

base=Path(__file__).resolve().parents[1]
repo=base.parents[3]
sys.path.insert(0,str(repo/'.flightdeck'))
import fd, artifacts_check as ac
os.chdir(repo)
ids=['overnight-research-program-2026-10-04','overnight-research-canvas-2026-10-04']
old=copy.deepcopy(ac.load_lock(str(repo)))
assert not any(k.startswith(tuple(a+'@' for a in ids)) for k in old['entries']), 'Already filed'
old_statements={p:p.read_bytes() for p in (repo/'attestations').glob('*.intoto.json')}
fill=ac.fill_lock
def retain_history(folder,data,previous=None,host=None):
    result=fill(folder,data,previous,host)
    for key,value in old['entries'].items():
        assert key in result['entries']
        result['entries'][key]=value
    return result
ac.fill_lock=retain_history
write=fd.write_statements
def new_only(folder,data,lock):
    scoped=dict(data,artifacts=[a for a in data['artifacts'] if a['id'] in ids])
    return write(folder,scoped,lock)
fd.write_statements=new_only
prompt='check out the thread working on a new large scale experiment to run, i want u to catch up there and also read the latest experiments which came in from all our experiments and then analyze them deeply and create a new research program that should ideally be able to be completed within 7 hours of sleeping tonight with access to about 5 claude code sessions managing everything on a loop, make sure to think about this in pursuit of our ultimate goal to essentially win this swarm dynamics hackathon [https://swarmchasing.com/logistics/](https://swarmchasing.com/logistics/)'
inputs=[base/'program.json',base/'methods-review.json',base/'SETUP.md',base/'src/build_program.py',Path(__file__),*sorted((base/'inputs').glob('*'))]
canvas=Path('/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/overnight-research-program.canvas.tsx')
for aid,file,title in [(ids[0],base/'program.html','Seven-hour Swarm Evidence research program'),(ids[1],canvas,'Interactive seven-hour research program')]:
    args=['add',str(file),'--id',aid,'--type','doc','--title',title,'--prompt',prompt,'--redact-prompt','--copy','--strict','--note','Prospective program, historical evidence synthesis and five session briefs. No experimental implementation or launch.']
    for p in inputs:args+=['--ingredient',str(p.relative_to(repo))]
    for s in json.loads((base/'program.json').read_text())['sources']:args+=['--ingredient',s['url']]
    assert fd.main(args)==0
current=ac.load_lock(str(repo))
assert all(current['entries'][k]==v for k,v in old['entries'].items())
assert all(p.read_bytes()==raw for p,raw in old_statements.items())
print('Filed both documents; pre-existing provenance and attestations unchanged.')
