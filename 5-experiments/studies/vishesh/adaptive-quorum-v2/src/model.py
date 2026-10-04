import importlib.util
import json
import math
from pathlib import Path
from study import CHOICES,RULE

spec=importlib.util.spec_from_file_location('v1_backend',Path(__file__).resolve().parents[2]/'adaptive-quorum/src/backend.py')
v1=importlib.util.module_from_spec(spec);spec.loader.exec_module(v1)


class Laya(v1.Laya):
    def __init__(self):
        super().__init__()
        self.calls=0;self.input_tokens=0

    def __call__(self,state):
        text=json.dumps(state,separators=(',',':'))
        q={'decision':{'type':'choice','instructions':RULE,
                      'criteria':{c: ('Select provider '+c if c in ('A','B','C') else
                          'All providers fail the requirements' if c=='NONE' else 'Evidence is insufficient; wait') for c in CHOICES}}}
        tokens=len(self.model.tok.encode(text))+len(self.model.tok.encode(json.dumps(q)))
        if tokens>850:raise ValueError('context_budget_exceeded')
        self.calls+=1;self.input_tokens+=tokens
        result=self.model.predict(text,q,max_len=1024)
        answer=result['answers']['decision'];p=answer['probabilities']
        self.receipts.append({'choice':answer['choice'],'probabilities':p,'input_tokens_estimate':tokens})
        if set(p)!=set(CHOICES) or any(not math.isfinite(v) or v<0 or v>1 for v in p.values()):raise ValueError('probabilities')
        if abs(sum(p.values())-1)>.001 or p[answer['choice']]<max(p.values())-.00001:raise ValueError('distribution')
        return answer['choice']
