"""Allowlisted HTTP failure metadata; no arbitrary messages/headers leave this boundary."""
import json
import math
from datetime import timezone
from email.utils import parsedate_to_datetime

BODY_LIMIT = 65536
ERROR_TYPES = frozenset({
    'invalid_request_error', 'authentication_error', 'permission_error',
    'not_found_error', 'request_too_large', 'rate_limit_error',
    'api_error', 'overloaded_error',
})
TOKEN_FIELDS = ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')


def retry_seconds(value, now):
    if not isinstance(value, str) or len(value) > 128:
        return None
    try:
        if value.strip().isdigit():
            seconds = float(value.strip())
        else:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                return None
            seconds = max(0., date.astimezone(timezone.utc).timestamp() - now)
        return seconds if math.isfinite(seconds) and 0 <= seconds <= 604800 else None
    except (ValueError, TypeError, OverflowError):
        return None


def http_failure(error, now):
    """Read a bounded body once, discard it, and retain only validated fields.

    Usage here never settles an unresolved reservation or infers actual cost.
    """
    status = error.code if type(error.code) is int and 100 <= error.code <= 599 else None
    result = {'http_status': status, 'provider_error_type': 'unknown', 'provider_error_code': 'unknown',
              'retry_after_seconds': None, 'error_usage': None,
              'error_metadata_state': 'unavailable'}
    try:
        result['retry_after_seconds'] = retry_seconds(error.headers.get('Retry-After'), now)
    except Exception:
        pass
    try:
        raw = error.read(BODY_LIMIT + 1)
        if len(raw) > BODY_LIMIT:
            result['error_metadata_state'] = 'oversized'
            return result
        body = json.loads(raw)
        if not isinstance(body, dict):
            result['error_metadata_state'] = 'malformed'
            return result
        result['error_metadata_state'] = 'parsed'
        detail = body.get('error')
        kind = detail.get('type') if isinstance(detail, dict) else None
        if isinstance(kind, str) and kind in ERROR_TYPES:
            result['provider_error_type'] = kind
        details = detail.get('details') if isinstance(detail, dict) else None
        if isinstance(details, dict) and details.get('error_code') == 'enforced_spend_limit_reached':
            result['provider_error_code'] = 'enforced_spend_limit_reached'
        usage = body.get('usage')
        if isinstance(usage, dict):
            safe = {k: usage[k] for k in TOKEN_FIELDS
                    if type(usage.get(k)) is int and 0 <= usage[k] <= 2**53 - 1}
            result['error_usage'] = safe or None
    except (ValueError, TypeError, UnicodeError, RecursionError):
        result['error_metadata_state'] = 'malformed'
    except Exception:
        result['error_metadata_state'] = 'unavailable'
    return result
