# Outdoor Workshop Booking and Waitlist Management System

**Accepted: L0 revision 3 and L1-L5. Current: L6 V1.0 candidate, HUMAN_REVIEW_PENDING. L7: NOT_STARTED.**

This classroom prototype helps participants find and book outdoor workshops and helps organisers prepare confirmed rosters. V1.0 provides creation, browsing, booking, own history and cancellation. CR-01 will add explicit waiting and FIFO promotion only after the V1.0 release gate.

L6 starts from accepted L5 commit 8a5c9723afe6a81bbafc634acc09b65dac436ee4. The author's new instruction authorises this integration/deployment/verification loop and supersedes the earlier L6 hold. It does not supply personal L6 observations or acceptance. Original L0-L5 review records and local folders/archives remain unchanged.

## V1.0 scope and architecture

| File | Responsibility and L6 change |
|---|---|
| [app.py](app.py) | Streamlit views, selected demo identity, session data and explicit-OK adoption. Only the module description and visible candidate label change in L6. |
| [booking.py](booking.py) | Dataclasses/lists and pure business operations. Byte-identical to accepted L5. |
| [test_booking.py](test_booking.py) | All 306 L1-L5 cases/115 functions and decorators retained. One new parametrised UI journey adds two integration cases. |

Keep app.py -> booking.py -> Python data structures. No database, framework, login, runtime module or dependency is added. [Single-job Actions](.github/workflows/quality-checks.yml), configuration and dependency locks retain L5 bytes.

V1.0 implements FR-01-FR-07: fixed identity/role selection, public workshop information, booking, own cancellation/history, creation and owned rosters. The two organisers are Rui Yan/organiser-1 and Alex/organiser-2; participants are Xingjian/participant-1 and Sam/participant-2.

S is workshop start, C=S minus 24 elapsed hours, and t is trusted server decision time. Creation requires S-t>24h, end>S and integer capacity 1-30. New booking and effective confirmed cancellation require t<C. Exactly C and later reject active changes even if spare capacity exists. Only the stored owner can cancel; an owned CANCELLED repeat returns ALREADY_CANCELLED without changing state or freeing another place, including after C/S. Book at capacity returns FULL and never adds a waiter. Rebooking before C creates a new ID and keeps cancelled history.

Failed creation retains all eight submitted values and field errors for that organiser's stable ID. Success resets only that organiser's form. Participant/no-identity menus hide organiser operations, while booking.py independently checks role/actual-target ownership. Roles are freely selectable; this is not real authentication or protection against deliberate identity switching.

Use fictional data only. All business data belongs to one temporary browser session. In-app Refresh view, reruns and identity changes preserve that session; independent sessions do not share bookings. Browser reload/new sessions, server restart or deployment may reset it. This does not provide durable records, concurrent shared allocation, notifications, weather decisions or emergency overrides. Full user suitability remains a human validation question.

## Deployment and run

| Target | Current evidence |
|---|---|
| Human preview | http://127.0.0.1:8518; retained for L6 personal checks. |
| Hosted V1.0 candidate | DEPLOYMENT_PENDING |
| GitHub coordinates | codex/l6-v1-integration; repository-root app.py and requirements.txt. |
| Python | Local/Actions 3.12.14. Select managed Python 3.12 for Community Cloud; record the actual hosted patch when exposed. |
| Deployment identity | DEPLOYMENT_IDENTITY_PENDING |

