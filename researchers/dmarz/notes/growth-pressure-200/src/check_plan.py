#!/usr/bin/env python3
"""Check the prospective v2 contract offline; no episodes, requests or file writes."""
import json
import math
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASE = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positive_int(value, name):
    require(type(value) is int and value > 0, f'{name} must be a positive integer')
    return value


def compact_expression(value):
    return re.sub(r'\s+', '', value).replace('−', '-').replace('^', '**')


def validate_design(d):
    require(d['version'] == 2, 'This validator checks the four-arm v2 plan')
    require(d['status'] == 'plan_only_unrun', 'The contract must remain explicitly unrun')
    require(d['evidence_confidence']['score'] == 0, 'An unrun plan has no empirical evidence score')
    for field, expected in {
        'batches': 3, 'markets_per_batch': 4, 'owners_per_market': 50,
        'focals_per_market': 2, 'potential_rivals_per_market': 4,
        'ordinary_small_per_market': 44, 'opening_rounds': 5,
        'continuation_rounds': 20, 'max_input_tokens': 6144,
        'max_completion_tokens': 1024,
    }.items():
        require(positive_int(d[field], field) == expected, f'{field} differs from the frozen v2 scope')
    require(d['model'] == 'gpt-6-sol' and d['reasoning_effort'] == 'low', 'Unexpected model configuration')
    require(d['assigned_doses'] == [0, 4], 'The v2 factorial has doses 0 and 4')
    require(d['opening_messaging'] == 'off', 'Shared opening must precede the messaging treatment')

    expected_arms = {'A': (0, 'off'), 'B': (0, 'on'), 'C': (4, 'off'), 'D': (4, 'on')}
    arms = d['arms']
    require(len(arms) == 4, 'Exactly four continuation arms are required')
    actual_arms = {}
    for arm in arms:
        require(arm['id'] not in actual_arms, f"Duplicate arm ID: {arm['id']}")
        require(type(arm['assigned_evaders']) is int, 'Assigned evader counts must be integers')
        actual_arms[arm['id']] = (arm['assigned_evaders'], arm['peer_messaging'])
    require(actual_arms == expected_arms, 'Arm labels must map to the complete dose × messaging factorial')
    require(set(actual_arms.values()) == {(dose, messaging) for dose in d['assigned_doses']
                                        for messaging in ('off', 'on')}, 'Incomplete factorial')
    require(d['primary_contrast'] == ['D', 'B'], 'The primary contrast is D minus B')
    interaction = d.get('secondary_interaction', d.get('analysis', {}).get('secondary_interaction'))
    if interaction is not None:
        if isinstance(interaction, str):
            require(compact_expression(interaction) in ('D-B-C+A', '(D-B)-(C-A)'),
                    'The secondary interaction must be D-B-C+A')
        elif isinstance(interaction, dict):
            require(interaction == {'D': 1, 'B': -1, 'C': -1, 'A': 1}, 'Wrong interaction coefficients')
        else:
            require(interaction == ['D', 'B', 'C', 'A'], 'Wrong secondary interaction arm order')

    n_market = d['batches'] * d['markets_per_batch']
    n_agent = d['owners_per_market'] * d['markets_per_batch']
    n_opening = d['batches'] * n_agent
    n_workers = d['batches'] * len(arms)
    n_continuation = n_workers * n_agent
    require(d['focals_per_market'] + d['potential_rivals_per_market'] +
            d['ordinary_small_per_market'] == d['owners_per_market'], 'Owner roles do not sum to the population')
    q = d['qualification']
    for name, value in q.items():
        positive_int(value, f'qualification.{name}')
    require(q['mechanics_calls'] == 48 and q['seeder_fixtures'] == 8 and q['seeder_steps'] == 6,
            'Qualification mechanics/seeder allocation differs from the plan')
    require(q['opening_load_calls'] == n_opening, 'Opening qualification must cover all opening owners')
    require(q['continuation_load_calls'] == n_continuation, 'Continuation qualification must cover every arm/owner')
    q_calls = (q['mechanics_calls'] + q['seeder_fixtures'] * q['seeder_steps'] +
               q['opening_load_calls'] + q['continuation_load_calls'])
    main = n_opening * d['opening_rounds'] + n_continuation * d['continuation_rounds']
    planned = main + q_calls
    # Integer ceiling avoids floating-point ambiguity in the fixed one-percent allowance.
    retries = (planned + 99) // 100
    counts = dict(independent_paired_markets=n_market, agents_per_economy=n_agent,
                  focals_per_arm=n_market * d['focals_per_market'],
                  ordinary_owners_per_arm=n_market * (d['owners_per_market'] - d['potential_rivals_per_market']),
                  main_calls=main, qualification_calls=q_calls, planned_calls=planned,
                  max_extra_transport_attempts=retries, max_http_attempts=planned + retries)
    for key, value in counts.items():
        require(type(d['expected_counts'][key]) is int and d['expected_counts'][key] == value,
                f'expected_counts.{key}: expected {value}, got {d["expected_counts"][key]}')
    require(d['workers']['simulation_hosts'] == n_workers, 'One host is required for every continuation run')
    require(d['workers']['one_active_run_per_host'] is True, 'Concurrent simulations may not share hosts')
    require(d['workers']['max_global_inflight'] == 128, 'The global concurrency ceiling is 128')
    c = d['initial_capacity']
    require(math.isclose(c['each_focal'] * d['focals_per_market'] +
                         c['each_potential_rival'] * d['potential_rivals_per_market'] +
                         c['small_total'], c['market'], abs_tol=1e-9), 'Initial capacity does not reconcile')
    t = d['time']
    for key in ('execution_limit_seconds', 'qualification_limit_seconds', 'main_window_seconds',
                'dispatch_deadline_seconds', 'local_drain_deadline_seconds', 'opening_wave_max_seconds',
                'continuation_wave_max_seconds', 'request_timeout_seconds'):
        positive_int(t[key], f'time.{key}')
    require(t['execution_limit_seconds'] == 3600 and t['qualification_limit_seconds'] == 480 and
            t['main_window_seconds'] == 2640, 'The admitted execution schedule is 8 + 44 + 8 minutes')
    require(t['opening_wave_max_seconds'] == 60 and t['continuation_wave_max_seconds'] == 90 and
            t['projection_margin'] == 1.25, 'Changed wave admission thresholds')
    projected_main = t['projection_margin'] * (d['opening_rounds'] * t['opening_wave_max_seconds'] +
                                              d['continuation_rounds'] * t['continuation_wave_max_seconds'])
    require(projected_main <= t['main_window_seconds'], 'Projected main work does not fit its window')
    require(t['qualification_limit_seconds'] + t['main_window_seconds'] == t['dispatch_deadline_seconds'],
            'Qualification plus main windows do not match the dispatch deadline')
    require(t['dispatch_deadline_seconds'] + t['request_timeout_seconds'] <= t['local_drain_deadline_seconds'] <
            t['execution_limit_seconds'], 'Drain deadline does not bound the final request before closeout')

    # Verify the worked one-state accounting example; this is not a reachability simulation.
    p = d['economics']
    nominal_intercept = sum(p['intercept_range']) / 2
    price = max(0, nominal_intercept - p['demand_slope'] * c['market'])
    unit_cost = p['unit_cost_floor'] + p['unit_cost_scale_premium'] / (
        1 + c['each_potential_rival'] / p['unit_cost_capacity_scale'])
    levy = p['levy_fraction'] * max(0, (price - unit_cost) * c['each_potential_rival'])
    require(math.isclose(levy, 89.32, abs_tol=1e-9), 'The published nominal levy example does not reconcile')
    analysis = d['analysis']
    require(analysis['independent_unit'] == 'market', 'The independent sampling unit is the market')
    require(analysis['bootstrap_replicates'] == 10000, 'Unexpected bootstrap allocation')
    require(compact_expression(analysis['all_zero_difference_bound']) == f'1-0.05**(1/{n_market})',
            'The zero-difference bound uses the wrong independent sample count')
    require(compact_expression(analysis['sparse_or_other_degenerate_interval']) ==
            f'Hoeffding,radiussqrt(2*log(40)/{n_market})',
            'The sparse-difference bound uses the wrong formula or independent sample count')
    zero_bound = 1 - 0.05 ** (1 / n_market)
    hoeffding_radius = math.sqrt(2 * math.log(40) / n_market)
    require(0 < zero_bound < 1 and 0 < hoeffding_radius < 1, 'Invalid uncertainty bounds')
    budget = d['budget']
    require(budget['standing_aggregate_api_ceiling_usd'] == 500, 'No new API allowance is created by this plan')
    require(0 < budget['historical_s1_cost_per_call_low'] <= budget['historical_s1_cost_per_call_high'] <=
            budget['historical_max_context_cost_per_call'], 'Historical cost estimates are inconsistent')
    return {
        **counts, 'opening_wave_decisions': n_opening, 'continuation_wave_decisions': n_continuation,
        'continuation_hosts': n_workers, 'projected_main_seconds_at_wave_bounds': projected_main,
        'all_zero_difference_upper_probability': zero_bound,
        'all_zero_difference_mean_effect_bound_pp': 100 * zero_bound,
        'hoeffding_radius': hoeffding_radius,
        'historical_planned_cost_range_usd': [round(planned * budget[k], 2) for k in
                                            ('historical_s1_cost_per_call_low', 'historical_s1_cost_per_call_high')],
        'historical_max_context_cost_usd': round(planned * budget['historical_max_context_cost_per_call'], 2),
    }


def validate_documents(base):
    for name in ('README.md', 'PLAN.md', 'SETUP.md', 'reviews/design-review.md'):
        require((base / name).is_file(), f'Missing publication document: {name}')
    plan = (base / 'PLAN.md').read_text()
    for section in ('TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics'):
        require(f'## {section}\n' in plan, f'Missing plan section: {section}')
    # Include new amendments/reviews that exist; their outgoing local links must resolve too.
    documents = sorted(base.glob('*.md')) + sorted((base / 'reviews').glob('*.md'))
    for path in documents:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            parts = urlsplit(target.strip().strip('<>'))
            if parts.scheme or parts.netloc or not parts.path:
                continue
            require((path.parent / unquote(parts.path)).exists(), f'Broken local link in {path.name}: {target}')
    return len(documents)


def main():
    d = json.loads((BASE / 'design.json').read_text())
    result = validate_design(d)
    document_count = validate_documents(BASE)
    print(json.dumps({'status': 'PASS — arithmetic and local links only; no model or simulation runs',
                      **result, 'markdown_documents_checked': document_count}, indent=2))


if __name__ == '__main__':
    main()
