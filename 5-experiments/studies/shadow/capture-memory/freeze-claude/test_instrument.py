#!/usr/bin/env python3
"""Offline instrument checks; no credentials and no requests."""
import copy
import json
import unittest
import run

class InstrumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.plan=run.jread('inputs.json')
    def test_budget(self):
        self.assertEqual(self.plan['nominal_calls'],12+sum(a['calls'] for a in self.plan['assignments']))
        self.assertLessEqual(self.plan['nominal_calls'],1450)
        self.assertEqual(self.plan['nominal_calls'],1248)
    def test_no_answer_metadata(self):
        prompt=run.user_prompt({'1':'cedar','-1':'raven'},[1,1,-1])
        self.assertIn('cedar, cedar, raven',prompt)
        for field in ['true last','majority','original','attacker','correct answer','latest name']:
            self.assertNotIn(field,prompt.lower())
    def test_prefix_capture(self):
        for root in self.plan['roots']:
            self.assertTrue(root['captured'])
            self.assertTrue(all(x<=0.25 for x in root['prefix_series'][-3:]))
            self.assertEqual(len(root['agents']),12)
    def test_fixed_projection_and_wipe(self):
        for root in self.plan['roots']:
            full=run.repair_agents(root,'full','removal')
            short=run.repair_agents(root,'1','removal')
            wipe=run.repair_agents(root,'full','wipe')
            self.assertEqual(len(full),6)
            self.assertEqual(run.frac(full),root['baseline'])
            for i in full:
                self.assertEqual(short[i]['mem'],full[i]['mem'][-1:])
                self.assertEqual(wipe[i]['mem'],[])
                self.assertEqual(short[i]['word'],wipe[i]['word'])
    def test_schedule_and_counts(self):
        for a in self.plan['assignments']:
            if a['stage']=='attack': continue
            root=next(x for x in self.plan['roots'] if x['task_id']==a['task_id'])
            agents=run.repair_agents(root,a['memory'],a['arm'])
            decisions=0
            for pairs in root['schedules']:
                self.assertEqual(sorted(x for p in pairs for x in p),list(range(12)))
                decisions+=len(run.heard_at(agents,pairs))
            self.assertEqual(decisions,a['calls'])
    def test_short_wipe_identical_visible_states(self):
        for root in self.plan['roots']:
            a=run.repair_agents(root,'1','removal'); b=run.repair_agents(root,'1','wipe')
            heard=run.heard_at(a,root['schedules'][0])
            for i,w in heard.items():
                a[i]['mem']=(a[i]['mem']+[w])[-1:]
                b[i]['mem']=(b[i]['mem']+[w])[-1:]
                self.assertEqual(a[i]['mem'],b[i]['mem'])
    def test_unanimous_and_conflict_qualification(self):
        q=self.plan['qualification']
        self.assertEqual(len(q),12)
        self.assertEqual(sum(x['unanimous'] for x in q),4)
        for x in q:
            if not x['unanimous']:
                self.assertNotEqual(1 if sum(x['history'])>0 else -1,x['history'][-1])

if __name__=='__main__': unittest.main()
