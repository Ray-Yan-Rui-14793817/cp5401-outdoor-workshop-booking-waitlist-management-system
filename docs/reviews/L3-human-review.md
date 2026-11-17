# L3 Work and Human Review

**Workshop creation, browsing, owned confirmed rosters and valid demo data. Human decision: HUMAN_REVIEW_PENDING. L4: NOT_STARTED.**

## Intake and scope

The author accepted L2, then explicitly requested L3 in L3_develop with creation/browsing, owned lists/rosters, valid demo data, >24h creation, capacity 1-30 and permission checks. Preserve the three-file architecture and single-job Actions, deliver English files/ZIP, retain a manual preview and stop for ACCEPT_LOOP. Base: accepted L2 commit e52dd74816fd89a0fad22e104caa68900d032da0. Executor/tool: Codex. The earlier L3 hold is superseded only for this requested loop.

| Surface | Implemented work |
|---|---|
| app.py | Public workshop information/counts/closure labels, organiser creation form and owned confirmed roster table. Read trusted time again on submission, handle missing date/time components, adopt only an OK candidate and reset obsolete roster selection after identity change. Retain role menus and independent private-view rejection. |
| booking.py | Retain models/identity contracts. Add create_workshop, browse_workshops, confirmed_count, list_owned_workshops, get_workshop_roster, server_now and create_demo_data. No Streamlit import, database or service framework. |
| test_booking.py | Retain all 87 L2 parameter cases; adapt four UI initialisation contexts and two view-message oracles to working/seeded L3 views. Add 71 cases; 158 total in 51 functions. |
| Documents/archive | Update the primary README/requirements/test-plan/Demo/AI records and add this one L3 record. Delivery has 20 files/nine Markdown documents. ZIP has the same root structure including .github, excluding caches, environments, generated reports and private tools. |
| Preserved | Accepted L0/L1/L2 folders and historical review files, original tracked working copy, FR/BR/QR/risk definitions, four dependency input/lock files, pyproject.toml and single-job workflow. |
| Deferred | Booking/history actions, cancellation/repeats, waitlist, full lifecycle/validation, deployment and releases. No PR, merge, release or L4 work. |

## Contracts and assumptions

- create_workshop receives current session state, a selected actor, intended workshop fields and trusted current time. Only a canonical organiser may create. IDs/owner come from the application. Validate required text, aware times/end>S, capacity integer 1-30 and S-t>24 elapsed hours. Exactly 24 hours or less returns INVALID_INPUT without record/counter changes.
- Success returns (OK, complete_new_state); reject returns an outcome with unchanged input. The new state's three mutable lists are independent while frozen rows may be reused. Unexpected construction exceptions propagate without changing the input; this is not a database rollback/recovery guarantee. The UI replaces state only after OK.
- server_now is the application UTC clock, called again at submission. Tests replace it; no current-time control is exposed to users. Intended form times use Asia/Singapore. Workshop/end/cutoff display includes seconds.
- Roster access looks up the actual workshop and passes its stored owner ID to check_permission. Wrong-role/non-owner results return no records; a valid organiser's missing target returns UNKNOWN_WORKSHOP. Confirmed rosters exclude CANCELLED history. Public counts also exclude cancelled rows.
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
| Proportionate design | Keep small outcome/state tuples, frozen rows/lists and native Streamlit controls. Retain menu hiding plus independent permission checks. No new app module, router, authentication system, dependency or generic exception wrapper. |
| Regression | Keep 87 parameter cases; explicitly preserve empty fixture assumptions and update message expectations to actual L3 content. Do not weaken denial/state assertions. |
| Human oversight | All H01-H07 below remain unchecked. AI/CI execution does not supply approval, personal observations or risk rationale. Seek suitable advice before dependent work if understanding, policy or review competence is unresolved. |

## Findings and dispositions

| ID | Finding / evidence | Disposition |
|---|---|---|
| L3-F01 | Empty date/time components must not reach datetime.combine unchecked. A private copy removing the guards fails four UI checks. | CORRECTED: pass missing components as invalid input to the business boundary; retain date-clear and explicit missing-time checks. No broad exception handler is added. |
| L3-F02 | AI's first UI test assumed unsent form fields survived an identity switch. The initial run had one failing test/145 passes because that assumption did not hold. | CORRECTED test precondition: choose the current organiser before filling, then prove the resulting owner is that organiser. Document the draft limitation; no draft-persistence feature is introduced. |
| L3-F03 | AppTest set_value(None) for a defaulted time widget normalises to its prior value; treating it as a real missing-time submission caused two test failures. | CORRECTED: inject None at the time-input return boundary after rendering the real widget. Keep two real date-clear cases. Record this mock limitation; do not claim a real-browser time-clearing result. |

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
| L3-06 | 2 | Valid relative history/independent fixtures and one-time web initialisation. |
| L3-07 | 6 | UI creation/current identity, fresh submission time, cleared dates and missing-time conversion. |
| L3-08 | 2 | Owned selector reset and forced foreign target denial. |
| Total | 158 | 51 functions: 30 retained plus 21 new. |

B03-B05 and B13 have implemented verification. B06 presentation/counts and B14's roster lookup are partial; later booking/cancellation/registration-target paths remain pending. Creation's late-form test does not complete I10's later registration operations. AI smoke checks do not close VAL-01/02/03 or R-08.

