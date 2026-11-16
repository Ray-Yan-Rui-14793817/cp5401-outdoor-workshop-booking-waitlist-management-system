# L1 Foundation Work and Human Review

**Loop: L1. Implementation and local verification complete. Human decision: PENDING. L2: NOT_STARTED.**

Date: 16 November 2026. Design: accepted L0 revision 3. AI executor: Codex assistant. Human reviewer: project author, review not yet recorded. The author's earlier ACCEPT_LOOP applies to L0 only.

## Intake and bounded task

Repository: [Outdoor Workshop project](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system).

Accepted parent: [822710b238bb14b8eba17cf2ab9a76ab2753bdb2](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/822710b238bb14b8eba17cf2ab9a76ab2753bdb2). This contains the author's completed seven-item L0 checklist and written rationale, preserved unchanged. The L0 record's NOT_STARTED status is historical to that decision.

The author requested a runnable three-file foundation, meaningful tests, GitHub Actions, English deliverables, AI disclosure and a personal acceptance gate. Preserve all accepted FR/BR/QR policies and the single-session/non-authenticated scope. Bilingual explanation belongs in chat.

Included: preview navigation, once-per-session state, fictional identity data, data models, structural validation, derived cutoff, foundation tests, dependency locks and CI. Excluded from this loop: actor selection/permissions, workshop creation, booking/cancellation, history operations, live deployment and all waitlist behaviour. These follow the existing L2-L9 plan.

## Deliverables and implementation choices

| Deliverable | Actual content |
|---|---|
| app.py | English Streamlit preview, three views, Refresh view and session counts; factory called only when demo_state is absent. No global mutable business state. |
| booking.py | Frozen DemoUser/Workshop/Registration rows, independent mutable DemoState collections/counters, fixed fictional identities, structural field checks and an aware elapsed-24h cutoff. No Streamlit dependency. |
| test_booking.py | 36 collected foundation cases; actual domain objects and Streamlit AppTest, not empty placeholder tests. |
| requirements.in / requirements.txt | Intentional runtime inputs and 34 resolved version/hash pins. |
| requirements-dev.in / requirements-dev.txt | Development inputs constrained by the runtime lock and 71 resolved version/hash pins, including packages with extras. |
| pyproject.toml | Python 3.12 Ruff configuration, pytest discovery and diagnostic booking-module branch coverage. |
| .github/workflows/quality-checks.yml | Four jobs, Python 3.12.14, read-only token, SHA-pinned Actions, hash installation and retained failure evidence. |
| Existing documents and this record | Current status, partial foundation mappings, actual reuse/AI contributions and pending human checklist. No auxiliary L0 document-checking tool reintroduced. |

Workshop construction validates structural data, not authority or current-time creation eligibility. Historical rows must remain representable. The L3 creation operation must separately enforce owner/role, fresh trusted time and S-t>24h. No UI exposes direct row construction in L1.

The factory starts with four fictional identities and no workshops/registrations. It creates a new set of mutable collections each time. No seed dates are regenerated on rerun; relatively dated workshop seeding remains L3 work. Fixed December examples here are frozen test fixtures.

## Foundation test mapping

FND IDs identify this loop's test groups, not replacements for the accepted B/W/I plan. Parameter cases are counted separately from functions.

| Group | Functions in test_booking.py | Cases | Supporting contract and scope |
|---|---|---|---|
| FND-01 | test_state_factories_do_not_share_lists_or_counters; test_fictional_identity_data_uses_unique_stable_ids_and_both_roles | 2 | QR-04/I09 factory foundation; identity data only, not FR-01 selection or permission enforcement. |
| FND-02 | test_workshop_represents_valid_capacity_boundaries; test_workshop_rejects_invalid_capacity | 10 | BR-02 structural capacity boundaries 1/30 and invalid types/ranges. B03/B04 operation/counter checks remain later. |
| FND-03 | test_workshop_rejects_missing_required_text | 8 | Structural required IDs/title/location; partial B05 support. |
| FND-04 | test_workshop_rejects_naive_or_missing_instants; test_workshop_rejects_non_positive_duration; test_data_model_can_represent_historical_workshops | 7 | BR-03 aware instants, duration and historical representation. No fresh-time creation/cutoff enforcement claimed. |
| FND-05 | test_cutoff_is_twenty_four_elapsed_hours_before_start | 1 | Known independent S/C example and 24 elapsed hours; partial BR-03 support, not B15/I10 action enforcement. |
| FND-06 | test_registration_rejects_naive_timestamps; test_registration_rejects_update_before_creation | 3 | Structural registration timestamps; not booking/cancellation behaviour. |
| FND-07 | test_app_views_start_without_exception; test_app_refresh_and_navigation_preserve_session_state; test_independent_app_sessions_do_not_share_state | 5 | Actual AppTest UI execution; automated supporting parts of I06/I08/I09. Manual browser lifecycle, role wiring and user validation remain pending. |

