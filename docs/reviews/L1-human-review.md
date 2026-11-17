# L1 Work and Human Review

**L1 simplified edition, deep review. Human decision: ACCEPT_LOOP, 17 November 2026 (Asia/Shanghai). H01-H07: AUTHOR_CONFIRMED_COMPLETE. L2: NOT_STARTED.**

## Review intake and scope

Author task: review the simplified L1 against accepted L0 revision 3, Assessment 3/HD criteria, supplied lecture transcripts and slides; check architecture, simplification, tests, Actions, workflow and AI records; fix findings and wait at L1. Executor/review tool: Codex. Technical analysis below is AI-assisted. The author's subsequent acceptance and completion statement are recorded separately in the human acceptance checklist.

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

AI proposes MEDIUM review depth: generated test oracles and CI organisation can create false confidence. Validators, actor boundaries and dependency versions are unchanged in this review; authentication/storage/dependency changes would require fresh risk triage. The author has declared H07 complete and supplied ACCEPT_LOOP. A separate written risk classification/rationale was not included in that message; the AI recommendation is not relabelled as the author's own reasoning. R-08 remains VALIDATION_PENDING.

## Findings and dispositions

| ID / significance | Affected work and assessment | Evidence and disposition |
|---|---|---|
| SR-01 / Medium | test_booking.py: Singapore-only cutoff assertions could miss subtraction in local wall time across DST. Existing coverage did not expose this oracle gap. | CORRECTED: preserve the original case and add fall-back/spring-forward cases with fixed expected instants. A private faulty copy passed the old cutoff test but failed both new cases; the real unchanged booking.py passes all 42. This is a test weakness, not a newly discovered production defect. |
| SR-02 / Medium | quality-checks.yml and prior review: the consolidated job had only local syntax/control checks; historical four-job success was insufficient evidence for the new configuration. | CORRECTED WITH EVIDENCE: the actual single-job run succeeded on the tested commit below. All relevant steps ran successfully and the combined reports artifact was uploaded. No further CI code change was needed. |
| SR-03 / Low | README L2 exit referenced B10/B12/B13 although actual read/create/cancel operations arrive in L3-L5. This could encourage overstating permission-helper coverage. | CORRECTED: L2 exits on actor resolution and permission-foundation tests. Full B10/B12/B13 remain required through real operations before V1.0. No scenario definition, release target or L0 file changes. |
| SR-04 / Low | Current evidence needed an explicit course comparison and separation of AI technical verification from the author's review. | CORRECTED IN DOCUMENTATION: this record links scope, assumptions, oracles, findings and course expectations. Human acceptance was pending at technical-review time; the author subsequently declared H01-H07 complete and supplied ACCEPT_LOOP on 17 November 2026. Individual personal notes were not supplied with that statement. |

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
| GitHub/CI evidence, 15%; S01 pp.5/12; S07 | One job is sufficient when it actually runs the relevant checks and retains evidence. The hosted commit/run below closes the execution gap in SR-02. Preserve progressive history and selected evidence before 14-day artifact expiry. |
| Defence/judgement, 15%; S01 pp.6-8/13; S05/S08 | AI-use records significant tasks and substantial generated work. The author now declares H01-H07 complete and accepts L1; individual personal notes are not transcribed from AI execution. Final defence still requires the author to explain and defend the submitted work; green CI cannot supply that understanding. |
| Lecture use of Demo; S02 p.2; S03 pp.6-7 | Keep app.py -> booking.py with dataclasses/lists and test_booking.py. The extra files are dependency/configuration or primary task/evidence documents. Three core files are a permitted simple pattern, not a ban on required evidence files. |
| Human oversight; S02 pp.8-10; S03 pp.2-4; S05/S08 | Human ownership starts before the PR. Each loop keeps intent, preserved behaviour, assumptions, evidence, findings and the author's reasoned decision. Review routing depends on actual risk; no external approval is invented. |

This supports alignment at the L1 stage. It does not certify a final HD mark or completion of the six assessment criteria.

## Verification results

Executor: AI using local Python 3.12.14 on Windows; review updated 2026-11-16T23:07:47+08:00. The original parent snapshot is 8ab483885f92a4861042486e40d152b63f4fa115, not the identity of the modified files. Hosted checks also passed on Ubuntu 24.04/Python 3.12.14; exact identity is recorded below.

| Check | Observed result |
|---|---|
| Local tests | 42/42 passed; booking.py 66/66 statements and 12/12 branches covered. Coverage describes the model foundation only. |
| Static/security/dependencies | Ruff zero findings; all three files formatted; pip check clean; Bandit zero findings/errors. Hash locks unchanged. Hosted strict audits found no known vulnerabilities and reconciled every pin: 34 runtime/71 development packages, with no omissions. |
| Preservation | app.py/booking.py and all four dependency files unchanged from the simplified input. Original 40 scenarios retained with two added parameters. All 13 L0 files and 23 original working-copy files remain byte-identical to their pre-change snapshots. Accepted rule/risk/scenario bodies, all 17 references, the 18-file inventory, English-only documents and local links/anchors passed preservation checks. |
| Single-job execution | PASSED: one quality-checks job, with successful runtime-only installation/imports, development installation, Ruff/format, pip check, Bandit, both complete audits, all 42 tests and report upload. All relevant steps succeeded; none was skipped. Explicit Bash/pipefail and continued evidence collection after check failures remain in the workflow. A local failing tee pipeline returned nonzero; that probe is not represented as a deliberately failed hosted run. |

