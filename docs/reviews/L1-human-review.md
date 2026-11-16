# L1 Foundation Work and Human Review

**Loop: L1. Implementation and local verification complete. Human decision: PENDING. L2: NOT_STARTED.**

Date: 16 November 2026. Design: accepted L0 revision 3. AI executor: Codex assistant. Human reviewer: project author, review not yet recorded. The author's earlier ACCEPT_LOOP applies to L0 only.

## Intake and bounded task

Repository: [Outdoor Workshop project](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system).

Accepted parent: [822710b238bb14b8eba17cf2ab9a76ab2753bdb2](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/822710b238bb14b8eba17cf2ab9a76ab2753bdb2). This contains the author's completed seven-item L0 checklist and written rationale, preserved unchanged. The L0 record's NOT_STARTED status is historical to that decision.

The author requested a runnable three-file foundation, meaningful tests, GitHub Actions, English deliverables, AI disclosure and a personal acceptance gate. Preserve all accepted FR/BR/QR policies and the single-session/non-authenticated scope. Bilingual explanation belongs in chat.

Included: preview navigation, once-per-session state, fictional identity data, data models, structural validation, derived cutoff, foundation tests, dependency locks and CI. Excluded from this loop: actor selection/permissions, workshop creation, booking/cancellation, history operations, live deployment and all waitlist behaviour. These follow the existing L2-L9 plan.

### Risk triage and reviewer routing

These are AI recommendations for the author's review, not recorded human risk acceptance.

| Scope | Proposed classification and rationale | Routing / decision status |
|---|---|---|
| Entire L1 foundation | HIGH review sensitivity: introduces third-party dependencies and input/time validation, matching the sensitive areas in Module 6's risk-triage guidance. Operational exposure is bounded by fictional, local, non-authenticated preview data; no booking allocation or durable storage exists yet. | Project author owns scope, code understanding and the individual-assessment self-review decision. Human confirmation PENDING. Seek suitable advice if the author cannot resolve a material dependency/validation question. |
| This L1 deep-review correction | MEDIUM: changes test oracles and CI failure/runtime checks, which affect confidence in the gate. app.py, booking.py, dependency versions and business policies remain unchanged. | Author reviews the focused diff and challenge evidence before ACCEPT_LOOP or a PR. Human confirmation PENDING. |

Relevant risks are R-04 state loss, R-05 time assumptions, R-06 unreviewed AI output and R-07 weak checks/regression. R-08 remains pending actual user validation. There is no risk waiver, specialist approval or human verification inferred from AI execution. The assessment permits the author's documented decision unless teaching staff require an external reviewer; reviewer competence and unresolved policy questions still determine escalation.

## Deliverables and implementation choices

| Deliverable | Actual content |
|---|---|
| app.py | English Streamlit preview, three views, Refresh view and session counts; factory called only when demo_state is absent. No global mutable business state. |
| booking.py | Frozen DemoUser/Workshop/Registration rows, independent mutable DemoState collections/counters, fixed fictional identities, structural field checks and an aware elapsed-24h cutoff. No Streamlit dependency. |
| test_booking.py | 40 collected foundation cases; actual domain objects and Streamlit AppTest, including four added timestamp regressions. |
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
| FND-04 | test_workshop_rejects_naive_or_missing_instants; test_workshop_rejects_non_positive_duration; test_data_model_can_represent_historical_workshops; test_workshop_orders_repeated_clock_times_by_instant | 9 | BR-03 aware instants, duration, historical representation and UTC-order regression. No fresh-time creation/cutoff enforcement claimed. |
| FND-05 | test_cutoff_is_twenty_four_elapsed_hours_before_start | 1 | Known independent S/C example and 24 elapsed hours; partial BR-03 support, not B15/I10 action enforcement. |
| FND-06 | test_registration_rejects_naive_timestamps; test_registration_rejects_update_before_creation; test_registration_orders_repeated_clock_times_by_instant | 5 | Structural timestamp chronology including repeated-clock UTC-order regression; not booking/cancellation behaviour. |
| FND-07 | test_app_views_start_without_exception; test_app_refresh_and_navigation_preserve_session_state; test_independent_app_sessions_do_not_share_state | 5 | Actual AppTest execution, mixed CONFIRMED/CANCELLED count and complete state/counter preservation; supports BR-04 and automated parts of I06/I08/I09. Manual lifecycle, role wiring and user validation remain pending. |

