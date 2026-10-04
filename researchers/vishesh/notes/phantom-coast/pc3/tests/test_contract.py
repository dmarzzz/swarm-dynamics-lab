import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import *

class Contract(unittest.TestCase):
    def setUp(self):self.w=development_world(600)
    def test_reserved_worlds_rejected(self):
        for seed in (200,700,800,1000,True):
            with self.assertRaises(ValueError):development_world(seed)
    def test_geometry_families(self):
        for family in ('block','scattered'):
            w=development_world(601,family);self.assertEqual(sum(v=='LAND' for v in w['truth'].values()),12);self.assertEqual(len(w['region']),4)
            self.assertTrue(all(w['truth'][c]=='LAND' for c in w['region']))
            if family=='scattered':
                for a in w['region']:
                    for b in w['region']:
                        if a!=b:self.assertGreater(sum(abs(int(x)-int(y)) for x,y in zip(a.split(','),b.split(','))),1)
    def test_all_cells_always_legal(self):
        e=Episode(self.w);c=self.w['region'][0]
        for _ in range(12):self.assertEqual(e.packet()['cells'],list(CELLS));e.step([c,c,c])
        self.assertEqual(metrics(e,reconstruct(e.packet()))['unique_cells'],1)
        with self.assertRaises(ValueError):e.step([c,c,c])
    def test_no_future_truth_or_condition_in_packet(self):
        e=Episode(self.w);before=e.packet();e.world['truth']={c:'WATER' for c in CELLS};e.world['family']='hidden';e.guard_cell='5,5'
        self.assertEqual(e.packet(),before)
        self.assertFalse({'truth','family','region','seed','guard','guard_cell','policy'}&set(before))
    def test_round_barrier_and_copy_isolation(self):
        e=Episode(self.w);p=e.packet();self.assertEqual(p['previous_proposals'],[])
        e.step(['0,0','0,1','0,2']);self.assertEqual(len(e.packet()['previous_proposals']),3)
        p['evidence']['observations'].clear();self.assertEqual(len(e.observations),5)
    def test_condition_only_changes_report_labels(self):
        a,b=[Episode(self.w,report=x).packet() for x in ('misleading','benign')]
        for p in (a,b):
            for r in p['evidence']['observations']:r['label']='MASK'
        self.assertEqual(a,b)
    def test_guard_removes_measured_choices_and_never_falls_back(self):
        e=Episode(self.w,guard=True);c='0,0'
        e.step([c]*3);self.assertNotIn(c,e.packet()['legal_cells'])
        e.step([c]*3);self.assertIsNone(e.events[-1]['target'])
        self.assertEqual(e.events[-1]['valid_proposals'],0)
        self.assertEqual(len(e.events),2)
    def test_guard_unique_path_and_missing_quorum(self):
        e=Episode(self.w,guard=True)
        for _ in range(12):e.step([e.legal()[0]]*3)
        self.assertEqual(metrics(e,reconstruct(e.packet()))['unique_cells'],12)
        self.assertFalse(any(x['repeated'] for x in e.events))
        f=Episode(self.w,guard=True)
        for _ in range(6):f.step([None]*3)
        self.assertEqual(sum(x['target'] is None for x in f.events),6)
    def test_no_single_survivor_team_action(self):
        e=Episode(self.w);x=e.step(['0,0',None,'invalid']);self.assertIsNone(x['target']);self.assertEqual(len(e.events),1)
    def test_plurality_and_frozen_ties(self):
        e=Episode(self.w);self.assertEqual(e.step(['0,0','0,1','0,1'])['target'],'0,1')
        a=Episode(self.w);b=Episode(self.w);self.assertEqual(a.step(['0,0','0,1','0,2'])['target'],b.step(['0,2','0,0','0,1'])['target'])
    def test_assignment_cardinality_required(self):
        with self.assertRaises(ValueError):Episode(self.w).step(['0,0'])
        with self.assertRaises(ValueError):Episode(self.w,policy='single').step(['0,0','0,1'])
        with self.assertRaises(ValueError):Episode(self.w,policy='uniform').step(['0,0'])
    def test_uniform_schedule_paired_and_no_replacement(self):
        a=Episode(self.w,policy='uniform');b=Episode(self.w,report='benign',policy='uniform')
        aa=[a.step()['target'] for _ in range(12)];bb=[b.step()['target'] for _ in range(12)]
        self.assertEqual(aa,bb);self.assertEqual(len(set(aa)),12)
    def test_guard_does_not_reveal_report_truth(self):
        a=Episode(self.w,guard=True);b=Episode(self.w,report='benign',guard=True)
        self.assertEqual(a.legal(),b.legal());self.assertEqual(a.legal(),list(CELLS))
        for p in ('team','single','uniform'):
            x=Episode(self.w,policy=p);y=Episode(self.w,policy=p,guard=True)
            self.assertEqual(x.uniform,y.uniform);self.assertEqual(x.order,y.order)
    def test_observation_overrides_report_without_retraction(self):
        e=Episode(self.w);c=self.w['region'][0];self.assertEqual(reconstruct(e.packet())[c],'WATER');e.step([c,c,c]);self.assertEqual(reconstruct(e.packet())[c],'LAND')
        self.assertEqual(e.packet()['evidence']['withdrawn'],[])
    def test_duplicate_acquisition_not_new_evidence(self):
        p=Episode(self.w).packet();p['evidence']['observations'].append(dict(p['evidence']['observations'][0],id='copy'))
        p['evidence']['withdrawn']=['copy'];self.assertEqual(reconstruct(p)[p['evidence']['observations'][0]['cell']],'UNKNOWN')
        p['evidence']['observations'][-1]['label']='LAND'
        with self.assertRaises(ValueError):reconstruct(p)
    def test_fixed_majority_missing_maps(self):
        truth=self.w['truth'];m=majority([truth,None,None]);self.assertEqual(error(m,truth)['upper'],1)
        self.assertEqual(majority([truth,truth,None]),truth)
    def test_empty_and_wrong_maps_are_not_success(self):
        self.assertEqual(error({},self.w['truth'])['upper'],1)
        wrong={c:'WATER' if v=='LAND' else 'LAND' for c,v in self.w['truth'].items()}
        self.assertEqual(error(wrong,self.w['truth'])['lower'],1)
    def test_no_visits_censored_and_no_denominator(self):
        e=Episode(self.w);m=metrics(e,{})
        self.assertIsNone(m['observed']['upper']);self.assertFalse(m['first_visit_censored']);self.assertIsNone(m['first_report_visit'])
        for _ in range(12):e.step([None]*3)
        self.assertTrue(metrics(e,{})['first_visit_censored'])
    def test_coverage_not_inferred_from_prediction(self):
        e=Episode(self.w);m=metrics(e,self.w['truth']);self.assertEqual(m['whole']['upper'],0);self.assertEqual(m['unique_cells'],0)
    def test_repeat_ids_unique_but_coverage_fixed(self):
        e=Episode(self.w);e.step(['0,0']*3);e.step(['0,0']*3)
        self.assertNotEqual(e.events[0]['observation']['acquisition_id'],e.events[1]['observation']['acquisition_id']);self.assertTrue(e.events[1]['repeated'])

if __name__=='__main__':unittest.main()
