# L3 Work and Human Review

**Workshop creation, browsing, owned confirmed rosters and valid demo data. Human decision: HUMAN_REVIEW_PENDING. L4: NOT_STARTED.**

## Intake and scope

The author accepted L2, then explicitly requested L3 in L3_develop with creation/browsing, owned lists/rosters, valid demo data, >24h creation, capacity 1-30 and permission checks. Preserve the three-file architecture and single-job Actions, deliver English files/ZIP, retain a manual preview and stop for ACCEPT_LOOP. Base: accepted L2 commit e52dd74816fd89a0fad22e104caa68900d032da0. Executor/tool: Codex. The earlier L3 hold is superseded only for this requested loop.

On 17 November 2026 (Asia/Singapore), the author requested this deep review of L3 candidate 367765d8e822e5e5a365810643e61a8c0f9980e4, with corrections, English files/ZIP and the live service retained. This instruction supplies review scope, not ACCEPT_LOOP. Changed files: app.py, booking.py, test_booking.py, README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md and this record.

The subsequent bounded creation-form request starts from L3 candidate 9d3d2bb8fc855ed0ef0d5a68d87bb4cfcaf61eab. It requires retained failed input, field-specific feedback, correction/resubmission, success-only form reset, unchanged rules/identity/business data and a pending human gate. The same nine files are changed; no delivery file, dependency or workflow is added. All 161 prior cases remain, with only five UI-summary expectations adapted to the new wording; 11 form cases are added. This is still L3 baseline development, not CR-01 or a release approval.

| Surface | Implemented work |
|---|---|
| app.py | Retain browsing, role menus, access rejection and owned rosters. Failed creation keeps all submitted values and shows inline errors; only success resets eight creation-widget keys before the next render. Use fresh trusted submission time, adopt only OK, preserve identity/business state and retain existing new-roster selection. |
| booking.py | Retain model/business/identity contracts and the outcome/state interface. Extract shared field checks for models and workshop_creation_errors; preserve model exception text. Creation and UI feedback use the same rules/decision time. No Streamlit import, database or service framework. |
| test_booking.py | Retain all 87 L2 and 74 preceding L3 cases. Add 11 form cases; 172 total in 55 functions. Five UI rejection cases expect the new human-readable summary while their state/clock assertions remain. |
| Documents/archive | Update the primary README/requirements/test-plan/Demo/AI records and add this one L3 record. Delivery has 20 files/nine Markdown documents. ZIP has the same root structure including .github, excluding caches, environments, generated reports and private tools. |
| Preserved | Accepted L0/L1/L2 folders and historical review files, original tracked working copy, FR/BR/QR/risk definitions, four dependency input/lock files, pyproject.toml and single-job workflow. |
| Deferred | Booking/history actions, cancellation/repeats, waitlist, full lifecycle/validation, deployment and releases. No PR, merge, release or L4 work. |

## Course and baseline alignment

The preceding deep review re-extracted the original assessment and three supplied transcript PDFs and inspected Week3-9 lecture material from Week1-9.zip; source hashes matched the earlier review. The rubric's page 10 was also rendered and inspected. Sources S01-S08/S13-S14 in [Demo reuse](../demo-reuse.md#references) identify the material; S21 records this bounded UI request. Automatic transcripts are supplied accounts, not audio independently checked by AI; the 09:40/10:45 texts are identical.

| Standard | Current evidence and limit |
|---|---|
| Accepted L0/L1/L2 | Keep normative FR/BR/QR/risk/scenario rows, fixed IDs/roles, role menus, reset rules, model contracts and accepted decisions. L3 implements the next agreed slice; local accepted folders, original tracked working copy and historical review files remain unchanged. |
| Requirements/quality planning, HD 15% | Explicit implemented/deferred scope, strict >24h creation and capacity 1-30; FR/BR/QR/risk-to-test mapping. Controls are verified only for executed L3 behaviour, not all future scenarios. |
| Functional application/deployment, HD 15% | Working creation, browsing and owned confirmed rosters in the retained local preview. Booking/cancellation and final browser-accessible release deployment remain later deliverables; localhost is not submitted deployment evidence. |
| V&V/automated testing, HD 20% | Requirement-derived outcomes, boundaries, invalid input, ownership, full-state comparisons and test-oracle fault challenges. User suitability VAL-01/02/03 and R-08 remain pending; automated UI checks are verification, not completed validation. No test-count/coverage grade threshold is invented. |
| Change/regression/release, HD 20% | Retain 87 L2 cases and focused L3 history/findings. L3 remains baseline construction. Working V1.0 must precede CR-01, impact analysis, separate change branch, new/regression tests, PR/review decision, approved merge and V1.1. None is represented as complete by this review. |
| GitHub/CI, HD 15% | Root-layout review branch, one automatic quality-checks job, locks, static/security/dependency checks, JUnit/coverage and recorded code identity. Final Issue/PR/release audit trail remains required later. |
| Authorship/defence, HD 15% | Exact AI tasks, assumptions, findings/corrections and actual executors are disclosed. The author must explain the code, assess evidence/risk and supply personal observations and decisions; presentation/defence remains future work. |
| Lecture method | S02 permits adapting the three-file teaching Demo to a different realistic domain. S05-S08 require bounded intent, preserved behaviour, independent oracles, risk-based review and human ownership. No new runtime module/framework is introduced. |