**Final local total: 40 cases; no failures or skips.** Test fixtures isolate one rejection cause. Expected capacity limits and the dated S/C example come from the accepted specification. The strengthened session test uses a workshop, one confirmed and one cancelled record, both counters and a complete state snapshot. It expects two retained records but only one confirmed count; refresh/navigation must preserve the entire snapshot. Empty screens alone would not establish those properties.

The initial 36 cases passed, including full current booking-module line/branch coverage. Further review reproduced a missed input category: 01:30 in the first occurrence followed by 01:15 in the second occurrence of a repeated local hour. The UTC instants are 45 minutes apart in chronological order. The old constructors rejected that valid order and accepted the reverse. Four new workshop/registration regression cases failed before correction. Comparing UTC instants fixed both errors; the full 40-case suite then passed. This is a real observed data-model defect, not an invented booking failure. Test input representation uses a repeated-hour zone; the application still displays Asia/Singapore and gains no new time-zone UI.

## Actual local verification

Executor: AI using the project virtual environment, Windows, Python 3.12.14. These are tool executions, not personal checks by the author.

| Check | Actual observed result | Evidence/scope |
|---|---|---|
| Hash-locked install | Completed | Runtime/development locks; local environment is excluded from Git. |
| pytest | Final run: 40 collected, 40 passed, 0 failed, 0 skipped | reports/junit.xml; includes five AppTest and four new timestamp regression cases. |
| booking.py branch coverage | 66/66 statements and 12/12 branch destinations covered, 100% | reports/coverage.xml; foundation module only. No full-requirement or production-quality claim. |
| Ruff lint and format | Passed | Three Python files; initial formatting was corrected before the clean check. |
| pip check | No broken requirements | Installed dependency consistency. |
| Bandit | Passed, zero findings | app.py and booking.py only; reports/bandit.json. |
| pip-audit runtime | All 34 pinned packages audited; zero known vulnerabilities and zero skips | Strict/hash mode with --disable-pip; reports/pip-audit-runtime.json; names/versions reconciled with the lock. |
| pip-audit development | All 71 pinned packages audited; zero known vulnerabilities and zero skips | Strict/hash mode with --disable-pip; reports/pip-audit-development.json; names/versions reconciled with the lock. |
| Workflow YAML | Parsed; expected four jobs/events/read-only permission verified | Syntax/configuration check, not a hosted run. |
| Local preview startup | Streamlit started on loopback port 8507 | Startup/health check only; no deployment or personal browser acceptance claimed. |
| Isolated runtime installation | Fresh environment installed requirements.txt with hashes; pip check and app/booking/Streamlit imports passed; pytest absent | Windows local check without the development environment. CI now repeats the runtime import check in a fresh Linux virtual environment. |
| Test-oracle fault challenges | Three copied faulty apps passed the old selected test and failed the strengthened test | Independently challenged registration-list loss, registration-counter reset and counting cancelled records. Faults existed only in private analysis copies, never in the real app or GitHub branch. |
| CI failure-path checks | Failed left-hand pipeline command now returns nonzero; successful gate control passed and nine failure/skipped/cancelled predecessor cases were rejected | Local Bash checks of workflow semantics. They are diagnostics, not additional pytest cases or deliberately failed hosted runs. |

Local reports are generated under ignored reports/; they are not helper tools or fabricated GitHub results. Hosted artifacts retain code identity, installed versions and selected reports. Advisory results are time-limited observations, not proof of absent vulnerabilities.

Initial hosted evidence: [run 43867810566](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/43867810566) passed all four jobs on commit 30918d42acd7ead5d75e9577fe7b0d878f54ae92 with the initial 36 cases. It predates the timestamp correction and does not verify that later change.

### Verified hosted evidence after correction

