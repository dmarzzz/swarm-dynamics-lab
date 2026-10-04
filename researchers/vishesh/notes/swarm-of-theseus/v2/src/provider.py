"""Native Anthropic adapter; fixed endpoint, safe errors, durable pre-dispatch reservations.

The local ledger is funded by a separate authority reservation; creating a ledger is
NOT authorization. runner.py requires a fresh deployment receipt before construction.
"""
import json
import os
from pathlib import Path
import sqlite3
import time
import urllib.error
import urllib.request
import uuid
from presentation import present

MODEL = 'claude-haiku-4-5-20251001'
SCHEMA = {'type': 'object', 'properties': {
    'decisions': {'type': 'array', 'items': {'type': 'object', 'properties': {
        'id': {'type': 'string'}, 'command': {'type': 'string'}},
        'required': ['id', 'command'], 'additionalProperties': False}},
    'notebook': {'type': 'string'}}, 'required': ['decisions', 'notebook'], 'additionalProperties': False}


class StopRun(Exception):
    """Resource/process limit; do not continue dispatching."""


def reserve(ledger, cost):
    with sqlite3.connect(ledger, timeout=30) as db:
        db.execute('BEGIN IMMEDIATE')
        row = db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
        if not row or row[0] != 15: raise StopRun('allocation_ledger_mismatch')
        cap, used, calls = row
        if used + cost > cap or calls >= 660: raise StopRun('allocation_exhausted')
        db.execute('UPDATE budget SET reserved=?,calls=? WHERE id=1', (used + cost, calls + 1))
    return calls + 1


def write_new(path, data):
    with Path(path).open('x') as f:
        json.dump(data, f, sort_keys=True); f.flush(); os.fsync(f.fileno())


class AnthropicPolicy:
    def __init__(self, config, receipt, output):
        if config['model'] != MODEL or config['input_rate'] != 1 or config['output_rate'] != 5:
            raise StopRun('unqualified_model_or_price')
        if config['max_output_tokens'] != 900 or config['max_input_bytes'] != 18000:
            raise StopRun('prompt_bounds_mismatch')
        if not 0 <= time.time() - config['pricing_verified_epoch'] < 7 * 86400:
            raise StopRun('pricing_verification_expired')
        self.key = os.environ.get('SWARM_MODEL_API_KEY', '')
        if not self.key: raise StopRun('credential_missing')
        self.workspace = os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        self.ledger = Path(os.environ['THESEUS_V2_LEDGER'])
        self.deadline = min(time.time() + 7200, receipt['claim_until_epoch'])
        self.output = Path(output); self.output.mkdir()
        self.config = config
        with sqlite3.connect(self.ledger) as db:
            db.execute('CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY CHECK(id=1), cap REAL, reserved REAL, calls INTEGER)')
            db.execute('INSERT OR IGNORE INTO budget VALUES (1,15,0,0)')
            db.execute('CREATE TABLE IF NOT EXISTS study_limit (id INTEGER PRIMARY KEY CHECK(id=1), deadline REAL)')
            db.execute('INSERT OR IGNORE INTO study_limit VALUES (1,?)', (time.time() + 7200,))
            self.deadline = min(self.deadline, db.execute('SELECT deadline FROM study_limit WHERE id=1').fetchone()[0])
            if db.execute('SELECT cap FROM budget WHERE id=1').fetchone()[0] != 15:
                raise StopRun('allocation_ledger_mismatch')

    def complete(self, request):
        if time.time() >= self.deadline: raise StopRun('wall_or_claim_limit')
        body = {'model': MODEL, 'system': request['instructions'], 'temperature': 0, 'max_tokens': 900,
                'messages': [{'role': 'user', 'content': present(request['observation'])}],
                'output_config': {'format': {'type': 'json_schema', 'schema': SCHEMA}}}
        encoded = json.dumps(body).encode()
        if len(encoded) > 18000: raise StopRun('input_bound_exceeded')
        # Conservative byte-token reservation. No refund after ambiguous errors.
        reserved = ((len(encoded) + 512) + 900 * 5) / 1e6
        call = reserve(self.ledger, reserved)
        ident = f'{call:04d}-{uuid.uuid4().hex[:8]}'
        started = {'call': call, 'reserved_usd': reserved, 'input_bytes': len(encoded),
                   'request': request, 'exact_user_text': body['messages'][0]['content'], 'started_epoch': time.time()}
        write_new(self.output / (ident + '-started.json'), started)
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01'}
        if self.workspace: headers['anthropic-workspace-id'] = self.workspace
        req = urllib.request.Request('https://api.anthropic.com/v1/messages', data=encoded, headers=headers)
        result = {'call': call, 'value': None, 'error': None, 'usage': None, 'actual_usd': None}
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                raw = response.read(1_000_001)
            if len(raw) > 1_000_000: raise ValueError('response_bound')
            data = json.loads(raw)
            usage = data.get('usage', {})
            if all(type(usage.get(k)) is int for k in ('input_tokens', 'output_tokens')):
                result['usage'] = {k: usage[k] for k in ('input_tokens', 'output_tokens')}
                result['actual_usd'] = (usage['input_tokens'] + usage['output_tokens'] * 5) / 1e6
            result['stop_reason'] = data.get('stop_reason') if data.get('stop_reason') in ('end_turn', 'max_tokens', 'refusal', 'tool_use') else 'other'
            if data.get('stop_reason') != 'end_turn':
                result['error'] = 'incomplete_output'
            else:
                texts = [v['text'] for v in data['content'] if v.get('type') == 'text']
                result['value'] = json.loads(''.join(texts))
        except urllib.error.HTTPError as e:
            result['error'] = 'http_' + str(e.code)
        except Exception as e:
            # Do not return exception text, provider body or transport URLs/headers.
            result['error'] = 'provider_' + type(e).__name__
        result['finished_epoch'] = time.time()
        write_new(self.output / (ident + '-finished.json'), result)
        return result
