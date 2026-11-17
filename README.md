# Outdoor Workshop Booking and Waitlist Management System

**Accepted: L0 revision 3 and L1-L3. Current: L4, HUMAN_REVIEW_PENDING. L5: NOT_STARTED.**

This classroom prototype manages fictional workshops and registrations in one browser session. L4 starts from accepted L3 commit 74f9281f420755a42141d9792c023cec5d53bf34. The author's explicit L4 instruction supersedes the earlier L4 hold, without accepting this new work. The three-file architecture remains Streamlit app.py -> pure Python booking.py -> dataclasses/lists, verified by test_booking.py and one Actions job.

## L4 development

| File | Responsibility |
|---|---|
| [app.py](app.py) | Existing fixed-role menus and creation form; participant Book controls, current-time submission, success/refusal feedback and personal current/history views. Adopt only an OK candidate. |
| [booking.py](booking.py) | Existing validated models, permissions, creation, browse, owned rosters and fixtures; book_workshop and list_own_registrations. No Streamlit import. |
| [test_booking.py](test_booking.py) | All 177 L1-L3 cases retained; 51 L4 cases, 228 total. This review retains all 221 preceding cases and adds seven. Requirements determine outcomes, not the teaching Demo's pass history. |

For a fresh session, select **Sam (PARTICIPANT)** and book **Outdoor Navigation Basics**. One new CONFIRMED record appears; the earlier CANCELLED record remains in History. My Bookings shows only Sam's records. Switch to Xingjian to inspect a different list, then Rui Yan's owned roster to see the updated participant list. A fresh Xingjian request for Outdoor Photography Walk returns FULL; a repeat request for Navigation returns DUPLICATE_ACTIVE. The final-24h and historical examples have disabled booking controls. There is no cancellation/Join action in L4.

### Booking contract

Use the latest same-session state. Resolve a valid participant, find the actual workshop, validate the aware trusted clock, enforce t<C, check active duplication, then capacity. C is S minus 24 elapsed hours; exactly C is closed, including after S. Full direct Book returns FULL without waitlisting. A cancelled record does not consume capacity or block a pre-cutoff rebooking. No overlap prohibition is added.

Success creates one new registration ID with CONFIRMED and equal creation/update instants, advances only next_registration_id once, and returns a complete state with independent mutable lists. The input snapshot remains unchanged. All refusals and construction exceptions preserve its records/counters. UI replacement occurs only after OK. Serial processing is assumed; no database transaction, concurrency guarantee or retry-idempotency token is claimed.

The business read derives the participant ID from the selected validated actor; it accepts no other person's ID. The UI splits returned records into upcoming CONFIRMED bookings and history (CANCELLED records or started workshops). This display grouping never changes stored status. Time/meeting point/IDs and original timestamps remain visible. Started CONFIRMED does not imply attendance or completion.

### Preserved behaviour and limits

Four fixed fictional identities, role menus, independent business checks, current-view reset, owned rosters, valid relative demo data, creation >24 hours ahead and capacity 1-30 are retained. Failed creation submissions retain all eight values/errors across navigation; only success clears the form. A failed draft may cross freely selectable demo roles within one session: use fictional data only.

L4-F05 is corrected: eight form defaults are initialised/restored in Session State before rendering, with no competing date/time/capacity widget defaults. Failed values remain intact; successful creation resets only those eight keys. Fresh-process tests and browser/server-log checks verify this without suppressing warnings.

In-app Refresh, navigation and actor switching retain that session's business state. New sessions are unshared; browser reload/server restart may reset data. Selection is not authentication or impersonation resistance. No database, real account, notifications, payments, weather API or emergency override is added. Outdoor preparation and weather/safety decisions remain with the organiser outside this prototype.

L4 adds no cancellation, waitlist, deployment or release approval. V1.0 still requires L5 cancellation and L6 release validation; V1.1 follows a separately reviewed CR-01. R-08 and VAL-01/02/03 remain pending real user suitability checks. Automated success does not guarantee an HD grade or replace assessment deliverables.

## Run and check

