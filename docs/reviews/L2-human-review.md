# L2 Work and Human Review

**Current revision: role-specific navigation, deep review on 17 November 2026 (Asia/Singapore). Human decision: HUMAN_REVIEW_PENDING. L3: NOT_STARTED.**

## Intake and earlier acceptance

On 17 November 2026 (Asia/Singapore), the author declared the UI and H01-H07 complete and supplied ACCEPT_LOOP for candidate 99627424ad05fcbe83196cc454dbccb772a776fc. The [historical author-confirmed checklist](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/blob/feb7b740ba7a35535a0b41ac673b6572f4aeb628/docs/reviews/L2-human-review.md#human-acceptance-checklist) preserves that statement, its declared completion and its limits. Commit feb7b740ba7a35535a0b41ac673b6572f4aeb628 records the acceptance without code/test changes.

The author subsequently requested hidden navigation combined with independent access rejection. That implementation was delivered as candidate bdbca42a6442479ab9550e6ef155005f9e00203e. The present task is a fresh deep review of that candidate against accepted L0/L1, the original assessment/HD rubric, lecture transcripts and decks, including fixes, English deliverables and a running preview. Executor/review tool: Codex. Earlier acceptance does not approve the later navigation revision. Stop before L3 pending renewed human acceptance.

## Scope and preserved behaviour

| File/surface | Current revision |
|---|---|
| app.py | UNCHANGED in this review. Role-appropriate menus, pre-widget view reset and independent UI permission checks remain. No production defect was reproduced in the reviewed L2 subset. |
| booking.py | UNCHANGED from accepted L2. Canonical ID resolution, role/owner checks and model/time contracts remain. |
| test_booking.py | Consolidate two duplicate no-identity parameters into one stronger case. Establish transition preconditions, assert resulting content and add two public-view retention parameters. Total: 87 cases in 30 functions. All 42 L1 parameters/assertions remain, with the two role-appropriate UI preconditions from the navigation implementation retained. |
| Existing documents | Update README, test plan, Demo reuse, AI use and this review. Six files change including test_booking.py; no new delivery file or helper tool. requirements.md is unchanged in this review. |
| Preserved | Accepted L0/L1 folders and their historical records, original tracked working copy, all four dependency files, pyproject.toml, Git configuration and the single-job Actions workflow. Package remains 19 files with eight Markdown documents. |
| Deferred | Actual workshop/booking/cancellation/roster operations, waitlist, full B10/B12/B13, validation, deployment and releases. No PR, main merge or L3 work. |

## Menu and access contract

| Identity | Visible menu | Hidden menu |
|---|---|---|
| None | Workshops | My Bookings; Organiser |
| Xingjian / Sam: PARTICIPANT | Workshops; My Bookings | Organiser |
| Rui Yan / Alex: ORGANISER | Workshops; Organiser | My Bookings |

1. Derive the menu from the canonical actor role, not a role editor or display name.
2. When the current view is no longer permitted, reset it to Workshops before widget creation. Same-role switches retain a permitted view. Unknown saved views also reset.
3. After menu selection, independently check a private view through booking.py. INVALID_ACTOR asks for a demo identity; FORBIDDEN rejects the wrong role. Only explicit OK displays private preview content. Unknown views/results display an unavailable-view error.
4. Navigation, switching, clearing and rejection never reseed or change business records or ID counters.
5. Fixed IDs remain organiser-1 Rui Yan, organiser-2 Alex, participant-1 Xingjian and participant-2 Sam. Selection remains freely switchable, temporary and non-authenticated.

The business helper resolves the canonical ID and checks role consistency plus an optional trusted owner ID without mutation. Future operations must look up the actual target and pass its stored owner ID. Menu hiding does not replace this callable boundary, and this preview does not prove full future operation permissions.

## Risk and simplicity review

| Risk / question | Control and evidence |
|---|---|
| R-03: hidden menu mistaken for access control | Keep booking.py checks and explicit-OK rendering. L2-07 forces hidden/unknown views past the menu and checks denial, absent private content and unchanged populated state. Direct role/owner/forged-actor tests remain. |
| R-04: identity change resets data | Change only current_view when needed. L2-04/L2-08/L2-09 compare complete state, object identity and counters. |
| R-06: AI expands scope or supplies human approval | Limit this review's changes to test_booking.py and five existing documents. Preserve the earlier acceptance separately and leave the current checklist pending. No future business operation is added. |
| R-07: tests disappear when menus hide options | Replace normal navigation to forbidden views with exact visibility assertions plus independent fault-injection rejection. Keep permitted-content assertions and the two abnormal-permission regressions. Record the two L1 UI precondition adaptations explicitly. |
| R-08: usability and policy suitability | Check understandable menus in the preview, but retain VALIDATION_PENDING. Actual VAL-01/02/03, including near-C promotion suitability, require later task feedback. |
| Proportionate architecture | One local role-to-view mapping, a short menu filter/reset and the existing guard. No new router, service, authentication framework, dependency or application file. Tests do not add an exposed route. |

AI recommends HIGH review depth for the role/permission boundary: menu hiding could conceal a missing business check, and a future operation could trust the wrong actor/owner. This is review-depth triage, not a claim of production authentication or an author-supplied rating. The author owns the actual classification, rationale and decision. Fictional session data limits exposure but does not establish correctness. If policy, understanding or suitable reviewer competence is unresolved, record SPECIALIST_ADVICE_REQUIRED and obtain suitable advice before a dependent PR/merge. No external approval is invented.

## Current findings and dispositions

| ID / priority | Finding, evidence and affected work | Assessment / disposition |
|---|---|---|
| ND-01 / Medium | test_booking.py: two no-identity parameters repeated the same exact-menu assertion but did not establish visible public content. A private copy removes Workshops content only when no actor is selected: all 86 previous cases still pass. | CORRECTED by AI: one stronger no-identity case checks exact menu, public heading/content and no warning/error. Transition/stale-state checks also require public content. The same fault now fails three checks. This is an oracle gap, not a runtime defect reproduced in the delivered app. |
| ND-02 / Medium | Transition tests checked the final heading/state without first proving the private starting view had rendered. An always-reset fault therefore passed four of six old transition cases; only same-role final-view cases detected it. | CORRECTED by AI: assert starting view/content and complete state, then resulting view/content/state. Add two cases retaining public Workshops across role changes. The faulty eight-case group now fails all six private-start cases; its two public-start cases correctly pass. |
| ND-03 / Low | This document called the historical checklist signed. The actual evidence is an author statement transcribed from the conversation; no signature or independent approval was supplied. | CORRECTED to author-confirmed, preserving the original ACCEPT_LOOP and its stated limits. Do not invent personal commands, observations, a separate risk rationale or a second reviewer. |

All corrections above are technical AI work on 17 November 2026. The project author still owns their assessment and acceptance. No unresolved blocking runtime finding was identified in this bounded review; full business-operation permissions and validation remain deferred, not passed.

### Simplicity decisions

| Question | Decision and reason |
|---|---|
| Hidden menu plus UI/business permission checks | RETAIN: visibility improves navigation; independent rejection protects the callable boundary. Controlled menu/helper faults are separately detected. These are different responsibilities. |
| Canonical actor resolution followed by role-claim recheck | RETAIN: display needs resolution; direct helper calls must reject inconsistent actors. No authentication framework is warranted in this fixed-identity prototype. |
| View reset/default denial | RETAIN: a short reset before widget creation handles changed options. Explicit OK and the small unknown-view/result guard prevent accidental admission. No generic fallback, catch-all exception layer or type-check matrix is added. |
| Repeated no-identity test parameters | CONSOLIDATE: exact equality to [Workshops] already excludes both private entries. The retained case now also proves useful public rendering. |
| Preview strings in tests | One independent PREVIEW_MESSAGES expectation table replaces repeated positive-message dictionaries. It is not imported from the implementation and does not create a second runtime registry. |
| Existing model validators and L1 cases | RETAIN unchanged: capacity and aware-time validation implement accepted contracts; historical regression assertions remain. No unrelated model cleanup is included. |

## Earlier findings retained

The [accepted deep review](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/blob/feb7b740ba7a35535a0b41ac673b6572f4aeb628/docs/reviews/L2-human-review.md#deep-review-findings-and-simplicity-decisions) retains DR-01 (missing permitted-content assertions), DR-02 (unknown permission results admitted by default) and DR-03 (retain the local preview). Corrections remain in the code/tests. Historical private controlled-fault results are preserved there; they are not relabelled as new executions.

## Fresh course and HD alignment

The original four PDFs were re-extracted and their SHA-256 hashes matched the prior source record. The 09:40 and 10:45 transcript page text is identical, so it is one account, not independent corroboration. Original Week3-9 PPTX text was read directly from the supplied archive; its hash is unchanged. Assessment rubric page 10 was also rendered to check the HD column. These are supplied automatic transcripts, not independently verified audio. Source identifiers remain S01-S18 in [Demo reuse](../demo-reuse.md#references); source files and private extraction tools are not redistributed.

| Criterion / source | L2 evidence and remaining obligation |
|---|---|
| Requirements and quality planning, 15%; S01 pp.3/10 | L0 FR/BR/QR/risk definitions are preserved. Menu/reset/rejection expectations trace to FR-01, BR-01/BR-14, QR-03/QR-04 and R-03/R-04/R-06/R-07. This review does not change timing or capacity policy. |
| Functional application/deployment, 15%; S01 pp.3/10 | The L2 identity/permission preview is coherent at this stage. Actual creation/booking/cancellation/rosters and a deployed working V1.0 remain later work. The local preview is not the assessed deployment or a complete minimum-functionality submission. |
| Verification, validation and tests, 20%; S01 pp.3-4/10-11; S06/S13/S14 | 87 tests and controlled faults check menu and permission properties against intended behaviour. The escaped public-content fault demonstrates critical review of AI oracles. Personal acceptance and VAL-01/02/03 are separate; R-08 remains VALIDATION_PENDING. |
| Change/regression/releases, 20%; S01 pp.4/12 | Retain all 42 L1 parameters/assertions, with the already-declared identity preconditions. L2 is pre-V1.0 foundation work, not CR-01. A working V1.0, meaningful waitlist change, impact analysis, focused branch/PR, regression, findings, justified merge and V1.1 release remain required. |
| GitHub/CI, 15%; S01 pp.5/12; S07 | Keep one job with tests, static/security/dependency checks, code identity and retained reports. No continue-on-error, automatic approval or merge is introduced. Fresh CI must match this test revision. |
| Defence/judgement, 15%; S01 pp.6-8/13; S05/S08 | Record intent, assumptions, actual AI files/tasks, findings, evidence and separate human fields. The author must explain why menu hiding is insufficient and why a green suite missed public content, then assess risk and the new checklist before proceeding. |

S02 p.2 and S03 pp.6-7 permit a realistic adaptation of the simple three-file teaching Demo; complexity is not the goal. S02 pp.8-10 and S05/S08 support bounded changes, human ownership before PR and explicit assumptions/evidence. Assessment p.4 permits the student's own justified decision unless the teaching team requires an external reviewer. Lecture permission/security escalation examples guide risk and reviewer routing; they are not evidence that specialist review occurred here. These findings support the L2 development method, not a final HD guarantee.

## Test mapping

The canonical exact-function mapping is [test-plan.md](../test-plan.md#l2-implemented-test-mapping).

| Group | Cases | Focus |
|---|---|---|
| L1 regression | 42 | Models, capacity/time representation and state/UI foundations. Original assertions retained; identity preconditions updated in two UI functions. |
| L2-01 | 8 | Fixed canonical identities and unresolved inputs. |
| L2-02 | 12 | Role/owner/forged-actor checks; no mutation. |
| L2-03 | 6 | Fixed identity options, exact role menus, permitted content and public content without an identity. |
| L2-04 | 1 | All identities/clear/refresh/navigation preserve populated state. |
| L2-05 | 1 | Separate selected identities in separate sessions. |
| L2-06 | 2 | None/unknown permission result denies permitted preview content. |
| L2-07 | 5 | Force a hidden/unknown view past the menu; independently reject it. |
| L2-08 | 8 | Established starting content/state, cross-role/clear resets, same-role and public-view retention, resulting content/state. |
| L2-09 | 2 | Forbidden/unknown saved view resets before widget creation and displays public content. |
| Total | 87 | 42 L1 plus 45 L2; 30 test functions. |

L2-07 renders the actual permitted radio, then substitutes its returned view in AppTest. It simulates bypass/abnormal control flow; it does not claim a public URL exploit. L2-09 seeds state before initial rendering. Normal stale-state recovery and independent access rejection are different properties.

## Verification results

Executor: AI using the existing Python 3.12.14 environment. Runtime files, workflow and dependency locks are unchanged in this review.

| Check | Observed result |
|---|---|
| Local pytest | PASS: 87/87, zero skipped, in 12.07 seconds, with JUnit/coverage outside the repository. Command: python -B -m pytest test_booking.py -q -p no:cacheprovider --junitxml=<private-output> --cov=booking --cov-branch. booking.py: 79/79 statements and 20/20 branches covered, diagnostic foundation coverage only. |
| Static/security | PASS locally and in hosted CI: Ruff check/format, Bandit and pip check. Fresh hosted strict audits report no known vulnerabilities, reconciling all 34 runtime/71 development pins without omissions. Point-in-time results; dependency inputs/locks are unchanged. |
| Controlled faults | Missing public content: old 86 pass, new 3 fail/84 pass. Always reset: old transition group 2 fail/4 pass, new 6 fail/2 pass. Bypassing the permission helper: 6 fail/1 pass in both focused groups. Show-all-menus: old 6 fail, new 5 fail after consolidation. Expected failures in private faulty copies; genuine code passes 87. |
| Browser route | Browser plugin not available. Used existing bundled Playwright 1.62.1/headless Chrome, no project dependency added. Temporary scripts, DOM and screenshots remain outside the repository. |
| Desktop | PASS at http://127.0.0.1:8512, 1280x900: correct URL/title, meaningful page, no Streamlit exception overlay. Public content without identity, all four menus/previews, both cross-role directions, clearing either private view, same-role/private retention, public-view retention and refresh verified. No console warnings/errors or page errors. |
| Mobile smoke | PASS at 390x844: after sidebar collapse, content remains visible without horizontal page overflow. Not full mobile/cross-browser acceptance. |
| Hosted CI | PASS for test revision d5da78ebc846bd2ca52f8b5eadfcdc41180a0acc: [run 44020706203](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44020706203), job 133829249225. One quality-checks job; all 18 steps succeeded, none skipped. Logs confirm 87 passed in 8.39 seconds, isolated runtime installation/imports, static checks, complete lock audits and report upload. The earlier bdbca42 run had 86 cases and remains historical. |
| Preservation | PASS before publication: 19 files; unchanged app.py/booking.py/config/locks/workflow, requirements.md, accepted L0/L1 folders and original tracked working copy. Accepted FR/BR/QR/risk/scenario definitions and all 16 L1 test functions/parameters/original assertions are retained; the two previously adapted UI preconditions are unchanged from bdbca42. English documents and all 47 local links/heading anchors checked. |

Key browser sequence: page.goto -> choose a fixed identity -> assert exact radio labels -> select permitted view -> switch same/cross role -> clear/refresh -> assert view/content -> desktop/mobile screenshot and console checks. The local preview remains running for personal checks. It is not deployment or user-validation evidence.

Hosted environment: Ubuntu 24.04/Python 3.12.14. Artifact quality-checks-44020706203-1 expires on 1 December 2026; preserve material evidence before expiry. This evidence-only document follow-up changes no executable/configuration hashes. Inspect the latest branch run when accepting; the linked run identifies the verified tests rather than claiming this document knew its own future commit SHA.

## Human acceptance checklist

These items apply to the new navigation revision and are intentionally unchecked. Do not copy the earlier acceptance into this revision.

- [ ] **H01 Identity and menus:** Confirm no identity shows only Workshops; Xingjian/Sam show Workshops and My Bookings; Rui Yan/Alex show Workshops and Organiser. Confirm the fixed labels/roles and absence of a role editor.
- [ ] **H02 Switch and clear:** From Organiser switch to a participant; from My Bookings switch to an organiser; clear either selection. Confirm Workshops is selected. Same-role switches retain a permitted view; refresh retains identity/view.
- [ ] **H03 Independent rejection:** Explain why hiding is insufficient. Inspect direct role/owner tests and L2-07/L2-09. Distinguish safe stale-state reset from rejection of a forced private view; explain INVALID_ACTOR, FORBIDDEN, unknown-result denial and later trusted owner lookup.
- [ ] **H04 State and limits:** Review full populated-state assertions and separate sessions. Confirm navigation does not change business data/counters. Explain that selection is not authentication and data is not durable/shared.
- [ ] **H05 Evidence:** Inspect 87 tests, mapping and fresh single-job Actions results. Explain why the old 86 passed missing public content, why transition preconditions matter, and why one stronger no-identity case replaces two duplicates. Distinguish controlled faults from delivered defects and verification from validation. Record actual personal checks separately.
- [ ] **H06 Diff and AI:** Review the navigation implementation against the earlier accepted snapshot, then this test_booking.py/five-document review diff against bdbca42. Confirm app.py/booking.py, rules, locks, workflow and L0/L1 are unchanged in this review. Record human edits or rejected suggestions.
- [ ] **H07 Decision:** Record reviewed commit, reviewer/date, finding dispositions, actual risk classification/rationale and ACCEPT_LOOP or CHANGES_REQUIRED. Use SPECIALIST_ADVICE_REQUIRED if understanding or suitable review is unresolved; never label AI/CI as approval. Keep L3 stopped until the decision and subsequent instruction.

| Current human record | Actual value |
|---|---|
| Earlier acceptance | Supplied for candidate 9962742; preserved in commit feb7b74 and the linked historical checklist. |
| Personal checks of this revision | NOT_YET_RECORDED. AI browser/tests are not personal human execution. |
| Reviewer/date/reviewed commit | TO_BE_RECORDED by the author for this revision. |
| Human edits/rejected suggestions | NOT_YET_RECORDED. |
| Risk classification/rationale and finding dispositions | TO_BE_RECORDED by the author; AI recommendations above are separate. |
| Current decision | HUMAN_REVIEW_PENDING. |

The author must understand the change, assess expected outcomes and actual evidence, and supply renewed ACCEPT_LOOP. L3 is NOT_STARTED. READY_TO_MERGE and ACCEPT_RELEASE remain separate under the [development workflow](../../README.md#development-workflow).
