"""Freeze Q2-only contract; never launches or grants admission."""
import importlib.util,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('q2_prior_prepare',ROOT/'prepare.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
digest=prior.digest

def packet():
 c=prior.contract();c.update(plan_sha256=hashlib.sha256((ROOT/'Q2-PLAN.md').read_bytes()).hexdigest(),instruction_revision='explicit-existing-string-limits-v1')
 return {'stage':'peer-contract-q2','native_dispatch_enabled':True,'contract':c,'contract_sha256':digest(c),'maximum_calls':48,'model_max_usd':2.657280,'infrastructure_max_usd':.03,'maximum_host_minutes':20,'prior_calls':711,'prior_reserved_usd':15.606955,'cumulative_model_cap_usd':28.368215,'comparison_authorized':False}
if __name__=='__main__':
 with Path(sys.argv[1]).open('x') as f:json.dump(packet(),f,indent=2)
