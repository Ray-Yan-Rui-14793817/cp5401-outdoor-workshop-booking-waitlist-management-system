# L1 Work and Human Review

**L1 simplified edition, deep review. Human decision: PENDING. L2: NOT_STARTED.**

## Review intake and scope

Author task: review the simplified L1 against accepted L0 revision 3, Assessment 3/HD criteria, supplied lecture transcripts and slides; check architecture, simplification, tests, Actions, workflow and AI records; fix findings and wait at L1. Executor/review tool: Codex. This record is AI-assisted technical analysis, not the author's personal acceptance.

| Boundary | Treatment |
|---|---|
| Preserved | Accepted FR-01-FR-11, BR-01-BR-16, QR-01-QR-04 and R-01-R-08; all original 40 test cases; app.py/booking.py; four dependency files; original working copy and L0_develop. |
| Current changes | Add two cutoff-boundary parameters in test_booking.py; clarify loop-level partial coverage in README; update this review, AI-use and the test count in Demo reuse. Five existing files change; the package still has 18 files/seven Markdown documents. |
| Earlier simplification | 23 to 18 files, 12 to seven Markdown documents and four CI jobs to one. Rules/risks moved to requirements.md, mappings to test-plan.md, workflow to README and references to demo-reuse.md. Only four optional slots=True settings were removed from the model. |
| Deferred work | Actor operations, creation, booking/cancellation, waitlisting, deployed releases, real-user validation and the assessed CR-01 remain later work. No PR, merge, release or L2 acceptance is recorded. |

## Assumptions and risk triage

| Assumption / ownership | Assessment |
|---|---|
| User-selected session architecture | One browser session, serial state and fictional identities remain the accepted scope. No database, service framework, secure login or shared-concurrency claim is added. |
| Already-declared aware-instant contract | The model accepts aware instants and derives 24 elapsed hours. New York dates challenge that existing contract; they do not add a timezone-selection feature. Display remains Asia/Singapore. |
| Unchanged policy | Creation needs more than 24h; at C close Book/confirmed cancellation/Join/promotion; permit owned waiting withdrawal until S. New tests calculate C only; enforcement remains later work. |
| Reviewer routing | The author owns the current self-review and must explain the code/oracles before a PR. Do not imply independent approval. Escalate unresolved policy or material security/competence questions as appropriate. |

AI proposes MEDIUM review depth: generated test oracles and CI organisation can create false confidence. Validators, actor boundaries and dependency versions are unchanged in this review; authentication/storage/dependency changes would require fresh risk triage. The author must record the actual risk judgement and decision below. R-08 remains VALIDATION_PENDING.

## Findings and dispositions

| ID / significance | Affected work and assessment | Evidence and disposition |
|---|---|---|
| SR-01 / Medium | test_booking.py: Singapore-only cutoff assertions could miss subtraction in local wall time across DST. Existing coverage did not expose this oracle gap. | CORRECTED: preserve the original case and add fall-back/spring-forward cases with fixed expected instants. A private faulty copy passed the old cutoff test but failed both new cases; the real unchanged booking.py passes all 42. This is a test weakness, not a newly discovered production defect. |
| SR-02 / Medium | quality-checks.yml and prior review: the consolidated job had only local syntax/control checks; historical four-job success was insufficient evidence for the new configuration. | HOSTED_PENDING: run the actual single-job workflow on codex/l1-simplified-review and inspect its steps/logs/artifacts before closing this finding. No CI code change is justified by inspection alone. |
| SR-03 / Low | README L2 exit referenced B10/B12/B13 although actual read/create/cancel operations arrive in L3-L5. This could encourage overstating permission-helper coverage. | CORRECTED: L2 exits on actor resolution and permission-foundation tests. Full B10/B12/B13 remain required through real operations before V1.0. No scenario definition, release target or L0 file changes. |
| SR-04 / Low | Current evidence needed an explicit course comparison and separation of AI technical verification from the author's review. | CORRECTED IN DOCUMENTATION: this record links scope, assumptions, oracles, findings and course expectations. Actual human observations/decision remain PENDING, so governance is not claimed complete. |

Earlier corrected L1 findings remain safeguards: UTC instant ordering, complete lock-audit reconciliation, explicit Bash/pipefail and full-state/mixed-status assertions. Historical detail: [prior L1 review](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/blob/8ab483885f92a4861042486e40d152b63f4fa115/docs/reviews/L1-human-review.md). Earlier four-job runs do not identify this reviewed export.

