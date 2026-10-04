"""Pinned local decision runtime with actual encoding checks and complete call receipts."""
import hashlib
import importlib.metadata
import json
import math
import time

MODEL='convaiinnovations/laya'
REVISION='55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851'
SOURCE='2e4d9c87e8b1621deb344eac7de5c7258f32f849'


class Runtime:
    def __init__(self):
        import torch,laya
        torch.set_num_threads(2);torch.manual_seed(0)
        self.agent=laya.load(MODEL,revision=REVISION,device='cpu',backend='eager')
        self.receipts=[]
        self.metadata={'model':MODEL,'checkpoint':REVISION,'laya_source':SOURCE,'laya_version':laya.__version__,
                       'device':'cpu','threads':2,'versions':{p:importlib.metadata.version(p) for p in ('torch','transformers','safetensors')}}

    def choose(self,state,instructions,criteria,context):
        from laya.common import build_sequence
        q={'type':'choice','instructions':instructions,'criteria':criteria}
        internal=self.agent._to_internal(q)
        ids,markers,options,truncation=build_sequence(self.agent.tok,state,internal,max_len=1024,head_max_len=256,return_stats=True,return_truncation_stats=True)
        receipt={'context':context,'state':state,'question':q,'input_hash':hashlib.sha256(json.dumps([state,q],sort_keys=True).encode()).hexdigest(),
                 'encoded_tokens':len(ids),'encoding':truncation,'options':options,'valid':False}
        start=time.monotonic();self.receipts.append(receipt)
        try:
            if truncation['truncated'] or options['options_distinct']!=len(criteria) or len(markers)!=len(criteria):raise ValueError('encoding_loss')
            answer=self.agent.predict(state,{'decision':q},max_len=1024,head_max_len=256)['answers']['decision']
            p=answer['probabilities'];choice=answer['choice']
            if set(p)!=set(criteria) or choice not in criteria or any(not math.isfinite(v) or not 0<=v<=1 for v in p.values()):raise ValueError('schema')
            if abs(sum(p.values())-1)>.001 or p[choice]<max(p.values())-.00001:raise ValueError('distribution')
            receipt.update(valid=True,choice=choice,probabilities=p)
            return choice
        except Exception as exc:
            receipt['error']=type(exc).__name__;raise
        finally:receipt['wall_s']=time.monotonic()-start
