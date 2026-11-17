# L5 Work and Human Review

**Current: L5 HUMAN_REVIEW_PENDING. Human decision: PENDING. H01-H07: unchecked. L6: NOT_STARTED.**

## Intake and baseline

The author explicitly requested L5 after accepted L4: participants cancel their own confirmed bookings, release capacity and retain history; enforce strict 24-hour, permission and repeat rules; keep the simple architecture, single-job Actions and L1-L4 regressions; update English delivery/AI/human records, provide a local-only ZIP and live preview, then stop for ACCEPT_LOOP. This supersedes the earlier L5 hold for this bounded implementation only.

Base: [accepted L4/GitHub 2f2504acff79317c20760971acae2965ee98a1fb](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2f2504acff79317c20760971acae2965ee98a1fb). Its underlying accepted candidate, UI/H01-H07, three human feedback items and AI evidence attribution remain byte-identical in [L4 history](L4-human-review.md#current-human-acceptance). The existing 21-file L5 starting folder and private metadata were checked against that GitHub tree before implementation. No pre-existing divergent user change was overwritten.

Executor: Codex assistant/local tools or GitHub Actions as labelled. Intake/local work began under the client date 17 November 2026; hosted verification is recorded on 18 November 2026 following the updated client context (both UTC+08:00). Workshop display is Asia/Singapore. No personal execution timestamp, feedback, risk rating, code edit or acceptance is supplied for L5.

## Scope, architecture and changed files

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

## Verification evidence

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

## Review observations and corrections

| ID | Actual observation and disposition |
|---|---|
| L5-F01 | Initial setup assumed a new private evidence directory and a child .venv. Existing metadata/starting files matched accepted L4 and were verified/reused; the first test invocation addressed no executable and ran no tests. Corrected to the existing parent environment before recording red/green evidence. No dependency install, accepted-file overwrite or product workaround. Closed setup correction. |
| L5-F02 | Repeated cancellation after C/S must be ALREADY_CANCELLED rather than an active time rejection. The implementation follows BR-06's owner-first/no-op-first order; five fresh repeat cases and two actual cancel/rebook chains confirm no extra release or ID change. This is intended behaviour, not a claimed inherited product defect. Human H04 pending. |
| L5-F03 | Only OK may replace UI state. Three distinct-candidate injections and one call-exception check verify the exact prior object/records/counters and no false success; retained F08 state and identity survive the happy path. No broad catch/repair abstraction was needed. Human evidence judgement pending. |
| L5-F04 | Pre-publication checks caught a duplicated old L4 status preamble and locally generated ignored pytest/Ruff caches. Remove the duplicate, clarify the current gate and move only those caches into private evidence after verifying source/destination paths. The final export has exactly 22 files; canonical definitions and historical acceptance files are unchanged. Closed documentation/packaging correction. |

No confirmed rule violation remains in the executed paths. Automated success is bounded evidence, not proof of all possible faults. Later findings must be recorded before acceptance; AI does not fabricate a student edit, rejected suggestion, risk decision or independent personal execution.

## Risk controls and remaining limits

| Risk | L5 control/evidence and pending judgement |
|---|---|
| R-01 | Exact count decrement, fixed IDs/counters, full-workshop release/rebook and repeat-old-ID sequencing. H02/H03 pending; simultaneous concurrency remains excluded. |
| R-03 | Business role/actual stored owner checks, same-name denial, own-only controls and hidden menus. H05 pending; demo selection remains freely switchable and is not authentication. |
| R-04 | Complete candidate/copied lists, preserved cancelled ID/created_at, unchanged other rows/counters, rejection/no-op/exception checks and independent sessions. H02/H06 pending; no durability/recovery claim. |
| R-05 | Fresh active C-1/C/C+1/S boundaries, equivalent instants, separate repeat semantics and actual submission-time wiring. H04 pending; no user clock/override. |
| R-06/R-07 | Bounded scope, retained 250 cases, independent exact-state oracles, disclosed internal injections/setup correction and unchanged single-job checks. H01/H07 must judge the evidence and AI contribution. |
| R-08 | Explicit cancellation/history/cutoff and temporary fictional-session disclosures. Full suitability/notification/near-C promotion validation remains VALIDATION_PENDING; no waitlist exists in L5. |
| R-02 | No FIFO/promotion in L5. Controls and tests remain future CR-01 scope. |

Carry forward L4-HF-01/02/03 without rewriting their original acceptance: cancellation now follows a new explicit instruction; negative tests isolate causes, serial-only scope remains, and AI browser/fault evidence stays distinct from author-verified prior CI. Original L3 HF-02 remains historical; current F08 isolation is retained.

## AI and human contribution

The author supplied scope/policy and accepted L0-L4. AI implemented one domain operation and its UI wiring, wrote 48 tests using the accepted contracts, preserved all prior tests/history, ran local/browser/hosted checks and prepared English delivery/mapping/ZIP. Actual changed paths are listed above. The author has not supplied L5 code edits, personal observations, per-finding dispositions, a risk rationale or ACCEPT_LOOP. GitHub Actions is an automated executor, not an approver.

## Human acceptance checklist

These are planned checks for the author, not AI-completed executions. Start with a fresh human session on [http://127.0.0.1:8516](http://127.0.0.1:8516). Use fictional data. For clock/ID/internal failure cases, inspect or rerun the supplied named tests; do not add a deployed clock editor to make a manual demonstration easier.

- [ ] **H01 - Candidate and scope.** Verify the L5 branch/code identity/current Actions and inspect the three-file diff, exact test mapping, AI contributions/findings and unchanged accepted L0-L4 history. Confirm the personal ZIP is local-only and L6 has not begun.
- [ ] **H02 - Own cancellation and history.** Select Sam -> My Bookings -> cancel registration-2 (Photography). Expect success, total confirmations three to two, no current Sam confirmation, registration-2/4 CANCELLED in History, and no repeat button. Refresh/navigation must not release another place. Inspect the exact-state test for preserved IDs/created_at/other rows and unchanged counters.
- [ ] **H03 - Reallocate one released place.** Switch to Xingjian -> Workshops -> Book Photography. Expect new registration-5, total confirmations three and retained Sam history. Alex's Photography roster must contain Xingjian. Inspect actual cancel/rebook/repeat tests to confirm an old cancelled ID cannot release this new place and a further eligible serial Book is FULL.
- [ ] **H04 - Strict cutoff and repeat semantics.** Inspect locked Trail Safety controls and fresh active C-1/C/C+1/S/S+1 tests, including a page rendered open but processed at C. Effective cancellation at C must reject without state/counter changes. Separately inspect owned CANCELLED repeats before/after C/S: ALREADY_CANCELLED with no mutation. Do not reuse a cancelled fixture to claim active deadline enforcement.
- [ ] **H05 - Permissions and identity.** Compare Sam/Xingjian own controls/history. No identity/organisers have no participant cancellation menu/control. Inspect direct wrong-role, forged-actor and other-owner tests with valid unrelated preconditions, plus equal-name checks. Explain why stored ownership is enforced in booking.py beyond menu hiding, and why demo selection is not real authentication.
- [ ] **H06 - Regression, drafts and session limits.** Fail Rui creation, navigate to cancel/rebook as participants, then return to Rui: his latest eight values/errors remain his own. Recheck F05 reset/restore and F08 owner-only success reset using retained tests. Check refresh and an independent browser session; explain reload/restart data loss. Inspect or run all 298 regressions and record what you actually executed rather than copying AI results.
- [ ] **H07 - Human judgement and next decision.** Explain Demo reuse and project-specific cancellation, exact independent oracles, serial scope, internal injections and AI evidence attribution. Review L5-F01-F04 and proposed High review depth; record actual findings/edits/rejected suggestions, residual-risk rationale and reviewer/date. Supply candidate-specific ACCEPT_LOOP, CHANGES_REQUIRED or proportionate escalation. Stop at L5; acceptance alone does not start L6.

Example commands from the repository root with an existing Python environment:

```powershell
python -m pytest test_booking.py -q
python -m pytest test_booking.py -k "l5_" -v
python -m pytest test_booking.py -k "l5_effective or l5_owned_cancelled or l5_stale" -v
```

Actual personal checks/observations: **PENDING**.
Human reviewer/date: **PENDING**.
Human code edits/rejected suggestions: **NOT SUPPLIED**.
Human risk judgement and rationale: **PENDING**.
Human decision: **PENDING**.

## Exit gate and delivery

Technical delivery requires current passing checks, accurate mapping/provenance and matching local/GitHub/archive contents. The author must inspect the candidate, complete relevant personal checks and explicitly ACCEPT_LOOP; AI records that statement separately from its own runs. No human approval is inferred from tests or this delivery. L6 is NOT_STARTED and needs later authorisation; no PR/main merge/release is included.

The 8516 service remains running for human review. L5_develop.zip is personal/local only and contains the 22 source files at archive root, including .github; no private tools/logs/reports/environments or nested project ZIP. GitHub source trees and release assets must contain no personal project ZIP. The normal Actions quality-report artifact is separate. Code rollback is possible through the accepted L4 source; temporary session data has no backup/recovery guarantee.
