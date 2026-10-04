"""Bounded error classification: never returns provider strings or headers."""
import hashlib,json
LIMIT=16384
KINDS=frozenset(['invalid_request','rate_limit_exceeded','context_length_exceeded','authentication','provider_unavailable','provider_overloaded','timeout','server','unmapped'])
def classify_http(exc):
 raw=exc.read(LIMIT+1);truncated=len(raw)>LIMIT;raw=raw[:LIMIT]
 result={'http_status':int(exc.code),'body_bytes_retained_for_hash':len(raw),'body_truncated':truncated,'body_sha256':hashlib.sha256(raw).hexdigest(),'category':'unclassified','raw_body_retained':False}
 try:
  obj=json.loads(raw);error=obj.get('error',{})
  if not isinstance(error,dict):return result
  metadata=error.get('metadata',{})
  if not isinstance(metadata,dict):metadata={}
  kind=metadata.get('error_type')
  if isinstance(kind,str) and kind in KINDS:result['category']=kind
  # Inspection remains inside this process; only a fixed category leaves it.
  text=json.dumps(error).lower()
  if 'schema is too complex' in text or 'compiled grammar is too large' in text:result['category']='schema_complexity'
 except (ValueError,TypeError,AttributeError):pass
 return result
