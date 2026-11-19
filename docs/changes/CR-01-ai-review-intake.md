# CR-01 AI Review Intake

| Field | Recorded value |
|---|---|
| Review scope | L7 planning and deep review through revision 2. Revision 3 records the author's acceptance and FIFO fixture requirement. |
| Reviewed baseline | [Published V1.0](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/releases/tag/v1.0), commit `36e7bff3c1d3f74bb29c1900373726ecffdd176b` |
| Tool | Codex assistant, with read-only GitHub inspection in the deep review and local file tools for English documentation and ZIP verification |
| Author request, English summary | Use the published and verified V1.0 baseline to prepare CR-01 for waitlist and FIFO promotion, impact analysis, risk classification, this intake, test mapping and regression planning. Preserve the baseline and current deployment. Stop for author acceptance before implementation. |
| Actual AI contribution | Drafted the five L7 records. During the deep review, checked the published baseline, rules, core code, rubric and lecture passages, and both stored CI reports. Revised the decision table, oracles, risk triage, regression comparison and human checklist. In revision 3, transcribed the author's decision, translated the fixture note, checked the identity model and synchronized the documents and local ZIP. |
| Implementation evidence | V1.1 source and test changes, candidate CI, PR review and VAL-03 remain future work. |
| Risk triage | The author approved High change classification and review depth under Week 6, slide 17. A change to an ordinary registration action affects allocation, ownership, deadlines and state integrity. Open policy and verification questions remain separate blockers. |

## Significant author interactions

| Author direction, English summary | Inputs inspected | Actual result and human status |
|---|---|---|
| Start L7 from published V1.0. Prepare CR-01, impact, risk, intake and tests. Hold implementation for acceptance. | V1.0 release evidence, requirements, test plan and the three core files. | Five English planning documents. The initial author decision remained pending. |
| Review the five documents against the baseline, HD rubric and lecture. Challenge FIFO, C/S, STATUS_CHANGED, High risk and retention of 317 cases. Fix findings and package the documents locally. | The document set, SHA-pinned V1.0 code and release, both exact-M CI reports, Assessment 3 pp. 4-5, 8, 12 and the lecture references below. | The five revisions and local ZIP preserve the prior scope. Planning findings and remaining decisions are recorded below and in the checklist. No runtime diff or human outcome was inferred. |
| Record completion of H01-H07 and ACCEPT_LOOP, approve D-01 and High, and require valid fixture identities for additional FIFO participants. Keep R-08 pending VAL-03 and hold V1.1 implementation. | The author's acceptance message, its six feedback items, the five revision 2 documents and the membership and role checks in `DemoState`, `resolve_actor` and `check_permission`. | Revision 3 records the human decision and updates the test-precondition wording. The author supplied the decisions and feedback. Codex updated the English records and local ZIP. See the [acceptance record](../reviews/L7-human-review.md#human-decision-record). |

Use fictional participants in test cases. A future reviewer needs relevant files, assumptions and evidence, with actual secrets, credentials and real participant data excluded.

## Intended behaviour and invariants

Create an explicit full-only WAITLISTED entry before C and automatically promote the earliest current waiter only when the selected owner effectively cancels a confirmed booking before C. Preserve strict creation lead, the confirmed freeze at C, effective waitlist withdrawal until S, historical IDs, confirmed roster counts, one active registration per participant/workshop and all V1.0 no-waiter behaviour. Preserve fictional identities and the single-session architecture. The outcome and expected state come from the accepted rules and CR, independently of proposed implementation.

## Expected change surface

- Future code: `booking.py` for state, actions, ownership and FIFO. `app.py` for current controls, feedback, views, clock wiring and adoption of completed results. `test_booking.py` for new tests and narrowly justified compatibility assertions where needed.
- Future evidence: the CR, requirements/test references, focused review, dispositions, Actions/PR checks and the author's decision. Link each significant prompt to the changed file or diff hunk, identify which code/tests/docs came from AI, and record author corrections or rejected suggestions with evidence. Keep unrelated changes out of the patch. The existing V1.0 sources remain immutable.
- Actual L7 files: `docs/changes/CR-01.md`, `docs/changes/CR-01-impact-and-risks.md`, `docs/changes/CR-01-ai-review-intake.md`, `docs/changes/CR-01-verification-plan.md` and `docs/reviews/L7-human-review.md` in the separate `L7_develop` workspace.

## Assumptions and planning findings

