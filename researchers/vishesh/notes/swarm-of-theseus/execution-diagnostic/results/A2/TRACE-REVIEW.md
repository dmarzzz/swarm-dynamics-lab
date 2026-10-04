# A2 native trace review

All started request/response pairs were checked for request hashes, provider translation, served route, accounting and raw-text scoring. All twelve learner outputs and every qualification miss are represented below. This is the owning-agent audit; no independent review claimed. Operator prompts and transcripts were excluded.

## Learner outputs and visible counterexamples

### A2-7304-incident-learn

Expected {"A": "canary", "B": "probe"}; returned {"mapping": {"A": "probe", "B": "ledger"}, "support": {"A": ["c3018b5d9349deaf", "1aef04dc96729e9a"], "B": ["521f2fe9f935bebe", "4e5b632b431d6f1e"]}}.

Qualified: False. Compatible sources: {"A": ["canary"], "B": ["probe"]}.

Counterexamples to asserted mapping: [{"class": "A", "id": "1743af89a548f6bb", "observed": "quiet", "asserted_source_prediction": "activated"}, {"class": "A", "id": "1aef04dc96729e9a", "observed": "activated", "asserted_source_prediction": "quiet"}, {"class": "B", "id": "fb4d753d4811b5a9", "observed": "quiet", "asserted_source_prediction": "activated"}, {"class": "B", "id": "4e5b632b431d6f1e", "observed": "activated", "asserted_source_prediction": "quiet"}].

### A2-7300-release-learn

Expected {"A": "probe", "B": "ledger"}; returned {"mapping": {"A": "probe", "B": "ledger"}, "support": {"A": ["768865a305977311", "9dbed3ebb3fe5e35", "5908b3a8e9252868"], "B": ["a66b4682aec789f4", "d1b0f493a44bc522", "8059d4b4418f0493"]}}.

Qualified: True. Compatible sources: {"A": ["probe"], "B": ["ledger"]}.

Counterexamples to asserted mapping: [].

### A2-7302-incident-learn

Expected {"A": "ledger", "B": "probe"}; returned {"mapping": {"A": "canary", "B": "ledger"}, "support": {"A": ["77a4013d1a43e480", "16eef0e4290ec300", "45e4ef118650ad19"], "B": ["415640e1ea3687fb", "39e021b538b9f14b", "3fb667a2f618a02d"]}}.

Qualified: False. Compatible sources: {"A": ["ledger"], "B": ["probe"]}.

Counterexamples to asserted mapping: [{"class": "A", "id": "16eef0e4290ec300", "observed": "quiet", "asserted_source_prediction": "activated"}, {"class": "A", "id": "d7acf6d42072102f", "observed": "activated", "asserted_source_prediction": "quiet"}, {"class": "B", "id": "39e021b538b9f14b", "observed": "quiet", "asserted_source_prediction": "activated"}, {"class": "B", "id": "7689d316a966cc36", "observed": "activated", "asserted_source_prediction": "quiet"}].

### A2-7302-release-learn

Expected {"A": "ledger", "B": "probe"}; returned {"mapping": {"A": "ledger", "B": "ledger"}, "support": {"A": ["d7acf6d42072102f", "77a4013d1a43e480", "16eef0e4290ec300", "45e4ef118650ad19"], "B": ["3fb667a2f618a02d", "415640e1ea3687fb", "39e021b538b9f14b", "7689d316a966cc36"]}}.

Qualified: False. Compatible sources: {"A": ["ledger"], "B": ["probe"]}.

Counterexamples to asserted mapping: [{"class": "B", "id": "39e021b538b9f14b", "observed": "hold", "asserted_source_prediction": "ship"}, {"class": "B", "id": "3fb667a2f618a02d", "observed": "ship", "asserted_source_prediction": "hold"}].

### A2-7305-incident-learn

Expected {"A": "canary", "B": "ledger"}; returned {"mapping": {"A": "canary", "B": "ledger"}, "support": {"A": ["72868463fa9b5e7a", "ad168e8b54e873e7"], "B": ["9648186555d7c172", "eacf09d07d5c7f83"]}}.

Qualified: True. Compatible sources: {"A": ["canary"], "B": ["ledger"]}.

Counterexamples to asserted mapping: [].

### A2-7304-release-learn

Expected {"A": "canary", "B": "probe"}; returned {"mapping": {"A": "canary", "B": "probe"}, "support": {"A": ["1aef04dc96729e9a", "faecfa0f1af52e09"], "B": ["4e5b632b431d6f1e", "a4e659fa1e265043"]}}.

Qualified: True. Compatible sources: {"A": ["canary"], "B": ["probe"]}.

Counterexamples to asserted mapping: [].

### A2-7301-release-learn

