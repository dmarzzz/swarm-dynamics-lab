"""Rebuild deterministic offline development evidence. No paid or network calls."""
import hashlib
import json
import unittest
from pathlib import Path
from prototype import World, ActorTools, build_case, reference

HERE=Path(__file__).resolve().parent

def main():
    suite=unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py')
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():raise SystemExit(1)
    output=HERE/'results';output.mkdir(exist_ok=True)
    runs=[];manifest=[]
    for structure in ('independent','serial','mixed'):
        for condition in ('fault','clean','insufficient'):
            case=build_case(structure,condition);case_id=structure+'-'+condition
            manifest.append({'id':case_id,'sha256':hashlib.sha256(json.dumps(case,sort_keys=True).encode()).hexdigest(),'case':case})
            for slots in (1,3):
                world=World(case,slots);packet=world.start();answer=reference(ActorTools(world));grade=world.evaluate(answer)
                assert grade['correct']
                runs.append(dict(case=case_id,slots=slots,actor_start=packet,evidence=world.receipts,actions=world.actions,answer=answer,grade=grade))
    (output/'development-cases-evaluator.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (output/'reference-runs.json').write_text(json.dumps(runs,indent=2)+'\n')
    summary={'scope':'nine authored development cases from three templates; deterministic reference, not native-agent evidence',
             'cases':9,'reference_executions':len(runs),'correct':sum(r['grade']['correct'] for r in runs),'tests_passed':result.testsRun,
             'fault_acquisition_rounds':{s:[r['grade']['query_rounds'] for r in runs if r['case']==s+'-fault'] for s in ('independent','serial','mixed')},
             'model_calls':0,'new_cost':0,'native_qualified':False,
             'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('PLAN.md','prototype.py','test_prototype.py','validate.py')}}
    (output/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
