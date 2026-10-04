"""Full parity receipt: every sybil-budget-sonnet Q0/S1 assignment equals the parent's row.

Offline, no model calls. Usage: python3 reporting/parity_check.py reporting/parity-receipt.json
"""
import hashlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
import study
spec=importlib.util.spec_from_file_location('parentstudy',ROOT.parent/'sybil-budget-api/src/study.py')
ps=importlib.util.module_from_spec(spec);spec.loader.exec_module(ps)
out={'source_hash':study.source_hash()}
for stage in ('Q0','S1'):
    mine={a['id']:a for a in study.assignments(stage)}
    theirs={a['id']:a for a in ps.assignments(stage)}
    assert set(mine)==set(theirs),'assignment_ids_differ'
    for k,a in mine.items():
        for f in ('packet_hash','expected','graph_metrics','verification_events','task','arm','checks','attacker_pass','kind'):
            assert a[f]==theirs[k][f],f'{f}_differs'
    out[stage]={'assignments':len(mine),'id_set_sha256':hashlib.sha256(json.dumps(sorted(mine)).encode()).hexdigest(),'all_fields_equal':True}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
