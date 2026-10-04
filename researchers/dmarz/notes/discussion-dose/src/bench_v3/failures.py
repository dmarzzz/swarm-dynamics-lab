"""Public failure metadata is an allowlist, never exception text or class names."""
import json
import socket
import urllib.error

REASONS = frozenset(('provider_timeout', 'provider_rate_limit', 'provider_credit_balance_low',
                     'provider_http_error', 'provider_transport_error', 'provider_schema_refusal',
                     'provider_incomplete', 'provider_malformed_output', 'provider_model_mismatch',
                     'provider_accounting_error', 'provider_local_limit', 'provider_unknown'))


def safe_failure(exc):
    reason = getattr(exc, 'public_reason', None)
    status = getattr(exc, 'http_status', None)
    if isinstance(exc, urllib.error.HTTPError): status = exc.code
    if status is None and type(reason) is str and reason.startswith('provider_http_') and reason[14:].isdigit():
        status = int(reason[14:])
    if reason not in REASONS:
        if reason == 'provider_http_429' or status == 429: reason = 'provider_rate_limit'
        elif isinstance(exc, (TimeoutError, socket.timeout)): reason = 'provider_timeout'
        elif type(status) is int: reason = 'provider_http_error'
        elif isinstance(exc, urllib.error.URLError):
            reason = 'provider_timeout' if isinstance(exc.reason, (TimeoutError, socket.timeout)) else 'provider_transport_error'
        elif isinstance(exc, (json.JSONDecodeError, ValueError)): reason = 'provider_malformed_output'
        elif type(status) is int or (type(reason) is str and reason.startswith('provider_http_') and reason[14:].isdigit()):
            if status is None: status = int(reason[14:])
            reason = 'provider_http_error'
        else: reason = 'provider_unknown'
    status_class = str(status // 100) + 'xx' if type(status) is int and 100 <= status <= 599 else None
    return {'reason': reason, 'http_status_class': status_class}
