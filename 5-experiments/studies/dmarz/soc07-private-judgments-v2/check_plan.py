"""Offline accounting for a planning document; never calls a model or the hub."""
import json
from pathlib import Path


def main():
    config = json.loads(Path(__file__).with_name("design.json").read_text())
    assert config["status"] == "planning-only"
    assert config["execution_enabled"] is False
    assert config["budget"]["allow_paid_execution"] is False
    phases = config["protocol"]["phases"]
    assert len(phases) == 4
    assert sum(p["max_output_tokens"] for p in phases) == 640
    assert len(config["model"]["revision"]) == 40
    print("All counts are plans, not measured runs. No network or model calls.")
    print("stage | worlds | episodes | allocated calls | unique calls | allocated output cap | unique output cap")
    for stage in config["stages"]:
        assert stage["worlds"] == len(config["regimes"]) * stage["worlds_per_regime"]
        assert len(stage["arms"]) == len(set(stage["arms"]))
        if stage["kind"] != "qualification":
            assert stage["calls_per_agent"] == len(phases)
            assert stage["output_tokens_per_agent"] == sum(p["max_output_tokens"] for p in phases)
        blocks = stage["worlds"] * stage["repeats"]
        episodes = blocks * len(stage["arms"])
        calls = episodes * stage["agents"] * stage["calls_per_agent"]
        tokens = episodes * stage["agents"] * stage["output_tokens_per_agent"]
        shared = set(stage["arms"]) & set(config["protocol"]["shared_initial_arms"])
        saved = blocks * stage["agents"] * max(0, len(shared) - 1) if stage["shared_initial"] else 0
        unique_calls = calls - saved
        unique_tokens = tokens - saved * phases[0]["max_output_tokens"]
        assert unique_calls > 0 and unique_tokens > 0
        print(f'{stage["id"]} | {stage["worlds"]} | {episodes} | {calls:,} | {unique_calls:,} | {tokens:,} | {unique_tokens:,}')
    assert config["protocol"]["automatic_retries"] == 0
    assert config["protocol"]["invalid_output_repairs"] == 0
    print("Plan invariants pass. Unresolved launch fields intentionally remain null.")


if __name__ == "__main__":
    main()
