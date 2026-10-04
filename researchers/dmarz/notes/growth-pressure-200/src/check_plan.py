#!/usr/bin/env python3
"""Offline contract arithmetic and document-link checks; no simulated episodes."""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
d = json.loads((BASE / 'design.json').read_text())
n_market = d['batches'] * d['markets_per_batch']
n_agent = d['owners_per_market'] * d['markets_per_batch']
q = d['qualification']
q_calls = q['mechanics_calls'] + q['seeder_fixtures'] * q['seeder_steps'] + q['opening_load_calls'] + q['continuation_load_calls']
main = d['batches'] * n_agent * (d['opening_rounds'] + len(d['assigned_doses']) * d['continuation_rounds'])
counts = dict(independent_paired_markets=n_market, agents_per_economy=n_agent,
              focals_per_arm=n_market*d['focals_per_market'],
              ordinary_owners_per_arm=n_market*(d['owners_per_market']-d['potential_rivals_per_market']),
              main_calls=main, qualification_calls=q_calls, planned_calls=main+q_calls)
for key, value in counts.items():
    assert d['expected_counts'][key] == value, (key, value)
e = d['expected_counts']
assert e['max_http_attempts'] == e['planned_calls'] + e['max_extra_transport_attempts']
assert d['focals_per_market'] + d['potential_rivals_per_market'] + d['ordinary_small_per_market'] == d['owners_per_market']
c = d['initial_capacity']
assert c['each_focal']*d['focals_per_market'] + c['each_potential_rival']*d['potential_rivals_per_market'] + c['small_total'] == c['market']
t = d['time']
projected_main = t['projection_margin'] * (d['opening_rounds']*t['opening_wave_max_seconds'] + d['continuation_rounds']*t['continuation_wave_max_seconds'])
assert projected_main <= t['main_window_seconds']
assert t['qualification_limit_seconds'] + t['main_window_seconds'] == t['dispatch_deadline_seconds']
assert t['dispatch_deadline_seconds'] + t['request_timeout_seconds'] <= t['local_drain_deadline_seconds'] < t['execution_limit_seconds']
assert d['workers']['simulation_hosts'] == d['batches'] * len(d['assigned_doses'])
# Check the one-state worked accounting example only, not economic reachability.
p = d['economics']
price = 60 - p['demand_slope']*c['market']
unit_cost = p['unit_cost_floor'] + p['unit_cost_scale_premium']/(1+c['each_potential_rival']/p['unit_cost_capacity_scale'])
levy = p['levy_fraction']*(price-unit_cost)*c['each_potential_rival']
assert abs(levy - 89.32) < 1e-9
plan = (BASE/'PLAN.md').read_text()
for section in ['TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics']:
    assert f'## {section}\n' in plan, section
for path in [BASE/'README.md', BASE/'PLAN.md', BASE/'SETUP.md', BASE/'reviews/design-review.md']:
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        local = target.split('#',1)[0]
        assert (path.parent/local).exists(), (path, target)
print(json.dumps({'status':'PASS — arithmetic and local links only; no model or simulation runs',
                  **counts, 'max_http_attempts':e['max_http_attempts'],
                  'projected_main_seconds_at_wave_bounds':projected_main,
                  'historical_planned_cost_range_usd':[round((main+q_calls)*d['budget'][k],2) for k in ['historical_s1_cost_per_call_low','historical_s1_cost_per_call_high']],
                  'historical_max_context_cost_usd':round((main+q_calls)*d['budget']['historical_max_context_cost_per_call'],2)}, indent=2))