Hosted executable snapshot: [0a440c531d0996a2fdf3149b3d09626143f8584c](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/0a440c531d0996a2fdf3149b3d09626143f8584c), [run 43892256417](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/43892256417), job 133386317315, branch codex/l1-simplified-review. The logs show all 42 tests passed with zero skips. Artifact quality-checks-43892256417-1 contains the combined reports and expires 30 November 2026; retain selected evidence before expiry. The documentation-only follow-up preserves the four executable hashes below; check the latest branch run when accepting. Main remains the accepted L0 commit 822710b238bb14b8eba17cf2ab9a76ab2753bdb2. No PR was opened by this task.

Local executable identity (SHA-256):

| File | SHA-256 |
|---|---|
| app.py | ee2eaf5172376376d62a8eb7b55f4cf6ee5f30bab6000c165e98838fa6625abc |
| booking.py | 54390b2354627337aea91b8e10dab5ca12a5bbf07bae60a255c98d317615555e |
| test_booking.py | dfaa30b9c9299cd6a6cf03df43e4a762118e9502ebb2c9908b92d7f97d4d1ef8 |
| .github/workflows/quality-checks.yml | 72513f8b1ce3ce00541f86e5ff875e9497dd55eb9fb2f328e0a86a1edd589850 |

Private JUnit/coverage, static-scan reports, source checks and controlled-fault results remain outside L1_develop. No auxiliary checker, new runtime module or source.md is added to the package.


## Human acceptance checklist

On 17 November 2026 (Asia/Shanghai), the project author explicitly supplied ACCEPT_LOOP and stated that H01-H07 had been completed. The checked items below record that author declaration, not an AI inference or independent external approval. The date is the confirmation/acceptance date; individual execution dates were not supplied.

English translation of the author's confirmation: "ACCEPT_LOOP. I have completed the H01-H07 human acceptance checks. Update my L1." This is a translation, not a verbatim English statement. The accepted candidate is the simplified L1 delivered in the preceding conversation: commit cb1f4a261e31e5486b4982b72317f4c39445eecf on codex/l1-foundation. Its [run 43901733050](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/43901733050) passed the single job and all 42 tests. AI previously verified that CI result; it is not represented as a fresh personal test execution by the author.

- [x] **H01 Setup:** Personally open the L1 preview and record the environment, three views and a refresh observation; optionally rerun pytest and record its actual result.
- [x] **H02 Code:** Explain the three core files, frozen rows/mutable session lists, independent factories and why model construction does not authorise workshop creation.
- [x] **H03 Oracles:** Predict capacity and cutoff outcomes before reading results; explain why the two new cases fail the private local-time fault and what they do not test.
- [x] **H04 Limits:** Check state/counter snapshots and mixed-status counting; explain fictional identity, session/reset, concurrency and pending business-operation limits.
- [x] **H05 CI:** Inspect the current single quality-checks run/commit, runtime-only install, audits, JUnit/coverage and failure controls. Check any old required-check context before a future merge.
- [x] **H06 AI and scope:** Compare changes with accepted L0 and this task; confirm retained policies/locks/original tests; record human edits, rejected suggestions and remaining findings.
- [x] **H07 Decision:** Record reviewer/date/code identity, risk rationale and ACCEPT_LOOP or CHANGES_REQUIRED. Treat R-08 and final assessment/release evidence separately.

| Human record | Actual value |
|---|---|
| Reviewer/date and reviewed code identity | Project author, identified by the user role in the project conversation. Confirmation date: 17 November 2026, Asia/Shanghai. Accepted candidate: cb1f4a261e31e5486b4982b72317f4c39445eecf, the simplified L1 most recently delivered. |
| Personally executed checks and observations | H01-H07 completion explicitly declared. Individual commands, environment details and step-by-step observations were not included in the acceptance message. |
| Results reviewed rather than executed | H05 completion declared. Run 43901733050 is linked as existing CI evidence; no separate personal execution log was supplied. |
| Code understanding and independent expected outcomes | H02-H04 completion declared. Individual explanations were not transcribed in this message. |
| Finding dispositions, edits or rejected suggestions | H06 completion declared; technical dispositions remain above. No additional human edits or rejected suggestions were reported in this message. |
| Risk judgement and residual limits | H07 completion and ACCEPT_LOOP explicitly declared. A separate written risk classification/rationale was not included. AI MEDIUM triage remains AI analysis; R-08 and later release validation remain open. |
| Decision | ACCEPT_LOOP, supplied by the author and transcribed by AI. |

The L1 human gate is SATISFIED by the explicit ACCEPT_LOOP. This record-only update changes no code, tests, workflow, dependency locks or business rules. L2 is eligible but NOT_STARTED, awaiting the author's next instruction. READY_TO_MERGE and ACCEPT_RELEASE remain separate decisions under the [workflow](../../README.md#development-workflow).
