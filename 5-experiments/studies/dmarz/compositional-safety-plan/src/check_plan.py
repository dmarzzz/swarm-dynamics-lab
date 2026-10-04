"""Validate planning arithmetic only. No model, network, or experiment calls."""

import json
import math
from pathlib import Path
from statistics import NormalDist


def main():
    root = Path(__file__).resolve().parents[1]
    design = json.loads((root / "design.json").read_text())
    total = 0
    stage_counts = {}
    for stage in design["stages"]:
        count = math.prod(stage["factors"].values())
        assert count == stage["expected_episodes"], stage["id"]
        stage_counts[stage["id"]] = count
        total += count
    assert total == design["expected_total_episodes"]
    assert design["execution_authorized_by_this_file"] is False
    assert design["holdout_opened"] is False
    assert len(set(design["core_arms"])) == 8
    z = NormalDist().inv_cdf(1 - design["alpha_two_sided"] / 2)
    power_z = NormalDist().inv_cdf(design["power_target"])
    delta = design["primary_effect_for_power"]
    sensitivity = [
        {"assumed_task_sd": sd,
         "independent_roots_normal_approximation": math.ceil((z + power_z) ** 2 * sd ** 2 / delta ** 2)}
        for sd in design["assumed_task_difference_sd_sensitivity"]
    ]
    output = {
        "status": "planning arithmetic, not experiment results or validated power",
        "episodes_by_stage": stage_counts,
        "episodes_total": total,
        "max_model_calls_at_proposed_cap": total * design["episode_caps_proposed"]["model_calls"],
        "power_sensitivity_assumptions": sensitivity,
        "illustrative_cost_before_overhead": [
            {"assumed_mean_episode_usd": cost, "total_usd": round(total * cost, 2)}
            for cost in design["illustrative_mean_episode_costs_usd"]
        ],
        "main_independent_roots": 500,
        "main_episode_count_is_not_independent_sample_size": True
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