**Total: 36 cases; no failures or skips in the local run.** Test fixtures isolate one rejection cause. Expected capacity limits and the dated S/C example come from the accepted specification. Factory/session tests insert a sentinel workshop and advance a counter to detect loss/aliasing; empty screens alone would not establish that property.

## Actual local verification

Executor: AI using the project virtual environment, Windows, Python 3.12.14. These are tool executions, not personal checks by the author.

| Check | Actual observed result | Evidence/scope |
|---|---|---|
| Hash-locked install | Completed | Runtime/development locks; local environment is excluded from Git. |
| pytest | 36 collected, 36 passed, 0 failed, 0 skipped | reports/junit.xml; includes five AppTest cases. |
| booking.py branch coverage | 66/66 statements and 12/12 branch destinations covered, 100% | reports/coverage.xml; foundation module only. No full-requirement or production-quality claim. |
| Ruff lint and format | Passed | Three Python files; initial formatting was corrected before the clean check. |
| pip check | No broken requirements | Installed dependency consistency. |
| Bandit | Passed, zero findings | app.py and booking.py only; reports/bandit.json. |
| pip-audit runtime | All 34 pinned packages audited; zero known vulnerabilities and zero skips | Strict/hash mode with --disable-pip; reports/pip-audit-runtime.json; names/versions reconciled with the lock. |
| pip-audit development | All 71 pinned packages audited; zero known vulnerabilities and zero skips | Strict/hash mode with --disable-pip; reports/pip-audit-development.json; names/versions reconciled with the lock. |
| Workflow YAML | Parsed; expected four jobs/events/read-only permission verified | Syntax/configuration check, not a hosted run. |
| Local preview startup | Streamlit started on loopback port 8507 | Startup/health check only; no deployment or personal browser acceptance claimed. |

Local reports are generated under ignored reports/; they are not helper tools or fabricated GitHub results. Hosted artifacts retain code identity, installed versions and selected reports. Advisory results are time-limited observations, not proof of absent vulnerabilities.

Hosted CI status at initial preparation: PENDING. Record the actual branch, tested commit and run after publication. A local pass is not a hosted CI pass. No PR is opened before the author's personal pre-PR review; push-triggered CI can verify this bounded branch first.

## GitHub Actions and review boundary

| Job | Actual configuration |
|---|---|
| static-quality | Ruff lint JSON, format check and pip check. |
| security-review | Bandit on application code, strict pre-resolved/hash-required audits of both locks, and a required name/version reconciliation step. Artifact hashes are verified during installation. |
| tests | pytest, JUnit and booking.py branch coverage; AppTest requires no browser/server. |
| quality-gate | Runs even when predecessors fail/skip; succeeds only when all three succeed. |

Events: main/codex branch pushes, PRs to main, and workflow_dispatch when available on the default branch. The workflow does not deploy or merge. The quality-gate job is suitable as a required check, but enforcement through repository rules must be confirmed separately before merging; a YAML job alone does not configure branch protection.

Actions are pinned to the inspected official release commits: checkout v7.0.1, setup-python v7.1.0 and upload-artifact v7.0.2. Hosted jobs install the committed locks with --require-hashes. Audit/network failures are failures; there is no continue-on-error bypass. Reports upload with always() and 14-day retention; retain material evidence for submission before expiry.

PR head, base, tested GitHub SHA and actual checked-out SHA are retained in reports. Pull-request runs may test GitHub's merge commit; head/base identity remains distinct. A current-head check is needed after relevant changes.

## AI task, assumptions and findings

AI generated the three core files, tests, dependency inputs/locks, tool configuration, workflow and record updates. AI inspected the pinned Demo's dataclass/session approach, chose foundation examples from the accepted rules, executed local checks and corrected formatting. The author supplied the task/design constraints; no new personal L1 observations or acceptance have been supplied.