| Reference | Assumption or finding | Evidence | Planning disposition |
|---|---|---|---|
| L7-F01 | A stale Withdraw can target a now-CONFIRMED record. The original draft lacked precedence for ownership, repeats and time. | Baseline `cancel_registration` looks up the current ID, checks ownership and handles owned CANCELLED before validating the effective time. CR-01 promotion keeps that ID. | The author approved D-01 and STATUS_CHANGED. CRV-01 defines the required future evidence. |
| L7-F02 | The fixed app identities give only two participants. The normal selector cannot provide three distinct participants for one serial queue scenario. | `create_demo_state` seeds two participants and two organisers. W06 requires one confirmed and two waiters. The author identified the risk of INVALID_ACTOR if an added ID is absent from the tested state. | Register additional fictional participants in the exact fixture's `DemoState.users`. Resolve actors there and assert the intended outcome. Live UI retains its existing identities. |
| L7-F03 | Older test text includes a baseline registration-window phrase, while the UI has baseline-only waitlist wording. | `app.py` labels FULL and the footer in V1.0 terms. `test_booking.py` checks the registration-window caption around C. | Preserve the contract assertions. Document any authorised wording-only adjustments with unchanged or stronger semantic checks. |
| L7-F04 | Time-of-allocation evidence alone does not establish preparation feasibility. | R-08 and VAL-03C/D explicitly consider discovery after promotion. No notifications are planned. | Retain future human VAL-03A-E. No suitability decision in L7. |
| L7-F05 | The original FIFO and rejoin examples did not prove against wrong-scope selection or reuse of a removed maximum sequence. | BR-09/10/11 require workshop-specific order and monotonic sequence. A test that only checks earlier than the active tail can miss a reused cancelled sequence. | Added the independent W05/W06 oracle and W09 history/counter fixtures. Planning corrected. Implementation verification pending. |
| L7-F06 | The initial boundary row listed instants without separate eligibility and refusal oracles for each action. | BR-16 and I10 distinguish two deadlines. A duplicate, full Book or already cancelled record can fail for a different cause. | Added the W12 operation matrix, authentic fixtures and independent stale-submit, invalid-clock and no-op checks. Planning corrected. |
| L7-F07 | A count of 317 alone cannot verify retained regression cases. | Both stored V1.0 artifacts contain the same exact-M JUnit identities. The workflow writes event identity and Tested SHA. | Recorded the reproducible inventory fingerprint, later per-case comparison and event-specific gates. Baseline comparison verified. Candidate comparison pending. |
| L7-F08 | The original High review rationale mixed technical depth, expected reset and release blockers. | Week 6 slide 17 distinguishes risk depth from blockers. Week 9 covers reviewer competence and escalation. | The author approved High review depth and confirmed that open policy or evidence questions are separate blockers. Residual risk decisions remain pending where evidence is needed. |

Assume serial operation in one temporary session and controllable clocks only in tests. Use the canonical selected identity and the target's stored owner at the business layer. Keep trusted time and operation intent attached to actual entry points. Hold an unresolved state or policy ambiguity for review before it can determine allocation. D-01 defines the approved action-state outcome for the planned change.

## Focused review instruction for a future patch

Review the exact candidate diff against AC-01-AC-07 and the retained V1.0 suite. Challenge: full Book accidentally joins, an old Withdraw cancels a newly promoted booking, wrong FIFO comparator or cross-workshop selection, C/S inequality, caller-supplied identity/time, non-owner waitlist reads, incorrect capacity arithmetic, duplicated promotion, aliased counters and partial adoption. Check the proposed expected results before reading implementation. Check the changed file list, configuration and dependency lock diff. Report only substantive findings with evidence and suggested severity.

| Finding | Exact file and line or test | Requirement or risk | Observed evidence | Author assessment | Disposition | Follow-up proof |
|---|---|---|---|---|---|---|
| Pending actual patch review | Pending | Pending | Pending | Pending | Corrected, dismissed with justification, or unresolved | Exact SHA/run/test or explicit blocker |

For a later review, record the tool or reviewer and exact diff identity next to the findings. Include the prompt's scope, the AI output that was kept or changed, the author's own assessment, the owner and evidence of rerun for each substantive issue. The CR and exact branch/head, base and tested SHA must be discoverable from the PR. If none of the issues can be resolved within the declared scope, record the actual blocker and reviewer needed. The planning dispositions above do not close code or validation findings.

## Required future author review

Inspect the actual file diff, approved scope and business guards. Explain FIFO, the one-decision-time transaction model within the session, and the way independent oracles detect wrong behaviours. Review denied paths for identity, ownership, caller-controlled input, data exposure and configuration defaults as applicable. Check any AI-generated conclusions against source evidence and retain rejected suggestions or fixes with rationale. Record actual observations in the human record and later PR. The author supplies a justified risk judgement and a justified READY_TO_MERGE, CHANGES_REQUIRED or SPECIALIST_ADVICE_REQUIRED decision after verification. The project author personally performs all actual merges and deployment branch fast-forwards.

Course cross-check: Assessment 3 pp. 4-5, 8 and 12 cover change control, evidence links, AI disclosure and justified decisions. The 16 November 10:45 transcript pp. 2 and 8-10 emphasises the small three-file adaptation, bounded diffs and human review. The 10:46 transcript pp. 4-7 emphasises precise AI disclosure, checks, escalation and evidence for the defence. The Week 6 slides 11/17 support bounded intent, prompt-to-diff trace and triage; Week 7 slide 25 supports independent tests and object ownership; Week 8 slides 14-16 support findings and evidence; Week 9 slides 1/5/10/12 support author accountability and escalation. Source titles are listed in the [baseline source catalogue](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/blob/36e7bff3c1d3f74bb29c1900373726ecffdd176b/docs/demo-reuse.md#references).

References: [CR-01](CR-01.md), [risk and impact](CR-01-impact-and-risks.md), [verification](CR-01-verification-plan.md) and [L7 human review](../reviews/L7-human-review.md).
