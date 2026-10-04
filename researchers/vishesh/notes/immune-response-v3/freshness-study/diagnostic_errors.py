"""Bounded error classification: arbitrary provider text never leaves this function."""
import json,hashlib
KEYWORDS=('anyOf','allOf','additionalProperties','required','type','enum','properties','reason')
REASONS={'unknown','schema_invalid_or_unsupported','schema_complexity','insufficient_credits','rate_limit'}
def safe_error(exc):
 out={'body_status':'unreadable','reported_reason':'unknown','keywords':[]}
 try:raw=exc.read(8193)
 except Exception:return out
 if not isinstance(raw,bytes):return out
 if len(raw)>8192:return {**out,'body_status':'oversized'}
 out['body_sha256']=hashlib.sha256(raw).hexdigest()
 try:body=json.loads(raw)
 except (ValueError,UnicodeError,RecursionError):return {**out,'body_status':'malformed'}
 if not isinstance(body,dict):return {**out,'body_status':'unknown_envelope'}
 # Locally generated relay envelope: copy only fixed-vocabulary diagnostics.
 if body.get('error')=='provider_http':
  out['body_status']=body.get('body_status') if body.get('body_status') in {'unreadable','oversized','malformed','unknown_envelope','parsed'} else 'unknown_envelope'
  out['reported_reason']=body.get('reported_reason') if body.get('reported_reason') in REASONS else 'unknown'
  out['keywords']=[k for k in KEYWORDS if isinstance(body.get('keywords'),list) and k in body['keywords']]
  return out
 error=body.get('error')
 if not isinstance(error,dict):return {**out,'body_status':'unknown_envelope'}
 out['body_status']='parsed';messages=[error.get('message')];metadata=error.get('metadata')
 if isinstance(metadata,dict) and isinstance(metadata.get('raw'),str):
  messages.append(metadata['raw'])
  try:
   inner=json.loads(metadata['raw']);e=inner.get('error') if isinstance(inner,dict) else None
   if isinstance(e,dict):messages.append(e.get('message'))
  except (ValueError,RecursionError):pass
 text=' '.join(x for x in messages if isinstance(x,str));lower=text.lower()
 if ('schema' in lower or 'grammar' in lower) and any(k in lower for k in ['invalid','unsupported','not supported','must','required','not allowed']):out['reported_reason']='schema_invalid_or_unsupported'
 if ('schema' in lower or 'grammar' in lower) and any(k in lower for k in ['too complex','complexity','compilation timeout','too many']):out['reported_reason']='schema_complexity'
 if 'insufficient credits' in lower:out['reported_reason']='insufficient_credits'
 if 'rate limit' in lower:out['reported_reason']='rate_limit'
 out['keywords']=[k for k in KEYWORDS if k.lower() in lower]
 return out
