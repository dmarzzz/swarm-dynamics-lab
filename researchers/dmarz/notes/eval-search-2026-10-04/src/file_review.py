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
aid = 'evaluation-shortlist-2026-10-04'
old = copy.deepcopy(ac.load_lock(str(repo)))
assert not any(key.startswith(aid + '@') for key in old['entries'])
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
args = ['add', '/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/evaluation-shortlist.canvas.tsx',
        '--id', aid, '--type', 'doc', '--title', 'Existing evaluations: suitability and scorer audit', '--copy', '--strict',
        '--prompt', 'look for those',
        '--note', 'Primary-source benchmark shortlist with pinned evaluator inspection and reproducible offline counterexamples. No paid model runs or deployment; no claim of qualified experiment readiness.']
inputs = [base / 'review.json', base / 'SETUP.md', base / 'fixture-audit.json',
          base / 'src/build_review.py', base / 'src/audit_fixtures.py', Path(__file__),
          *sorted((base / 'inputs').glob('*'))]
for path in inputs:
    args += ['--ingredient', str(path.relative_to(repo))]
import json
review = json.loads((base / 'review.json').read_text())
urls = {s['url'] for c in review['candidates'] for s in c['sources']}
urls.update(c['source'] for c in review['localComponents'])
for url in sorted(urls):
    args += ['--ingredient', url]
assert fd.main(args) == 0
current = ac.load_lock(str(repo))
assert all(current['entries'][k] == v for k, v in old['entries'].items())
assert all(p.read_bytes() == raw for p, raw in old_statements.items())
print('Historical provenance and attestations preserved.')
