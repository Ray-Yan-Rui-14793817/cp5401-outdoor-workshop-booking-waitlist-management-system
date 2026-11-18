# Outdoor Workshop Booking and Waitlist Management System

**Accepted: L0 revision 3 and L1-L5. L6: HUMAN_REVIEW_PENDING. L7: NOT_STARTED. Release: PENDING.**

This classroom prototype helps participants find/book outdoor workshops and organisers prepare confirmed rosters. V1.0 integrates fixed demo identities, creation, browsing, booking, own cancellation/history and owned rosters. CR-01 waiting/FIFO is later work, after the separate V1.0 release decision. The author owns requirements, expected behaviour, review, acceptance and release; AI/Actions provide explicitly labelled technical work.

## V1.0 scope and architecture

| File | Responsibility/current change |
|---|---|
| [app.py](app.py) | Streamlit controls, selected identity and temporary session state. The deep review adds a read-only, once-per-session source/Git/Python/runtime-package log for deployment verification; no business behaviour changes. |
| [booking.py](booking.py) | Dataclasses/lists and pure operations. Byte-identical to accepted L5. |
| [test_booking.py](test_booking.py) | 317 cases/119 functions. All 308 initial-L6 cases/116 test function ASTs/decorators remain; nine review cases strengthen final-State failure and runtime-provenance evidence. |

Keep app.py -> booking.py -> Python data structures. No new framework, database, login, runtime module or waitlist feature is introduced. [Actions](.github/workflows/quality-checks.yml) remains the same single job, Python 3.12.16, pinned Actions, read-only permissions and all checks. requirements.in/requirements.txt/requirements-dev.txt change only to constrain existing PyArrow to 24.0.0; requirements-dev.in and all other pin/hash blocks remain unchanged.

Rui Yan/organiser-1 and Alex/organiser-2 are ORGANISER; Xingjian/participant-1 and Sam/participant-2 are PARTICIPANT. Identity selection is freely switchable, not real authentication. Hidden menus supplement business-layer canonical role/actual stored-owner checks. Use fictional data only.

S is the aware start instant; C=S-24 elapsed hours; t is trusted fresh server decision time. Creation requires S-t>24h, end>S and integer capacity 1-30. Booking/effective confirmed cancellation require t<C. Exactly C and later refuse active changes even with spare capacity. An owned CANCELLED repeat is ALREADY_CANCELLED without further allocation/release, even after C/S. Full Book returns FULL without waiting; pre-C rebooking creates a new ID and retains cancelled history. Failed creation preserves eight submitted values/errors by organiser ID; success resets only that organiser's form. Unsubmitted edit persistence is not promised.

All business data belongs to one temporary browser session. Reruns, Refresh view and identity changes preserve it. Independent sessions do not share allocation; reload/new session, restart or deployment may reset it. Reinitialisation is not persisted recovery. Shared concurrency, durable records, notifications, real login, weather decisions and emergency overrides are outside scope.

## Deployment and run

