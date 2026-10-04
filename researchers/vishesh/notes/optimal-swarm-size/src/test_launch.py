import json
from pathlib import Path
import unittest
from run_qualification import launch_errors
class Launch(unittest.TestCase):
    def test_draft_cannot_launch(self):
        cfg=json.loads((Path(__file__).parent.parent/'qualification-config.json').read_text())
        errors=launch_errors(cfg)
        for key in ('independent_review_commit','exclusive_machine_claim','public_plan_receipt'):
            self.assertIn('missing:'+key,errors)
        self.assertIn('config_not_ready',errors)
        self.assertNotIn('missing:spending_authorization',errors)
        self.assertEqual(cfg['stage_cap_microdollars'],20_000_000)
        self.assertEqual(cfg['episode_cap_microdollars'],2_000_000)
    def test_cap_cannot_exceed_authorization(self):
        cfg=json.loads((Path(__file__).parent.parent/'qualification-config.json').read_text())
        cfg['stage_cap_microdollars']=20_000_001
        self.assertIn('stage_exceeds_authorization',launch_errors(cfg))
        cfg['stage_cap_microdollars']=20_000_000
        cfg['episode_cap_microdollars']=20_000_001
        self.assertIn('episode_exceeds_stage',launch_errors(cfg))


    def test_config_cannot_raise_recorded_allowance(self):
        cfg=json.loads((Path(__file__).parent.parent/'qualification-config.json').read_text())
        cfg['authorized_total_microdollars']=40_000_000
        cfg['stage_cap_microdollars']=40_000_000
        self.assertIn('authorization_record_mismatch',launch_errors(cfg))
        self.assertIn('stage_exceeds_authorization',launch_errors(cfg))

if __name__=='__main__':unittest.main()
