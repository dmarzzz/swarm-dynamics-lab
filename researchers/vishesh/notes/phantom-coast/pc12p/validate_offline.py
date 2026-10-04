"""Broad deterministic software challenge sweep, never native evidence."""
import itertools,json
from instrument import *
from native import request

def validate_all():
 n=0;maxerr=0;wrong_copy=0
 for terrain in itertools.product(('LAND','WATER'),repeat=4):
  for accuracy,positive,copies,sources,receipt in itertools.product((.6,.8,.95),(False,True),(1,3,9),(1,3),(None,'LAND','WATER')):
   rs=[[f'o{i}',f's{i}','A','LAND' if positive else 'WATER',accuracy,f'r{j}'] for i in range(sources) for j in range(copies)]
   direct=[['B',terrain[1]]]+([['A',receipt]] if receipt else []);p=packet('offline','A',rs,direct);a=posterior(p);b=enumerated(p);err=max(abs(a[s]-b[s]) for s in SITES);assert err<1e-10;maxerr=max(maxerr,err);n+=1
   if copies>1 and not receipt and abs(posterior(p,False)['A']-a['A'])>.01:wrong_copy+=1
 sizes=[]
 for w in worlds():
  for f,c in arms(w):
   for i in range(10):
    for phase in ('before','after'):
     p=main_packet(w,f,c,i,phase,dict(p=.12345678901234567,label='UNKNOWN',inspect='A') if phase=='after' else None);sizes.append(len(canonical(request(p)).encode()))
 for c in qualification():sizes.append(len(canonical(request(c['packet'])).encode()))
 assert n>=256 and wrong_copy>0 and max(sizes)<=1280
 return dict(evidence_kind='SCRIPTED—NOT MODEL EVIDENCE',parameter_combinations=n,independent_world_enumeration_max_error=maxerr,faulty_origin_blind_detected_cases=wrong_copy,native_packet_shapes_checked=len(sizes),max_body_bytes=max(sizes),calls=0)
if __name__=='__main__':print(json.dumps(validate_all(),indent=2))
