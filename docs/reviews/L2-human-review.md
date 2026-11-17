# L2 Work and Human Review

**L2 identity and permission foundations, deep review, 17 November 2026 (Asia/Singapore). Human decision: PENDING. L3: NOT_STARTED.**

## Intake and scope

The author accepted L1 and declared its H01-H07 complete, then explicitly requested L2 with Rui Yan/Alex as ORGANISER and Xingjian/Sam as PARTICIPANT. Start point: accepted GitHub L1 commit 19b5cb58e689247dd70cfb7363fdc6923a8e3d4b. Tool/executor: Codex. L2 personal verification and ACCEPT_LOOP have not been supplied.

| Scope | Delivered treatment |
|---|---|
| app.py | One fixed-ID selector with a no-selection option, derived role caption and role checks for My Bookings/Organiser previews. Refresh and navigation retain session state. Deep review requires explicit OK and denies abnormal permission results. |
| booking.py | Update the four display labels; add resolve_actor and check_permission. Stable IDs and their logical roles remain unchanged. Existing models, capacity and time contracts remain unchanged. |
| test_booking.py | Retain all 42 L1 cases and their assertions; add 31 L2 cases in eleven functions. Total: 73 cases in 27 functions. All initial cases remain, with four UI assertions strengthened and two regressions added. |
| Task records | Update README, requirements, test-plan, Demo reuse and AI-use; add this single loop record. The package has 19 files, including eight Markdown documents. |
| Preserved | All four dependency input/lock files, pyproject.toml, Git configuration files and the single-job workflow. Local L0_develop/L1_develop and original tracked working-copy files are unchanged. Historical L0/L1 records in this package are byte-identical to the accepted L1. |
| Deferred | Workshop creation/browsing data, booking, cancellation, target-record access, waitlisting, validation and releases. Permission helpers do not complete B10/B12/B13. No PR, merge or release is part of this delivery. |

Deep-review task: check L2 candidate b5dfe6dd5d1bf7e912c83c4ce553886786063aff against accepted L0/L1 and course sources, fix findings, retain the manual preview and stop at L2. This is a continuation of L2, not CR-01.

## Contracts and assumptions

| Contract / assumption | Reason and limit |
|---|---|
| Fixed identities | organiser-1 Rui Yan; organiser-2 Alex; participant-1 Xingjian; participant-2 Sam. These are author-specified demonstration labels, not verified accounts. No contact, password or credential data is added. |
| resolve_actor(state, user_id) | Return the canonical session DemoUser for the ID, otherwise None. Display names are not keys. The application creates the fixed roster; no user-management UI exists. |
| check_permission(state, actor, required_role, owner_id=None) | INVALID_ACTOR for no/unknown identity or inconsistent role claim; FORBIDDEN for a valid identity with the wrong operation role or owner; otherwise OK. Never mutate the input. |
| Trusted operation context | required_role is an application constant. Future business functions must look up the actual target and pass its stored owner_id; accepting a caller's owner claim would not establish ownership. This helper performs no target lookup or mutation. |
| Independent backend check | The UI resolves an ID for display. The permission helper independently rechecks the actor against canonical state, so direct calls cannot skip role consistency. This is a deliberate boundary check. |
| Session scope | The same-session roster/state is authoritative. Selection is freely switchable; it is not secure login, tamper-proof storage or impersonation resistance. Start L2 in a fresh session for the updated labels; no live migration is claimed. |

## Risk-based review

AI proposes HIGH review depth for the role/owner-check code, following the permission-related focus in the course risk triage. Prototype exposure is limited by fictional, temporary session data, but that does not prove the checks correct. Review expected outcomes, role claims, owner provenance, state preservation and UI wiring. No dependency, credential or authentication change is introduced.

The author owns the actual risk classification/rationale and acceptance. Do not invent an independent or specialist approval. Escalate unresolved policy/security questions rather than inferring new permissions. R-03/R-06/R-07 receive the foundation evidence below; R-08 remains VALIDATION_PENDING. Freely selecting another identity is a disclosed prototype limit.

## Test oracles and review findings

