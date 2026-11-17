# Outdoor Workshop Booking and Waitlist Management System

**Accepted design: L0 revision 3. L1/L2: ACCEPT_LOOP. Current loop: L3 workshop creation, browsing and owned confirmed rosters. Human decision: HUMAN_REVIEW_PENDING. L4: NOT_STARTED.**

A small classroom application for one outdoor workshop provider. It manages fictional workshop details and selected demo identities in one browser session. The simplified architecture remains Streamlit app.py -> Python booking.py -> dataclasses and in-memory lists, checked by test_booking.py and one GitHub Actions job.

## L3 development

| File | Responsibility |
|---|---|
| [app.py](app.py) | Role-specific navigation, workshop cards, creation form, current-time submission, owned roster selection and complete successful-state adoption. |
| [booking.py](booking.py) | Retained models/identity checks; creation, public ordering/counts, owned list/roster access, trusted clock and valid relative demo fixtures. No Streamlit import. |
| [test_booking.py](test_booking.py) | 158 parameter cases in 51 functions: all 87 L2 cases retained with documented UI-context/message adaptations, plus 71 L3 cases. |

| Fixed ID | Demo name | Role | Visible menu |
|---|---|---|---|
| None | No identity selected | Public | Workshops |
| organiser-1 | Rui Yan | ORGANISER | Workshops; Organiser |
| organiser-2 | Alex | ORGANISER | Workshops; Organiser |
| participant-1 | Xingjian | PARTICIPANT | Workshops; My Bookings |
| participant-2 | Sam | PARTICIPANT | Workshops; My Bookings |

Roles come from fixed canonical IDs. Hidden menus improve navigation; independent UI/business checks reject forbidden access. Same-role switches retain permitted views; disallowed views reset to Workshops. Organiser switches also reset obsolete roster selections to an owned target. Anyone may select a demo identity, so this is not authentication or impersonation protection.

L3 implements creation only when S-t>24 elapsed hours, integer capacity 1-30, valid aware times/end>S and required text. IDs/ownership are assigned by the application. Creation returns an outcome and complete new state without mutating the input; the UI adopts only OK results. A roster lookup checks the actual stored owner and returns confirmed records only.

## Demo data and limits

Each new session loads four relative workshops once: two open examples at least 48 hours ahead, including a full capacity-one workshop; one within its final 24 hours; one historical workshop. Both organisers have owned examples. Three confirmed registrations and one cancelled history row support counts/roster checks. The factory reconstructs legal creation seven days earlier and pre-cutoff registrations; seeded history is not a new booking feature.

In-app Refresh, navigation and identity changes retain business data. New browser sessions do not share it; reload or restart may reset it. Select the intended organiser before filling a creation form; unsubmitted drafts are not promised across reruns/navigation. Use fictional data only. Weather and on-site safety decisions remain with the organiser outside this prototype.

Booking, own booking history, cancellation, waiting, notification, account management, durable/shared storage and concurrent multi-user guarantees remain outside L3. Displayed closure labels explain the approved policy; later operations must enforce their own deadlines. This preview is not V1.0, the assessed deployment, or completed user validation.

## Run and check

