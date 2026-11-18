# Test Plan and Traceability

## L6 integration and verification

L6 HUMAN_REVIEW_PENDING; L7 NOT_STARTED. Accepted L5 is 8a5c9723afe6a81bbafc634acc09b65dac436ee4; deep-review intake is fc964bb7bde9476e98aaabfee85ff8ab15156300. All 308 intake case identities, 116 test ASTs/decorators and seven existing helper definitions remain unchanged. Current: 317 cases/119 test functions; all 51 canonical scenario rows below retain their content. [Current evidence](reviews/L6-human-review.md) | [Human validation](reviews/L6-human-review.md#validation-record).

| Group | Exact function/cases | Independent expectations and mapping |
|---|---|---|
| L6-01 | test_l6_created_workshop_completes_the_v1_baseline_journey (2) | Empty valid State; actual invalid form retains eight values/counters 1/1, correction creates owned workshop-1 and resets only that form. Book -> explicit duplicate-before-capacity precedence -> isolated other-participant FULL -> own cancellation/history -> registration-2 replacement -> actual owner's roster -> exact-C disabled controls -> cleared identity with unchanged final State. FR-01-FR-07; BR-01/02/03/04/05/06/07/13/15/16; QR-01-04; B/I journey portions and R-01/03/04/05/06/07. |
| L6-02 | All 306 L1-L5 cases, unchanged | Unit/invalid/boundary/permission/failure/UI evidence, including F05/F08, spare-capacity duplicate, multiple-attendee cancellation and clicked-target oracles. The capacity-1 journey cannot replace these or prove concurrency. |
| L6-03 | Native browser/deployment, separately labelled | Actual hosted meaningful UI/control flow, package/source/managed-Python proof, Refresh/independence/reload/restart limits and console checks. I06/I08/I09, QR-03/04; R-03/04/07/08. Record real executor and target. |
| L6-04 | Author VAL-01/VAL-02/manual I06/I08/I09 | PENDING real task observations and policy/reset judgement. Record tester label, candidate/target, task, concern, rationale and ACCEPTABLE_WITHIN_SCOPE/CHANGES_REQUIRED/UNRESOLVED. AI success is not human suitability evidence. |
| L6-05 / F08-F09 | test_l6_review_final_candidate_failure_preserves_creation_and_booking_input (4: Create/Book x domain/UI) | Use valid actors/open targets/available capacity, snapshot full input and list identities/counters, then raise only at final DemoState replacement after model construction. Original records/counters remain exact; UI keeps original State/actor, submitted creation values and no false success. FR-03/06; BR-07/13; QR-02; V1.0 creation/booking I05; R-04/06/07. |
| L6-06 / F10 | test_l6_runtime_identity_is_read_only_and_explicit_about_git_metadata (4) | Known distinct source bytes/package values; absent/detached/loose-branch/invalid Git fixtures. Exact expected digest/payload and byte-unchanged files, unknown metadata stays None. Operational deployment evidence, not a new business requirement. |
| L6-07 / F10 | test_l6_runtime_identity_logs_once_without_changing_business_state (1) | Initial log once with exact schema; actor rerun adds no log and leaves the business object/state unchanged. No identity/booking/secret logging. Operational evidence for I06/QR-04 and R-04/07. |
| L6-08 / F10-F11 resolution | One explicitly authorised cloud reboot plus native control walkthrough; AI executor | Match actual logged Git SHA to the branch HEAD at execution, three raw source digests to GitHub/local, Python to 3.12.16 and every installed runtime pin to the 34-row lock. Then run invalid/corrected Create -> Browse -> two-person Book -> own Cancel -> Rebook -> History/owned roster, isolated FULL and spare-capacity duplicate. Technical deployment closure only; H/VAL/release remain pending. |

Two private late-counter-mutation copies each passed all 308 old cases (Create 53.97s, Book 53.58s). With L6-05, each copy has two failures for its domain/UI routes; genuine four focused cases pass. Thus the new assertion probes a previously untested failure boundary. Genuine booking.py already satisfied it and is unchanged. Faults are private experiments, not production defects or product red/green fixes. No old assertion is removed/weakened.

Revised-lock local full execution: 317 passed in 80.97s, no failures/errors/skips, Python 3.12.14/PyArrow 24.0.0; Ruff/format/Bandit/pip check PASS. Strict runtime/development audits cover all 34/71 pins with no known vulnerabilities/omissions. The comparison run in the original 26.0.1 environment passes 317 in 81.34s but is not revised-environment proof. Diagnostic booking coverage remains 99% with the existing demo-fixture guard missing.

PASS: observed deployed source 2cad4b53899f5827c0d51cfb298c49f704d77b6b, [run 44276124671](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44276124671), job 134704585509, Python 3.12.16, 317 passed in 55.48s, no failures/errors/skips; one job/all 18 steps successful. Its downloaded artifact 14415250708 verifies tested SHA/JUnit317, all 308 old case identities, all 34 installed runtime pins, complete strict 34/71-package audits and no known vulnerabilities/omissions. Ruff/format/Bandit/pip check/runtime-only imports pass; diagnostic booking coverage is 99%. This is the executed runtime candidate result; a later documentation-only HEAD receives its own Actions/artifact check before delivery.

VERIFIED - L6-F10/L6-F11 CLOSED_TECHNICAL_FOR_TESTED_TARGET. The author explicitly authorised one controlled reboot of the existing candidate. Actual cloud runtime logs observed at 18 November 2026 17:42:47 UTC+08:00 report Git SHA 2cad4b53899f5827c0d51cfb298c49f704d77b6b, exactly the codex/l6-v1-integration HEAD at execution; Python 3.12.16, Streamlit 1.67.0 and PyArrow 24.0.0. All 34 installed project runtime pins exactly match requirements.txt, with no missing packages or version differences; SHA256 of app.py, booking.py and requirements.txt exactly matches the local/GitHub source. The new 09:42 UTC build installs Arrow 24.0.0 directly and has no new Arrow replacement event. Hosted business workflows were rerun against this attested application. Subsequent evidence-only commits must be identified separately and their unchanged application/lock blobs compared; never relabel the actually logged deployment SHA. Human validation, ACCEPT_LOOP and release remain PENDING.

PASS after the authorised controlled reboot, executed by AI in a fresh connected CUA Chrome session. Baseline 4 workshops/3 confirmations; eligible Xingjian receives FULL on Photography without allocation. Rui fails creation for missing meeting point, all eight submitted values remain exact; Alex has a blank title/no Rui error and switching back restores all eight. Correction creates workshop-5, then resets title/meeting point/notes and capacity to 10. Xingjian books the new capacity-2 workshop as registration-5; repeating with one place still free returns DUPLICATE_ACTIVE. Sam books registration-6. Cancel only Xingjian registration-5: total confirmations 5->4 and the freshly painted roster still contains Sam registration-6. Xingjian rebooks as registration-7: total 5, old registration-5 remains CANCELLED in History, and Rui's final roster contains exactly confirmed 6/Sam and 7/Xingjian. Alex's choices contain only his workshops 4/2. These are AI technical executions, not human validation. Final refresh/session/console observations are recorded in the controlled-restart section.

The independent private boundary audit has 16 passing decisions, separate from pytest counts: Create/Book/active cancellation x C-1/C/C+1/S and four separately owned-CANCELLED repeats. It checks literal outcomes, exact whole result/input, IDs/counters/history; active refusals and no-ops return the original object. Fixed NOW exists only in tests; UI decisions receive fresh server_now. Existing stale creation, test_l4_stale_booking_ui_uses_fresh_time_at_the_operation and test_l5_stale_cancellation_ui_uses_fresh_decision_time remain the V1.0 I10 evidence. Exact-C disabled controls alone are not stale-submit evidence.

Actual isolated 8520 restart: native Sam cancellation produces 4 workshops/2 confirmations; verified process stop/start and reconnect/rerun restores factory 4/3, registration-2 CONFIRMED and no cancellation success. Sam's widget selection survives while view/business state reinitialises. Existing 8518/cloud are preserved. Ordinary Refresh before restart retained 4/2 in initial L6 evidence; independent sessions and actual reload are tested separately. This establishes reset semantics, not durable recovery. Human I06/I08/I09 judgement stays PENDING.

Initial L6 historical verification: 308 local cases in 66.67s and intake-head fc964bb CI run 44244879029/job 134601303777, Python 3.12.16, 308 in 71.14s/all 18 steps PASS. Its artifact 14400843523 was downloaded and verified against fc964bb/JUnit308/digest, but it does not verify the new locks/source. The earlier generated insertion error and narrowed precedence/UI mapping remain explained in the review. Historical sections below retain their dated totals.

## Controlled restart follow-up

The 18 November author instruction permits one existing-candidate reboot. Actual manager logs plus L6_RUNTIME_IDENTITY close the earlier F10/F11 proof gap for observed source 2cad4b53899f5827c0d51cfb298c49f704d77b6b. Independent comparison checks all 34 versions and all three raw source digests, not only Arrow/Streamlit or a branch label. Runtime-only managed extras remain outside project pin/audit scope.

The fresh hosted chain uses a capacity-2 new workshop and two participants. It independently isolates FULL on the seeded Photography workshop, DUPLICATE_ACTIVE while the new workshop still has spare capacity, exactly one cancellation leaving Sam's confirmed row intact, new-ID rebooking and exact own History/organiser roster rows. The first valid registration remains 5 after the isolated FULL and failed creation; IDs 6/7 and workshop-5 support no extra allocation in the exercised path. This native sequence supplements the full State/counter assertions in retained automated tests; the browser cannot directly inspect arbitrary internal State. Exact reset and current CI/artifact evidence are in the L6 review.

No test/code/lock/workflow changes are required. All 317 tests and canonical scenario rows remain unchanged. AI native walkthroughs remain verification; genuine VAL-01/02, manual human I06/I08/I09 and H01-H07 are PENDING.

## Retained technical and acceptance history

L0 revision 3 definitions remain unchanged. The L5 deep-review suite has 306 cases in 115 functions: all 298 pre-review cases and all 112 test function ASTs/decorators are unchanged; eight cases in three appended functions strengthen independent oracles. The original 250 L1-L4 cases remain included. Historical sections retain their original execution counts. [Technical deep-review evidence](reviews/L5-human-review.md#deep-review-verification) | [Subsequent author acceptance and feedback](reviews/L5-human-review.md#current-human-acceptance) | [Historical L4 acceptance](reviews/L4-human-review.md#current-human-acceptance).

On 18 November 2026, the author accepted candidate b597babb5a648d3a576edf5b9c26bb2e7304d45c and declared updated UI/H01-H07 complete. Their feedback specifically recognises why multiple confirmed attendees strengthen the cancellation oracle, why active-cutoff and cancelled-repeat fixtures must be distinct, and why improved assertions matter more than growth from 298 to 306 cases or high coverage. This is actual human feedback, separate from AI-executed tests/browser/fault evidence. The source/tests/scenario definitions are unchanged in this acceptance update; the classroom identity and serial-only limits remain.

[Rules](../requirements.md#business-rules) | [Risks](../requirements.md#risk-controls) | [Traceability](#traceability) | [Loop evidence format](../README.md#record-for-each-loop)

## L5 implemented test mapping

Names below are exact suffixes after test_l5_. Every negative scenario uses valid unrelated preconditions unless explicitly named as a precedence, inconsistent-fixture or injected-boundary check. Expected outcomes/state are requirement-based, not generated from the returned result.

| Group | Cases | Exact suffixes | Requirement/scenario/risk and independent oracle |
|---|---:|---|---|
| L5-01 | 4 | cancel_retains_one_history_row_and_returns_an_independent_complete_state | FR-04/05; BR-04/06/13; QR-01/02; B11; R-01/04. Both owners/capacities 1 and 30: exact whole candidate, one retained CANCELLED row, unchanged ID/created_at/other rows/counters and independent collections; confirmed count decreases by one. |
| L5-02 | 11 | cancel_role_denials_preserve_every_record_and_counter (6); cancel_checks_the_stored_owner_even_for_cancelled_targets (2); equal_display_names_do_not_grant_cancellation_ownership; unknown_registration_is_explicit_and_does_not_change_state; missing_referenced_workshop_does_not_release_a_place | BR-01/06/07/13; QR-02/03; B12/B14 and cancellation I08; R-03/04. Exact role/owner/unknown outcomes, full unchanged input/object/counters. Missing workshop is a labelled internal inconsistent fixture; no deletion feature exists. |
| L5-03 | 9 | effective_cancellation_requires_strictly_before_cutoff (5); cancellation_compares_equivalent_aware_instants (2); active_cancellation_rejects_an_unusable_application_clock (2) | BR-03/16; QR-01/02; B15; R-05/07. Fresh active records at C-1/C/C+1/S/S+1; equivalent UTC/New York instants; unusable clock safely rejects. Otherwise role/owner/record are valid. |
| L5-04 | 7 | owned_cancelled_repeat_is_a_no_op_before_and_after_cutoff_and_start (5); serial_cancel_rebook_and_repeat_preserve_history_and_one_place (2) | FR-04/05; BR-04/06/07/13/16; QR-01/02; B11/B16/B17; R-01/04/07. ALREADY_CANCELLED precedes time for owned no-ops; actual cancel -> same/other actor rebook -> repeat old ID never releases the new seat, with new-ID history retained. Serial, not concurrent. |
| L5-05 | 1 | cancel_construction_exception_preserves_complete_input | BR-13; QR-02; cancellation I05; R-04/07. Inject dataclass replacement failure at the actual cancellation construction; exception propagates and every original row/counter remains. |
| L5-06 | 9 | ui_cancel_updates_history_capacity_and_owned_roster_without_losing_drafts; ui_exposes_only_own_confirmed_cancellation_targets (2); non_participants_have_no_cancellation_menu_or_controls (3); ui_disables_effective_cancellation_at_cutoff_and_after_start (3) | FR-01/04/05/07; BR-01/04/06/13/16; QR-01-04; B11/B12/B15, I06/I08; R-01/03/04/05. Real controls update exact history/counts, released Book/new ID and owned roster; keep actor/current view/forms/unrelated state, hide foreign/cancelled targets and disable closed ones. |
| L5-07 | 2 | stale_cancellation_ui_uses_fresh_decision_time | BR-03/16; QR-01/02; B15 and cancellation I10; R-05/07. Render open, submit with C/C+1 at the actual business call: specific closure, no success and exact original object/state/counters. No deployed user clock editor. |
| L5-08 | 4 | ui_never_adopts_a_non_ok_cancellation_candidate (3); ui_cancellation_exception_keeps_the_original_business_snapshot | BR-13; QR-02; cancellation I05/I08; R-04/07. Internal injection: FORBIDDEN/ALREADY_CANCELLED/unrecognised result paired with different data/counters, or an exception. UI keeps its exact prior snapshot and displays no false success. This is not a claim that normal domain refusals return changed data. |
| L5-09 | 1 | cancel_in_one_session_does_not_change_an_independent_session | QR-04; cancellation I09; R-04. Actual cancellation in one AppTest session leaves another initialised session's records/control/counters unchanged. Browser reload/restart limits remain separately observed/disclosed. |
| L5-10 / deep review | 4 | review_cancel_changes_only_target_among_multiple_confirmations | FR-04/05; BR-01/04/06/13; QR-01/02/03; B11/B12; R-01/03/04/07. Legitimate capacity-two workshop has two owners' confirmations plus cancelled history and another workshop. Cancel either owned ID in either row order: change only that exact row, retain order/other IDs/history/counters, decrement only the target workshop by one and preserve complete input. |
| L5-11 / deep review | 2 | review_final_state_construction_failure_preserves_domain_and_ui_input | BR-13; QR-02; cancellation I05/I08; R-04/07. Fail the final DemoState replacement after constructing the changed Registration, through both actual domain and UI calls. Require exception evidence, exact original State/list identity/records/counters and no UI success/adoption. This is a test-only fault seam, not a deployed failure switch or database rollback claim. |
| L5-12 / deep review | 2 | review_ui_cancels_the_clicked_booking_when_two_are_eligible | FR-04/05; BR-01/04/06/07/13; QR-01-04; B11/B17 and I08; R-01/03/04/07. Sam actually books Navigation first, then owns eligible registration-2 and registration-5. Click each distinct control in separate cases; require only the clicked ID to become CANCELLED, the other to remain current/CONFIRMED, exact History and complete unchanged input/counters/identity. |

Current total: 56 L5 cases (including eight review cases) + 250 L1-L4 cases = 306. The following initial-implementation result is historical: 48 new cases plus 250 retained cases gave 298. Before implementation, 45 new cases failed and three passed (non-participant controls were already absent), with 250 deselected. After implementation, all 48 pass; the complete suite passes 298 in 60.15s locally. No old function/parameter/assertion adaptation is made. Actual CI/browser evidence and pending H01-H07 are in the L5 review.

I05 now covers successful/refused/exceptional V1.0 cancellation; promotion-failure paths remain V1.1 work. I10 now covers Book and confirmed cancellation at a fresh decision clock, while Join/promotion/withdrawal remain future. R-08/VAL suitability is not completed by AI AppTest/Chrome runs. L4-HF-01/02/03 remain historical feedback; they are not personal L5 executions or acceptance.

## Deep-review oracle and rollback evidence

Three private faulty copies each passed the full 298-case pre-review suite: cancelling every confirmed attendee in the target workshop (298 passed in 43.69s), temporarily changing input before final State construction (298 passed in 43.11s), and always cancelling the first owned confirmation regardless of the clicked button (298 passed in 43.60s). These faults were never introduced into the delivered runtime.

The new tests detect the same copies: four failures for the multi-attendee fault; two failures for late input mutation (domain/UI); one failure and one pass for wrong UI target (first target remains a passing control, second target fails). The genuine eight cases pass in 3.52s; the genuine full suite passes 306 in 62.74s with zero failures/skips. All 112 prior test bodies/decorators and 298 JUnit case identities remain unchanged. The runtime was already correct, so no implementation workaround was added.

The earlier construction-failure test stops at Registration replacement. L5-11 additionally reaches final DemoState construction, exposing failure after a temporary input mutation that the earlier injection could not observe. Here rollback means no partial mutation/publication of the original in-memory state; there is no database transaction, durable recovery or simultaneous-concurrency guarantee. B13's participant/organiser restrictions and actual roster ownership remain in the retained L1-L4 tests. B14 is specifically UNKNOWN_WORKSHOP/UNKNOWN_REGISTRATION with valid actors and unchanged state, covered by the retained actual Book/roster/cancellation target checks. B15/B16 deliberately use separate active and already-cancelled fixtures rather than treating a no-op as proof of deadline rejection.

Statement/branch coverage stays 99% diagnostic while these faulty copies previously passed. This is why coverage and pass count alone do not establish the intended property. The author has supplied L5 human loop acceptance; full intended-user validation and R-08 remain pending.

## L4 implemented test mapping

The names below are exact test suffixes after test_l4_. All use actual business entry points or Streamlit AppTest unless a fault-injection boundary is explicitly identified.

| Group | Cases | Exact test suffixes | Requirement/scenario/risk and oracle |
|---|---:|---|---|
| L4-01 | 3 | booking_allocates_one_complete_independent_candidate; rebooking_retains_cancelled_history_and_allows_an_overlapping_workshop | FR-03/05; BR-04/05/07/13/14; QR-01/02; B07/B17; R-01/R-04. Capacity 1/30, complete expected candidate, one allocation, cancelled history retained and overlapping workshops independent. |
| L4-02 | 9 | booking_role_denials_preserve_all_data; unknown_booking_target_is_explicit_without_mutation; booking_rejects_an_unusable_clock_without_allocating | FR-03; BR-01/03/07/13; QR-02/03; Book B14 and permission scope; R-03/R-05. Missing/unknown/forged identities, both organisers, unknown target and unusable clock all preserve complete state/counters. |
| L4-03 | 9 | booking_uses_strict_cutoff_even_with_spare_capacity; booking_compares_actual_instants_across_zones; booking_rejection_precedence_is_time_then_duplicate_then_full | BR-03/16; QR-01; Book B06/B15/B17; R-05/R-07. Otherwise eligible actor with spare capacity at C-1/C/C+1/S/after S; equivalent UTC/New York instants; precedence checked separately, not used to hide isolated causes. |
| L4-04 | 4 | full_booking_does_not_waitlist_or_advance_ids; duplicate_with_spare_capacity_keeps_original_id; serial_last_place_and_repeated_request_use_the_latest_state; registration_construction_failure_preserves_complete_input | BR-04/05/13; QR-01/02; B07-B09; I01/I02 and booking I05; R-01/R-04/R-07. FULL with eligible actor, duplicate with spare capacity, feed successful state into next request, repeated IDs/counts unchanged and injected construction exception. Serial checks are not concurrency tests. |
| L4-05 | 7 | own_records_filter_by_id_and_keep_all_statuses; private_read_denials_return_no_records; empty_personal_history_is_a_successful_empty_read | FR-05; BR-01/05; QR-03; B10; R-03. Both IDs including equal display names, all retained statuses, empty success and no returned records for wrong/missing actors. No arbitrary other-user read endpoint exists. |
| L4-06 | 7 | ui_booking_updates_counts_own_history_and_owned_roster; ui_rejection_keeps_every_record_and_counter; booking_controls_are_participant_only; locked_and_started_booking_controls_are_disabled | FR-03/05/07; BR-01/04/05/13/16; QR-01-04; Book/own-view B06-B10, partial I06/I08/I09; R-01/R-03/R-04/R-07. Real controls create one record, update counts/owned roster, retain draft/identity, show only own IDs and reject full/repeat without mutation. |
| L4-07 | 5 | stale_booking_ui_uses_fresh_time_at_the_operation; started_confirmed_record_is_history_without_status_change; personal_ui_does_not_render_records_on_non_ok_result; booking_isolated_from_another_session_and_failure_ui_preserves_input | BR-03/13/16; QR-02-04; booking portions of I05/I09/I10; R-03-R-05/R-07. Inject decision clock across C, preserve original historical status, reject non-OK even with private rows, independent factory state and injected UI-call exception with no false success/replacement. |
| L4-08 | 2 | creation_restoration_and_reset_do_not_log_duplicate_defaults | FR-06; BR-13/15; QR-02/04; R-04/R-07; L4-F05. Re-enable Streamlit's once-per-process warning as on a fresh server, exercise real form success/reset and invalid-draft restoration, and require no duplicate-default log while preserving values, identity, business records and counters. This test seam is not deployed code. |
| L4-09 | 3 | personal_history_moves_at_start_without_rewriting_records | FR-05; QR-01/04; R-04/R-07/R-08; L4-F06. At S-1/S/S+1, assert the actual table's placement relative to both section headings, its ID/status and unchanged complete state. The old existence-of-History-heading assertion did not prove grouping. |
| L4-10 | 2 | booking_ui_never_adopts_a_rejected_candidate | BR-13; QR-02; booking I05/I08; R-04/R-07; L4-F07. Inject FORBIDDEN/unrecognised results paired with a different candidate; require the UI to retain the exact prior object/records/counters and display no success. This challenges only the explicit-OK adoption boundary, not a claim that ordinary business refusals return changed state. |
| L4-11 / F08 | 10 | f08_failed_drafts_and_errors_are_isolated_by_organiser_id (3); f08_success_clears_only_the_current_organisers_failed_form (2); f08_draft_identity_fields_cannot_assign_workshop_ownership (2); f08_latest_failure_replaces_only_its_own_values_and_errors (1); f08_unsubmitted_edits_are_not_shown_to_a_different_organiser (1); f08_feedback_is_scoped_even_when_failure_outcomes_differ (1) | Explicit F08 UI acceptance; FR-01/06, BR-01/13/15, QR-02/03/04, R-03/04/06/07. Fixed-ID maps, eight values, independent errors/feedback, direct/participant/cleared switches, same-owner restoration, both success directions, latest-only replacement, ignored draft identity metadata and unchanged business records/counters on failure. The differing-outcome case injects a denial to test feedback routing, not a real organiser permission defect. |
| L4-12 / F08 review | 10 | f08_review_restores_invalid_values_without_substitution | FR-06; QR-02/04; R-04/R-07; F05/F08. Clear actual AppTest start/end date/time controls or submit capacity 0; after public or other-organiser navigation require all eight exact failed values and own errors, unchanged other-owner failure, selected actor and complete business object/records/counters. No truthy-default substitution. |
| L4-13 / F08 review | 2 | f08_review_creation_refusal_does_not_adopt_a_different_candidate | FR-06; BR-13; QR-02; creation portion of I05/I08; R-04/R-07. Inject INVALID_INPUT/FORBIDDEN with a distinct empty candidate/counters 900/901; require original object/state/counters, retained submitted values, unchanged Alex failure and no success. This internal adoption-boundary test does not claim ordinary domain refusals mutate state or a valid organiser is genuinely forbidden. |

Total: 44 initial L4 cases + seven pre-F08 deep-review cases + 10 F08 implementation cases + 12 F08 deep-review cases + 177 L1-L3 cases = 250. Fault injection proves the specified wiring/failure boundary, not that an ordinary user can edit the clock or force an internal error. The stale Book test renders with an open display clock, then supplies C at the actual business call. I10's later cancellation/Join/promotion/withdrawal paths remain unimplemented. Browser reload/restart behaviour in I09 remains distinct from a business-operation factory isolation check.

Before the F05 correction, the seven new checks produced two failures (reset/restore warning), five passes and 221 deselected. After correction all seven pass; the full suite passes 228. No previous test body/parameter/oracle changes in this review.

The two retained L3 missing-time tests remain explicit UI-conversion injections. After the F05 widget-default correction, three separate private AppTest probes also cleared the actual start-time, end-time and capacity controls to None: each retained the empty value, showed the corresponding field error, kept four workshops and produced no exception. These probes are additional AI observations, not three extra suite cases or browser/user-validation claims.

Two isolated faults each passed all 221 old cases: grouping history at workshop end, and adopting a candidate after a rejected Book. With the stronger tests, the history fault fails S/S+1 (two failures, one pre-S pass) and the rejected-candidate fault fails both outcomes. Those faults existed only in private test copies. Genuine history/adoption logic was already correct and is unchanged. This is concrete review of oracle limitations, not evidence that all possible faults are detected.

## F08 regression adaptation and evidence

All 10 new F08 cases failed against the shared-draft implementation (228 deselected). After implementation, the 10 new cases and three affected parameter cases passed; the full suite passed 238. Existing parameter sets are unchanged.

- test_failed_creation_survives_leaving_the_form_and_retry_uses_current_owner keeps public/role-switch parameters. The role route now checks Alex's clean form, then returns to Rui's own failed draft through the participant/organiser round trip. The old expectation that Alex inherited Rui's draft directly contradicts F08 and is preserved only in history. Existing ownership, record/counter, retry/reset and unrelated-state assertions remain.
- test_l4_ui_booking_updates_counts_own_history_and_owned_roster replaces its obsolete shared creation_draft marker with a complete organiser-2 creation_forms fixture, verifying Book leaves that UI data unchanged. Its booking/history/roster and business assertions remain.

The other 82 prior test bodies match their pre-F08 ASTs. F05's warning-enabled reset/restore tests remain unchanged and pass. Six new functions exercise actual Streamlit controls; two owner-metadata parameters and the differing-outcome case use explicit internal injections at the stated boundary. UI role hiding is complemented by the retained direct business permission tests. This is selected-identity/session isolation, not authentication or cross-session recovery.

## F08 deep-review oracle evidence

The two new functions are test_l4_f08_review_restores_invalid_values_without_substitution (five invalid controls x two routes = 10 cases) and test_l4_f08_review_creation_refusal_does_not_adopt_a_different_candidate (two outcomes). Expected values/state are fixed from the submitted controls and a saved pre-operation snapshot, rather than generated from the application's result.

Two private faulty copies each passed all 238 old cases: using draft.get(key, default) or default silently discards zero/None on restoration; adopting a returned creation candidate before checking OK replaces state even after refusal. The new tests reject these faults with 10 and two failures respectively. All 12 focused genuine cases pass; the complete genuine suite passes 250 in 50.41s with zero failures/skips. These were oracle weaknesses, not defects found in the delivered app.py/booking.py. All 90 old function ASTs/decorators are unchanged and all 238 old JUnit case identities remain.

Fresh Chrome checks also restore capacity 0 and a date cleared with the widget's native Clear date control after an organiser round trip; no record is created. A text-only automation attempt to empty the date input did not commit an empty widget value. AI corrected that browser interaction and checked the actual empty value before submission; no runtime change was needed. Browser smoke and fault-injection evidence do not replace human acceptance or VAL/R-08 validation.

## L2 implemented test mapping

The accepted L2 baseline contained 87 cases in 30 functions: 42 L1 plus 45 L2. All parameter cases below remain in L4. Public/organiser message expectations now describe working views. Three empty-state L1 UI functions explicitly initialise create_demo_state; the abnormal-permission test preloads its populated fixture before injecting the fault, so demo seeding is not the condition under test. Expected behaviour remains derived from FR-01, BR-01/BR-14, QR-03/QR-04 and the author's menu instruction. PREVIEW_MESSAGES is independent of app.py. Historical L2 results are not relabelled as L3 execution.

| Group | New cases | Exact tests | Requirement/risk and acceptance focus |
|---|---|---|---|
| L2-01 | 8 | test_fixed_identity_resolves_by_id_without_mutation; test_unselected_unknown_and_display_name_inputs_do_not_resolve | B01/B02; FR-01/BR-01; R-03/R-07. Four exact ID/name/role mappings; no identity, unknown IDs and display names do not resolve. |
| L2-02 | 12 | test_role_and_owner_checks_return_explicit_outcomes_without_mutation; test_unknown_or_role_inconsistent_actor_is_invalid; test_equal_display_names_do_not_grant_another_organisers_permission | BR-01, QR-03; R-03/R-06/R-07. Correct role/owner gives OK; wrong role/owner gives FORBIDDEN; forged/unknown actors give INVALID_ACTOR. Compare complete populated state/counters. Partial B10/B12/B13 foundation only. |
| L2-03 | 6 | test_identity_selector_has_only_the_fixed_demo_options; test_fixed_roles_show_only_allowed_menu_and_preview; test_unselected_identity_shows_public_preview_and_only_public_menu | B01/B02, partial I08; R-03/R-08. Fixed labels/roles, exact visible menus, permitted content and public content without an identity, with no warnings/errors. Two duplicate no-identity parameters are consolidated into one stronger case. No authentication/user-validation claim. |
| L2-04 | 1 | test_identity_switch_clear_refresh_and_navigation_preserve_complete_state | B01, QR-04; partial I06/I08; R-04. All four identities, clearing, navigation and refresh preserve complete populated state, object identity and counters. |
| L2-05 | 1 | test_separate_sessions_do_not_share_selected_identity | QR-04; partial I09; R-04. Separate AppTest sessions retain different selections. Browser reload/restart lifecycle remains separately checked. |
| L2-06 | 2 | test_permission_failure_does_not_render_allowed_preview_or_change_state | QR-03/QR-04; partial I08; R-03/R-07. Inject None/unrecognised helper results for valid selected actors. Show an access-unavailable error, hide allowed content and preserve complete populated state/counters. |
| L2-07 | 5 | test_bypassing_hidden_menu_still_rejects_access_without_mutation | BR-01, QR-03/QR-04; partial I08; R-03/R-07. Render the real permitted radio but inject a different returned view. Wrong roles and no identity are denied; an unknown view displays an error. No private content or input mutation. |
| L2-08 | 8 | test_identity_change_resets_only_disallowed_current_view | FR-01, QR-04; partial I06/I08; R-03/R-04. First establish that the starting view and its content rendered with unchanged state. Cross-role/clear resets private views; same-role switches retain them. Workshops remains selected across both role changes. Check resulting content and complete state/counters. |
| L2-09 | 2 | test_stale_or_unknown_saved_view_resets_before_widget_creation | FR-01, QR-03/QR-04; partial I08; R-03/R-07. Seed a forbidden/unknown current_view before the initial render. Safely reset to visible public Workshops content, with no exception or business-state mutation. |

Private controlled copies challenge role-claim validation, owner comparison and missing allowed-view content. Four original UI cases passed the missing-content copy; strengthened assertions fail all four. Two abnormal-result cases failed before the explicit-OK UI guard and pass after it. They are not changes to the delivered application or evidence of a defect that existed there. Helper and preview checks do not complete actual cancellation/roster scenarios. Human review and VAL-01/02/03 remain separate from these automated results.

Those controlled-copy observations are historical deep-review evidence, not fresh executions for the navigation revision. L2-07 fault injection simulates bypass of the menu's return value; it does not create or claim an exposed URL route. Normal stale saved state resets safely, whereas a forced private view is independently rejected. No full business-operation access control is inferred from preview checks.

The historical L2 navigation review added controlled-copy evidence: removing public content only for an unselected identity passed the old 86-case suite but failed three strengthened checks. An always-reset fault previously passed four transition cases whose starting private view had never rendered; strengthened checks detected all six private-start failures. Show-all-menus and bypass-helper faults were also rejected. These were deliberate private faults, not production defects. See the unchanged L2 record for those historical results and limitations.

<a id="l3-implemented-test-mapping"></a>

## L3 retained test mapping (historical development)

The following 90 L3 cases use otherwise-valid fixtures to isolate each rejection, except the explicit role-before-invalid-input precedence parameters and the named multiple-error form case. FR/BR and the author's bounded form request define expected outcomes and state; the application is not its own test oracle.

| Group | Cases | Exact tests | Requirement/risk and acceptance focus |
|---|---|---|---|
| L3-01 | 6 | test_create_assigns_id_owner_and_normalised_fields_without_input_mutation; test_sequential_creation_uses_returned_state_and_preserves_older_snapshots; test_creation_exception_preserves_all_input_records_and_counters | FR-06; BR-02/BR-13/BR-15; QR-02; R-04/R-07. Capacity 1/30 for both organisers, assigned IDs/ownership, optional notes, independent candidate lists, sequential returned state and no partial mutation on injected failure. |
| L3-02 | 8 | test_creation_rejects_invalid_capacity_without_allocating_an_id | B04; BR-02; R-01/R-07. Reject 0, negative, 31, fraction, booleans, text and None through the actual creation operation, with unchanged complete state/counters. |
| L3-03 | 22 | test_creation_requires_strictly_more_than_twenty_four_hours; test_creation_rejects_invalid_fields_and_times_without_mutation; test_creation_compares_elapsed_hours_between_aware_instants | B03/B05; BR-02/BR-03/BR-15; R-05/R-07. >24h, =24h, <24h/past, blank/invalid fields, missing/naive times, end<=start, mixed zones and DST elapsed-time boundaries. |
| L3-04 | 23 | test_creation_enforces_actor_and_role_before_invalid_input; test_owned_workshop_list_enforces_role_and_filters_by_id_without_mutation; test_roster_checks_actual_target_owner_and_returns_no_records_on_denial; test_roster_does_not_trust_a_previous_owner_selection | B13; partial B14; FR-06/FR-07; BR-01; QR-03; R-03. Valid-input role denials plus precedence parameters, both owners, no selected/forged actor, actual stored ownership, unknown target, confirmed-only records and empty data on denial. |
| L3-05 | 2 | test_public_browse_orders_instants_and_counts_only_matching_confirmed_records; test_public_view_shows_full_details_counts_and_closed_policy | FR-02; partial B06; BR-03/BR-04; R-05/R-08. Correct date/time/C/zone/location/preparation, confirmed-only counts, full/locked/historical information and no public roster table. |
| L3-06 | 2 | test_demo_data_has_valid_relative_history_capacity_and_independent_collections; test_app_seeds_once_and_refresh_uses_current_time_without_reseeding | FR-01/FR-02; BR-04/BR-05; QR-04; partial I06/I09; R-01/R-04/R-07/R-08. Unique fixture IDs, valid owner/participant references and roles, active-pair uniqueness, valid relative history/capacity, independent state and fresh display time without reseeding. |
| L3-07 | 6 | test_ui_creates_for_current_identity_then_browse_and_refresh_preserve_it; test_creation_form_checks_fresh_submission_time_and_preserves_rejection_state; test_cleared_creation_date_is_rejected_without_crashing; test_missing_time_at_ui_boundary_is_rejected_without_mutation | FR-06; B05; BR-03/BR-13/BR-15; R-04/R-05/R-07. Current organiser at submission, successful UI adoption, late submission, cleared dates and missing time-component conversion; rejection preserves state/counters. |
| L3-08 | 5 | test_organiser_identity_switch_resets_roster_to_owned_target; test_owned_roster_displays_selected_confirmed_count; test_forced_foreign_roster_selection_is_denied_without_disclosure | FR-07; B13; BR-01/BR-04; QR-03; R-03/R-07/R-08. Owned selector reset, actual private table names and selected counts of one/one/zero across both owners, plus forced foreign target denied without a roster or state change. |
| L3-09 | 11 | test_creation_failure_keeps_all_fields_and_identifies_the_error; test_corrected_creation_adds_one_workshop_and_resets_only_the_form; test_creation_shows_all_field_errors_without_discarding_invalid_values | FR-06; BR-02/BR-03/BR-13/BR-15; QR-02/QR-04; R-04/R-05/R-06/R-07. Eight isolated invalid submissions compare all input values, complete business state/counters, identity and other session data. Both organisers correct only the invalid field, create exactly one valid owned workshop, retain prior records, reset all eight defaults and reject a subsequent empty submit. One case checks all five simultaneous errors and preserves invalid entries. |
| L3-10 | 5 | test_failed_creation_survives_leaving_the_form_and_retry_uses_current_owner; test_retry_replaces_previous_errors_and_allocates_only_after_correction; test_creation_feedback_uses_the_attempt_time_when_the_clock_advances | FR-01/FR-06; BR-01/BR-03/BR-13/BR-15; QR-02/QR-04; R-04/R-05/R-06/R-07. Two navigation/role-switch paths restore all rejected values and use the current owner on correction; success removes the failed snapshot even after leaving/reopening. Two sequential-invalid retries replace old errors without allocation. A clock advanced after the operation must not change the feedback for that attempt. Compare complete input state/counters and exact error sets. |

Retained 87 + new 90 = 177 cases in 58 functions. L2-06/L2-07 also assert absence of a private dataframe and creation control after denial; error wording alone does not establish this property. The two missing-time cases inject None after rendering the real widget: AppTest normalises set_value(None) to the widget's existing default, so these verify the UI conversion boundary rather than claiming a real browser-clearing result. Cleared-date cases use actual AppTest date controls. The creation-clock tests verify the creation boundary/wiring; they do not complete I10's later Book/cancellation/Join/promotion paths.

L3-09's literal expectations are independent of the validator. Test-only date snapshots normalise AppTest's pending single-date tuple to the same date/None representation returned after a run; they do not change the selected value. A real browser separately checks retained edited dates/times, invalid capacity entries and reset behaviour, because AppTest alone does not fully exercise frontend clear_on_submit semantics.

The form deep review reproduced loss of rejected values with stale feedback after navigation: the two new lifecycle cases failed before the fix; three new retry/clock cases already passed the correct source. Private copies that merged obsolete errors or re-read time for feedback each passed all 172 old cases. The new tests reject those same copies: two retry failures and one clock-feedback failure. These are test-gap findings, not claims that delivery contained either injected fault. Exact-message checks exclude unrelated errors; browser checks separately confirm error placement beside the field. A private measurement verifies that successful creation reduces shared field checks from two to one while retaining one model construction and unchanged input.

Private L3 controlled faults check oracle strength: allowing exactly 24h fails the strict-boundary test; omitting stored roster ownership fails four checks including the forced-target UI path; removing date/time conversion guards fails four checks. The genuine source passes. Exact executions, limitations, browser smoke and human fields are in the L3 record. Full product validation remains pending.

The deep review challenged two further private copies. Rendering a private table after access denial and duplicating a cancelled fixture's registration ID each passed the old 158-case suite. Stronger assertions now reject those same copies: six denial cases fail for the table fault; the fixture-integrity case fails for the duplicate ID. The actual application did not contain either fault. Three new selected-count cases failed before the count caption was added and pass afterwards. These checks support observable outcomes and test-oracle review; they do not replace human acceptance or prove all possible disclosure and data faults absent.

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

These mappings retain accepted FR, BR, QR, risk and scenario identifiers. Executed V1.0 subsets and pending V1.1/manual/validation portions are distinguished in the current L6 mapping above. The retained L2 mapping records identity/permission evidence; the [L1 review](reviews/L1-human-review.md#foundation-test-mapping) preserves earlier foundation evidence.

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

The [L0 review record](ai-use.md#l0-review-findings) records corrections to this design, including test isolation, derived positions and evidence ownership. These are specification findings, not invented runtime defects. The author's [ACCEPT_LOOP](reviews/L0-human-acceptance.md) accepts the design baseline; it does not itself supply later application execution or validation. Actual dated V1.0 executions appear in the L1-L6 records, while V1.1/human validation remains pending.