Assessment p.4 permits the student's own justified review decision unless the teaching team requires an external reviewer. Lecture security/senior-review examples call for stronger review of sensitive changes; they do not supply an actual specialist approval here. The author must record routing/competence and seek suitable advice where needed. This is stage alignment, not a claim that L3 already meets every final HD criterion or earns a grade.

## Contracts and assumptions

- create_workshop receives current session state, a selected actor, intended workshop fields and trusted current time. Only a canonical organiser may create. IDs/owner come from the application. Normalise text before constructing/validating one Workshop. Validate required text, aware times/end>S, capacity integer 1-30 and S-t>24 elapsed hours. Exactly 24 hours or less returns INVALID_INPUT without record/counter changes.
- Success returns (OK, complete_new_state); reject returns an outcome with unchanged input. The new state's three mutable lists are independent while frozen rows may be reused. Unexpected construction exceptions propagate without changing the input; this is not a database rollback/recovery guarantee. The UI replaces state only after OK.
- server_now is the application UTC clock, called again at submission. Tests replace it; no current-time control is exposed to users. Intended form times use Asia/Singapore. Workshop/end/cutoff display includes seconds.
- Roster access looks up the actual workshop and passes its stored owner ID to check_permission. Wrong-role/non-owner results return no records; a valid organiser's missing target returns UNKNOWN_WORKSHOP. Only after OK does the UI show the selected confirmed count/table. Confirmed rosters and public counts exclude CANCELLED history.
- Demo identity selection remains freely switchable and is not authentication. Independent browser sessions do not share data. The current state is authoritative only within its session.
- create_demo_state remains the empty factory. create_demo_data reconstructs four valid creations seven days earlier and pre-cutoff registrations. Two examples are at least 48 hours ahead, one is within the final 24 hours, and one is historical; a capacity-one workshop is full. The UI seeds once, never on refresh/identity change. These are fixtures, not implemented booking/cancellation actions.
- Select the intended organiser before filling the form. Unsubmitted drafts are not promised across unrelated reruns/navigation. Submitted business records remain preserved. Editing workshop details/capacity and ownership overrides remain excluded.
- On a rejected submit, retain all eight raw form values, including whitespace, missing dates and out-of-range integer capacity; place red error messages beside affected controls. The UI asks booking.py for feedback using the attempted operation's decision time. It contains no separate capacity, duration or 24-hour test. On success reset only title, start/end dates/times, meeting point, capacity and notes: empty text, local date+3 days, 09:00/12:00 and 10 places. Clear old feedback and display the success message. Never call Session State clear; selected identity and existing business data remain intact.

## Risk and simplicity review

AI recommends HIGH review depth for this input/ownership boundary, without attributing that classification to the author. R-03 concerns actual roster access; R-05 concerns trusted time and strict lead; R-04/R-07 concern complete state and regression. R-06 requires bounded AI work and a separate human decision. R-08 remains VALIDATION_PENDING.

| Control | Evidence / remaining limit |
|---|---|
| Backend creation validation | Both capacity bounds, invalid types, required fields, strict lead and aware-instant tests; no caller-supplied ID/owner parameter. New registrations are not created here. |
| Stored ownership | Both owners' lists/rosters, wrong roles, missing/forged actors, changed stored owner and forced foreign selector checked. Freely selecting another demo identity remains a disclosed limit. |
| Failure safety | Compare all original rows/counters after rejection or injected construction failure. Use returned state for sequential successes. No persistent/shared/concurrent transaction claim. |
| Proportionate design | Remove the second Workshop construction/validation; keep small outcome/state tuples, frozen rows/lists and native Streamlit controls. Input/type checks implement declared invalid-input contracts; UI conversion guards prevent an observed exception. Menu hiding, UI role checks and target-owner checks serve separate boundaries. Copied mutable lists preserve input snapshots. No new module, router, authentication system, dependency, broad exception wrapper or generic data-validation framework. |
| Regression | Keep 87 parameter cases; explicitly preserve empty fixture assumptions and update message expectations to actual L3 content. Do not weaken denial/state assertions. |
| Human oversight | All H01-H07 below remain unchecked. AI/CI execution does not supply approval, personal observations or risk rationale. Seek suitable advice before dependent work if understanding, policy or review competence is unresolved. |

