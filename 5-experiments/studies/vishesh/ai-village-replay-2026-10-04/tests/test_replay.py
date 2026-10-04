import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from replay import REVISION, actor_record, digest, eligible, prepare, score, select, validate_splits
from inventory import project


def record(rid='a', minute=1, text='The gate is closed.'):
    return {'id':rid, 'revision':REVISION, 'kind':'tool_evidence',
            'created_at':f'2026-01-01T00:{minute:02d}:00Z',
            'updated_at':f'2026-01-01T00:{minute:02d}:00Z',
            'available_at':f'2026-01-01T00:{minute:02d}:00Z',
            'availability_status':'reviewed', 'redacted':False, 'visible_to':['agent-a'], 'content':text,
            'source_sha256':'a'*64}


def episode(rows):
    return {'id':'dev-1','revision':REVISION,'agent':'agent-a',
            'mode':'historical_visibility','visibility_review_id':'fixture-only',
            'privacy_review_id':'fixture-only','cutoff':'2026-01-01T00:10:00Z',
            'question':'What is the gate status?', 'allowed_records':{r['id']:digest(r) for r in rows},
            'component_id':'component-a','dependency_keys':['artifact-a'],'split':'development'}


class ReplayTests(unittest.TestCase):
    def test_future_update_and_boundary_are_excluded(self):
        rows=[record(),record('future',11),record('tie',10),record('updated',2)]
        rows[-1]['updated_at']='2026-01-01T00:12:00Z'
        visible, excluded=eligible(rows,episode(rows))
        self.assertEqual([r['id'] for r in visible],['a'])
        self.assertEqual(excluded['future_updated_or_boundary_tie'],3)

    def test_visibility_is_not_inferred(self):
        rows=[record(),record('b',2)]
        rows[1]['visible_to']=['agent-b']
        e=episode(rows)
        self.assertEqual(len(eligible(rows,e)[0]),1)
        del e['visibility_review_id']
        with self.assertRaises(ValueError): eligible(rows,e)

    def test_unreviewed_record_excluded(self):
        row=record(); e=episode([row])
        self.assertEqual(eligible([row,record('b',2)],e)[1]['not_reviewed_visible'],1)

    def test_source_mutation_refused(self):
        row=record();e=episode([row]);row['content']='Gate is open.'
        with self.assertRaises(ValueError): eligible([row],e)

    def test_missing_record_refused(self):
        with self.assertRaises(ValueError): eligible([],episode([record()]))

    def test_duplicate_refused(self):
        with self.assertRaises(ValueError): eligible([record(),record()],episode([record()]))

    def test_ambiguous_order_quarantined(self):
        rows=[record(),record('b')]
        self.assertEqual(eligible(rows,episode(rows))[0],[])

    def test_redaction_unknown_and_present_excluded(self):
        rows=[record(),record('b',2)]
        rows[0]['redacted']=True;del rows[1]['redacted']
        self.assertEqual(eligible(rows,episode(rows))[1]['redacted_or_unknown'],2)

    def test_naive_timestamp_and_reverse_time_refused(self):
        for key,value in [('created_at','2026-01-01T00:00:00'),('updated_at','2025-01-01T00:00:00Z')]:
            row=record();row[key]=value
            with self.assertRaises(ValueError): eligible([row],episode([row]))

    def test_evaluator_metadata_does_not_change_payload(self):
        row=record();e=episode([row]);before=prepare([row],e)[0]
        row.update(gold='refuted',family='bad_case',treatment='structured')
        e['allowed_records']={row['id']:digest(row)}
        e.update(gold='unknown',family='new_family')
        self.assertEqual(prepare([row],e)[0],before)
        self.assertNotIn('gold',json.dumps(before))

    def test_recent_complete_record_ceiling(self):
        rows=[actor_record(record()),actor_record(record('b',2,'x'*100))]
        cap=len(json.dumps([rows[0]],ensure_ascii=False,separators=(',',':')))
        self.assertEqual(select(rows,'gate','recent',cap),[rows[0]])
        self.assertEqual(select(rows,'gate','recent',1),[])

    def test_bm25_query_match_and_determinism(self):
        rows=[actor_record(record(text='gate gate closed')),actor_record(record('b',2,'unrelated receipt'))]
        cap=len(json.dumps([rows[0]],ensure_ascii=False,separators=(',',':')))
        self.assertEqual(select(rows,'gate','bm25',cap),[rows[0]])
        self.assertEqual(select(rows,'gate','bm25',1000),select(list(reversed(rows)),'gate','bm25',1000))

    def test_component_and_shared_artifact_leakage(self):
        e=episode([record()]);f=copy.deepcopy(e);f.update(id='eval-1',split='evaluation')
        with self.assertRaises(ValueError):validate_splits([e,f])
        f['component_id']='component-b'
        with self.assertRaises(ValueError):validate_splits([e,f])
        f['dependency_keys']=['artifact-b'];validate_splits([e,f])

    def test_missing_is_not_wrong(self):
        self.assertEqual(score(None,{},{}),{'status':'missing','correct':None})

    def test_valid_id_wrong_label_and_invented_citation_fail(self):
        actor=prepare([record()],episode([record()]))[0];rid=actor['records'][0]['id']
        gold={'label':'refuted','sufficient_citation_sets':[[rid]]}
        self.assertFalse(score({'label':'supported','citations':[rid]},gold,actor)['correct'])
        self.assertFalse(score({'label':'refuted','citations':['invented']},gold,actor)['correct'])
        self.assertTrue(score({'label':'refuted','citations':[rid]},gold,actor)['correct'])

    def test_truth_requires_evidence(self):
        with self.assertRaises(ValueError):score({'label':'supported','citations':[]},{'label':'supported'}, {'records':[]})
        self.assertTrue(score({'label':'unknown','citations':[]},{'label':'unknown'}, {'records':[]})['correct'])

    def test_projection_excludes_provider_messages_and_commands(self):
        row={'id':'a','data':{'actionType':'AGENT_TALK','output':'PRIVATE','command':'DO NOT EXECUTE'},'agent_messages':'PRIVATE'}
        out=json.dumps(project('events',row))
        self.assertNotIn('PRIVATE',out);self.assertNotIn('command',out)


