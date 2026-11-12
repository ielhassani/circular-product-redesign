#!/usr/bin/env python3
"""Calculate a supplementary CIRCit-aligned design-enabler gap score.

This script intentionally keeps evidence confidence separate from product
performance. It does not calculate the Material Circularity Indicator, an LCA,
or compliance with ISO standards.
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
CONTEXT_FIELDS = (
    "functional_unit",
    "system_boundary",
    "time_horizon",
    "geography",
    "use_conditions",
    "scoring_rules",
)


class InputError(ValueError):
    """Raised when assessment input is invalid or not comparable."""


def _number(value: Any, field: str, allowed: set[int]) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value not in allowed:
        choices = ", ".join(str(item) for item in sorted(allowed))
        raise InputError(f"{field} must be one of: {choices}")
    return value


def _evidence(value: Any, field: str) -> str:
    if not isinstance(value, str) or value not in EVIDENCE_WEIGHTS:
        choices = ", ".join(EVIDENCE_WEIGHTS)
        raise InputError(f"{field} must be one of: {choices}")
    return value


def validate(data: Any, strict: bool = False) -> list[dict[str, Any]]:
    if not isinstance(data, dict):
        raise InputError("The input root must be a JSON object.")
    if strict:
        for field in CONTEXT_FIELDS:
            if not isinstance(data.get(field), str) or not data[field].strip():
                raise InputError(f"{field} must be a non-empty string in strict mode.")
    criteria = data.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        raise InputError("criteria must be a non-empty list.")

    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for index, raw in enumerate(criteria):
        prefix = f"criteria[{index}]"
        if not isinstance(raw, dict):
            raise InputError(f"{prefix} must be an object.")
        criterion_id = raw.get("id")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise InputError(f"{prefix}.id must be a non-empty string.")
        if criterion_id in seen:
            raise InputError(f"Duplicate criterion id: {criterion_id}")
        seen.add(criterion_id)

        item = dict(raw)
        item["id"] = criterion_id
        item["importance"] = _number(
            raw.get("importance"), f"{prefix}.importance", IMPORTANCE_VALUES
        )
        item["before_fulfillment"] = _number(
            raw.get("before_fulfillment"),
            f"{prefix}.before_fulfillment",
            FULFILLMENT_VALUES,
        )
        item["after_fulfillment"] = _number(
            raw.get("after_fulfillment"),
            f"{prefix}.after_fulfillment",
            FULFILLMENT_VALUES,
        )
        item["before_evidence"] = _evidence(
            raw.get("before_evidence", "unknown"), f"{prefix}.before_evidence"
        )
        item["after_evidence"] = _evidence(
            raw.get("after_evidence", "unknown"), f"{prefix}.after_evidence"
        )
        validated.append(item)

    if not any(item["importance"] > 0 for item in validated):
        raise InputError("At least one criterion must have importance greater than zero.")
    return validated


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 2)


def score_case(criteria: list[dict[str, Any]], case: str) -> dict[str, float]:
    gap = sum(item["importance"] * item[f"{case}_fulfillment"] for item in criteria)
    minimum = sum(item["importance"] for item in criteria)
    maximum = sum(item["importance"] * 5 for item in criteria)
    normalized = 100.0 * (maximum - gap) / (maximum - minimum)
    importance_total = sum(item["importance"] for item in criteria)
    evidence_coverage = 100.0 * sum(
        item["importance"] * EVIDENCE_WEIGHTS[item[f"{case}_evidence"]]
        for item in criteria
    ) / importance_total
    return {
        "native_gap_score": float(gap),
        "minimum_possible_gap": float(minimum),
        "maximum_possible_gap": float(maximum),
        "normalized_design_score": _round(normalized),
        "weighted_evidence_coverage_percent": _round(evidence_coverage),
    }


def calculate(data: dict[str, Any], strict: bool = False) -> dict[str, Any]:
    criteria = validate(data, strict=strict)
    before = score_case(criteria, "before")
    after = score_case(criteria, "after")
    point_change = after["normalized_design_score"] - before["normalized_design_score"]
    native_reduction = before["native_gap_score"] - after["native_gap_score"]

    baseline_score = before["normalized_design_score"]
    relative_change = None
    if baseline_score != 0:
        relative_change = 100.0 * point_change / baseline_score

    remaining_gap_closed = None
    if baseline_score < 100:
        remaining_gap_closed = 100.0 * point_change / (100.0 - baseline_score)

    contributions = []
    for item in criteria:
        importance = item["importance"]
        before_gap = importance * item["before_fulfillment"]
        after_gap = importance * item["after_fulfillment"]
        contributions.append(
            {
                "id": item["id"],
                "name": item.get("name", item["id"]),
                "importance": importance,
                "before_fulfillment": item["before_fulfillment"],
                "after_fulfillment": item["after_fulfillment"],
                "before_gap_contribution": before_gap,
                "after_gap_contribution": after_gap,
                "native_gap_reduction": before_gap - after_gap,
                "before_evidence": item["before_evidence"],
                "after_evidence": item["after_evidence"],
                "note": item.get("note", ""),
            }
        )

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
            "name": "Supplementary CIRCit-aligned design-enabler gap score",
            "native_direction": "lower is better",
            "normalized_direction": "higher is better",
            "normalized_status": "internal presentation transformation; not an official CIRCit score",
        },
        "before": before,
        "after": after,
        "comparison": {
            "normalized_score_point_change": _round(point_change),
            "native_gap_reduction": _round(native_reduction),
            "relative_change_from_baseline_percent": _round(relative_change),
            "remaining_design_gap_closed_percent": _round(remaining_gap_closed),
            "direction": "improved" if point_change > 0 else "worsened" if point_change < 0 else "unchanged",
        },
        "criteria": contributions,
        "limitations": [
            "Scores are comparable only under the same functional unit, boundary, criteria, importance weights, and data-quality rules.",
            "Evidence coverage is separate from performance and does not validate assumptions.",
            "This result is not an MCI, LCA, certification, safety review, or proof of sustainability improvement.",
        ],
    }


def example() -> dict[str, Any]:
    return {
        "product": "Example product",
        "functional_unit": "Deliver the required service for one year",
        "system_boundary": "Product and replacements required for the functional unit",
        "time_horizon": "10 years",
        "geography": "Named market and recovery region",
        "use_conditions": "Indoor use, 2 hours per day",
        "scoring_rules": "Importance 0-3; fulfillment 1/3/5; unknown evidence is not failure",
        "criteria": [
            {
                "id": "repair-access",
                "name": "Access to repair-critical parts",
                "importance": 3,
                "before_fulfillment": 5,
                "after_fulfillment": 1,
                "before_evidence": "documented",
                "after_evidence": "estimated",
                "note": "Redesign replaces a bonded cover with reversible fasteners.",
            },
            {
                "id": "actual-recovery-route",
                "name": "Plausible collection and recovery route",
                "importance": 2,
                "before_fulfillment": 5,
                "after_fulfillment": 3,
                "before_evidence": "documented",
                "after_evidence": "assumed",
            },
        ],
    }


def self_test() -> None:
    data = example()
    result = calculate(data, strict=True)
    assert result["before"]["native_gap_score"] == 25.0
    assert result["after"]["native_gap_score"] == 9.0
    assert math.isclose(result["before"]["normalized_design_score"], 0.0)
    assert math.isclose(result["after"]["normalized_design_score"], 80.0)
    assert result["comparison"]["native_gap_reduction"] == 16.0
    assert result["comparison"]["direction"] == "improved"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("input", nargs="?", type=Path, help="Input assessment JSON file")
    mode.add_argument("--example", action="store_true", help="Print an example input JSON")
    mode.add_argument("--self-test", action="store_true", help="Run built-in invariant checks")
    parser.add_argument("--output", type=Path, help="Write result JSON to this file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require complete comparison framing before calculation",
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
        with args.input.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
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
