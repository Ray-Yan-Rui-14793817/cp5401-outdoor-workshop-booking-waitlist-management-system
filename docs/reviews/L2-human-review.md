# L2 Work and Human Review

**Current revision: role-specific hidden menus plus independent access rejection. Human decision: HUMAN_REVIEW_PENDING. L3: NOT_STARTED.**

## Intake and earlier acceptance

On 17 November 2026 (Asia/Singapore), the author declared the UI and H01-H07 complete and supplied ACCEPT_LOOP for candidate 99627424ad05fcbe83196cc454dbccb772a776fc. The [historical signed checklist](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/blob/feb7b740ba7a35535a0b41ac673b6572f4aeb628/docs/reviews/L2-human-review.md#human-acceptance-checklist) preserves that statement, its declared completion and its limits. Commit feb7b740ba7a35535a0b41ac673b6572f4aeb628 records the acceptance without code/test changes.

The author subsequently requested hidden navigation combined with independent access rejection. This bounded L2 revision starts from that accepted snapshot. Earlier acceptance remains historical; it does not approve the later UI change. AI may implement and verify this instruction, but must stop before L3 pending renewed human acceptance.

## Scope and preserved behaviour

| File/surface | Current revision |
|---|---|
| app.py | Offer only role-appropriate views. Reset disallowed/unknown saved views before constructing the radio. Retain independent UI permission checks; reject unknown returned views. |
| booking.py | UNCHANGED from the accepted L2. Canonical ID resolution, role/owner checks and model/time contracts remain. |
| test_booking.py | Adapt UI cases to the new menu contract; add 13 cases. Total: 86 cases in 30 functions. Retain 42 L1 parameter cases and original assertions; two L1 UI functions select an appropriate identity before private navigation. |
| Existing documents | Update README, requirements, test plan, Demo reuse, AI use and this review. No new delivery document or helper tool. |
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
| R-06: AI expands scope or supplies human approval | Limit changes to app.py, test_booking.py and six existing documents. Preserve the earlier acceptance separately and leave this checklist pending. No future business operation is added. |
| R-07: tests disappear when menus hide options | Replace normal navigation to forbidden views with exact visibility assertions plus independent fault-injection rejection. Keep permitted-content assertions and the two abnormal-permission regressions. Record the two L1 UI precondition adaptations explicitly. |
| R-08: usability and policy suitability | Check understandable menus in the preview, but retain VALIDATION_PENDING. Actual VAL-01/02/03, including near-C promotion suitability, require later task feedback. |
| Proportionate architecture | One local role-to-view mapping, a short menu filter/reset and the existing guard. No new router, service, authentication framework, dependency or application file. Tests do not add an exposed route. |

AI recommends focused review of the permission boundary and navigation state. The author owns the final risk classification, rationale and decision; none is supplied by AI. Fictional session data limits exposure but does not establish correctness.

## Earlier findings retained

The [accepted deep review](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/blob/feb7b740ba7a35535a0b41ac673b6572f4aeb628/docs/reviews/L2-human-review.md#deep-review-findings-and-simplicity-decisions) retains DR-01 (missing permitted-content assertions), DR-02 (unknown permission results admitted by default) and DR-03 (retain the local preview). Corrections remain in the code/tests. Historical private controlled-fault results are preserved there; they are not relabelled as new executions.

The course/source comparison from that review remains the basis for the unchanged three-file architecture, bounded AI task, meaningful tests, CI and separate human decisions. This navigation update supports those methods and the author-requested behaviour. It is not a fresh full-assessment audit or a guarantee of an HD grade.

## Test mapping

The canonical exact-function mapping is [test-plan.md](../test-plan.md#l2-implemented-test-mapping).

| Group | Cases | Focus |
|---|---|---|
| L1 regression | 42 | Models, capacity/time representation and state/UI foundations. Original assertions retained; identity preconditions updated in two UI functions. |
| L2-01 | 8 | Fixed canonical identities and unresolved inputs. |
| L2-02 | 12 | Role/owner/forged-actor checks; no mutation. |
| L2-03 | 7 | Fixed identity options, exact role menus and permitted preview content. |
| L2-04 | 1 | All identities/clear/refresh/navigation preserve populated state. |
| L2-05 | 1 | Separate selected identities in separate sessions. |
| L2-06 | 2 | None/unknown permission result denies permitted preview content. |
| L2-07 | 5 | Force a hidden/unknown view past the menu; independently reject it. |
| L2-08 | 6 | Cross-role/clear resets; same-role retention, with state preservation. |
| L2-09 | 2 | Forbidden/unknown saved view resets before widget creation. |
| Total | 86 | 42 L1 plus 44 L2; 30 test functions. |

L2-07 renders the actual permitted radio, then substitutes its returned view in AppTest. It simulates bypass/abnormal control flow; it does not claim a public URL exploit. L2-09 seeds state before initial rendering. Normal stale-state recovery and independent access rejection are different properties.

## Verification results

Executor: AI using the existing Python 3.12.14 environment. Current source/test changes were checked before publication.

| Check | Observed result |
|---|---|
| Local pytest | PASS: 86/86, zero skipped, in 8.54 seconds. Command: python -B -m pytest test_booking.py -q -p no:cacheprovider. |
| Static/security | PASS: Ruff check and format check for all three Python files; Bandit for app.py/booking.py; pip check. No code/dependency changes followed these checks. Hosted lock-audit status must be tied to the run below. |
| Browser route | Browser plugin not available. Used existing bundled Playwright 1.62.1/headless Chrome, no project dependency added. Temporary scripts, DOM and screenshots remain outside the repository. |
| Desktop | PASS at http://127.0.0.1:8512, 1280x900: correct URL/title, meaningful page, no Streamlit exception overlay. All four exact role menus and allowed previews, clear reset, cross-role reset, same-role retention and refresh verified. No console warnings/errors or page errors. |
| Mobile smoke | PASS at 390x844: after sidebar collapse, content remains visible without horizontal page overflow. Not full mobile/cross-browser acceptance. |
| Hosted CI | PENDING for the navigation revision at document preparation; replace with observed commit/run and job results after publication. The single-job workflow is unchanged. |
| Preservation | PASS before publication: 19 files; unchanged booking.py/config/locks/workflow, L0/L1 folders and original tracked working copy. Accepted FR/BR/QR/risk/scenario definitions remain unchanged. All 16 L1 test functions retain their parameters and original assertions; exactly two UI preconditions were adapted. English Markdown and local link targets checked. |

Key browser sequence: page.goto -> choose a fixed identity -> assert exact radio labels -> select permitted view -> switch same/cross role -> clear/refresh -> assert view/content -> desktop/mobile screenshot and console checks. The local preview remains running for personal checks. It is not deployment or user-validation evidence.

## Human acceptance checklist

These items apply to the new navigation revision and are intentionally unchecked. Do not copy the earlier acceptance into this revision.

- [ ] **H01 Identity and menus:** Confirm no identity shows only Workshops; Xingjian/Sam show Workshops and My Bookings; Rui Yan/Alex show Workshops and Organiser. Confirm the fixed labels/roles and absence of a role editor.
- [ ] **H02 Switch and clear:** From Organiser switch to a participant; from My Bookings switch to an organiser; clear either selection. Confirm Workshops is selected. Same-role switches retain a permitted view; refresh retains identity/view.
- [ ] **H03 Independent rejection:** Explain why hiding is insufficient. Inspect direct role/owner tests and L2-07/L2-09. Distinguish safe stale-state reset from rejection of a forced private view; explain INVALID_ACTOR, FORBIDDEN, unknown-result denial and later trusted owner lookup.
- [ ] **H04 State and limits:** Review full populated-state assertions and separate sessions. Confirm navigation does not change business data/counters. Explain that selection is not authentication and data is not durable/shared.
- [ ] **H05 Evidence:** Inspect 86 tests, exact mapping and fresh single-job Actions results. Understand the 13 additions and two L1 UI precondition changes; choose meaningful personal checks and record actual results separately.
- [ ] **H06 Diff and AI:** Review app.py, test_booking.py and six existing documents against the accepted snapshot. Confirm booking.py, business rules, locks, workflow and L0/L1 remain unchanged. Record human edits or rejected suggestions.
- [ ] **H07 Decision:** Record reviewed commit, reviewer/date, observed findings, risk rationale and ACCEPT_LOOP or CHANGES_REQUIRED. Keep L3 stopped until the new decision and subsequent instruction.

| Current human record | Actual value |
|---|---|
| Earlier acceptance | Supplied for candidate 9962742; preserved in commit feb7b74 and the linked historical checklist. |
| Personal checks of this revision | NOT_YET_RECORDED. AI browser/tests are not personal human execution. |
| Reviewer/date/reviewed commit | TO_BE_RECORDED by the author for this revision. |
| Human edits/rejected suggestions | NOT_YET_RECORDED. |
| Risk classification/rationale and finding dispositions | TO_BE_RECORDED by the author; AI recommendations above are separate. |
| Current decision | HUMAN_REVIEW_PENDING. |

The author must understand the change, assess expected outcomes and actual evidence, and supply renewed ACCEPT_LOOP. L3 is NOT_STARTED. READY_TO_MERGE and ACCEPT_RELEASE remain separate under the [development workflow](../../README.md#development-workflow).
