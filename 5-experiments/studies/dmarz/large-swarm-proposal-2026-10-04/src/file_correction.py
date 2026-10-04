"""File the correction via fd.py add while preserving historical provenance."""
from pathlib import Path
import copy
import os
import sys

base = Path(__file__).resolve().parents[1]
repo = base.parents[3]
sys.path.insert(0, str(repo / '.flightdeck'))
import fd
import artifacts_check as ac

os.chdir(repo)
aid = 'large-swarm-experiment-proposal-2026-10-04'
old = copy.deepcopy(ac.load_lock(str(repo)))
assert aid + '@1' in old['entries']
assert aid + '@2' not in old['entries']
old_statements = {p: p.read_bytes() for p in (repo / 'attestations').glob('*.intoto.json')}
original_fill = ac.fill_lock

def keep_history(folder, data, previous=None, host=None):
    result = original_fill(folder, data, previous, host)
    for key, value in old['entries'].items():
        assert key in result['entries']
        result['entries'][key] = value
    return result

ac.fill_lock = keep_history
original_write = fd.write_statements
original_pairs = fd.version_pairs

def write_new_only(folder, data, lock):
    # Preserve full lineage for the new statement without rewriting old ones.
    def new_pairs(all_data, all_lock):
        return [row for row in original_pairs(all_data, all_lock) if row[2] not in old['entries']]
    fd.version_pairs = new_pairs
    try:
        return original_write(folder, data, lock)
    finally:
        fd.version_pairs = original_pairs

fd.write_statements = write_new_only
args = ['add', '/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/large-swarm-experiment.canvas.tsx',
        '--id', aid, '--copy', '--strict',
        '--prompt', 'if we dont have a good eval then we shouldnt even do thiss, please dont take evals so laxily. we cant plan really without knowing what the eval will be',
        '--note', 'Withdraw the premature scale, model and cost recommendation. Record evaluation validity as unresolved and the prerequisite to any experiment recommendation; preserve v1 as history.']
inputs = [base / 'proposal.json', base / 'SETUP.md', base / 'src/build_review.py', Path(__file__),
          repo / 'tooling/agent-experiments/EXPERIMENT-SETUP.md',
          repo / 'artifacts/large-swarm-experiment-proposal-2026-10-04/large-swarm-experiment-proposal-2026-10-04-v1.tsx']
for path in inputs:
    args += ['--ingredient', str(path.relative_to(repo))]
assert fd.main(args) == 0
current = ac.load_lock(str(repo))
assert all(current['entries'][k] == v for k, v in old['entries'].items())
assert all(p.read_bytes() == raw for p, raw in old_statements.items())
print('Historical provenance and attestations preserved.')
