# Outdoor Workshop Booking and Waitlist Management System

**Accepted: L0 revision 3 and L1-L4. Current: L5, HUMAN_REVIEW_PENDING. L6: NOT_STARTED.**

L5 starts from accepted L4/GitHub commit 2f2504acff79317c20760971acae2965ee98a1fb. The new author instruction permits own confirmed cancellation, released capacity and retained history. It supersedes the historical L4 hold for L5 development only. All five historical reviews and accepted local L0-L4 folders/archives remain unchanged.

## L5 implementation

| File | Responsibility |
|---|---|
| [app.py](app.py) | Existing views/forms plus own cancellation controls in My Bookings, fresh submission time, cutoff display/disabled controls and explicit-OK state adoption. |
| [booking.py](booking.py) | Pure operations over dataclasses/lists. New cancel_registration checks the stored owner and cutoff, retains history and releases one place. |
| [test_booking.py](test_booking.py) | 298 cases in 112 functions: all 250 prior cases/92 function ASTs/decorators unchanged, plus 48 L5 cases in 20 functions. |

Keep app.py -> booking.py -> Python data structures. No runtime module, database, framework, real login or dependency is added. The single-job Actions workflow and both dependency lock pairs remain unchanged.

### Cancellation contract

Cancel by registration ID. Check the selected participant role, actual target and stored owner. INVALID_ACTOR, FORBIDDEN and UNKNOWN_REGISTRATION preserve the entire input. An owned CANCELLED record returns ALREADY_CANCELLED without mutation/allocation, including at/after C or S. This no-op is checked before time closure.

An active confirmation requires fresh aware trusted time and t<C, where C=S minus 24 elapsed hours. Exactly C and later return REGISTRATION_CLOSED. Success changes the same row to CANCELLED, keeps its IDs/created_at, updates updated_at in UTC and leaves other rows and both counters unchanged. Return a complete new state with copied mutable lists; never mutate the input. Construction exceptions propagate without partial state. Only OK replaces the UI business state; ALREADY_CANCELLED is informational. No broad state repair or exception suppression is added.

One effective cancellation releases exactly one confirmed place. A subsequent eligible pre-C Book creates a new ID and preserves cancelled history. Repeating the old cancellation cannot release the newly booked place. FULL stays FULL. No waitlist/promotion or overlap restriction is added; serial allocation is tested, not simultaneous multi-user concurrency.

My Bookings exposes only the selected participant's confirmed targets. Locked/started controls are disabled; the business operation independently checks its decision time. Cancelled rows remain in History with no repeat button. Success feedback is actor-scoped. Selection, organiser failed drafts/errors and unrelated session data are retained.

### Preview scenario

In a fresh session, select Sam, open My Bookings and cancel registration-2 (Outdoor Photography Walk). The confirmed total drops from three to two; registration-2 and the existing registration-4 remain in History. Refresh must not release another place or allocate an ID. Switch to Xingjian and Book Photography: the released place becomes registration-5. Switch to Alex, open Organiser and select Photography: its roster contains Xingjian. Sam's cancelled row remains history. Xingjian's Trail Safety cancellation is disabled under the final-24h policy.

## Preserved behaviour and limits

Creation remains >24h with integer capacity 1-30, valid dates and current-organiser ownership. Fixed identities, hidden menus, independent business rejection, own-record filtering, owned rosters, once-per-session fixtures, L4-F05 defaults/reset and F08 failed-draft isolation are retained. No prior test function is adapted for L5.

L4-HF-01 reserved actual cancellation for an authorised L5; the new instruction now implements it. L4-HF-02's isolated refusal oracles and serial-only scope remain. L4-HF-03's author/AI evidence distinction remains. Historical L3 HF-02 and all accepted reviews retain their original bytes.

Use fictional data. Selection is not authentication or impersonation resistance. In-app refresh/reruns preserve the session; independent sessions are unshared and browser reload/new sessions/restart may reset data. Source rollback is not data recovery. No notifications, payments, weather API or emergency override is added. Full VAL/R-08 suitability and release/deployment evidence remain later work.

## Run and check

