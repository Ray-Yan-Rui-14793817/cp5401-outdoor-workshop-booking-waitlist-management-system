# Requirements and Test Traceability

L0 revision 3. All execution links are PENDING. Later add test function/parameters, environment/SHA, observed result, CI or human evidence, PR decision and release.

Definitions: [requirements](../requirements.md), [rules](business-rules.md), [risks](risks.md), [tests](test-plan.md), [workflow](development-workflow.md).

## Functional coverage

| Requirement | Rules | Quality and risks | Planned scenarios and loops |
|---|---|---|---|
| FR-01 | BR-01, BR-14 | QR-03, QR-04; R-03, R-04 | B01, B02, I06, I08; L2 |
| FR-02 | BR-03, BR-04, BR-16 | QR-01, QR-04; R-05, R-08 | B06, B15, W13, I06, VAL-01; L3/L6 |
| FR-03 | BR-01, BR-03, BR-04, BR-05, BR-07, BR-12, BR-13, BR-16 | QR-01, QR-02; R-01, R-05, R-07 | B07, B08, B09, B14, B15, B17, I01, I02, I05, I10; L4 |
| FR-04 | BR-01, BR-03, BR-06, BR-10, BR-13, BR-16 | QR-01, QR-02, QR-03; R-02, R-03, R-05 | B11, B12, B15, B16, W06, W07, W10, I04, I05, I10; L5/L8 |
| FR-05 | BR-01, BR-06, BR-07, BR-14 | QR-03, QR-04; R-03, R-04, R-08 | B10, B17, W13, I06, I08, VAL-01; L4/L7 |
| FR-06 | BR-01, BR-02, BR-03, BR-14, BR-15 | QR-01, QR-03; R-03, R-05 | B03, B04, B05, B13, VAL-02; L3 |
| FR-07 | BR-01, BR-04, BR-16 | QR-03, QR-04; R-03, R-08 | B13, W14, I06, I08, VAL-02; L3/L7 |
| FR-08 | BR-01, BR-03, BR-05, BR-08, BR-09, BR-13, BR-16 | QR-01, QR-02; R-01, R-02, R-05 | W01, W02, W03, W04, W05, W09, W12, I03, I07, I10; L7 |
| FR-09 | BR-01, BR-03, BR-06, BR-11, BR-13, BR-16 | QR-01, QR-02, QR-03; R-02, R-03, R-05 | W08, W09, W12, W16, I05, I10; L7 |
| FR-10 | BR-03, BR-06, BR-09, BR-10, BR-12, BR-13, BR-16 | QR-01, QR-02; R-02, R-05, R-07 | W05, W06, W07, W08, W10, W11, W12, W15, I03, I04, I05, I10; L8 |
| FR-11 | BR-01, BR-09, BR-11, BR-16 | QR-03, QR-04; R-03, R-08 | W13, W14, I06, I07, VAL-03, VAL-03A, VAL-03B, VAL-03C, VAL-03D, VAL-03E; L7/L8 |

## Rule coverage

| Rule | Planned checks | Acceptance focus |
|---|---|---|
| BR-01 | B01, B02, B10, B12, B13, W13, W14, I08 | Selected valid-actor role/owner boundaries, not real authentication |
| BR-02 | B03, B04, B05 | Valid boundaries and invalid types |
| BR-03 | B05, B06, B15, W12, I10 | Fresh trusted submission time and isolated clock cases |
| BR-04 | B06, B07, B08, W06, W07, W08, I01 | CONFIRMED-only counts and no confirmed release on withdrawal |
| BR-05 | B09, W03, W04, W16, I02 | Active-state uniqueness and stable IDs |
| BR-06 | B16, W10, W16, I04 | No-op repeats, separate from active deadline rejection |
| BR-07 | B14, B17 | New IDs, history and unchanged failures |
| BR-08 | W01, W02 | Explicit full-only joining |
| BR-09 | W05, W09, W11, W13, W14, I03 | Sequence order, derived contiguous position and workshop isolation |
| BR-10 | W06, W07, W08, W10, I03, I04, I05 | Complete single promotion without partial mutation |
| BR-11 | W08, W09, W12, W16, I10 | Withdrawal allowed after C before S, rejected at S, confirmed roster unchanged |
| BR-12 | W15, W12 | No queue bypass or post-C allocation |
| BR-13 | B16, I01, I02, I03, I04, I05 | Latest state, input snapshots and full result replacement |
| BR-14 | B09, I06, I08, I09; L0 scope and later PR review | Explicit single-session/non-authenticated/non-durable scope |
| BR-15 | B03, B05, VAL-02 | Creation strictly more than 24 hours ahead |
| BR-16 | B06, B15, B16, W08, W12, W13, W14, I10, VAL-01, VAL-02, VAL-03E | Operation-specific three-phase matrix |

## Quality coverage

| Quality | Planned checks | Risks |
|---|---|---|
| QR-01 | B03, B04, B05, B06, B07, B08, B09, B15; W03, W04, W05, W06, W07, W08, W09, W10, W11, W12; I01, I02, I03, I04, I10 | R-01, R-02, R-05, R-07 |
| QR-02 | B16, W10, W16, I04, I05 | R-01, R-02, R-04, R-07 |
| QR-03 | B01, B02, B10, B12, B13, B14, W13, W14, I08 | R-03, R-06, R-07 |
| QR-04 | I06, I07, I09, VAL-01, VAL-02, VAL-03 | R-04, R-08 |

The [risk register](risks.md) is canonical for R-01 through R-08 controls. R-06 also requires actual intake, review and decisions. R-08 needs task feedback, not just tests.

## Validation coverage

| Scenario | Scope | Human judgement |
|---|---|---|
| VAL-01 | FR-02, FR-03, FR-04, FR-05; R-08 | Baseline tasks, cutoffs and prototype limits |
| VAL-02 | FR-06, FR-07; BR-15, BR-16; R-08 | Creation lead, organising usefulness and session model |
| VAL-03A | FR-08, FR-11; R-08 | Unconfirmed state, C and notification expectations |
| VAL-03B | FR-09, FR-10, FR-11; R-08 | State comprehension and next action |
| VAL-03C | FR-10, FR-11; R-08 | Near-C promotion feasibility |
| VAL-03D | FR-04, FR-09, FR-11; R-08 | Delayed discovery and distinct cancellation/withdrawal deadlines |
| VAL-03E | FR-09, FR-11; BR-11, BR-16; R-08 | Post-C withdrawal without promotion and closure at S |

## Evidence and authorship

Requirement -> rule/quality/risk -> scenario -> actual result -> human decision -> release.

For FR-09, trace BR-11/BR-16 -> R-05 -> W08/W12/I10 -> actual outcomes -> CR-01 decision -> V1.1. The [loop recording format](development-workflow.md#record-for-each-loop) binds executor, human assessment, evidence and SHA. Document review does not populate application results.

The [L0 review record](ai-use.md#l0-review-findings) records corrections to this design, including test isolation, derived positions and evidence ownership. These are specification findings, not invented runtime defects. The author's [ACCEPT_LOOP](reviews/L0-human-acceptance.md) accepts this design baseline; all application execution links above remain pending.
