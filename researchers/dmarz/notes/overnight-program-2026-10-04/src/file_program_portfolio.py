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
assert all(a+'@3' in old['entries'] and a+'@4' not in old['entries'] for a in ids), 'Expected unfiled v4'
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
prompt='honestly im looking for maybe one new set of experiment line which is very well thought out and ran at a large scale, then probably 3 more lines which atleast have some conenction and advance some of the work of our other experiments to study swarm dynamcis\ni really want one which exapnds on the will they sybil under rules and make it much larger and a bit more complex'
inputs=[base/'program.json',base/'methods-review-v4.json',base/'SETUP.md',base/'src/build_program.py',base/'src/build_program_portfolio.py',base/'selected-model.json',Path(__file__),*sorted((base/'inputs').glob('*'))]
canvas=Path('/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/overnight-research-program.canvas.tsx')
for aid,file,title in [(ids[0],base/'program.html','Four-line research program: 180-agent Sybil market flagship'),(ids[1],canvas,'Four-line interactive research program')]:
    args=['add',str(file),'--id',aid,'--type','doc','--title',title,'--prompt',prompt,'--copy','--strict','--note','Prospective v4: large native Sybil-under-rules market plus trust, verification and memory follow-ups; 8,112 total call ceiling. No experiments launched.']
    for p in inputs:args+=['--ingredient',str(p.relative_to(repo))]
    for s in json.loads((base/'program.json').read_text())['sources']:args+=['--ingredient',s['url']]
    assert fd.main(args)==0
current=ac.load_lock(str(repo))
assert all(current['entries'][k]==v for k,v in old['entries'].items())
assert all(p.read_bytes()==raw for p,raw in old_statements.items())
print('Filed both documents; pre-existing provenance and attestations unchanged.')
