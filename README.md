# Outdoor Workshop Booking and Waitlist Management System

**Design: accepted L0 revision 3. L1: ACCEPT_LOOP. Current L2 navigation revision: ACCEPT_LOOP, 17 November 2026 (Asia/Singapore). UI/H01-H07: AUTHOR_CONFIRMED_COMPLETE. L3: NOT_STARTED, held at the author's explicit request.**

A classroom prototype for one outdoor workshop provider. The application uses Streamlit, Python dataclasses/lists and temporary data in one browser session. Independent sessions do not share bookings; reload or restart may reset data. Fictional identity selection is not secure login.

## L2 development

| File | Responsibility |
|---|---|
| [app.py](app.py) | Fixed demo identity selection, role-specific menus, independent preview access checks, safe view reset, refresh and once-per-session initialisation. |
| [booking.py](booking.py) | Existing models/time contracts plus resolve_actor and check_permission. No Streamlit dependency. |
| [test_booking.py](test_booking.py) | 42 L1 cases plus 45 L2 cases: 87 total. Two L1 UI functions retain role-appropriate identity preconditions and their original assertions. Deep review consolidates duplicate no-identity cases and strengthens public-content/transition checks. |

| Fixed ID | Demo name | Fixed role |
|---|---|---|
| organiser-1 | Rui Yan | ORGANISER |
| organiser-2 | Alex | ORGANISER |
| participant-1 | Xingjian | PARTICIPANT |
| participant-2 | Sam | PARTICIPANT |

The selector starts with no identity and supports clearing. Roles come from the fixed ID records; there is no separate role editor.

| Selected identity | Visible menu |
|---|---|
| None | Workshops |
| PARTICIPANT | Workshops, My Bookings |
| ORGANISER | Workshops, Organiser |

Switching or clearing an identity resets a no-longer-permitted view to Workshops before rendering the menu. A permitted view remains selected on a same-role switch. Invalid saved views also reset safely. Menu filtering improves navigation; independent UI and booking.py permission checks still reject unauthorised access. Only explicit OK admits a private preview; unknown view/results are denied. Anyone may select another demo identity, so these checks are not authentication or impersonation protection.

L2 starts with no workshops or registrations. Creation, booking/cancellation and roster operations follow later loops. check_permission compares a valid actor's role and an optional trusted owner ID; it does not look up or modify a target. Complete B10/B12/B13 require actual operations in L3-L5. The accepted timing/capacity policies remain in [requirements.md](requirements.md); L2 is not application V1.0.

## Run and check

