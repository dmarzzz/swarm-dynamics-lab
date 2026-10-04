"""Offline policy contract; no provider, credential or dispatch functions."""
import re
from decimal import Decimal

def normalized(token,locale):
 if locale not in {'ID','MY'} or not isinstance(token,str):return None
 s=token.strip()
 if re.fullmatch(r'\d+',s):pass
 elif re.fullmatch(r'\d{1,3}(?:[.,]\d{3})+',s):
  # Mixed thousands separators are invalid.
  marks=set(re.findall(r'[^\d]',s))
  if len(marks)!=1:return None
  s=re.sub(r'[.,]','',s)
 elif re.fullmatch(r'\d+\.\d{2}',s):pass
 elif locale=='ID' and re.fullmatch(r'\d+,\d{2}',s):s=s.replace(',','.')
 elif re.fullmatch(r'\d{1,3}(?:,\d{3})+\.\d{2}',s):s=s.replace(',','')
 elif locale=='ID' and re.fullmatch(r'\d{1,3}(?:\.\d{3})+,\d{2}',s):s=s.replace('.','').replace(',','.')
 else:return None
 return format(Decimal(s),'.2f')

def direct(r):
 if not isinstance(r,dict) or r.get('decision')!='accept':return None
 a=r.get('amount');return a if isinstance(a,str) and re.fullmatch(r'\d+\.\d{2}',a) else None

def literal(r,locale):
 if not isinstance(r,dict) or r.get('decision')!='accept':return None
 return normalized(r.get('token'),locale)

def policies(d1,d2,a,b,c,locale):
 da,db=direct(d1),direct(d2);la,lb=literal(a,locale),literal(b,locale)
 at=a.get('token') if isinstance(a,dict) else None;bt=b.get('token') if isinstance(b,dict) else None
 ct=c.get('token') if isinstance(c,dict) else None
 eq=lambda x,y:isinstance(x,str) and isinstance(y,str) and x.strip()==y.strip()
 return {'direct':da if da is not None and da==db else None,'literal':la,
 'blind':la if la is not None and la==lb and eq(at,bt) else None,
 'conditioned':la if la is not None and c.get('verified') is True and eq(at,ct) else None}

def outcome(value,gold):
 if value is None:return 'refer'
 if gold is None:return 'unsupported_accept'
 return 'correct' if value==gold else 'wrong_accept'

def admission(manifest):
 assert len(manifest)==56,'expected48scorable_plus8unresolved'
 ids=[c['id'] for c in manifest];assert len(ids)==len(set(ids)),'duplicate_id'
 hashes=[c['image_sha256'] for c in manifest];assert len(hashes)==len(set(hashes)),'duplicate_image'
 main=[c for c in manifest if c['gold'] is not None];assert len(main)==48
 families={c['family'] for c in main};assert len(families)>=24,'too_few_families'
 assert all(sum(c['family']==f for c in main)<=2 for f in families),'family_overrepresented'
 for loc in ['ID','MY']:
  for quality in ['clear','degraded']:
   assert sum(c['locale']==loc and c['quality']==quality for c in main)==12,'unfilled_stratum'
   assert sum(c['locale']==loc and c['quality']==quality and c['gold'] is None for c in manifest)==2
 for c in manifest:
  assert c['prior_exposure'] is False and c['pixel_reviewed'] is True
  assert c['gold'] is None or c['label_status']=='adjudicated'
 return {'scorable_receipts':48,'unresolved_receipts':8,'family_count':len(families)}