## Findings and dispositions

| ID | Finding / evidence | Disposition |
|---|---|---|
| L3-F01 | Empty date/time components must not reach datetime.combine unchecked. A private copy removing the guards fails four UI checks. | CORRECTED: pass missing components as invalid input to the business boundary; retain date-clear and explicit missing-time checks. No broad exception handler is added. |
| L3-F02 | AI's first UI test assumed unsent form fields survived an identity switch. The initial run had one failing test/145 passes because that assumption did not hold. | CORRECTED test precondition: choose the current organiser before filling, then prove the resulting owner is that organiser. Document the draft limitation; no draft-persistence feature is introduced. |
| L3-F03 | AppTest set_value(None) for a defaulted time widget normalises to its prior value; treating it as a real missing-time submission caused two test failures. | CORRECTED: inject None at the time-input return boundary after rendering the real widget. Keep two real date-clear cases. Record this mock limitation; do not claim a real-browser time-clearing result. |
| L3-F04 / Medium | Retained denial tests checked error/info text and state, but did not directly exclude a private table or creation control. A private app.py fault rendered a table after denial and still passed all 158 old cases. The actual app did not render that table. | CORRECTED test gap: strengthen the two existing denial functions with no-dataframe/no-create-control assertions. The same faulty copy now fails six denial cases; the unaffected unknown-view case passes. QR-03; R-03/R-07. |
| L3-F05 / Medium | Demo validation checked dates/capacity but not unique registration IDs and all references. A private booking.py fault duplicated a cancelled record's ID and passed all 158 old cases. Actual fixtures were valid. | CORRECTED test gap: assert unique expected fixture IDs, existing role-correct owner/participant references, workshop references and active-pair uniqueness. The same faulty copy now fails the fixture-integrity case. No runtime validation framework is added. R-01/R-04/R-07. |
| L3-F06 / Low | create_workshop constructed a Workshop, then used replace to reconstruct/revalidate it only to trim text. A private measurement observed two model validations for one successful create. | CORRECTED redundancy: trim validated text inputs before the single construction. Existing invalid-input, normalisation, failure and state tests pass. The same measurement observes one validation and unchanged input. No business rule changes. |
| L3-F07 / Low | The owned roster displayed names but no explicit selected-workshop count; the top metric is session-wide. Three independent FR-07 UI cases failed before the correction. | CORRECTED: display Confirmed participants only after successful owned-roster access. Counts one/one/zero across both owners now pass, with matching table/empty state. R-07/R-08; suitability validation remains open. |
| L3-F08 / Medium | clear_on_submit=True and one generic INVALID_INPUT message do not satisfy the author's new failure-retention/field-feedback request. | CORRECTED: retain values on rejection, show shared business-layer field messages, allow correction, and reset only the eight form keys after OK. All 11 new cases failed before implementation and now pass, including exact state/counter and identity checks. Real-browser verification covers the frontend behaviour separately. FR-06; QR-02/QR-04; R-04/R-05/R-07. |
| L3-F09 / Low | The first new test snapshot compared AppTest's pending single-date tuple with its post-run date value. Nine post-implementation tests failed on representation differences; the two correction/success cases passed. | CORRECTED test oracle: normalise only the test API's date/None representation and still compare every selected date and other input exactly. No runtime workaround or weaker field assertion is introduced. R-06/R-07. |

All findings/dispositions above are AI technical work. The author must assess them and record actual acceptance. Historical L2 findings and human decisions remain in their unchanged record.

## Test mapping

