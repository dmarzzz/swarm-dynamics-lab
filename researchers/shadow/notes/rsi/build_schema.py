#!/usr/bin/env python3
"""Generate the versioned, closed public wire schema. No source traces are read."""
import json
from pathlib import Path
V = "swarm-trace/0.2.0"
def obj(properties, optional=()):
    return {"type": "object", "properties": properties, "required": [k for k in properties if k not in optional], "additionalProperties": False}
def enum(*values): return {"enum": list(values)}
def ref(name): return {"$ref": "#/$defs/" + name}
def nullable(schema): return {"anyOf": [schema, {"type": "null"}]}
def arr(schema, minimum=0, maximum=256): return {"type": "array", "items": schema, "minItems": minimum, "maxItems": maximum}
ID = {"type": "string", "pattern": "^[a-zA-Z0-9][a-zA-Z0-9_./:-]{0,127}$"}
HASH = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
INT = {"type": "integer", "minimum": 0, "maximum": 9007199254740991}
SCORE = {"type": "integer", "minimum": 0, "maximum": 10000}
BPS = SCORE
BOOL = {"type": "boolean"}
def header(kind): return {"schema_version": {"const": V}, "record_type": {"const": kind}}
defs = {}
defs['content_commitment'] = obj({"commitment": HASH, "algorithm": {"const": "sha256-domain-nonce-v1"}, "representation": enum("pool-request-utf8", "pool-collected-response-utf8", "slj1-content"), "completeness": enum("stored-snapshot", "clipped", "unknown"), "tier": {"const": "sealed"}})
defs['integrity'] = obj({"record_hash": HASH, "previous_event_hash": nullable(HASH), "signature": nullable(obj({"algorithm": {"const": "ed25519"}, "key_id": ID, "value": {"type": "string", "pattern": "^[0-9a-f]{128}$"}}))})
defs['score'] = obj({"metric_id": ID, "value_bps": SCORE, "evaluator_id": ID, "evaluation_receipt_hash": HASH, "rubric_hash": HASH, "status": enum("provisional", "final", "disputed")})
defs['tool'] = obj({"call_id": ID, "name": ID, "parent_model_span_id": nullable({"type": "string", "pattern": "^(?!0{16}$)[0-9a-f]{16}$"}), "arguments": nullable(ref('content_commitment')), "result": nullable(ref('content_commitment')), "state": enum("proposed", "started", "completed", "failed", "unknown")})
defs['attributes'] = obj({
 "gen_ai.operation.name": enum("chat", "generate_content", "text_completion", "execute_tool", "invoke_agent", "invoke_workflow", "plan"),
 "gen_ai.provider.name": ID, "gen_ai.request.model": ID, "gen_ai.response.model": ID,
 "gen_ai.agent.id": ID, "gen_ai.request.stream": BOOL,
 "gen_ai.usage.input_tokens": INT, "gen_ai.usage.output_tokens": INT,
 "gen_ai.usage.cache_read.input_tokens": INT, "gen_ai.usage.cache_write.input_tokens": INT,
 "error.type": enum("timeout", "rate_limit", "credit_exhausted", "schema_invalid", "cancelled", "transport_error", "_OTHER")
}, optional=("gen_ai.provider.name", "gen_ai.request.model", "gen_ai.response.model", "gen_ai.agent.id", "gen_ai.request.stream", "gen_ai.usage.input_tokens", "gen_ai.usage.output_tokens", "gen_ai.usage.cache_read.input_tokens", "gen_ai.usage.cache_write.input_tokens", "error.type"))
defs['event'] = obj({**header('event'), "event_id": ID, "stream_id": ID, "stream_seq": INT,
 "trace_id": {"type": "string", "pattern": "^(?!0{32}$)[0-9a-f]{32}$"},
 "span_id": {"type": "string", "pattern": "^(?!0{16}$)[0-9a-f]{16}$"},
 "parent_span_id": nullable({"type": "string", "pattern": "^(?!0{16}$)[0-9a-f]{16}$"}),
 "span_kind": enum("CLIENT", "INTERNAL"), "step_id": nullable(ID), "parent_step_id": nullable(ID),
 "links": arr(obj({"event_id": ID, "relation": enum("depends_on", "follows", "supersedes", "derived_from", "reviews")})),
 "event_type": enum("span_started", "span_ended", "span_snapshot", "step_committed", "artifact_published", "review_recorded", "assignment_created", "run_cancelled"),
 "producer_id": ID, "agent_id": nullable(ID), "owner_id": ID,
 "run_id": nullable(ID), "task_id": nullable(ID), "attempt_id": nullable(ID),
 "source": obj({"adapter": enum("pool-meter", "openclaw", "codex", "claude-code", "hub", "experiment", "synthetic"), "mode": enum("live", "historical-import", "synthetic"), "attribution": enum("exact-run-id", "approved-task-text-match", "owner-approved", "synthetic"), "identity_quality": enum("native", "import-generated")}),
 "timing": obj({"observed_at": {"type":"string","format":"date-time"}, "precision_ms": INT, "duration_ms": nullable(INT), "ttfb_ms": nullable(INT), "start_time": nullable({"type":"string","format":"date-time"}), "end_time": nullable({"type":"string","format":"date-time"})}),
 "otel_semconv_revision": {"const":"e07f4ebacb08f56db8c4c882d117720333fbca04"}, "attributes": ref('attributes'),
 "transport": obj({"http_status": nullable({"type":"integer","minimum":100,"maximum":599}), "state": enum("ok", "error", "unknown"), "stream_terminal_observed": nullable(BOOL)}),
 "tool_calls": nullable(arr(ref('tool'))),
 "cost": obj({"currency": {"const":"USD"}, "estimated_microusd": nullable(INT), "billed_microusd": nullable(INT), "receipt_hash": nullable(HASH), "coverage": enum("unknown", "estimated", "billed", "partial")}),
 "outcome": obj({"state": enum("ungraded", "accepted", "rejected", "inconclusive", "failed", "cancelled"), "score": nullable(ref('score'))}),
 "content": obj({"prompt": nullable(ref('content_commitment')), "response": nullable(ref('content_commitment'))}),
 "disclosure": obj({"envelope_tier": enum("private", "sealed", "public"), "content_tier": enum("private", "sealed", "public"), "policy_id": ID, "hints": arr(enum("operation", "model", "usage", "latency", "transport-status", "commitments", "review-status", "task-class")), "permitted_builders": arr(ID), "release_state": enum("sealed", "owner-authorized-public", "withdrawn"), "reveal_not_before": nullable({"type":"string","format":"date-time"})}),
 "market": obj({"eligible": BOOL, "opportunity_id": nullable(ID), "source_rebate_floor_bps": BPS, "permit_hash": nullable(HASH)}),
 "integrity": ref('integrity')})
