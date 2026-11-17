# L4 Work and Human Review

**Current candidate: L4-F08. State: HUMAN_REVIEW_PENDING. Human decision: PENDING. H01-H07: unchecked. L5: NOT_STARTED.**

## Intake and preserved scope

On 17 November 2026, the author explicitly requested L4 from accepted L3/GitHub: participant booking and personal records/history; capacity, duplicate-active, 24-hour and permission rules; L4_develop; retained simple architecture, single-job Actions and L1-L3 regressions; English files, local-only ZIP, live preview and a stop for ACCEPT_LOOP. This instruction supersedes the earlier L4 hold, but supplies no L4 personal acceptance.

Base: [accepted L3 74f9281f420755a42141d9792c023cec5d53bf34](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/74f9281f420755a42141d9792c023cec5d53bf34). Its author-approved candidate, UI/H01-H07 declaration and HF-01-HF-03 remain unchanged in the historical L3 review. Executor: Codex assistant. Records use the supplied client date, 17 November 2026; workshop time display remains Asia/Singapore. No precise personal execution time is inferred.

Changed files: app.py, booking.py, test_booking.py, README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md and this new review. The other twelve files, including workflow, dependency inputs/locks, configuration and four historical reviews, retain their L3 bytes. Accepted local L0-L3 folders/archives and original tracked files are protected separately.

## Current L4-F08 intake and scope

Base candidate: a441bb6ae6ab6e5f350448db524e63ce7b05c3e9 on codex/l4-bookings. The author explicitly requested Per-organiser Workshop Creation Draft Isolation after the prior technical review, with eight functional goals and a stop at L4. This is a UI-state refinement during V1.0 development, not the later assessed CR-01 waitlist change. Human acceptance remains PENDING.

Executable changes are confined to app.py and test_booking.py. Six existing Markdown documents record the scope/mapping/evidence. No delivery file is added: 21 files/10 Markdown documents remain. booking.py, FR/BR/QR/risk/scenario definitions, dependency files, configuration and the single-job workflow remain unchanged. Original L0-L3 files, accepted reviews and the original tracked working copy retain their bytes.

Implementation: creation_forms[user_id] stores one organiser's latest failed eight values, errors and feedback. The existing eight widget keys are only the visible form; a creation_form_owner marker forces reload from the selected organiser's entry/defaults on an organiser switch. Missing widget keys restore that same organiser's last failure. Success replaces only that organiser's entry with scoped one-time feedback/reset, then resets those eight inputs. Draft identity metadata is never used to resolve the actor or assign Workshop ownership. Existing menu hiding and direct business rejection remain independent.

The original L3 HF-02 accepted shared failed-draft reuse across fictional identities. The explicit F08 instruction supersedes that current UI behaviour while the historical record remains untouched. Earlier F05/deep-review results below describe those candidates. Freely choosing demo identities still does not authenticate a person; use fictional data. Unsubmitted edits and cross-session/restart persistence remain unpromised. Old unowned shared UI draft data is not automatically attributed to whichever organiser is selected after the code update.

AI-proposed corrective-patch risk: Medium, because visible UI values/errors/reset now depend on selected identity and must preserve unrelated state. Controls: fixed-ID namespaces, active-form reload, current-actor business ownership, scoped replacement, complete state/counter checks and retained F05/permission regressions. Human risk disposition and acceptance are pending; no security/authentication approval or reviewer action is fabricated.

### F08 acceptance and test mapping

