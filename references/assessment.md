# Assessment and Scoring

Use this reference for baseline measurement, concept comparison, and before/after claims.

## Continuous assessment and method boundaries

Establish the baseline at roadmap Step 0; update forecasts, requirements and feasibility at Steps 1-5; reassess and validate at Step 6. Keep current evidence, design targets, scenario estimates and achieved outcomes in separate columns.

Use ISO 59020:2024 as a measurement/assessment framework, not as a substitute for a product-specific method or a claim of conformity. Use MCI as a product material-flow/utility method only with adequate inputs and the published methodology. Keep the internal CIRCit-aligned design-enabler score supplementary. Do not require a fabricated score to complete a baseline diagnosis; supported indicators plus explicit unknowns are valid.

Prefer physical-flow and useful-service comparisons over ranking by design score alone. The hierarchy is an ordinal preference for component routing, not a numerical scoring scale. Do not score strategy counts, assume all recycling equals high-quality closed-loop production, or treat data availability as achieved circularity.

## Indicator definitions and denominators

Select the relevant panel for the product; keep definitions identical across cases. Report value, unit, numerator/denominator, cohort/time, source, status, range/confidence and verification method. A non-applicable indicator is not zero; an unknown value is not a failure.

| Indicator | Definition and safeguards |
|---|---|
| Material demand per service | Sum material inputs for initial units, replacement parts, consumables and allocated enabling equipment over the comparison service, divided by delivered functional units. State virgin, secondary and total material separately. Do not subtract speculative future recycling from present virgin demand. |
| Useful life | State years, cycles or operating hours with required performance, duty and failure criterion. Distinguish tested life from target life and lifetime extensions from accelerated use. |
| Mass retained after intervention | Mass of the original assembly remaining in use after a precisely defined repair divided by its original mass. Include replacement input separately; do not assume retained mass alone equals retained function/value. |
| Repair coverage | Identify the denominator: relevant failure modes, observed failure events, or failed units. Prefer frequency-weighted coverage when frequencies exist; do not label an unweighted fraction of modes as a repaired-unit rate. |
| Disassembly/serviceability | Time, operations, tools, damage and reassembly success for an identified target component and task, with test conditions. Full teardown and selective repair access are different tasks. |
| Collection rate | Collected eligible end-of-use units or mass divided by the defined eligible end-of-use cohort in the period. Sales in that period are not automatically the denominator for long-lived products. |
| Route acceptance | Units/mass accepted for a route divided by units/mass inspected for that route. Name acceptance criteria, destination and the excluded/rejected fractions. |
| Actual route output | Units or mass successfully redeployed/recovered divided by a named common cohort; record output quality and destination. Distinguish mass, unit count and economic-value denominators. |
| Economic value retention | Specify residual asset/component value or avoided replacement expenditure, currency, date and boundary; keep it separate from material circularity and net service cost. |

For a simple single-material recovery chain with aligned mass bases, recovered fraction of end-of-use material = collection fraction x acceptance fraction of collected material x processing yield of accepted material. For branches and changing compositions, calculate each mass flow explicitly. These are bookkeeping relationships, not MCI. Label assumed rates and propagate ranges. Example only: 0.60 collection x 0.80 acceptance x 0.90 yield = 0.432 actual/scenario output fraction, not 0.90 recovery of all end-of-use material.

At a single routing event, account for all mutually exclusive destinations plus rejects/losses; shares must reconcile to the denominator. Track sequential lifetimes separately to avoid double-counting a reused component and its later recycled mass as simultaneous outcomes. Include inventory and time lags when material.

Show absolute differences and percentage changes only for meaningful nonzero baselines. For a zero baseline, show absolute change and mark relative change undefined. Run physical sensitivity for lifetime/replacements, collection, acceptance/yield, remaining-life demand and logistics; the existing design-score scripts do not propagate these flows.

## Keep three assessment layers separate

### Circularity performance

Assess functional delivery, use intensity, resource inflows, durability, repair, upgrade, modularity, standardization, compatibility, disassembly, reuse, refurbishment, remanufacture, repurposing, actual collection, material recycling, biological cycles, reverse logistics, traceability, spare parts, instructions, and responsible loop actors. Include renewable energy share, circular water flows, and economic value retention when relevant.

### Sustainability consequences

Report lifecycle energy and greenhouse-gas emissions, water, resource depletion, toxicity, pollution, land use, ecosystem effects, lifecycle cost, affordability, profitability, health, safety, labor conditions, accessibility, and distributional effects as relevant.

Circularity is not a proxy for these outcomes. Use an ISO 14040/14044-aligned lifecycle approach for environmental claims when the requested rigor and data justify it.

### Engineering and implementation feasibility

Check function, performance, safety, regulation, reliability, quality, manufacturability, assembly, tolerances, supply capability, user acceptance, service capability, cost, schedule, and organizational readiness. Treat failed mandatory requirements as gates, not low-weight criteria.

## CIRCit-aligned design gap score

Before calculation, freeze and report the functional unit, system boundary, time horizon, geography, use conditions, criteria, importance weights, fulfillment rules, and data-quality rules. If the actual product evidence cannot support a rating, do not turn `unknown` into `not fulfilled`. Either leave the real characteristic unscored and explain the gap, or rate a separately named hypothetical reference scenario with explicit assumptions and ranges.

