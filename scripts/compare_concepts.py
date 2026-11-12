#!/usr/bin/env python3
"""Calculate supplementary design-enabler scores for comparable concepts.

The calculation is CIRCit-aligned but original to this skill. Evidence coverage,
mandatory gates, physical indicators, advantages, and disadvantages remain
separate from circularity performance.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


IMPORTANCE_VALUES = {0, 1, 2, 3}
FULFILLMENT_VALUES = {1, 3, 5}
EVIDENCE_WEIGHTS = {
    "measured": 1.0,
    "documented": 0.8,
    "estimated": 0.5,
    "assumed": 0.25,
    "unknown": 0.0,
}
GATE_STATUSES = {"pass", "fail", "unknown", "not_applicable"}
VALUE_STATUSES = {"measured", "calculated", "estimated", "assumed", "design_target", "unknown"}
CONFIDENCE_LEVELS = {"high", "medium", "low", "unknown"}
CONTEXT_FIELDS = (
    "functional_unit",
    "system_boundary",
    "time_horizon",
    "geography",
    "use_conditions",
    "scoring_rules",
)


class InputError(ValueError):
    """Raised when multi-concept comparison input is invalid."""


def _allowed_int(value: Any, field: str, allowed: set[int]) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value not in allowed:
        choices = ", ".join(str(item) for item in sorted(allowed))
        raise InputError(f"{field} must be one of: {choices}")
    return value


def _evidence(value: Any, field: str) -> str:
    if not isinstance(value, str) or value not in EVIDENCE_WEIGHTS:
        raise InputError(f"{field} must be one of: {', '.join(EVIDENCE_WEIGHTS)}")
    return value


def _string_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise InputError(f"{field} must be a list of strings")
    return value


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 2)


def validate(data: Any, strict: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(data, dict):
        raise InputError("The input root must be a JSON object")
    if strict:
        for field in CONTEXT_FIELDS:
            if not isinstance(data.get(field), str) or not data[field].strip():
                raise InputError(f"{field} must be a non-empty string in strict mode")

    raw_cases = data.get("cases")
    if not isinstance(raw_cases, list) or len(raw_cases) < 2:
        raise InputError("cases must contain one baseline and at least one concept")

    cases: list[dict[str, Any]] = []
    case_ids: set[str] = set()
    baseline_ids: list[str] = []
    for index, raw in enumerate(raw_cases):
        prefix = f"cases[{index}]"
        if not isinstance(raw, dict):
            raise InputError(f"{prefix} must be an object")
        case_id = raw.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise InputError(f"{prefix}.id must be a non-empty string")
        if case_id in case_ids:
            raise InputError(f"Duplicate case id: {case_id}")
        case_ids.add(case_id)

        kind = raw.get("kind")
        if kind not in {"baseline", "concept"}:
            raise InputError(f"{prefix}.kind must be baseline or concept")
        if kind == "baseline":
            baseline_ids.append(case_id)

        item = dict(raw)
        item["id"] = case_id
        item["name"] = raw.get("name", case_id)
        item["advantages"] = _string_list(raw.get("advantages"), f"{prefix}.advantages")
        item["disadvantages"] = _string_list(raw.get("disadvantages"), f"{prefix}.disadvantages")

        indicators = raw.get("physical_indicators", [])
        if not isinstance(indicators, list) or any(not isinstance(x, dict) for x in indicators):
            raise InputError(f"{prefix}.physical_indicators must be a list of objects")
        if strict and not indicators:
            raise InputError(f"{prefix}.physical_indicators must not be empty in strict mode")
        clean_indicators: list[dict[str, Any]] = []
        for indicator_index, indicator in enumerate(indicators):
            indicator_prefix = f"{prefix}.physical_indicators[{indicator_index}]"
            if not isinstance(indicator.get("name"), str) or not indicator["name"].strip():
                raise InputError(f"{indicator_prefix}.name must be a non-empty string")
            if "evidence" in indicator:
                _evidence(indicator["evidence"], f"{indicator_prefix}.evidence")
            clean_indicator = dict(indicator)
            if strict:
                indicator_id = indicator.get("id")
                if not isinstance(indicator_id, str) or not indicator_id.strip():
                    raise InputError(f"{indicator_prefix}.id must be a non-empty string in strict mode")
                if not isinstance(indicator.get("unit"), str) or not indicator["unit"].strip():
                    raise InputError(f"{indicator_prefix}.unit must be a non-empty string in strict mode")
                value_status = indicator.get("value_status")
                if value_status not in VALUE_STATUSES:
                    raise InputError(
                        f"{indicator_prefix}.value_status must be one of: {', '.join(sorted(VALUE_STATUSES))}"
                    )
                _evidence(indicator.get("evidence"), f"{indicator_prefix}.evidence")
                if not isinstance(indicator.get("source"), str) or not indicator["source"].strip():
                    raise InputError(f"{indicator_prefix}.source must be a non-empty string in strict mode")
                if indicator.get("confidence") not in CONFIDENCE_LEVELS:
                    raise InputError(
                        f"{indicator_prefix}.confidence must be one of: {', '.join(sorted(CONFIDENCE_LEVELS))}"
                    )
                value = indicator.get("value")
                if value_status != "unknown" and (
                    isinstance(value, bool) or not isinstance(value, (int, float))
                ):
                    raise InputError(f"{indicator_prefix}.value must be numeric unless value_status is unknown")
            clean_indicators.append(clean_indicator)
        item["physical_indicators"] = clean_indicators

        gates = raw.get("gates", [])
        if not isinstance(gates, list) or any(not isinstance(x, dict) for x in gates):
            raise InputError(f"{prefix}.gates must be a list of objects")
        if strict and not gates:
            raise InputError(f"{prefix}.gates must not be empty in strict mode")
        for gate_index, gate in enumerate(gates):
            status = gate.get("status")
            if status not in GATE_STATUSES:
                choices = ", ".join(sorted(GATE_STATUSES))
                raise InputError(f"{prefix}.gates[{gate_index}].status must be one of: {choices}")
        if strict and not any(gate.get("id") == "function" for gate in gates):
            raise InputError(f"{prefix}.gates must include a function gate in strict mode")
        item["gates"] = gates
        cases.append(item)

    if len(baseline_ids) != 1:
        raise InputError("Exactly one case must have kind baseline")

    if strict:
        indicator_units: dict[str, str] | None = None
        for case in cases:
            current: dict[str, str] = {}
            for indicator in case["physical_indicators"]:
                indicator_id = indicator["id"]
                if indicator_id in current:
                    raise InputError(f"Duplicate physical indicator id {indicator_id} in case {case['id']}")
                current[indicator_id] = indicator["unit"]
            if indicator_units is None:
                indicator_units = current
            elif current != indicator_units:
                raise InputError(
                    "All cases must use the same physical indicator IDs and units in strict mode"
                )

    raw_criteria = data.get("criteria")
    if not isinstance(raw_criteria, list) or not raw_criteria:
        raise InputError("criteria must be a non-empty list")

    criteria: list[dict[str, Any]] = []
    criterion_ids: set[str] = set()
    for index, raw in enumerate(raw_criteria):
        prefix = f"criteria[{index}]"
        if not isinstance(raw, dict):
            raise InputError(f"{prefix} must be an object")
        criterion_id = raw.get("id")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise InputError(f"{prefix}.id must be a non-empty string")
        if criterion_id in criterion_ids:
            raise InputError(f"Duplicate criterion id: {criterion_id}")
        criterion_ids.add(criterion_id)

        importance = _allowed_int(raw.get("importance"), f"{prefix}.importance", IMPORTANCE_VALUES)
        ratings = raw.get("ratings")
        if not isinstance(ratings, dict):
            raise InputError(f"{prefix}.ratings must be an object keyed by case id")
        if set(ratings) != case_ids:
            missing = sorted(case_ids - set(ratings))
            extra = sorted(set(ratings) - case_ids)
            raise InputError(f"{prefix}.ratings case mismatch; missing={missing}, extra={extra}")

        clean_ratings: dict[str, dict[str, Any]] = {}
        for case_id in case_ids:
            rating = ratings[case_id]
            if not isinstance(rating, dict):
                raise InputError(f"{prefix}.ratings.{case_id} must be an object")
            clean_ratings[case_id] = {
                "fulfillment": _allowed_int(
                    rating.get("fulfillment"),
                    f"{prefix}.ratings.{case_id}.fulfillment",
                    FULFILLMENT_VALUES,
                ),
                "evidence": _evidence(
                    rating.get("evidence", "unknown"),
                    f"{prefix}.ratings.{case_id}.evidence",
                ),
                "note": rating.get("note", ""),
            }

        criteria.append(
            {
                "id": criterion_id,
                "name": raw.get("name", criterion_id),
                "importance": importance,
                "ratings": clean_ratings,
            }
        )

    if not any(item["importance"] > 0 for item in criteria):
        raise InputError("At least one criterion must have importance greater than zero")
    validate_sensitivity(data.get("sensitivity_scenarios", []), case_ids, criterion_ids, strict)
    return cases, criteria


def validate_sensitivity(
    scenarios: Any,
    case_ids: set[str],
    criterion_ids: set[str],
    strict: bool,
) -> None:
    if not isinstance(scenarios, list):
        raise InputError("sensitivity_scenarios must be a list")
    if strict and not scenarios:
        raise InputError("sensitivity_scenarios must contain at least one scenario in strict mode")
    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        prefix = f"sensitivity_scenarios[{index}]"
        if not isinstance(scenario, dict):
            raise InputError(f"{prefix} must be an object")
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise InputError(f"{prefix}.id must be a non-empty string")
        if scenario_id in seen:
            raise InputError(f"Duplicate sensitivity scenario id: {scenario_id}")
        seen.add(scenario_id)
        importance_overrides = scenario.get("importance_overrides", {})
        if not isinstance(importance_overrides, dict) or not set(importance_overrides).issubset(criterion_ids):
            raise InputError(f"{prefix}.importance_overrides contains an invalid criterion id")
        for criterion_id, value in importance_overrides.items():
            _allowed_int(value, f"{prefix}.importance_overrides.{criterion_id}", IMPORTANCE_VALUES)
        fulfillment_overrides = scenario.get("fulfillment_overrides", {})
        if not isinstance(fulfillment_overrides, dict) or not set(fulfillment_overrides).issubset(case_ids):
            raise InputError(f"{prefix}.fulfillment_overrides contains an invalid case id")
        for case_id, overrides in fulfillment_overrides.items():
            if not isinstance(overrides, dict) or not set(overrides).issubset(criterion_ids):
                raise InputError(f"{prefix}.fulfillment_overrides.{case_id} contains an invalid criterion id")
            for criterion_id, value in overrides.items():
                _allowed_int(
                    value,
                    f"{prefix}.fulfillment_overrides.{case_id}.{criterion_id}",
                    FULFILLMENT_VALUES,
                )
        if strict:
            assumptions = scenario.get("assumptions")
            if not isinstance(assumptions, dict) or not assumptions:
                raise InputError(f"{prefix}.assumptions must be a non-empty object in strict mode")
            if not importance_overrides and not fulfillment_overrides:
                raise InputError(f"{prefix} must change an importance or fulfillment value in strict mode")


def gate_summary(gates: list[dict[str, Any]]) -> str:
    statuses = [gate["status"] for gate in gates if gate["status"] != "not_applicable"]
    if not statuses:
        return "not_assessed"
    if "fail" in statuses:
        return "fail"
    if "unknown" in statuses:
        return "unknown"
    return "pass"


def rank_groups(scored: dict[str, dict[str, Any]], concept_ids: list[str]) -> list[list[str]]:
    ordered = sorted(
        concept_ids,
        key=lambda case_id: (
            -scored[case_id]["normalized_design_score"],
            scored[case_id]["native_gap_score"],
            case_id,
        ),
    )
    groups: list[list[str]] = []
    for case_id in ordered:
        if not groups or scored[groups[-1][0]]["normalized_design_score"] != scored[case_id]["normalized_design_score"]:
            groups.append([case_id])
        else:
            groups[-1].append(case_id)
    return groups


def sensitivity_results(
    data: dict[str, Any],
    cases: list[dict[str, Any]],
    criteria: list[dict[str, Any]],
    base_groups: list[list[str]],
) -> dict[str, Any]:
    concept_ids = [item["id"] for item in cases if item["kind"] == "concept"]
    results: list[dict[str, Any]] = []
    for scenario in data.get("sensitivity_scenarios", []):
        weights = {
            item["id"]: scenario.get("importance_overrides", {}).get(item["id"], item["importance"])
            for item in criteria
        }
        importance_total = sum(weights.values())
        if importance_total <= 0:
            raise InputError(f"Sensitivity scenario {scenario['id']} sets all importance values to zero")
        minimum = importance_total
        maximum = importance_total * 5
        scenario_scored: dict[str, dict[str, Any]] = {}
        for case in cases:
            case_id = case["id"]
            fulfillment_overrides = scenario.get("fulfillment_overrides", {}).get(case_id, {})
            gap = sum(
                weights[item["id"]]
                * fulfillment_overrides.get(item["id"], item["ratings"][case_id]["fulfillment"])
                for item in criteria
            )
            normalized = 100.0 * (maximum - gap) / (maximum - minimum)
            scenario_scored[case_id] = {
                "native_gap_score": float(gap),
                "normalized_design_score": _round(normalized),
            }
        groups = rank_groups(scenario_scored, concept_ids)
        results.append(
            {
                "id": scenario["id"],
                "name": scenario.get("name", scenario["id"]),
                "assumptions": scenario.get("assumptions", {}),
                "note": scenario.get("note", ""),
                "importance_overrides": scenario.get("importance_overrides", {}),
                "fulfillment_overrides": scenario.get("fulfillment_overrides", {}),
                "concept_scores": {
                    case_id: scenario_scored[case_id]["normalized_design_score"]
                    for case_id in concept_ids
                },
                "rank_groups": groups,
                "ties": [group for group in groups if len(group) > 1],
                "top_rank_changed": set(groups[0]) != set(base_groups[0]),
                "full_ranking_changed": groups != base_groups,
            }
        )
    return {
        "scenarios": results,
        "top_rank_robust_across_scenarios": all(not item["top_rank_changed"] for item in results),
        "full_rank_groups_robust_across_scenarios": all(
            not item["full_ranking_changed"] for item in results
        ),
        "warning": "Sensitivity results depend on the documented mapping from changed assumptions to weight or fulfillment overrides.",
    }


def calculate(data: dict[str, Any], strict: bool = False) -> dict[str, Any]:
    cases, criteria = validate(data, strict=strict)
    importance_total = sum(item["importance"] for item in criteria)
    minimum = importance_total
    maximum = importance_total * 5
    baseline_id = next(item["id"] for item in cases if item["kind"] == "baseline")

    scored: dict[str, dict[str, Any]] = {}
    for case in cases:
        case_id = case["id"]
        gap = sum(
            item["importance"] * item["ratings"][case_id]["fulfillment"]
            for item in criteria
        )
        normalized = 100.0 * (maximum - gap) / (maximum - minimum)
        evidence_coverage = 100.0 * sum(
            item["importance"] * EVIDENCE_WEIGHTS[item["ratings"][case_id]["evidence"]]
            for item in criteria
        ) / importance_total
        scored[case_id] = {
            "id": case_id,
            "name": case["name"],
            "kind": case["kind"],
            "native_gap_score": float(gap),
            "normalized_design_score": _round(normalized),
            "weighted_evidence_coverage_percent": _round(evidence_coverage),
            "mandatory_gate_status": gate_summary(case["gates"]),
            "gates": case["gates"],
            "physical_indicators": case["physical_indicators"],
            "advantages": case["advantages"],
            "disadvantages": case["disadvantages"],
            "criterion_contributions": [
                {
                    "criterion_id": item["id"],
                    "criterion_name": item["name"],
                    "importance": item["importance"],
                    "fulfillment": item["ratings"][case_id]["fulfillment"],
                    "gap_contribution": item["importance"]
                    * item["ratings"][case_id]["fulfillment"],
                    "evidence": item["ratings"][case_id]["evidence"],
                    "note": item["ratings"][case_id]["note"],
                }
                for item in criteria
            ],
        }

    baseline = scored[baseline_id]
    comparisons: list[dict[str, Any]] = []
    for case in cases:
        if case["kind"] != "concept":
            continue
        result = scored[case["id"]]
        point_change = result["normalized_design_score"] - baseline["normalized_design_score"]
        native_reduction = baseline["native_gap_score"] - result["native_gap_score"]
        remaining_gap_closed = None
        if baseline["normalized_design_score"] < 100:
            remaining_gap_closed = 100.0 * point_change / (
                100.0 - baseline["normalized_design_score"]
            )
        comparisons.append(
            {
                "concept_id": case["id"],
                "concept_name": case["name"],
                "normalized_score_point_change": _round(point_change),
                "native_gap_reduction": _round(native_reduction),
                "remaining_design_gap_closed_percent": _round(remaining_gap_closed),
                "direction": "improved" if point_change > 0 else "worsened" if point_change < 0 else "unchanged",
                "mandatory_gate_status": result["mandatory_gate_status"],
            }
        )

    concept_ids = [item["id"] for item in cases if item["kind"] == "concept"]
    base_rank_groups = rank_groups(scored, concept_ids)
    circularity_ranking = [case_id for group in base_rank_groups for case_id in group]
    sensitivity = sensitivity_results(data, cases, criteria, base_rank_groups)

    return {
        "product": data.get("product", "Unspecified product"),
        "functional_unit": data.get("functional_unit", "Not stated"),
        "system_boundary": data.get("system_boundary", "Not stated"),
        "time_horizon": data.get("time_horizon", "Not stated"),
        "geography": data.get("geography", "Not stated"),
        "use_conditions": data.get("use_conditions", "Not stated"),
        "scoring_rules": data.get("scoring_rules", "Not stated"),
        "strict_mode": strict,
        "method": {
            "name": "Supplementary CIRCit-aligned multi-concept design-enabler comparison",
            "native_direction": "lower is better",
            "normalized_direction": "higher is better",
            "normalized_status": "internal presentation transformation; not an official CIRCit score",
            "minimum_possible_gap": float(minimum),
            "maximum_possible_gap": float(maximum),
        },
        "baseline_id": baseline_id,
        "cases": [scored[item["id"]] for item in cases],
        "comparisons_to_baseline": comparisons,
        "supplementary_design_score_ranking": circularity_ranking,
        "circularity_ranking_only": circularity_ranking,
        "base_rank_groups": base_rank_groups,
        "base_ties": [group for group in base_rank_groups if len(group) > 1],
        "sensitivity_analysis": sensitivity,
        "ranking_warning": "This ranks supplementary design scores, not actual circularity outcomes or hierarchy routes. It is not a selection decision and cannot override mandatory gates.",
        "limitations": [
            "Scores are comparable only under the same functional unit, boundary, criteria, importance weights, and data-quality rules.",
            "Evidence coverage is separate from performance and does not validate assumptions.",
            "Advantages, disadvantages, sustainability consequences, feasibility, and mandatory gates must remain visible beside the score.",
            "This result is not an MCI, LCA, certification, safety review, or proof of sustainability improvement.",
        ],
    }


def example() -> dict[str, Any]:
    return {
        "product": "Example product",
        "functional_unit": "Deliver the required service for one year",
        "system_boundary": "Product, replacements, maintenance, and recovery needed for the functional unit",
        "time_horizon": "10 years",
        "geography": "Named market and recovery region",
        "use_conditions": "Indoor use, 2 hours per day",
        "scoring_rules": "Importance 0-3; fulfillment 1/3/5; unknown evidence is not failure",
        "cases": [
            {
                "id": "baseline",
                "name": "Current product",
                "kind": "baseline",
                "advantages": ["Established user behaviour"],
                "disadvantages": ["Whole-unit replacement"],
                "physical_indicators": [
                    {"id": "virgin-material", "name": "Virgin material per functional unit", "value": 100, "unit": "g/FU", "value_status": "calculated", "evidence": "estimated", "source": "Measured mass plus replacement schedule", "confidence": "medium"}
                ],
                "gates": [{"id": "function", "name": "Required function", "status": "pass"}],
            },
            {
                "id": "concept-a",
                "name": "Modular concept",
                "kind": "concept",
                "advantages": ["Retains durable structure"],
                "disadvantages": ["Adds an interface"],
                "physical_indicators": [
                    {"id": "virgin-material", "name": "Virgin material per functional unit", "value": 35, "unit": "g/FU", "value_status": "design_target", "evidence": "assumed", "source": "Concept mass budget", "confidence": "low"}
                ],
                "gates": [{"id": "function", "name": "Required function", "status": "unknown"}],
            },
            {
                "id": "concept-b",
                "name": "Take-back concept",
                "kind": "concept",
                "advantages": ["Creates a controlled recovery route"],
                "disadvantages": ["Depends on reverse logistics"],
                "physical_indicators": [
                    {"id": "virgin-material", "name": "Virgin material per functional unit", "value": 60, "unit": "g/FU", "value_status": "estimated", "evidence": "estimated", "source": "Concept mass and take-back model", "confidence": "medium"}
                ],
                "gates": [{"id": "function", "name": "Required function", "status": "pass"}],
            },
        ],
        "criteria": [
            {
                "id": "life-matching",
                "name": "Match component lives to wear",
                "importance": 3,
                "ratings": {
                    "baseline": {"fulfillment": 5, "evidence": "documented"},
                    "concept-a": {"fulfillment": 1, "evidence": "assumed"},
                    "concept-b": {"fulfillment": 3, "evidence": "estimated"},
                },
            },
            {
                "id": "recovery-route",
                "name": "Plausible actual recovery route",
                "importance": 2,
                "ratings": {
                    "baseline": {"fulfillment": 5, "evidence": "documented"},
                    "concept-a": {"fulfillment": 3, "evidence": "unknown"},
                    "concept-b": {"fulfillment": 1, "evidence": "estimated"},
                },
            },
        ],
        "sensitivity_scenarios": [
            {
                "id": "low-take-back",
                "name": "Low take-back",
                "assumptions": {"concept-b take-back rate": "20% instead of 70%"},
                "fulfillment_overrides": {"concept-b": {"recovery-route": 5}},
                "note": "Low take-back weakens recovery-route fulfillment.",
            },
            {
                "id": "short-module-life",
                "name": "Short module life",
                "assumptions": {"concept-a repair frequency": "Three times the base estimate"},
                "fulfillment_overrides": {"concept-a": {"life-matching": 5}},
                "note": "Frequent module failures weaken lifetime matching.",
            },
        ],
    }


def self_test() -> None:
    result = calculate(example(), strict=True)
    cases = {item["id"]: item for item in result["cases"]}
    assert cases["baseline"]["native_gap_score"] == 25.0
    assert cases["baseline"]["normalized_design_score"] == 0.0
    assert cases["concept-a"]["native_gap_score"] == 9.0
    assert cases["concept-a"]["normalized_design_score"] == 80.0
    assert cases["concept-a"]["mandatory_gate_status"] == "unknown"
    assert result["circularity_ranking_only"] == ["concept-a", "concept-b"]
    assert result["supplementary_design_score_ranking"] == ["concept-a", "concept-b"]
    assert math.isclose(result["comparisons_to_baseline"][0]["native_gap_reduction"], 16.0)
    assert result["base_rank_groups"] == [["concept-a"], ["concept-b"]]
    assert result["sensitivity_analysis"]["scenarios"][0]["full_ranking_changed"] is False
    assert result["sensitivity_analysis"]["scenarios"][1]["top_rank_changed"] is True
    assert result["sensitivity_analysis"]["top_rank_robust_across_scenarios"] is False
    tied = example()
    tied["criteria"][0]["ratings"]["concept-b"]["fulfillment"] = 1
    tied["criteria"][1]["ratings"]["concept-b"]["fulfillment"] = 3
    tied_result = calculate(tied, strict=True)
    assert tied_result["base_ties"] == [["concept-a", "concept-b"]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("input", nargs="?", type=Path, help="Input comparison JSON file")
    mode.add_argument("--example", action="store_true", help="Print an example input JSON")
    mode.add_argument("--self-test", action="store_true", help="Run built-in invariant checks")
    parser.add_argument("--output", type=Path, help="Write result JSON to this file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require complete comparison framing, traceable indicators, and sensitivity input",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.example:
        print(json.dumps(example(), indent=2, ensure_ascii=False))
        return 0
    if args.self_test:
        self_test()
        print("Self-test passed.")
        return 0

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = calculate(data, strict=args.strict)
    except (OSError, json.JSONDecodeError, InputError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