| Goal | Planned/verified acceptance | Automated evidence |
|---|---|---|
| 1 | Eight failed values/errors/feedback belong to fixed user_id, independently for Rui/Alex. | f08_failed_drafts_and_errors_are_isolated_by_organiser_id; f08_feedback_is_scoped_even_when_failure_outcomes_differ |
| 2 | Alex initially sees defaults and no Rui errors/feedback, including direct same-role switching. | f08_failed_drafts_and_errors_are_isolated_by_organiser_id (direct/participant/cleared); f08_unsubmitted_edits_are_not_shown_to_a_different_organiser |
| 3 | After both failures, returning to Rui restores Rui's latest values/errors only. | f08_failed_drafts_and_errors_are_isolated_by_organiser_id; f08_latest_failure_replaces_only_its_own_values_and_errors |
| 4 | Same-owner public/role round trips restore that owner's failed submission. | Retained test_failed_creation_survives_leaving_the_form_and_retry_uses_current_owner, with declared F08 role-route adaptation |
| 5 | Either organiser's success creates one owned Workshop, resets only their form and leaves the other's failure unchanged. | f08_success_clears_only_the_current_organisers_failed_form (both owners) |
| 6 | Draft owner/selected-ID fields cannot control ownership; use the validated current actor. | f08_draft_identity_fields_cannot_assign_workshop_ownership (both owners); retained business permission tests |
| 7 | Participant/no identity sees no creation menu/form; business role/owner denials persist. | New direct/participant/cleared routes plus unchanged role-menu, bypass and business-denial regressions |
| 8 | Only latest failed snapshots are saved; identity selection stays fictional, data stays session-only. | f08_latest_failure_replaces_only_its_own_values_and_errors; f08_unsubmitted_edits_are_not_shown_to_a_different_organiser; retained session-isolation tests and disclosed limits |

### F08 verification

Actual executor: AI/local tools or Actions as labelled, not the author.

| Check | Result |
|---|---|
| Before implementation | All 10 new F08 cases failed, with 228 deselected. |
| Focused implementation run | 13 passed: 10 F08 cases plus three affected prior parameter cases. |
| Full local regression | 238 passed in 44.20s, zero failures/skips; 90 test functions. All 228 prior parameter cases remain. |
| Regression adaptations | Two prior UI functions are explicitly adapted: shared-draft role route now returns to the original organiser, and Book's preserved UI-state fixture uses organiser-keyed storage. All parameter sets and business assertions remain; 82 prior bodies are identical. |
| Static/dependency consistency | Ruff, format check, Bandit and pip check pass. Business module, dependency locks and workflow are byte-identical to the base. |
| Browser | PASS: eight Chrome flows, desktop 1440x1400/mobile 390x844, fresh QA process on 8515. Correct title/URL/nonblank page; no framework exception, browser warning/error or page error. Both drafts restore, Rui success leaves Alex's failure, restricted menus hide, Alex success stays owned, and Book/history still work. Fresh server has no F05 warning. Primary human service remains on 8514 and a separate smoke check confirms it serves F08. The temporary 8515 QA process was stopped after verification. Browser plugin not available; existing bundled Playwright used. |
| Current Actions | PASS: [run 44085569318](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44085569318), job 134046977451, tested F08 code candidate baa675ac7428a818e7202bf703bd3ef2ce5b290c. All 18 steps of the single quality-checks job succeeded, including 238 tests and complete audits of 34 runtime/71 development pins with no known vulnerabilities or omitted packages. Earlier 228-case Actions below are historical. A subsequent records-only commit records these results; its current Actions must also pass. |
| Packaging/baselines | All 21 source files are checked against the branch/archive by raw contents; 94 protected prior files/archive, historical reviews and canonical definitions remain unchanged. The personal ZIP stays local, includes the workflow at archive root and excludes private tools/reports/environments. Final comparison is repeated after this records-only update. |

QA correction: early script assertions observed frontend hydration/rerendering before completion. Waiting for the approved default, completed render and target absence, and normalising equivalent time representations resolves the harness assumptions. No additional runtime workaround or rule change was needed. UI evidence is not human acceptance or R-08 validation.

## Pre-F08 deep-review intake

Review candidate: ede6f67fd3009e567a70a701e0976115ebe15945 on codex/l4-bookings. The latest author instruction requests source-based review and corrections, including F05, but supplies no personal H01-H07 result or ACCEPT_LOOP. This correction changes eight existing files: app.py, test_booking.py, README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md and this record. booking.py, all FR/BR/QR/risk/scenario definitions, workflow, dependencies and historical reviews remain unchanged. No new delivery file is added.

AI-proposed risk triage: High for the L4 candidate as a whole, because allocation, selected-role enforcement, cutoff validation and state/ID integrity require careful review. The corrective patch is Medium: bounded user-visible form initialisation plus stronger generated tests, without role, allocation, storage or dependency-policy changes. These are proposed review classifications, not human approval. The author must confirm or revise and justify them at H07. The prototype's fictional identities, one-session memory and absence of real authentication remain explicit; no specialist approval or production suitability is inferred.

