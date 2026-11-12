# Evidence and Intake

Use this reference when the task starts from images, incomplete product information, or an ambiguous request.

## Decision-changing opening intake

Do not repeat default preferences or ask a fixed questionnaire. Before a substantive diagnosis, ask only unanswered questions whose answers could change the next decision, normally two to four at a time. Cover the highest-value subset of:

- exact product and service;
- intended user and operating conditions;
- waste, failure, cost, safety, or obsolescence problem;
- dimensions, mass, views, drawings, model identifier, or physical access;
- functions, interfaces, safety constraints, appearance, or business constraints that must not change;
- any proposed change to the delivered service and any additional equipment it would require;
- intended final depth.

If the user does not specify a depth, explain that the default complete path ends with a final conceptual redesign, comparison, CAD-ready brief, and checked conceptual STEP. Do not ask every possible question at once.

## Evidence register

Maintain a compact register with these fields:

| Field | Meaning |
|---|---|
| Item | The claim, dimension, material, function, process, or outcome being considered |
| Status | `provided`, `observed`, `externally sourced`, `assumed`, `calculated`, or `unknown` |
| Source | File, image, drawing, manual, supplier, interview, calculation, or URL |
| Confidence | `high`, `medium`, `low`, or `unknown` |
| Decision relevance | What decision would change if the item were wrong |
| Validation action | Measurement, disassembly, supplier query, test, search, or review |

Do not convert an observed color, texture, or shape into a definitive material or process identification. Do not label hidden joints, poor repairability, inaccessible components, or end-of-use outcomes as observed from a photograph. Keep unknown evidence separate from an assumption introduced to continue the analysis.

## Information levels

### Level A — Visual exploration

Typical inputs:

- one or more images;
- product name or likely product category;
- intended function;
- redesign motivation.

Permitted outcomes:

- visible-feature inventory;
- preliminary lifecycle and architecture hypotheses;
- possible circularity hotspots;
- alternative design directions;
- targeted requests for evidence.

Do not provide an evidence-backed material circularity score or production-ready CAD at this level. A photo-only weakness may be framed as a hypothesis to test, not an observed defect.

### Level B — Concept assessment

Useful additional inputs:

- multiple orthogonal views and a scale reference;
- approximate overall dimensions and mass;
- user, context, duty cycle, and expected life;
- known materials and assembly methods;
- common failures, maintenance, and repair practices;
- current end-of-use route.

Permitted outcomes:

- baseline architecture;
- provisional scoring with confidence labels;
- concept comparison;
- preliminary exploded view and CAD-ready brief.

### Level C — Engineering development

Useful additional inputs:

- drawings, CAD, interface control information, and tolerances;
- bill of materials with masses and material grades;
- functional and safety requirements;
- manufacturing processes and production volume;
- verified failure, repair, return, recycling, and supplier data;
- regulatory and test requirements.

Permitted outcomes depend on the available engineering and CAD tools. Detailed design still requires appropriate domain review and physical verification.

## Progressive questions

Ask only questions whose answers can change the next decision. Ask two to four at a time, usually in this order:

1. What exact service must the product provide, to whom, and under what conditions?
2. What failure, cost, waste, obsolescence, or user problem motivates the redesign?
3. What dimensions, mass, model identifier, drawings, or additional views are available?
4. Which functions, safety constraints, interfaces, or appearance features must not change?
5. What is known about materials, joints, internal components, production, maintenance, and end-of-use?
6. Which circular outcome matters most: longer life, repair, upgrade, reuse, refurbishment, remanufacture, recycling, biological return, or reduced material demand?
7. What output is required now: diagnostic, concepts, score, report, render, or CAD-ready handoff?

If the answer is unknown, do not stall automatically. Record an assumption, choose a conservative range when useful, show the decision sensitivity, and add a validation task.

## Assumption fallback protocol

When useful evidence is unavailable and the user wants to continue:

1. Record the missing item as `unknown`.
2. Add a separate `assumed` value or range; do not replace the unknown record.
3. State the rationale and which decision the assumption enables.
4. Prefer an envelope or conservative range over false precision.
5. Mark whether changing the assumption could alter concept selection, scoring, mass indicators, geometry, or safety.
6. Add a physical measurement, supplier query, test, or review to the validation plan.

## Real baseline and constructed reference scenario

When data are incomplete, present two layers in this order:

1. **Evidence-supported real-product assessment:** state what can and cannot be concluded about the actual product from provided data, observations, and external sources.
2. **Hypothetical reference scenario, if needed:** give it a distinct name and version; define central values, plausible ranges, rationale, and validation actions. Use this scenario for calculations only when the real evidence is insufficient.

Never transfer a hypothetical material, mass, joint, lifetime, failure rate, or recovery route back onto the photographed product as fact. Do not assign a poor fulfillment rating solely because a characteristic is unknown. If a score needs a rating, rate the explicit constructed scenario and label the result accordingly.

For the final constructed scenario, freeze the assumptions in a versioned register so the report, render, score, CAD brief, and STEP use the same values.

## Image request guidance

When more images would materially help, request:

- front, rear, both sides, top, and underside;
- open, partially disassembled, or internal views when safe;
- labels, fasteners, connectors, wear areas, and failed parts;
- a ruler or object of known size in the same plane as the feature being estimated.

Perspective images with a scale object support rough estimates only. They do not replace calibrated photographs, scans, or drawings.
