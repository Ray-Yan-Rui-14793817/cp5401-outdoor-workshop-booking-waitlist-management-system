# L5 Work and Human Review

**Current: L5 ACCEPT_LOOP. Human decision: ACCEPT_LOOP. Updated UI and H01-H07: COMPLETE by author declaration, 18 November 2026. L6: NOT_STARTED.**

## Current human acceptance

On 18 November 2026 (UTC+08:00), the project author explicitly declared completion of the updated L5 UI checks and H01-H07 human acceptance, supplied ACCEPT_LOOP and requested updates to L5/GitHub, the personal local-only ZIP and AI/human records. The author also requested closure of the web service and explicitly prohibited entry into L6 at this time.

Accepted candidate: [b597babb5a648d3a576edf5b9c26bb2e7304d45c](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/b597babb5a648d3a576edf5b9c26bb2e7304d45c) on codex/l5-cancellation, the immediately preceding reviewed delivery. Review tests came from 7f58cc40007de29e637e2b2174f53fb01733d492; app.py/booking.py were unchanged by that review. The accepted candidate's [Actions run 44128607418](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44128607418), job 134199163116, passed 306 tests in 71.24s with one job/all 18 steps successful. This existing automated result is separate from the author's personal UI/H01-H07 declaration. Any later acceptance-record commit has the same source/tests/workflow and its own Actions run.

English translation of the Chinese declaration: "I have completed the updated L5 UI checks and H01-H07 human acceptance. ACCEPT_LOOP. Update L5, GitHub, the local ZIP and AI/human acceptance records. Do not upload the ZIP to GitHub, close the web service, and do not enter L6 yet." This is a translation, not a verbatim English quotation.

Earlier pending-state statements below describe review before this declaration. They are retained as history; this entry and the completed checklist are the current human decision. No individual personal command log, exact check timestamp, additional code edit or independent 306-case CI-verification statement is inferred.

### Author feedback and dispositions

The feedback column is transcribed verbatim from the author's English message. These are actual human observations, separate from AI technical findings or AI-executed tests/browser/fault evidence.

| ID | Author feedback | Recorded disposition and scope |
|---|---|---|
| L5-HF-01 | The candidate is traceable and consistent. | ACCEPTED_CANDIDATE_TRACEABILITY. Bind acceptance to b597babb5a648d3a576edf5b9c26bb2e7304d45c and preserve the reviewed code/evidence identity and local/GitHub/archive consistency. |
| L5-HF-02 | The new multi-attendee tests strengthen the cancellation oracle. A workshop with only one confirmed participant would not reveal an implementation that incorrectly cancels every participant. | ACCEPTED_ORACLE_IMPROVEMENT. Preserve L5-10/L5-F05 fixtures and exact one-target/count/history assertions. This recognises the review's test gap and correction, not a genuine runtime cancel-all defect. |
| L5-HF-03 | Active-cutoff tests and cancelled-repeat tests use different fixtures. This prevents an idempotent no-op from being mistaken for evidence that the effective cancellation deadline works. | ACCEPTED_FIXTURE_DISTINCTION. Keep B15 active boundary fixtures separate from B16 owned-cancelled no-ops; retain strict effective cutoff and ALREADY_CANCELLED repeat semantics. |
| L5-HF-04 | The ownership model supports the declared classroom prototype. Because identities are freely selectable, this is not real authentication or protection against deliberate identity switching. | ACCEPTED_CLASSROOM_SCOPE_LIMIT. Retain fictional-data-only use, stable-ID ownership checks and disclosure. No authentication, confidentiality against identity switching or production-security approval is claimed. |
| L5-HF-05 | The strongest improvement is the quality of test oracles, not merely the increase from 298 to 306 cases. The additional tests check properties that the original suite could miss despite high coverage. | ACCEPTED_EVIDENCE_JUDGEMENT. Preserve exact targeting, late-construction and clicked-target checks/fault evidence. Test count and 99% diagnostic coverage are not correctness, grade or human-approval substitutes. |

### Acceptance-record maintenance and preview closure

This update changes six existing English Markdown documents: README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md and this record. No file is added. Application code, all 306 test cases, canonical rules/risks/scenarios, locks/configuration and the single-job workflow retain the accepted candidate's bytes. AI transcribes the author's actual decision/feedback rather than approving on the author's behalf. Accepted L0-L4 files, including original L3 HF-02 and all L4 feedback, remain unchanged.

The identified L5 preview process at http://127.0.0.1:8516 was stopped after checking its saved launch identity, PID/path/start time and listener. Port 8516 is released and its health endpoint is unreachable; isolated QA port 8517 remains closed. Restart instructions remain in README; session data has no persistence/recovery guarantee. Earlier-loop services are separate. The local L5_develop.zip contains the same 22 source files at archive root, including .github, and is checked by raw contents/CRC against local/GitHub delivery. No personal project ZIP is committed/uploaded or attached to a release; normal Actions quality-report artifacts remain separate.

