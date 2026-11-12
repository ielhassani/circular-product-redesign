# Multi-Concept Comparison Data

Use this schema with `scripts/compare_concepts.py` when comparing a baseline with several redesign concepts.

This schema covers supplementary design-enabler scoring, not the full roadmap assessment. Supply the roadmap application table, six-axis strategy matrix and component routing register separately. The script does not validate these, calculate MCI, or propagate material flows. Interpret its ranking as a design-score ranking only; physical indicators, route evidence and mandatory gates determine the conditional recommendation.

```json
{
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
        {
          "id": "virgin-material",
          "name": "Virgin material per functional unit",
          "value": 100,
          "unit": "g/FU",
          "value_status": "calculated",
          "evidence": "estimated",
          "source": "Measured product mass plus documented replacement schedule",
          "confidence": "medium"
        }
      ],
      "gates": [
        {"id": "function", "name": "Required function", "status": "pass", "note": "Reference performance"}
      ]
    },
    {
      "id": "concept-a",
      "name": "Modular concept",
      "kind": "concept",
      "advantages": ["Retains the durable structure"],
      "disadvantages": ["Adds an interface"],
      "physical_indicators": [
        {
          "id": "virgin-material",
          "name": "Virgin material per functional unit",
          "value": 35,
          "unit": "g/FU",
          "value_status": "design_target",
          "evidence": "assumed",
          "source": "Concept mass budget and assumed replacement schedule",
          "confidence": "low"
        }
      ],
      "gates": [
        {"id": "function", "name": "Required function", "status": "unknown", "note": "Prototype required"}
      ]
    }
  ],
  "criteria": [
    {
      "id": "life-matching",
      "name": "Match component lives to wear",
      "importance": 3,
      "ratings": {
        "baseline": {"fulfillment": 5, "evidence": "documented", "note": "Whole product is replaced."},
        "concept-a": {"fulfillment": 1, "evidence": "assumed", "note": "Only the worn module is replaced."}
      }
    }
  ],
  "sensitivity_scenarios": [
    {
      "id": "low-take-back",
      "name": "Low take-back",
      "assumptions": {
        "concept-a take-back rate": "20% instead of 70%"
      },
      "fulfillment_overrides": {
        "concept-a": {"life-matching": 1}
      },
      "note": "Low take-back changes collection-dependent physical outputs, not the life-matching design criterion by itself. Recalculate those flows separately; add a collection-specific scoring criterion only with an explicit causal rating rule."
    }
  ]
}
```

## Rules

- Include exactly one case with `kind: baseline` and one or more cases with `kind: concept`.
- Use stable case IDs that also identify the images and report rows.
- Every criterion must rate every case.
- `importance`: `0`, `1`, `2`, or `3`.
- `fulfillment`: `1` fulfilled, `3` partly fulfilled, or `5` not fulfilled.
- Evidence: `measured`, `documented`, `estimated`, `assumed`, or `unknown`.
- Gate status: `pass`, `fail`, `unknown`, or `not_applicable`.
- Keep advantages and disadvantages concise and product-specific.
- Physical indicators must use the same definitions and units across comparable cases.
- Give each physical indicator a stable `id`. In `--strict` mode, every case must provide the same indicator IDs and units, plus `value_status`, `evidence`, `source`, and `confidence`.
- `value_status`: `measured`, `calculated`, `estimated`, `assumed`, `design_target`, or `unknown`.
- `confidence`: `high`, `medium`, `low`, or `unknown`.
- Define the functional unit, system boundary, time horizon, geography, use conditions, and scoring rules before calculation. `--strict` requires these fields.

## Sensitivity scenarios

Each scenario may include:

- `importance_overrides`: criterion IDs mapped to new importance values;
- `fulfillment_overrides`: case IDs mapped to criterion IDs and new fulfillment values;
- `assumptions`: a JSON object recording the lifetime, mass, repair frequency, take-back, or other changed assumptions that justify the overrides;
- `note`: interpretation or rationale.

The script recalculates rank groups, identifies ties, and reports whether the top-ranked group changes from the base scenario. It does not infer how a changed physical assumption alters a fulfillment rating; document that causal mapping in the scenario.

Use the output field `supplementary_design_score_ranking`. The legacy compatibility field `circularity_ranking_only` contains the same ordering but does not represent actual circularity outcomes or hierarchy routes. Neither field makes the selection decision, merges sustainability into circularity, or overrides mandatory gates. Interpret physical indicators and route evidence separately.

## Run

```text
python scripts/compare_concepts.py comparison.json --strict --output comparison-results.json
```

Print an example or run invariant checks with:

```text
python scripts/compare_concepts.py --example
python scripts/compare_concepts.py --self-test
```

