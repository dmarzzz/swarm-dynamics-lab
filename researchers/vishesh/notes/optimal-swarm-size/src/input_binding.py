"""Public-only redundant worker bindings; no evaluator imports or arithmetic."""
import hashlib,json

def binding(public,item,ledger):
    if public['family']!='evidence' or item not in public['items']:raise ValueError('binding_scope')
    j=public['items'].index(item)
    names=['a_'+str(j),'b_'+str(j)]
    if not public['dependencies'][item]:names.append('opening')
    return {'item':item,'rule':public['rules'][item],
            'public_records':{k:public['records'][k] for k in names},
            'prerequisite_artifacts':{k:ledger[k] for k in public['dependencies'][item]}}

def serialized(value):return json.dumps(value,sort_keys=True,separators=(',',':'))
def receipt(value):
    data=serialized(value).encode()
    return {'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}

def futile(outcomes):
    first=[r for r in outcomes if r['assignment']['root']==6]
    if len(first)!=4:return False
    values={(r['assignment']['structure'],r['assignment']['arm']):r['evaluation']['quality'] for r in first}
    return all(values[(s,'bound')]<=values[(s,'full')] for s in ('parallel','chain'))
