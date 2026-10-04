"""Exact Swarm Lab Keychain selection. No printing, fallback or transfer behavior."""
import re
import subprocess

SERVICE = 'swarm-lab-anthropic'
ACCOUNT = 'vishesh'
KEY_PATTERN = re.compile(r'(?<![A-Za-z0-9_-])sk-ant-[A-Za-z0-9_-]+(?![A-Za-z0-9_-])')


class CredentialUnavailable(RuntimeError):
    pass


def load_swarm_lab_anthropic():
    try:
        result = subprocess.run(
            ['security', 'find-generic-password', '-a', ACCOUNT, '-s', SERVICE, '-w'],
            capture_output=True, text=True, timeout=15, check=False)
    except Exception:
        raise CredentialUnavailable('swarm_lab_keychain_unavailable') from None
    if result.returncode != 0:
        raise CredentialUnavailable('swarm_lab_keychain_unavailable')
    keys = KEY_PATTERN.findall(result.stdout)
    if len(keys) != 1 or result.stdout.count('sk-ant-') != 1:
        raise CredentialUnavailable('swarm_lab_keychain_ambiguous_or_invalid')
    return keys[0]


def credential_payload():
    """Only this single value may cross to an admitted experiment worker."""
    return {'SWARM_MODEL_API_KEY': load_swarm_lab_anthropic()}


def validate_payload(payload):
    if type(payload) is not dict or set(payload) != {'SWARM_MODEL_API_KEY'}:
        raise CredentialUnavailable('unexpected_credential_payload')
    key = payload['SWARM_MODEL_API_KEY']
    if type(key) is not str or KEY_PATTERN.fullmatch(key) is None:
        raise CredentialUnavailable('invalid_credential_payload')