| Field | Actual evidence |
|---|---|
| Branch | [codex/l1-foundation](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/tree/codex/l1-foundation) |
| Tested implementation commit | [aaf324cccd995b831a7f09347cc329a71b41bcd6](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/aaf324cccd995b831a7f09347cc329a71b41bcd6) |
| Completed run | [43868519549](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/43868519549), push event, conclusion SUCCESS |
| Environment | GitHub-hosted ubuntu-24.04, Python 3.12.14; committed hash locks installed successfully |
| Jobs | static-quality SUCCESS; security-review SUCCESS; tests SUCCESS; quality-gate SUCCESS |
| Test log inspected | 40 collected, 40 passed; 66/66 statements and 12/12 branch destinations covered in booking.py |
| Security log inspected | Both audits report no known vulnerabilities; reconciliation confirms all 34 runtime and 71 development pins without omissions |
| Artifacts confirmed | static-quality-43868519549-1; security-review-43868519549-1; tests-43868519549-1 |
| Artifact retention | These three artifacts expire 30 November 2026; this committed record retains the selected findings/counts/code identity. Preserve further material reports before expiry if needed for submission. |
| Assessed by | AI executor inspecting actual GitHub logs/metadata; author review remains PENDING |
| Main and PR state | Main remains 822710b238bb14b8eba17cf2ab9a76ab2753bdb2. No PR opened, merge, deployment or release. |

Any later evidence-only documentation commit must have its own current branch checks inspected. The implementation run above verifies the exact code commit, not future edits. A human decision must identify the branch/PR head actually reviewed. No PR is opened before the author's personal pre-PR review; push-triggered CI verifies the bounded branch first.

## GitHub Actions and review boundary

| Job | Actual configuration |
|---|---|
| static-quality | Ruff lint JSON, format check and pip check. |
| security-review | Bandit on application code, strict pre-resolved/hash-required audits of both locks, and a required name/version reconciliation step. Artifact hashes are verified during installation. |
| tests | Fresh runtime-only installation/import check before development dependencies, then pytest, JUnit and booking.py branch coverage; AppTest requires no browser/server. |
| quality-gate | Runs even when predecessors fail/skip; succeeds only when all three succeed. |

Events: main/codex branch pushes, PRs to main, and workflow_dispatch when available on the default branch. The workflow does not deploy or merge. The quality-gate job is suitable as a required check, but enforcement through repository rules must be confirmed separately before merging; a YAML job alone does not configure branch protection.

Actions are pinned to the inspected official release commits: checkout v7.0.1, setup-python v7.1.0 and upload-artifact v7.0.2. Hosted jobs install the committed locks with --require-hashes. Audit/network failures are failures; there is no continue-on-error bypass. Reports upload with always() and 14-day retention; retain material evidence for submission before expiry.

Run steps explicitly select Bash, enabling pipefail as well as fail-fast behaviour. This matters for pip-check/report pipelines: a successful tee must not hide the failing check. The isolated runtime reports record dependency consistency, imports and installed versions. These checks support a runnable foundation, not a deployed or functionally complete V1.0.

## L1 deep technical review

Review checkpoint: 3e3b98a37425f62c3f4c736f3452c5699008e301. Requested focus: accepted L0, Assessment 3/HD rubric, lecture requirements, Demo comparison, architecture, test quality, CI and honest AI/human records. Reviewer/executor: Codex AI assistant, also the implementation assistant; this is not an independent human review. The author requested corrections but has not supplied L1 ACCEPT_LOOP.

The review re-read assessment pages 3-5 and 8-13; the 16 November 09:40 transcript pages 1-2 and 8-10; the 10:46 transcript pages 1-7; and relevant original Week 3-9 supplementary slides. The supplied 09:40 and 10:45 transcript PDFs contain identical extracted text and are one account, not independent corroboration. These are automatic transcripts, not independently verified original audio. No source.md was created and the existing sources.md was left unchanged.

### Findings, assessment and disposition

