# Concept Development and CAD Readiness

Use this reference after the baseline, goals, and priority requirements are established.

## Generate structurally different concepts

Concepts may vary in service delivery, operating principle, product architecture, form, components, module boundaries, lifetime strategy, material route, manufacturing route, joint logic, next-use loop, return system, or value-network configuration. Do not anchor alternatives to the original product form or technical solution. Preserve the required service, functions, comparable performance, use conditions, and safety constraints unless an explicit, separately compared compromise is accepted. Do not present color, styling, or superficial material swaps as distinct circular concepts when the architecture and loop remain unchanged.

For every concept, explain:

- how it works and how its architecture differs;
- which functions and performance conditions are preserved and which are compromised;
- the causal mechanisms that improve circularity rather than only naming a strategy;
- advantages, disadvantages, critical assumptions, and success conditions;
- maintenance, spare-part, collection, inspection, cleaning, refurbishment, remanufacture, and recovery needs;
- any additional equipment or service change, included within the comparison boundary.

### Determine the number of alternatives

Treat three concepts as a practical lower bound for ordinary concept exploration, not a universal circularity rule. Generate the number needed to cover the priority hotspots and credible loop architectures—normally three to five alternatives, with fewer or more when justified by product simplicity, complexity, risk, or value-network choices. Keep the unchanged baseline as a reference but do not count it as an alternative.

Do not generate one concept mechanically for each strategy. Use exactly the six design axes from framework.md as matrix rows: Narrow, Slow (long life), Slow (life extension), Close, Regenerate, Inform. Treat maintain, repair, reuse, refurbish, remanufacture and recycle as component routes in the separate hierarchy, not alternative names for those axes. Add a concept when it introduces a meaningful architecture or loop covering an important unresolved hotspot.

### Standard concept sheet and feasibility decision

Use the same sheet structure for every retained concept:

1. Concept ID, delivered function, operating principle and a short use sequence.
2. Component/module list, interfaces, retained/replaced parts and relevant material/process candidates.
3. Design strategy axes, causal circular mechanisms and condition-dependent component routes.
4. Common circularity indicators versus the baseline, value status, assumptions and evidence confidence.
5. Specific advantages and disadvantages, including added material, complexity, user effort, cost or infrastructure when applicable.
6. Feasibility matrix and critical uncertainties, followed by the next calculation, prototype or test that can resolve each one.
7. Explanatory visual tied to this sheet, with a recorded consistency check.

Assess these feasibility dimensions for each concept, marking non-applicable entries with reasons:

| Dimension | Required question/evidence |
|---|---|
| Function and physical principle | Can it deliver the required service under the stated conditions? Use proportionate calculations, precedents or tests; identify missing loads, capacity, energy or flow requirements. |
| Materials and manufacturing | Are candidate materials, processes and interfaces compatible with the function and proposed production scale? Distinguish available capability from assumed supplier capability. |
| Assembly, disassembly and service | Can parts be assembled, accessed, replaced and reassembled with the proposed tools and clearances? Check spare availability and repair tasks. |
| Safety and essential constraints | Which mandatory requirements are satisfied, failed or unresolved? Specify evidence without claiming certification. |
| User operation | Are handling, cleaning, maintenance, dosing or other relevant tasks practical? Identify usability tests and changed user obligations. |
| Economics and implementation | What drives initial and lifecycle cost, who pays, and what volumes/capacity are needed? Do not invent exact costs or operators. |
| Circular loops | Do retention/recovery actors, acceptance criteria, logistics and next-use demand exist, or remain assumptions? |

For each dimension, record status, rationale, evidence and verification action. Use statuses: supported at stated maturity; plausible but unverified; blocked by identified constraint; not applicable. Use precise confidence, not an unsupported universal feasibility percentage. An unknown is not a pass or a failure. A blocked mandatory requirement excludes the current concept; plausible concepts remain conditional candidates for development. A numerically high circularity score never compensates for a non-working operating principle.

### Comparable concept images and visual consistency

For an end-to-end run, illustrate every retained concept before selection. Prefer one coherent comparison board; separate images are acceptable when density would reduce clarity. Keep approximately consistent:

- viewpoint, scale, crop, background, and lighting;
- product orientation and user context;
- visible module boundaries and retained/replaced parts;
- exploded or return-loop logic when it differentiates the concept;
- visual maturity and annotation density.

Use concise concept identifiers that match the comparison matrix. Mark generated views as illustrative and assumption-based. Do not allow rendering quality, color, or styling to substitute for architecture evidence. After selection, create a more detailed final render that remains consistent with the selected module tree and later STEP model.

