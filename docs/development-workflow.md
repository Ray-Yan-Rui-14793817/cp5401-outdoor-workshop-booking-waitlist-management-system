# Development Workflow

Accepted design: L0 revision 3. **Current loop: L1 foundation. Human decision: PENDING. L2 NOT_STARTED.**

The L0 design gate is satisfied. The author has requested L1 implementation under the accepted plan. See the preserved [L0 acceptance](reviews/L0-human-acceptance.md), current [L1 work/review record](reviews/L1-human-review.md) and [baseline document index](../README.md#design-baseline-documents). L1 automation does not provide human acceptance.

Keep the app.py / booking.py / test_booking.py structure while retaining a controlled engineering process. Use the compact record below when each development increment actually occurs. No separate L0 checking tool is part of the baseline.

## Human oversight

| Stage | AI contribution | Required personal contribution |
|---|---|---|
| Before implementation | Draft options, assumptions, test ideas and a bounded plan | Own the intent, expected examples, preserved behaviour, files and justified risk |
| During implementation | Generate changes, run checks and repair within scope | Resolve policy questions and reject unapproved scope or changed expectations |
| Before PR | Summarise the diff and evidence | Understand material lines, inspect independent oracles, remove unrelated work and personally verify selected scenarios |
| After CI/review | Summarise findings and potential fixes | Assess findings against code/specification, confirm current evidence and record the merge decision |
| Release | Prepare deployment notes and evidence | Decide release, inspect deployed behaviour and explain residual limits |

The author owns the decisions even when AI generates most text or code. Evidence must show what the author actually understood, checked, changed or rejected. AI execution, CI execution, human execution and human review of results are distinct.

If intent, authority or policy is unresolved, stop the dependent work and escalate to the human owner. Do not invent a policy to satisfy a test. Use permitted tools and fictional/sanitised data, excluding real credentials/private records.

## Decision scopes

| Decision | Meaning |
|---|---|
| ACCEPT_LOOP | Accept this loop and permit the next bounded loop; no automatic merge/release |
| READY_TO_MERGE | Complete PR, current CI and findings checked; no blocking issue |
| ACCEPT_RELEASE | Deployment, smoke checks and required validation complete |
| CHANGES_REQUIRED | Rework, more evidence or revised requirements |
| SPECIALIST_ADVICE_REQUIRED | Further advice is needed on a material unresolved issue |

Individual self-review must be labelled honestly. The assessment permits the author's justified decision unless teaching staff require external review. Do not invent a second reviewer. Seek suitable advice when the author cannot explain or resolve a material risk.

Record final pre-merge decisions against current head/base and tested SHA, preferably in a PR comment after the last code change. New relevant changes invalidate the previous decision until rechecked.

## Record for each loop

Create a short record such as docs/reviews/L1-human-review.md during the actual loop. The format below is a recording guide, not completed evidence. Scale detail to the change, and link existing test/PR evidence rather than duplicating it.

| Record | Content to supply from actual work |
|---|---|
| Identity | Loop, intended release, date, author/reviewer role and Issue/CR/PR when one exists. |
| Intent and scope | FR/BR/QR/risk IDs, requested behaviour, examples chosen by the author, behaviour to preserve, allowed files and exclusions. |
| AI task | Actual tool/model if known, significant prompt summary, constraints, affected functions/tests and assumptions requiring human confirmation. |
| AI output | What was generated or changed and checks actually executed by AI, with evidence. |
| Human contribution | Policy decisions, personally reviewed code, human edits, rejected/deferred suggestions and reasons. Do not relabel AI work as personal execution. |
| Automated checks | Command/environment, collected/passed/failed/skipped counts, executor, observed result, run URL and tested SHA. |
| Personal acceptance checks | Scenario ID, valid preconditions, expected outcome from the specification, actual observation, personal executor/date and evidence. Distinguish running a scenario from reviewing somebody else's result. |
| Findings | Source, affected file/line, claim, human assessment, evidence and disposition: corrected, dismissed with justification or unresolved. |
| Residual risk | Remaining limitation, owner, mitigation and any justified exception/expiry. Unresolved blockers stop progression. |
| Decision | Actual human decision, scope, date, rationale and evidence/code identity. Use ACCEPT_LOOP, READY_TO_MERGE, ACCEPT_RELEASE, CHANGES_REQUIRED or SPECIALIST_ADVICE_REQUIRED. |

For C/S checks, use a fresh active fixture for each boundary; record no-op repeats separately. Permission checks need a valid selected actor, target and unrelated timing conditions. The author should explain why the chosen examples would detect the relevant failure.

Entry to the next loop requires the current loop's scoped outputs, relevant passing checks, assessed findings and a genuine human ACCEPT_LOOP. AI must stop at the gate until that decision is supplied. Relevant changes after a decision require renewed review. L0 already has its actual ACCEPT_LOOP; the current request authorises L1 only.

## Loop plan

### L0 Design review

- AI: consolidate requirements/rules/risks/reuse/tests, perform source-based design review and prepare English documents.
- Human: reviewed the design scope, requirements, business rules, risks, test mapping and prototype limitations. Seven L0 self-review checks and a written ACCEPT_LOOP rationale are recorded in the human acceptance file. These records do not represent application execution or independent external review.
- Outputs: accepted requirements, rules, risks, Demo reuse, test mappings, this workflow, AI-use/review findings, source references and the actual human acceptance record.
- Exit: genuine ACCEPT_LOOP with no material implementation ambiguity. R-08 validation remains planned; release is not pre-approved.

Historical outcome: the author accepted L0 revision 3 on 16 November 2026, later adding seven self-review confirmations and a written rationale in GitHub. The new bounded request started L1; it did not change the accepted rules.

### L1 Simple skeleton and CI

- AI: create the core files, dataclass/list state factory, applicable rules, meaningful pytest checks, dependency locks and CI.
- Human: reproduce setup, inspect separation/initialisation, understand a rule and its boundary tests, and check tool scope.
- Outputs: runnable skeleton, real tests, locked dependencies and Actions.
- Exit: functions actually built have collected passing checks, setup/CI work and the human accepts the loop.

Current L1 scope is the runnable shell, immutable row models, mutable per-session state factories, structural data checks, derived cutoff, 36 foundation test cases, hash-locked dependencies and four CI jobs. It excludes actor selection/permissions, creation/booking/cancellation operations and all waitlist behaviour. The [L1 record](reviews/L1-human-review.md) provides the actual evidence and pending human checklist. Stop here until ACCEPT_LOOP; L2 has not started.

### L2 Demo actors and ownership

- AI: implement fixed-ID/role selection and selected-actor function checks.
- Human: use valid actors to challenge role/owner boundaries; confirm no authentication claim.
- Outputs: selection, B01/B02/B10/B12/B13 as applicable and actual human evidence.
- Exit: implemented boundaries and CI pass with clear limits.

### L3 Creation and browsing

- AI: implement FR-02/FR-06/FR-07, strict creation lead and field/capacity validation.
- Human: check >24h/=24h/<24h, invalid types, S/C display, ownership and presentation-day seed readiness.
- Outputs: views/rules, B03-B06 and observations.
- Exit: valid creation works, rejection preserves input/counters, display/CI pass.

### L4 Booking and own history

- AI: implement FR-03/FR-05, I01/I02 and booking I10 using latest serial state.
- Human: check last place, duplicates, actor changes and stale submission, using fixtures that isolate each cause.
- Outputs: B07-B10 and in-memory integration evidence.
- Exit: selected capacity/uniqueness/time contracts and CI pass.

### L5 Cancellation and failure safety

- AI: implement pre-C cancellation, repeated-request safety, history/rebooking, I05 and cancellation I10.
- Human: verify valid non-owner denial, C boundaries, no-op repeats and original-state snapshots after failure.
- Outputs: B11-B17, I05/I10 and review evidence; full promotion I04 belongs to V1.1.
- Exit: history, cutoff, no-partial-mutation and regression checks pass.

### L6 Working V1.0

- AI: prepare complete baseline evidence, same-session demonstration and deployment notes.
- Human: perform VAL-01/VAL-02 and manual I06/I08/I09, inspect actual browser reset behaviour and accept declared limits.
- Outputs: CI, V&V, deployment URL, exact commit and v1.0 release.
- Exit: baseline FR/BR/QR and required validation accepted without blockers; record ACCEPT_RELEASE before waitlist implementation.

### L7 CR-01 waitlist increment

- AI: branch from V1.0, create Issue/intake/impact analysis and implement Join/Withdraw/positions plus I07 fixture compatibility.
- Human: inspect positive withdrawal during C<=t<S, post-C Join rejection, confirmed-list equality, position calculations and ownership.
- Outputs: branch, Draft PR after self-review, relevant W/I07 results and personal observations.
- Exit: ACCEPT_LOOP for the increment only. Incomplete promotion is not ready for complete-feature merge/release.

### L8 Complete CR-01

- AI: finish FIFO/complete-state promotion, old/new regression, three-phase I10 and a focused review task.
- Human: check independent test oracles, fresh boundary fixtures, repeats/withdrawn entries/failures, VAL-03A-VAL-03E and R-08 decisions.
- Outputs: complete PR, reports, AI disclosure, assessed findings and a current-SHA decision.
- Exit: critical checks and material user needs resolved before READY_TO_MERGE; otherwise changes/advice required.

### L9 V1.1 deployment and submission

- AI: prepare release notes, deployment/seed instructions and evidence links.
- Human: confirm current PR/CI and decide/execute merge; inspect main CI and deployed role/state flows, then decide release.
- Outputs: merged PR, main CI, smoke evidence, URL, v1.1 and submission materials.
- Exit: verified deployed commit, required validation and ACCEPT_RELEASE.

Each loop ends with a real personal decision. A record for an earlier increment is not approval for later commits. Prefer small coherent PRs; split oversized work without deploying incomplete features.

## CI implemented in L1

| Job | Checks and evidence |
|---|---|
| static-quality | Ruff on app.py, booking.py and test_booking.py; pip check; reports/installed versions |
| security-review | Bandit on app.py/booking.py and pip-audit on locked dependencies; scope, versions and assessed findings |
| tests | pytest test_booking.py; JUnit and booking.py branch coverage; applicable B/W/I scenarios, not a pretend database suite |
| quality-gate | Required quality gate succeeds only if all required preceding jobs succeed |

The executable [workflow](../.github/workflows/quality-checks.yml) uses Python 3.12.14, SHA-pinned Actions, hash-locked dependencies and a read-only contents token. It runs on main/codex branch pushes, PRs to main and manual dispatch when available on the default branch. Deployment dependencies must remain aligned in later loops. The current dependency audits cover runtime and development locks and query public package advisory data; there is no application database or credential requirement.

Retain available reports even on failure. Do not use blanket failure bypass; audit-network errors are not clean results. Record collected/passed/failed/skipped counts, head/base/tested SHA and run URL. Do not silently skip critical scenarios or call manual validation automated.

Assess substantive findings individually. A narrowly scoped temporary exception needs reason, owner, mitigation and expiry. Preserve selected evidence beyond artifact retention.

## Branches and releases

Use reviewed main, short codex/... branches/PRs and v1.0/v1.1 tags. Deploy accepted main commits; no extra release branch is required. L0 does not rename the current branch, publish a repository or create a release.

Commit coherent increments as the work actually occurs. Keep Issues, branches, checks and decisions in their real order rather than constructing a fictional development history at submission time. No arbitrary number of commits is required.

Merge only after current PR checks and human decision. Deployment may reset temporary data. Verify main CI and deployed smoke behaviour before accepting/tagging the release. Reversion is code-version recovery, not a promise to restore in-memory bookings.

The actual V1.0 tag must precede CR-01. Retain baseline tests/history; record approved requirement changes rather than rewriting releases.

## Submission and defence

Submit repository/app URLs, PPTX, a short submission document linking versions/CR/reviews/decisions, and AI-use documentation or Appendix A.

Aim for approximately 8-10 slides, 8-10 minutes presentation/demo and 4-5 minutes questions within the brief's approximate 12-15-minute session, subject to teaching instructions. Use the submitted deck unless changes are authorised.

Demonstrate the application and GitHub live. Explain a real defect, requirement weakness or lesson, selected test oracles, AI assumptions, findings and why merge was justified. Do not manufacture a runtime bug or reviewer approval.
