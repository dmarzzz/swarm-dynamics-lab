"""Allowlisted error receipts. Never retain free-form messages, headers or metadata."""
import email.utils
import json
import time

TYPES = frozenset(('rate_limit_exceeded', 'provider_overloaded', 'provider_unavailable',
    'authentication', 'permission_denied', 'payment_required', 'invalid_request',
    'invalid_prompt', 'not_found', 'precondition_failed', 'payload_too_large',
    'unprocessable', 'context_length_exceeded', 'max_tokens_exceeded',
    'token_limit_exceeded', 'content_policy_violation', 'refusal', 'server', 'timeout', 'unmapped'))
LIMIT_SOURCES = frozenset(('openrouter_in_flight_budget', 'openrouter_key_limit', 'openrouter_credits'))
REASONS = frozenset(('in_flight_budget_exhausted', 'weight_exceeds_budget'))
PROVIDER_CODES = frozenset(('rate_limited', 'rate_limit_error', 'rate_limit_exceeded',
    'insufficient_quota', 'insufficient_credits', 'overloaded_error', 'resource_exhausted'))
MARKERS = ('response_format', 'json', 'model', 'provider', 'unsupported', 'not found',
    'credits', 'quota', 'rate', 'max_tokens', 'authentication', 'region', 'parameter', 'stream', 'valid')
FIELDS = frozenset(('error_type', 'http_status', 'diagnostic_code', 'error_markers',
    'body_error_status', 'provider_error_type', 'provider_code', 'provider_name',
    'limit_source', 'limit_reason', 'retry_after_seconds', 'rate_limit', 'rate_remaining', 'rate_reset'))


def _bounded_integer(value, maximum):
    if isinstance(value, str) and value.isascii() and value.isdecimal() and len(value) <= 12:
        value = int(value)
    return value if type(value) is int and 0 <= value <= maximum else None


def retry_after(value, now=None):
    seconds = _bounded_integer(value, 86400)
    if seconds is not None:
        return seconds
    if not isinstance(value, str) or len(value) > 64:
        return None
    try:
        date = email.utils.parsedate_to_datetime(value)
        if date.tzinfo is None:
            return None
        seconds = date.timestamp() - (time.time() if now is None else now)
        return max(0, round(seconds)) if -86400 <= seconds <= 86400 else None
    except (ValueError, TypeError, OverflowError):
        return None


def has_provider_error(raw):
    if not isinstance(raw, dict):
        return False
    if isinstance(raw.get('error'), dict):
        return True
    choices = raw.get('choices', [])
    return isinstance(choices, list) and any(isinstance(c, dict) and
        (isinstance(c.get('error'), dict) or c.get('finish_reason') == 'error') for c in choices)


def safe_error(http_status, body, headers=None, expected_provider=None, now=None):
    result = {'error_type': 'provider_http' if http_status != 200 else 'provider_body_error',
              'http_status': http_status}
    if isinstance(body, bytes):
        try:
            body = json.loads(body[:32000])
        except (ValueError, UnicodeError):
            body = {}
    if not isinstance(body, dict):
        body = {}
    error = body.get('error')
    if not isinstance(error, dict):
        candidates = body.get('choices', [])
        error = next((x['error'] for x in candidates if isinstance(x, dict) and isinstance(x.get('error'), dict)), {}) if isinstance(candidates, list) else {}
    code = _bounded_integer(error.get('code'), 599)
    if code is not None and code >= 400:
        result['body_error_status'] = code
    meta = error.get('metadata', {})
    if not isinstance(meta, dict):
        meta = {}
    for source, target, allowed in [('error_type','provider_error_type',TYPES),
                                  ('provider_code','provider_code',PROVIDER_CODES),
                                  ('limit_source','limit_source',LIMIT_SOURCES),
                                  ('reason','limit_reason',REASONS)]:
        value = meta.get(source)
        if isinstance(value, str) and value in allowed:
            result[target] = value
    if expected_provider and meta.get('provider_name') == expected_provider:
        result['provider_name'] = expected_provider
    message = error.get('message', '')
    result['error_markers'] = [word for word in MARKERS if isinstance(message,str) and word in message.lower()]
    headers = headers or {}
    value = retry_after(headers.get('Retry-After'), now)
    if value is not None:
        result['retry_after_seconds'] = value
    for key, field in [('X-RateLimit-Limit','rate_limit'), ('X-RateLimit-Remaining','rate_remaining'), ('X-RateLimit-Reset','rate_reset')]:
        value = _bounded_integer(headers.get(key), 10_000_000_000)
        if value is not None:
            result[field] = value
    return result


class ProviderBodyError(Exception):
    """Carries only an already-sanitized receipt; used for HTTP200 error envelopes."""
    def __init__(self, receipt):
        super().__init__('provider_body_error')
        self.receipt = receipt
