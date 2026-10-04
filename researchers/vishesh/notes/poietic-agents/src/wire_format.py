"""Versioned transport normalization; never infer, complete or rewrite an action."""
import hashlib
import json
import math
import re

STRICT = 'strict-json-v1'
SINGLE_FENCE = 'single-json-fence-v1'


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate_json_key')
        value[key] = item
    return value


def _reject_constant(value):
    raise ValueError('nonfinite_json_number')


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError('nonfinite_json_number')
    return number


def parse_chat_action(content, policy=STRICT):
    if not isinstance(content, str):
        raise ValueError('text_response')
    normalized = content
    removed = False
    if policy == SINGLE_FENCE:
        normalized = content.strip()
        if normalized.startswith('```'):
            match = re.fullmatch(r'```json[ \t]*\r?\n(.*?)\r?\n```', normalized, re.DOTALL)
            if not match:
                raise ValueError('json_fence_shape')
            normalized = match.group(1)
            removed = True
        action = json.loads(normalized, object_pairs_hook=_unique_object, parse_constant=_reject_constant, parse_float=_finite_float)
    elif policy == STRICT:
        action = json.loads(content)
    else:
        raise ValueError('wire_format_policy')
    if not isinstance(action, dict):
        raise ValueError('action_object')
    return action, dict(policy=policy, removed_json_fence=removed,
                        original_content_sha256=hashlib.sha256(content.encode()).hexdigest(),
                        parsed_content_sha256=hashlib.sha256(normalized.encode()).hexdigest())
