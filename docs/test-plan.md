# Test Plan and Traceability

L0 revision 3 scenario definitions are unchanged. The 42 L1 cases are retained; two UI functions select a role-appropriate identity before private navigation, retaining their original assertions. L2 adds identity/menu/permission verification for B01/B02 and foundation support for later scenarios; remaining full B/W/I operations and validation are PLANNED / NOT_EXECUTED. The [L1 record](reviews/L1-human-review.md#foundation-test-mapping) is historical; the [L2 record](reviews/L2-human-review.md#verification-results) reports current observations. IDs represent scenarios and parameter groups, not passing-test counts.

[Rules](../requirements.md#business-rules) | [Risks](../requirements.md#risk-controls) | [Traceability](#traceability) | [Loop evidence format](../README.md#record-for-each-loop)

## L2 implemented test mapping

Expected results come from FR-01, BR-01/BR-14, QR-03/QR-04 and the author's fixed-name/role and menu instructions. The complete collected suite has 86 cases in 30 functions: 42 L1 cases plus 44 L2 cases. Actual execution and the renewed human gate are in the L2 record.

| Group | New cases | Exact tests | Requirement/risk and acceptance focus |
|---|---|---|---|
| L2-01 | 8 | test_fixed_identity_resolves_by_id_without_mutation; test_unselected_unknown_and_display_name_inputs_do_not_resolve | B01/B02; FR-01/BR-01; R-03/R-07. Four exact ID/name/role mappings; no identity, unknown IDs and display names do not resolve. |
| L2-02 | 12 | test_role_and_owner_checks_return_explicit_outcomes_without_mutation; test_unknown_or_role_inconsistent_actor_is_invalid; test_equal_display_names_do_not_grant_another_organisers_permission | BR-01, QR-03; R-03/R-06/R-07. Correct role/owner gives OK; wrong role/owner gives FORBIDDEN; forged/unknown actors give INVALID_ACTOR. Compare complete populated state/counters. Partial B10/B12/B13 foundation only. |
| L2-03 | 7 | test_identity_selector_has_only_the_fixed_demo_options; test_fixed_roles_show_only_allowed_menu_and_preview; test_unselected_identity_hides_restricted_menu | B01/B02, partial I08; R-03/R-08. Fixed labels/roles, exact visible menus, permitted content without errors and no private menu without identity. Rejection is separately checked below; no authentication/user-validation claim. |
| L2-04 | 1 | test_identity_switch_clear_refresh_and_navigation_preserve_complete_state | B01, QR-04; partial I06/I08; R-04. All four identities, clearing, navigation and refresh preserve complete populated state, object identity and counters. |
| L2-05 | 1 | test_separate_sessions_do_not_share_selected_identity | QR-04; partial I09; R-04. Separate AppTest sessions retain different selections. Browser reload/restart lifecycle remains separately checked. |
| L2-06 | 2 | test_permission_failure_does_not_render_allowed_preview_or_change_state | QR-03/QR-04; partial I08; R-03/R-07. Inject None/unrecognised helper results for valid selected actors. Show an access-unavailable error, hide allowed content and preserve complete populated state/counters. |
| L2-07 | 5 | test_bypassing_hidden_menu_still_rejects_access_without_mutation | BR-01, QR-03/QR-04; partial I08; R-03/R-07. Render the real permitted radio but inject a different returned view. Wrong roles and no identity are denied; an unknown view displays an error. No private content or input mutation. |
| L2-08 | 6 | test_identity_change_resets_only_disallowed_current_view | FR-01, QR-04; partial I06/I08; R-03/R-04. Cross-role and clearing reset private views to Workshops; both same-role switches retain permitted views. Preserve complete state/counters. |
| L2-09 | 2 | test_stale_or_unknown_saved_view_resets_before_widget_creation | FR-01, QR-03/QR-04; partial I08; R-03/R-07. Seed a forbidden/unknown current_view before the initial render. Safely reset to Workshops, with no exception or business-state mutation. |

Private controlled copies challenge role-claim validation, owner comparison and missing allowed-view content. Four original UI cases passed the missing-content copy; strengthened assertions fail all four. Two abnormal-result cases failed before the explicit-OK UI guard and pass after it. They are not changes to the delivered application or evidence of a defect that existed there. Helper and preview checks do not complete actual cancellation/roster scenarios. Human review and VAL-01/02/03 remain separate from these automated results.

Those controlled-copy observations are historical deep-review evidence, not fresh executions for the navigation revision. L2-07 fault injection simulates bypass of the menu's return value; it does not create or claim an exposed URL route. Normal stale saved state resets safely, whereas a forced private view is independently rejected. No full business-operation access control is inferred from preview checks.

## Test design and independent oracles

Rule tests call actual booking.py functions independently of Streamlit UI execution. Separate Streamlit AppTest smoke/state tests exercise the shell. Neither replaces later personal browser checks or user validation. Serially feed each successful returned state into the next action when operations exist. Independent copies are not a shared-concurrency test.

For every negative or boundary parameter:

1. Use a fresh fixture with valid actor, role, target, ownership and time unless that is the condition under test.
2. Isolate the intended rejection. B12 must use a valid non-owner, active target and open workshop; B09 must leave spare capacity when proving duplication; B15 must leave capacity and avoid duplicates.
3. Use a fresh active WAITLISTED record at each W12/I10 time. A previously withdrawn CANCELLED record proves no-op safety, not start-time rejection.
4. Derive expected outcome and state from FR/BR before comparing implementation. Assert reason plus records, IDs, counters, counts and absence of side effects.
5. For failures, compare the entire original state with its snapshot. For successful mutations also confirm the original snapshot was not changed.
6. Record missing cases, skips and mock limitations. An injected helper failure proves only the selected failure path; it does not prove all exceptional behaviour.

Use a controlled aware clock; do not sleep through actual deadlines. app.py must obtain trusted time when processing submission rather than reusing render-time state. Test UI wiring separately.

Lecture examples of automatic full-session waitlisting or overlap rejection are not this project's oracle. Apply the declared FULL/separate-Join contract and per-workshop scope instead.

## Baseline scenarios

Implement B01-B17 in V1.0 and retain them in V1.1. Preserve no-waiter fixture preconditions rather than changing old assertions to waitlist outcomes.

| ID | Scenario and expected result |
|---|---|
| **B01** | Valid fictional selection resolves fixed ID/role. Switching/clearing selection preserves business state in the same session. |
| **B02** | Unknown ID or inconsistent role produces INVALID_ACTOR without restricted action or state change; this is not credential authentication. |
| **B03** | Valid capacity 1/30 and lead 24h+1 second create correct ID/owner. Use separate valid fixtures for each boundary. |
| **B04** | Reject zero, negative, 31, fraction, True and missing capacity as INVALID_INPUT; no record/counter advance. |
| **B05** | Independently reject blank fields, end<=S, past start and S-t<=24h, including exactly 24h. Input remains unchanged. |
| **B06** | Display correct S/C, zone, location and CONFIRMED-only counts. Spare capacity does not permit booking at/after C. |
| **B07** | Normal and last-place booking before C yield one CONFIRMED ID and correct counts. Original input remains unchanged. |
| **B08** | New eligible actor books an open but full workshop: FULL, no new record and no automatic waiting in either release. |
| **B09** | With spare capacity, an active same-user/workshop duplicate yields DUPLICATE_ACTIVE and preserves the original ID. A distinct workshop remains independent without overlap rejection. |
| **B10** | Own-record functions filter by selected ID. Any targeted non-owner read is denied; changing the demo selector is not prevented or called authentication. |
| **B11** | Own confirmed cancellation before C without waiters retains CANCELLED history and releases exactly one place. |
| **B12** | Valid selected A cancels B's active ID in an otherwise valid open scenario: FORBIDDEN; original records/counts unchanged. |
| **B13** | Valid participants cannot create/read organiser rosters; a valid non-owner organiser cannot read another roster. Isolate these role/owner failures from timing errors. |
| **B14** | Well-formed unknown workshop/registration targets return the corresponding UNKNOWN outcome without mutation or false success. |
| **B15** | Use fresh otherwise-valid fixtures at C-1, C and C+1 second. Book/confirmed cancellation work before C and return REGISTRATION_CLOSED at/after C, including stale forms. |
| **B16** | Repeat owned CANCELLED IDs before/after C and S: ALREADY_CANCELLED, no additional release, ID advance or promotion. |
| **B17** | Before C, rebooking uses a new ID with old history retained; after C reject with no record/counter changes. |

## Waitlist scenarios

W01-W16 apply only to V1.1. Allocation uses C; withdrawal uses S.

| ID | Scenario and expected result |
|---|---|
| **W01** | Explicit pre-C full joining creates one WAITLISTED ID/sequence without consuming confirmed capacity. |
| **W02** | An otherwise-valid Join with spare capacity returns USE_BOOKING without registration. |
| **W03** | A confirmed actor joining the same queue returns DUPLICATE_ACTIVE, with no second active record. |
| **W04** | Repeated Join by a waiter returns DUPLICATE_ACTIVE; preserve original ID/sequence and the next-sequence counter. |
| **W05** | Equal displayed timestamps still produce distinct sequence FIFO, independent of names/browser times. |
| **W06** | Participant A is confirmed; B then D are waiting. Cancel A before the cutoff: only B confirms, D becomes position 1 and confirmed count is unchanged. |
| **W07** | Pre-C confirmed cancellation without waiters releases one place and promotes nobody. |
| **W08** | In independent pre-C and final-24h cases, head/tail withdrawal preserves every confirmed ID/state/count and others' relative order. A later pre-C cancellation excludes the withdrawn head; a post-C withdrawal promotes nobody. |
| **W09** | Pre-C withdrawal/rejoin creates a new ID/tail sequence and retains history. During C<=t<S allow withdrawal but reject rejoining. |
| **W10** | Repeat cancellation that already promoted a waiter: ALREADY_CANCELLED with no second promotion. |
| **W11** | Two workshop queues remain isolated when one is changed. |
| **W12** | Fresh active fixtures at C-1/C/C+1 and S-1/S/S+1. Reject allocation/confirmed cancellation/Join at C, allow owner waiting withdrawal until S, then reject active withdrawal as WORKSHOP_STARTED. No-op cases are separate. |
| **W13** | In-app refresh shows own outcome and contiguous positions, including non-contiguous active sequences such as 3/8. Withdrawal during final 24h updates remaining positions; joining/promotion stay closed. After S show history. |
| **W14** | Only the selected owner organiser reads ordered rosters. After C the queue may shrink but confirmed records remain identical. |
| **W15** | An intentionally inconsistent open spare-place/queue fixture returns INTEGRITY_ERROR without direct bypass or state changes. |
| **W16** | Repeat an owned cancelled waiting record, including after S: ALREADY_CANCELLED without changes. Equal display names with distinct IDs remain independent. |

## In-memory integration and system scenarios

| ID | Version and method | Planned acceptance |
|---|---|---|
| **I01** | Both; automated serial actions | Feed A's successful last-place result into B. Exactly one confirms and B is FULL; do not call independent state copies a concurrent race. |
| **I02** | Both; automated serial actions | Repeated actor requests produce one active registration/counter allocation. |
| **I03** | V1.1; automated serial actions | Check Join-then-Cancel and Cancel-then-Join ordering. Existing waiters have priority and new arrivals cannot bypass. |
| **I04** | V1.1; automated repeats | One confirmed ID cancelled repeatedly causes one effective cancellation/promotion, including a later post-C no-op. |
| **I05** | Both; automated snapshot/failure | Success returns a complete candidate without changing input. Rejection or injected promotion-helper failure leaves all original records and counters unchanged; UI retains its prior state on failure. |
| **I06** | Both; manual UI plus rule checks | Ordinary reruns, in-app Refresh and fictional actor changes preserve one session; do not reseed on selector changes. Distinguish browser reload. |
| **I07** | V1.1; automated baseline fixtures | Representative V1.0 CONFIRMED/CANCELLED fixtures retain IDs, owners, history and time contracts under V1.1 defaults. This is not live migration. |
| **I08** | Both; separate automated/manual parts | Check selected-role/owner wiring, safe failure and no false success. UI clearly labels demo identities, temporary/unshared data and in-app versus browser refresh. |
| **I09** | Both; automated factory isolation plus manual lifecycle | Independent initialisations share no mutable collections; changing A through operations does not affect B. Ordinary reruns preserve data while new sessions/browser reload/restart follow reset limits. No backup/recovery claim. |
| **I10** | Both; automated clock scenarios plus manual UI wiring | A form rendered before C submits at/after C with fresh trusted time: reject Book/confirmed cancellation/Join/promotion. In a fresh active waiting fixture, withdrawal at C<=t<S succeeds. A separate fresh pre-S form submitted at/after S returns WORKSHOP_STARTED. |

I09/I10 were re-scoped during unaccepted L0 revision 2. There are no previous executed application results to relabel. Once a working baseline exists, preserve its genuine history.

## Verification and validation

Verification compares a work product or behaviour with its specification. Examples are this requirements review and later boundary/state tests.

Validation examines whether the intended users can complete useful tasks and accept the declared policy/limits. Passing pytest cannot close R-08.

| ID | User task and evidence |
|---|---|
| **VAL-01** | Find a suitable workshop, identify S/C and complete pre-C booking/cancellation. Explain post-C restrictions and the single-session, non-authenticated demonstration. |
| **VAL-02** | Create a >24h workshop and inspect owned rosters. Assess whether the 24h freeze supports preparation and whether the prototype demonstrates the organising task coherently. |
| **VAL-03** | Complete waiting, withdrawal and promotion; explain C/S differences and assess preparation, awareness and participation feasibility. |

| Scenario | Task and acceptance question |
|---|---|
| **VAL-03A** | After Join, explain that WAITLISTED is unconfirmed and identify C, refresh requirements and lack of notifications. |
| **VAL-03B** | Locate confirmation after ordinary pre-C promotion and explain the next action. |
| **VAL-03C** | S=10 December 09:00, C=9 December 09:00, promotion=9 December 08:59. Separately assess comprehension, preparation/arrival feasibility and latest useful confirmation with reasons. |
| **VAL-03D** | In one preserved demo session simulate pre-C promotion discovered after C. Explain closed confirmed cancellation versus permitted waiting withdrawal. A recreated session follows reset limits, not recovered prior data. |
| **VAL-03E** | Withdraw during C<=t<S without changing confirmed records or promoting another waiter; explain closure at S and assess whether this is understandable/useful. |

### Validation recording and decisions

Record actual tester/role label, version, task, intended need, observations, feedback, issue, owner and decision. Distinguish external testers from author role-play; do not invent participants or claim real multi-user operation.

Task comprehension is acceptable when the tester correctly identifies state, applicable deadline and next permitted action without unresolved critical confusion. Product suitability is a separate human judgement supported by feedback and preparation/arrival constraints.

Use ACCEPTABLE_WITHIN_SCOPE, CHANGES_REQUIRED or UNRESOLVED, with rationale. A critical unmet need prevents the relevant release. R-08 remains pending until these activities actually occur.

The old same-day 08:59 promotion for a 09:00 start is prohibited under W12/I10. Promotion shortly before C is the valid scenario. Allocation time does not guarantee awareness time.

## Traceability

These mappings retain the accepted FR, BR, QR, risk and scenario identifiers. Full business-operation B/W/I results remain pending. The L2 mapping above records the current identity/permission subset; the [L1 review](reviews/L1-human-review.md#foundation-test-mapping) preserves earlier foundation evidence.

### Functional coverage

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

### Rule coverage

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

### Quality coverage

| Quality | Planned checks | Risks |
|---|---|---|
| QR-01 | B03, B04, B05, B06, B07, B08, B09, B15; W03, W04, W05, W06, W07, W08, W09, W10, W11, W12; I01, I02, I03, I04, I10 | R-01, R-02, R-05, R-07 |
| QR-02 | B16, W10, W16, I04, I05 | R-01, R-02, R-04, R-07 |
| QR-03 | B01, B02, B10, B12, B13, B14, W13, W14, I08 | R-03, R-06, R-07 |
| QR-04 | I06, I07, I09, VAL-01, VAL-02, VAL-03 | R-04, R-08 |

The [risk register](../requirements.md#risk-controls) is canonical for R-01 through R-08 controls. R-06 also requires actual intake, review and decisions. R-08 needs task feedback, not just tests.

### Validation coverage

| Scenario | Scope | Human judgement |
|---|---|---|
| VAL-01 | FR-02, FR-03, FR-04, FR-05; R-08 | Baseline tasks, cutoffs and prototype limits |
| VAL-02 | FR-06, FR-07; BR-15, BR-16; R-08 | Creation lead, organising usefulness and session model |
| VAL-03A | FR-08, FR-11; R-08 | Unconfirmed state, C and notification expectations |
| VAL-03B | FR-09, FR-10, FR-11; R-08 | State comprehension and next action |
| VAL-03C | FR-10, FR-11; R-08 | Near-C promotion feasibility |
| VAL-03D | FR-04, FR-09, FR-11; R-08 | Delayed discovery and distinct cancellation/withdrawal deadlines |
| VAL-03E | FR-09, FR-11; BR-11, BR-16; R-08 | Post-C withdrawal without promotion and closure at S |

### Evidence and authorship

Requirement -> rule/quality/risk -> scenario -> actual result -> human decision -> release.

For FR-09, trace BR-11/BR-16 -> R-05 -> W08/W12/I10 -> actual outcomes -> CR-01 decision -> V1.1. The [loop recording format](../README.md#record-for-each-loop) binds executor, human assessment, evidence and SHA. Document review does not populate application results.

The [L0 review record](ai-use.md#l0-review-findings) records corrections to this design, including test isolation, derived positions and evidence ownership. These are specification findings, not invented runtime defects. The author's [ACCEPT_LOOP](reviews/L0-human-acceptance.md) accepts this design baseline; all application execution links above remain pending.
