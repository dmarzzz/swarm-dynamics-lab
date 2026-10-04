"""Actor input is only the public simulator observation; no treatment/evaluator packet."""
import json
import os
import time
from pathlib import Path
import provider
import sim

class MockResponse:
    def __init__(self, data): self.data=data
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,*args):return json.dumps(self.data).encode()

def mock_opener(request, timeout):
    body=json.loads(request.data);obs=json.loads(body['messages'][0]['content'])
    # A rehearsal policy exercises registration under every regulator, without making a discovery claim.
    arm='split_control' if obs['portfolio']['max_firms']>1 else 'merged'
    action=sim.scripted_action(obs,arm)
    return MockResponse({'model':body['model'],'stop_reason':'end_turn',
        'usage':{'input_tokens':100,'output_tokens':80},
        'content':[{'type':'text','text':json.dumps(action)}]})

class Policy:
    def __init__(self, client, path, identity, backend, max_seconds):
        self.client=client;self.path=Path(path);self.identity=identity;self.backend=backend
        self.calls=[];self.started=time.monotonic();self.max_seconds=max_seconds
    def __call__(self, obs, arm):
        if time.monotonic()-self.started>self.max_seconds:raise TimeoutError('episode_time_limit')
        call_id=f'{self.identity}:{arm}:r{obs["round"]}'
        item={'call_id':call_id,'arm':arm,'round':obs['round'],'observation':obs,
              'prompt_sha256':sim.digest(provider.SYSTEM),'backend':self.backend}
        try:
            action,account=self.client.call(obs,call_id)
            item.update(action=action,accounting=account,status='ok')
            return action
        except provider.CallFailure as exc:
            item.update(status=exc.category,accounting=exc.accounting)
            raise
        finally:
            self.calls.append(item)
            with self.path.open('a') as f:
                f.write(json.dumps(item,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
    def metrics(self,arm=None):
        rows=[r for r in self.calls if arm is None or r['arm']==arm]
        return {'model_calls':sum(bool(r.get('accounting',{}).get('attempted')) for r in rows) if self.backend=='anthropic' else 0,
                'api_cost_usd':sum(r.get('accounting',{}).get('actual_usd',0) for r in rows) if self.backend=='anthropic' else 0,
                'unpriced_calls':sum(bool(r.get('accounting',{}).get('attempted')) and not r.get('accounting',{}).get('usage_reported') for r in rows) if self.backend=='anthropic' else 0}