| Target | Evidence/limit |
|---|---|
| Aligned local review preview | http://127.0.0.1:8520, Python 3.12.14/PyArrow 24.0.0 in the isolated revised-lock environment. Retained for human checks. |
| Existing preview | http://127.0.0.1:8518 is preserved, but its earlier environment still has PyArrow 26.0.1. It is not revised-environment parity evidence. |
| Hosted candidate | [https://cp5401-outdoor-workshops-v1.streamlit.app/](https://cp5401-outdoor-workshops-v1.streamlit.app/) |
| Source coordinates | Repository branch codex/l6-v1-integration; repository-root app.py and requirements.txt; Python 3.12 selected. |
| Current reviewed source | [cb9b1f6bc9883c3e3162a98209b4b0de6b4193df](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/cb9b1f6bc9883c3e3162a98209b4b0de6b4193df); documentation-only follow-up heads have their own Actions checks. |

VERIFIED - L6-F10/L6-F11 CLOSED_TECHNICAL_FOR_TESTED_TARGET. The author explicitly authorised one controlled reboot of the existing candidate. Actual cloud runtime logs observed at 18 November 2026 17:42:47 UTC+08:00 report Git SHA 2cad4b53899f5827c0d51cfb298c49f704d77b6b, exactly the codex/l6-v1-integration HEAD at execution; Python 3.12.16, Streamlit 1.67.0 and PyArrow 24.0.0. All 34 installed project runtime pins exactly match requirements.txt, with no missing packages or version differences; SHA256 of app.py, booking.py and requirements.txt exactly matches the local/GitHub source. The new 09:42 UTC build installs Arrow 24.0.0 directly and has no new Arrow replacement event. Hosted business workflows were rerun against this attested application. Subsequent evidence-only commits must be identified separately and their unchanged application/lock blobs compared; never relabel the actually logged deployment SHA. Human validation, ACCEPT_LOOP and release remain PENDING.

Cloud initially installed locked PyArrow 26.0.1, then explicitly replaced it with 24.0.0. The author authorised only this pin/hash correction. pip-tools 7.7.0 regenerated both locks from the existing inputs/locks with generated/reused hashes and --upgrade-package=pyarrow; runtime 34/development 71 pins retain every unrelated pin/hash block. Streamlit 1.67.0 declares pyarrow!=25.0.0,<27,>=12.0.0, which admits 24.0.0. The provider's warning references an upstream issue about 25.0.0; no 26.0.1 crash in this project was reproduced. This is alignment with the observed provider, not proof that 24.0.0 is the only generally compatible release. Platform-added logging/installer packages are outside the project's 34 runtime pins.

From repository/extracted-archive root, create or deliberately update an environment for the current locks:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest test_booking.py
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8520 --server.headless true
```

An already running earlier environment does not automatically adopt lock changes. Runtime hosting uses requirements.txt, not requirements-dev.txt. No secrets or external data service is required. The metadata log contains only code identity and package versions, no actor, booking or environment-secret values; an absent local .git is explicitly unknown.

## Verification evidence

| Check | Actual result |
|---|---|
| Revised-lock local regression | 317 passed in 80.97s on Python 3.12.14/PyArrow 24.0.0; no failures/errors/skips. All original 308 cases/123 prior top-level test/helper ASTs remain unchanged. |
| Local quality/security | Ruff, formatting, Bandit and pip check PASS. Strict full-lock pip-audit: 34 runtime and 71 development packages, no omitted/skipped packages or known vulnerabilities at execution. This is not a complete managed-platform audit. |
| Source-candidate CI | PASS: observed deployed source 2cad4b53899f5827c0d51cfb298c49f704d77b6b, [run 44276124671](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44276124671), job 134704585509, Python 3.12.16, 317 passed in 55.48s, no failures/errors/skips; one job/all 18 steps successful. Its downloaded artifact 14415250708 verifies tested SHA/JUnit317, all 308 old case identities, all 34 installed runtime pins, complete strict 34/71-package audits and no known vulnerabilities/omissions. Ruff/format/Bandit/pip check/runtime-only imports pass; diagnostic booking coverage is 99%. This is the executed runtime candidate result; a later documentation-only HEAD receives its own Actions/artifact check before delivery. |
| Independent boundary audit | 16 decisions: active Create/Book/Cancel at C-1/C/C+1/S plus distinct owned-CANCELLED repeats; required outcome, full State/history/counters/input properties pass. Separate private audit, not extra pytest cases. |
| Oracle challenge | Two private faulty copies each passed all original 308 tests; the new final-candidate tests reject late Create/Book counter mutation (two failing routes per copy). Genuine booking.py was already correct and remains unchanged. |
| Coverage | 99% booking diagnostic: 200 statements/one missing, 70 branches/one partial. The existing demo-fixture guard is unexecuted. Coverage/counts are not completeness or grade guarantees. |
| Revised hosted smoke | PASS after the authorised controlled reboot, executed by AI in a fresh connected CUA Chrome session. Baseline 4 workshops/3 confirmations; eligible Xingjian receives FULL on Photography without allocation. Rui fails creation for missing meeting point, all eight submitted values remain exact; Alex has a blank title/no Rui error and switching back restores all eight. Correction creates workshop-5, then resets title/meeting point/notes and capacity to 10. Xingjian books the new capacity-2 workshop as registration-5; repeating with one place still free returns DUPLICATE_ACTIVE. Sam books registration-6. Cancel only Xingjian registration-5: total confirmations 5->4 and the freshly painted roster still contains Sam registration-6. Xingjian rebooks as registration-7: total 5, old registration-5 remains CANCELLED in History, and Rui's final roster contains exactly confirmed 6/Sam and 7/Xingjian. Alex's choices contain only his workshops 4/2. These are AI technical executions, not human validation. Final refresh/session/console observations are recorded in the controlled-restart section. |
| Actual restart | Only the isolated 8520 process was restarted. Cancellation 4 workshops/2 confirmations was lost; after reconnect/rerun the factory restored 4/3 and registration-2 CONFIRMED. Sam's widget selection survived, while view/business state reinitialised. Existing 8518/cloud were not stopped. |

DEPLOYMENT_VERIFIED_FOR_OBSERVED_RUNTIME; L6-F10/F11 CLOSED_TECHNICAL_FOR_TESTED_TARGET. L6 remains HUMAN_REVIEW_PENDING; H01-H07, VAL-01/VAL-02, residual-risk judgement and ACCEPT_LOOP are PENDING. V1.0 release approval is NOT_AUTHORISED; L7 NOT_STARTED.

## Controlled restart evidence

The author authorises one reboot only; no second manual reboot, app deletion/recreation or GitHub access expansion is performed. Reboot logs show disconnect at 09:42:02 UTC, the new branch build at 09:42:07, dependencies processed at 09:42:19 and server start at 09:42:21. The actual source/package record was independently compared at 18 November 2026 17:42:47 UTC+08:00. Temporary data reinitialises from the earlier 5/4 session to factory 4/3, with no selected identity; this is not persisted recovery.

The [deployment evidence and all 34 installed versions](docs/reviews/L6-human-review.md#controlled-restart-resolution) preserve the previously open finding, actual authorisation, exact observed Git/source/package identity and post-reboot business flow. Application code, tests, policies, workflow and all four dependency input/lock files are unchanged in this evidence-resolution update.

## Demonstration and validation

Use a fresh session for fixture IDs and retain it throughout each task. Photography starts full, Navigation open, Trail Safety inside the final 24h and Past Nature Walk historical. The open-window caption describes time; counts show fullness. This accepted wording limit remains.

VAL-01: as Sam cancel Photography registration-2 before C, retain history and release one place; as Xingjian book it as registration-5, then inspect own records and Alex's roster. Explain S/C, full versus locked, location/preparation and identity/reset limits. VAL-02: as Rui create a capacity-1 workshop >24h away, first omit meeting point, correct retained fields, observe one new workshop/reset, book as a participant and inspect owned versus other-organiser lists. Judge whether the strict freeze/cancellation rule supports the intended organising task.

AI browser checks are verification. Genuine author role-play/external tester observations and policy suitability decisions remain PENDING in [L6 review](docs/reviews/L6-human-review.md#validation-record). R-08 remains VALIDATION_PENDING; near-C promotion/awareness scenarios VAL-03A-03E remain V1.1 work. Twenty-four hours before start does not guarantee discovery of promotion before C.

## Design baseline documents

| Document | Purpose |
|---|---|
| [Requirements](requirements.md) | Unchanged canonical FR/BR/QR/risk definitions and current subset. |
| [Test plan](docs/test-plan.md) | Canonical scenarios, current mappings, oracles and validation tasks. |
| [Demo reuse](docs/demo-reuse.md) | Pinned source, explained adaptations and course/technical references. |
| [AI use](docs/ai-use.md) | Actual AI work, corrections and human contribution boundary. |
| [L6 review](docs/reviews/L6-human-review.md) | Findings, source/environment/results, seven unchecked human tasks and decisions. |
| [L0](docs/reviews/L0-human-acceptance.md), [L1](docs/reviews/L1-human-review.md), [L2](docs/reviews/L2-human-review.md), [L3](docs/reviews/L3-human-review.md), [L4](docs/reviews/L4-human-review.md), [L5](docs/reviews/L5-human-review.md) | Byte-identical accepted historical reviews/feedback. |

Put L6_develop contents at repository root, including .github. The 23-file L6_develop.zip is personal/local only, with files at archive root. No ZIP, environment, cache, private QA script/log/screenshot/report or course original enters GitHub. Normal 14-day Actions quality-report artifacts are separate from the personal source ZIP.

## Development workflow

The author sets scope, requirements and independent expectations. AI implements bounded work, discloses assumptions/findings and runs labelled checks. The author personally reviews code/evidence, performs H01-H07 and VAL tasks, judges risk and issues a candidate-specific decision. Green CI and AI review never supply that decision.

## Record for each loop

Record scope/preserved behaviour, affected files, FR/BR/QR/risk/test mapping, independent oracles, actual executor/environment/source SHA, findings/dispositions, personal observations/edits/rejected suggestions, residual-risk rationale, reviewer/date and decision. Distinguish planned from executed controls and AI verification from human validation.

## Loop plan and release gate

| Gate | Status/condition |
|---|---|
| L0-L5 | ACCEPT_LOOP; historical evidence retained. |
| L6 technical | Current evidence/finding status above; still HUMAN_REVIEW_PENDING. |
| L6 human | H01-H07, VAL-01/VAL-02, actual feedback/risk judgement and ACCEPT_LOOP are PENDING. |
| Merge | READY_TO_MERGE is a distinct explicit decision; reviewed-main CI/deployment must then be verified. No main merge is authorised here. |
| Release | ACCEPT_RELEASE, formal v1.0 tag and GitHub Release remain unauthorised/PENDING. ACCEPT_LOOP alone does not approve release. |
| L7/CR-01 | NOT_STARTED. No waiting/FIFO code is added; a working approved V1.0 precedes the assessed change. |

## GitHub Actions

The unchanged quality-checks job runs on main/codex pushes, PRs to main and dispatch. It records tested/head/base identity; verifies isolated hash-locked runtime imports; installs the development lock; checks Ruff/format/pip consistency/Bandit; strictly audits every runtime/development pin; executes all tests with JUnit/booking branch coverage; and uploads reports. No failure bypass or weakened assertion is added. Current-head Actions/artifact results must be checked independently of historical runs.

The later CR-01 issue/impact/branch/PR/review/justified merge/V1.1 release, final assessment submission and oral defence remain future work. The technical candidate does not establish a final HD outcome.
