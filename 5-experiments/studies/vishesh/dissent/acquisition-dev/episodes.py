"""Public authored development worlds. No network, credentials or native dispatch."""
from copy import deepcopy
import hashlib
import json


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build():
    worlds = []

    def world(identity, mechanism, family, domain, requirements, minimum, incumbent, rationale):
        w = {'id': identity, 'mechanism': mechanism, 'structural_family': family,
             'rationale': rationale, 'task': {'domain': domain, 'scope': 'scope-'+digest(identity)[:12],
             'revision': 'r1', 'now': 100, 'deadline': 102, 'ttl': 7,
             'requirements': requirements, 'minimum_authority': minimum,
             'source_authorities': {}, 'rule': 'PROCEED only when all required predicates '
             'have current authoritative true evidence. HOLD when any required predicate '
             'has authoritative false evidence. Otherwise DEFER. For each predicate use '
             'the highest acquired eligible authority, then latest observed_at; tied '
             'contradiction is unresolved. Optional predicates do not govern action.'},
             'incumbent': {'action': incumbent, 'origin': 'scripted'},
             'budget': {'checks': 1, 'credits': 1}, 'initial': [], 'sources': [],
             'gold_by_choice': {}}
        worlds.append(w)
        return w

    def doc(w, origin, facts, at=99, suffix='cached'):
        return {'id': 'evidence-'+digest([w['id'],origin,suffix])[:16], 'origin': origin,
                'scope': w['task']['scope'], 'revision': 'r1', 'observed_at': at,
                'text': '; '.join(k.replace('_', ' ')+' = '+str(v).lower() for k,v in facts.items()),
                'facts': facts}

    def initial(w, origin, rank, facts, at=99):
        w['task']['source_authorities'][origin] = rank
        w['initial'].append(doc(w, origin, facts, at))

    def source(w, identity, description, covers, rank, priority, facts, at=100):
        w['task']['source_authorities'][identity] = rank
        w['sources'].append({'id': identity, 'description': description, 'covers': covers,
            'authority': rank, 'priority': priority, 'latency': 1, 'cost': 1,
            'response': [doc(w, identity, facts, at, 'lookup')]})

    w=world('dev-expiry','metadata_expired','single_predicate', 'software release',
            ['integration_pass'], {'integration_pass':1}, 'HOLD',
            'A formerly passing integration receipt is too old; refresh can justify reopening.')
    initial(w,'build_registry',2,{'integration_pass':True},91)
    source(w,'A','Read the deployment audit receipt',['audit_recorded'],1,2,{'audit_recorded':True})
    source(w,'B','Read the integration test registry',['integration_pass'],2,1,{'integration_pass':True})
    w['gold_by_choice']={'NONE':'DEFER','A':'DEFER','B':'PROCEED'}

    w=world('dev-coverage','missing_conjunct','conjunctive_requirements','software release',
            ['integration_pass','migration_pass'], {'integration_pass':1,'migration_pass':1},
            'PROCEED','The registered release certificate covers integration but not the required migration.')
    initial(w,'release_certificate',2,{'integration_pass':True})
    source(w,'A','Refresh the integration release certificate',['integration_pass'],2,1,{'integration_pass':True})
    source(w,'B','Read the migration test record',['migration_pass'],2,2,{'migration_pass':False})
    w['gold_by_choice']={'NONE':'DEFER','A':'DEFER','B':'HOLD'}

    w=world('dev-authority','authority_supersession','authority_order','data publication',
            ['publication_allowed'], {'publication_allowed':3}, 'PROCEED',
            'The current cached review lacks the authority required for publication; the authoritative source contains a restriction.')
    initial(w,'department_review',1,{'publication_allowed':True})
    source(w,'A','Read the authoritative publication register',['publication_allowed'],3,2,{'publication_allowed':False})
    source(w,'B','Refresh the departmental review',['publication_allowed'],1,1,{'publication_allowed':True})
    w['gold_by_choice']={'NONE':'DEFER','A':'HOLD','B':'DEFER'}

    w=world('dev-conflict','current_conflict','authority_order','equipment return-to-service',
            ['inspection_clear'], {'inspection_clear':1}, 'HOLD',
            'Equally ranked current inspections conflict; the designated higher authority can resolve them.')
    initial(w,'inspector_left',2,{'inspection_clear':True})
    initial(w,'inspector_right',2,{'inspection_clear':False})
    source(w,'A','Read the final inspection register',['inspection_clear'],3,1,{'inspection_clear':True})
    source(w,'B','Read the unchanged right-side inspection',['inspection_clear'],2,2,{'inspection_clear':False},99)
    w['gold_by_choice']={'NONE':'DEFER','A':'PROCEED','B':'DEFER'}

    w=world('dev-unchanged','benign_unchanged','single_predicate','inventory dispatch',
            ['load_clear'], {'load_clear':1}, 'PROCEED',
            'Load clearance is current. An expired cosmetic receipt is irrelevant; needless challenge cannot improve the action.')
    initial(w,'load_register',2,{'load_clear':True})
    initial(w,'cosmetic_register',1,{'cosmetic_clear':False},91)
    source(w,'A','Refresh load clearance',['load_clear'],2,1,{'load_clear':True})
    source(w,'B','Read the cosmetic inspection',['cosmetic_clear'],1,2,{'cosmetic_clear':False})
    w['gold_by_choice']={'NONE':'PROCEED','A':'PROCEED','B':'PROCEED'}

    w=world('dev-unresolved','one_check_insufficient','conjunctive_requirements','inventory dispatch',
            ['supply_clear','transport_clear'], {'supply_clear':1,'transport_clear':1}, 'PROCEED',
            'Two independently required clearances are absent and each source covers only one; one check cannot justify dispatch.')
    source(w,'A','Read supply clearance',['supply_clear'],2,1,{'supply_clear':True})
    source(w,'B','Read transport clearance',['transport_clear'],2,2,{'transport_clear':True})
    w['gold_by_choice']={'NONE':'DEFER','A':'DEFER','B':'DEFER'}
    return deepcopy(worlds)
