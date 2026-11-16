# Risk Register

L0 revision 3. Risk owner: project author, name pending. Controls: PLANNED. R-08 suitability: VALIDATION_PENDING. Initial ratings are qualitative planning judgements for human review, not measured probabilities.

[Rules](business-rules.md) | [Tests](test-plan.md) | [Traceability](traceability.md) | [Sources](sources.md)

## Controls and planned acceptance

| ID / version | Risk and control | Acceptance evidence |
|---|---|---|
| **R-01** / Both | Overbooking, duplicate active records or stale replacement. Use current same-session state, validate capacity/uniqueness and serially adopt returned results. Verify last-place/repeated actions without claiming shared-concurrency correctness. | B04, B07-B09; W03/W04; I01/I02 |
| **R-02** / V1.1 | Unfair FIFO or incorrect transitions. Use stable sequences, earliest current WAITLISTED, tail rejoining and a complete cancellation/promotion result. Exclude withdrawn entries; never promote twice for one cancellation. | W05-W11/W15/W16; I03-I05 |
| **R-03** / Both | Missing selected-role/owner checks or overstated security. Enforce rules in booking.py, filter by selected ID and disclose freely switchable fictional identities. Use no real private data. These controls do not prevent identity impersonation. | B01/B02/B10/B12-B14; W13/W14; I08; scope acceptance |
| **R-04** / Both | Accidental rerun reset, aliased lists or misunderstood memory loss. Initialise once per session, preserve state on actor change and use independent state factories. Test actual lifecycle; new-session/restart reset remains a disclosed limitation. | I05-I09; VAL-01/VAL-02 |
| **R-05** / Both | Wrong timing, particularly blocking withdrawal at C or allowing it after S. Use fresh trusted time and operation-specific deadlines. Isolate C/S boundaries with fresh active records and test late form submission. | B03/B05/B06/B15/B16; W08/W12/W16; I10 |
| **R-06** / AI-assisted work | Unchecked AI assumptions, changed policy or unrelated complexity. Bound intent/files, preserve contracts, inspect oracles/dependencies and record human corrections and decisions. | AI-use, loop review, CR-01, PR and findings records |
| **R-07** / Both | Weak tests, false-positive denials or baseline regressions. Derive oracles from requirements; isolate each rejection cause, retain baseline tests and inspect collected/skipped/mocked scope. Protect full rejection, empty-queue cancellation and no-op safety. | B01-B17, W01-W16 and applicable I checks; especially B08/B11/B12/B15/B16, W06/W07/W10/W12 and I05 |
| **R-08** / Both | Misunderstood states, delayed confirmation awareness, cutoff restrictions or temporary data. Explain S/C, no notification, permitted waiting withdrawal, closed confirmed cancellation and session limits; validate actual tasks and feasibility. | VAL-01/VAL-02/VAL-03A-VAL-03E |

Acceptance requires the specified outcomes and state assertions in the linked scenarios, not merely a green report or a helper function's presence.

## Initial likelihood and impact

M means Medium; H means High. Unknown means evidence is still required.

| Risk | Likelihood / impact | Rationale |
|---|---|---|
| R-01 | M / H | Capacity is central and successive actions can use stale state. |
| R-02 | M / H | One state change can allocate a place to another participant. |
| R-03 | M / M for rule defects | Fictional-role checks matter; free identity selection is an intentional limitation, not solved authentication. |
| R-04 | M / H for accidental loss | Unexpected same-session loss breaks the demonstration; new-session reset is expected scope. |
| R-05 | M / H | C and S deliberately permit different actions. |
| R-06 | M / H | Generated work can retain superseded assumptions or change tests to fit code. |
| R-07 | M / H | An error can pass through weak assertions or a denial caused by the wrong precondition. |
| R-08 | Unknown / H | Preparation, arrival and restriction acceptability have not been observed. |

## Monitoring and human decisions

After each control is implemented, record owner, environment/SHA, expected and observed results, evidence, residual risk and decision using the [loop recording format](development-workflow.md#record-for-each-loop).

Progress from PLANNED to IMPLEMENTED_NOT_VERIFIED and then VERIFIED_FOR_STATED_SCOPE. Record residual acceptance separately; verification never means all possible failures are eliminated.

Capacity errors, selected-role/owner bypass, wrong C/S behaviour, partial mutation and material FIFO defects block the relevant release. Freely selectable actors and temporary unshared state are scope limitations only after clear disclosure and genuine author acceptance. They are not technically eliminated risks.

Use VAL-01/02 for baseline suitability and VAL-03 before V1.1 merge. Unresolved critical user needs prevent the relevant release. Return policy uncertainty to the human owner rather than adding authentication, notifications or overrides without an agreed change.

## Change-review depth

The planned CR-01 changes core user-visible business state. Start with Medium review depth and justify the actual classification at intake. Reclassify/escalate if the patch changes role boundaries, validation contracts, dependencies or broader data handling. The absence of a database removes migration concerns, not correctness responsibilities.

Track open blockers, missing evidence, test failures/skips, findings dispositions and outstanding human decisions. Do not substitute prompt counts or generated lines of code for quality measures.
