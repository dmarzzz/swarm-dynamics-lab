import importlib.util,json,sys,tempfile,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import native
from corpus import source_controller,canonical
from prepare import ROOT
from report import analyze,validate_annotations
sp=importlib.util.spec_from_file_location('b2_test_ledger',ROOT.parent/'src/ledger.py');lm=importlib.util.module_from_spec(sp);sp.loader.exec_module(lm)

class NativeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.out=self.root/'run'
        self.ledger=lm.Ledger(self.root/'budget.sqlite',5000000000,'original Telephone USD5 authority')
        self.ledger.reserve('history','A1','infrastructure',113744701,'historical');self.ledger.settle('history',113744701)
        self.ledger.reserve('infra','B2-allocation','infrastructure',250000000,'allocation')
        self.p=native.packet();self.count=0
    def tearDown(self):self.ledger.db.close();self.tmp.cleanup()
    def fake(self,req):
        self.count+=1;e=json.loads(req['messages'][1]['content'])
        if 'source_packet'in e:
            src=e['source_packet'];text='\n'.join(r['text'] for r in src['records'])
            decision=('HOLD' if 'unknown'in text else 'GO') if len(src['records'])==1 else source_controller(src)
            obj={'handoff':text,'decision':decision}
        else:obj=e['previous_handoff']
        return {'id':f'gen-{self.count}','model':native.base.MODEL,'provider':'OpenAI','choices':[{'finish_reason':'stop','message':{'role':'assistant','content':canonical(obj)}}],
                'usage':{'prompt_tokens':500,'completion_tokens':300,'total_tokens':800,'cost':.004}}
    def qualified(self):
        native.qualify(self.p,self.out,self.ledger,self.fake,time.time()+5000)
        return {'manifest_sha256':self.p['manifest_sha256'],'assessor':'offline fixture',
                'responses':{cid:{'response_sha256':native.sha(json.loads((self.out/(cid+'.response.json')).read_text())),'decision_rule_preserved':True,'uncertainty_preserved':True,'rationale':'Fixture copied full explicit rule and uncertainty.'} for cid in ('q01','q02')}}
    def test_full_packet_original_ledger_and_replay(self):
        review=self.qualified();self.assertEqual(self.ledger.summary()['total_upper_nano'],4942880845)
        result=native.main_run(self.p,self.out,self.ledger,self.fake,time.time()+5000,review)
        self.assertEqual((result['valid'],result['unstarted'],self.count),(144,0,146))
        report=analyze(self.out);self.assertEqual(report['observed_valid_calls'],144);self.assertEqual(len(report['semantic_annotations']),1008)
        self.assertEqual(report['blocks'][0]['assigned_bounds'],[0,0]);self.assertEqual(report['repeat_disagreement']['P']['decision_disagreements'],0)
        self.assertFalse(report['semantic_review_complete']);self.assertFalse(report['fresh_run_stability_accepted'])
        with self.assertRaises(ValueError):validate_annotations(report,report['semantic_annotations'])
        with self.assertRaises(FileExistsError):native.main_run(self.p,self.out,self.ledger,self.fake,time.time()+5000,review)
    def test_failed_return_retains_raw_stops_and_releases_only_unstarted(self):
        review=self.qualified()
        def bad(req):r=self.fake(req);r['provider']='Other';return r
        result=native.main_run(self.p,self.out,self.ledger,bad,time.time()+5000,review)
        self.assertEqual((result['failed'],result['unstarted']),(1,143))
        self.assertEqual(len(native.release_unstarted(self.p,self.out,self.ledger,True)),143)
        self.assertEqual(self.ledger.summary()['unresolved_model_calls'],1)
        self.assertEqual(analyze(self.out)['blocks'][0]['assigned_bounds'],[-1,1])
    def test_failed_qualification_blocks_main(self):
        review=self.qualified();review['responses']['q02']['uncertainty_preserved']=False
        with self.assertRaises(ValueError):native.main_run(self.p,self.out,self.ledger,self.fake,time.time()+5000,review)
        self.assertEqual(self.count,2)
    def test_budget_packet_reservation_is_atomic(self):
        self.ledger.reserve('other','other','model',2000000,'existing')
        with self.assertRaises(ValueError):native.reserve_packet(self.p,self.ledger)
        self.assertEqual(self.ledger.db.execute("SELECT COUNT(*) FROM charges WHERE stage='B2'").fetchone()[0],0)
    def test_semantic_mistake_kept_without_intervention(self):
        review=self.qualified()
        def wrong(req):
            r=self.fake(req);r['choices'][0]['message']['content']=canonical({'handoff':'All requirements met.','decision':'GO'});return r
        result=native.main_run(self.p,self.out,self.ledger,wrong,time.time()+5000,review)
        self.assertEqual(result['valid'],144);report=analyze(self.out)
        self.assertEqual(sum(r['outcome']=='false_go' for r in report['rows']),72)
        self.assertFalse(report['blocks'][0]['first_hop_competence']['P']['screen_passed'])
    def test_replay_detects_modified_parent_context(self):
        review=self.qualified();native.main_run(self.p,self.out,self.ledger,self.fake,time.time()+5000,review)
        a=next(r for r in self.p['assignments'] if r['hop']==2);f=self.out/(a['id'].replace(':','_')+'.request.json')
        req=json.loads(f.read_text());req['messages'][1]['content']='{}';f.write_text(json.dumps(req))
        with self.assertRaises(ValueError):analyze(self.out)
    def test_admission_blocks_missing_flags_or_changed_transport(self):
        f=self.root/'bridge.py';f.write_text('# offline fixture')
        a={'stage':'B2','manifest_sha256':self.p['manifest_sha256'],'model':native.base.MODEL,'pi_decision_id':'test-only',
           'additional_cap_nano':4884624146,'cumulative_cap_nano':5000000000,'deadline':time.time()+5000,'claim_expires':time.time()+6000,
           'public_plan_url':'https://example.invalid/test-only','transport_sha256':native.file_sha(f),'infrastructure_reservation_id':'infra'}
        for k in ('portfolio_reserved','public_plan_verified','condition_tldrs_registered','account_verified','exclusive_claim_verified','worker_idle_verified','runtime_verified'):a[k]=True
        native.check_admission(self.p,a,self.ledger,f)
        a['exclusive_claim_verified']=False
        with self.assertRaises(ValueError):native.check_admission(self.p,a,self.ledger,f)
        self.assertEqual(self.count,0)
    def test_crash_start_marker_keeps_reservation(self):
        self.qualified();a=self.p['assignments'][0];(self.out/(a['id'].replace(':','_')+'.started.json')).write_text('{}')
        self.assertEqual(len(native.release_unstarted(self.p,self.out,self.ledger,True)),143)
        self.assertEqual(self.ledger.summary()['unresolved_model_calls'],1)

if __name__=='__main__':unittest.main()