Use Python 3.12.14. From the extracted repository root on Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8513 --server.headless true
```

With an existing environment, reuse it. Linux/macOS use Python 3.12 and .venv/bin/python. Runtime-only installation uses --require-hashes -r requirements.txt. No secrets/database setup is required.

The retained L3 preview is [http://127.0.0.1:8513](http://127.0.0.1:8513). Use the running service for personal checks; the command above is for a later restart. L2's separate preview remains at port 8512.

Keep requirements.in/requirements.txt and requirements-dev.in/requirements-dev.txt. Inputs/locks and tool versions are unchanged from accepted L2. Regenerate locks deliberately when dependencies change, then rerun checks.

## Design baseline documents

| Document | Content |
|---|---|
| [Requirements](requirements.md) | Project purpose, implemented L3 subset, accepted FR/BR/QR definitions and risk controls. |
| [Test plan](docs/test-plan.md) | Preserved B/W/I/validation definitions, retained L2 mapping and exact L3 test groups. |
| [Demo reuse](docs/demo-reuse.md) | Pinned teaching reference, adaptation decisions and course sources. |
| [AI use](docs/ai-use.md) | Significant AI tasks, actual execution and separate human responsibility. |
| [L0 acceptance](docs/reviews/L0-human-acceptance.md) | Historical accepted design. |
| [L1 review](docs/reviews/L1-human-review.md) | Historical foundation and acceptance. |
| [L2 review](docs/reviews/L2-human-review.md) | Historical navigation/permission work, findings and author acceptance. |
| [L3 review](docs/reviews/L3-human-review.md) | Current scope, findings, verification, risk judgement and pending H01-H07 checklist. |

Historical L0/L1/L2 records are unchanged and describe their decision dates, including then-current next-loop holds. The author's new L3 instruction supersedes that earlier hold for this loop. Current status belongs in the L3 review.

L3_develop contents belong at the GitHub repository root on codex/l3-workshops, including .github. The delivery ZIP contains the same 20 files at its archive root. It excludes virtual environments, caches, generated reports, course originals and private checking tools. Accepted local L0/L1/L2 folders and the original working copy remain unchanged.

## Development workflow

The author sets intent, constraints and expected behaviour; AI implements the bounded task and records evidence; the author checks understanding, independent outcomes, selected personal executions and findings before approving progression. Record actual executor and reviewer separately.

| Human decision | Scope |
|---|---|
| ACCEPT_LOOP | Accept this bounded loop; begin a later loop only when requested. |
| READY_TO_MERGE | Approve a reviewed PR using current evidence and resolved findings. |
| ACCEPT_RELEASE | Approve a verified deployment/release with required validation. |
| CHANGES_REQUIRED / SPECIALIST_ADVICE_REQUIRED | Correct or seek suitable advice before dependent work. |

AI/CI are evidence rather than approval. L3 stops at HUMAN_REVIEW_PENDING; L4 is NOT_STARTED. No PR, merge or release is included. Use the [L3 checklist](docs/reviews/L3-human-review.md#human-acceptance-checklist) for actual reviewer/date/code identity, observations, human edits/rejected suggestions, risk rationale and the decision. Do not generate personal observations from AI tests.

## Record for each loop

Record the intended/unchanged behaviour, FR/BR/risk scope, significant AI task, affected files/assumptions, independent test expectations, actual executor/results, findings/dispositions, code identity and human reviewer/date/decision. The author supplies actual personal checks, edits/rejected suggestions and justified risk rationale; AI/CI evidence remains separately labelled. Link current CI rather than duplicating logs.

## Loop plan

| Loop | Work and exit |
|---|---|
| L0-L2 | Accepted design, foundations and navigation/permission checks; historical decisions retained. |
| L3 | Current workshop creation/browsing/owned rosters/demo data. Tests/CI plus H01-H07 and ACCEPT_LOOP required. |
| L4-L5 | Booking/own history, then cancellation/repeats; relevant baseline, permission, state and deadline tests. |
| L6 | Working V1.0, deployment, required baseline validation and ACCEPT_RELEASE. |
| L7-L8 | CR-01 waitlist intake/impact, implementation, new/regression tests, validation, findings and justified pre-merge decision. |
| L9 | Approved merge, main/deployment smoke, V1.1 release and submission/defence material. |

Full B/W/I scenarios remain required at their release stage. L3 presentation checks do not complete future Book/cancellation deadlines or real-user validation; R-08 remains pending.

## GitHub Actions

[quality-checks.yml](.github/workflows/quality-checks.yml) is unchanged from accepted L2: one quality-checks job, Python 3.12.14, isolated runtime installation/imports, locked development install, Ruff/format, pip check, Bandit, complete audits of both locks and pytest/JUnit/booking branch coverage.

The workflow runs on main/codex pushes and PRs to main, with manual dispatch when available on the default branch. SHA-pinned Actions, read-only permissions, Bash/pipefail, no bypassed failures and always-uploaded reports remain. Reports identify tested/head/base commits and expire after 14 days; retain material evidence before expiry. Coverage is diagnostic, not a grade threshold.

## Version and submission evidence

Establish this project's functioning V1.0 before CR-01; retain meaningful branches, commits, PR decisions and v1.0/v1.1 releases. A code rollback does not recover temporary booking data.

Final submission still needs repository/deployment URLs, PPTX, a short submission document with release/change/review/merge links, AI disclosure and oral defence as specified by the assessment. This L3 delivery supplies development evidence, not a completed final submission.