Canonical exact-function/requirement/risk mapping is in [test-plan.md](../test-plan.md#l3-implemented-test-mapping).

| Group | Cases | Focus |
|---|---|---|
| Retained L2 | 87 | Canonical identities, menu visibility, independent denial/default rejection, model/time contracts and session preservation. |
| L3-01 | 6 | Valid creation/ownership/IDs, complete independent candidate state, sequential adoption and construction-failure preservation. |
| L3-02 | 8 | Invalid capacities rejected without allocation/mutation. |
| L3-03 | 22 | Strict lead, required/invalid fields, aware/end times, mixed zones and DST elapsed hours. |
| L3-04 | 23 | Actual creation/list/roster roles, stored owner, unknown targets and no data on denial. |
| L3-05 | 2 | Public detail/order/counts, cancelled exclusion and closure information. |
| L3-06 | 2 | Valid relative history, unique IDs/references/active pairs, independent fixtures and one-time web initialisation. |
| L3-07 | 6 | UI creation/current identity, fresh submission time, cleared dates and missing-time conversion. |
| L3-08 | 5 | Owned selector reset, three selected confirmed-count cases and forced foreign target denial. |
| L3-09 | 11 | Eight isolated failures, two owner-specific correction/success/reset flows and one simultaneous-error case. All input values, full business state/counters, selected identity and unrelated session marker checked. |
| Total | 172 | 55 functions: 30 retained plus 25 L3. All 161 preceding cases retained. |

B03-B05 and B13 have implemented verification. B06 presentation/counts and B14's roster lookup are partial; later booking/cancellation/registration-target paths remain pending. Creation's late-form test does not complete I10's later registration operations. AI smoke checks do not close VAL-01/02/03 or R-08.

## Verification results

Executor: AI in the existing Python 3.12.14 environment; no dependency change or installation. Temporary reports/scripts/screenshots remain outside the delivery.

| Check | Actual result |
|---|---|
| Local suite | Fresh PASS: 172/172, zero skipped, 25.15 seconds. Focused new set: 11 passed/161 deselected. Before implementation all 11 new cases failed. JUnit/branch-coverage output is outside the project package. |
| Coverage | booking.py: 146/147 statements and 47/48 branches covered, 99% aggregate. The invalid-hardcoded-demo-fixture failure branch is not exercised in the genuine suite. Coverage is diagnostic, not proof of complete business functionality or an HD threshold. |
| Static/security | Fresh local PASS: Ruff check/format, Bandit and pip check. Locks/workflow are unchanged. Fresh hosted evidence is pending publication of this form revision; earlier audit results are not relabelled as current. |
| Earlier controlled faults | Historical initial-L3 checks: exactly-24h admission 1 failed/3 passed; omitted stored owner 4 failed/8 passed; missing conversion guards 4 failed. These observations remain linked to the initial 158-case candidate, not relabelled as new executions. |
| Earlier deep-review challenges | Historical private table fault: old 158 passed, stronger tests 6 failed/1 passed. Historical duplicate fixture ID: old 158 passed, stronger test failed. Selected-count regression failed before the caption. These are prior AI executions, not fresh form-revision runs; no fault was inserted in delivery code. |
| Earlier construction measurement | Historical isolated before/after measurement: 2 -> 1 Workshop constructions/validations for normalisation, original input unchanged. Current creation still constructs one Workshop. Shared field checks now serve model and input-feedback contracts; no framework is added. |
| Browser | Fresh PASS: Playwright/headless Chrome, 1440x1200 and 390x844 at http://127.0.0.1:8513; a 1440x1450 capture includes success and the complete reset form. Correct page/title, nonblank content and no exception overlay. A missing meeting point and capacities 0/31 retain all eight edited values, identity and original roster selection while the count stays four. Correcting only invalid fields creates workshop-5 once, shows success, resets all defaults and preserves three confirmed records. Another empty submit is rejected; the one new workshop survives browse/refresh. Mobile inline errors retain input without horizontal page overflow. No console warnings/errors or page errors. Screenshots were visually inspected; the independent QA session has five workshops, while a fresh session starts with four. |
| Browser route | Browser plugin not available; existing bundled Playwright 1.62.1/headless Chrome is used. No browser dependency is added to the project. |
| Hosted CI | Form-revision run PENDING at this writing stage. Earlier candidate 9d3d2bb8fc855ed0ef0d5a68d87bb4cfcaf61eab passed [run 44046068677](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44046068677) with 161 tests; that result does not verify this new form revision. |
| Preservation/package | PASS: 20 English files/nine Markdown documents, 51 local links/anchors, and hashes of all 73 protected accepted-folder/original-tracked files. All 39 accepted normative rows and 51 scenario definitions match L0. Model schema/time properties, the other 15 business definitions, locks and single-job workflow are unchanged; model field checks are extracted without changing their tested contracts. All 52 preceding test names/parameters remain, with 11 cases in three new functions. ZIP CRC and all 20 archive-root file bytes match delivery, without environments, reports or private tools. The archive is regenerated after evidence-only documentation updates. |

Reproduce with python -m pytest test_booking.py and the Ruff/Bandit/audit commands in the unchanged workflow. The manual preview is [http://127.0.0.1:8513](http://127.0.0.1:8513), kept running for the author; L2's separate service remains at port 8512. This is local development evidence, not deployed release evidence.

Browser automation uses the actual visible hour/minute spinbutton segments; the backing time input is hidden and cannot be filled as a visible control. The running preview initially cached the older booking module and showed an import error for the new validator. AI refreshed that module in place without restarting/clearing sessions, then restored the exact reviewed app source; no reload/debug hook is delivered. The final browser flow passed against the restored source. AppTest checks complete records/counters and both owners; browser checks are complementary AI verification, not the author's personal execution or product validation. Firefox/Safari and assistive-technology interaction were not checked. Browser scripts, probes and screenshots stay outside the source/ZIP.

Hosted target remains Ubuntu 24.04/Python 3.12.14; artifacts expire after 14 days. Retain material evidence before expiry and inspect the actual latest branch SHA/run when accepting. An evidence-only document follow-up cannot know its own future commit SHA.

## Human acceptance checklist

All items are pending the author's own review. Predict expected outcomes before reading AI results; record what you actually inspect or execute.

- [ ] **H01 Demo and browsing:** In a fresh L3 session, inspect four workshop examples, full dates/S/C/time zone, meeting/preparation details and confirmed/remaining counts. Explain open/full/locked/historical states and cancelled-row exclusion.
- [ ] **H02 Valid/corrected creation:** Select an organiser, fill all fields and submit with a missing meeting point. Check all values remain, correct only that field and resubmit. Confirm exactly one new owned workshop, one ID advance, success feedback and all eight reset defaults. Repeat valid boundary capacities 1/30; confirm identity/old records remain and a subsequent empty submit adds nothing.
- [ ] **H03 Invalid/time boundaries:** Check title/meeting point, end<=start, exactly 24h, cleared dates and capacities 0/31 receive specific inline messages while all values, records and counters remain. Inspect 24h+1 second and fresh late-submission tests. Explain why retained invalid capacity is useful feedback, the model/business rules remain unchanged, and missing-time injection is not a real-browser claim.
- [ ] **H04 Roles and ownership:** Compare Rui Yan's workshop-1/3 targets with Alex's workshop-2/4 targets, confirmed names and selected counts. Switch identities and inspect selector reset. Review wrong-role/non-owner/unknown-target outcomes and forced foreign-target tests. Private-view denial must hide both roster and creation controls; a valid organiser's refused roster target must return no roster while their creation permission remains valid. Confirm unchanged state and distinguish selected-roster counts from the session-wide metric.
- [ ] **H05 State and limits:** Create then navigate/refresh/switch identities without reseeding. Inspect independent-session and valid historical-fixture checks. Explain non-durable, non-authenticated session data and that booking/cancellation/waitlist actions are not implemented.
- [ ] **H06 AI and evidence:** Read the three-file diff, L3-F01-F09, L3-09 mapping, 172-case results and fresh single-job CI. Explain shared validation, one decision time, targeted reset and AppTest/browser limits. Assess the corrected date-oracle assumption and earlier findings. Record actual human checks, edits/rejected suggestions and remaining concerns separately from AI/CI executions.
- [ ] **H07 Decision:** Record reviewer/date/reviewed commit, actual risk classification/rationale, finding assessment and ACCEPT_LOOP or CHANGES_REQUIRED. Use SPECIALIST_ADVICE_REQUIRED if necessary. Keep L4 stopped until your acceptance and a subsequent instruction.

| Human field | Actual value |
|---|---|
| Reviewer/date/reviewed code | TO_BE_RECORDED by the author. |
| Personally executed checks/observations | NOT_YET_RECORDED. |
| Code understanding/independent outcomes | TO_BE_RECORDED by the author. |
| Human edits/rejected suggestions/finding assessment | NOT_YET_RECORDED. |
| Risk classification/rationale/residual limits | TO_BE_RECORDED by the author; AI HIGH review-depth recommendation is separate. |
| Decision | HUMAN_REVIEW_PENDING. |

L3 stops at this human loop gate. L4 is NOT_STARTED. ACCEPT_LOOP, READY_TO_MERGE and ACCEPT_RELEASE remain separate under the [workflow](../../README.md#development-workflow). No personal checks, approval or final user validation are inferred from AI/CI results.