Use Python 3.12.14. From the repository or extracted archive root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8516 --server.headless true
```

Reuse an existing environment. In this workspace, from L5_develop use ..\.venv\Scripts\python.exe for the existing parent environment. Linux/macOS use the equivalent bin/python path. Runtime-only installation uses --require-hashes -r requirements.txt.

The live human preview is [http://127.0.0.1:8516](http://127.0.0.1:8516), retained for personal checks. AI browser sessions are separate. Relative demo dates initialise once; they are not fixed assessment dates.

## Design baseline documents

| Document | Content |
|---|---|
| [Requirements](requirements.md) | Unchanged canonical FR/BR/QR/risk targets and implemented L5 scope. |
| [Test plan](docs/test-plan.md) | Preserved scenarios, retained regressions and exact 48-case L5 mapping. |
| [Demo reuse](docs/demo-reuse.md) | Pinned reference and explained project-specific adaptation. |
| [AI use](docs/ai-use.md) | Actual tasks, assumptions/corrections and distinct human responsibility. |
| [L0](docs/reviews/L0-human-acceptance.md), [L1](docs/reviews/L1-human-review.md), [L2](docs/reviews/L2-human-review.md), [L3](docs/reviews/L3-human-review.md), [L4](docs/reviews/L4-human-review.md) | Unchanged historical decisions/feedback. |
| [L5 review](docs/reviews/L5-human-review.md) | Current intent/evidence/findings/risks and unchecked H01-H07. |

Historical next-loop holds describe earlier decisions. The new instruction authorises L5 only; its review is the current gate record. Put L5_develop contents at repository root on codex/l5-cancellation, including .github. The 22-file personal L5_develop.zip stays local with source at archive root. Do not commit/upload it or attach it to a release. Exclude private QA tools/reports/screenshots, environments, caches and course originals.

## Development workflow

The author sets intent and judges independent expected outcomes. AI implements bounded changes and discloses assumptions/corrections/evidence. The author inspects code/tests, performs actual checks, reviews findings/risks and records the next decision. Actions cannot provide human acceptance.

| Decision | Meaning |
|---|---|
| ACCEPT_LOOP | Accept the identified loop after personal review; a later loop needs a later instruction. |
| READY_TO_MERGE | Approve a reviewed PR with current checks and justified findings/risk dispositions. |
| ACCEPT_RELEASE | Approve verified deployment/release and required validation. |
| CHANGES_REQUIRED / SPECIALIST_ADVICE_REQUIRED | Correct findings or seek proportionate advice before dependent work. |

L5 UI/H01-H07, actual personal feedback/edits, risk judgement, reviewer/date and ACCEPT_LOOP are PENDING. No L4 checkmarks or independent CI-verification declaration are copied into L5. No PR, main merge, release or L6 work is included.

## Record for each loop

Record intended/preserved behaviour, FR/BR/QR/risk/test mapping, changed files, AI tasks/assumptions/corrections, independent oracles, actual executor/results, code identity, findings, reviewer/date/decision and residual limits. Record genuine human feedback and edited/rejected AI suggestions without inventing contributions. Link CI rather than committing generated logs.

## Loop plan

| Loop | Work and exit |
|---|---|
| L0-L4 | Accepted design, foundations, fixed roles, creation/rosters, booking/history and F08 isolation. |
| L5 | Own cancellation/history/capacity; stop pending UI/H01-H07 and ACCEPT_LOOP. |
| L6 | NOT_STARTED. Working V1.0 deployment/validation/release after separate authorisation. |
| L7-L8 | CR-01 waitlist impact/change, new/regression tests, validation and justified pre-merge decision. |
| L9 | Approved merge, deployment/release and final submission/defence evidence. |

## GitHub Actions

[quality-checks.yml](.github/workflows/quality-checks.yml) is byte-identical to L4: one job, Ubuntu 24.04/Python 3.12.14, isolated runtime installation/imports, locked development installation, Ruff/format, pip check, Bandit, complete audits and all tests with JUnit/booking branch coverage. Coverage is diagnostic, not a grade threshold.

Main/codex pushes and PRs to main trigger checks. Immutable Action pins, read-only permissions, tested/head/base identities, Bash/pipefail and failure reports remain. Reports expire after 14 days and are separate from the personal source ZIP. Current code/run evidence is in the L5 review.

## Version and submission evidence

L5 builds V1.0; it is not CR-01 or a release approval. Working V1.0 deployment/validation must precede the meaningful waitlist change/review/merge/release. Final repository/deployment URLs, PPTX, submission document, AI disclosure and oral defence remain required assessment work. Technical success here does not complete those obligations or guarantee an HD grade.