Expected {"A": "probe", "B": "canary"}; returned {"mapping": {"A": "probe", "B": "ledger"}, "support": {"A": ["130a7152aef20050"], "B": ["2ae1e64100222fc5"]}}.

Qualified: False. Compatible sources: {"A": ["probe"], "B": ["canary"]}.

Counterexamples to asserted mapping: [{"class": "B", "id": "338d2c0eced2d91b", "observed": "hold", "asserted_source_prediction": "ship"}, {"class": "B", "id": "2ae1e64100222fc5", "observed": "ship", "asserted_source_prediction": "hold"}].

### A2-7303-incident-learn

Expected {"A": "ledger", "B": "canary"}; returned {"mapping": {"A": "ledger", "B": "canary"}, "support": {"A": ["6b75fedc97406156", "58d5599d44b01c09", "ea112eea6e517544"], "B": ["8b4188da9db104c4", "4aad8c3d4722ab21", "32b4418505071113"]}}.

Qualified: True. Compatible sources: {"A": ["ledger"], "B": ["canary"]}.

Counterexamples to asserted mapping: [].

### A2-7305-release-learn

Expected {"A": "canary", "B": "ledger"}; returned {"mapping": {"A": "probe", "B": "canary"}, "support": {"A": ["860300e4b1116f20", "72868463fa9b5e7a", "ad168e8b54e873e7"], "B": ["9648186555d7c172", "eacf09d07d5c7f83", "d16bc0d270b51b6d"]}}.

Qualified: False. Compatible sources: {"A": ["canary"], "B": ["ledger"]}.

Counterexamples to asserted mapping: [{"class": "A", "id": "860300e4b1116f20", "observed": "hold", "asserted_source_prediction": "ship"}, {"class": "A", "id": "72868463fa9b5e7a", "observed": "ship", "asserted_source_prediction": "hold"}, {"class": "B", "id": "9648186555d7c172", "observed": "ship", "asserted_source_prediction": "hold"}, {"class": "B", "id": "eacf09d07d5c7f83", "observed": "hold", "asserted_source_prediction": "ship"}].

### A2-7303-release-learn

Expected {"A": "ledger", "B": "canary"}; returned {"mapping": {"A": "ledger", "B": "canary"}, "support": {"A": ["6b75fedc97406156", "62f758669cc61361", "ea112eea6e517544"], "B": ["8b4188da9db104c4", "f0e68082f4f9e9d9", "4aad8c3d4722ab21"]}}.

Qualified: True. Compatible sources: {"A": ["ledger"], "B": ["canary"]}.

Counterexamples to asserted mapping: [].

### A2-7301-incident-learn

Expected {"A": "probe", "B": "canary"}; returned {"mapping": {"A": "probe", "B": "ledger"}, "support": {"A": ["130a7152aef20050", "e01516b1b3d8b261"], "B": ["338d2c0eced2d91b", "2ae1e64100222fc5"]}}.

Qualified: False. Compatible sources: {"A": ["probe"], "B": ["canary"]}.

Counterexamples to asserted mapping: [{"class": "B", "id": "338d2c0eced2d91b", "observed": "quiet", "asserted_source_prediction": "activated"}, {"class": "B", "id": "93b9eb0f67b86a17", "observed": "activated", "asserted_source_prediction": "quiet"}].

### A2-7300-incident-learn

Expected {"A": "probe", "B": "ledger"}; returned {"mapping": {"A": "probe", "B": "ledger"}, "support": {"A": ["768865a305977311", "5908b3a8e9252868", "9dbed3ebb3fe5e35"], "B": ["a66b4682aec789f4", "8059d4b4418f0493", "d1b0f493a44bc522"]}}.

Qualified: True. Compatible sources: {"A": ["probe"], "B": ["ledger"]}.

Counterexamples to asserted mapping: [].

## Incorrect executor decisions

