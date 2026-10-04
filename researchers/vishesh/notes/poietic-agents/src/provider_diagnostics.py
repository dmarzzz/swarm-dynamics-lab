"""Allowlisted error receipts. Never retain free-form messages, headers or metadata."""
import email.utils
import math
import json
import time

TYPES = frozenset(('rate_limit_exceeded', 'provider_overloaded', 'provider_unavailable',
    'authentication', 'permission_denied', 'payment_required', 'invalid_request',
    'invalid_prompt', 'not_found', 'precondition_failed', 'payload_too_large',
    'unprocessable', 'context_length_exceeded', 'max_tokens_exceeded',
    'token_limit_exceeded', 'content_policy_violation', 'refusal', 'server', 'timeout', 'unmapped'))
LIMIT_SOURCES = frozenset(('openrouter_in_flight_budget', 'openrouter_key_limit', 'openrouter_credits', 'upstream_provider_shared_pool'))
REASONS = frozenset(('in_flight_budget_exhausted', 'weight_exceeds_budget'))
PROVIDER_CODES = frozenset(('rate_limited', 'rate_limit_error', 'rate_limit_exceeded',
    'insufficient_quota', 'insufficient_credits', 'overloaded_error', 'resource_exhausted'))
MARKERS = ('response_format', 'json', 'model', 'provider', 'unsupported', 'not found',
    'credits', 'quota', 'rate', 'max_tokens', 'authentication', 'region', 'parameter', 'stream', 'valid')
FIELDS = frozenset(('error_type', 'http_status', 'diagnostic_code', 'error_markers',
    'body_error_status', 'provider_error_type', 'provider_code', 'provider_name',
    'limit_source', 'limit_reason', 'retry_after_seconds', 'rate_limit', 'rate_remaining', 'rate_reset',
    'provider_status', 'expected_provider', 'provider_name_source', 'provider_name_mismatch', 'provenance',
    'quota_hints', 'diagnostic_conflicts', 'retry_eligible_envelope', 'output_present'))


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
        return max(0, math.ceil(seconds)) if -86400 <= seconds <= 86400 else None
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


KNOWN_PROVIDERS = frozenset(('DekaLLM','DeepInfra','Anthropic','Alibaba','Google','OpenAI'))


def _object(value):
    if isinstance(value, bytes):
        if len(value)>32000:return {}
        try:value=json.loads(value)
        except (ValueError,UnicodeError,RecursionError):return {}
    elif isinstance(value,str):
        if len(value)>32000:return {}
        try:value=json.loads(value)
        except (ValueError,RecursionError):return {}
    return value if isinstance(value,dict) else {}


def _safe_headers(headers, now):
    if not hasattr(headers,'items'):return {}
    lowered={str(k).lower():v for k,v in headers.items() if isinstance(k,str) and k.lower() in
             ('retry-after','x-ratelimit-limit','x-ratelimit-remaining','x-ratelimit-reset')}
    out={};v=retry_after(lowered.get('retry-after'),now)
    if v is not None:out['retry_after_seconds']=v
    for key,field in [('x-ratelimit-limit','rate_limit'),('x-ratelimit-remaining','rate_remaining'),('x-ratelimit-reset','rate_reset')]:
        v=_bounded_integer(lowered.get(key),10_000_000_000)
        if v is not None:out[field]=v
    return out


def safe_error(http_status, body, headers=None, expected_provider=None, now=None):
    """Project fixed enums/numbers only, including JSON embedded in metadata.raw.

    Expected routing is a separate field, never evidence of the observed provider.
    Arbitrary text/headers and unrecognized fields never enter the receipt.
    """
    result={'error_type':'provider_http' if http_status!=200 else 'provider_body_error','http_status':http_status}
    body=_object(body);error=body.get('error')
    if not isinstance(error,dict):
        choices=body.get('choices',[])
        error=next((x['error'] for x in choices if isinstance(x,dict) and isinstance(x.get('error'),dict)),{}) if isinstance(choices,list) else {}
    code=_bounded_integer(error.get('code'),599)
    if code is not None and code>=400:result['body_error_status']=code
    meta=_object(error.get('metadata'));raw=_object(meta.get('raw'));raw_error=_object(raw.get('error'))
    sources=[('error.metadata',meta),('error.metadata.raw.error.metadata',_object(raw_error.get('metadata'))),
             ('error.metadata.raw.error',raw_error),('error.metadata.raw',raw)]
    provenance={};conflicts=set()
    specs=[('error_type','provider_error_type',TYPES),('type','provider_error_type',TYPES),
           ('provider_code','provider_code',PROVIDER_CODES),('provider_error_code','provider_code',PROVIDER_CODES),
           ('code','provider_code',PROVIDER_CODES),('limit_source','limit_source',LIMIT_SOURCES),('reason','limit_reason',REASONS)]
    for location,fields in sources:
        for source,target,allowed in specs:
            value=fields.get(source)
            if isinstance(value,str) and value in allowed:
                if target in result and result[target]!=value:conflicts.add(target)
                if target not in result:result[target]=value;provenance[target]=location+'.'+source
    if isinstance(expected_provider,str) and expected_provider in KNOWN_PROVIDERS:result['expected_provider']=expected_provider
    for location,fields in sources:
        for key in ('provider_code','provider_error_code','code'):
            status=_bounded_integer(fields.get(key),599)
            if status is not None and status>=400:
                if 'provider_status' in result and result['provider_status']!=status:conflicts.add('provider_status')
                if 'provider_status' not in result:
                    result['provider_status']=status;provenance['provider_status']=location+'.'+key
        provider=fields.get('provider_name')
        if isinstance(provider,str) and provider in KNOWN_PROVIDERS:
            if 'provider_name' not in result:
                result['provider_name']=provider;result['provider_name_source']=location+'.provider_name'
                result['provider_name_mismatch']=bool(expected_provider and provider!=expected_provider)
            elif provider!=result['provider_name']:conflicts.add('provider_name')
    message=error.get('message','')
    result['error_markers']=[w for w in MARKERS if isinstance(message,str) and w in message.lower()]
    hints=[]
    for location,h in [('http.headers',headers)]+[(loc+'.headers',fields.get('headers')) for loc,fields in sources]:
        values=_safe_headers(h,now)
        if values:
            hints.append(dict(source=location,**values))
            for field,value in values.items():
                if field not in result:result[field]=value;provenance[field]=location
                elif field=='retry_after_seconds' and value>result[field]:result[field]=value;provenance[field]=location
    if hints:result['quota_hints']=hints
    if provenance:result['provenance']=provenance
    if conflicts:result['diagnostic_conflicts']=sorted(conflicts)
    output=any(obj.get(k) not in (None,[],{},'') for obj in (body,raw) for k in ('choices','output','content','text','answers','message','id'))
    result['output_present']=output
    usage=body.get('usage');unbilled=usage is None or (isinstance(usage,dict) and all(type(x) in (int,float) and x==0 for x in usage.values()))
    result['retry_eligible_envelope']=bool(http_status==429 and isinstance(body.get('error'),dict) and code==429 and not output and unbilled)
    return result


class ProviderBodyError(Exception):
    """Carries only an already-sanitized receipt; used for HTTP200 error envelopes."""
    def __init__(self, receipt):
        super().__init__('provider_body_error')
        self.receipt = receipt