Use Python 3.12.14. From the repository/extracted archive root on Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8514 --server.headless true
```

Reuse an existing environment when available. Linux/macOS use .venv/bin/python. Runtime-only installation uses --require-hashes -r requirements.txt. Keep both input/lock pairs unchanged until a deliberate dependency revision.

The L4 personal preview is [http://127.0.0.1:8514](http://127.0.0.1:8514). Its temporary service is for human checking; the command is for a later restart. Earlier loop previews are separate. Tests/browser smoke runs are AI executions, not the author's acceptance.

## Design baseline documents

| Document | Content |
|---|---|
| [Requirements](requirements.md) | Accepted FR/BR/QR/risk definitions and current implemented subset. |
| [Test plan](docs/test-plan.md) | Preserved B/W/I/validation definitions; retained mapping and new L4 test groups. |
| [Demo reuse](docs/demo-reuse.md) | Pinned Demo, project-specific adaptation and course reference identifiers. |
| [AI use](docs/ai-use.md) | Significant tasks, assumptions, actual AI work and distinct human responsibility. |
| [L0 acceptance](docs/reviews/L0-human-acceptance.md) | Historical accepted design. |
| [L1 review](docs/reviews/L1-human-review.md), [L2 review](docs/reviews/L2-human-review.md), [L3 review](docs/reviews/L3-human-review.md) | Unchanged historical evidence/acceptance, including L3 H01-H07 and HF-01-HF-03. |
| [L4 review](docs/reviews/L4-human-review.md) | Current intent, evidence, findings, residual risks and unchecked H01-H07. |

Historical next-loop holds describe the decision at that time. The new instruction authorises L4 development only. Current gate status is in the L4 review.

L4_develop contents belong at repository root on codex/l4-bookings, including .github. The 21-file personal L4_develop.zip stays local, with the same source files at archive root. Do not upload/commit it or attach it to a release. ZIP extensions are ignored in any case. Environments, caches, reports, private QA scripts and course originals are excluded. Accepted local folders/archives and the original tracked working copy are preserved.

## Development workflow

The author sets intent/rules and evaluates independent expected results. AI implements the bounded task, reports corrections/assumptions and supplies automated evidence. The author inspects code, performs actual checks, reviews findings/limits and records the next decision. A green Actions job cannot provide human acceptance.

| Decision | Meaning |
|---|---|
| ACCEPT_LOOP | Accept the identified bounded candidate after personal review. A later loop begins only when requested. |
| READY_TO_MERGE | Approve a reviewed PR with current evidence and justified findings/risk dispositions. |
| ACCEPT_RELEASE | Approve a verified release/deployment with required validation. |
| CHANGES_REQUIRED / SPECIALIST_ADVICE_REQUIRED | Correct findings or obtain appropriate advice before dependent work. |

L3 ACCEPT_LOOP remains historical. L4 H01-H07, actual personal observations, justified risk disposition, reviewer/date and ACCEPT_LOOP are pending. Do not copy L3 checkmarks into L4. No PR, merge, release, L5 work or user validation is inferred from this delivery.

## Record for each loop

Record intended/preserved behaviour, FR/BR/QR/risk/test mapping, AI task/assumptions, actual changed files, independent oracles, actual executor/results, findings/corrections, code identity, reviewer/date/decision and residual risks. Record genuine human feedback and any rejected/edited AI suggestion; do not fabricate contributions. Link CI rather than duplicating generated logs.

## Loop plan

| Loop | Work and exit |
|---|---|
| L0-L3 | Accepted design, foundations, fixed identities/navigation, workshop creation/browsing/owned rosters. Historical records unchanged. |
| L4 | Participant booking and personal history; technical checks and personal H01-H07, then stop pending ACCEPT_LOOP. |
| L5 | Own cancellation, retained history, repeat safety and relevant regression/deadline/permission tests; not started. |
| L6 | Working V1.0, required deployment/validation and ACCEPT_RELEASE. |
| L7-L8 | CR-01 waitlist impact/implementation, regression/new tests, validation and justified pre-merge decision. |
| L9 | Approved merge, main/deployment smoke, V1.1 release and submission/defence evidence. |

## GitHub Actions

[quality-checks.yml](.github/workflows/quality-checks.yml) remains byte-identical to accepted L3: one quality-checks job, Ubuntu 24.04/Python 3.12.14, isolated runtime installation/import, locked development installation, Ruff/format, pip check, Bandit, complete audits of both locks and all pytest cases with JUnit/booking branch coverage.

Triggers remain main/codex pushes and PRs to main, with dispatch when available on default branch. SHA-pinned Actions, read-only permissions, recorded tested/head/base commits, Bash/pipefail and no bypassed failed checks are retained. Reports upload even after failures and expire after 14 days. Coverage is diagnostic, not a grade threshold. A quality report artifact is distinct from the personal project ZIP, which stays local.

## Version and submission evidence

Establish this project's functioning V1.0 before CR-01; retain meaningful commits, review/merge decisions, deployments and v1.0/v1.1 evidence. A code rollback cannot recover temporary booking data. The final assessment still needs repository/deployment URLs, PPTX, the specified submission document, change/review/merge/release links, AI disclosure and oral defence. This is an L4 development candidate, not a completed final submission.