## Verification results

Executor: AI in the existing Python 3.12.14 environment; no dependency change or installation. Temporary reports/scripts/screenshots remain outside the delivery.

| Check | Actual result |
|---|---|
| Local suite | PASS: 158/158, zero skipped, 20.71 seconds. JUnit/branch-coverage output is outside the project package. A later test-name clarification changes no assertion/parameter. |
| Coverage | booking.py: 129/130 statements and 37/38 branches covered, 99% aggregate. The invalid-hardcoded-demo-fixture failure branch is not exercised in the genuine suite. Coverage is diagnostic, not proof of complete business functionality or an HD threshold. |
| Static/security | PASS locally and in hosted CI: Ruff check/format, Bandit and pip check. Hosted strict audits found no known vulnerabilities and reconciled all 34 runtime/71 development pins without omissions. Point-in-time evidence; inputs/locks/workflow are unchanged. |
| Controlled faults | Exactly-24h admission: 1 failed/3 passed. Omitting stored roster owner: 4 failed/8 passed, including the forced-target UI path. Removing date/time guards: 4 failed. These expected failures are in private copies; delivered code passes. |
| Browser | PASS: headless Chrome/Playwright, 1440x1000 and 390x844 at http://127.0.0.1:8513. Correct page/title, nonblank public data, no exception overlay, both owners' targets, blank-input rejection, capacity-one/thirty creation, browsing/refresh, role reset, owned-list exclusion and mobile overflow checks passed. No console warnings/errors or page errors. Screenshots show a private QA session with two added workshops (six total); a fresh human session starts with four fixtures. |
| Browser route | Browser plugin not available; existing bundled Playwright 1.62.1/headless Chrome is used. No browser dependency is added to the project. |
| Hosted CI | PASS for code/test commit 47a965614a34ab59ca0335ac5f3ea319895c801b on codex/l3-workshops: [run 44040466634](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44040466634), job 133893533263. One quality-checks job; all 18 steps succeeded, none skipped. Logs confirm 158 passed in 11.54 seconds, runtime-only installation/imports, static/security checks, complete lock audits and report upload. |
| Preservation/package | PASS: 20 English source files/nine Markdown documents; all 50 local links/anchors; unchanged accepted L0/L1/L2/original working copy, rule/scenario rows, retained model/identity definitions, locks and workflow. The delivered L3_develop.zip contains those same 20 root-relative files, verified by CRC and byte comparison; no environment, caches, reports or private tools. |

Reproduce with python -m pytest test_booking.py and the Ruff/Bandit/audit commands in the unchanged workflow. The manual preview is [http://127.0.0.1:8513](http://127.0.0.1:8513), kept running for the author; L2's separate service remains at port 8512. This is local development evidence, not deployed release evidence.

Browser automation was corrected to read selectbox values, use the visible Open button and reacquire a dropdown closed by a Streamlit rerun. Final assertions still compare the full owned-option set; no failed application assertion was waived. Roster names and forced-target denial are checked by AppTest as documented above. Browser screenshots/temporary scripts stay outside the source/ZIP.

Hosted environment: Ubuntu 24.04/Python 3.12.14. Artifact quality-checks-44040466634-1 expires on 1 December 2026; retain material evidence before expiry. This evidence-only document follow-up changes no executable/configuration hashes. Inspect the latest branch run when accepting; this link identifies the tested code rather than claiming the document knew its own future commit SHA.

## Human acceptance checklist

All items are pending the author's own review. Predict expected outcomes before reading AI results; record what you actually inspect or execute.

- [ ] **H01 Demo and browsing:** In a fresh L3 session, inspect four workshop examples, full dates/S/C/time zone, meeting/preparation details and confirmed/remaining counts. Explain open/full/locked/historical states and cancelled-row exclusion.
- [ ] **H02 Valid creation:** Select Rui Yan or Alex before filling the form. Create >24h workshops with capacity 1 and 30. Check assigned ID/current owner, newly owned empty roster, public visibility and updated metrics. Observe draft behaviour separately from submitted data.
- [ ] **H03 Invalid/time boundaries:** Inspect/run selected creation tests for 24h+1 second, exactly 24h, less/past, invalid capacities/types, blank fields, missing dates and fresh late submission. Explain why UI range controls do not replace backend checks and why missing-time injection is not a real-browser claim. Confirm complete-state/ID preservation.
- [ ] **H04 Roles and ownership:** Compare Rui Yan's workshop-1/3 targets with Alex's workshop-2/4 targets and their confirmed names. Switch identities and inspect selector reset. Review wrong-role/non-owner/unknown-target outcomes and the forced foreign-target test; predict that denial returns no roster or mutation.
- [ ] **H05 State and limits:** Create then navigate/refresh/switch identities without reseeding. Inspect independent-session and valid historical-fixture checks. Explain non-durable, non-authenticated session data and that booking/cancellation/waitlist actions are not implemented.
- [ ] **H06 AI and evidence:** Read the three-file diff, L3-F01-F03, exact mapping, controlled faults, 158-case results and fresh single-job CI. Explain the three tested faults and the two corrected AI test assumptions. Record actual human edits, rejected suggestions and checks separately from AI/CI executions.
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