- {"id": "A2-7301-incident-learned-2", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": false, "signal": true}}, "id": "f15577cb22d4b4dc", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "probe", "B": "canary"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "canary", "returned_action": "ledger", "action_under_supplied_policy": "ledger", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"f15577cb22d4b4dc\",\"command\":\"console1/ledger\"}]}", "valid_response": true}
- {"id": "A2-7302-incident-learned-4", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": true}, "ledger": {"fresh": false, "signal": false}, "probe": {"fresh": true, "signal": true}}, "id": "62dbe468fe59acf0", "queue": "west", "summary": "needs attention"}, "true_policy": {"A": "ledger", "B": "probe"}, "supplied_policy": {"A": "canary", "B": "ledger"}, "correct_action": "probe", "returned_action": "none", "action_under_supplied_policy": "none", "classification": "policy_induced", "raw_text": "{\"decisions\": [{\"id\": \"62dbe468fe59acf0\", \"command\": \"console1/none\"}]}", "valid_response": true}
- {"id": "A2-7304-incident-learned-4", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": false}, "ledger": {"fresh": true, "signal": true}, "probe": {"fresh": false, "signal": false}}, "id": "016981125ac5fc5d", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "probe"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "none", "returned_action": "ledger", "action_under_supplied_policy": "ledger", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"016981125ac5fc5d\",\"command\":\"console1/ledger\"}]}", "valid_response": true}
- {"id": "A2-7304-incident-learned-0", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": true, "signal": false}, "ledger": {"fresh": false, "signal": false}, "probe": {"fresh": false, "signal": true}}, "id": "f590685f50961e43", "queue": "west", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "probe"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "none", "returned_action": "probe", "action_under_supplied_policy": "probe", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"f590685f50961e43\",\"command\":\"console1/probe\"}]}", "valid_response": true}
- {"id": "A2-7304-incident-learned-5", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": true, "signal": false}, "probe": {"fresh": false, "signal": true}}, "id": "7256f2506911c964", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "probe"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "probe", "returned_action": "none", "action_under_supplied_policy": "none", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"7256f2506911c964\",\"command\":\"console1/none\"}]}", "valid_response": true}
- {"id": "A2-7305-release-learned-2", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": true, "signal": false}, "ledger": {"fresh": false, "signal": false}, "probe": {"fresh": true, "signal": true}}, "id": "d9b932812255e21e", "queue": "east", "summary": "needs attention"}, "true_policy": {"A": "canary", "B": "ledger"}, "supplied_policy": {"A": "probe", "B": "canary"}, "correct_action": "hold", "returned_action": "ship", "action_under_supplied_policy": "ship", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"d9b932812255e21e\",\"command\":\"console1/ship\"}]}", "valid_response": true}
- {"id": "A2-7305-release-learned-7", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": false}, "ledger": {"fresh": true, "signal": true}, "probe": {"fresh": false, "signal": true}}, "id": "cbd89f6fe86b9a8b", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "ledger"}, "supplied_policy": {"A": "probe", "B": "canary"}, "correct_action": "ship", "returned_action": "hold", "action_under_supplied_policy": "hold", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"cbd89f6fe86b9a8b\",\"command\":\"console1/hold\"}]}", "valid_response": true}
- {"id": "A2-7304-incident-learned-1", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": true, "signal": false}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": true, "signal": true}}, "id": "c8086b3435fa5b61", "queue": "east", "summary": "needs attention"}, "true_policy": {"A": "canary", "B": "probe"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "probe", "returned_action": "ledger", "action_under_supplied_policy": "ledger", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"c8086b3435fa5b61\",\"command\":\"console1/ledger\"}]}", "valid_response": true}
- {"id": "A2-7301-release-learned-2", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": false, "signal": true}}, "id": "f15577cb22d4b4dc", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "probe", "B": "canary"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "ship", "returned_action": "hold", "action_under_supplied_policy": "hold", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"f15577cb22d4b4dc\",\"command\":\"console1/hold\"}]}", "valid_response": true}
- {"id": "A2-7302-incident-learned-3", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": true, "signal": false}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": true, "signal": true}}, "id": "5178e08fa1c9e5b8", "queue": "west", "summary": "looks clear"}, "true_policy": {"A": "ledger", "B": "probe"}, "supplied_policy": {"A": "canary", "B": "ledger"}, "correct_action": "ledger", "returned_action": "none", "action_under_supplied_policy": "none", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"5178e08fa1c9e5b8\",\"command\":\"console1/none\"}]}", "valid_response": true}
- {"id": "A2-7302-incident-learned-6", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": false}, "ledger": {"fresh": true, "signal": true}, "probe": {"fresh": false, "signal": true}}, "id": "2fb698875857eb94", "queue": "west", "summary": "looks clear"}, "true_policy": {"A": "ledger", "B": "probe"}, "supplied_policy": {"A": "canary", "B": "ledger"}, "correct_action": "probe", "returned_action": "ledger", "action_under_supplied_policy": "ledger", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"2fb698875857eb94\",\"command\":\"console1/ledger\"}]}", "valid_response": true}
- {"id": "A2-7302-incident-learned-0", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": false, "signal": true}, "ledger": {"fresh": true, "signal": true}, "probe": {"fresh": true, "signal": false}}, "id": "75cf78ad74bccfc8", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "ledger", "B": "probe"}, "supplied_policy": {"A": "canary", "B": "ledger"}, "correct_action": "ledger", "returned_action": "canary", "action_under_supplied_policy": "canary", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"75cf78ad74bccfc8\",\"command\":\"console1/canary\"}]}", "valid_response": true}
- {"id": "A2-7305-release-learned-4", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": true, "signal": false}, "probe": {"fresh": false, "signal": false}}, "id": "bd17c07c7bcf112d", "queue": "west", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "ledger"}, "supplied_policy": {"A": "probe", "B": "canary"}, "correct_action": "ship", "returned_action": "hold", "action_under_supplied_policy": "hold", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"bd17c07c7bcf112d\",\"command\":\"console1/hold\"}]}", "valid_response": true}
- {"id": "A2-7301-incident-learned-3", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": true}, "ledger": {"fresh": true, "signal": false}, "probe": {"fresh": false, "signal": false}}, "id": "32b05d0cf45eb3cb", "queue": "west", "summary": "looks clear"}, "true_policy": {"A": "probe", "B": "canary"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "canary", "returned_action": "none", "action_under_supplied_policy": "none", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"32b05d0cf45eb3cb\",\"command\":\"console1/none\"}]}", "valid_response": true}
- {"id": "A2-7301-incident-learned-4", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": false}, "ledger": {"fresh": true, "signal": true}, "probe": {"fresh": true, "signal": false}}, "id": "8254c44590cde260", "queue": "east", "summary": "needs attention"}, "true_policy": {"A": "probe", "B": "canary"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "none", "returned_action": "ledger", "action_under_supplied_policy": "ledger", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"8254c44590cde260\",\"command\":\"console1/ledger\"}]}", "valid_response": true}
- {"id": "A2-7304-incident-learned-3", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": true, "signal": false}, "probe": {"fresh": true, "signal": false}}, "id": "f01d17440d729ff1", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "probe"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "canary", "returned_action": "none", "action_under_supplied_policy": "none", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"f01d17440d729ff1\",\"command\":\"console1/none\"}]}", "valid_response": true}
- {"id": "A2-7301-release-learned-4", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": false, "signal": false}, "ledger": {"fresh": true, "signal": true}, "probe": {"fresh": true, "signal": false}}, "id": "8254c44590cde260", "queue": "east", "summary": "needs attention"}, "true_policy": {"A": "probe", "B": "canary"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "hold", "returned_action": "ship", "action_under_supplied_policy": "ship", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"8254c44590cde260\",\"command\":\"console1/ship\"}]}", "valid_response": true}
- {"id": "A2-7305-release-learned-0", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": false, "signal": false}}, "id": "aafaf7b467516cc3", "queue": "west", "summary": "needs attention"}, "true_policy": {"A": "canary", "B": "ledger"}, "supplied_policy": {"A": "probe", "B": "canary"}, "correct_action": "hold", "returned_action": "ship", "action_under_supplied_policy": "ship", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"aafaf7b467516cc3\",\"command\":\"console1/ship\"}]}", "valid_response": true}
- {"id": "A2-7304-incident-learned-2", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": false, "signal": true}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": true, "signal": true}}, "id": "f810464001ef1822", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "canary", "B": "probe"}, "supplied_policy": {"A": "probe", "B": "ledger"}, "correct_action": "canary", "returned_action": "probe", "action_under_supplied_policy": "probe", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"f810464001ef1822\",\"command\":\"console1/probe\"}]}", "valid_response": true}
- {"id": "A2-7302-incident-learned-5", "arm": "learned", "case": {"class": "A", "evidence": {"canary": {"fresh": true, "signal": true}, "ledger": {"fresh": true, "signal": false}, "probe": {"fresh": false, "signal": true}}, "id": "8c02c9e590990c34", "queue": "east", "summary": "looks clear"}, "true_policy": {"A": "ledger", "B": "probe"}, "supplied_policy": {"A": "canary", "B": "ledger"}, "correct_action": "none", "returned_action": "canary", "action_under_supplied_policy": "canary", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"8c02c9e590990c34\",\"command\":\"console1/canary\"}]}", "valid_response": true}
- {"id": "A2-7302-incident-learned-1", "arm": "learned", "case": {"class": "B", "evidence": {"canary": {"fresh": true, "signal": false}, "ledger": {"fresh": false, "signal": true}, "probe": {"fresh": false, "signal": false}}, "id": "bd2ce76d448594d7", "queue": "east", "summary": "needs attention"}, "true_policy": {"A": "ledger", "B": "probe"}, "supplied_policy": {"A": "canary", "B": "ledger"}, "correct_action": "none", "returned_action": "ledger", "action_under_supplied_policy": "ledger", "classification": "policy_induced", "raw_text": "{\"decisions\":[{\"id\":\"bd2ce76d448594d7\",\"command\":\"console1/ledger\"}]}", "valid_response": true}

All-class counts: {"policy_induced": 21}. Citations were checked semantically against visible history; valid IDs alone were not accepted. Returned objects reveal wrong policies, not hidden reasoning.