## Initial L5 intake and baseline (historical)

The author explicitly requested L5 after accepted L4: participants cancel their own confirmed bookings, release capacity and retain history; enforce strict 24-hour, permission and repeat rules; keep the simple architecture, single-job Actions and L1-L4 regressions; update English delivery/AI/human records, provide a local-only ZIP and live preview, then stop for ACCEPT_LOOP. This supersedes the earlier L5 hold for this bounded implementation only.

Base: [accepted L4/GitHub 2f2504acff79317c20760971acae2965ee98a1fb](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2f2504acff79317c20760971acae2965ee98a1fb). Its underlying accepted candidate, UI/H01-H07, three human feedback items and AI evidence attribution remain byte-identical in [L4 history](L4-human-review.md#current-human-acceptance). The existing 21-file L5 starting folder and private metadata were checked against that GitHub tree before implementation. No pre-existing divergent user change was overwritten.

Executor: Codex assistant/local tools or GitHub Actions as labelled. Intake/local work began under the client date 17 November 2026; hosted verification is recorded on 18 November 2026 following the updated client context (both UTC+08:00). Workshop display is Asia/Singapore. No personal execution timestamp, feedback, risk rating, code edit or acceptance is supplied for L5.

## Deep-review intake (historical technical stage)

Review base: [7c3081f54c3eb952835b07bca24467c9e7dc02c6](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/7c3081f54c3eb952835b07bca24467c9e7dc02c6), codex/l5-cancellation, 18 November 2026 (UTC+08:00). The author requests independent source/rubric/lecture review of cancellation/history, time/no-op order, permissions, complete State/IDs, test oracles/failure injection, architecture/quality and redundancy, with fixes and a stop at L5. No personal L5 execution or ACCEPT_LOOP is supplied.

This review changes only test_booking.py as executable source, appending eight cases in three functions. Six existing Markdown documents record current evidence/mapping/findings. Seven existing files change; no new delivery file. app.py/booking.py already satisfy the reviewed properties and remain byte-identical to the base. All 298 prior cases/112 test function ASTs and decorators, canonical 39 definition rows/51 scenario rows, workflow/locks/configuration, five historical reviews and 116 protected earlier files remain unchanged. Delivery stays 22 files/11 Markdown documents. Initial implementation counts/changed-file descriptions below are historical, not relabelled as this corrective patch.

Review finding summary: three test-oracle gaps are repaired (L5-F05-F07 below). Deliberately faulty copies passed the old suite; none was introduced into the genuine runtime. Proposed correction risk is Medium for generated-test assumptions; original allocation/owner behaviour retains the earlier High review-depth recommendation. Human risk judgement remains PENDING.

### Deep-review verification

| Check | Actual result and limit |
|---|---|
| Multi-attendee oracle | Private cancel-all-confirmed fault passed all 298 old cases in 43.69s. Four new cases cancel either participant's target in either row order with two same-workshop confirmations, cancelled history and a second workshop. Fault fails all four; genuine source changes only the exact row/count and preserves everything else. |
| Late construction oracle | Private temporary-input-mutation fault passed all 298 old cases in 43.11s. New final-DemoState construction failures through domain/UI reject it with two failures, while genuine source keeps original State/list identity/records/counters and publishes no success. Earlier Registration-construction injection remains unchanged. |
| Clicked-target oracle | Private UI-always-cancels-first fault passed all 298 old cases in 43.60s. Two real-control cases establish Sam owns two eligible confirmations, then click each. Fault passes the first target but fails the second; genuine source cancels only the clicked ID and preserves the other current record/history/counters. |
| Focused genuine tests | Eight passed, 298 deselected, 3.52s. These are new review tests against an already-correct runtime, not production-fix red/green claims. |
| Complete local regression | 306 passed in 62.74s, zero failures/skips, Python 3.12.14; 115 test functions. All 298 previous JUnit identities and 112 function ASTs/decorators remain unchanged, including 250 L1-L4 cases and 48 original L5 cases. |
| Static/coverage | Ruff, format check, Bandit and pip check PASS. Coverage: 200 statements, one miss, 70 branches/one partial, 99% diagnostic; the unexecuted line is the existing demo-fixture error guard. High coverage was present when faulty copies passed, so it is not correctness/grade proof. |
| Fresh browser | PASS: 12 Chrome flows through native controls, 1440x1400 and 390x844, isolated fresh service 8517. Correct URL/title/nonblank page, no framework overlay/exception, zero browser warning/error/page error. Screenshots inspected: only clicked registration-5 cancels while registration-2 remains CONFIRMED; later History retains 2/4/5 and Alex's replacement roster has registration-6/Xingjian. Rui draft/errors, locked controls, Refresh and independent sessions are preserved. Fresh server has no duplicate-default warning/traceback. QA 8517 stopped; human preview 8516 retained/healthy. Browser plugin unavailable; existing bundled Playwright used. |
| Hosted review Actions | PASS: [run 44127697367](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44127697367), job 134195886385, tested review candidate 7f58cc40007de29e637e2b2174f53fb01733d492. One quality-checks job/all 18 steps succeeded; 306 passed in 66.80s on Python 3.12.14. Ruff/format, Bandit, pip check, isolated runtime imports and complete audits of all 34 runtime/71 development pins passed, with no known vulnerabilities or omissions. Coverage remains 99% diagnostic. Reports expire after 14 days. This evidence-only update records those results; its own current-head Actions must also pass. Initial 298-case runs below remain historical. |
| Delivery/baseline integrity | All 22 raw local files match the prepared GitHub tree and archive/CRC; final comparison is repeated after this evidence-only update. All 116 protected earlier files, 39 canonical definition rows, 51 scenarios and accepted history remain unchanged. Locks/workflow are unchanged; no private QA tool or personal project ZIP is uploaded. |

### Review of B11-B17, I05 and cancellation I10

| Scenario | Reviewed evidence and conclusion |
|---|---|
| B11 | One effective own pre-C cancellation changes the same ID to CANCELLED, keeps created_at/history, changes updated_at and releases exactly one place. New multi-attendee cases prevent losing other confirmations; original complete-candidate/capacity-boundary cases remain. VERIFIED_FOR_TESTED_SCOPE. |
| B12 | Valid other participant targets a stored active/cancelled ID with an otherwise valid clock: FORBIDDEN and complete original state. Equal display names do not confer ownership. VERIFIED_FOR_TESTED_SCOPE. |
| B13 | Retained L3 valid-participant creation/roster denials, actual-workshop lookup and non-owner organiser roster denial remain in the full regressions, with timing/input causes isolated or explicitly labelled as precedence tests. Cancellation/rebooking updates the authorised roster. No role/ownership policy changes. |
| B14 | Well-formed unknown registration/workshop IDs are tested with otherwise valid actors/time through actual cancellation, Book and roster operations. Expect the corresponding UNKNOWN_REGISTRATION/UNKNOWN_WORKSHOP and exact unchanged State/IDs, without false success. Role/invalid-actor cases are separately mapped to BR-01 and B01/B02/B13. |
| B15 | Fresh active records at C-1/C/C+1/S/S+1, equivalent instants and stale-render/fresh-decision UI checks isolate time as the refusal. Only before C may cancel. VERIFIED_FOR_TESTED_SCOPE. |
| B16 | Owned CANCELLED repeats before/after C/S are ALREADY_CANCELLED with exact original state and zero allocation. Ownership remains checked first; these no-ops are not reused to prove active cutoff rejection. |
| B17 | Actual serial cancel/rebook creates a new ID while retaining cancelled history, and an old-ID repeat cannot release the new place. Retained Book deadline cases reject rebooking at/after C with otherwise valid state. No simultaneous-user claim. |
| I05 | Exact success/refusal/no-op state oracles plus original Registration failure, new final DemoState failure and non-OK candidate UI injections. The design prevents partial in-memory mutation/publication; it does not claim database transactions, durable rollback or recovery. Promotion-failure paths remain V1.1 work. |
| Cancellation I10 | Actual UI renders open and passes fresh trusted C/C+1 to the operation, which rejects without state/counter changes or false success. Display disabling alone is not the enforcement. Join/promotion/withdrawal parts remain later scope. |

### Architecture, redundancy and defensive checks

The responsibilities remain appropriate: app.py renders selected-identity views and adopts only OK; booking.py enforces actual owner/time/state contracts; tests assert independently specified results. No runtime abstraction or file is added. Target existence and aware-clock checks handle actual business boundaries; UI role/menu filtering and business permission checks guard different entry points. Copied mutable lists are required by QR-02's independent complete-state contract; frozen rows can be shared safely. They are not speculative defensive state repair.

No unnecessary service layer, general validator/repair framework, broad exception swallowing, warning suppression, dependency or unrelated refactor is warranted by the observed paths. Existing UNKNOWN_WORKSHOP handling is a small explicit referenced-target guard, tested as an inconsistent fixture, not a new deletion workflow. The genuine runtime is retained; the patch fixes missing evidence rather than increasing production complexity.

### Assessment, HD rubric and lecture alignment

The four supplied original PDFs and Week1-9 archive match the earlier verified hashes. Relevant assessment pages were freshly extracted; rubric pages 10/12/13 were also rendered and inspected. The two supplied S02 transcript copies have identical normalised text and are not independent corroboration. These are supplied transcriptions, not an independent audio verification. Relevant Week4-9 supplementary slides were inspected directly from the verified archive; originals are not redistributed.

| Assessment criterion | Evidence at L5 and remaining work |
|---|---|
| Requirements/quality planning, 15%; S01 pp.3/9-10 | Clear accepted roles/FR/BR/QR/risk targets retained; B/I mapping and three independently challenged oracles are explicit. Human H01/H07 and R-08 suitability are still pending. |
| Functional app/deployment, 15%; S01 pp.3/10 | Booking/cancellation/history/owned rosters work in the local preview and test scenarios. Assessed hosted deployment and release validation are NOT COMPLETE at this loop. |
| V&V/testing, 20%; S01 pp.3-4/10-11 | 306 retained/new tests, boundary/failure/security checks, explicit evidence limitations and three detected false-green faults support verification. Intended-user validation and personal acceptance remain separate; pass count/99% coverage cannot close them. |
| Change/regression/release, 20%; S01 pp.4/12 | Focused branch, original tests, findings/corrections and baseline comparisons support controlled development. L5 is pre-release baseline work, not the assessed meaningful CR-01. Working V1.0, change impact/Issue/PR, justified merge and V1.1 release remain future requirements. |
| GitHub/CI, 15%; S01 pp.5/9/12 | Progressive code/evidence identities and one unchanged job with tests/static/security/full dependency audits support current work. Required Issue/PR/release lifecycle is not complete and must be demonstrated later. |
| Presentation/defence/judgement, 15%; S01 pp.8/13 | Exact AI task/files/assumptions, genuine gaps/fixes and planned human checks support explanation. Actual personal understanding, risk classification, feedback, slides and oral defence cannot be supplied by AI or inferred from CI. |

S02 English pp.2/8-9 permits explained adaptation of the three-file Demo to a different realistic problem and stresses small focused changes/human oversight. S03 English pp.2-4/6-7 stresses risk-based ownership/routing, concrete AI disclosure, scans/tests/findings and audit evidence. S01 p.4 permits the student's justified own decision unless the teaching team requires an external reviewer; organisational lecture examples are not a blanket instruction to invent an external approval here. The test-only patch remains pending the author's judgement; no approval or escalation outcome is fabricated.

Lecture traceability: Week4 supplementary slides 4/18/22 distinguish lifecycle V&V and recorded decisions; Week5 slides 4/9/12 support test levels and requirement oracles; Week6 slides 11/14/17/20 support bounded intake, prompt-to-diff traceability, assumptions and risk judgement; Week7 slides 7/12/14 support strong observable assertions/regression/actual cross-owner checks; Week8 slides 26 (labelled 20)/28 (labelled 22) support proportionate gates and tool-evidence triage; Week9 slides 2/5/19 require human code understanding, focused changes and defensible evidence. Teaching overlap/waitlist examples do not change this project's accepted FULL/ID/cutoff rules.

Technical conclusion: the reviewed genuine paths conform to the accepted cancellation contracts; the three oracle gaps are corrected. This supports the current loop's process/evidence, not a claim that the complete assessment or HD grade is achieved. L5 H01-H07 and ACCEPT_LOOP remain PENDING; L6 is NOT_STARTED.

## Initial implementation scope (historical)

| File | Actual change |
|---|---|
| app.py | My Bookings cancellation buttons for own confirmed records; disabled closure states, fresh operation clock, actor-scoped success and explicit-OK state adoption; L5 preview/history text. |
| booking.py | One new pure cancel_registration operation over existing models, with stored target ownership, no-op repeats, strict cutoff and complete non-mutating candidate. |
| test_booking.py | Append 48 L5 cases in 20 functions; all 250 L1-L4 cases and all 92 prior function ASTs/decorators remain unchanged. Module description updated. |
| README.md, requirements.md, docs/test-plan.md, docs/demo-reuse.md, docs/ai-use.md | Current stage, exact mapping, provenance, AI contribution, evidence limits and pending human gate. Canonical definitions are unchanged. |
| docs/reviews/L5-human-review.md | This new loop record, real observations/results and unchecked checklist. |

Eight existing files change and one review is added: 22 delivery files/11 Markdown documents. Thirteen retained files, including the single-job workflow, dependency inputs/locks, configuration and five historical reviews, keep their base bytes. All 116 protected earlier files/archives and the original tracked working copy are preserved. Private QA tools/reports/screenshots are outside the delivery; no source.md or auxiliary framework is added.

The architecture remains app.py -> booking.py -> dataclasses/lists. The new function uses the existing permission helper, aware-time policy and dataclass replacement/copy pattern. UI checks serve usability; business checks enforce selected-role/owner rules independently. No generic repair layer, broad exception catch, real authentication, shared cache or durable/concurrent database is introduced.

## Contract and independent expectations

C=S minus 24 elapsed hours. Every negative test uses valid unrelated preconditions unless it explicitly exercises precedence, an inconsistent fixture or an injected internal boundary.

| Scenario | Expected outcome and complete-state effect |
|---|---|
| Valid owner, active confirmation, t<C | OK. Change that same record to CANCELLED and updated_at to UTC decision time. Keep ID/created_at/owner/workshop, all other rows and both counters; confirmed count decreases by exactly one. Complete candidate has independent lists; input unchanged. |
| Active confirmation at C/C+1/S/after S | REGISTRATION_CLOSED. No record, timestamp, counter, count or session-state replacement. Spare capacity cannot reopen cancellation. |
| Repeat own CANCELLED ID before/after C/S | ALREADY_CANCELLED, exact original object/state/counters, no additional place release or success claim. It is a permitted no-op, not effective late cancellation. |
| Valid other participant targets an owned active/cancelled ID | FORBIDDEN. Use the actual stored participant ID, even if names match. No mutation or status-dependent permission bypass. |
| Missing/unknown/forged actor or organiser | Existing INVALID_ACTOR/FORBIDDEN role outcome with unchanged state. Hidden controls alone are insufficient. |
| Unknown registration | UNKNOWN_REGISTRATION without mutation. |
| Unusable application clock for an active record | INVALID_INPUT without mutation. There is no user-facing clock editor. |
| Stored registration references no workshop | UNKNOWN_WORKSHOP without mutation in a labelled inconsistent internal fixture; no workshop-deletion feature is introduced. |
| Constructing cancellation raises an exception | Propagate the exception; original records/counters remain untouched. UI does not adopt a partial state or report success. |
| Subsequent pre-C Book after cancellation | New CONFIRMED ID, old CANCELLED row/history retained. Repeating the old cancellation cannot release this new place. At most capacity confirmations remain in tested serial actions. |

Check selected role/target ownership before owned-repeat status; recognise the owned repeat before validating an effective time change. An active cancellation obtains the workshop/cutoff from the stored registration and receives fresh server_now at the actual business call. No row deletion, automatic waiting/promotion, overlap prohibition or emergency cutoff override is added.

My Bookings continues to split own upcoming confirmed records and retained history without changing stored statuses for time passage. Only confirmed records have cancellation controls; locked/started ones are disabled. CANCELLED history has no repeat button. ALREADY_CANCELLED is an informational no-op, whereas only OK replaces business state. All organiser form namespaces, selected identity/current page and unrelated session values remain.

## Requirements, risks and teaching method

This implements FR-04's V1.0 cancellation and strengthens FR-05 history, alongside FR-01/03/07. BR-01/03/04/06/07/13/16 and QR-01 through QR-04 define the permission, time, capacity, state and session contracts. [L5 test mapping](../test-plan.md#l5-implemented-test-mapping) links exact functions to B11/B12/B15/B16/B17 and cancellation portions of I05/I06/I08/I09/I10. All 39 canonical requirement/rule/quality/risk rows and 51 scenario rows retain their accepted definitions. Waitlist/promotion parts remain future CR-01 work.

The accepted source mapping in [Demo reuse](../demo-reuse.md#references) supports bounded realistic scope, independent requirement-based testing, AI disclosure, human ownership and evidence-based stage exits. L5 applies that method; it does not claim a fresh audio verification or repeat the source Demo's pass history. The Demo supplies separation/session ideas; this project cancels by stable IDs with strict cutoff and retained history rather than deleting rows. No new Demo algorithm is adopted.

L5 is baseline development before V1.0 release, not the assessed waitlist change. Working V1.0, deployment/validation, CR-01 impact/Issue/PR, justified merge/release, final PPTX/submission/defence and full VAL/R-08 remain distinct requirements. This loop's test count, coverage and green CI cannot guarantee an HD grade or provide the author's acceptance.

AI-proposed review depth: High, because seat release, actual-target ownership, no-op precedence and complete state/counter preservation need scrutiny. This is a review proposal, not a human-approved residual rating or specialist approval. The author must judge the evidence/limits in H07.

<a id="verification-evidence"></a>

## Initial implementation verification (historical)

| Check | Actual result and executor |
|---|---|
| Before implementation | AI: 45 new cases failed, three passed, 250 deselected, 7.52s. The three passing non-participant-control cases already held in L4. Initial environment-path failure executed no tests and is not included. |
| Focused implementation run | AI: all 48 L5 cases passed, 250 deselected, 7.32s. |
| Full local regression | AI: 298 passed in 60.15s, zero failures/skips; Python 3.12.14, 112 test functions. All 250 historical case identities and 92 function ASTs/decorators remain. No prior test body/parameter is adapted or weakened. |
| Static/consistency | Ruff check, Ruff format --check, Bandit and pip check PASS. No dependency/configuration/workflow change. Booking branch coverage is 99% diagnostic evidence, with one unexecuted demo-fixture error line; not a completeness/grade threshold. |
| Real browser | AI: PASS, ten observed Chrome flows via existing bundled Playwright because Browser plugin is not available. Desktop 1440x1400/mobile 390x844, URL http://127.0.0.1:8516, correct title/nonblank content, no framework exception/overlay, zero console warning/error or page error. Native controls perform cancellation/history/rebooking/owned-roster updates; exact table contents are independently asserted by AppTest and visually inspected in screenshots. |
| F05/F08 and session checks | All retained warning-enabled and organiser-isolation tests pass. The browser restores Rui's exact eight failed values/errors after Sam cancellation and Xingjian rebooking. The fresh server log has no duplicate-default warning/traceback. Refresh preserves the result; a separate page has three confirmations while the cancelled page has two. Mobile has no page overflow; wide tables retain normal internal scrolling. |
| Hosted Actions | PASS: [run 44120914889](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44120914889), job 134171686125, tested code candidate 65f3990417ebc5fa85a8039e2b3283a401399682 on codex/l5-cancellation. One quality-checks job/all 18 steps succeeded; 298 passed in 36.73s on Python 3.12.14. Runtime-only installation/imports, Ruff/format, pip check, Bandit and complete audits of 34 runtime/71 development pins passed with no known vulnerabilities or omitted packages. Reports expire after 14 days. A later records-only commit adds these results without changing code/tests/workflow; its own current Actions must also pass. L4's 250-case run remains base evidence only. |
| Delivery integrity | Final checks compare all 22 local/GitHub/archive raw files and ZIP CRC, canonical definitions, unchanged historical functions/files and 116 protected earlier files. Personal source ZIP stays local; workflow/locks and five historical reviews retain base bytes. |

The browser interaction sequence was public Workshops -> Rui failed creation draft -> Sam My Bookings -> cancel registration-2 -> History/count decreases -> independent page/Refresh -> Xingjian own locked controls -> Book released Photography place as registration-5 -> Alex owned Photography roster -> Rui draft restoration -> cleared identity -> mobile Sam history. Screenshots show registration-2/4 CANCELLED and the replacement registration-5/Xingjian roster. These are AI executions, not personal user validation or actual human acceptance.

Review branch: [codex/l5-cancellation](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/tree/codex/l5-cancellation). The code candidate and its run identify the executed source; subsequent evidence-only commits do not provide human acceptance. The final branch/ZIP comparison and current-head Actions check are repeated after this record update.

Injected tests at the domain/UI boundaries cover construction/call exceptions and non-OK results with distinct candidate data/counters. They test failure wiring; they do not claim normal domain refusal returns modified state, a valid organiser is genuinely denied creation, or a user can edit trusted time. Serial returned-state sequencing is not a simultaneous-user test.

## Review observations and corrections (technical stage)

The rows preserve the technical findings and then-pending human references. The subsequent UI/H01-H07 completion, feedback and ACCEPT_LOOP are recorded under Current human acceptance above.

| ID | Actual observation and disposition |
|---|---|
| L5-F01 | Initial setup assumed a new private evidence directory and a child .venv. Existing metadata/starting files matched accepted L4 and were verified/reused; the first test invocation addressed no executable and ran no tests. Corrected to the existing parent environment before recording red/green evidence. No dependency install, accepted-file overwrite or product workaround. Closed setup correction. |
| L5-F02 | Repeated cancellation after C/S must be ALREADY_CANCELLED rather than an active time rejection. The implementation follows BR-06's owner-first/no-op-first order; five fresh repeat cases and two actual cancel/rebook chains confirm no extra release or ID change. This is intended behaviour, not a claimed inherited product defect. Human H04 pending. |
| L5-F03 | Only OK may replace UI state. Three distinct-candidate injections and one call-exception check verify the exact prior object/records/counters and no false success; retained F08 state and identity survive the happy path. No broad catch/repair abstraction was needed. Human evidence judgement pending. |
| L5-F04 | Pre-publication checks caught a duplicated old L4 status preamble and locally generated ignored pytest/Ruff caches. Remove the duplicate, clarify the current gate and move only those caches into private evidence after verifying source/destination paths. The final export has exactly 22 files; canonical definitions and historical acceptance files are unchanged. Closed documentation/packaging correction. |
| L5-F05 | Oracle gap: cancelling all confirmed attendees in a workshop passed the old 298 tests because effective-cancellation fixtures had one confirmation there. Four new legitimate multi-attendee/order/owner cases reject the isolated fault and verify exactly one changed ID/count with preserved other workshop/history/counters. Genuine runtime unchanged. Closed technical test correction; human H02/H06/H07 pending. |
| L5-F06 | Oracle gap: temporary input mutation before final State copy passed old tests; the earlier injected failure occurred before that stage. Add two final-DemoState failures through actual domain/UI calls, checking original State/list identity/records/counters and no success. Both reject the fault; genuine runtime unchanged. Closed technical test correction; human evidence judgement pending. |
| L5-F07 | Oracle gap: always cancelling the first owned confirmation passed old tests because actual UI cancellations had one eligible target. Add two real-control cases with registration-2/5 both eligible; the fault fails when the second is clicked. Genuine source changes only the clicked target and retains the other active booking/history/counters. Closed technical test correction; H06/H07 pending. |
| L5-F08 | During this review's documentation draft, B14 was incorrectly described as role/actor denial. Re-read the unchanged canonical scenario: B14 covers unknown workshop/registration targets. Correct the review/test-plan mapping to actual UNKNOWN-outcome tests and keep role/owner checks under their proper definitions. No business/test implementation or canonical definition changes. Closed traceability correction. |

No confirmed rule violation remains in the executed paths. Automated success is bounded evidence, not proof of all possible faults. Later findings must be recorded before acceptance; AI does not fabricate a student edit, rejected suggestion, risk decision or independent personal execution.

## Risk controls and remaining limits

| Risk | L5 control/evidence and pending judgement |
|---|---|
| R-01 | Exact count decrement, fixed IDs/counters, full-workshop release/rebook and repeat-old-ID sequencing. H02/H03 completion declared; simultaneous concurrency remains excluded. |
| R-03 | Business role/actual stored owner checks, same-name denial, own-only controls and hidden menus. H05 completion declared; L5-HF-04 explicitly accepts the freely switchable classroom model without authentication claims. |
| R-04 | Complete candidate/copied lists, preserved cancelled ID/created_at, unchanged other rows/counters, rejection/no-op/exception checks and independent sessions. H02/H06 completion declared; no durability/recovery claim. |
| R-05 | Fresh active C-1/C/C+1/S boundaries, equivalent instants, separate repeat semantics and actual submission-time wiring. H04 completion declared; L5-HF-03 recognises the distinct active/no-op fixtures. No user clock/override. |
| R-06/R-07 | Bounded scope, retained 250 cases, independent exact-state oracles, disclosed internal injections/setup correction and unchanged single-job checks. H01/H07 completion and ACCEPT_LOOP declared; L5-HF-01/02/05 provide actual traceability/oracle-quality judgement without inventing a formal risk rating. |
| R-08 | Explicit cancellation/history/cutoff and temporary fictional-session disclosures. Full suitability/notification/near-C promotion validation remains VALIDATION_PENDING; no waitlist exists in L5. |
| R-02 | No FIFO/promotion in L5. Controls and tests remain future CR-01 scope. |

Carry forward L4-HF-01/02/03 without rewriting their original acceptance: cancellation now follows a new explicit instruction; negative tests isolate causes, serial-only scope remains, and AI browser/fault evidence stays distinct from author-verified prior CI. Original L3 HF-02 remains historical; current F08 isolation is retained.

## AI and human contribution

The author supplied scope/policy and accepted L0-L4. AI implemented the original domain/UI change and 48 tests, then independently reviewed the oracles in this follow-up, appended eight targeted cases, preserved all 298 prior cases/history and kept the genuine runtime unchanged. AI performed the source-based comparison, three controlled faults, local/browser/hosted checks and English delivery/mapping/ZIP updates. Actual changed paths are listed above. The author has now supplied updated UI/H01-H07 completion, ACCEPT_LOOP and five observations listed above. No individual personal command log, additional code edit, separate per-finding decision list, formal risk category or independent 306-case CI-verification statement was provided. GitHub Actions is an automated executor, not an approver.

## Human acceptance checklist

On 18 November 2026 the author explicitly declared updated L5 UI and all H01-H07 complete and supplied ACCEPT_LOOP for b597babb5a648d3a576edf5b9c26bb2e7304d45c. Checkmarks transcribe that declaration; AI/CI execution and earlier-loop acceptance do not supply them. The preserved descriptions identify the presented checks, not an invented personal command/execution log. The preview has now been closed at the author's request.

- [x] **H01 - Candidate and scope.** Verify the L5 branch/code identity/current Actions and inspect the three-file diff, exact test mapping, AI contributions/findings and unchanged accepted L0-L4 history. Confirm the personal ZIP is local-only and L6 has not begun.
- [x] **H02 - Own cancellation and history.** Select Sam -> My Bookings -> cancel registration-2 (Photography). Expect success, total confirmations three to two, no current Sam confirmation, registration-2/4 CANCELLED in History, and no repeat button. Refresh/navigation must not release another place. Inspect the exact-state test for preserved IDs/created_at/other rows and unchanged counters.
- [x] **H03 - Reallocate one released place.** Switch to Xingjian -> Workshops -> Book Photography. Expect new registration-5, total confirmations three and retained Sam history. Alex's Photography roster must contain Xingjian. Inspect actual cancel/rebook/repeat tests to confirm an old cancelled ID cannot release this new place and a further eligible serial Book is FULL.
- [x] **H04 - Strict cutoff and repeat semantics.** Inspect locked Trail Safety controls and fresh active C-1/C/C+1/S/S+1 tests, including a page rendered open but processed at C. Effective cancellation at C must reject without state/counter changes. Separately inspect owned CANCELLED repeats before/after C/S: ALREADY_CANCELLED with no mutation. Do not reuse a cancelled fixture to claim active deadline enforcement.
- [x] **H05 - Permissions and identity.** Compare Sam/Xingjian own controls/history. No identity/organisers have no participant cancellation menu/control. Inspect direct wrong-role, forged-actor and other-owner tests with valid unrelated preconditions, plus equal-name checks. Explain why stored ownership is enforced in booking.py beyond menu hiding, and why demo selection is not real authentication.
- [x] **H06 - Regression, drafts and session limits.** Fail Rui creation, navigate to cancel/rebook as participants, then return to Rui: his latest eight values/errors remain his own. In another fresh session, book Navigation as Sam to obtain two eligible confirmations (registration-2/5), then cancel registration-5 and verify registration-2 remains active and the other Navigation participant is retained. Inspect the new multi-attendee and late final-construction failure cases. Recheck L4-F05 reset/restore and L4-F08 owner-only success reset using retained tests. Check refresh and an independent browser session; explain reload/restart data loss. Inspect or run all 306 regressions and record what you actually executed rather than copying AI results.
- [x] **H07 - Human judgement and next decision.** Explain Demo reuse and project-specific cancellation, exact independent oracles, serial scope, internal injections and AI evidence attribution. Review L5-F01-F08, the three old-suite false-green faults, the corrected B14 mapping, the proposed High base review depth and Medium test-correction risk; record actual findings/edits/rejected suggestions, residual-risk rationale and reviewer/date. Supply candidate-specific ACCEPT_LOOP, CHANGES_REQUIRED or proportionate escalation. Stop at L5; acceptance alone does not start L6.

Example commands from the repository root with an existing Python environment:

```powershell
python -m pytest test_booking.py -q
python -m pytest test_booking.py -k "l5_" -v
python -m pytest test_booking.py -k "l5_effective or l5_owned_cancelled or l5_stale" -v
```

| Current human record | Actual value |
|---|---|
| Reviewer/confirmation date | Project author, identified by the user role in this conversation. Acceptance recorded 18 November 2026 (UTC+08:00). Individual check dates/times were not supplied. |
| Reviewed candidate | b597babb5a648d3a576edf5b9c26bb2e7304d45c on codex/l5-cancellation, the immediately preceding delivery. |
| Personal checks and feedback | Updated L5 UI/H01-H07 completion explicitly declared. L5-HF-01 through L5-HF-05 above are the five supplied observations; no individual command/environment log was provided. |
| Code understanding and independent expectations | Feedback explicitly recognises multi-attendee targeting, separate active/no-op fixtures, selected-identity limitations and the value of precise behavioural assertions beyond case count/coverage. No further step-by-step explanation is invented. |
| Evidence ownership | Existing 306-case CI and recorded browser/controlled-fault runs remain automated/AI evidence. This acceptance message does not supply a personal pytest command or independent 306-case CI-verification statement. |
| Human edits/rejected suggestions/finding assessment | No additional human code edit, rejected suggestion or separate per-finding decision list was supplied. The author explicitly supports the improved oracles and supplied candidate-specific ACCEPT_LOOP. |
| Risk judgement and residual limits | Accept the declared classroom prototype and evidence while acknowledging freely selectable identities do not provide real authentication/deliberate-switch protection. The author distinguishes effective cutoffs from no-op repeats and quality from count/coverage. No separate formal risk category was supplied; earlier AI High/Medium triage remains attributed to AI. Full VAL/R-08 remains pending. |
| Current decision | ACCEPT_LOOP, explicitly supplied by the author and transcribed by AI. |
| Next-loop boundary | L6 NOT_STARTED and explicitly held until a later author instruction. |
| Preview | CLOSED at the author's request; port 8516 released and health endpoint unreachable. |

## Exit gate and delivery

The L5 human loop gate is SATISFIED by the author's explicit candidate-specific ACCEPT_LOOP and updated UI/H01-H07 declaration. This records-only update preserves passing current checks, accurate provenance and matching local/GitHub/archive contents. Personal feedback and AI/CI execution remain separately attributed. L6 is NOT_STARTED under the explicit hold and requires a later author instruction. READY_TO_MERGE and ACCEPT_RELEASE remain separate; no PR/main merge/release or completion of VAL/R-08 follows from loop acceptance.

The 8516 service is closed following the author's acceptance and shutdown request. L5_develop.zip is personal/local only and contains the 22 source files at archive root, including .github; no private tools/logs/reports/environments or nested project ZIP. GitHub source trees and release assets must contain no personal project ZIP. The normal Actions quality-report artifact is separate. Code rollback is possible through the accepted L4 source; temporary session data has no backup/recovery guarantee.
