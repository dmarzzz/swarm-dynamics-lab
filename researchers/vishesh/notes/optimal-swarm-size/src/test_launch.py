import json
from pathlib import Path
import unittest
from run_qualification import launch_errors
class Launch(unittest.TestCase):
    def test_draft_cannot_launch(self):
        cfg=json.loads((Path(__file__).parent.parent/'qualification-config.json').read_text())
        errors=launch_errors(cfg)
        for key in ('spending_authorization','stage_cap_microdollars','independent_review_commit','exclusive_machine_claim','public_plan_receipt'):
            self.assertIn('missing:'+key,errors)
        self.assertIn('config_not_ready',errors)
if __name__=='__main__':unittest.main()