| Item | Assessment / disposition | Human review needed |
|---|---|---|
| Initial formatting | Ruff reformatted all three generated Python files; subsequent checks pass. This was a formatting finding, not an observed business defect. | Inspect the final diff; no invented runtime defect is claimed. |
| Audit package coverage | The initial successful audits reported 33 runtime/67 development packages, while complete locks contain 34/71. Changed to documented --disable-pip with --require-hashes; final reports cover all 34/71 packages. Added required CI name/version reconciliation. Hash verification remains enforced during install. | Assess the complete-set evidence rather than relying on exit code alone. |
| Empty foundation preview | Intentional L1 scope. Business controls remain in later loops; no placeholder Book button returns fake success. | Confirm the bounded increment is appropriate. |
| Structural versus creation rules | Historical dataclasses are permitted; service-level lead/role checks remain L3 obligations. | Explain why constructing a row is not an authorised create operation. |
| Identity/session limits | Fictional data and independently resettable sessions retained. No real login, shared concurrency or durability claim. | Confirm the stated prototype limits. |
| AppTest versus user evidence | Test harness insertion exercises state preservation; it is not a real booking task or user validation. | Assess assertions, perform own checks and leave R-08 pending. |
| Dependency/platform scope | Locks generated on Python 3.12.14/Windows. Hosted Ubuntu installation must be verified before treating CI as complete. | Review the real run and any findings. |

No substantive human rejection/edit, external review or finding disposition is invented. Record such actions below when they actually occur. All future permission, capacity-allocation, atomic-operation and cutoff-action controls remain required by the accepted design.

## Personal acceptance checklist

All boxes remain unchecked until the author performs or reviews the stated work and records observations. Reading AI results is a review activity; running a command personally is execution. Record which occurred.

- [ ] **H01 Setup and preview:** Install from the committed lock or verify the existing environment, run Streamlit, visit all three views and Refresh view, and record errors/observations. Expect a clearly limited preview with no business controls.
- [ ] **H02 Architecture:** Explain in your own words what app.py, booking.py and test_booking.py own. Confirm no database, password login or shared mutable global business state was added.
- [ ] **H03 Independent expectations:** Before running selected cases, predict capacity 1/30/0/31/True and the known S/C result. Run or inspect the relevant parametrised tests, explain why unrelated failures are excluded, and record actual results.
- [ ] **H04 State evidence:** Inspect/run the sentinel-state rerun and independent-session tests. Explain what they establish and why they do not prove browser reload recovery, real multi-user concurrency or actual booking behaviour.
- [ ] **H05 CI and findings:** Inspect all four hosted jobs for the current branch/code identity, reports and tool scope. Assess warnings/findings and confirm the gate cannot pass if a required job fails or is skipped. Later PR changes require current head/base checks; confirm repository-rule enforcement separately before merge.
- [ ] **H06 AI review and scope:** Inspect material code/assumptions, note any human edits or rejected suggestions, verify English/fictional data, and confirm actor operations and all waitlist code remain outside L1. Explain why 100% foundation coverage does not complete the B/W/I plan.
- [ ] **H07 Decision:** Record actual observations, findings/residual limits, date/code identity and a reasoned ACCEPT_LOOP or CHANGES_REQUIRED. L2 stays stopped until your explicit decision.

Useful commands from the project root on Windows:

```powershell
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m ruff check app.py booking.py test_booking.py
.\.venv\Scripts\python.exe -m ruff format --check app.py booking.py test_booking.py
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m bandit app.py booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Dependency audit reproduction uses `python -m pip_audit --strict --require-hashes --disable-pip -r requirements.txt` and the same command with requirements-dev.txt, through the project interpreter. These fully resolved files already contain the transitive pins; --disable-pip audits their complete package set without another resolver environment. Installation separately verifies artifact hashes. Advisory-network access is required. Do not regenerate locks merely to rerun tests; dependency changes require reviewed inputs, regenerated hashes and checks.

## Human observations and decision

| Field | Author to complete from actual work |
|---|---|
| Reviewer and date | NOT_RECORDED |
| Reviewed branch or PR/head/base/tested SHA | NOT_RECORDED |
| Personally executed checks and observations | NOT_RECORDED |
| Results reviewed rather than executed | NOT_RECORDED |
| Code understanding / independently predicted outcomes | NOT_RECORDED |
| Findings, human edits, rejected suggestions and reasons | NOT_RECORDED |
| Residual limits and rationale | NOT_RECORDED |
| Decision | PENDING |

Exit requires relevant passing checks, assessed findings and actual human ACCEPT_LOOP. Merge/release decisions remain separate. R-08 validation remains pending. The next permitted implementation loop after acceptance is L2; no L2 work has been performed.