Review method: compare accepted definitions and exact historical test bodies; inspect real business/UI entry points and candidate adoption; reproduce F05 with warnings enabled; challenge independent oracles with isolated faulty copies; rerun the retained/new suite and static checks; verify fresh-process browser behaviour, branch identity and archive contents. No speculative framework, generic validator, defensive data repair or unrelated feature is introduced.

## Behaviour and independent expectations

| Operation | Expected outcome and state |
|---|---|
| Eligible participant, spare place, t<C | OK; one new CONFIRMED row/new ID, equal creation/update instants, only registration counter advances. Complete candidate, unchanged input. |
| Eligible participant, full workshop, t<C | FULL; no record, counter advance or automatic waiting. |
| Active same-participant/workshop record, spare place, t<C | DUPLICATE_ACTIVE; original record/ID unchanged. |
| Existing CANCELLED history, t<C | May book a new ID if capacity allows; preserve cancelled row. An overlapping workshop remains independent. |
| At C or later, including S/after S | REGISTRATION_CLOSED; no effective Book. UI uses fresh trusted time at the actual operation even when rendered before C. |
| Missing/forged actor, organiser, unknown workshop | INVALID_ACTOR, FORBIDDEN or UNKNOWN_WORKSHOP; complete input unchanged. No arbitrary participant ID is accepted for an own-record read. |
| Personal record read | OK and only the selected participant's IDs, including history; wrong role/invalid actor returns no records. Freely changing the demo identity remains possible. |
| Failure before candidate adoption | Original session state/counters remain; no false success. Construction/programming exceptions propagate rather than being concealed by a broad exception handler. |

Order follows the accepted observable contract: role, actual target, valid clock, time, duplicate, capacity. Tests isolate each intended refusal with valid other preconditions. Missing/naive application clock input returns INVALID_INPUT; this is an internal safe rejection, not a UI clock editor or a new participant policy.

Current/history grouping is presentation only: upcoming CONFIRMED records appear under upcoming bookings; CANCELLED and started workshop records appear in History. A started CONFIRMED row keeps CONFIRMED and does not establish attendance/completion. All records come from the role-checked actor-ID filter.

## Architecture, Demo and course alignment

Keep app.py -> booking.py -> Python dataclasses/lists, plus test_booking.py. L4 adds two small domain entry points, not a service/repository layer, database, auth framework or shared cache. Mutable lists are copied on success because BR-13/QR-02 require input independence. Role checks in UI and business code serve different boundaries; hidden controls do not enforce the operation. Trusted clock validation rejects unusable input before arithmetic; no global defensive state-repair or speculative fallback policy is introduced.

The pinned CampusConnect Demo supplies separation, session memory and pytest ideas. L4's ID-based permission/filtering, strict cutoff, retained history and complete-state contract are project-specific AI-assisted code. Do not inherit name keys, overlap rejection, deletion or automatic waiting. Explain why full Book stays FULL and why cancelled history permits a new ID. [Demo reuse and source references](../demo-reuse.md) retain the exact provenance.

Assessment/lecture mapping uses the accepted source review rather than inventing a new marking threshold: S01/S02 establish realistic scope and permitted explained adaptation; S04/S05/S08 support bounded AI tasks, assumptions, human ownership and stage exits; S06/S14 support independent rule-based oracles and retained regressions; S07 supports static/security/dependency checks and findings dispositions; S13 distinguishes verification from user validation. The linked references identify the original assessment, transcripts and slides. This loop supplies evidence toward those criteria; it is not a claim that all HD rubric, release, validation, deployment or submission requirements are complete.

## Assessment, HD rubric and lecture check

Baseline comparison: all 39 FR/BR/QR/risk definition rows and 51 canonical scenario rows match each accepted L0-L3 snapshot. L0 keeps business rules/risks in separate documents; compare their combined definitions with the consolidated current requirements rather than treating that file-layout difference as a rule change. All 94 protected prior files/archive retain their hashes.

