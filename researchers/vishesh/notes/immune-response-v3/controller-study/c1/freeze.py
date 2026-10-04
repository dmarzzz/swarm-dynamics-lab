"""Offline packet construction. Re-freezing changes its hash and needs new admission."""
import hashlib,importlib.util,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c1_freeze_run',BASE/'run.py');run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
def freeze():
    files=[p for directory in ['src','scenario-study','evidence-study','freshness-study','controller-study'] for p in (BASE.parent.parent/directory).rglob('*.py')]
    files += [BASE.parent/'opus-config.json',BASE/'PLAN.md',BASE.parent/'next-contract/PLAN.md']
    sources={str(p.relative_to(BASE.parent)) if p.is_relative_to(BASE.parent) else '../'+str(p.relative_to(BASE.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    packet={'stage':'controller-c1','model':'anthropic/claude-opus-4.6','assignments':run.assignments(),'max_calls':32,'model_max_usd':1.771520,'infrastructure_max_usd':.15,'all_in_max_usd':1.921520,'source_sha256':sources,'diagnosis_shared_between_arms':True,'holdouts_consumed':False,'successor_authorized':False}
    (BASE/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
if __name__=='__main__':freeze()
