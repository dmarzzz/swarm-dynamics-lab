"""Freeze source/world contract and test qualification binding; no dispatch."""
import hashlib
import json
import sys
from pathlib import Path
import peer_collection
import peer_qualification
import peer_instrument as i

ROOT=Path(__file__).resolve().parent
STUDY=ROOT.parent

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def contract():
    # Loaded source dependency inventory, plus each owned collection module.
    paths={Path(m.__file__).resolve() for m in list(sys.modules.values())
           if getattr(m,'__file__',None) and str(Path(m.__file__).resolve()).startswith(str(STUDY)) and str(m.__file__).endswith('.py')}
    paths.update(ROOT.glob('*.py'))
    sources={str(p.relative_to(STUDY)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    sources['../experiment-documentation/public_plan.py']=hashlib.sha256((STUDY.parent/'experiment-documentation/public_plan.py').read_bytes()).hexdigest()
    return {'model':'anthropic/claude-opus-4.6','provider':'anthropic','fallbacks':False,
            'worlds_sha256':digest(i.roots()),'source_sha256':sources,
            'plan_sha256':hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest(),
            'ticks':6,'request_bytes':8000,'output_tokens':512,'reason_max_characters':240}


def packet():
    c=contract()
    return {'packet_revision':3,'stage':'peer-correction-Q-and-first-repeat','native_dispatch_enabled':True,
            'contract':c,'contract_sha256':digest(c),'worlds':i.roots(),
            'Q':{'worlds':4,'calls':48,'model_max_usd':2.657280,'external_source':False},
            'first_repeat':{'worlds':4,'arms':3,'shared_initial_calls':16,'branch_calls':168,'calls':184,'model_max_usd':10.186240},
            'maximum_calls':232,'model_max_usd':12.843520,'infra_max_proposed_usd':.15,
            'prior_reserved_usd':15.524695,'current_cap_usd':16.877155,
            'minimum_proposed_cumulative_model_cap_usd':28.368215,
            'second_repeat_authorized':False,'qualification_binding_required':True}


def verify_qualification(receipt, expected):
    if receipt.get('contract_sha256')!=expected['contract_sha256']:
        raise ValueError('qualification_contract_mismatch')
    if receipt.get('completed_worlds')!=4 or receipt.get('api_calls')!=48:
        raise ValueError('qualification_incomplete')
    if not all(receipt.get(k) is True for k in ('native','all_automated_pass','manual_reason_review_pass','usage_reconciled')):
        raise ValueError('qualification_not_passed')
    # This validates scientific binding ONLY, never grants budget/allocation.
    return True


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: prepare.py NEW_PACKET_PATH')
    with Path(sys.argv[1]).open('x') as f:json.dump(packet(),f,indent=2)