| Condition / review focus | Expected result and evidence |
|---|---|
| Every fixed ID | Exact author-specified name/role resolves. Unknown IDs, no selection and a display name used as an ID do not resolve. |
| Known actor with inconsistent claimed role | INVALID_ACTOR before operation-role/owner decisions. Compare the complete populated input state and counters. |
| Valid actor, wrong required role | FORBIDDEN. A valid same-role actor with another owner's ID is also FORBIDDEN. Equal display names confer no ownership. |
| Valid actor with matching role/owner | OK without mutation. This does not authorise an unimplemented creation/cancellation operation. |
| Switching, clearing and refreshing | The same state object, all user/workshop/registration rows and counters remain unchanged. Separate sessions retain independent selections. |
| Test strength: role claim | A private copy omitting actor-role consistency fails two of the three focused cases. The genuine code passes all three. |
| Test strength: owner | A private copy omitting owner comparison fails three of nine focused cases. The genuine code passes all nine. |

Both faults were deliberately introduced only in private copies outside the delivery package. They are controlled checks of assertion strength, not defects claimed to have existed in the delivered application. Tests isolate permission causes without unrelated capacity/cutoff failures. Retained L1 test functions are unchanged.

The first browser probe clicked Streamlit's visually hidden native radio input and timed out. The private probe was corrected to click the visible View label; the application required no change. A second probe waits for completed rendering rather than assuming that the first heading means all widgets are ready. Neither automation issue is recorded as an application defect.

## Deep-review findings and simplicity decisions

| ID / significance | Finding and affected work | Evidence / disposition |
|---|---|---|
| DR-01 / Medium | test_booking.py: allowed-role tests checked absence of warnings without establishing that allowed content appeared. | CORRECTED: assert permitted content is visible and no error is shown. A private missing-content copy passes all four old role/view cases; the four strengthened cases fail it. Full booking.py coverage had not proved this UI property. |
| DR-02 / Medium | app.py: the last permission else admitted any result other than the two known denials. This was permissive failure handling if the helper contract failed; the real helper normally returns only its declared outcomes. | CORRECTED: admit only explicit OK, otherwise display an unavailable-view error. Two new AppTest cases inject None/unrecognised results: both fail before the fix and pass afterward, with allowed content absent and complete input state unchanged. No exploit through the normal selector is claimed. |
| DR-03 / Delivery update | The author requests a running preview for personal checks. The earlier QA server was intentionally stopped after its completed run. | IMPLEMENTED for this review: a hidden background Streamlit service bound to 127.0.0.1 is kept running at http://127.0.0.1:8512. Health and browser checks are below. This local service is not deployment/release evidence. |

| Simplicity question | Review decision |
|---|---|
| UI resolution plus backend recheck | RETAIN. Display needs canonical resolution; backend role-claim validation protects its own callable boundary. Existing forged-role fault tests demonstrate why the recheck matters. |
| Capacity/aware-time validators | RETAIN unchanged: they implement accepted BR-02/BR-03, including boolean capacity rejection and comparable instants. |
| Lists/dataclasses, fixed roster and optional owner | RETAIN. A four-row list and two small helpers fit the accepted architecture. Actual target-record binding remains later work. |
| New failure guard | One explicit-OK branch and a tested default denial are proportionate. No new application module, service layer, dependency, generic exception wrapper or runtime type matrix is introduced. |
| Expected identity data in tests/documents | These tables supply independent oracles from the author's instruction, rather than a second runtime registry. |

## Test mapping

