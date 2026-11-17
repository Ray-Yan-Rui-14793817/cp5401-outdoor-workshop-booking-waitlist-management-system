# L2 Work and Human Review

**L2 identity and permission foundations, 17 November 2026 (Asia/Singapore). Human decision: PENDING. L3: NOT_STARTED.**

## Intake and scope

The author accepted L1 and declared its H01-H07 complete, then explicitly requested L2 with Rui Yan/Alex as ORGANISER and Xingjian/Sam as PARTICIPANT. Start point: accepted GitHub L1 commit 19b5cb58e689247dd70cfb7363fdc6923a8e3d4b. Tool/executor: Codex. L2 personal verification and ACCEPT_LOOP have not been supplied.

| Scope | Delivered treatment |
|---|---|
| app.py | One fixed-ID selector with a no-selection option, derived role caption and role checks for My Bookings/Organiser previews. Refresh and navigation retain session state. |
| booking.py | Update the four display labels; add resolve_actor and check_permission. Stable IDs and their logical roles remain unchanged. Existing models, capacity and time contracts remain unchanged. |
| test_booking.py | Retain all 42 L1 cases and their assertions; add 29 L2 cases in ten functions. Total: 71 cases in 26 functions. |
| Task records | Update README, requirements, test-plan, Demo reuse and AI-use; add this single loop record. The package has 19 files, including eight Markdown documents. |
| Preserved | All four dependency input/lock files, pyproject.toml, Git configuration files and the single-job workflow. Local L0_develop/L1_develop and original tracked working-copy files are unchanged. Historical L0/L1 records in this package are byte-identical to the accepted L1. |
| Deferred | Workshop creation/browsing data, booking, cancellation, target-record access, waitlisting, validation and releases. Permission helpers do not complete B10/B12/B13. No PR, merge or release is part of this delivery. |

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

## Test mapping

Canonical mappings are in [test-plan.md](../test-plan.md#l2-implemented-test-mapping).

| Group | New cases | Scope |
|---|---|---|
| L2-01 | 8 | Fixed IDs/roles, unresolved inputs, no mutation; B01/B02 foundation. |
| L2-02 | 12 | Role, owner, forged identity and duplicate display names; partial B10/B12/B13, QR-03. |
| L2-03 | 7 | Fixed UI options, all four identities against both restricted previews and unselected denial; B01/B02, partial I08. |
| L2-04 | 1 | All identity changes/clear, views and refresh preserve populated state; partial I06/I08, QR-04. |
| L2-05 | 1 | Separate selected-identity state; partial I09, QR-04. |

All 42 L1 cases remain regression evidence. Current automated identity/preview checks are verification, not user validation or proof of full business-operation permissions. Full B10/B12/B13, manual lifecycle parts of I06/I08/I09 and VAL-01/02/03 remain later work.

## Verification results

Executor: AI, using the existing Python 3.12.14 environment. No additional application dependencies were installed.

| Check | Observed result |
|---|---|
| Local suite | 71/71 passed. booking.py: 79/79 statements and 20/20 branches covered. Coverage describes current foundations only. |
| Static/security | Ruff clean; formatting corrected and checked; pip check clean; Bandit reports zero findings/errors. Hosted lock audits remain pending. |
| Controlled faults | Role-claim fault: 2 failed/1 passed. Owner fault: 3 failed/6 passed. Both focused genuine-code groups pass within the complete suite. |
| Browser desktop | PASS at http://127.0.0.1:8512, headless Chrome/Playwright 1.62.1, 1280x900. Correct URL/title, nonblank page, no error overlay, all four role/view paths, clear and refresh verified. No console/page errors. The temporary QA server is stopped; start the app as described in README for human review. |
| Browser route | Browser plugin not available. Used the existing bundled Playwright and Chrome; no browser dependency was added to the project. Temporary scripts, DOM snapshots and screenshots are outside the repository. |
| Mobile smoke | PASS at 390x844 after the sidebar collapse completed: main content renders without horizontal page overflow. This is not full mobile or cross-browser acceptance. |
| Hosted CI | PENDING on codex/l2-identities. Workflow remains byte-identical to accepted L1: one quality-checks job, hash installs, isolated runtime, static/security/audits, tests and reports. |
| Preservation | PASS: L0/L1/original working-copy hashes unchanged; all 42 L1 test functions/parameters retained; accepted FR/BR/QR/risk bodies, historical decisions, four dependency files and workflow unchanged. English documents, local links and seven pending L2 checks verified. |

Executable snapshot (SHA-256):

| File | SHA-256 |
|---|---|
| app.py | 4af50f5d8cd7c1837c09813711bf5a16193be476f863c58b7923f207f5ce8618 |
| booking.py | fa4c75b02f1d72f8ceb4f264008ac2a6722bfeb2e6c247a231c6d02616e96a28 |
| test_booking.py | 678ed60879c60505676f7a1a86a9e677ebbf75153870535f38063362cac67e22 |
| .github/workflows/quality-checks.yml | 72513f8b1ce3ce00541f86e5ff875e9497dd55eb9fb2f328e0a86a1edd589850 |

## Human acceptance checklist

These are L2 checks. The accepted L1 checklist remains historical and does not accept L2. Record actual personal actions separately from AI/CI results; no item is pre-completed by AI.

- [ ] **H01 Fixed identities:** Open a fresh L2 preview. Verify all four exact names, IDs/roles in the code, no identity selected initially and no free role editor.
- [ ] **H02 UI decisions:** Check both roles in My Bookings/Organiser; clear the selection and verify both restricted previews are denied. Workshops remains a public preview.
- [ ] **H03 Backend contract:** Explain canonical ID resolution, INVALID_ACTOR versus FORBIDDEN, optional owner comparison and why owner_id must come from an actual target later. Predict selected negative cases before reading their results.
- [ ] **H04 State and limits:** Inspect or rerun populated-state tests; switch/clear/refresh without reseeding. Explain independent sessions, reset limits and why identity selection is not secure login.
- [ ] **H05 Evidence:** Inspect the 71-case run, retained L1 tests, controlled-fault results and single-job Actions. Distinguish private faulty copies from delivered code and automated verification from validation.
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