class IntegrationTests(unittest.TestCase):
    def test_every_profile_requires_its_evidence_roles(self):
        profiles=json.loads((Path(__file__).resolve().parents[1]/'profiles.json').read_text())
        for profile in profiles.values():
            row=record();ep=episode([row])
            with self.assertRaises(ValueError):prepare([row],ep,profile=profile)
            ep['evidence_roles']={role:['a'] for role in profile['roles']}
            prepare([row],ep,profile=profile)
            ep['evidence_roles'][profile['roles'][0]]=['absent']
            with self.assertRaises(ValueError):prepare([row],ep,profile=profile)

    def test_normalizer_never_grants_visibility(self):
        from normalize import normalize
        row=normalize('chat_messages',{'id':'a','created_at':'2026-01-01 00:00:00','updated_at':'2026-01-01 00:00:01','content':'A public-looking message'})
        self.assertEqual(row['visible_to'],[])
        self.assertIsNone(row['redacted'])
        self.assertTrue(row['created_at'].endswith('+00:00'))
        self.assertEqual(eligible([row],episode([row]))[0],[])

    def test_cli_retains_unicode_line_separator_inside_json_string(self):
        import tempfile,subprocess
        row=record(text='Evidence before\u2028evidence after')
        ep=episode([row]);ep['evidence_roles']={'target_claim':['a'],'observable_receipt':['a']}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            (path/'records.jsonl').write_text(json.dumps(row,ensure_ascii=False)+'\n')
            (path/'episodes.json').write_text(json.dumps([ep]))
            result=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'src/replay.py'),'--records',str(path/'records.jsonl'),'--episodes',str(path/'episodes.json'),'--episode','dev-1','--study','healing','--out',str(path/'out')],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertNotIn('Evidence before',result.stdout)
            self.assertEqual(json.loads((path/'out/actor.json').read_text())['records'][0]['text'],row['content'])
            self.assertEqual((path/'out/actor.json').stat().st_mode & 0o777,0o600)

    def test_authored_semantic_controls_and_citation_scoring(self):
        cases=json.loads((Path(__file__).parent/'semantic-fixtures.json').read_text())
        self.assertEqual(len(cases),18)
        self.assertEqual(len({c['family'] for c in cases}),6)
        validate_splits([c['episode'] for c in cases])
        for case in cases:
            actor,_=prepare(case['records'],case['episode'])
            gold=case['gold'];citations=gold['sufficient_citation_sets'][0] if gold['sufficient_citation_sets'] else []
            self.assertTrue(score({'label':gold['label'],'citations':citations},gold,actor)['correct'])
            bad='refuted' if gold['label']=='supported' else 'supported'
            self.assertFalse(score({'label':bad,'citations':citations},gold,actor)['correct'])
            self.assertNotIn('family',actor)
            self.assertNotIn('gold',actor)

if __name__=='__main__':unittest.main()
