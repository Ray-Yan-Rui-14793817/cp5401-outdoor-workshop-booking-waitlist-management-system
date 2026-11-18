# L6 V1.0 Integration, Deployment and Human Review

**Current: L6 V1.0 candidate, HUMAN_REVIEW_PENDING. Human decision: PENDING. L7: NOT_STARTED.**

## Intake and accepted base

On 18 November 2026 (UTC+08:00), the author explicitly authorises L6 integration, deployment and verification after accepted L5. Preserve app.py -> booking.py -> data structures, one Actions job and every L1-L5 regression; English delivery, local-only ZIP, a retained web preview, actual AI/human records and a stop for ACCEPT_LOOP are required.

Base: [8a5c9723afe6a81bbafc634acc09b65dac436ee4](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/8a5c9723afe6a81bbafc634acc09b65dac436ee4), codex/l5-cancellation. All 22 raw local files match that GitHub tree before copying. Original L5 accepted candidate b597babb, completed H01-H07 and five exact human feedback items remain unchanged in [L5 history](L5-human-review.md#current-human-acceptance); no earlier acceptance/checkmark is transferred to L6. Protect 139 earlier local files/archives, including root tracked files and accepted L0-L5 deliveries.

## Intended and preserved behaviour

Working V1.0 combines FR-01-FR-07. No change to the 39 canonical definition rows, 51 scenario rows, capacity 1-30, strict creation lead, C=S-24h, role/actual-target ownership, one-active-registration rule, cancellation history/new-ID rebooking, owned CANCELLED no-op precedence or complete returned-state integrity. No waiting/promotion, persistence, real authentication, notification, shared-concurrency claim or emergency override is added.

app.py changes only its module description and visible V1.0 candidate caption. booking.py retains accepted L5 bytes. test_booking.py appends one parametrised integration test with two role permutations; all 306 prior case identities/115 test ASTs/decorators and helpers remain unchanged. All dependency/configuration files retain accepted bytes. The single job retains its steps, immutable Action pins, permissions and checks; only its Python patch pin moves from 3.12.14 to the observed cloud 3.12.16 for target-version regression. Changes to five existing English Markdown documents plus this new review explain the candidate/deployment/tests/gates. No private tools/reports/screenshots/course originals or personal source ZIP enter GitHub.

## Independent oracles and technical findings

| ID | Observation, evidence and disposition |
|---|---|
| L6-F01 | The first generated test insertion used an ambiguous repeated context and interrupted a pre-existing function. Two focused cases failed with NameError; Ruff identified leaked names. Restore the entire accepted test source and append the complete new function at file end, then verify all 122 prior helper/test definitions and decorators against L5. Focused 2 passed and full 308 passed. CORRECTED, test placement only; not a genuine business-code defect or a product red/green claim. |
| L6-F02 | V1.0 integration needs actual creation -> allocation -> cancellation -> replacement -> owned roster continuity, rather than only operations over seeded fixtures. Two new real-control journeys establish exact State snapshots, fixed IDs/counters, isolated duplicate versus eligible FULL causes, role reset/ownership and active exact-C control closure. Existing multi-attendee and late-failure oracles remain unchanged. IMPLEMENTED/VERIFIED_LOCALLY. |
| L6-F03 | The deployment form defaulted to 3.14, so Python 3.12 was explicitly selected. Logs show managed Python 3.12.16/Streamlit 1.67.0; initial local/CI used 3.12.14. Align the single-job Python pin to 3.12.16 and require a fresh full run. Actual native hosted controls and a separate no-login IAB session work; source evidence is branch/head-at-launch, not an independently exposed remote Git SHA. DEPLOYED_SMOKE_VERIFIED; TARGET_CI_PENDING. |
| L6-F04 | Passing tests or an AI role-play is verification, not evidence that intended users accept a 24h cancellation freeze or reset/identity limits. VAL-01/VAL-02 require actual author/external-user observations and a reasoned decision; R-08 remains open. HUMAN_VALIDATION_PENDING. |
| L6-F05 | Cloud manager warns that requirements.txt and pyproject.toml are both candidates, then explicitly installs the unchanged requirements.txt with uv; Streamlit 1.67.0 is observed. pyproject.toml contains test/lint/coverage settings, not a competing package lock. Keep required configuration and assess the actual selected file rather than removing it to silence a warning. DISMISSED_WITH_EVIDENCE; no package-input change. |
| L6-F06 | Input-targeted automation did not switch a radio view; visible native/semantic label clicks were used and the resulting view checked before proceeding. Canvas roster accessibility can briefly retain previous cells: a fresh painted snapshot/screenshot confirms workshop-5 with registration-6/Sam. These are browser-check corrections, not fabricated application defects. CORRECTED_VERIFICATION_METHOD. |

The new journey has capacity one to isolate an eligible different participant's FULL request. It cannot alone reveal cancelling every confirmed attendee; the unchanged L5 multi-attendee/order/owner tests establish that property. Active C-1/C/C+1/S fixtures remain separate from owned-CANCELLED no-op repeats. No assertion is weakened to accommodate generated code. The initial source-excerpt print required UTF-8 stdout; that was a private tooling correction with no application change.

## Verification results

| Check | Actual execution and limits |
|---|---|
| Focused new journeys | AI, local Python 3.12.14: 2 passed, 306 deselected, 3.47s. Actual Streamlit AppTest controls, two organiser/participant role permutations. |
| Full retained/new regression | AI, local Python 3.12.14: 308 passed in 66.67s, zero failures/skips. All 306 old JUnit identities and 115 test function ASTs/decorators retained. |
| Static consistency | Ruff, format check, Bandit and pip check PASS; locks unchanged and one-job structure retained. Python patch aligned to cloud 3.12.16; its fresh CI is recorded separately. |
| Coverage | 99% diagnostic: 200 statements, one missing, 70 branches/one partial; only existing demo-fixture guard is unexecuted. Coverage/case count is not a correctness or grade guarantee. |
| Hosted Actions | Initial source [source run 44241849816](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44241849816), job 134591387283, candidate 4ca9631b8833ac0835526bc5ac4afc90b1777a3c: 308 passed in 74.12s on Python 3.12.14; one job/all 18 steps succeed; complete audits of 34 runtime/71 development pins report no known vulnerabilities/omissions. TARGET_CI_PENDING for aligned 3.12.16. |
| Browser identity/render/console | PASS: connected CUA Chrome at 1707x876, plus separate no-login IAB at 912x871. Correct URL/title/nonblank app/no framework overlay; zero relevant browser console errors/warnings. Real hosted cancellation/history, new-ID replacement, per-organiser failed draft isolation, corrected creation/reset and new-workshop booking/owned roster operate. Screenshots inspected; no mobile-specific viewport run is claimed. |
| Integrated native control flow | Cloud Sam cancels registration-2, history keeps 2/4, confirmations 3->2; Xingjian rebooks Photography as registration-5, total 3. Rui fails missing meeting point with retained values; Alex has blank title/no Rui error; Rui draft restores, correction creates workshop-5 and clears only his form. Sam books it as registration-6; a fresh rendered Rui roster shows registration-6/participant-2/Sam/CONFIRMED, totals 5 workshops/4 confirmations. |
| Session lifecycle/reset | Local native cancellation yields 4 workshops/2 confirmations; Refresh view snapshot retains 4/2. Actual browser reload returns no identity and original 4/3. The separate no-login IAB hosted session independently starts 4/3 without the Chrome session's new workshop-5. Actor changes retain the cloud session; no sharing/durability claim. |
| Local/GitHub/archive integrity | Final delivery compares all 23 raw files and local ZIP contents/CRC against the prepared/published GitHub tree, preserving 139 earlier files, six historical reviews, 39 canonical definition rows, 51 scenarios and every prior test AST/decorator. No project ZIP or private tool is uploaded. |

Every execution above belongs to AI tools or Actions as labelled. No personal command execution, user feedback, formal human risk category or L6 ACCEPT_LOOP is supplied by technical success. Full fault-injection evidence remains in unchanged earlier tests/reviews; no new fault is represented as a real production defect.

## Deployment record

| Field | Observed value/status |
|---|---|
| Review branch | codex/l6-v1-integration; root app.py and requirements.txt. |
| Local human preview | http://127.0.0.1:8518; retained for personal checks. |
| Hosted candidate URL | [https://cp5401-outdoor-workshops-v1.streamlit.app/](https://cp5401-outdoor-workshops-v1.streamlit.app/); meaningful app renders without the owner account in separate IAB. |
| Local / CI Python | Local compatibility: 3.12.14. Initial source CI: 3.12.14. Current workflow is aligned to observed cloud 3.12.16; same locks/Streamlit pin/single job. |
| Hosted managed Python | 3.12.16, observed build log; Streamlit 1.67.0, dependencies installed from root requirements.txt with uv. Python 3.12 was explicitly selected in the form. |
| Source/build provenance | Launched from GitHub source candidate 4ca9631b8833ac0835526bc5ac4afc90b1777a3c; manager log confirms repository, codex/l6-v1-integration, root app.py and requirements.txt. The cloud UI/log exposes no independent Git HEAD SHA; record the branch/head-at-launch and observed UI rather than claiming such an attestation. Later records/workflow updates keep app.py/booking.py bytes unchanged. |
| Actual hosted smoke | PASS through real controls in Chrome and public/no-login rendering in IAB; default viewports 1707x876 and 912x871. No viewport override/mobile-specific run, real-user validation or production-security certification is claimed. |
| Acceptance/release | HUMAN_REVIEW_PENDING / RELEASE_PENDING. No main merge, tag or release approval is inferred. |

Community Cloud follows its configured branch. Recheck target and current-head Actions after later commits; record exact exposed source evidence rather than pretending a branch label proves an unexposed remote Git SHA. All application data is temporary and unshared. Deployment/reboot can reset sessions; code rollback does not recover bookings. Restore accepted source/configuration on a reviewed branch to recover code, then rerun CI/deployment smoke. No persistent-data backup/restore is claimed.

## Validation record

Verification asks whether specified behaviour is implemented; validation asks whether the intended task/policy meets user needs. The author's actual role-play can count if identified honestly; do not invent external testers or turn an AI script into human feedback.

| Task | Intended need and concrete check | Technical evidence | Actual human observation/decision |
|---|---|---|---|
| VAL-01 / participant | Find a suitable workshop; identify S/C, meeting point/preparation, available versus full/locked; book, inspect own confirmation, cancel before C, retain history and explain the next action. Explain closed confirmed cancellation at C and freely selectable/temporary unshared sessions. | Retained B/I tests and new L6 serial journey; native browser results recorded separately. | PENDING. Tester/role, candidate/target, actual steps, comprehension, concern, rationale and ACCEPTABLE_WITHIN_SCOPE/CHANGES_REQUIRED/UNRESOLVED must be supplied. |
| VAL-02 / organiser | Create >24h with capacity 1-30; reject missing meeting point without losing draft/ID, correct/reset, inspect own current roster and preparation information. Judge whether the 24h freeze is useful and cancellation restriction acceptable for the classroom task. | Retained creation/owner tests and new real-form integration; native browser results recorded separately. | PENDING. Record actual preparation/policy judgement; merely seeing a lock or passing a test does not establish usefulness. |
| Manual I06/I08/I09 | Rerun/Refresh view and role changes keep session data; menus/owned lists match selected IDs. A separate session is independent; actual browser reload/new session/restart may reset data. | AppTest fixtures and actual native browser observations, labelled by executor. | PENDING. Explain observed lifecycle and accept or challenge it without claiming shared storage/authentication. |
| R-08 / V1.1 carry-forward | Before later release, evaluate VAL-03A-VAL-03E: waiting is unconfirmed, no notification/refresh, promotion just before C may be discovered after C, preparation/arrival feasibility and post-C withdrawal. Same-day pre-S promotion is prohibited by current C policy. | Not implemented in V1.0; no waitlist exists. | VALIDATION_PENDING / DEFERRED_TO_V1.1. Do not close from V1.0 or infer that 24h notice guarantees awareness. |

## Risk/control status and course alignment

| Risk | Implemented evidence/control and remaining decision |
|---|---|
| R-01/R-02 | Capacity/duplicates/one-place serial cancellation/rebooking verified by retained/new tests; no shared concurrency. Waiting/FIFO remains CR-01. |
| R-03 | Hidden menus plus canonical role/actual-target stored-owner checks; fictional-data disclosure. The L5 author accepted the classroom model, not authentication. L6 deployment suitability still needs H05/H07. |
| R-04 | Pure candidate adoption, exact history/IDs/counters, retained failure tests and session independence; no durable recovery. Verify/disclose target reset behaviour, then request actual acceptance. |
| R-05 | Trusted fresh decision clock, strict C/S, independent active/no-op fixtures, unchanged 24h/1-30 rules. Browser controls complement the business check. |
| R-06/R-07 | Bounded patch, preserved 306 tests/ASTs, explicit new oracles, recorded F01 correction, one unchanged job and source/target evidence. Human understanding/risk judgement PENDING. |
| R-08 | Clear information and preparation instructions plus genuine VAL-01/VAL-02 task/policy review. Human suitability remains PENDING; V1.1 awareness feasibility remains separate. |

S01 Assessment 3 pp.3-5/8/10 requires a working browser deployment, testable baseline, correct V&V distinction, automated/regression evidence, traceability and AI disclosure. L6 supplies the technical candidate and evidence; human validation/release and later assessed CR-01 lifecycle remain separate. S02 lecture pp.1-2/8 permits explained adaptation of the three core files and requires student ownership/understanding before accepting changes. Week4/5/7/8/9 teaching guidance supports independent oracles, review dispositions, scope and human decisions. Source hashes were rechecked against the original four PDFs and lecture archive; the ASR transcript wording is interpreted cautiously. No fixed file count/test total/coverage threshold or automatic HD entitlement is attributed to the teaching material.

AI proposes Medium patch review depth for deployment/environment provenance and generated tests; existing allocation/permission contracts retain their established scrutiny. The author must assess the evidence and residual scope. Do not label that AI proposal as a human-approved risk classification.

## Human acceptance checklist

All items start unchecked. Only the author's actual results/decision can complete them. Use a fresh session where the scenario calls for original fixture IDs; keep the same session within a scenario.

- [ ] **H01 - Candidate and evidence.** Verify accepted L5 base, current L6 GitHub head/Actions, actual deployment coordinates and local ZIP parity. Explain the two-line runtime-label change, unchanged booking.py/locks, retained single-job structure and cloud-aligned Python patch and retained 306 cases plus two new journeys. Review F01-F06 and the actual AI contribution.
- [ ] **H02 - VAL-01 participant task.** In a fresh session inspect S/C/location/preparation/counts; as Sam cancel Photography registration-2, retain cancelled history, then as Xingjian book the released place as registration-5 and inspect own records. Explain strict C and the difference between active deadline tests and cancelled repeats. Record actual comprehension/policy observations.
- [ ] **H03 - VAL-02 organiser task.** Create a capacity-1 workshop >24h away, omit meeting point to check all eight failed values/errors/no ID advance, correct it and check one workshop plus success-only reset. Book as a participant, inspect the creating organiser's roster and the other organiser's list. Judge whether the 24h freeze and cancellation restriction support preparation.
- [ ] **H04 - Boundary and oracle review.** Inspect active C-1/C/C+1/S versus separate owned-CANCELLED repeats, eligible FULL versus duplicate fixtures, exact histories/new IDs/counters, multi-attendee cancellation, final construction failure, clicked target, F05 defaults and F08 organiser isolation. Explain why two new capacity-1 journeys do not replace these oracles. No shared-concurrency claim.
- [ ] **H05 - Session/identity checks.** Execute manual I06/I08/I09: identity/menu reset, owned/private lists, rerun/Refresh view, another independent session and actual browser reload/new-session behaviour. Explain fictional-data-only use, no authentication, temporary unshared records and no recovery guarantee. Record actual observed reset behaviour.
- [ ] **H06 - Deployment and validation findings.** Open the actual hosted URL, check meaningful UI and native controls on the tested desktop views; add personal mobile checks where relevant, inspect declared Python/source/environment evidence and compare core flows with localhost. Identify role-play versus external tester, complete VAL-01/VAL-02 observations/decisions and preserve unresolved R-08/V1.1 feasibility questions.
- [ ] **H07 - Human decision and release boundary.** Explain AI tasks, corrections, independent expectations and Demo reuse; record actual findings/edits/rejected suggestions, residual-risk rationale, reviewer/date and candidate-specific ACCEPT_LOOP or CHANGES_REQUIRED. Separately decide READY_TO_MERGE/ACCEPT_RELEASE only when their evidence is ready. Stop at L6; no L7/CR-01 follows automatically.

| Human record | Actual value |
|---|---|
| Reviewer/check date/candidate | PENDING. |
| Personal commands/browser tasks and observations | PENDING; AI/CI results above are not personal execution. |
| VAL-01 / VAL-02 decision and rationale | PENDING. |
| Findings/edits/rejected suggestions and risk judgement | PENDING; no actual student contribution is invented. |
| Current loop decision | PENDING; waiting for author ACCEPT_LOOP. |
| Main merge / v1.0 release | PENDING; distinct human decisions/current-main evidence required. |
| Next loop | L7 NOT_STARTED. |

## Exit and release preparation

The author requested a stop after L6 delivery. Keep the preview available and the personal L6_develop.zip local. No human checklist, READY_TO_MERGE, ACCEPT_RELEASE, v1.0 tag or L7 authorisation is supplied by AI/Actions. Required technical verification/deployment evidence must be complete and material human VAL findings resolved before promoting the working candidate to the baseline release. Preserve V1.0 source/tests/tag before later CR-01.

Prepared release summary: fixed fictional roles; valid outdoor workshop creation/browsing; serial booking, own cancellation/history/new-ID replacement and owned rosters; strict creation/C policies and capacity 1-30; simplified session architecture and quality evidence. Disclose temporary unshared state, selectable identities, no notifications/persistence/waitlist. Publish/tag only after actual human release approval and verified reviewed-main deployment.
