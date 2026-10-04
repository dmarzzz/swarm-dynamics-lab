"""Frozen D7 schema adapter and bounded local relay. No credential discovery."""
import hashlib,json,math,os,urllib.request,urllib.error
from pathlib import Path
MODEL='anthropic/claude-haiku-4.5'
ENDPOINT='https://openrouter.ai/api/v1/chat/completions'
PROVIDER={'only':['Anthropic'],'order':['Anthropic'],'allow_fallbacks':False,'require_parameters':True,'max_price':{'prompt':1,'completion':5}}

def wire_from_d6(body):
    """Historical D7 mapping: omits structured output. Use output_contract_d8 for repair."""
    assert body['model']=='claude-haiku-4-5-20251001'
    return {'model':MODEL,'messages':[{'role':'system','content':body['system']}]+body['messages'],'max_tokens':body['max_tokens'],'temperature':body['temperature'],'reasoning':{'enabled':False},'provider':PROVIDER,'stream':False}

def normalize(result):
    assert isinstance(result,dict) and 'error' not in result
    u=result['usage'];assert isinstance(u,dict)
    choices=result['choices'];assert isinstance(choices,list) and len(choices)==1
    choice=choices[0];message=choice['message']
    assert isinstance(message['content'],str)
    return {'usage':{'input_tokens':u.get('prompt_tokens'),'output_tokens':u.get('completion_tokens')},'provider_cost_usd':u.get('cost'),'stop_reason':'end_turn' if choice.get('finish_reason')=='stop' else 'incomplete','content':[{'type':'text','text':message['content']}],'route':{'model':result.get('model'),'provider':result.get('provider')},'tool_calls':message.get('tool_calls')}

def verify_route(result):
    assert result['route']=={'model':MODEL,'provider':'Anthropic'}
    assert not result['tool_calls']

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('redirect_refused')

class Relay:
    """One fresh durable journal, frozen hashes in order, no retry after ambiguity."""
    def __init__(self,packet,journal):
        self.hashes=[i['wire_sha256'] for i in packet['requests']]
        assert len(self.hashes)==2 and len(set(self.hashes))==2
        self.journal=Path(journal);self.journal.mkdir(mode=0o700)
        self.count=0;self.stopped=False
    def send(self,raw,request):
        if self.stopped or self.count>=2 or len(raw)>32768:raise ValueError('relay_closed')
        if hashlib.sha256(raw).hexdigest()!=self.hashes[self.count]:
            self.stopped=True;raise ValueError('wire_refused')
        fd=os.open(self.journal/f'{self.count+1}.start',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        with os.fdopen(fd,'w') as f:f.write(self.hashes[self.count]);f.flush();os.fsync(f.fileno())
        fd=os.open(self.journal,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
        self.count+=1
        try:answer=request(raw)
        except BaseException:self.stopped=True;raise
        if not isinstance(answer,bytes) or len(answer)>1_000_000:
            self.stopped=True;raise ValueError('response_bound')
        return answer
