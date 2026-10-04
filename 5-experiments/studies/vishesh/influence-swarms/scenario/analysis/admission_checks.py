"""Pure admission validators, used before credential selection; no secret output."""
import datetime

def verify_claims(servers,claims,host,claim_id,operator,now):
 if host not in servers:raise ValueError('unregistered destination')
 claim=claims.get(claim_id,{})
 def live(c):
  return c.get('status') in ('running','active') and datetime.datetime.fromisoformat(c['until'].replace('Z','+00:00'))>now
 if not live(claim) or claim.get('shared') is not False or claim.get('by')!=operator or claim.get('experiment')!='influence-swarms' or claim.get('servers')!=[host]:raise ValueError('exclusive current claim required')
 if any(k!=claim_id and live(c) and host in c.get('servers',[]) for k,c in claims.items()):raise ValueError('conflicting allocation')
 return claim

def validate_envelope(value,validate_secret):
 if type(value) is not dict or set(value)!= {'secret','routing'}:raise ValueError('unexpected envelope')
 validate_secret(value['secret'])
 import re
 r=value['routing']
 if type(r) is not dict or set(r)!= {'workspace_id'} or not isinstance(r['workspace_id'],str) or not re.fullmatch(r'wrkspc_[A-Za-z0-9]+',r['workspace_id']):raise ValueError('unexpected routing payload')
