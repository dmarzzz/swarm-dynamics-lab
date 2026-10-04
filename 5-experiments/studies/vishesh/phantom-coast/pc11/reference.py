import itertools
def enumerate_action(qs,h,first):
 """Independent enumeration of world probabilities and conditional action trees."""
 worlds=[]
 for bits in itertools.product((0,1),repeat=4):
  p=1.
  for q,bit in zip(qs,bits):p*=q if bit else 1-q
  if p:worlds.append((bits,p))
 def terminal(ws):return sum(min(sum(w*b[j] for b,w in ws),sum(w*(1-b[j]) for b,w in ws),.25*sum(w for _,w in ws)) for j in range(4))
 def pick(ws,n,i):return sum(solve(sub,n-1) for bit in (0,1) if (sub:=[(b,w) for b,w in ws if b[i]==bit]))
 def solve(ws,n):return terminal(ws) if n==0 else min(pick(ws,n,j) for j in range(4))
 return pick(worlds,h,first)

