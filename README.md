# Outdoor Workshop Booking and Waitlist Management System

**Accepted: L0 revision 3 and L1-L6. L6: ACCEPT_LOOP. L7: NOT_STARTED / HELD_BY_AUTHOR. Merge/tag/V1.0 release: NOT_AUTHORISED.**

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
| Actual cloud checkout / reviewed branch | Cloud [2cad4b53899f5827c0d51cfb298c49f704d77b6b](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2cad4b53899f5827c0d51cfb298c49f704d77b6b); intake [78cdce5ce906ea0f42aad03cb346e21ccf0c0c16](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/78cdce5ce906ea0f42aad03cb346e21ccf0c0c16). Different commit identities; verified difference is documentation only, with identical executable/lock content. |

REVERIFIED at 18 November 2026 18:07:04 UTC+08:00 from a newly generated cloud runtime record. Actual checkout SHA is 2cad4b53899f5827c0d51cfb298c49f704d77b6b; review intake HEAD is 78cdce5ce906ea0f42aad03cb346e21ccf0c0c16. They are NOT the same Git commit. GitHub comparison establishes that the intake is one commit ahead with exactly six modified Markdown files; all runtime/test/dependency/configuration/workflow blobs are unchanged. Cloud SHA256 of app.py, booking.py and requirements.txt exactly matches the current L6 branch, Python is 3.12.16, Streamlit is 1.67.0, and all 34 installed runtime pins match requirements.txt, including PyArrow 24.0.0, with zero missing/version differences. F10/F11 remain technically closed for the verified executable/lock target; literal checkout-versus-documentation-HEAD equality is explicitly not claimed. No new server reboot is performed in this review. Later evidence-only heads are checked for the same non-runtime delta and have their own CI. At this 18 November technical stage, human validation and ACCEPT_LOOP were still pending. The author supplied UI/H01-H07 completion, VAL-01/02 results and ACCEPT_LOOP on 19 November; the current human acceptance record supersedes that gate. Merge/tag/release remain NOT_AUTHORISED.

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
| Fresh local regression | 317 passed in 76.81s on Python 3.12.14/PyArrow 24.0.0; no failures/errors/skips. All original 308 cases/123 prior top-level test/helper ASTs remain unchanged. |
| Local quality/security | Ruff, formatting, Bandit and pip check PASS. Strict full-lock pip-audit: 34 runtime and 71 development packages, no omitted/skipped packages or known vulnerabilities at execution. This is not a complete managed-platform audit. |
| Reviewed branch CI | Accepted-candidate CI: [run 44284607153](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44284607153) tests 5c1e3ff92168b34397e2bee2ace85431ae4d124e; job 134733904416, Python 3.12.16, 317 passed in 55.10s, zero failures/errors/skips, one job/all 18 steps successful. Runtime/development audits cover all 34/71 pins without known vulnerabilities or omissions. Artifact 14418996361 (quality-checks-44284607153-1) was independently checked for digest/CRC, exact tested SHA, all 317 case identities, quality reports and all 34 installed runtime versions. This accepted candidate and subsequent acceptance-record heads have unchanged executable/test/lock/workflow files relative to the observed cloud checkout. The records-only acceptance commit receives a separate exact-head Actions/artifact check; this run is not relabelled as that later result. |
| Independent boundary audit | 16 decisions: active Create/Book/Cancel at C-1/C/C+1/S plus distinct owned-CANCELLED repeats; required outcome, full State/history/counters/input properties pass. Separate private audit, not extra pytest cases. |
| Oracle challenge | Two private faulty copies each passed all original 308 tests; the new final-candidate tests reject late Create/Book counter mutation (two failing routes per copy). Genuine booking.py was already correct and remains unchanged. |
| Coverage | 99% booking diagnostic: 200 statements/one missing, 70 branches/one partial. The existing demo-fixture guard is unexecuted. Coverage/counts are not completeness or grade guarantees. |
| Revised hosted smoke | PASS in a new AI-operated CUA Chrome session: eligible Xingjian receives FULL on seeded Photography; Alex submits a new workshop with capacity 0 and otherwise valid fields, receives only the capacity error and retains all eight inputs. Rui has blank title/no Alex error; switching back restores Alex's exact invalid zero and all other values. Correction to capacity 2 creates workshop-5 under Alex and resets only his form. Sam receives registration-5; a repeat while one place remains returns DUPLICATE_ACTIVE. Xingjian receives registration-6, then cancels only that second attendee. Sam registration-5 remains CONFIRMED in Alex's actual roster. Xingjian rebooks as registration-7; own History keeps CANCELLED registration-6 and unrelated 1/3 remain confirmed. Final Alex roster contains exactly confirmed 5/Sam and 7/Xingjian; Rui's choices exclude Alex workshop-5. These are fresh technical observations, not genuine human validation or direct inspection of all internal State. |
| Historical local restart check | During the earlier isolated 8520 check, cancellation 4/2 reset to factory 4/3 and registration-2 CONFIRMED; Sam widget selection could survive. That event did not stop 8518/cloud. |
| Subsequent authorised cloud restart | The separately authorised single cloud reboot at 09:42 UTC supplied actual source/version evidence and reinitialised the temporary session. This further review performs zero additional server restarts and preserves services. |

