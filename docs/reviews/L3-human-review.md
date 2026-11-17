# L3 Work and Human Review

**Workshop creation, browsing, owned confirmed rosters and valid demo data. Human decision: HUMAN_REVIEW_PENDING. L4: NOT_STARTED.**

## Intake and scope

The author accepted L2, then explicitly requested L3 in L3_develop with creation/browsing, owned lists/rosters, valid demo data, >24h creation, capacity 1-30 and permission checks. Preserve the three-file architecture and single-job Actions, deliver English files/ZIP, retain a manual preview and stop for ACCEPT_LOOP. Base: accepted L2 commit e52dd74816fd89a0fad22e104caa68900d032da0. Executor/tool: Codex. The earlier L3 hold is superseded only for this requested loop.

On 17 November 2026 (Asia/Singapore), the author requested this deep review of L3 candidate 367765d8e822e5e5a365810643e61a8c0f9980e4, with corrections, English files/ZIP and the live service retained. This instruction supplies review scope, not ACCEPT_LOOP. Changed files: app.py, booking.py, test_booking.py, README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md and this record.

| Surface | Implemented work |
|---|---|
| app.py | Public workshop information/counts/closure labels, organiser creation form and owned confirmed roster table. Read trusted time again on submission, handle missing date/time components, adopt only an OK candidate and reset obsolete roster selection after identity change. Retain role menus and independent private-view rejection. |
| booking.py | Retain models/identity contracts. Add create_workshop, browse_workshops, confirmed_count, list_owned_workshops, get_workshop_roster, server_now and create_demo_data. No Streamlit import, database or service framework. |
| test_booking.py | Retain all 87 L2 parameter cases; adapt four UI initialisation contexts and two view-message oracles to working/seeded L3 views. Strengthen denial/fixture assertions. Add 74 cases; 161 total in 52 functions. |
| Documents/archive | Update the primary README/requirements/test-plan/Demo/AI records and add this one L3 record. Delivery has 20 files/nine Markdown documents. ZIP has the same root structure including .github, excluding caches, environments, generated reports and private tools. |
| Preserved | Accepted L0/L1/L2 folders and historical review files, original tracked working copy, FR/BR/QR/risk definitions, four dependency input/lock files, pyproject.toml and single-job workflow. |
| Deferred | Booking/history actions, cancellation/repeats, waitlist, full lifecycle/validation, deployment and releases. No PR, merge, release or L4 work. |

## Course and baseline alignment

AI re-extracted the original assessment and three supplied transcript PDFs and inspected Week3-9 lecture material from Week1-9.zip; source hashes match the earlier review. The rubric's page 10 was also rendered and inspected. Sources S01-S08/S13-S14 in [Demo reuse](../demo-reuse.md#references) identify the material. Automatic transcripts are supplied accounts, not audio independently checked by AI; the 09:40/10:45 texts are identical.

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
| Total | 161 | 52 functions: 30 retained plus 22 new. Retained denial assertions are strengthened. |

B03-B05 and B13 have implemented verification. B06 presentation/counts and B14's roster lookup are partial; later booking/cancellation/registration-target paths remain pending. Creation's late-form test does not complete I10's later registration operations. AI smoke checks do not close VAL-01/02/03 or R-08.

## Verification results

Executor: AI in the existing Python 3.12.14 environment; no dependency change or installation. Temporary reports/scripts/screenshots remain outside the delivery.