## Independent test review

| Input / independent oracle | What the test establishes and its limit |
|---|---|
| Capacity 1/30 accepted; 0/-1/31/fraction/bool/string/None rejected | Structural model constraints from BR-02; not last-seat booking correctness. |
| S = 10 Dec 2026 09:00 Singapore | C = 9 Dec 09:00 Singapore. The original case remains. |
| S = 1 Nov 2026 09:00 New York = 14:00 UTC | C = 31 Oct 14:00 UTC = 22:00 Singapore. A local-calendar subtraction gives 25 elapsed hours and must fail. |
| S = 8 Mar 2026 09:00 New York = 13:00 UTC | C = 7 Mar 13:00 UTC = 21:00 Singapore. A local-calendar subtraction gives 23 elapsed hours and must fail. |
| Repeated local clock values | UTC instants determine valid workshop/update order. These existing regressions retain the earlier actual correction. |
| One CONFIRMED and one CANCELLED row plus non-default counters | Refresh/navigation preserve the complete state; confirmed count is one. AppTest does not establish secure ownership, business actions, a real browser lifecycle or intended-user suitability. |

The DST oracle was derived from fixed UTC offsets on the stated dates, before evaluating the implementation. Its private challenge changes only a copied booking.py: subtract in local time instead of UTC. Original cutoff subset: 1 passed. Strengthened subset on the same fault: 2 failed, 1 passed. Faulty copies and helper scripts are outside the delivery package; the application was not replaced by a fault.

## Foundation test mapping

| Group | Cases | Supporting property |
|---|---|---|
| FND-01 | 2 | Independent collections/counters and stable fictional IDs/roles; QR-04/I09 foundation. |
| FND-02 | 10 | Structural capacity; partial BR-02/B04 support. |
| FND-03 | 8 | Required structural text; partial B05 support. |
| FND-04 | 9 | Aware dates, positive duration, history and UTC instant ordering; partial BR-03 support. |
| FND-05 | 3 | 24-elapsed-hour cutoff including both DST directions; not action-time enforcement. |
| FND-06 | 5 | Registration timestamp structure and UTC ordering. |
| FND-07 | 5 | AppTest views, state/counter preservation, confirmed counts and separate sessions; partial I06/I08/I09 and BR-04 support. |

Total: 42 parameter cases in the same 16 test functions. Full B/W/I scenarios and VAL-01/02/03 remain planned in the [test plan](../test-plan.md). No baseline booking, role enforcement, real user validation or R-08 closure is claimed by these counts.

## Course and HD alignment

