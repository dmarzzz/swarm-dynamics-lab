"""Saved C1 semantic/protocol audit; no model or network calls."""
import copy,importlib.util,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c1_audit_run',BASE/'run.py');run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
def audit(out):
    out=Path(out);rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];frames=0
    for row in rows:
        c=row['case'];state=copy.deepcopy(c['initial']);history=[];trace=[]
        for frame in row['trace']:
            o=run.cases.observe(c,state,frame['tick'],history,[]);assert o==frame['observation']
            q=run.candidate.action_request(c,o,frame['diagnosis'],row['order']);assert list(frame['raw_response'])==q['response_schema']['required']==frame['observed_key_order']
            action=run.cases.f.controller.decode(c['fixture'],frame['raw_response']);assert action==frame['action'];x=run.cases.f.step(c['fixture'],state,action)
            for k,v in x.items():assert frame[k]==v
            assert frame['diagnosis_correct']==(frame['diagnosis']==run.public_reference.labels(o));trace.append(x);history.append({'action':action,'result':x['result']});frames+=1
        assert run.cases.gate(c,trace)==row['outcome_pass']
    return {'episodes_replayed':len(rows),'frames_replayed':frames,'manual_semantic_agreement_review':'still_required','new_model_calls':0}
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2))
