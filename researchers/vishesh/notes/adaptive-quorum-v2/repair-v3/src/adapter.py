"""Declared hybrid: model extracts predicates, deterministic code combines constraints."""
import hashlib
import json
from engine import OPTIONS


class Hybrid:
    def __init__(self,runtime):
        self.runtime=runtime;self.cache={};self.invocations=[]

    def __call__(self,rows,context):
        allowed=[]
        for k in OPTIONS:
            row=rows[k]
            state=f"Provider {k}: scanned PDF support is {row['scanned']}; retention is {row['retention_days']} days; accuracy is {row['accuracy']} percent."
            tests=[f'Does provider {k} support scanned PDFs?',f'Does provider {k} retain documents for zero days?',f'Does provider {k} have accuracy at least 90 percent?']
            answers=[]
            for question in tests:
                key=hashlib.sha256(json.dumps([state,question]).encode()).hexdigest()
                cached=key in self.cache
                if not cached:
                    answer=self.runtime.choose(state,question,{'YES':'Yes','NO':'No'},dict(context,provider=k))
                    self.cache[key]=(answer,len(self.runtime.receipts)-1)
                answer,receipt=self.cache[key]
                self.invocations.append({'context':context,'provider':k,'predicate':question,'receipt':receipt,'cached':cached})
                answers.append(answer)
            if all(a=='YES' for a in answers):allowed.append(k)
        return min(allowed,key=lambda k:(rows[k]['price'],k)) if allowed else 'NONE'
