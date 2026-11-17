# L4 Work and Human Review

**Current state: HUMAN_REVIEW_PENDING. Human decision: PENDING. H01-H07: unchecked. L5: NOT_STARTED.**

## Intake and preserved scope

On 17 November 2026, the author explicitly requested L4 from accepted L3/GitHub: participant booking and personal records/history; capacity, duplicate-active, 24-hour and permission rules; L4_develop; retained simple architecture, single-job Actions and L1-L3 regressions; English files, local-only ZIP, live preview and a stop for ACCEPT_LOOP. This instruction supersedes the earlier L4 hold, but supplies no L4 personal acceptance.

Base: [accepted L3 74f9281f420755a42141d9792c023cec5d53bf34](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/74f9281f420755a42141d9792c023cec5d53bf34). Its author-approved candidate, UI/H01-H07 declaration and HF-01-HF-03 remain unchanged in the historical L3 review. Executor: Codex assistant. Records use the supplied client date, 17 November 2026; workshop time display remains Asia/Singapore. No precise personal execution time is inferred.

Changed files: app.py, booking.py, test_booking.py, README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md and this new review. The other twelve files, including workflow, dependency inputs/locks, configuration and four historical reviews, retain their L3 bytes. Accepted local L0-L3 folders/archives and original tracked files are protected separately.

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

## Verification results

Actual executor is AI/local tooling or GitHub Actions as identified below. No result in this section is the author's personal execution.

| Check | Current evidence |
|---|---|
| Test-first L4 checks | Before implementation: 41 failed, 3 passed, 177 deselected. The passing three were absence-of-participant-controls checks already true in L3. Failures concerned missing L4 API/UI. |
| Full local suite | 221 passed, zero failures/skips, Python 3.12.14. The 177 retained parameter cases remain; 44 new cases in 23 functions make 81 test functions. |
| Retained-test comparison | All 58 pre-existing test-function ASTs and parameter definitions match L3. Only the shared My Bookings placeholder message oracle changes to implemented content. |
| Static/installation checks | Ruff check, Ruff format --check, Bandit and pip check all passed. No dependency or workflow change. Hosted audits are recorded separately below. |
| Real browser | PASS: seven observed flows at http://127.0.0.1:8514, Chrome via existing bundled Playwright, desktop 1440x1100/1300 and mobile 390x844. Correct title/URL, nonblank content, no framework exception, zero browser console warnings/errors and page errors. Browser plugin not available; no new dependency. See the inherited server-log warning in L4-F05. |
| Hosted Actions | PASS: [run 44071187695](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44071187695), job 133997683150, tested code candidate eeaeb51d875a24527f37f7892f815f2fba5aedcd. Collected 221; 221 passed in 29.56s. All 18 job steps succeeded, including isolated runtime imports and complete audits of 34 runtime/71 development pins, with no known vulnerabilities or omitted packages. |
| Delivery integrity | The 21-file prepared GitHub tree matches all local blobs; twelve retained files match L3 byte for byte. Personal archive/export verification compares all 21 raw file contents and CRC, excludes private tools/reports/environments and confirms no tracked ZIP. All 94 protected prior files/archive remain unchanged. The final delivery is checked again after the records-only update. |

Review branch: [codex/l4-bookings](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/tree/codex/l4-bookings). The code candidate above includes the implementation and tests. A subsequent records-only update adds these completed results without changing code/tests/workflow/locks; current branch Actions must also pass. Quality artifacts expire after 14 days; they are distinct from the personal source ZIP.

Coverage is diagnostic. Test identities, clocks and injected failures are fixtures, not hidden deployed user controls. I01/I02 prove serial same-session ordering, not a concurrent race. I05/I06/I08/I09/I10 are covered only for implemented operations/observed lifecycle; later cancellation/waitlist paths remain planned. Browser smoke checks are not VAL/R-08 user validation.

## Review findings and dispositions

