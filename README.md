# cp5401 Outdoor Workshop Booking and Waitlist Management System

A small, single-session prototype for one outdoor workshop provider. Participants reserve limited places and manage their own selected-demo-user records. Organisers create workshops and inspect their own rosters. Release V1.1 adds an explicit FIFO waitlist and automatic promotion before registration closes.

**Design baseline: L0 revision 3, accepted 16 November 2026. Current loop: L1. Human decision: PENDING. L2: NOT_STARTED.**

This repository now contains the L1 foundation under the accepted design: a runnable Streamlit shell, independent Python models/state factory, foundation tests and GitHub Actions. Participant/organiser operations, a working V1.0, waitlist change and deployment remain later work. The accepted functional design is unchanged.

## L1 delivery and review

See the [L1 work and human review record](docs/reviews/L1-human-review.md) for actual results, AI contributions, test mappings and the unchecked personal acceptance checklist. L0's seven-item author review remains preserved in its historical record. L1 requires its own actual ACCEPT_LOOP before L2.

| File | L1 responsibility |
|---|---|
| [app.py](app.py) | Preview views and once-per-session initialisation; no business-action controls yet. |
| [booking.py](booking.py) | Dataclasses, fictional identity data, independent state factories, structural field checks and derived cutoff. No Streamlit import. |
| [test_booking.py](test_booking.py) | Foundation checks and separate Streamlit AppTest smoke/state checks. |
| [requirements.txt](requirements.txt) / [requirements-dev.txt](requirements-dev.txt) | Resolved runtime and development versions with hashes; inputs are the corresponding .in files. |
| [pyproject.toml](pyproject.toml) | Pytest, Ruff and booking-module coverage configuration. |
| [quality-checks.yml](.github/workflows/quality-checks.yml) | Static quality, security review, tests and aggregate quality gate. |

### Run locally

Use Python 3.12.14. For an existing project virtual environment on Windows, run the commands below from the repository root. To recreate it with an installed Python 3.12 launcher, first run `py -3.12 -m venv .venv`.

```powershell
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

On Linux/macOS, create the environment with Python 3.12 and use `.venv/bin/python` in the same commands. Runtime-only installation uses `--require-hashes -r requirements.txt`. No secrets or database setup are needed.

The preview intentionally starts with no workshops or registrations. Navigation and Refresh view work; actor selection, creation, booking and cancellation are not implemented in L1. This is not application V1.0.

## Design baseline documents

The baseline consists of this README and the ten documents below. The two root Git configuration files support normal repository use; no L0 document-checking tool or generated report is required.

| Document | Purpose |
|---|---|
| [Requirements](requirements.md) | Problem, users, scope, releases, functional and quality requirements, architecture |
| [Business rules](docs/business-rules.md) | Sixteen rules, operation outcomes and the C/S timing matrix |
| [Risk register](docs/risks.md) | Risks, controls, planned acceptance and residual limitations |
| [Demo reuse](docs/demo-reuse.md) | Pinned source, file/function decisions and attribution |
| [Test plan](docs/test-plan.md) | B/W/I scenarios, independent test oracles and validation |
| [Traceability](docs/traceability.md) | Requirements, rules, risks, tests and development loops |
| [Development workflow](docs/development-workflow.md) | AI tasks, personal checks, outputs, progression gates and CI |
| [Human acceptance](docs/reviews/L0-human-acceptance.md) | Seven-item author self-review, written decision rationale and L0 acceptance record |
| [AI use and L0 review](docs/ai-use.md) | Actual assistance, design-review findings, human direction/acceptance and evidence limits |
| [Sources](docs/sources.md) | Assessment, lecture and technical references |

## Architecture and limits

    app.py -> booking.py -> dataclasses and in-memory lists
                 |
          test_booking.py -> pytest -> GitHub Actions

Use the teacher's simple file-based development approach. Streamlit owns views, fictional actor selection and session state; booking.py owns independently testable rules.

Within one preserved browser session, switching fictional participants and organisers uses the same state. Independent browser sessions do not share bookings. Browser reload, session recreation or server restart can reset data. In-app Refresh means a normal rerun, not browser reload.

Actor selection is not authentication. Visitors can select another fictional identity. Role/ownership checks are evaluated within that declared demo model; use fictional data only. This prototype makes no production identity, durability or shared-concurrency claim.

## Releases

| Release | Scope |
|---|---|
| V1.0 | Demo actors, creation/browsing, booking/cancellation, own history, organiser rosters, 24-hour policy, session state and quality checks. No waitlist. |
| V1.1 | CR-01 adds Join/Withdraw, FIFO, promotion and waitlist display while preserving baseline timing, roles, capacity and history contracts. |

Establish and accept an actual working V1.0 before implementing CR-01. A full Book request remains rejected in both releases; Join Waitlist is a separate V1.1 action.

## Timing policy

S is the workshop start, C = S - 24 elapsed hours, and t is trusted server decision time.

| Operation | t < C | C <= t < S | t >= S |
|---|---|---|---|
| Create the proposed workshop | Allow if otherwise valid | Reject | Reject |
| Book | Apply booking rules | Reject | Reject |
| Cancel CONFIRMED | Owner may cancel | Reject | Reject |
| Join waitlist | Apply V1.1 rules | Reject | Reject |
| Withdraw WAITLISTED | Owner may withdraw | Owner may still withdraw | Reject effective withdrawal |
| Promote | With effective confirmed cancellation | Prohibited | Prohibited |
| Read or repeat an owned CANCELLED record | Role/ownership rules | Same | Same |

Creation requires strictly more than 24 hours of lead time. In the final 24 hours, freeze the confirmed roster and close joining/promotion, but allow the waitlist to shrink through owner withdrawal. Withdrawal never changes confirmed places or triggers promotion.

## Current gate and evidence

The project author recorded the L0 Revision 3 ACCEPT_LOOP decision on 16 November 2026. The [acceptance record](docs/reviews/L0-human-acceptance.md) documents seven author self-review checks and a written decision rationale. This is a design acceptance decision, not independent reviewer approval or evidence of executed application tests.

The L0 design gate has been accepted by the project author. L1 is implemented and awaiting its own human review. ACCEPT_LOOP permits progression to the next bounded development task but does not approve a merge, deployment or release. The L0 documentation baseline and L1 foundation are not application v1.0.

Demo inspection and planned reuse are recorded directly in [Demo reuse](docs/demo-reuse.md). L0 findings and actual AI/human contributions are in [AI use](docs/ai-use.md). Future loops record the AI task, actual checks, human judgement and progression decision using the compact format in the [workflow](docs/development-workflow.md#record-for-each-loop).

R-08 user suitability remains pending the planned validation activities. Design acceptance is not evidence that the unimplemented controls work or that intended users accept the policy.

## GitHub baseline history

The repository was initialised before the L0 documentation was added. L1 starts from accepted main commit 822710b238bb14b8eba17cf2ab9a76ab2753bdb2. The separate codex/l1-foundation branch provides code and CI for personal review. Open a draft PR after the author's pre-PR review required by the workflow; do not merge or create application release tags as an automatic consequence of AI checks.

Keep supplied course PDFs, recordings, ZIPs, screenshots, private chat exports, local analysis and old drafts outside the repository. Their relevant references are recorded in Sources. Add application files, executable Actions, test results and later loop records only when that work actually occurs.

The next implementation step after L1 acceptance is L2, demo actors and ownership. L2 remains NOT_STARTED. Later design changes require a recorded reason, impact assessment and human decision rather than silently changing this baseline.

