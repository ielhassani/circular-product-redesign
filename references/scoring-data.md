# Scoring Data Schema

Use this schema with `scripts/calculate_scores.py`.

```json
{
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
      "note": "Redesign replaces bonded cover with reversible fasteners."
    }
  ]
}
```

## Allowed values

- `importance`: `0`, `1`, `2`, or `3`.
- `before_fulfillment` and `after_fulfillment`: `1`, `3`, or `5`.
- evidence: `measured`, `documented`, `estimated`, `assumed`, or `unknown`.

Use the same importance value for both cases. If importance changes after seeing the redesign, the comparison is vulnerable to goalpost shifting. Revisit and document the baseline assessment instead of silently changing the weight.

## Run the calculation

```text
python scripts/calculate_scores.py assessment.json --strict --output results.json
```

Print a valid example with:

```text
python scripts/calculate_scores.py --example
```

Run the built-in invariant checks with:

```text
python scripts/calculate_scores.py --self-test
```

## Interpretation

- The native gap score is CIRCit-aligned: lower is better.
- The normalized score is an internal transformation: higher is better.
- Evidence coverage is reported separately and never changes the performance score.
- A positive score-point change or native gap reduction indicates improvement.
- A result is comparable only when the functional unit, boundary, requirements, criteria, and weights are unchanged.
- Define the functional unit, system boundary, time horizon, geography, use conditions, criteria, weights, and rating rules before running the calculation. `--strict` requires these context fields.
- Do not encode unknown real-product characteristics as `5` merely because evidence is missing. If a score requires a rating, calculate a separately labeled hypothetical reference scenario and preserve the real-product unknown in the evidence register.