From the repository or extracted archive root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8518 --server.headless true
```

Reuse an existing environment. In this workspace, from L6_develop use ..\.venv\Scripts\python.exe. Linux/macOS use bin/python. Runtime deployment uses the unchanged hash-locked requirements.txt, not requirements-dev.txt; no secrets or external data service are needed.

Community Cloud selects repository/branch/entrypoint and follows later commits on that branch. Check the final head's CI and hosted smoke behaviour after any update. This working branch is a review deployment; promotion to reviewed main and the v1.0 tag require the distinct human decisions below. A running preview is not a released baseline.

## Demonstration and validation

Start with a fresh demo session. Photography is full, Navigation is open, Trail Safety is inside the final 24h and Past Nature Walk is historical. Inspect full/open/closed/started information before choosing an action. The open-window caption describes time; the counts independently show a full workshop, a retained L3/L5 accepted wording limit.

For VAL-01, as Sam cancel registration-2/Photography before C: its same ID becomes CANCELLED, total confirmations fall from three to two, and cancelled registration-4 is retained. As Xingjian, Book the released Photography seat: new registration-5, confirmed total three. As Alex, inspect Photography's confirmed roster. Explain C versus S, own records, identity selection and reset limits.

For VAL-02, as Rui create a capacity-1 workshop more than 24h away with meeting point/preparation. First omit the meeting point: fields/errors persist and no ID is consumed. Correct it: one new workshop and a success-only form reset. Book as a participant, inspect Rui's owned roster and compare Alex's list. Judge whether the 24h freeze supports preparation and whether its cancellation restriction is acceptable for this demonstration.

AI walkthroughs verify specified behaviour. They do not supply intended-user feedback or a human suitability judgement. The author can perform declared role-play; identify it honestly rather than inventing external testers. [L6 validation/acceptance](docs/reviews/L6-human-review.md#validation-record) keeps observations, rationale and decisions pending until supplied. R-08 remains open; the near-C promotion/awareness scenarios VAL-03A-VAL-03E belong to V1.1.

## Verification evidence

| Check | Actual result |
|---|---|
| New integration journey | 2 passed, 306 deselected, 3.47s. Creates through the actual form and serially books/cancels/rebooks that same new workshop. |
| Complete local regression | 308 passed, 66.67s, zero failures/skips, Python 3.12.14. All 306 prior case identities/115 test function ASTs and decorators retained. |
| Local static checks | Ruff, format check, Bandit and pip check PASS. |
| Diagnostic booking coverage | 99%; existing demo-fixture error guard is the only unexecuted statement. Coverage and case count do not establish completeness or a grade. |
| Current L6 Actions | CI_PENDING |
| Actual browser/deployment smoke | BROWSER_PENDING |

The capacity-1 integration path isolates eligible FULL versus DUPLICATE_ACTIVE. It cannot alone detect cancelling all attendees; retained L5 multi-attendee/order/owner oracles provide that evidence. Existing active cutoff fixtures remain separate from cancelled-repeat no-ops. New journey checks do not replace unit, failure-injection or boundary tests.

## Design baseline documents

| Document | Purpose |
|---|---|
| [Requirements](requirements.md) | Preserved FR/BR/QR/risk definitions and L6 scope. |
| [Test plan](docs/test-plan.md) | Canonical scenarios, exact retained/new tests and validation tasks. |
| [Demo reuse](docs/demo-reuse.md) | Pinned Demo architecture/code explanation and sources. |
| [AI use](docs/ai-use.md) | Actual AI tasks, assumptions/corrections and human responsibility. |
| [L6 review](docs/reviews/L6-human-review.md) | Intake, changes, findings, actual evidence, deployment, H01-H07 and human decisions. |
| [L0](docs/reviews/L0-human-acceptance.md), [L1](docs/reviews/L1-human-review.md), [L2](docs/reviews/L2-human-review.md), [L3](docs/reviews/L3-human-review.md), [L4](docs/reviews/L4-human-review.md), [L5](docs/reviews/L5-human-review.md) | Byte-identical accepted historical decisions/feedback. Their earlier next-loop holds describe those dates. |

Put L6_develop contents at repository root on codex/l6-v1-integration, including .github. The 23-file L6_develop.zip stays personal/local with source at archive root. Exclude project ZIPs, environments/caches, private checks/logs/screenshots/reports and course originals from GitHub. Normal Actions quality-report artifacts are separate and expire after 14 days.

## Development workflow

The author sets scope and independent expected behaviour. AI implements bounded work, runs labelled checks and discloses assumptions/findings. The author inspects the candidate, performs H01-H07/VAL tasks, judges risk and records the actual decision. Actions and AI review cannot approve on the author's behalf.

## Record for each loop

Record scope/preserved behaviour, affected files, FR/BR/QR/risk/test mapping, independent oracles, actual executor/environment/source identity, findings/dispositions, human observations/risk rationale/reviewer/date/decision and remaining limits. Keep generated technical execution separate from personal verification. Record only actual human edits, rejected suggestions and feedback.

## Loop plan and release gate

| Stage | Status/next condition |
|---|---|
| L0-L5 | ACCEPT_LOOP, preserved history. |
| L6 technical candidate | V1.0 integration/deployment/verification; HUMAN_REVIEW_PENDING. |
| L6 personal gate | H01-H07, VAL-01/VAL-02 and manual I06/I08/I09; actual feedback and ACCEPT_LOOP pending. |
| V1.0 release gate | Resolve material findings/user needs; obtain READY_TO_MERGE, verify reviewed main CI/deployment, then ACCEPT_RELEASE and v1.0. RELEASE_PENDING. |
| L7-L9 | NOT_STARTED. A later explicit author instruction and working released V1.0 precede CR-01/waitlist. |

The release note is prepared: V1.0 introduces fixed demo roles, creation >24h/capacity 1-30, browsing, serial booking/own cancellation/history/owned rosters and strict C. It discloses temporary unshared state, no authentication/notifications and no waiting. This text is a release preparation, not an existing tag or approval.

## GitHub Actions

One unchanged quality-checks job runs on main/codex pushes, PRs to main and manual dispatch: isolated runtime installation/imports; locked development install; Ruff/format, pip check, Bandit, complete dependency audits and every test with JUnit/booking branch coverage. Action SHAs are pinned, permissions read-only, failures are not bypassed and head/base/tested identity is recorded. Current commit-specific evidence belongs in the L6 review.

The assessed CR-01 Issue/impact/PR/review/merge/V1.1 lifecycle, final submission URLs/PPTX/document/AI disclosure and oral defence remain later work. Green checks or this loop's implementation do not guarantee an HD result.
