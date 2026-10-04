"""Offline reference for collective consultation; never fixes a native action."""
from itertools import permutations

def decide(required, receipts, epoch):
    # A receipt is relevant only when attributed to the required specialist and
    # the current epoch. Unknown or stale acknowledgments cannot authorize work.
    by={who:[r['allow'] for r in receipts if r['who']==who and r['epoch']==epoch] for who in required}
    if any(not values or len(set(values))!=1 for values in by.values()):return 'defer'
    return 'allow' if all(values[0] for values in by.values()) else 'hold'

def fixtures():
    base=[{'who':'b','epoch':1,'allow':True},{'who':'e','epoch':1,'allow':True}]
    return [
        ('both_current',('b','e'),base,'allow'),
        ('one_veto',('b','e'),[base[0],dict(base[1],allow=False)],'hold'),
        ('missing_second',('b','e'),base[:1],'defer'),
        ('stale_second',('b','e'),[base[0],dict(base[1],epoch=0)],'defer'),
        ('conflicting_second',('b','e'),base+[dict(base[1],allow=False)],'defer'),
        ('responsibility_changed',('b','f'),base,'defer'),
        ('changed_with_fresh_proof',('b','f'),[base[0],dict(base[1],who='f')],'allow'),
        ('irrelevant_third_veto',('b','e'),base+[{'who':'a','epoch':1,'allow':False}],'allow')]

def validate():
    checks=0
    for _,required,receipts,expected in fixtures():
        assert decide(required,receipts,1)==expected;checks+=1
        for perm in permutations(receipts):assert decide(required,perm,1)==expected;checks+=1
        names={c:chr(ord('u')+n) for n,c in enumerate('abcdef')}
        renamed=[dict(r,who=names[r['who']]) for r in receipts]
        assert decide(tuple(names[x] for x in required),renamed,1)==expected;checks+=1
    return {'evidence_type':'scripted_collective_reference','native_calls':0,'distinct_cases':8,'invariant_checks':checks,'native_consultation_qualified':False}
if __name__=='__main__':
    import json
    print(json.dumps(validate(),indent=2))