References S01-S17 are retained in [Demo reuse](../demo-reuse.md#references). The original PDFs and Week1-9 archive were re-read; cached extracts match the supplied originals. The 09:40 and 10:45 transcripts are duplicate accounts, not independent corroboration. No original audio file was supplied; automatic transcript wording remains transcription evidence.

| Assessment / classroom expectation | Current L1 position and remaining evidence |
|---|---|
| Requirements/quality planning, 15%; S01 pp.3/10 | Accepted testable FR/BR/QR, risks and complete mappings remain intact. Simplification changes their locations, not their meaning. |
| Functioning application/deployment, 15%; S01 pp.3/10 | L1 supplies an honest preview and foundation. The required working features, two meaningful operational roles and deployed application remain L2-L6 work. L1 is not V1.0. |
| V&V/testing, 20%; S01 pp.3/10-11; S13/S14/S06 | This document/code review and 42 automated cases are verification. Strengthened oracles detect a concrete fault. User validation, core-business failure cases and selected security boundaries remain later activities. |
| Controlled change/releases, 20%; S01 pp.4/12 | Retain working V1.0 before CR-01, impact analysis, changed tests plus regression, PR/findings/human merge decision and V1.1 deployment. This L1 review is not the assessed change. |
| GitHub/CI evidence, 15%; S01 pp.5/12; S07 | One job is sufficient when it actually runs the relevant checks and retains evidence. The hosted commit/run below is required to close SR-02. Preserve progressive history and selected evidence before 14-day artifact expiry. |
| Defence/judgement, 15%; S01 pp.6-8/13; S05/S08 | AI-use records significant tasks and substantial generated work. Author understanding, personal observations, risk judgement and acceptance are still required; green CI or AI review cannot supply them. |
| Lecture use of Demo; S02 p.2; S03 pp.6-7 | Keep app.py -> booking.py with dataclasses/lists and test_booking.py. The extra files are dependency/configuration or primary task/evidence documents. Three core files are a permitted simple pattern, not a ban on required evidence files. |
| Human oversight; S02 pp.8-10; S03 pp.2-4; S05/S08 | Human ownership starts before the PR. Each loop keeps intent, preserved behaviour, assumptions, evidence, findings and the author's reasoned decision. Review routing depends on actual risk; no external approval is invented. |

This supports alignment at the L1 stage. It does not certify a final HD mark or completion of the six assessment criteria.

## Verification results

Executor: AI using local Python 3.12.14 on Windows; recorded 2026-11-16T23:01:24+08:00. The original parent snapshot is 8ab483885f92a4861042486e40d152b63f4fa115, not the identity of the modified files. Hosted identity is recorded separately once executed.

| Check | Observed result |
|---|---|
| Local tests | 42/42 passed; booking.py 66/66 statements and 12/12 branches covered. Coverage describes the model foundation only. |
| Static/security/dependencies | Ruff zero findings; all three files formatted; pip check clean; Bandit zero findings/errors. Hash locks unchanged; hosted audit results pending. |
| Preservation | app.py/booking.py and all four dependency files unchanged from the simplified input. Original 40 scenarios retained with two added parameters. L0, original working copy, accepted rule/risk/scenario bodies and file inventory are checked separately before delivery. |
| Single-job execution | HOSTED_PENDING on codex/l1-simplified-review. Local configuration, explicit Bash/pipefail and continued evidence collection after check failures are retained. |

Local executable identity (SHA-256):

| File | SHA-256 |
|---|---|
| app.py | ee2eaf5172376376d62a8eb7b55f4cf6ee5f30bab6000c165e98838fa6625abc |
| booking.py | 54390b2354627337aea91b8e10dab5ca12a5bbf07bae60a255c98d317615555e |
| test_booking.py | dfaa30b9c9299cd6a6cf03df43e4a762118e9502ebb2c9908b92d7f97d4d1ef8 |
| .github/workflows/quality-checks.yml | 72513f8b1ce3ce00541f86e5ff875e9497dd55eb9fb2f328e0a86a1edd589850 |

Private JUnit/coverage, static-scan reports, source checks and controlled-fault results remain outside L1_develop. No auxiliary checker, new runtime module or source.md is added to the package.


## Human acceptance checklist

All items require actual author observations. Record whether you executed a check or assessed AI/CI evidence. Self-review is not independent external approval.

- [ ] **H01 Setup:** Personally open the L1 preview and record the environment, three views and a refresh observation; optionally rerun pytest and record its actual result.
- [ ] **H02 Code:** Explain the three core files, frozen rows/mutable session lists, independent factories and why model construction does not authorise workshop creation.
- [ ] **H03 Oracles:** Predict capacity and cutoff outcomes before reading results; explain why the two new cases fail the private local-time fault and what they do not test.
- [ ] **H04 Limits:** Check state/counter snapshots and mixed-status counting; explain fictional identity, session/reset, concurrency and pending business-operation limits.
- [ ] **H05 CI:** Inspect the current single quality-checks run/commit, runtime-only install, audits, JUnit/coverage and failure controls. Check any old required-check context before a future merge.
- [ ] **H06 AI and scope:** Compare changes with accepted L0 and this task; confirm retained policies/locks/original tests; record human edits, rejected suggestions and remaining findings.
- [ ] **H07 Decision:** Record reviewer/date/code identity, risk rationale and ACCEPT_LOOP or CHANGES_REQUIRED. Treat R-08 and final assessment/release evidence separately.

| Human record | Actual value |
|---|---|
| Reviewer/date and reviewed code identity | NOT_RECORDED |
| Personally executed checks and observations | NOT_RECORDED |
| Results reviewed rather than executed | NOT_RECORDED |
| Code understanding and independent expected outcomes | NOT_RECORDED |
| Finding dispositions, edits or rejected suggestions | NOT_RECORDED |
| Risk judgement and residual limits | NOT_RECORDED |
| Decision | PENDING |

Actual ACCEPT_LOOP is required before L2. READY_TO_MERGE and ACCEPT_RELEASE remain separate decisions under the [workflow](../../README.md#development-workflow).
