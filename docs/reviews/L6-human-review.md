# L6 V1.0 Integration, Deployment and Deep Review

**L6: HUMAN_REVIEW_PENDING. Human decision: PENDING. L7: NOT_STARTED. Merge/release: NOT_AUTHORISED.**

## Intake and accepted base

Client date: 18 November 2026 (UTC+08:00). Accepted L5 branch head: 8a5c9723afe6a81bbafc634acc09b65dac436ee4. Initial L6 review base: fc964bb7bde9476e98aaabfee85ff8ab15156300. Revised source: [cb9b1f6bc9883c3e3162a98209b4b0de6b4193df](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/cb9b1f6bc9883c3e3162a98209b4b0de6b4193df). Preserve original accepted L0-L5 reviews, L3 HF-02, L4-F08 and all five actual L5 feedback items in [L5 history](L5-human-review.md#current-human-acceptance). No old human checkmark transfers to L6.

The author authorises this technical review, bounded repairs, GitHub/local ZIP updates and retained services. After the actual cloud mismatch is identified, they specifically permit necessary PyArrow pin/hash correction with existing tools, no fabricated hashes or unrelated upgrades. They require an open deployment finding if revised environment/function proof fails. Neither instruction is personal validation, ACCEPT_LOOP, main merge, ACCEPT_RELEASE, tag, GitHub Release or L7/CR-01 authority.

## Intended and preserved behaviour

V1.0 implements FR-01-FR-07. Preserve all 39 canonical FR/BR/QR/risk rows and 51 scenario rows; integer capacity 1-30; creation strictly >24h; C=S-24h; new Book/effective confirmed Cancel only t<C; valid canonical actor/actual stored ownership; no active duplicate; CANCELLED history/new-ID pre-C rebooking; owned cancelled-repeat ALREADY_CANCELLED even after C/S; exact input/counter integrity. Full Book does not waitlist. No policy, data model, persistence, authentication, shared concurrency, notification, new framework or waitlist feature is added.

app.py retains UI/session responsibilities and adds a bounded read-only deployment identity log. booking.py retains accepted L5 bytes, independent role/target ownership and pure complete-State operations. test_booking.py retains all 308 intake cases/116 test ASTs/decorators plus seven helpers and appends nine cases in three functions. requirements.in and both locks change only the authorised existing Arrow pin/hash; requirements-dev.in, pyproject.toml and the entire single-job workflow remain unchanged. All 33 runtime/70 development unrelated pin/hash blocks are identical. Six current English documents change; no delivery file is added. Delivery remains 23 files/12 Markdown documents.

## Independent findings and dispositions

| ID | Actual observation, correction/evidence and status |
|---|---|
| L6-F01 (initial) | Initial generated insertion interrupted an old test. Focused failures/Ruff caught it; restore accepted source and append properly. Historical test-placement correction, not a product defect. |
| L6-F02 (initial) | Add two real-control serial Create -> Browse -> Book -> Cancel -> Rebook -> History/Roster journeys. Retained, including two role permutations and exact IDs/full-State expectations. |
| L6-F03 (initial) | Deployment form defaulted to Python 3.14; select 3.12. Managed Python is 3.12.16. Initial job patch aligned from local 3.12.14 to 3.12.16. Exact source/runtime proof is strengthened by F10/F11 below. |
| L6-F04 | Green tests/AI role-play do not establish useful user policy. VAL-01/VAL-02 and residual-risk judgement are HUMAN_VALIDATION_PENDING. |
| L6-F05 (initial) | Manager detects requirements.txt and tool-only pyproject.toml, but explicitly selects root requirements.txt with uv. Keep necessary configuration; no evidence of wrong dependency input. DISMISSED_WITH_EVIDENCE. |
| L6-F06 (initial) | Browser radio-input automation and stale canvas cells gave unreliable intermediate evidence. Use visible semantic labels and a fresh painted state/screenshot. Verification-method correction, not a manufactured product defect. |
| L6-F07 (initial) | Full-plus-duplicate tests refusal precedence, not isolated B09. Exact-C disabled controls are not stale-submit I10. Correct mapping; keep spare-capacity duplicate and fresh-time tests unchanged. |
| L6-F08 | A private Create counter mutation before final DemoState construction, undone on ordinary success, passes all 308 intake cases (53.97s). Add Create domain/UI final-construction failure checks; two new tests reject it. Genuine creation was correct. ORACLE_GAP_CORRECTED. |
| L6-F09 | Equivalent private Book mutation passes all 308 old cases (53.58s). Add Book domain/UI final-construction checks; two new tests reject it. Genuine booking was correct. ORACLE_GAP_CORRECTED. |
| L6-F10 | Initial deployment record only established branch/head-at-launch, not independently observed remote SHA/package parity. Add read-only root Git/source/Python/runtime-package log and five metadata tests. Close only against actual revised hosted observation below. |
| L6-F11 | Real build installs locked Arrow 26.0.1 then replaces it with 24.0.0. Initial lock/runtime parity claim was incomplete. Author permits targeted correction; pip-tools regenerates consistent 24.0.0 locks with 50 generated Arrow hashes each and no unrelated pin/hash change. Installed Streamlit permits 24.0.0. Current deployment disposition is recorded below; CI alone cannot close it. |
| L6-F12 | Initial reset disclosure lacked an actual process-restart observation. Isolated revised-lock 8520 stop/start plus native reconnect/rerun confirms factory reset 4/2 -> 4/3, original registration-2 CONFIRMED. Existing 8518/cloud preserved. VERIFIED_RESET_SEMANTICS, not data recovery. |

The fault copies exist only in private evidence. No genuine late mutation was found in booking.py; improving test oracles is the actual repair. No original assertion/function/parameter is weakened. New tests isolate valid actors/open clocks/capacity, inject only final State failure, assert exact original records/list identity/counters and check the UI retains actor/submitted fields with no false success. The four creation/booking paths supplement retained late cancellation/multiple-attendee/clicked-target tests. Coverage alone had not revealed these gaps.

## Verification results

| Check | Actual result/executor/limit |
|---|---|
| Revised-lock local full suite | AI; Python 3.12.14, PyArrow 24.0.0: 317 passed in 80.97s, no failures/errors/skips. All 308 intake case identities and 123 prior top-level test/helper ASTs/decorators retained. |
| Original-environment comparison | AI; Python 3.12.14/PyArrow 26.0.1: 317 passed in 81.34s. Not revised-environment proof. Original running 8518 is deliberately not modified. |
| Local quality/security | Ruff/format/Bandit/pip check PASS. Strict runtime/development pip-audit covers all 34/71 locked packages, no known vulnerabilities/skips/omissions at execution. Platform extras are outside this audit. |
| Coverage | 99% booking diagnostic; 200 statements/one missing, 70 branches/one partial. Existing demo-fixture guard remains unexecuted. No grade/completeness claim. |
| Private independent boundary matrix | 16 passing literal decisions: active Create/Book/Cancel x C-1/C/C+1/S plus separately owned-CANCELLED repeats at four instants. Check exact State/history/counters/input, active refusals and no-op identity. Separate from pytest count. |
| Current source CI | PASS: source candidate cb9b1f6bc9883c3e3162a98209b4b0de6b4193df, [run 44252306874](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44252306874), job 134625664411, Python 3.12.16, 317 passed in 89.16s, no failures/errors/skips; one job/all 18 steps successful. Runtime-only hash install/imports and all 34 runtime versions match the revised lock (PyArrow 24.0.0/Streamlit 1.67.0/Pandas 3.1.1). Ruff/format/pip check/Bandit and strict 34/71-package dependency audits PASS, no known vulnerabilities/skips/omissions. Artifact 14403844500 was downloaded and verified for SHA256 d49f47bd29b05c251da58495051b8e1a6172bd630f03c0bc0719f3a23de600ca, CRC, tested SHA/JUnit317 and report contents; expires 2 December 2026. A later records-only HEAD still requires its own current-head check. |
| Revised hosted browser | PASS for the currently served, source-unattested instance, executed by AI using connected CUA Chrome (1707x876); separate public/no-owner IAB (912x871) renders meaningful 4-workshop/3-confirmation data. Fresh Chrome Sam cancels registration-2 (confirmations 3->2), then rebooks Photography as registration-5 (2->3); History keeps cancelled 2/4. Rui's missing-meeting-point submission keeps title/capacity/notes/dates/times and consumes no workshop ID; Alex has blank title/no Rui error, and Rui's own failure restores. Correction creates only workshop-5 and resets his fields (title empty/capacity 10). Xingjian books it as registration-6; the freshly painted Rui roster shows registration-6/participant-1/Xingjian/CONFIRMED with totals 5/4. Refresh view retains 5/4; a separate unchanged Chrome session stays 4/3. Console error/warning collection is empty. These are technical observations, not current-source deployment proof, human validation or mobile-specific testing. |
| Actual isolated restart | Verified target PID/path/start-time and unhealthy -> healthy transition for 8520 only. Native cancellation before restart is lost after reconnect/rerun; factory 4 workshops/3 confirmations and registration-2 CONFIRMED return. Sam selection can survive; main view/data reset. Existing 8518 stays healthy, cloud not stopped. |
| Protection/delivery | Compare all 23 local/source-tree/archive raw bytes and CRC; preserve 139 earlier files/archives, six historical reviews and 39/51 canonical rows. Source ZIP remains local, private tools/evidence outside repository. Final head Actions and parity are checked after records update. |

Historical intake evidence, not this patch's result: run 44244879029/job 134601303777 at fc964bb, Python 3.12.16, 308 passed in 71.14s/all 18 steps. Artifact 14400843523 was independently downloaded, CRC/digest/tested SHA/JUnit308 checked; digest cff4bc890a66defa31d6778359bf1dc0653a0886c7d008d0a8ac8049f83b6603. Earlier aligned source 1c952ee and run 44244177092 also belong to initial L6. An empty legacy commit-status collection is not a failed Actions run; actual jobs/artifacts are authoritative here.

## Dependency revision record

| Item | Actual evidence |
|---|---|
| Original input | Runtime and development locks pin PyArrow 26.0.1. Cloud Python 3.12.16/Streamlit 1.67.0 log installs it, then reports replacement with pyarrow<25 and installs 24.0.0. |
| Reason/constraint | Align this provider's observed functioning version and test a reproducible project environment. Installed Streamlit requires pyarrow!=25.0.0,<27,>=12.0.0; 24.0.0 satisfies it. No 26.0.1 application crash was reproduced. |
| Upstream interpretation | [Arrow issue 50471](https://github.com/apache/arrow/issues/50471) concerns 25.0.0/mimalloc and is closed; it reports 24 as a workaround. Do not generalise that issue into proof that 26.0.1 is broken or 24 is the only compatible version. |
| Authority | Author's explicit targeted pin/hash permission. It is not permission for unrelated upgrades or release. |
| Tool/method | Existing pip-tools 7.7.0, official PyPI, existing inputs/locks, --generate-hashes --reuse-hashes --allow-unsafe --resolver=backtracking --upgrade-package=pyarrow. Add direct pyarrow==24.0.0 constraint to requirements.in, compile requirements.txt then development lock constrained by runtime. No handwritten hashes. |
| Actual difference | Only version 26.0.1 -> 24.0.0; 50 tool-generated Arrow hashes in each lock, related via/input explanation. Runtime 34/development 71 package sets unchanged; all other 33/70 pin/hash blocks identical. requirements-dev.in unchanged. |
| Rejected private draft | Initial private compile omitted --allow-unsafe and failed retained-pin checking. Corrected before application/publication. The extras-aware audit parser matches the unchanged workflow; pip/setuptools and every other pin remain included. |
| Verification | Fresh isolated install --require-hashes from revised development lock, 317 full tests/static checks and complete strict audits. CI/runtime-only install and real cloud evidence must independently agree. |

## Deployment record

| Field | Observed value/status |
|---|---|
| Hosted candidate | [https://cp5401-outdoor-workshops-v1.streamlit.app/](https://cp5401-outdoor-workshops-v1.streamlit.app/), branch codex/l6-v1-integration, root app.py/requirements.txt. |
| Managed Python | 3.12.16 observed in actual build logs. Workflow remains pinned to 3.12.16; local compatibility environment is 3.12.14. |
| Revised local human preview | http://127.0.0.1:8520, isolated hash-installed Arrow 24.0.0. Kept running. |
| Original preview | http://127.0.0.1:8518 kept running with earlier Arrow 26.0.1; explicitly not current-lock environment proof. |
| Source/runtime proof | OPEN - L6-F10/L6-F11. Real manager logs confirm configured codex/l6-v1-integration/root app.py, Python 3.12.16/Streamlit 1.67.0 and the original installation's PyArrow 26.0.1 -> 24.0.0 replacement. After publication, fresh page/session checks still expose only that initial 05:09 UTC build log and no L6_RUNTIME_IDENTITY record. Therefore the exact current deployed SHA, three revised source digests and all 34 installed runtime pins have NOT been independently established. Hosted native workflows work, but they are not proof that cb9b1f6 or the revised requirements are deployed. Keep the existing service available; do not reboot/delete/recreate it or expand GitHub access as part of this preserved-service check. DEPLOYMENT_CONDITION_NOT_MET until an actual revised deployment and source/package match are observed. |
| Log scope | Once per Streamlit session: root Git SHA or explicit None, SHA256 of app.py/booking.py/requirements.txt, Python and installed runtime pin versions. Read-only; no user/session business data, arbitrary environment values or secrets. New/fresh session is required after a source update. |
| Platform boundary | Provider installs logging/installer extras beyond project lock. Project pin parity is not a claim of bit-identical OS/Python patch across local/cloud or full platform vulnerability certification. |
| Release state | LOCAL_AND_CI_VERIFIED_FOR_TESTED_SCOPE; CLOUD_SOURCE_AND_ENVIRONMENT_PROOF_UNRESOLVED; DEPLOYMENT_CONDITION_NOT_MET. L6-F10/F11 remain OPEN. V1.0 is not release-ready or approved; human validation/acceptance and release decisions remain PENDING. Human acceptance/validation and release remain separate. |

Community Cloud follows the review branch; verify a fresh runtime identity after each candidate/update. If the exact source, revised pins or real controls cannot be established, leave F10/F11 OPEN and deployment condition NOT_MET. Do not silently substitute historical CI/local smoke or claim source proof from a branch label alone. Code/config rollback requires a reviewed source revision and new CI/smoke; it does not recover temporary bookings. The actual isolated restart demonstrates reinitialisation only.

## Integration, architecture and review depth

FR-01 identity/menu reset; FR-02 complete information/time/counts; FR-03 Book; FR-04 own Cancel; FR-05 own current/history; FR-06 valid Create; FR-07 actual-owner roster are integrated. The two serial journeys use an empty valid State and literal expected IDs/counters/records across the real UI controls. Retained multi-attendee tests check that only the target row changes; distinct active deadline/no-op fixtures prevent false deadline evidence. Capacity/full/duplicate/role/owner/unknown target checks keep valid isolated preconditions.

The UI takes fresh trusted time at actual submission; hidden/disabled controls are additional usability checks, not sole authority. Domain permission uses canonical actor and actual looked-up ownership. Original input is never modified by genuine success/refusal/no-op/failure, and UI adopts only explicit OK. There is no database transaction or shared-user race guarantee. All relevant F05/F08 regressions remain unchanged; L3 HF-02 is historical, not a current shared-draft contract.

No extra application layer, generic recovery abstraction, speculative persistence or duplicated rule validation is added. Only deployment provenance has a bounded metadata helper; missing metadata becomes unknown rather than inventing a SHA or mutating state. Existing unknown-target/invalid-clock/explicit-OK checks defend actual interfaces and rejected-candidate tests, not arbitrary state repair. Actual observed risk motivates the dependency fix. Review depth is AI-proposed Medium for this bounded environment/evidence patch; student judgement and allocation/permission scrutiny remain required.

## Risk/control and test mapping

| Risk | Implemented/executed control | Remaining acceptance/limit |
|---|---|---|
| R-01 | Capacity 1-30, CONFIRMED counts, duplicates, latest-state serial allocation and one-place cancellation/rebooking; retained B04/B07-B09/I01-I02. | No shared concurrency claim; human checks actual UI/results. |
| R-02 | V1.0 no waitlist/FIFO implementation. Full Book remains FULL. | W/I03/I04/I07 and CR-01 stay future. |
| R-03 | Role menus plus business canonical-actor/actual owner; B01/B02/B10/B12-B14/I08. F08 isolates accidental draft mixing. | Freely selectable fictional identities are not authentication; personal H05/H07 PENDING. |
| R-04 | Pure complete-State adoption/full input/counter snapshots; new Create/Book late-failure checks plus retained cancellation I05; independent initialisation and actual reset evidence I09. | No durable recovery; old preview environment differs; lifecycle acceptance PENDING. |
| R-05 | Aware instants, trusted fresh clock, strict C/S and separate active/no-op fixtures, stale-submit I10; independent 16-decision audit. | Human policy suitability remains unconfirmed; no emergency override. |
| R-06 | Bounded author scope, actual code/dependency differences, generated-hash provenance, rejected-tool assumptions and AI ledger. | Author must understand/review and choose ACCEPT_LOOP; AI cannot approve. |
| R-07 | All 308 old cases retained, nine independent review cases, private faults and current-SHA CI/artifacts/audits; no reduced assertions. | 99% coverage/317 cases do not prove completeness; full platform extras are outside audit. |
| R-08 | Information, status/deadline/preparation disclosures and concrete VAL-01/VAL-02 tasks. | Actual human observations/rationale PENDING; V1.1 near-C awareness/feasibility VAL-03A-03E not closed. |

I05 now tests late construction for all V1.0 mutations, not future promotion rollback. I06 combines automated preservation with AI browser observations; human lifecycle checks stay PENDING. I08 separates role/owner/adoption correctness from genuine human comprehension. I09 tests independent factory/session State and actual reset, not storage restoration. I10 has actual stale Create/Book/confirmed Cancel clock seams; waiting/promotion/withdrawal variants remain V1.1.

## Course and HD alignment

Original Assessment 3, three transcript PDFs and Week3-9 archive were re-extracted; source hashes match and 22 teaching decks were inspected as relevant. The rubric weights requirements/planning 15%, functioning app/deployment 15%, V&V/testing 20%, change/regression/release 20%, GitHub CI 15% and presentation/defence 15%. This technical review supports scoped/testable/traceable requirements, a genuine browser candidate, independent tests and documented human control; it cannot confer a grade.

The lecture permits explained adaptation of the three Demo core files and requires student understanding/ownership of AI/code/tests/acceptance. Verification versus actual user validation, risk-based tool findings, independent oracles, regression and justified human decisions are kept distinct. The assessed later CR-01 issue/impact/branch/PR/review/merge/V1.1 release, final document/PPTX/URLs and defence remain incomplete future work. A dependency alignment fix is not substituted for the assessed waitlist change. Earlier accepted reviews remain byte-identical. No rigid file count, test count or coverage percentage is represented as an HD requirement.

## Validation record

Verification asks whether specified behaviour works; validation asks whether the intended user task/policy is useful. Record actual author role-play honestly or identify real external testers; never invent either.

| Task | Personal task/acceptance question | Actual human evidence/decision |
|---|---|---|
| VAL-01 / participant | In a fresh session find suitable workshop; explain S/C/location/preparation/full versus locked; cancel Sam's Photography registration-2 before C, retain history; book as Xingjian (registration-5), inspect own records and next action. Explain post-C restriction and temporary/selectable identity limits. Is this coherent/useful for the declared task? | PENDING: tester/role, target/SHA/date, actual actions/observations, comprehension or concern, rationale and ACCEPTABLE_WITHIN_SCOPE/CHANGES_REQUIRED/UNRESOLVED. |
| VAL-02 / organiser | Create capacity-1 workshop >24h away, intentionally omit meeting point, inspect all eight retained values/errors/no consumed ID, correct/reset, book as participant and inspect creating/other organiser rosters. Does the 24h freeze support preparation; is closed confirmed cancellation acceptable? | PENDING actual observations/policy judgement, not merely automated lock verification. |
| Manual I06/I08/I09 | Exercise identity/menu reset, owner/private lists, Refresh view/ordinary rerun, independent session and actual reload/new-session semantics. Explain possible factory reset and lack of secure login/sharing/recovery. | PENDING personal execution and explicit limit/risk judgement. No need to stop the preserved service to repeat AI's isolated restart. |
| R-08 / later waiting | VAL-03A-E: unconfirmed waiting/no notification, latest useful discovery, promotion just before C discovered after C, preparation/arrival and post-C waiting withdrawal. No promotion at/after C under accepted policy. | VALIDATION_PENDING / DEFERRED_TO_V1.1. Neither 24h rule nor AI browser success closes feasibility/awareness concerns. |

## Human acceptance checklist

All seven items remain unchecked until supplied by the author. Use fresh sessions when fixture IDs are required; preserve a session within each journey.

- [ ] **H01 - Candidate/evidence.** Verify current L6 GitHub HEAD, its actual Actions/job/artifact, source candidate SHA, deployed identity/version comparison and 23-file local ZIP parity. Explain preserved booking.py/308 old cases/single job, nine new cases and only the authorised Arrow pin/hash correction. Review F01-F12 and AI contribution.
- [ ] **H02 - VAL-01 participant.** Perform the participant task above, check exact cancellation/history/replacement IDs/counts and explain full versus deadline closure. Record actual comprehension, next action and cancellation-policy judgement.
- [ ] **H03 - VAL-02 organiser.** Perform invalid -> corrected creation/reset and participant booking/owned-roster task. Check >24h/capacity 1-30, eight failed fields, no invalid ID advance, current identity ownership and other organiser isolation; record preparation-policy feedback.
- [ ] **H04 - Independent oracle review.** Inspect active C-1/C/C+1/S versus separate owned-CANCELLED repeats; spare-capacity duplicate versus eligible FULL; multiple-attendee/clicked-target cancellation; old-input/counters/history and late Create/Book/Cancel failure tests; F05/F08 regressions. Explain why high coverage or capacity-1 journeys could miss the private faults.
- [ ] **H05 - Identity/session lifecycle.** Personally check role-specific menus plus business permission evidence, same-organiser failure restore/other-organiser isolation, Refresh/rerun, another session and reload. Explain no secure authentication/shared allocation/durable recovery; use fictional data only. Prefer aligned 8520 for revised local checks; 8518 is preserved with older Arrow.
- [ ] **H06 - Actual deployment/validation.** Open the hosted candidate and inspect Participant/Organiser native workflows; compare observed SHA/source/package evidence and declared Python patches. Record genuine VAL-01/02 observations/rationale and any unresolved environment or suitability issue; preserve R-08/V1.1 questions. AI screenshots are not personal execution.
- [ ] **H07 - Human decision/release boundary.** Explain AI/Demo contributions and test expectations; record actual findings/edits/rejected suggestions, residual-risk reasoning, reviewer/date/candidate and ACCEPT_LOOP or CHANGES_REQUIRED. ACCEPT_LOOP does not imply READY_TO_MERGE or ACCEPT_RELEASE. Do not start L7/CR-01 automatically.

| Human record | Current value |
|---|---|
| Reviewer/date/candidate | PENDING. |
| Personal UI/commands/observations | PENDING; AI/Actions evidence is not personal execution. |
| VAL-01/VAL-02 decision/rationale | PENDING. |
| Actual feedback/edits/rejected suggestions/risk judgement | PENDING; scope permission is recorded separately. |
| L6 loop decision | PENDING; wait for actual ACCEPT_LOOP. |
| Main merge | NOT_AUTHORISED/PENDING; separate reviewed-main evidence and decision. |
| Formal v1.0 tag/GitHub Release | NOT_AUTHORISED/PENDING; separate ACCEPT_RELEASE required. |
| L7 | NOT_STARTED. |

## Current technical candidate and gate

LOCAL_AND_CI_VERIFIED_FOR_TESTED_SCOPE; CLOUD_SOURCE_AND_ENVIRONMENT_PROOF_UNRESOLVED; DEPLOYMENT_CONDITION_NOT_MET. L6-F10/F11 remain OPEN. V1.0 is not release-ready or approved; human validation/acceptance and release decisions remain PENDING.

PASS: source candidate cb9b1f6bc9883c3e3162a98209b4b0de6b4193df, [run 44252306874](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44252306874), job 134625664411, Python 3.12.16, 317 passed in 89.16s, no failures/errors/skips; one job/all 18 steps successful. Runtime-only hash install/imports and all 34 runtime versions match the revised lock (PyArrow 24.0.0/Streamlit 1.67.0/Pandas 3.1.1). Ruff/format/pip check/Bandit and strict 34/71-package dependency audits PASS, no known vulnerabilities/skips/omissions. Artifact 14403844500 was downloaded and verified for SHA256 d49f47bd29b05c251da58495051b8e1a6172bd630f03c0bc0719f3a23de600ca, CRC, tested SHA/JUnit317 and report contents; expires 2 December 2026. A later records-only HEAD still requires its own current-head check.

OPEN - L6-F10/L6-F11. Real manager logs confirm configured codex/l6-v1-integration/root app.py, Python 3.12.16/Streamlit 1.67.0 and the original installation's PyArrow 26.0.1 -> 24.0.0 replacement. After publication, fresh page/session checks still expose only that initial 05:09 UTC build log and no L6_RUNTIME_IDENTITY record. Therefore the exact current deployed SHA, three revised source digests and all 34 installed runtime pins have NOT been independently established. Hosted native workflows work, but they are not proof that cb9b1f6 or the revised requirements are deployed. Keep the existing service available; do not reboot/delete/recreate it or expand GitHub access as part of this preserved-service check. DEPLOYMENT_CONDITION_NOT_MET until an actual revised deployment and source/package match are observed.

Human H01-H07/VAL-01/VAL-02, residual-risk judgement and ACCEPT_LOOP remain PENDING regardless of technical success. Retain both existing services and the aligned local preview; keep ZIP personal/local. No accepted/tagged V1.0 is asserted. Technical verification, human acceptance, merge approval and release approval are four distinct decisions/evidence boundaries.

## Exit and release preparation

Stop at L6. Do not merge main, create v1.0, publish a Release or enter L7/CR-01. Resolve any material technical finding and genuine validation issue before a later human release decision; verify reviewed-main CI/deployment if explicitly authorised then. Preserve a released V1.0 baseline before the assessed change.

Prepared release scope, not a publication: fixed fictional roles, valid outdoor workshop creation/browsing, serial booking/own cancellation/history/new-ID replacement and owned rosters, strict creation/C policy and capacity 1-30. Disclose temporary unshared state, no authentication/notifications/waitlist and managed environment limits. The author retains the release decision.