Create the architecture brief before its image. Include an overall view and, where needed to explain the mechanism, an exploded, sectional or sequential explanatory view. Identify the function of key parts, what remains, what is replaced, and the intervention/return path. Do not rely on an attractive exterior render to explain an invisible mechanism.

Use a controlled schematic or CAD-derived diagram for exact component relationships, dimensions, connections, movement, fluid/electrical paths or disassembly order. Use image generation for illustrative appearance; its details are not engineering evidence. Keep annotations and dimensions controlled and legible; do not invent specifications to fill a visual.

Inspect every concept image against the written sheet before presenting it as checked. Verify:

- component count/identity, boundaries and interfaces match the described architecture;
- no invented functional module, connector, fastener or performance claim was added;
- assembly and exploded views agree; the shown access and separation directions are consistent;
- visible connections, motion and flows do not contradict the described operating principle;
- retained/replaced parts and any added equipment are identified consistently;
- assumed dimensions/materials and unresolved internal mechanisms are labelled;
- legible labels correspond to the concept ID and component list.

Correct or regenerate inconsistent images; simplify to a controlled schematic when exact geometry cannot be represented reliably. State unresolved visual limitations rather than certifying an unseen or unchecked view. Never promise zero hallucination: a visual consistency review reduces identifiable errors and is not physical validation.

For the selected concept, derive the final technical views from the actual CAD model wherever available. Keep any separate illustrative rendering clearly subordinate to that model. Do not reverse-engineer invented engineering dimensions from generated pixels.

## Circular design-for-X review

Apply the relevant subset:

- durability, reliability, attachment, and continued desirability;
- inspection, cleaning, maintenance, and repair;
- modularity, standardization, compatibility, and upgrade;
- non-destructive disassembly and reassembly;
- reuse, refurbishment, remanufacture, and repurposing;
- material identification, separation, and high-quality recycling;
- safe biological return when justified;
- manufacturing, assembly, logistics, reverse logistics, traceability, and condition assessment.

Check conflicts including durability versus separability, sealing versus repair access, lightweighting versus robustness, modularity versus added material, recycled content versus performance, and shared use versus accelerated wear.

## CAD maturity levels

### Visual concept

Communicates form and intended architecture but is not geometry evidence.

### Parametric concept model

Requires approximate or explicitly assumed dimensions, module boundaries, interfaces, component envelopes, and chosen mechanisms. It supports packaging and design discussion, not production release.

### Engineering CAD

Requires controlled dimensions, tolerances, material grades, interfaces, load cases, safety requirements, manufacturing constraints, standard parts, and validation responsibilities.

### Production release

Requires domain review, calculations, drawings, tolerances, configuration control, prototypes, tests, supplier validation, and regulatory evidence. This skill alone does not authorize production release.

## Minimum CAD-ready handoff

Provide the functional architecture, module tree, overall envelope, critical dimensions, interfaces, datum scheme, component envelopes, keep-out zones, material candidates, joints, fasteners, access directions, tool clearances, assembly and disassembly sequence, service access, expected loads, operating environment, manufacturing assumptions, tolerances needing resolution, validation plan, and unresolved risks.

If exact geometry is unavailable, use dimension ranges and label the model as conceptual.

## Assumption-led conceptual STEP

When the user wants the full workflow but measured geometry is unavailable, create a conceptual STEP from the frozen assumption register rather than stopping at a written brief. The model may communicate:

- overall envelope and proportions;
- module boundaries and body count;
- replaceable versus retained units;
- access and disassembly directions;
- nonfunctional interface envelopes;
- keep-out volumes and dummy component envelopes.

Do not invent functional safety geometry. Replace hazardous or safety-critical features with blunt, blocked, oversized, disabled, or otherwise nonfunctional envelopes. Use explicit names such as `CONCEPT_NONFUNCTIONAL`, `DUMMY_ENVELOPE`, or `NOT_FOR_MANUFACTURING` in the assembly and filenames.

For modular products, export the assembly plus useful individual part files and the parametric source. Record which dimensions are provided, measured, externally sourced, estimated, or assumed.

## Visual and CAD output rules

- Rendered images do not validate fit, strength, assembly, or manufacturability.
- Exploded views must match the stated module and disassembly logic.
- Check CAD exports for file integrity, units, body count, and expected dimensions when tooling permits.
- Round-trip import each final STEP or at least the assembly and record the imported solid count and bounding box. Use `scripts/verify_step.py` when CadQuery is available.
- Keep the rendered concept, CAD brief, and exported module tree consistent. If they differ, state which artifact controls the current concept.
- Prefer STEP for neutral solid geometry; use STL or 3MF primarily for mesh-based prototyping and DXF for appropriate 2D geometry.