Canonical mappings are in [test-plan.md](../test-plan.md#l2-implemented-test-mapping).

| Group | New cases | Scope |
|---|---|---|
| L2-01 | 8 | Fixed IDs/roles, unresolved inputs, no mutation; B01/B02 foundation. |
| L2-02 | 12 | Role, owner, forged identity and duplicate display names; partial B10/B12/B13, QR-03. |
| L2-03 | 7 | Fixed UI options, all four identities against both restricted previews and unselected denial; B01/B02, partial I08. |
| L2-04 | 1 | All identity changes/clear, views and refresh preserve populated state; partial I06/I08, QR-04. |
| L2-05 | 1 | Separate selected-identity state; partial I09, QR-04. |
| L2-06 | 2 | Abnormal-result denial, no allowed content and preserved input; partial I08, QR-03/QR-04. |

All 42 L1 cases remain regression evidence. Current automated identity/preview checks are verification, not user validation or proof of full business-operation permissions. Full B10/B12/B13, manual lifecycle parts of I06/I08/I09 and VAL-01/02/03 remain later work.

## Course and HD alignment

Original PDFs and Week3-9 PPTX text were rechecked against the supplied originals. References remain S01-S18 in Demo reuse. The 09:40/10:45 transcripts are duplicate accounts; automatic transcription is not independently verified audio.

| Criterion / source | Current evidence and remaining obligation |
|---|---|
| Requirements/quality planning, 15%; S01 pp.3/10 | Accepted FR/BR/QR/risk definitions remain intact. L2 identity/guard behaviours link to explicit outcomes, risks and exact tests. |
| Functional application/deployment, 15%; S01 pp.3/10 | L2 supplies four fixed identities and permission foundations. Actual workshop/booking functions, complete role workflows and assessed deployment remain L3-L6 work. A local preview is not V1.0 or deployment evidence. |
| V&V/tests, 20%; S01 pp.3/10-11; S06/S13/S14 | Review and 73 automated cases are verification. DR-01/02 critically check generated oracles and failure defaults. User validation, complete business permissions and R-08 suitability remain separate and pending. |
| Change/regression/releases, 20%; S01 pp.4/12 | L1 tests are retained and rerun. L2 remains pre-V1.0 work; CR-01 still needs working V1.0, impact analysis, focused branch/PR, new/regression tests, findings, a human merge decision and V1.1 release later. |
| GitHub/CI, 15%; S01 pp.5/12; S07 | One job retains tests, static/security/dependency checks, tested identity and failure reports. Fresh run identity below must correspond to reviewed code. Preserve material evidence before artifact expiry. |
| Defence/judgement, 15%; S01 pp.6-8/13; S05/S08 | AI tasks, assumptions, files, findings and executions are disclosed. The author must explain code/oracles, assess findings/risk and record L2 acceptance before the next loop or PR. AI/CI cannot fill those human fields. |

The lecture permits the simple three-file Demo to be adapted to a realistic scenario (S02 p.2; S03 pp.6-7). Its oversight and focused-review teaching is reflected in bounded intent, preserved behaviour, assumptions, findings and a separate human gate (S02 pp.8-10; S03 pp.2-4; S05/S08). This supports the L2 stage; it does not certify a final HD mark or invent independent approval.

## Verification results

Executor: AI, using the existing Python 3.12.14 environment. No additional application dependencies were installed.

| Check | Observed result |
|---|---|
| Local suite | 73/73 passed. booking.py: 79/79 statements and 20/20 branches covered. Coverage describes current foundations only. |
| Static/security | Ruff clean; formatting corrected and checked; pip check clean; Bandit reports zero findings/errors. Fresh hosted strict audits found no known vulnerabilities and reconciled all 34 runtime/71 development pins without omissions. This is a point-in-time result; locks are unchanged. |
| Controlled faults | Role-claim fault: 2 failed/1 passed. Owner fault: 3 failed/6 passed. Both genuine-code groups pass within the suite. Added evidence: missing-content fault passes the old four UI cases and fails the strengthened four; abnormal-result regressions fail 2/2 before the fix and pass in the 73-case suite afterward. |
| Browser desktop | PASS at http://127.0.0.1:8512, headless Chrome/Playwright 1.62.1, 1280x900. Correct URL/title, nonblank page, no error overlay, all four role/view paths, clear and refresh verified. No console/page errors. The local preview is kept running for the author as requested, bound to loopback. Use the README command after a future restart. |
| Browser route | Browser plugin not available. Used the existing bundled Playwright and Chrome; no browser dependency was added to the project. Temporary scripts, DOM snapshots and screenshots are outside the repository. |
| Mobile smoke | PASS at 390x844 after the sidebar collapse completed: main content renders without horizontal page overflow. This is not full mobile or cross-browser acceptance. |
| Hosted CI | PASS for this revision on codex/l2-identities. The single quality-checks job executed every configured step successfully: isolated runtime/imports, development install, Ruff/format, pip check, Bandit, complete lock audits, 73 tests and report upload. No checks were skipped. The workflow is unchanged. |
| Preservation | PASS: L0/L1/original working-copy hashes unchanged; all 16 original L1 test functions and their parameters retained (42 cases); accepted FR/BR/QR/risk bodies, historical decisions, four dependency files and workflow unchanged. English documents, local links and seven pending L2 checks verified. |

Earlier L2 snapshot b5dfe6dd5d1bf7e912c83c4ce553886786063aff passed [run 44004517662](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44004517662) with 71 cases. That historical run does not verify these changes. Current deep-review code [864ab69e7028af80621f5334cc74cd25dfaba542](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/864ab69e7028af80621f5334cc74cd25dfaba542) passed [run 44008568183](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44008568183), job 133789755491, on Ubuntu 24.04/Python 3.12.14. Logs confirm 73 passed, zero skipped and complete audits. Artifact quality-checks-44008568183-1 expires 1 December 2026; retain selected evidence before expiry. The documentation-only follow-up preserves the executable hashes below; inspect the latest branch run when accepting.

Reproduction: run `python -m pytest test_booking.py` in the project environment, with the Ruff/Bandit/audit commands in quality-checks.yml. Private browser verification used page.goto, the fixed combobox options, visible View labels, clear/Refresh, DOM assertions, console events and screenshots. Mobile screenshots wait for the sidebar transition to complete. Browser evidence remains outside the GitHub source tree.

Executable snapshot (SHA-256):

| File | SHA-256 |
|---|---|
| app.py | 6b1f63f8e1721bbecb464cf588a46e8ba61dc11c544c974422885305aec60f6a |
| booking.py | fa4c75b02f1d72f8ceb4f264008ac2a6722bfeb2e6c247a231c6d02616e96a28 |
| test_booking.py | e46d7dc50484ecc17d8dbfde1756b2f289a1c634f15f2d1f399be0a6f93647b5 |
| .github/workflows/quality-checks.yml | 72513f8b1ce3ce00541f86e5ff875e9497dd55eb9fb2f328e0a86a1edd589850 |

## Human acceptance checklist

These are L2 checks. The accepted L1 checklist remains historical and does not accept L2. Record actual personal actions separately from AI/CI results; no item is pre-completed by AI.

- [ ] **H01 Fixed identities:** Open a fresh L2 preview. Verify all four exact names, IDs/roles in the code, no identity selected initially and no free role editor.
- [ ] **H02 UI decisions:** Check both roles in My Bookings/Organiser; clear the selection and verify both restricted previews are denied. Workshops remains a public preview.
- [ ] **H03 Backend contract:** Explain canonical ID resolution, INVALID_ACTOR versus FORBIDDEN, optional owner comparison and why owner_id must come from an actual target later. Predict selected negative cases before reading results, including why an unrecognised permission result must not admit the preview.
- [ ] **H04 State and limits:** Inspect or rerun populated-state tests; switch/clear/refresh without reseeding. Explain independent sessions, reset limits and why identity selection is not secure login.
- [ ] **H05 Evidence:** Inspect the 73-case run, retained L1 tests, controlled-fault results and single-job Actions. Distinguish private faulty copies from delivered code and verification from validation; explain why no warning alone did not prove allowed content.
- [ ] **H06 Scope and AI:** Review the three core files, author-requested label changes, mappings and AI contributions. Confirm unchanged timing/capacity rules, locks and L0/L1. Record human edits or rejected suggestions.
- [ ] **H07 Decision:** Record reviewer/date/code identity, actual risk rationale, finding dispositions and ACCEPT_LOOP or CHANGES_REQUIRED. Keep L3 stopped until the loop decision.

| Human record | Actual value |
|---|---|
| Reviewer/date and reviewed code identity | NOT_RECORDED |
| Personally executed checks and observations | NOT_RECORDED |
| AI/CI results reviewed rather than personally executed | NOT_RECORDED |
| Code understanding and independent expected outcomes | NOT_RECORDED |
| Human edits, rejected suggestions and finding dispositions | NOT_RECORDED |
| Actual risk classification/rationale and residual limits | NOT_RECORDED |
| Decision | PENDING |

L2 stops here for the author's ACCEPT_LOOP. L3 is NOT_STARTED. READY_TO_MERGE and ACCEPT_RELEASE remain separate under the [workflow](../../README.md#development-workflow).
