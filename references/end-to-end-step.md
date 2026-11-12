# End-to-End Conceptual STEP Workflow

Use this reference when the user wants the redesign carried through to a STEP file, including when measured geometry is incomplete.

## 1. Declare the maturity

Choose one label and repeat it in the report, CAD brief, model names, and filenames:

- `CONCEPT_NONFUNCTIONAL` for assumption-led geometry that cannot be used as a functioning product;
- `PARAMETRIC_CONCEPT` when interfaces and envelopes are meaningful but not released;
- `ENGINEERING_CAD` only when controlled dimensions, materials, tolerances, loads, safety requirements, and review responsibilities exist.

Missing data normally leads to `CONCEPT_NONFUNCTIONAL`, not to a fabricated engineering model.

## 2. Freeze the constructed scenario

Before modelling, version the assumptions for:

- overall envelope and module dimensions;
- part count and retained/replaced units;
- material candidates;
- joints, access directions, and disassembly order;
- reference components and their nominal envelopes;
- functional life and physical-indicator allocations;
- omitted or neutralized safety-critical features.

Use the same values in the render, report, CAD brief, score interpretation, and model.

Record the selected concept ID and decision status (user choice, delegated choice, or provisional recommendation). Use its reviewed architecture and dimension register as the modelling source; do not turn an image directly into purportedly verified engineering geometry. Before export, reconcile the component list, interfaces and model with the selected concept's feasibility conditions. Mark unresolved interfaces and assumptions explicitly.

Do not begin this selected-concept modelling stage until the baseline diagnosis, baseline calculation or explicit reference scenario, comparable concept illustrations, measures for every retained concept, comparison table, and ranking sensitivity have been presented and the selection rationale has been recorded.

## 3. Select the CAD route

1. Prefer an available native CAD or parametric solid-modelling capability.
2. If none is available, create product-specific parametric source for a suitable solid kernel.
3. If a workspace-local dependency is necessary, request authorization before downloading or installing it.
4. Do not claim a STEP exists until the file has been created and checked.
5. If no backend can be used after safe in-scope attempts, deliver the source and brief and report STEP generation as blocked rather than silently ending the workflow.

Do not embed one product's geometry as a universal generator. The product architecture should determine the source model.

## 4. Neutralize unresolved hazards

For sharp, electrical, pressure-containing, load-bearing, medical, child-safety, food-contact, or other consequential products:

- use dummy envelopes instead of functional hazardous parts;
- omit cutting edges, live contacts, pressure seals, released load paths, or clinical interfaces;
- leave critical gaps, exposure, clearances, retention forces, tolerances, and materials unresolved;
- prevent a conceptual model from appearing production-authorized through filenames and metadata.

## 5. Export package

For a modular product, normally provide:

- assembly STEP;
- individual part STEP files when they aid inspection or reuse;
- parametric source;
- CAD README with units, maturity, assumptions, omitted geometry, and restrictions;
- machine-readable verification result.

Prefer names such as `Product_CONCEPT_NONFUNCTIONAL_v1.step`.

## 6. Verify

At minimum check:

- STEP file is non-empty and has a valid ISO-10303 header;
- schema when detectable;
- units;
- expected body or solid count;
- round-trip import;
- overall bounding box and critical envelopes;
- individual part integrity;
- correspondence with the module tree and exploded view.

Where the model detail and tools permit, inspect interference, intended mating/access clearances and assembly/disassembly paths. Record what was actually checked and what remains unverified; do not report these as passed merely because the STEP opens. Generate final explanatory CAD views from the checked model and correct any earlier illustrative view that contradicts it.

Run `scripts/verify_step.py INPUT.step --expected-solids N --output verification.json` when CadQuery is importable. A successful check proves file integrity only; it does not prove safety, fit, strength, manufacturability, or compliance.

## 7. Handoff language

State separately:

- directly evidenced geometry;
- externally sourced component envelopes;
- assumed geometry;
- calculated indicators;
- deliberately omitted functional geometry;
- tests, supplier confirmations, detailed engineering, and independent reviews still required.

