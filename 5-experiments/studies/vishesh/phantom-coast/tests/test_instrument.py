import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import instrument as pc

class Contracts(unittest.TestCase):
    def setUp(self):
        self.w=pc.world(100)
        self.initial=pc.packet(self.w,'A','private','retain',0,0)
        self.previous=[pc.deterministic(self.initial) for _ in range(3)]

    def test_balanced_world_and_whole_grid(self):
        self.assertEqual(len(self.w['truth']),36)
        self.assertEqual(list(self.w['truth'].values()).count('LAND'),12)
        self.assertEqual(len(self.w['exposed']),4)

    def test_holdout_unavailable(self):
        for seed in (200,211,1000):
            with self.assertRaises(ValueError): pc.world(seed)

    def test_first_exposure_counterbalanced(self):
        a=pc.ledger(self.w,'A',0); b=pc.ledger(self.w,'B',0)
        self.assertEqual({r['label'] for r in a['observations']},{'WATER'})
        self.assertEqual({r['label'] for r in b['observations']},{'LAND'})
        self.assertEqual(len(a['observations']),len(b['observations']))

    def test_cumulative_facts_equal(self):
        for step in (1,2): self.assertEqual(pc.ledger(self.w,'A',step),pc.ledger(self.w,'B',step))

    def test_reset_byte_identity(self):
        for actor in range(3):
            payloads=[pc.canonical(pc.packet(self.w,h,c,'reset',2,actor,self.previous))
                      for h in ('A','B') for c in ('private','social')]
            self.assertEqual(len(set(payloads)),1)

    def test_reset_removes_state(self):
        p=pc.packet(self.w,'A','social','reset',2,0,self.previous)
        self.assertIsNone(p['prior']); self.assertEqual(p['peers'],[])

    def test_retention_and_social_manipulation(self):
        p=pc.packet(self.w,'A','social','retain',2,0,self.previous)
        self.assertEqual(p['prior'],self.previous[0]); self.assertEqual(len(p['peers']),3)
        q=pc.packet(self.w,'A','private','retain',2,0,self.previous)
        self.assertEqual(q['peers'],[]); self.assertEqual(q['evidence'],p['evidence'])

    def test_no_truth_or_condition_leakage(self):
        w=copy.deepcopy(self.w); w['truth']={c:'WATER' for c in pc.CELLS}; w['exposed']=[]
        w['condition']='SECRET_EVALUATOR_TAG'
        for r in w['early']+w['fresh']: r['gold']='SECRET_EVALUATOR_TAG'
        self.assertEqual(pc.packet(w,'A','private','retain',0,0),self.initial)
        self.assertNotIn('SECRET_EVALUATOR_TAG',pc.canonical(pc.packet(w,'A','social','reset',2,0)))

    def test_prior_cannot_carry_extra_fields(self):
        self.previous[0]['gold']='LAND'
        with self.assertRaises(ValueError): pc.packet(self.w,'A','social','retain',1,0,self.previous)

    def test_retraction_not_deletion(self):
        f=pc.ledger(self.w,'A',2)
        self.assertEqual(len(f['withdrawn']),4)
        self.assertTrue(set(f['withdrawn'])<={r['id'] for r in f['observations']})

    def test_exact_mapper_recovers(self):
        p=pc.packet(self.w,'A','private','reset',2,0)
        self.assertEqual(pc.deterministic(p)['map'],self.w['truth'])

    def test_equal_time_conflict_unknown(self):
        p=pc.packet(self.w,'A','private','retain',1,0,self.previous)
        m=pc.deterministic(p)['map']
        self.assertTrue(all(m[c]=='UNKNOWN' for c in self.w['exposed']))

    def test_copy_does_not_change_map(self):
        p=copy.deepcopy(self.initial); r=dict(p['evidence']['observations'][0],id='copy')
        p['evidence']['observations'].append(r)
        self.assertEqual(pc.deterministic(p)['map'],pc.deterministic(self.initial)['map'])

    def test_retraction_revokes_copy(self):
        p=copy.deepcopy(self.initial); r=dict(p['evidence']['observations'][0],id='copy')
        p['evidence']['observations'].append(r); p['evidence']['withdrawn']=[r['acquisition_id']]
        self.assertEqual(pc.deterministic(p)['map'][r['cell']],'UNKNOWN')

    def test_conflicting_copy_rejected(self):
        p=copy.deepcopy(self.initial); r=dict(p['evidence']['observations'][0],id='copy',label='LAND')
        p['evidence']['observations'].append(r)
        with self.assertRaises(ValueError): pc.deterministic(p)

    def test_schema_rejects_missing_cell(self):
        x=copy.deepcopy(self.previous[0]); del x['map']['0,0']
        with self.assertRaises(ValueError): pc.response(x,set())

    def test_schema_rejects_hallucinated_source(self):
        x=copy.deepcopy(self.previous[0]); x['evidence_ids']=['invented']
        with self.assertRaises(ValueError): pc.response(x,set())

    def test_schema_rejects_invalid_label(self):
        x=copy.deepcopy(self.previous[0]); x['map']['0,0']='MAYBE'
        with self.assertRaises(ValueError): pc.response(x,set())

    def test_fixed_quorum(self):
        one=dict(map={c:'LAND' for c in pc.CELLS},evidence_ids=[])
        self.assertEqual(set(pc.aggregate([one,None,None]).values()),{'UNKNOWN'})
        self.assertEqual(set(pc.aggregate([one,one,None]).values()),{'LAND'})

    def test_all_missing_error_bounds(self):
        b=pc.bounds({},self.w['truth'])
        self.assertEqual((b['lower'],b['upper'],b['missing']),(0,1,36))

    def test_partial_missing_hand_calculation(self):
        cells=list(pc.CELLS); pred=dict(self.w['truth'])
        pred[cells[0]]='UNKNOWN'; pred[cells[1]]='LAND' if self.w['truth'][cells[1]]=='WATER' else 'WATER'
        b=pc.bounds(pred,self.w['truth'])
        self.assertEqual((b['lower'],b['upper']),(1/36,2/36))

    def test_disagreement_missing_not_agreement(self):
        self.assertEqual(pc.disagreement({},self.w['truth'])['upper'],1)
        self.assertEqual(pc.disagreement(self.w['truth'],self.w['truth'])['upper'],0)

    def test_schedule_count_and_dependencies(self):
        a=pc.assignments(100)
        self.assertEqual(len(a),87); self.assertEqual(len({r['id'] for r in a}),87)
        self.assertEqual([r['step'] for r in a],sorted(r['step'] for r in a))
        self.assertEqual(sum(r['kind']=='pooled' for r in a),12)

    def test_unstarted_preserved(self):
        a=pc.assignments(100); r=pc.reconcile(a,[dict(id=a[0]['id'],status='timeout')])
        self.assertEqual(r['assigned'],87); self.assertEqual(r['counts']['not-started'],86)

    def test_duplicate_and_unknown_outcome_rejected(self):
        a=pc.assignments(100); r=dict(id=a[0]['id'],status='valid')
        for rows in ([r,r],[dict(id='invented',status='valid')]):
            with self.assertRaises(ValueError): pc.reconcile(a,rows)

    def test_pooled_and_clean_inputs(self):
        rows=pc.assignments(100)
        clean=next(a for a in rows if a['kind']=='clean')
        p=pc.request_for_assignment(self.w,clean)
        self.assertEqual(len(p['evidence']['observations']),36); self.assertEqual(p['peers'],[])
        pooled=next(a for a in rows if a['kind']=='pooled' and a['step']==0)
        q=pc.request_for_assignment(self.w,pooled)
        self.assertEqual(len(q['evidence']['observations']),4)

    def test_replay_metrics_match_every_frame(self):
        for fail in (False,True):
            trace=pc.fixtures(fail=fail)
            self.assertIn('NO MODEL CALLS',trace['mode'])
            for f in trace['frames']:
                self.assertEqual(f['metrics'],pc.bounds(f['map'],trace['truth']))
                self.assertEqual(f['map'],pc.aggregate(f['outcomes']))
            self.assertEqual(trace['frames'][-1]['metrics']['upper'],1 if fail else 0)

    def test_interaction_hand_calculation(self):
        land={c:'LAND' for c in pc.CELLS}; water={c:'WATER' for c in pc.CELLS}
        maps={(h,c,s):land for h in ('A','B') for c in ('social','private') for s in ('retain','reset')}
        maps['B','social','retain']=water
        self.assertEqual(pc.history_interaction(maps),{'lower':1,'upper':1})
        self.assertEqual(pc.history_interaction({}),{'lower':-2,'upper':2})

    def test_declared_sensor_reliability(self):
        p=pc.packet(self.w,'A','private','reset',2,0)
        self.assertEqual({r['reliability'] for r in p['evidence']['observations'] if r['epoch']==0},{0.8})
        self.assertEqual({r['reliability'] for r in p['evidence']['observations'] if r['epoch']==2},{1.0})

if __name__=='__main__': unittest.main()