| ID | Finding, correction and current disposition |
|---|---|
| L4-F01 | A test insertion initially displaced two retained metric assertions into a new test. The first implementation run was 43/44 for new cases and exposed the misplaced fixture assumption. AI restored both assertions to their original regression function, moved all new functions to the end, then compared retained ASTs. No original assertion/parameter is removed; all 221 cases pass. Closed technical correction. |
| L4-F02 | An old My Bookings message promised a future feature. AI replaced the shared UI/test placeholder oracle with the implemented personal-view message and added assertions on actual registration IDs/statuses for both identities. Historical test-function bodies remain unchanged. Closed adaptation. |
| L4-F03 | The initial formatted check found whitespace introduced when relocating tests. AI ran the existing formatter. This affects layout only, with a subsequent format check required; no extra test helper/framework is delivered. Closed by final formatting verification. |
| L4-F04 | The first browser script assumed Navigation was the default owned target, but the retained sort correctly selects the earlier Trail Safety workshop. AI corrected the script to select the intended owned target before asserting its count. The rerun passes all seven flows; this was a QA target assumption, not an ownership/count defect. |
| L4-F05 | A fresh server logged the inherited L3 creation-widget warning after targeted form reset: new_start_date has both a widget default and a Session State value. There was no framework exception, browser console warning, record loss or failed reset. The accepted creation code is retained; this non-blocking initialisation-log warning is disclosed for human disposition rather than hidden by logging configuration or an unrelated form rewrite. |

Browser flow: public Workshops -> Xingjian full/duplicate refusals -> Sam successful Book -> My Bookings/history -> identity switch -> Rui Yan's actual Navigation roster -> retained failed/corrected creation -> independent new page -> mobile view. Screenshots and temporary scripts stay outside the delivery. The personal page is independent of AI test sessions.

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
| HF-02: rejected draft can cross fictional roles | Preserve the accepted draft lifecycle; retain fictional-data warning. Booking tests confirm the draft/identity survive successful booking. No confidentiality claim is added. |
| HF-03: ownership is enforced in business code | Keep actual-owner organiser roster checks; add independent participant role checks and actor-ID personal reads. Cancellation ownership remains L5 work. |

## Human acceptance checklist

These are planned author checks. None is completed by AI or by historical L3 acceptance. Use the local preview; high-risk boundary cases can be inspected/re-executed with the supplied pytest names without adding a user clock editor.

- [ ] **H01 - Candidate and evidence.** Confirm the L4 branch/code identity and current single-job Actions result. Inspect the actual nine changed files, retained test functions, mapping and findings. Confirm L0-L3 records are unchanged and the ZIP is local-only.
- [ ] **H02 - Booking and own history.** In a fresh L4 session, select Sam and book Outdoor Navigation Basics. Expect one new CONFIRMED registration-5, four confirmed records overall and the original CANCELLED registration-4 retained. My Bookings must show only Sam's current/history IDs. Refresh/navigation must not add another row. Inspect Rui Yan's Navigation roster for Sam plus Xingjian.
- [ ] **H03 - Capacity and duplicates.** As Xingjian, a fresh Navigation request returns DUPLICATE_ACTIVE; a Photography request returns FULL, with no waitlist/record/counter change. Inspect or run the serial last-place and rebooking tests to verify latest-state use, one allocation and new-ID history retention. These are serial checks, not a concurrency claim.
- [ ] **H04 - Time and denied-state safety.** Inspect S/C/zone and disabled locked/started controls. Inspect/re-execute the strict-cutoff and stale-submission tests: C-1 may succeed, C/C+1/S/after S reject with spare capacity. The actual Book must receive fresh trusted time. Check every refusal preserves records/counters and no success appears on failure.
- [ ] **H05 - Roles and personal filtering.** No identity/organisers see no Book controls; participants see no Organiser menu. Switch Sam/Xingjian and inspect actual own record IDs. Inspect direct business denials, forged actor checks and stored-owner roster enforcement; menu hiding alone is insufficient. Explain that freely selecting another demo identity remains possible.
- [ ] **H06 - Regression and session limits.** Recheck failed creation input/error retention, corrected success/reset, selected identity/draft preservation, owned rosters, refresh and role/page reset. A new browser session starts independent demo data; reload/restart may reset it. Use fictional data. Inspect/re-execute the full regression suite as appropriate and record what you actually ran.
- [ ] **H07 - Human judgement and AI disclosure.** Explain the Demo reuse/project-specific rules, two new domain functions, pure state contract and key test oracles. Review AI assumptions/corrections, HF-01-HF-03 and residual R-08/session/security limits. Record actual feedback/edits/rejected suggestions, risk rationale and reviewer/date, then choose ACCEPT_LOOP, CHANGES_REQUIRED or suitable escalation.

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
