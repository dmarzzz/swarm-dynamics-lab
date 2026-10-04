"""Exact, uncached public-plan and locally supplied deployment-receipt checks."""
import hashlib
import json
import re
import time
import urllib.request

EXPERIMENT = 'swarm-of-theseus-v2'


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Theseus-v2-preflight', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=25) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000: raise ValueError('public_document_too_large')
    return data.decode()


def validate_plan(experiment, markdown, expected_url, expected_hash, tldr):
    if experiment.get('id') != EXPERIMENT: raise ValueError('wrong_experiment')
    if not re.fullmatch(r'https://github.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/researchers/vishesh/notes/swarm-of-theseus/v2/PLAN.md', expected_url):
        raise ValueError('immutable_v2_plan_required')
    if experiment.get('url') != expected_url: raise ValueError('registered_plan_revision_mismatch')
    if hashlib.sha256(markdown.encode()).hexdigest() != expected_hash: raise ValueError('public_plan_hash_mismatch')
    if not experiment.get('description', '').startswith('TLDR: '): raise ValueError('registered_tldr_missing')
    if len(tldr) < 80: raise ValueError('condition_tldr_missing')
    for s in ('TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics', 'Launch gates'):
        if '\n## ' + s + '\n' not in markdown: raise ValueError('required_plan_section_missing')
    return {'experiment': EXPERIMENT, 'url': expected_url, 'plan_sha256': expected_hash, 'tldr': tldr,
            'checked_epoch': time.time()}


def check_plan(config, tldr):
    state = json.loads(fetch('https://swarm-live.pages.dev/api/state'))
    exp = next((e for e in state['experiments'] if e['id'] == EXPERIMENT), {})
    url = config['plan_url']
    raw = url.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/')
    return validate_plan(exp, fetch(raw), url, config['plan_sha256'], tldr)


def validate_receipt(receipt, source_commit, now=None):
    now = time.time() if now is None else now
    if receipt.get('experiment') != EXPERIMENT: raise ValueError('allocation_experiment_mismatch')
    if receipt.get('source_commit') != source_commit: raise ValueError('allocation_source_mismatch')
    if not receipt.get('exclusive_claim_verified') or not receipt.get('claim_id') or not receipt.get('host'):
        raise ValueError('fresh_exclusive_claim_required')
    if not 0 <= now - receipt.get('verified_epoch', 0) <= 900: raise ValueError('stale_deployment_verification')
    if receipt.get('claim_until_epoch', 0) < now + 7200: raise ValueError('claim_too_short')
    if receipt.get('reserved_usd') != 15 or receipt.get('max_calls') != 660:
        raise ValueError('new_fifteen_dollar_reservation_required')
    if not receipt.get('authority_allocation_id') or not receipt.get('owner_authorization_ref'):
        raise ValueError('owner_budget_authority_required')
    return receipt


def check_review(config):
    url = config['pre_run_review_url']
    if not re.fullmatch(r'https://github\.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/researchers/vishesh/notes/swarm-of-theseus/v2/reviews/.+-pre\.md', url):
        raise ValueError('immutable_pre_run_review_required')
    raw = url.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/')
    body = fetch(raw)
    if hashlib.sha256(body.encode()).hexdigest() != config['pre_run_review_sha256']:
        raise ValueError('pre_run_review_hash_mismatch')
    if 'Status: ready' not in body and 'Status: diagnostic-only' not in body:
        raise ValueError('pre_run_review_blocked')
    return {'url': url, 'sha256': config['pre_run_review_sha256'], 'checked_epoch': time.time()}
