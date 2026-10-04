"""Offline-qualified OpenRouter error redaction; no transport or retries."""
import json
from acquisition_d6 import safe_http

def safe_openrouter_error(exc):
    out={**safe_http(exc),'error_body_status':'unreadable','reported_reason':'unknown'}
    try:raw=exc.read(8193)
    except Exception:return out
    if not isinstance(raw,bytes):return out
    if len(raw)>8192:return {**out,'error_body_status':'oversized'}
    try:body=json.loads(raw)
    except (ValueError,UnicodeError,RecursionError):return {**out,'error_body_status':'malformed'}
    error=body.get('error') if isinstance(body,dict) else None
    if not isinstance(error,dict):return {**out,'error_body_status':'unknown_envelope'}
    out['error_body_status']='parsed'
    messages=[error.get('message')]
    metadata=error.get('metadata')
    if isinstance(metadata,dict) and isinstance(metadata.get('raw'),str):
        messages.append(metadata['raw'])
        try:
            upstream=json.loads(metadata['raw'])
            nested=upstream.get('error') if isinstance(upstream,dict) else None
            if isinstance(nested,dict):messages.append(nested.get('message'))
        except (ValueError,RecursionError):pass
    messages=[s.lower() for s in messages if isinstance(s,str)]
    reasons=set()
    for message in messages:
        if ('schema' in message or 'grammar' in message) and any(x in message for x in ('too complex','complexity','compilation timeout','too many','limit exceeded')):reasons.add('schema_complexity')
        elif 'schema' in message and any(x in message for x in ('unsupported','not supported','invalid','must be','is required')):reasons.add('schema_invalid_or_unsupported')
        if 'insufficient credits' in message:reasons.add('insufficient_credits')
        if 'rate limit' in message:reasons.add('rate_limit')
    if len(reasons)==1:out['reported_reason']=next(iter(reasons))
    elif len(reasons)>1:out['reported_reason']='ambiguous'
    return out

REASONS={'unknown','schema_complexity','schema_invalid_or_unsupported','insufficient_credits','rate_limit','ambiguous'}
BODY_STATES={'unreadable','oversized','malformed','unknown_envelope','parsed'}
def safe_relay_error(exc):
    out=safe_http(exc)
    try:
        raw=exc.read(8193)
        if len(raw)>8192:return out
        body=json.loads(raw)
        if isinstance(body,dict):
            if body.get('reported_reason') in REASONS:out['reported_reason']=body['reported_reason']
            if body.get('error_body_status') in BODY_STATES:out['error_body_status']=body['error_body_status']
    except Exception:pass
    return out
