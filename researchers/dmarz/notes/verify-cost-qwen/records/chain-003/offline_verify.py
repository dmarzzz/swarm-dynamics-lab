"""Offline re-verification of chain 003 from the saved records (no hub, no model call)."""
import gzip, hashlib, json, os, sys
from pathlib import Path
os.environ['STUDY_MODEL'] = 'gpt-6-luna'
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
import analyze, chain, manifest, study, worker
base = Path(sys.argv[1]); status = json.loads((base / 'results' / 'chain-status.json').read_text())
assert status['source_hash'] == study.source_hash(), 'records are from another source hash'
ref = manifest.reference(); out = {'source_hash': study.source_hash(), 'model': status['model'], 'stages': {}}
class Offline:      # stands in for the hub: local file hashes and the saved summary's own numbers
    def __init__(self, directory, entry): self.d, self.e = directory, entry
    def get_run(self, run):
        s = json.loads((self.d / 'summary.json').read_text())
        return {'status': self.e['status'], 'metrics': worker.hub_metrics(s),
                'artifacts': [{'name': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in self.d.iterdir()
                              if p.name in worker.ARTIFACTS]}
probe = None
for stage in study.STAGES:
    e = dict(status['stages'][stage]); d = base / 'results' / Path(e['directory']).name; e['directory'] = str(d)
    res, rows = chain.verify_stage(Offline(d, e), stage, e, ref, probe=probe if stage == 'Q0' else None)
    if stage == 'P0': probe = rows
    hub_only = ('hub_status_matches', 'hub_has_every_artifact', 'artifact_checksums', 'hub_metrics_match')
    res['offline_checks'] = {k: v for k, v in res['checks'].items() if k not in hub_only}
    res['hub_checks_not_possible_offline'] = list(hub_only); res['ok_offline'] = all(res['offline_checks'].values()); res.pop('checks'); res.pop('ok')
    if stage == 'S1': res['units'] = chain.units(rows, ref)
    out['stages'][stage] = res
out['ok_offline'] = all(s['ok_offline'] for s in out['stages'].values())
print(json.dumps(out, indent=1, sort_keys=True))