The four original PDFs were re-extracted and their hashes match the L3 source review. The 09:40/10:45 lecture copies are duplicated transcription accounts, not independent audio verification. The supplied Week1-9 archive was read directly; relevant Week3-9 slides were inspected. Source identifiers remain in [Demo reuse](../demo-reuse.md#references). Original course files/private QA tools are not delivered.

| Criterion / source | L4 evidence and remaining work |
|---|---|
| Requirements/quality planning, 15%; S01 pp.3/10 | Accepted FR/BR/QR/risk/scenario rows unchanged; implemented subset and exact new test mapping remain explicit. H01/H07 review and R-08 suitability are pending. |
| Functional application/deployment, 15%; S01 pp.3/10 | Booking, history, fixed roles, creation and owned rosters verified in the local preview. This is not the assessed hosted deployment or a completed V1.0; L5/L6 remain necessary. |
| V&V/automated testing, 20%; S01 pp.3/10-11; S06/S13/S14 | Rule outcomes, complete state/counters, cutoff boundaries, negative cases and stronger independent oracles are verified. Real-user VAL/R-08 validation and the author's executions are separate and pending. A high test count or coverage value cannot close them. |
| Change/regression/release, 20%; S01 pp.4/12 | Preserve all 221 existing tests and compare historical definitions; retain focused findings/corrections and branch evidence. L4 builds the initial baseline; it is not CR-01. Working V1.0 must precede waitlist impact analysis, Issue/CR, PR, justified merge and V1.1 deployment/release. |
| GitHub/CI, 15%; S01 pp.5/12; S07 | Progressive branch commits, explicit code identities, one unchanged quality-checks job and reports support this stage. The assessed Issue/PR/release lifecycle remains later work; current hosted results must match the candidate. |
| Presentation/defence/judgement, 15%; S01 pp.8/13; S02/S03/S08 | Specific AI tasks, real mistakes/corrections, Demo differences, findings and H01-H07 support explainability. The author's personal understanding, risk decision, PPTX, oral defence and final submission are not created by AI checks. |

S02 English p.2 permits adapting the three core Demo files to a different realistic project; pp.8-9 require explained changes, tests, assumptions, small scope and human review. S03 English pp.2-4/6-7 emphasises risk-based routing, substantive AI disclosure, static/security/dependency evidence and an audit trail. These teaching examples do not add overlap rules, real login, databases or mandatory additional reviewers to this accepted prototype.

Lecture standards checked: Week3 supplementary slides 4/17 (plans, stages and ownership); Week4 slides 4/18/22 (lifecycle V&V, findings and traceability); Week5 slides 4/9/12 (test levels and requirement oracles); Week6 slides 11/14/17/20 (intent, assumptions, triage and human verification); Week7 slides 7/12/14 (observable assertions and retained safeguards); Week8 supplementary slide 26, labelled 20, and slide 28, labelled 22 (proportionate gates and judgement); Week9 slides 2/3/5/18/19 (author ownership, bounded changes, evidence and defence). CampusConnect waitlist/overlap examples teach the method; the project's accepted FULL/ID/cutoff contracts remain the oracle.

Technical review conclusion: the reviewed genuine booking/history/capacity/duplicate/cutoff/selected-permission/state/counter paths show no confirmed rule violation. F05 is corrected and two oracle weaknesses are addressed. The architecture remains proportionate: list copies meet BR-13, UI/business checks serve separate boundaries, and no extra service layer, broad catch, dependency or generic state fallback is needed. This supports the L4 stage, not a declaration of an HD grade or final assessment completion. Human decision remains PENDING.

## Verification results

Historical pre-F08 execution results follow. The current 238-case candidate is recorded under F08 verification above.

Actual executor is AI/local tooling or GitHub Actions as identified below. No result in this section is the author's personal execution.

| Check | Current evidence |
|---|---|
| Test-first L4 checks | Before implementation: 41 failed, 3 passed, 177 deselected. The passing three were absence-of-participant-controls checks already true in L3. Failures concerned missing L4 API/UI. |
| Full local suite | 228 passed in 38.91s, zero failures/skips, Python 3.12.14. All 221 prior cases remain, including 177 L1-L3 cases. Seven new cases in three functions give 84 test functions. |
| Retained-test comparison | All 81 initial L4 test-function ASTs and parameter definitions are unchanged by this review; all 58 historical L1-L3 functions remain. No existing oracle is weakened. The initial L4 placeholder-message adaptation remains historical. |
| Static/installation checks | Ruff check, Ruff format --check, Bandit and pip check all passed. No dependency or workflow change. Hosted audits are recorded separately below. |
| Cleared controls | Three private AppTest probes cleared actual start-time/end-time/capacity controls to None after the fix. Empty values and specific field errors remained, workshop count stayed four, and no exception occurred. The retained historical time-conversion injections remain separately labelled; these probes are not extra suite cases or browser/user-validation evidence. |
| Real browser | PASS: seven observed flows on a fresh process at port 8515, Chrome via existing bundled Playwright, desktop 1440x1100/1300 and mobile 390x844. Correct title/URL, nonblank content, no framework exception, zero browser warnings/errors/page errors. Invalid-draft restoration and success reset preserve all eight intended values; the fresh server log contains no duplicate-default warning or traceback. Primary human preview remains http://127.0.0.1:8514. Browser plugin not available; no new dependency. |
| Hosted Actions | PASS: [run 44077560907](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44077560907), job 134019409676, tested corrective code candidate b971001beefa253b7166fd8548f36d1f483ff674. Collected 228; 228 passed in 39.07s. All 18 steps succeeded, including runtime-only installation/imports, static checks and complete audits of 34 runtime/71 development pins, with no known vulnerabilities or omissions. The earlier 221-case runs remain historical. |
| Delivery integrity | The 21-file prepared GitHub tree matches all local blobs; twelve retained files match L3 byte for byte. Personal archive/export verification compares all 21 raw file contents and CRC, excludes private tools/reports/environments and confirms no tracked ZIP. All 94 protected prior files/archive remain unchanged. The final delivery is checked again after the records-only update. |

Review branch: [codex/l4-bookings](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/tree/codex/l4-bookings). Code/run identities are recorded for their actual execution; historical results are not relabelled as current. A later records-only commit may add completed evidence without changing code/tests/workflow/locks; current branch Actions must also pass. Quality artifacts expire after 14 days; they are distinct from the personal source ZIP.

Deep-review reproduction: before fixing F05, the seven new cases gave two failures (success reset and draft restore), five passes and 221 deselected. After the fix, seven pass; the full suite passes 228. Two isolated faults each passed all 221 old cases. New history-boundary assertions reject the end-time fault at S/S+1 (two failures, one pre-S pass); new rejected-candidate assertions reject both outcomes (two failures). The genuine history/adoption implementation was already correct and is unchanged.

Coverage is diagnostic. Test identities, clocks and injected failures are fixtures, not hidden deployed user controls. I01/I02 prove serial same-session ordering, not a concurrent race. I05/I06/I08/I09/I10 are covered only for implemented operations/observed lifecycle; later cancellation/waitlist paths remain planned. Browser smoke checks are not VAL/R-08 user validation.

## Review findings and dispositions

| ID | Finding, correction and current disposition |
|---|---|
| L4-F01 | A test insertion initially displaced two retained metric assertions into a new test. The first implementation run was 43/44 for new cases and exposed the misplaced fixture assumption. AI restored both assertions to their original regression function, moved all new functions to the end, then compared retained ASTs. No original assertion/parameter is removed; all 221 cases pass. Closed technical correction. |
| L4-F02 | An old My Bookings message promised a future feature. AI replaced the shared UI/test placeholder oracle with the implemented personal-view message and added assertions on actual registration IDs/statuses for both identities. Historical test-function bodies remain unchanged. Closed adaptation. |
| L4-F03 | The initial formatted check found whitespace introduced when relocating tests. AI ran the existing formatter. This affects layout only, with a subsequent format check required; no extra test helper/framework is delivered. Closed by final formatting verification. |
| L4-F04 | The first browser script assumed Navigation was the default owned target, but the retained sort correctly selects the earlier Trail Safety workshop. AI corrected the script to select the intended owned target before asserting its count. The rerun passes all seven flows; this was a QA target assumption, not an ownership/count defect. |
| L4-F05 | Confirmed inherited form warning: Session State and widget arguments supplied competing defaults after reset/restore. Corrected in app.py by using the existing eight-key defaults as the single initialisation/restoration source and value=None on date/time/capacity widgets. Two new warning-enabled tests fail before and pass after the fix. Existing form regressions pass, and a fresh browser/server log confirms no warning, with correct retained inputs/reset/identity/records/counters. No logging suppression. Closed technically; personal H06 remains pending. |
| L4-F06 | Oracle gap, not a genuine product defect: a private copy grouping personal history at workshop end passed all 221 old cases. Add S-1/S/S+1 checks on the actual table's section placement, ID/status and complete unchanged state. The faulty copy now fails at S/S+1; genuine source passes. Closed by stronger tests; no history rule or production logic change. |
| L4-F07 | Oracle gap, not a genuine product defect: a private copy adopting rejected Book candidates passed all 221 old cases because normal refusals return the original state. Add FORBIDDEN/unrecognised-result injection with a distinct candidate and assert exact original object/state/counters plus no success. Both new checks detect the faulty copy; genuine explicit-OK code passes unchanged. Closed by stronger tests. |
| L4-F08 | Explicitly requested refinement to the accepted L3 HF-02 UI behaviour: shared values/errors/feedback could mix across organisers. Correct app.py with one per-ID form-state map and a visible-form owner marker; scope failure/success/reset to the selected actor. Add 10 failing-before/passing-after cases, declare the two necessary regression adaptations, retain all 228 prior cases and preserve business ownership/counters. Technical verification is recorded above; personal acceptance remains PENDING. |


Browser flow: public Workshops -> Xingjian full/duplicate refusals -> Sam successful Book -> My Bookings/history -> identity switch -> Rui Yan's actual Navigation roster -> retained failed/corrected creation -> independent new page -> mobile view. Screenshots and temporary scripts stay outside the delivery. The personal page is independent of AI test sessions.

The primary preview's historical log is preserved; an older F05 line predates this correction. The new, warning-enabled process at port 8515 verifies the patched restore/reset without relying on Streamlit's already-shown flag. That temporary QA process was stopped after verification; port 8514 remains the human-check service.

These are actual development/review observations, not invented student findings. Any later browser/CI issue must be recorded before delivery. No unresolved technical issue is silently marked closed by a test count alone.

## Risk controls and residual limits

| Risk | L4 control/evidence and remaining decision |
|---|---|
| R-01 | Capacity/active uniqueness and latest serial state tested through real Book; original counters/records checked. Shared/concurrent storage remains excluded. Human H02/H03 pending. |
| R-03 | Business role rejection, selected-ID filtering, no arbitrary other-user read target; role menus remain independent. Equal display names tested. This is not authentication and uses fictional data. Human H05 pending. |
| R-04 | Independent candidate collections, original-state preservation, refresh/switch checks and factory isolation. Reload/new-session/restart loss remains an explicit prototype limit, not recovery. H06 pending. |
| R-05 | Strict C-1/C/C+1/S boundaries, UTC-equivalent instants and fresh decision-clock wiring. Cancellation/waitlist deadline paths await later loops. H04 pending. |
| R-06/R-07 | Bounded task, unchanged rules/configuration, retained ASTs/177 cases, new independent oracles, explicit AI correction log and pending personal decision. Human H01/H07 must judge evidence and understanding. |
| R-08 | Clear times/meeting point/status/history and session/identity limits. No notification or attendance guarantee. R-08 remains VALIDATION_PENDING, including promotion shortly before C in V1.1. L4 UI checks cannot close it. |
| R-02 | No waitlist algorithm in L4; FIFO/promotion/withdrawal control evidence remains future CR-01 work. |

The author owns final risk dispositions. No new human-approved residual rating, specialist advice, release suitability or acceptance is fabricated.

### Carry-forward L3 human feedback

| Feedback | L4 treatment |
|---|---|
| HF-01: open window can coexist with full capacity | Preserve separate time/capacity meanings; the open caption now directs attention to counts. Full Book explicitly returns FULL. This wording adaptation does not add a waitlist or change capacity/time rules. Personal L4 wording review pending. |
| HF-02: rejected draft can cross fictional roles | Historical L3 acceptance is retained unchanged. The explicit F08 request now isolates values/errors/feedback by organiser ID in current L4. Same-owner restoration and owner-only success reset replace cross-organiser reuse. Fictional-data/no-authentication limits remain. |
| HF-03: ownership is enforced in business code | Keep actual-owner organiser roster checks; add independent participant role checks and actor-ID personal reads. Cancellation ownership remains L5 work. |

## Human acceptance checklist

These are planned author checks. None is completed by AI or by historical L3 acceptance. Use the local preview; high-risk boundary cases can be inspected/re-executed with the supplied pytest names without adding a user clock editor.

- [ ] **H01 - Candidate and evidence.** Confirm the L4 branch/code identity and current single-job Actions result. Inspect the cumulative nine-file L4 change and this eight-file corrective patch, retained test functions, mapping and findings. Confirm L0-L3 records are unchanged and the ZIP is local-only.
- [ ] **H02 - Booking and own history.** In a fresh L4 session, select Sam and book Outdoor Navigation Basics. Expect one new CONFIRMED registration-5, four confirmed records overall and the original CANCELLED registration-4 retained. My Bookings must show only Sam's current/history IDs. Refresh/navigation must not add another row. Inspect Rui Yan's Navigation roster for Sam plus Xingjian.
- [ ] **H03 - Capacity and duplicates.** As Xingjian, a fresh Navigation request returns DUPLICATE_ACTIVE; a Photography request returns FULL, with no waitlist/record/counter change. Inspect or run the serial last-place and rebooking tests to verify latest-state use, one allocation and new-ID history retention. These are serial checks, not a concurrency claim.
- [ ] **H04 - Time and denied-state safety.** Inspect S/C/zone and disabled locked/started controls. Inspect/re-execute the strict-cutoff and stale-submission tests: C-1 may succeed, C/C+1/S/after S reject with spare capacity. The actual Book must receive fresh trusted time. Check every refusal preserves records/counters and no success appears on failure.
- [ ] **H05 - Roles and personal filtering.** No identity/organisers see no Book controls; participants see no Organiser menu. Switch Sam/Xingjian and inspect actual own record IDs. Inspect direct business denials, forged actor checks and stored-owner roster enforcement; menu hiding alone is insufficient. Explain that freely selecting another demo identity remains possible.
- [ ] **H06 - Regression and session limits.** Check F08: Rui fails, Alex sees a clean form, Alex fails differently, Rui restores his own failure, Rui succeeds and Alex still restores his own failure; repeat success as Alex. Check same-owner public/participant/cleared round trips and unchanged failure-state counters. Recheck F05 with corrected success/reset to all eight defaults; inspect warning-enabled test and fresh-server evidence. Check selected identity/draft preservation, owned rosters, refresh and role/page reset. A new browser session starts independent demo data; reload/restart may reset it. Use fictional data. Inspect/re-execute the full regression suite as appropriate and record what you actually ran.
- [ ] **H07 - Human judgement and AI disclosure.** Explain the Demo reuse/project-specific rules, two new domain functions, pure state contract and key test oracles. Review AI assumptions/corrections, proposed risk triage, F05 closure, F08 versus historical HF-02, the two declared regression adaptations, the isolated oracle challenges, HF-01-HF-03 and residual R-08/session/security limits. Record actual feedback/edits/rejected suggestions, risk rationale and reviewer/date, then choose ACCEPT_LOOP, CHANGES_REQUIRED or suitable escalation.

Example commands from the L4 repository root, using an existing Python environment:

```powershell
python -m pytest test_booking.py -q
python -m pytest test_booking.py -k "l4_booking_uses_strict_cutoff or l4_stale_booking or l4_serial_last_place" -v
```

Actual personal executions/observations: **PENDING**.
Human reviewer/date: **PENDING**.
Residual-risk decision and rationale: **PENDING**.
Human decision: **PENDING**.

## Exit gate

The technical candidate must have passing current checks, accurate traceability/provenance, resolved or explicitly dispositioned findings and consistent local/GitHub/archive contents. The author must complete the relevant personal checks and supply an explicit candidate-specific ACCEPT_LOOP. AI then records that declaration separately from its own runs. L5 does not start from a green CI run or this delivery; it requires later authorisation. No PR/main merge/release is included.