defs['event']['allOf']=[{"if":{"properties":{"market":{"properties":{"eligible":{"const":True}}}}},"then":{"properties":{"market":{"properties":{"permit_hash":HASH,"opportunity_id":ID}},"integrity":{"properties":{"signature":{"type":"object"}}}}}}]
defs['content_public'] = obj({**header('content_public'), "event_id": ID, "projection": {"const":"omitted-by-policy"}, "prompt": {"const":"[SEALED]"}, "response": {"const":"[SEALED]"}, "tool_arguments": {"const":"[OMITTED]"}, "tool_results": {"const":"[OMITTED]"}})
defs['bundle'] = obj({**header('bundle'), "bundle_id": ID, "searcher_id": ID, "searcher_principal_id": ID, "opportunity_id": ID,
 "mode": enum("proposal", "offline-demo"), "kind": enum("next-step", "fix", "routing", "backrun-review", "backrun-replication", "backrun-hypothesis"),
 "trigger_event_ids": arr(ID,1), "source_event_hashes": arr(HASH,1),
 "inclusion": obj({"epoch_min": INT, "epoch_max": INT, "after_release": BOOL, "task_version_hash": HASH}),
 "body": arr(obj({"action_id": ID, "operation": enum("offline-check", "review", "replicate", "propose-brief", "route-task", "hypothesis"), "depends_on": arr(ID), "artifact_hash": HASH, "failure_policy": enum("abort-publication", "continue-diagnostic")}),1,16),
 "read_set": arr(ID), "write_set": arr(ID), "permitted_builders": arr(ID,1),
 "budget": obj({"max_model_calls": INT, "max_microusd": INT, "max_runtime_ms": INT}),
 "valuation": obj({"metric_id": ID, "rubric_hash": HASH, "baseline_artifact_hash": HASH, "claimed_gain_bps": SCORE, "requested_bounty_microusd": INT}),
 "rebates": obj({"trace_originator_bps": BPS, "searcher_bps": BPS, "builder_bps": BPS, "evaluator_bps": BPS}),
 "orderflow_bid": obj({"funded_microusd": INT, "escrow_receipt_hash": nullable(HASH)}),
 "capabilities": obj({"network": {"const":False}, "paid_calls": {"const":False}, "publish_raw": {"const":False}, "write_scope": {"const":"isolated-candidate"}}),
 "nonce": {"type":"string","pattern":"^[0-9a-f]{64}$"}, "integrity": ref('integrity')})
schema={"$schema":"https://json-schema.org/draft/2020-12/schema", "$id":"https://swarm-lab.invalid/schemas/swarm-trace-0.2.0.schema.json", "title":"Swarm Trace and Bundle Protocol 0.2.0, public/offline profile", "$comment":"Draft. The invalid domain is an identifier, not a hosted validation endpoint. Semantic, signature and authorization checks are additional requirements.", "oneOf":[ref('event'),ref('content_public'),ref('bundle')], "$defs":defs}
if __name__ == '__main__':
    p=Path(__file__).with_name('trace.schema.json')
    p.write_text(json.dumps(schema,indent=2)+'\n')
    print('wrote',p.name)
