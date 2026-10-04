"""Bounded JSON policy adapter. Secret values never enter diagnostics or artifacts.

The shared SQLite ledger reserves conservative cost BEFORE dispatch, across processes
and both studies. Reservations are never refunded, including ambiguous failures.
"""
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import urllib.error
import urllib.request


class PolicyError(Exception):
    pass


class HTTPPolicy:
    scientific = True

    def __init__(self):
        config = json.loads(Path(os.environ['SWARM_MODEL_CONFIG_FILE']).read_text())
        self.model = config['model']
        self.input_rate = float(config['input_usd_per_million'])
        self.output_rate = float(config['output_usd_per_million'])
        self.max_output = int(config.get('max_output_tokens', 1024))
        self.max_input_bytes = int(config.get('max_input_bytes', 24000))
        self.timeout = min(60, float(config.get('timeout_seconds', 45)))
        self.base = os.environ['SWARM_MODEL_BASE_URL'].rstrip('/')
        self.key = os.environ.get('SWARM_MODEL_API_KEY', '')
        self.ledger = os.environ['SWARM_BUDGET_LEDGER']
        self.cap = min(45., float(config['total_api_cap_usd']))
        self.calls = 0
        if not self.model or self.model.startswith('REPLACE') or min(self.input_rate, self.output_rate) < 0:
            raise PolicyError('invalid model or pricing')
        if not config.get('qualified_nonreasoning_endpoint') or not config.get('pricing_verified_date'):
            raise PolicyError('qualified endpoint and pricing date required')
        if not (self.base.startswith('https://') or self.base.startswith('http://127.0.0.1:')):
            raise PolicyError('HTTPS or loopback required')
        with closing(sqlite3.connect(self.ledger)) as db, db:
            db.execute('CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY CHECK(id=1), cap REAL, reserved REAL, calls INTEGER)')
            db.execute('INSERT OR IGNORE INTO budget VALUES (1, ?, 0, 0)', (self.cap,))
            cap = db.execute('SELECT cap FROM budget').fetchone()[0]
            if cap != self.cap:
                raise PolicyError('budget ledger cap mismatch')

    def complete(self, request, fallback):
        body = {'model': self.model, 'temperature': 0, 'max_tokens': self.max_output,
                'response_format': {'type': 'json_object'}, 'messages': [
                    {'role': 'system', 'content': request['instructions']},
                    {'role': 'user', 'content': json.dumps(request['observation'], sort_keys=True)}]}
        encoded = json.dumps(body).encode()
        if len(encoded) > self.max_input_bytes:
            raise PolicyError('input bound exceeded')
        # Byte count plus envelope bounds input tokens for qualified byte-token endpoints.
        cost = ((len(encoded)+512)*self.input_rate + self.max_output*self.output_rate)/1e6
        with closing(sqlite3.connect(self.ledger, timeout=20)) as db, db:
            db.execute('BEGIN IMMEDIATE')
            cap, used, calls = db.execute('SELECT cap,reserved,calls FROM budget').fetchone()
            if used + cost > cap or calls >= 6500:
                raise PolicyError('shared budget exhausted')
            db.execute('UPDATE budget SET reserved=?,calls=? WHERE id=1', (used+cost, calls+1))
        self.calls += 1
        headers = {'Content-Type': 'application/json'}
        if self.key:
            headers['Authorization'] = 'Bearer '+self.key
        req = urllib.request.Request(self.base+'/chat/completions', data=encoded, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read(1_000_001)
            if len(raw) > 1_000_000:
                raise PolicyError('response size exceeded')
            result = json.loads(raw)
            choice = result['choices'][0]
            if choice['finish_reason'] != 'stop':
                raise PolicyError('incomplete output')
            value = json.loads(choice['message']['content'])
            if not isinstance(value, dict):
                raise PolicyError('object required')
            return value
        except urllib.error.HTTPError as exc:
            raise PolicyError('HTTP status '+str(exc.code)) from None
        except PolicyError:
            raise
        except Exception as exc:
            raise PolicyError('provider '+type(exc).__name__) from None


class ScriptedPolicy:
    scientific = False
    model = 'scripted-observation-policy-v1'
    calls = 0

    def complete(self, request, fallback):
        return fallback(request['observation'])


def output_schema(example):
    if isinstance(example,dict):
        return {'type':'object','properties':{k:output_schema(v) for k,v in example.items()},
                'required':list(example),'additionalProperties':False}
    if isinstance(example,list):
        return {'type':'array','items':output_schema(example[0]) if example else {'type':'string'}}
    if type(example) is bool:return {'type':'boolean'}
    if type(example) in (int,float):return {'type':['number','null']}
    if example is None:return {'type':['number','null']}
    return {'type':'string'}


class AnthropicPolicy(HTTPPolicy):
    """Native adapter for the same pinned Haiku used by discussion-dose."""
    def __init__(self):
        super().__init__()
        self.workspace=os.environ.get('SWARM_MODEL_WORKSPACE_ID','')
        self.actual_usd=0.;self.usage_missing=0;self.input_tokens=0;self.output_tokens=0
        if not self.key:raise PolicyError('model credential required')

    def complete(self,request,fallback):
        # Retry only enumerated transient HTTP statuses, once. Each _once call
        # reserves again, including ambiguous billed failures. No parse retries.
        for attempt in range(2):
            try:return self._once(request,fallback)
            except PolicyError as exc:
                if attempt or str(exc) not in ('HTTP status 429','HTTP status 502','HTTP status 503','HTTP status 504'):raise
                __import__('time').sleep(.5)

    def _once(self,request,fallback):
        body={'model':self.model,'system':request['instructions'],'temperature':0,
              'max_tokens':self.max_output,'messages':[{'role':'user','content':json.dumps(request['observation'],sort_keys=True)}],
              'output_config':{'format':{'type':'json_schema','schema':output_schema(fallback(request['observation']))}}}
        encoded=json.dumps(body).encode()
        if len(encoded)>self.max_input_bytes:raise PolicyError('input bound exceeded')
        cost=((len(encoded)+512)*self.input_rate+self.max_output*self.output_rate)/1e6
        with closing(sqlite3.connect(self.ledger,timeout=20)) as db, db:
            db.execute('BEGIN IMMEDIATE')
            cap,used,calls=db.execute('SELECT cap,reserved,calls FROM budget').fetchone()
            if used+cost>cap or calls>=6500:raise PolicyError('shared budget exhausted')
            db.execute('UPDATE budget SET reserved=?,calls=? WHERE id=1',(used+cost,calls+1))
        headers={'Content-Type':'application/json','x-api-key':self.key,'anthropic-version':'2023-06-01'}
        if self.workspace:headers['anthropic-workspace-id']=self.workspace
        req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=encoded,headers=headers)
        self.calls+=1;self.usage_missing+=1
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as response:raw=response.read(1_000_001)
            if len(raw)>1_000_000:raise PolicyError('response size exceeded')
            result=json.loads(raw);usage=result.get('usage',{})
            if all(type(usage.get(k)) is int for k in ('input_tokens','output_tokens')):
                self.actual_usd+=(usage['input_tokens']*self.input_rate+usage['output_tokens']*self.output_rate)/1e6
                self.usage_missing-=1
                self.input_tokens+=usage['input_tokens'];self.output_tokens+=usage['output_tokens']
            if result.get('stop_reason')!='end_turn':raise PolicyError('incomplete output')
            return json.loads(result['content'][0]['text'])
        except urllib.error.HTTPError as exc:raise PolicyError('HTTP status '+str(exc.code)) from None
        except PolicyError:raise
        except Exception as exc:raise PolicyError('provider '+type(exc).__name__) from None
