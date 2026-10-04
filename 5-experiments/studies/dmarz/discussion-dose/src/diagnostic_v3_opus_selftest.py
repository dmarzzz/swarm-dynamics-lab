"""Offline checks for diagnostic_v3_opus: no network, no model calls.

Usage: python3 diagnostic_v3_opus_selftest.py <retained Q0 directory>
"""
import io
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('SWARM_MODEL_API_KEY', 'offline-test-placeholder')
import diagnostic_v3_opus as o
from bench_v3.policies import Scripted
from tasks import digest


class _Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): pass


def _fake(blocks, stop='end_turn', model=o.MODEL):
    payload = json.dumps({'model': model, 'stop_reason': stop, 'content': blocks,
                          'usage': {'input_tokens': 100, 'output_tokens': 50}}).encode()
    return lambda request, timeout: _Response(payload)


def main(q0):
    plan, inputs = o.all_inputs(Path(q0), o.DEFAULT_PLAN)
    assert len(inputs) == 72
    order = o.schedule(plan)
    assert len(order) == len(set(order)) == 72 and order == o.schedule(plan)
    counts = Counter(inputs[k]['selected']['group'] for k in order)
    assert counts == Counter({'memory': 36, 'report_snapshot': 18, 'diagnostic': 6, 'fresh_diagnostic': 12})
    assert not set(o.FRESH_WORLDS) & (set(range(50001, 50007)) | set(range(30000, 30024)) | set(range(20001, 20007)))
    # Request contract for claude-opus-5-5.
    prov = o.provider(30)
    item = inputs['fresh-52001']
    body = prov.request_body(item['request'])
    assert 'temperature' not in body and body['thinking'] == {'type': 'adaptive'}
    assert body['output_config']['effort'] == 'high' and body['max_tokens'] == 16000 and body['model'] == o.MODEL
    # Parsing: thinking + one text accepted; everything else fails closed.
    import urllib.request
    original = urllib.request.urlopen
    try:
        answer = Scripted().complete(item['request'])
        urllib.request.urlopen = _fake([{'type': 'thinking', 'thinking': '', 'signature': 's'}, {'type': 'text', 'text': json.dumps(answer)}])
        assert prov.complete(item['request']) == answer and prov.last_usage == {'input_tokens': 100, 'output_tokens': 50}
        for blocks, stop, reason in (([{'type': 'text', 'text': '{}'}, {'type': 'text', 'text': '{}'}], 'end_turn', 'provider_schema_refusal'),
                                     ([{'type': 'text', 'text': json.dumps(answer)}], 'max_tokens', 'provider_incomplete'),
                                     ([{'type': 'tool_use'}], 'end_turn', 'provider_schema_refusal'),
                                     ([], 'refusal', 'provider_schema_refusal')):
            urllib.request.urlopen = _fake(blocks, stop)
            try: prov.complete(item['request']); raise AssertionError('accepted invalid response')
            except o.ProviderFailure as exc: assert exc.public_reason == reason, exc.public_reason
        assert prov.last_stop_reason == 'refusal'
        urllib.request.urlopen = _fake([{'type': 'text', 'text': ' ' * 8001 + json.dumps(answer)}])
        try: prov.complete(item['request']); raise AssertionError('accepted over-long visible answer')
        except o.ProviderFailure as exc: assert exc.public_reason == 'provider_incomplete'
        with tempfile.TemporaryDirectory() as folder:
            urllib.request.urlopen = _fake([{'type': 'thinking', 'thinking': '', 'signature': 's'}, {'type': 'text', 'text': '{"vote": "A", "claims": {}}'}])
            ledger = Path(folder) / 'ledger'; ledger.mkdir()
            probe = o.probe(Path(folder) / 'probe.json', ledger, 5)
            assert probe['model_calls'] == 1 and probe['returned_model'] == o.MODEL and probe['cost_usd'] == 0.0014
            try: o.probe(Path(folder) / 'probe2.json', ledger, 5); raise AssertionError('second probe accepted')
            except FileExistsError: pass
    finally:
        urllib.request.urlopen = original
    # Scripted control through the full execute/summarize path; never passes the scientific gate.
    rows = [{'call_id': f'd1o-{i:03d}', 'key': k, 'group': inputs[k]['selected']['group'], 'label': inputs[k]['selected']['label'],
             'request_sha256': inputs[k]['selected']['request_sha256'], 'provider_body_sha256': digest(prov.request_body(inputs[k]['request'])),
             'reservation_microusd': 0} for i, k in enumerate(order)]
    frozen = {'attempt': o.ATTEMPT, 'schedule': rows, 'counts': dict(counts)}
    with tempfile.TemporaryDirectory() as folder:
        ledger = Path(folder) / 'ledger'; ledger.mkdir()
        result = o.execute(frozen, inputs, Path(folder) / 'out', ledger, Scripted(), False)
        assert result['terminal'] == 72 and result['physical_calls'] == 0
        summary = json.loads((Path(folder) / 'out/summary.json').read_text())
        assert summary['valid'] == 72 and summary['fresh_gate']['evidence_justified'] == 12 and summary['fresh_gate']['passed'] is False
        try: o.execute(frozen, inputs, Path(folder) / 'out2', ledger, Scripted(), False); raise AssertionError('duplicate start accepted')
        except FileExistsError: pass
    print(json.dumps({'selftest': 'pass', 'inputs': 72, 'fresh_scripted_justified': 12, 'model_calls': 0}))


if __name__ == '__main__': main(sys.argv[1])
