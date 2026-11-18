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

OPEN - L6-F10/L6-F11. Real manager logs confirm configured codex/l6-v1-integration/root app.py, Python 3.12.16/Streamlit 1.67.0 and the original installation's PyArrow 26.0.1 -> 24.0.0 replacement. After publication, fresh page/session checks still expose only that initial 05:09 UTC build log and no L6_RUNTIME_IDENTITY record. Therefore the exact current deployed SHA, three revised source digests and all 34 installed runtime pins have NOT been independently established. Hosted native workflows work, but they are not proof that cb9b1f6 or the revised requirements are deployed. Keep the existing service available; do not reboot/delete/recreate it or expand GitHub access as part of this preserved-service check. DEPLOYMENT_CONDITION_NOT_MET until an actual revised deployment and source/package match are observed.

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
| Source-candidate CI | PASS: source candidate cb9b1f6bc9883c3e3162a98209b4b0de6b4193df, [run 44252306874](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44252306874), job 134625664411, Python 3.12.16, 317 passed in 89.16s, no failures/errors/skips; one job/all 18 steps successful. Runtime-only hash install/imports and all 34 runtime versions match the revised lock (PyArrow 24.0.0/Streamlit 1.67.0/Pandas 3.1.1). Ruff/format/pip check/Bandit and strict 34/71-package dependency audits PASS, no known vulnerabilities/skips/omissions. Artifact 14403844500 was downloaded and verified for SHA256 d49f47bd29b05c251da58495051b8e1a6172bd630f03c0bc0719f3a23de600ca, CRC, tested SHA/JUnit317 and report contents; expires 2 December 2026. A later records-only HEAD still requires its own current-head check. |
| Independent boundary audit | 16 decisions: active Create/Book/Cancel at C-1/C/C+1/S plus distinct owned-CANCELLED repeats; required outcome, full State/history/counters/input properties pass. Separate private audit, not extra pytest cases. |
| Oracle challenge | Two private faulty copies each passed all original 308 tests; the new final-candidate tests reject late Create/Book counter mutation (two failing routes per copy). Genuine booking.py was already correct and remains unchanged. |
| Coverage | 99% booking diagnostic: 200 statements/one missing, 70 branches/one partial. The existing demo-fixture guard is unexecuted. Coverage/counts are not completeness or grade guarantees. |
| Revised hosted smoke | PASS for the currently served, source-unattested instance, executed by AI using connected CUA Chrome (1707x876); separate public/no-owner IAB (912x871) renders meaningful 4-workshop/3-confirmation data. Fresh Chrome Sam cancels registration-2 (confirmations 3->2), then rebooks Photography as registration-5 (2->3); History keeps cancelled 2/4. Rui's missing-meeting-point submission keeps title/capacity/notes/dates/times and consumes no workshop ID; Alex has blank title/no Rui error, and Rui's own failure restores. Correction creates only workshop-5 and resets his fields (title empty/capacity 10). Xingjian books it as registration-6; the freshly painted Rui roster shows registration-6/participant-1/Xingjian/CONFIRMED with totals 5/4. Refresh view retains 5/4; a separate unchanged Chrome session stays 4/3. Console error/warning collection is empty. These are technical observations, not current-source deployment proof, human validation or mobile-specific testing. |
| Actual restart | Only the isolated 8520 process was restarted. Cancellation 4 workshops/2 confirmations was lost; after reconnect/rerun the factory restored 4/3 and registration-2 CONFIRMED. Sam's widget selection survived, while view/business state reinitialised. Existing 8518/cloud were not stopped. |

LOCAL_AND_CI_VERIFIED_FOR_TESTED_SCOPE; CLOUD_SOURCE_AND_ENVIRONMENT_PROOF_UNRESOLVED; DEPLOYMENT_CONDITION_NOT_MET. L6-F10/F11 remain OPEN. V1.0 is not release-ready or approved; human validation/acceptance and release decisions remain PENDING.

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