Use Python 3.12.14. With an existing project environment on Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8512
```

To create the environment with an installed Python 3.12 launcher, first run `py -3.12 -m venv .venv`. On Linux/macOS, use Python 3.12 to create it and use `.venv/bin/python`. Runtime-only installation uses `--require-hashes -r requirements.txt`. No secrets or database setup are required.

Local manual-preview URL after startup: http://127.0.0.1:8512. The current review keeps this local service running for the author. It is a development preview, not the assessed deployed release.

Keep both pairs of dependency files: requirements.in/requirements.txt and requirements-dev.in/requirements-dev.txt. The .in files specify inputs; the .txt files are generated version/hash locks. Dependency updates regenerate both locks using their recorded commands and rerun the checks. No dependency version or hash changed in L2.

## Design baseline documents

| Document | Primary content |
|---|---|
| [Requirements](requirements.md) | Overview, roles, releases, FR/BR/QR definitions and risk controls. |
| [Test plan](docs/test-plan.md) | B/W/I scenarios, validation and traceability. |
| [Demo reuse](docs/demo-reuse.md) | Reference versions, adaptation decisions and references. |
| [AI use](docs/ai-use.md) | Significant tasks and actual AI/human contributions. |
| [L0 acceptance](docs/reviews/L0-human-acceptance.md) | Historical author decision and seven recorded checks. |
| [L1 review](docs/reviews/L1-human-review.md) | Historical findings/results and author-confirmed ACCEPT_LOOP. |
| [L2 review](docs/reviews/L2-human-review.md) | Deep-review findings, course alignment, AI/CI evidence and author-confirmed UI/H01-H07 completion with ACCEPT_LOOP. |

For GitHub delivery, the contents of L2_develop belong at the repository root, including the hidden .github directory. Use codex/l2-identities for L2 verification. The [L2 review](docs/reviews/L2-human-review.md#verification-results) identifies actual results/commit/run. Local L0_develop, L1_develop and the original working copy remain unchanged.

Each topic has one primary location. Historical L0/L1 records describe their decision dates, including the then-current next-loop status. Current status belongs in the L2 review. Those historical records are retained unchanged from the accepted L1.

## Development workflow

The author bounds the task and expected behaviour before AI changes files. AI implements that scope and produces evidence. The author then understands material code, checks independent expected outcomes, performs selected personal checks and assesses findings before a PR. Record actual executor and reviewer separately. If intent, policy or competence is unresolved, stop dependent work and seek suitable advice.

| Human decision | Scope |
|---|---|
| ACCEPT_LOOP | Accept this bounded loop and permit the next requested loop. |
| READY_TO_MERGE | Current PR, CI and findings justify merge. |
| ACCEPT_RELEASE | Deployment, smoke checks and required validation justify release. |

Use CHANGES_REQUIRED or SPECIALIST_ADVICE_REQUIRED when appropriate. AI and CI do not grant these human decisions. Relevant changes after a decision require renewed review. Label author self-review honestly; do not invent an independent reviewer.

## Record for each loop

Use a short record in docs/reviews/ containing the task/FR/BR/risk scope, preserved behaviour, AI tool and significant task, affected files/assumptions, human edits or rejected suggestions, actual checks with expected/observed results and executor, findings/dispositions, code identity, risk rationale and the dated human decision. Link CI evidence rather than repeating logs. Never fill personal observations from AI execution.

## Loop plan

| Loop | AI task and outputs | Personal check | Exit condition |
|---|---|---|---|
| L0 | Requirements, rules, risks, reuse and test plan. | Review scope/policies and explain the design. | ACCEPT_LOOP recorded in the historical L0 record. |
| L1 | Three-file foundation, real tests, locks and CI; current simplified documents. | Reproduce setup, understand boundaries and assess the L1 checklist. | SATISFIED: author declared H01-H07 complete and supplied ACCEPT_LOOP on 17 November 2026; see the L1 review. |
| L2 | Fixed-ID selection, role-specific menus and independent role/owner checks. | Check visible menus, switch/reset behaviour, access rejection and identity limits. | SATISFIED: author declared updated UI/H01-H07 complete and supplied ACCEPT_LOOP on 17 November 2026. L3 remains NOT_STARTED at the author's request; complete B10/B12/B13 through later actual operations. |
| L3 | Creation, browsing, rosters and valid demo fixtures. | Check >24h/=24h/<24h, input types, S/C and ownership. | B03-B06, unchanged-input rejection and CI pass; ACCEPT_LOOP. |
| L4 | Booking and own history using latest serial state. | Check last place, duplicates, actor changes and stale submission. | B07-B10 and relevant I01/I02/I10 pass; ACCEPT_LOOP. |
| L5 | Cancellation, history, repeats and failure safety. | Check owner denial, cutoff, no-op and full-state preservation. | B11-B17 and relevant I05/I10/regression pass; ACCEPT_LOOP. |
| L6 | Working baseline, deployment and V1.0 evidence. | Perform VAL-01/VAL-02 and manual I06/I08/I09; inspect actual reset limits. | Baseline FR/BR/QR, CI and required validation pass; ACCEPT_RELEASE before CR-01. |
| L7 | CR-01 intake/impact, branch, Join/Withdraw/positions and I07 fixtures. | Check post-C withdrawal, rejected Join, confirmed-list equality and FIFO positions. | Increment checks pass; ACCEPT_LOOP only. Incomplete promotion is not release-ready. |
| L8 | Promotion, full regression and focused change review. | Assess oracles, failures/repeats, VAL-03 and R-08; complete personal review before PR. | Complete change, current checks and resolved blockers support READY_TO_MERGE. |
| L9 | Main deployment, smoke evidence, V1.1 and submission materials. | Decide merge, inspect main CI/deployed behaviour and release limits. | Verified deployed commit, validation and ACCEPT_RELEASE. |

Loop-level foundation evidence is partial support for later scenarios. Complete business scenarios remain required before V1.0/V1.1 release; permission-helper tests alone do not complete B10/B12/B13. L2 does not fulfil the assessment's functioning-application, validation or release criteria yet.

The earlier L2 acceptance remains in Git history. The author has now accepted the updated navigation/deep-review candidate 2e014b273f555af2f011968a1352a77c833c634d and declared its UI/H01-H07 complete. This update records that human statement without changing code or tests. L3 remains NOT_STARTED at the author's explicit request. READY_TO_MERGE and ACCEPT_RELEASE are separate decisions. The local preview remains running as requested.

## GitHub Actions

[quality-checks.yml](.github/workflows/quality-checks.yml) now has one job, **quality-checks**. It runs isolated runtime installation, Ruff/formatting, pip check, Bandit, both lock audits and audit-completeness reconciliation, then pytest/JUnit/branch coverage. Setup and development installation happen once. Checks after installation still run to retain useful evidence if another check fails; no failure is bypassed.

The workflow retains SHA-pinned Actions, read-only contents permission, hash installation, explicit Bash/pipefail and reports uploaded even on failure. Reports include head/base/tested identity and tool versions, with 14-day retention. Preserve material evidence for submission before expiry. Coverage is diagnostic, not an HD threshold.

Events remain main/codex pushes, PRs to main and manual dispatch when the workflow is on the default branch. The single job's failure status replaces the old aggregate job. If repository rules require the old quality-gate name, update the required check to quality-checks before merging. L2 ends at the human loop gate; PR, merge and release decisions remain separate.

## Version and submission evidence

Keep actual commits, small codex branches and working v1.0/v1.1 releases. Establish this project's working V1.0 before implementing CR-01. A code rollback does not restore temporary booking data.

Submit the repository/app URLs, PPTX, short submission document linking releases/CR/review/merge decisions, and AI-use documentation as specified in the assessment. Demonstrate the app and GitHub evidence and explain actual findings, test choices and human decisions. Course PDFs, recordings and local analysis stay outside the repository.
