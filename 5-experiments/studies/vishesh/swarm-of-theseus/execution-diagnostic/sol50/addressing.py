"""Exact current-roster address resolution. Never repairs a wrong peer choice."""
def resolve_pair(values,roster,owner):
    if not isinstance(values,list) or len(values)!=2 or any(not isinstance(x,str) for x in values):raise ValueError('pair_shape')
    aliases={};positions=set();identities=set()
    for row in roster:
        if not isinstance(row,dict) or set(row)!={'position','identity'}:raise ValueError('roster_shape')
        position,identity=row['position'],row['identity']
        if not isinstance(position,str) or not isinstance(identity,str) or position in positions or identity in identities:raise ValueError('ambiguous_roster')
        positions.add(position);identities.add(identity)
        for alias in (position,identity):
            if alias in aliases and aliases[alias]!=position:raise ValueError('ambiguous_alias')
            aliases[alias]=position
    if owner not in positions:raise ValueError('unknown_owner')
    if any(x not in aliases for x in values):raise ValueError('unknown_or_retired_address')
    resolved=[aliases[x] for x in values]
    if len(set(resolved))!=2 or owner in resolved:raise ValueError('duplicate_or_self')
    return resolved
