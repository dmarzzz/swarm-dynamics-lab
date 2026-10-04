"""Pinned OpenRouter wire adapter. Transport/credentials are injected, never discovered.

UTF-8 bytes plus 1024 framing tokens is a conservative admission estimate, not a
provider tokenizer measurement. Reported usage must also fit the admitted bound.
Actual router charge is retained for ledger settlement; token list-price
charge is cross-checked with one nanodollar rounding tolerance. No retries, tools, model/provider fallback, or implicit credential lookup.
"""
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from contract import MODEL, MAX_INPUT, MAX_OUTPUT, canonical, validate_count

ROUTER_MODEL = 'anthropic/claude-haiku-4.5'
PROVIDER = 'Anthropic'
ENDPOINT = 'https://openrouter.ai/api/v1/chat/completions'


def build_request(req):
    if (set(req) != {'model','max_tokens','temperature','system','messages'} or
        req['model'] != MODEL or req['max_tokens'] != MAX_OUTPUT or
        req['temperature'] != 0 or not isinstance(req['system'], str) or
        not isinstance(req['messages'], list) or len(req['messages']) != 1):
        raise ValueError('openrouter_request_contract')
    message = req['messages'][0]
    if set(message) != {'role','content'} or message['role'] != 'user' or not isinstance(message['content'], str):
        raise ValueError('openrouter_message_contract')
    return {'model': ROUTER_MODEL,
            'messages': [{'role':'system','content':req['system']}, dict(message)],
            'max_tokens': MAX_OUTPUT, 'temperature': 0, 'stream': False,
            'reasoning': {'enabled':False},
            'provider': {'order':['anthropic'], 'only':['anthropic'],
                         'allow_fallbacks':False, 'require_parameters':True,
                         'data_collection':'deny',
                         'max_price':{'prompt':1,'completion':5}}}


def count_tokens(req):
    # Byte-level vocabulary cannot require more text tokens than UTF-8 bytes;
    # explicit framing reserve covers two messages and system wrapping.
    wire = build_request(req)
    return validate_count(len(canonical(wire).encode('utf-8')) + 1024)


def normalize(raw, input_bound=MAX_INPUT):
    validate_count(input_bound)
    if (not isinstance(raw, dict) or raw.get('error') or
        raw.get('model') != ROUTER_MODEL or raw.get('provider') != PROVIDER or
        not isinstance(raw.get('id'),str) or not raw['id']):
        raise ValueError('openrouter_route')
    choices = raw.get('choices')
    if not isinstance(choices,list) or len(choices) != 1:
        raise ValueError('openrouter_choices')
    choice = choices[0]; message = choice.get('message', {})
    if (choice.get('finish_reason') != 'stop' or
        choice.get('native_finish_reason', 'end_turn') not in ('end_turn','stop') or
        message.get('role') != 'assistant' or not isinstance(message.get('content'),str) or
        not message['content'].strip() or message.get('tool_calls') or
        message.get('function_call') or message.get('reasoning') or
        message.get('reasoning_details') or message.get('refusal')):
        raise ValueError('openrouter_completion')
    usage = raw.get('usage', {})
    inp = validate_count(usage.get('prompt_tokens')); out = usage.get('completion_tokens')
    if inp > input_bound or type(out) is not int or not 0 < out <= MAX_OUTPUT:
        raise ValueError('openrouter_usage_bound')
    if usage.get('total_tokens') != inp + out:
        raise ValueError('openrouter_total_usage')
    prompt_details = usage.get('prompt_tokens_details') or {}
    completion_details = usage.get('completion_tokens_details') or {}
    if (any(prompt_details.get(k,0) != 0 for k in ('cached_tokens','cache_write_tokens','audio_tokens','video_tokens')) or
        any(completion_details.get(k,0) != 0 for k in ('reasoning_tokens','audio_tokens')) or
        usage.get('is_byok',False) is not False):
        raise ValueError('openrouter_extra_usage')
    try:
        if isinstance(usage.get('cost'),bool) or usage.get('cost') is None:
            raise ValueError('openrouter_cost_missing')
        cost = Decimal(str(usage['cost']))
        if not cost.is_finite() or cost < 0:
            raise ValueError('openrouter_cost_invalid')
        cost_nano = int((cost * 1000000000).to_integral_value(rounding=ROUND_CEILING))
    except (InvalidOperation, TypeError):
        raise ValueError('openrouter_cost_invalid') from None
    list_cost = inp*1000 + out*5000
    if cost_nano > list_cost + 1:
        raise ValueError('openrouter_cost_exceeds_reserved_rate')
    return {'role':'assistant','model':MODEL,'stop_reason':'end_turn',
            'content':[{'type':'text','text':message['content']}],
            'usage':{'input_tokens':inp,'output_tokens':out},
            'openrouter':{'model':raw['model'],'provider':raw['provider'],
                          'generation_id':raw['id'],'actual_cost_nano':cost_nano,
                          'token_rate_cost_nano':list_cost,
                          'input_bound_method':'utf8_wire_bytes_plus_1024',
                          'input_bound':input_bound},
            'openrouter_response':raw}


def generate(req, post_json):
    """Call injected transport exactly once; do not log exceptions or credentials."""
    bound = count_tokens(req)
    return normalize(post_json(build_request(req)), bound)