| Check | Actual result |
|---|---|
| Local suite | PASS: 161/161, zero skipped, 22.67 seconds. Focused corrected set: 11 passed/150 deselected. JUnit/branch-coverage output is outside the project package. |
| Coverage | booking.py: 128/129 statements and 37/38 branches covered, 99% aggregate. The invalid-hardcoded-demo-fixture failure branch is not exercised in the genuine suite. Coverage is diagnostic, not proof of complete business functionality or an HD threshold. |
| Static/security | Fresh local PASS: Ruff check/format, Bandit and pip check. Dependencies/workflow are unchanged; fresh hosted results are recorded below when available. |
| Earlier controlled faults | Historical initial-L3 checks: exactly-24h admission 1 failed/3 passed; omitted stored owner 4 failed/8 passed; missing conversion guards 4 failed. These observations remain linked to the initial 158-case candidate, not relabelled as new executions. |
| Fresh test challenges | Private table after denial: old 158 passed in 18.11s; strengthened tests 6 failed/1 passed/154 deselected. Duplicate cancelled fixture ID: old 158 passed in 18.37s; strengthened test 1 failed/160 deselected. Selected-count regression: 3 failed/158 deselected before the caption, now passes. These expected failures are in controlled copies or the pre-fix genuine UI; delivered code passes. |
| Construction measurement | Isolated before/after measurement: 2 -> 1 model validations for the same successful normalised creation, original state unchanged. This is a private diagnostic, not a new implementation-mirroring test. |
| Browser | Fresh PASS: headless Chrome/Playwright, 1440x1000 and 390x844 at http://127.0.0.1:8513. Correct page/title, four initial examples, no exception overlay, both owners' targets, selected counts one/zero, blank-input rejection, capacity-one/thirty creation, browsing/refresh, role reset, owned-list exclusion and mobile overflow checks. No console warnings/errors or page errors. Screenshots show a private QA session with two added workshops (six total); a fresh human session starts with four fixtures. Screenshots were visually inspected. |
| Browser route | Browser plugin not available; existing bundled Playwright 1.62.1/headless Chrome is used. No browser dependency is added to the project. |
| Hosted CI | Fresh review run PENDING at this code-writing stage. Prior candidate 367765d8e822e5e5a365810643e61a8c0f9980e4 passed [run 44041203015](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44041203015) with 158 cases; that is historical evidence, not proof of this revised candidate. |
| Preservation/package | PASS: 20 English files/nine Markdown documents and 51 local links/anchors. Hashes of 73 protected accepted-folder/original-tracked files match the pre-review snapshot; historical review files, normative rows, retained models/helpers, locks and workflow are unchanged. All 51 old test names/parameter definitions remain; three cases in one new function are added. ZIP has the same 20 root-relative files including .github, checked by CRC/byte comparison; no environment, reports or private tools. The archive is regenerated after evidence-only documentation updates. |

Reproduce with python -m pytest test_booking.py and the Ruff/Bandit/audit commands in the unchanged workflow. The manual preview is [http://127.0.0.1:8513](http://127.0.0.1:8513), kept running for the author; L2's separate service remains at port 8512. This is local development evidence, not deployed release evidence.

Browser automation was corrected to read selectbox values, use the visible Open button and reacquire a dropdown closed by a Streamlit rerun. Final assertions still compare the full owned-option set; no failed application assertion was waived. Roster names and forced-target denial are checked by AppTest as documented above. Browser screenshots/temporary scripts stay outside the source/ZIP.

Hosted target environment remains Ubuntu 24.04/Python 3.12.14. Quality artifacts expire after 14 days; retain material evidence before expiry. Inspect the latest branch run and actual SHA when accepting; an evidence-only document follow-up cannot know its own future commit SHA.

## Human acceptance checklist

All items are pending the author's own review. Predict expected outcomes before reading AI results; record what you actually inspect or execute.

- [ ] **H01 Demo and browsing:** In a fresh L3 session, inspect four workshop examples, full dates/S/C/time zone, meeting/preparation details and confirmed/remaining counts. Explain open/full/locked/historical states and cancelled-row exclusion.
- [ ] **H02 Valid creation:** Select Rui Yan or Alex before filling the form. Create >24h workshops with capacity 1 and 30. Check assigned ID/current owner, newly owned empty roster with selected count zero, public visibility and updated metrics. Observe draft behaviour separately from submitted data.
- [ ] **H03 Invalid/time boundaries:** Inspect/run selected creation tests for 24h+1 second, exactly 24h, less/past, invalid capacities/types, blank fields, missing dates and fresh late submission. Explain why UI range controls do not replace backend checks and why missing-time injection is not a real-browser claim. Confirm complete-state/ID preservation.
- [ ] **H04 Roles and ownership:** Compare Rui Yan's workshop-1/3 targets with Alex's workshop-2/4 targets, confirmed names and selected counts. Switch identities and inspect selector reset. Review wrong-role/non-owner/unknown-target outcomes and forced foreign-target tests. Private-view denial must hide both roster and creation controls; a valid organiser's refused roster target must return no roster while their creation permission remains valid. Confirm unchanged state and distinguish selected-roster counts from the session-wide metric.
- [ ] **H05 State and limits:** Create then navigate/refresh/switch identities without reseeding. Inspect independent-session and valid historical-fixture checks. Explain non-durable, non-authenticated session data and that booking/cancellation/waitlist actions are not implemented.
- [ ] **H06 AI and evidence:** Read the three-file diff, L3-F01-F07, exact mapping, controlled faults, 161-case results and fresh single-job CI. Explain why the two old test gaps mattered, how the stronger assertions detect them and why duplicate construction was removed. Assess earlier AI test assumptions and review limits. Record actual human edits, rejected suggestions and checks separately from AI/CI executions.
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