APPLICATION_AND_RUNTIME_LOCK_PARITY_VERIFIED; DOCUMENTATION_ONLY_CHECKOUT_DELTA_EXPLICIT. F10/F11 remain closed for the verified executable target, without claiming that the actual cloud checkout equals a later documentation HEAD. L6: ACCEPT_LOOP by the author on 19 November 2026; UI/H01-H07 complete, VAL-01 9/9 and VAL-02 10/10 accepted within classroom scope. R-08 baseline timing/session suitability is ACCEPTABLE_WITHIN_SCOPE; V1.1 waiting/promotion validation remains pending. L7: NOT_STARTED / HELD_BY_AUTHOR. Main merge, tag and V1.0 release: NOT_AUTHORISED; ACCEPT_LOOP is not ACCEPT_RELEASE.

## Controlled restart evidence

The author authorises one reboot only; no second manual reboot, app deletion/recreation or GitHub access expansion is performed. Reboot logs show disconnect at 09:42:02 UTC, the new branch build at 09:42:07, dependencies processed at 09:42:19 and server start at 09:42:21. The actual source/package record was independently compared at 18 November 2026 17:42:47 UTC+08:00. Temporary data reinitialises from the earlier 5/4 session to factory 4/3, with no selected identity; this is not persisted recovery.

The [deployment evidence and all 34 installed versions](docs/reviews/L6-human-review.md#controlled-restart-resolution) preserve the previously open finding, actual authorisation, exact observed Git/source/package identity and post-reboot business flow. Application code, tests, policies, workflow and all four dependency input/lock files are unchanged in this evidence-resolution update.

## Further deep-review result

The [fresh L6 review](docs/reviews/L6-human-review.md#further-l6-deep-review) rechecks code/independent oracles, all 317 tests, a separate 16-decision clock/state matrix, actual runtime identity and the opposite organiser/participant order. No business-code, test, lock, policy or workflow repair is required. The necessary corrections are record clarity: label the local/cloud restart chronology separately and distinguish an actual deployed checkout from a later documentation-only branch head. Complete 34-pin parity does not imply identical Git commit IDs or a full platform/security certification.

## Demonstration and validation

Use a fresh session for fixture IDs and retain it throughout each task. Photography starts full, Navigation open, Trail Safety inside the final 24h and Past Nature Walk historical. The open-window caption describes time; counts show fullness. This accepted wording limit remains.

VAL-01: as Sam cancel Photography registration-2 before C, retain history and release one place; as Xingjian book it as registration-5, then inspect own records and Alex's roster. Explain S/C, full versus locked, location/preparation and identity/reset limits. VAL-02: as Rui create a capacity-1 workshop >24h away, first omit meeting point, correct retained fields, observe one new workshop/reset, book as a participant and inspect owned versus other-organiser lists. Judge whether the strict freeze/cancellation rule supports the intended organising task.

The author personally declared UI/H01-H07 and VAL-01/02 complete on 19 November 2026 (Asia/Shanghai, UTC+08:00), accepted candidate [5c1e3ff92168b34397e2bee2ace85431ae4d124e](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/5c1e3ff92168b34397e2bee2ace85431ae4d124e) and supplied seven actual feedback items across two messages. VAL-01 is author-reported PASS 9/9; VAL-02 is PASS 10/10, both ACCEPTABLE_WITHIN_SCOPE for the classroom prototype. The cutoff supports equipment, activity, transport and safety preparation; late cancellations remain restricted and must be explained. Confirmed records do not guarantee attendance or require unsafe participation; private emergencies may cause absence. Temporary session data is acceptable only for the declared demonstration. These are human judgements, separate from AI browser verification. See [human acceptance and feedback](docs/reviews/L6-human-review.md#current-human-acceptance). R-08 baseline suitability is accepted within this scope; V1.1 near-C promotion/discovery VAL-03A-03E remains VALIDATION_PENDING.

## Design baseline documents

| Document | Purpose |
|---|---|
| [Requirements](requirements.md) | Unchanged canonical FR/BR/QR/risk definitions and current subset. |
| [Test plan](docs/test-plan.md) | Canonical scenarios, current mappings, oracles and validation tasks. |
| [Demo reuse](docs/demo-reuse.md) | Pinned source, explained adaptations and course/technical references. |
| [AI use](docs/ai-use.md) | Actual AI work, corrections and human contribution boundary. |
| [L6 review](docs/reviews/L6-human-review.md) | Findings, source/environment/results, completed author-declared H01-H07, actual validation feedback and separate release gates. |
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
| L6 technical | Verified executable/lock target and accepted-candidate evidence above; acceptance-record HEAD receives its own CI. |
| L6 human | ACCEPT_LOOP for 5c1e3ff92168b34397e2bee2ace85431ae4d124e; author declares UI/H01-H07 and VAL-01 9/9, VAL-02 10/10 complete, with actual policy/session/safety feedback. |
| Merge | READY_TO_MERGE is a distinct explicit decision; reviewed-main CI/deployment must then be verified. No main merge is authorised here. |
| Release | ACCEPT_RELEASE, formal v1.0 tag and GitHub Release remain unauthorised/PENDING. ACCEPT_LOOP alone does not approve release. |
| L7/CR-01 | NOT_STARTED / HELD_BY_AUTHOR. This loop acceptance does not authorise the next loop; a separately approved released V1.0 precedes the assessed change. |

## GitHub Actions

The unchanged quality-checks job runs on main/codex pushes, PRs to main and dispatch. It records tested/head/base identity; verifies isolated hash-locked runtime imports; installs the development lock; checks Ruff/format/pip consistency/Bandit; strictly audits every runtime/development pin; executes all tests with JUnit/booking branch coverage; and uploads reports. No failure bypass or weakened assertion is added. Current-head Actions/artifact results must be checked independently of historical runs.

The later CR-01 issue/impact/branch/PR/review/justified merge/V1.1 release, final assessment submission and oral defence remain future work. The technical candidate does not establish a final HD outcome.