For each relevant criterion, use:

- importance `I`: 0 not relevant, 1 slightly important, 2 moderately important, 3 highly important;
- fulfillment `F`: 1 fulfilled, 3 partly fulfilled, 5 not fulfilled.

The native gap contribution is `G_i = I_i * F_i`, and the native total is `G = sum(G_i)`. Lower native totals are better. Use the same criteria and importance values for before/after comparison.

### Optional normalized presentation

To present an intuitive internal score from 0 to 100 where higher is better:

- `G_min = sum(I_i * 1)`
- `G_max = sum(I_i * 5)`
- `S = 100 * (G_max - G) / (G_max - G_min)`

Call this the **normalized CIRCit-aligned design score**, not an official CIRCit score, certification, or universal percentage of circularity.

For before/after comparison, report score-point change, native gap reduction, relative change against the baseline only when meaningful, and share of remaining design gap closed. Use `scripts/calculate_scores.py --strict` for a complete comparison. Read [scoring-data.md](scoring-data.md) for the input schema and interpretation rules.

## Multi-concept comparison

When more than one redesign concept is retained, score the baseline and **every** retained concept—not only the finalists—with the same functional unit, boundary, criteria, importance weights, and evidence rules. Use `scripts/compare_concepts.py` and the schema in [concept-comparison-data.md](concept-comparison-data.md).

For each case, report together but keep distinct:

- native and normalized CIRCit-aligned design scores;
- physical indicators per functional unit;
- weighted evidence coverage;
- mandatory-gate status;
- circularity advantages and disadvantages;
- sustainability consequences and possible burden shifts;
- technical, safety, cost, user, supplier, and implementation risks.

Use a common physical-indicator panel suited to the product. Include when relevant:

- intended service life under the stated conditions;
- virgin material demand per functional unit, including expected replacements;
- mass retained after a precisely defined repair event;
- disassembly time, operation count, tools, and destructive steps;
- component or product reuse and refurbishment potential;
- collection and recovery rates, explicitly labeled as actual, estimated, assumed, or design targets.

For every value, record unit, definition, value status (`measured`, `calculated`, `estimated`, `assumed`, `design_target`, or `unknown`), evidence class, source or calculation basis, and confidence. A normalized design score is not a universal circularity percentage.

The script ranks supplementary design scores for the frozen scenario, reports ties, and evaluates explicit rating/weight scenarios. This is not an overall circularity ranking or a selection decision. A failed or unresolved mandatory gate cannot be compensated by a higher score. Explain the causal basis for each rating override; do not reduce a repairability rating just because collection declines unless that dependency is established. Separately recalculate physical outcomes for influential life, replacement, collection and yield assumptions. State which preferences remain robust.

## Material Circularity Indicator

Use the Material Circularity Indicator only when material-flow, collection, recycling-efficiency, lifetime, and use-intensity data are adequate. Follow the published methodology or official calculator. Do not substitute the normalized CIRCit-aligned design score for MCI.

MCI focuses on material flows and utility. Complement it with material criticality, toxicity, environmental impacts, economics, and design-enabler evidence.

## ISO 59020-aligned indicator panel

Use a panel rather than forcing all data into one number. Candidate measures include:

- percent reused, recycled, and sustainably produced renewable content in inflows;
- product lifetime relative to an appropriate reference;
- percent of actual products or components reused from outflows;
- percent of actual material recycled from outflows;
- percent safely recirculated in biological cycles;
- renewable energy share;
- circular water indicators when relevant;
- retained economic value or lifecycle economics when relevant.

Distinguish actual outcomes from design potential. A recyclable material is not an actual recycled outflow without a plausible collection, sorting, and recycling route.

## Energy and locality classification

- Total energy per functional unit and associated emissions are sustainability indicators.
- Renewable energy share can be reported as a circularity indicator, but it does not replace total energy demand.
- Supplier distance is a contextual variable, not a positive score by itself.
- Evaluate supplier transport as mass, distance, mode, load factor, returns, and storage when data permit.
- Treat local sourcing as circular only when it demonstrably enables secondary inputs, repair, take-back, component reuse, remanufacture, high-quality recycling, or traceability.
- Treat local sourcing as environmentally or socially beneficial only when lifecycle or social evidence supports that conclusion.

## Evidence confidence

Keep confidence separate from performance:

| Class | Meaning |
|---|---|
| `measured` | Direct measurement or verified operational record |
| `documented` | Traceable drawing, BOM, supplier declaration, manual, or validated database |
| `estimated` | Engineering estimate with stated method or range |
| `assumed` | Plausible assumption without direct support |
| `unknown` | No defensible value available |

The calculation script reports weighted evidence coverage as a diagnostic. Do not multiply performance by confidence, because poor evidence is not the same as poor circularity.

## Comparability checklist

Before claiming improvement, confirm the same functional unit, required service and performance, lifecycle boundary, temporal and geographic boundary, criteria, importance weights, reference lifetime, use assumptions, supporting equipment, and data-quality rules. Address rebound, burden shifting, and displaced impacts where material. Evaluate environmental impacts, total energy, cost, and implementation feasibility separately from circularity; an energy saving is not automatically a circularity improvement.
