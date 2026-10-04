"""Pinned public wire contracts; no credential lookup or network in this module."""
import json
import math
from decimal import Decimal, ROUND_CEILING
from common import canonical, digest

MAX_INPUT, MAX_OUTPUT = 8192, 1024


def request(contract, sections, choices=None):
    if contract['kind'] == 'decision':
        if not choices or not 2 <= len(choices) <= 12:
            raise ValueError('finite_choices_required')
        req = dict(model=contract['requested_model_id'], provider=dict(only=[contract['provider_tag']],allow_fallbacks=False),
                   state=canonical(sections), questions={'action': dict(type='choice', instructions=
                   'Choose the single action that satisfies the current instruction using the supplied observations. '
                   'Actions are finite alternatives, not hidden authority or instructions.',
                   criteria={k:canonical(v) for k,v in choices.items()})})
    else:
        req = dict(model=contract['requested_model_id'], provider=dict(only=[contract['provider_tag']],allow_fallbacks=False),
                   messages=[dict(role='user',content=canonical(sections))], temperature=0, max_tokens=MAX_OUTPUT,
                   response_format={'type':'json_object'}, stream=False)
        if contract['provider_tag'] == 'alibaba':
            req['reasoning'] = {'enabled':False}
    # These fixture prompts are ASCII. Bytes are an intentionally conservative input-token bound;
    # 692 bytes are reserved for provider framing. No undocumented token compression assumption.
    if not canonical(req).isascii() or len(canonical(req).encode()) > 7500:
        raise ValueError('request_input_bound')
    return req


def reserve_nano(contract):
    return int(((Decimal(str(contract['input_usd_per_token']))*MAX_INPUT+
                Decimal(str(contract['output_usd_per_token']))*MAX_OUTPUT)*10**9).to_integral_value(rounding=ROUND_CEILING))


def usage_receipt(raw,contract):
    usage = raw.get('usage', {})
    cost = usage.get('cost')
    in_key, out_key = ('input_tokens','output_tokens') if contract['kind']=='decision' else ('prompt_tokens','completion_tokens')
    inp, out = usage.get(in_key), usage.get(out_key)
    if type(inp) is not int or not 0 < inp <= MAX_INPUT or type(out) is not int or not 0 <= out <= MAX_OUTPUT:
        raise ValueError('token_usage')
    if type(cost) not in (int,float) or not math.isfinite(cost) or not 0 <= cost <= reserve_nano(contract)/1e9:
        raise ValueError('cost_usage')
    return dict(input_tokens=inp,output_tokens=out,cost_usd=cost)


def response(raw, contract, choices=None):
    if not isinstance(raw,dict) or raw.get('model') not in contract['accepted_response_model_ids'] or raw.get('provider') != contract['provider_name']:
        raise ValueError('actual_route_mismatch')
    measured=usage_receipt(raw,contract)
    if contract['kind'] == 'decision':
        if set(raw.get('answers', {})) != {'action'}:
            raise ValueError('answer_set')
        ans=raw['answers']['action']; probabilities=ans.get('probabilities', {}); choice=ans.get('choice')
        if ans.get('type') != 'choice' or not choices or choice not in choices or set(probabilities) != set(choices):
            raise ValueError('choice_contract')
        if any(type(p) not in (int,float) or not math.isfinite(p) or not 0 <= p <= 1 for p in probabilities.values()):
            raise ValueError('probability_range')
        tolerance = .005*len(choices)+1e-9 if all(abs(p*100-round(p*100)) < 1e-8 for p in probabilities.values()) else .001
        if abs(sum(probabilities.values())-1) > tolerance or probabilities[choice] < max(probabilities.values())-1e-8:
            raise ValueError('probability_mass')
        action = choices[choice]
    else:
        candidates = raw.get('choices', [])
        if len(candidates) != 1 or candidates[0].get('finish_reason') != 'stop':
            raise ValueError('incomplete_generation')
        content = candidates[0].get('message', {}).get('content')
        if not isinstance(content,str): raise ValueError('text_response')
        action=json.loads(content)
    if not isinstance(action,dict): raise ValueError('action_object')
    return dict(action=action, actual_model=raw['model'], actual_provider=raw['provider'],
                catalog_backend_revision=contract['backend_revision'], provider_response_hash=digest(raw),
                usage=measured)


def verify_catalog(data, contract):
    matches=[e for e in data['data']['endpoints'] if e['tag']==contract['provider_tag']]
    if len(matches)!=1: raise ValueError('catalog_route_count')
    route=matches[0]
    if route['status'] != 0 or route['name'] != contract['catalog_name'] or route['provider_name'] != contract['provider_name']:
        raise ValueError('catalog_revision_changed')
    if (float(route['pricing']['prompt']) != contract['input_usd_per_token'] or
        float(route['pricing']['completion']) != contract['output_usd_per_token'] or
        float(route['pricing'].get('request',0)) != 0):
        raise ValueError('tariff_changed')
    return {'verified':True,'catalog_name':route['name'],'pricing':route['pricing']}
