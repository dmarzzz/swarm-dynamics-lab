"""Proposed saved-data provenance alternative. Not enabled in native launchers.

Only the model-selected candidate/group citation is examined. Declared values
are checked, never filled from a different document or an evaluator. Literal
quote fidelity stays visible as a separate measurement.
"""
import copy
import typed_policy as tp

def align_source(answer,obs):
    tp.validate(answer,obs)
    docs={d['id']:d for d in obs['documents']}
    if len(docs)!=len(obs['documents']):raise ValueError('ambiguous document IDs')
    result={}
    for candidate,groups in answer['candidate_facts'].items():
        result[candidate]={}
        for group,fields in tp.GROUPS.items():
            item=groups[group];doc=docs.get(item['citation'])
            allowed=doc is not None and doc['id'].startswith(group+'-') and doc['title'].startswith(candidate+' ')
            parsed=tp.excerpt_values(group,doc['text']) if allowed else {}
            quote_exact=bool(item['excerpt']) and allowed and item['excerpt'] in doc['text']
            for field in fields:
                reported=tp.reported_value(item,field);matches=field in parsed and reported==parsed[field]
                result[candidate][field]={'reported':reported,'accepted':copy.deepcopy(reported) if matches else None,'aligned':matches,'citation':item['citation'],'quote_exact':bool(quote_exact),'reason':'explicitly unconfirmed in selected source' if matches and reported is None else 'value verified against selected source' if matches else 'selected source does not support value'}
    return result

def compile_source(answer,obs):
    return tp.compile_aligned(align_source(answer,obs),answer,obs)