| ID / priority | Affected location | Finding, evidence and correction | Owner / disposition |
|---|---|---|---|
| L1-RV01 / P2 | .github/workflows/quality-checks.yml: defaults.run.shell and pip-check pipelines | Unspecified Linux shell uses Bash without pipefail. A failed left-hand command piped to tee returned 0 in the control probe. Explicit shell: bash now makes the same probe return 1. This closes a latent false-green CI path; no actual broken installed dependency is claimed. | AI correction and local verification complete; author assessment PENDING. |
| L1-RV02 / P2 | test_booking.py: test_app_refresh_and_navigation_preserve_session_state | The old fixture seeded only a workshop, leaving registration state and the confirmed metric unchallenged. Three private app variants individually cleared registrations, reset the registration counter or counted cancelled records. The old selected test passed each; the strengthened snapshot/mixed-state test rejects each. The real 40-case suite passes. | AI test correction verified; author assesses the oracle and scope. |
| L1-RV03 / P2 | .github/workflows/quality-checks.yml: tests job | Installing only the development lock did not establish runtime-lock independence. Added a fresh runtime-only virtual environment, hashed install, pip check and app/domain/Streamlit imports before development installation. A fresh local environment passes without pytest installed. This was an evidence gap, not an observed runtime import failure. | AI CI correction locally verified; hosted revalidation required on the new commit. |
| L1-RV04 / P2 | This record's intake and AI-use record | Existing intake lacked a named, justified loop risk classification and reviewer route. Added separate foundation/correction risk recommendations, rationale, ownership and escalation conditions. No personal check or acceptance is invented. | Recording gap corrected; human risk judgement and ACCEPT_LOOP remain PENDING. |

Verification after these corrections is separate from the earlier hosted runs above. The current branch must pass its updated CI, including runtime isolation. app.py, booking.py, the accepted rules/risks, dependency locks and the author's L0 record are unchanged by this correction. No new dependency or application feature was introduced.

The pipeline probe follows [GitHub's documented shell semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell). The three mutation challenges are test-strength evidence from private copies; they are not reported as defects found in the unmodified application. The existing timestamp defect/regression history remains the actual L1 data-model defect example.

### Assessment and teaching alignment

| Assessment criterion / weight | Current L1 evidence | Required later evidence |
|---|---|---|
| Requirements/quality planning, 15% | Accepted FR/BR/QR/risk plan retained; foundation mappings, explicit limits and risk triage. | Implement and verify all release requirements; retain actual author decisions. |
| Functional app/deployment, 15% | Runnable three-file preview with independent data/state. | At least three meaningful working functions, two meaningful roles, reliable business rules and browser-accessible deployment. L1 alone does not satisfy this criterion. |
| V&V/testing, 20% | Specification review, 40 foundation cases, timestamp regression, stronger state/count oracle and negative CI-control probes. | Full B/W/I coverage, personal browser checks and genuine VAL-01/02/03 evidence. Green CI and AppTest do not establish user suitability. |
| Change/regression/release, 20% | Genuine focused branch/commits and preserved tests; no premature waitlist code or release claim. | Own working V1.0, then CR-01 impact analysis, branch, regression, focused review, justified PR decision, approved merge and V1.1. L1 fixes do not substitute for that assessed change. |
| GitHub/CI evidence, 15% | Actual hosted runs/artifacts, four configured jobs, immutable Action pins, complete audit sets and failure controls. | Issues/PRs/releases and current-code decisions as the later work occurs; repository-rule enforcement before merge. |
| Presentation/judgement, 15% | Precise reuse and AI contribution records plus actual findings to explain. | Author explains material code, independent expected cases, findings, risk and eventual merge rationale in the live defence. No grade or human understanding is certified by this review. |

This follows Module 3's proportionate planning/stage exits, Module 4's evidence-decision traceability, Module 5's requirement-driven test oracles, Module 6's intake/risk triage, Module 7's strong assertions/regression, Module 8's tool-versus-approval distinction and Module 9's pre-PR ownership. The teacher's example overlap and automatic-waitlist outcomes are not this project's requirements.

Technical outcome: corrections are locally verified and ready for hosted revalidation and author review. Human outcome: PENDING. L2: NOT_STARTED. A simple architecture is consistent with the lecture; it does not remove the final functionality, validation, controlled-change or defence requirements.

PR head, base, tested GitHub SHA and actual checked-out SHA are retained in reports. Pull-request runs may test GitHub's merge commit; head/base identity remains distinct. A current-head check is needed after relevant changes.

## AI task, assumptions and findings

AI generated the three core files, tests, dependency inputs/locks, tool configuration, workflow and record updates. AI inspected the pinned Demo's dataclass/session approach, chose foundation examples from the accepted rules, executed local checks and corrected formatting. The author supplied the task/design constraints; no new personal L1 observations or acceptance have been supplied.

| Item | Assessment / disposition | Human review needed |
|---|---|---|
| Initial formatting | Ruff reformatted all three generated Python files; subsequent checks pass. This was a formatting finding, not an observed business defect. | Inspect the final diff; no invented runtime defect is claimed. |
| Timestamp ordering | Further code review reproduced incorrect ordering of repeated local times. Four added cases failed before the two comparisons were changed to UTC; all 40 now pass locally. The initial 100% line/branch figure did not detect this missing input category. | Explain the intended instant-order property and review the regression evidence; keep the Singapore display policy. |
| Audit package coverage | The initial successful audits reported 33 runtime/67 development packages, while complete locks contain 34/71. Changed to documented --disable-pip with --require-hashes; final reports cover all 34/71 packages. Added required CI name/version reconciliation. Hash verification remains enforced during install. | Assess the complete-set evidence rather than relying on exit code alone. |
| Empty foundation preview | Intentional L1 scope. Business controls remain in later loops; no placeholder Book button returns fake success. | Confirm the bounded increment is appropriate. |
| Structural versus creation rules | Historical dataclasses are permitted; service-level lead/role checks remain L3 obligations. | Explain why constructing a row is not an authorised create operation. |
| Identity/session limits | Fictional data and independently resettable sessions retained. No real login, shared concurrency or durability claim. | Confirm the stated prototype limits. |
| AppTest versus user evidence | Test harness insertion exercises state preservation; it is not a real booking task or user validation. | Assess assertions, perform own checks and leave R-08 pending. |
| Dependency/platform scope | Locks generated on Python 3.12.14/Windows. Both initial and corrected hosted Ubuntu runs installed them successfully; corrected run 43868519549 passed all four jobs and 40 tests. | Review the actual branch/head identity and retained artifacts. |

No substantive human rejection/edit, external review or finding disposition is invented. Record such actions below when they actually occur. All future permission, capacity-allocation, atomic-operation and cutoff-action controls remain required by the accepted design.

## Personal acceptance checklist

All boxes remain unchecked until the author performs or reviews the stated work and records observations. Reading AI results is a review activity; running a command personally is execution. Record which occurred.

- [ ] **H01 Setup and preview:** Install from the committed lock or verify the existing environment, run Streamlit, visit all three views and Refresh view, and record errors/observations. Expect a clearly limited preview with no business controls.
- [ ] **H02 Architecture:** Explain in your own words what app.py, booking.py and test_booking.py own. Confirm no database, password login or shared mutable global business state was added.
- [ ] **H03 Independent expectations:** Before running selected cases, predict capacity 1/30/0/31/True and the known S/C result. Run or inspect the relevant parametrised tests, explain why unrelated failures are excluded, and record actual results.
- [ ] **H04 State evidence:** Inspect/run the complete-snapshot/mixed-status rerun and independent-session tests. Explain why the strengthened oracle rejects the three private faulty variants and what remains unproved about reload recovery, real concurrency and booking operations.
- [ ] **H05 CI and findings:** Inspect all four hosted jobs, runtime-isolation reports, shell/pipeline failure evidence and current code identity. Assess L1-RV01-L1-RV04 and the proposed risk levels. Later PR changes require current head/base checks; confirm repository-rule enforcement separately before merge.
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
| Foundation/correction risk classification and reviewer competence | NOT_RECORDED; AI recommendations above require human judgement |
| Decision | PENDING |

Exit requires relevant passing checks, assessed findings and actual human ACCEPT_LOOP. Merge/release decisions remain separate. R-08 validation remains pending. The next permitted implementation loop after acceptance is L2; no L2 work has been performed.
