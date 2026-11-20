# L7 human review and planning acceptance

Status: **ACCEPT_LOOP**, recorded in revision 3. The project author reported completing L7-H01 through L7-H07, approved D-01 and High review depth, and supplied the feedback below. V1.1 is **NOT_STARTED** and held by the author.

Owner: project author. Date prepared: 19 November 2026, Asia/Shanghai.

## Completed technical planning review

The revision 2 technical review verified the annotated `v1.0` tag and release against M, the Main and deployment branch heads, and the two stored exact-M CI artifacts. Both JUnit artifacts have 317 passing case identities and matching inventory fingerprints. The [review findings](../changes/CR-01-ai-review-intake.md#assumptions-and-planning-findings) record the contract, oracle and review corrections. R-08 remains open for real VAL-03 evidence.

Assessment 3 pp. 4-5, 8 and 12 cover change scope, revised and retained tests, auditable CI and AI use, justified decisions and a versioned release. This package prepares the L7 evidence for that lifecycle. The later implementation, PR decision, validation and release have separate evidence gates. The lecture cross-check is recorded in the [AI Review Intake](../changes/CR-01-ai-review-intake.md). It informs the bounded three-file change, risk triage, test oracles and author-led decisions.

## Completed author checklist

Completion and observations are recorded from the author's acceptance message.

- [x] **L7-H01 - Confirm the published baseline.** The author confirmed M, the annotated tag, Release, both CI runs and the separate planning package.
- [x] **L7-H02 - Walk through the change contract.** The author confirmed explicit Join, workshop-scoped FIFO, history and counter preservation, sequence gaps and rejoining.
- [x] **L7-H03 - Decide D-01 and check C/S.** The author confirmed the boundary matrix and approved STATUS_CHANGED for a stale withdrawal on a promoted record, with actor and owner checks first.
- [x] **L7-H04 - Review impact and risk.** The author approved High review depth and separate treatment of unresolved policy and verification blockers.
- [x] **L7-H05 - Challenge the test oracles and regression gate.** The author accepted the independent expected results and 317-case baseline inventory, and required registration of test-only participants in the relevant fixture state.
- [x] **L7-H06 - Review AI use and validation.** The author confirmed the separation of planning and future evidence, with R-08 pending VAL-03.
- [x] **L7-H07 - Record the planning decision.** The author supplied ACCEPT_LOOP and directed that implementation remain on hold.

## Human decision record

| Field | Author entry |
|---|---|
| Reviewer and record date | Project author. Acceptance recorded on 19 November 2026, Asia/Shanghai. |
| Checked items and observations | H01-H07 complete. See all six feedback items below. |
| Reviewed revision and V1.0 baseline SHA | The author reviewed revision 2 against M `36e7bff3c1d3f74bb29c1900373726ecffdd176b`. Revision 3 records that review and the author's fixture clarification. |
| CR-01 scope and correction | Waitlist and FIFO promotion in the serial demo scope. Additional FIFO participants must be valid users in the test fixture's own `DemoState.users`. |
| D-01 stale action precedence | Approved. Actor and stored ownership checks precede the stale-status response. A stale Withdraw for a promoted confirmation yields STATUS_CHANGED and preserves the state. |
| Review depth and blockers | High approved for allocation, ownership, deadlines and state integrity. Assess unresolved policy or verification questions as separate blockers. |
| Remaining validation and owner | R-08 pending the project author's disposition based on future human VAL-03 evidence about awareness and preparation feasibility. |
| Decision | **ACCEPT_LOOP** for L7 planning. V1.1 implementation remains held pending further author direction. |

## Author feedback

Items 1-6 are the author's submitted observations. The fixture requirement appended to item 5 has been translated into English.

1. CR-01 correctly uses the published V1.0 commit M as its baseline. The annotated tag, Release and two successful CI runs are traceable. The five L7 planning documents are separate from the accepted baseline.
2. The CR-01 contract distinguishes direct booking from explicit waiting. FIFO promotion selects the earliest active waiter in the same workshop. Withdrawal and repeated requests preserve history, capacity and counters. Independent examples cover sequence gaps and rejoining after withdrawal.
3. The C/S boundary matrix is consistent with the accepted policy. I recommend approving D-01: a stale withdrawal targeting a promoted confirmation should return STATUS_CHANGED without modifying the record. Actor and ownership checks must precede this result.
4. High review depth is justified because the change affects allocation, ownership, deadlines and state integrity. The proposed classification is a review priority, not evidence of an existing production defect. Unresolved policy or verification questions must be treated as separate blockers.
5. The verification plan uses independent expected IDs, statuses, sequences, capacities and full-state snapshots. The 317-case V1.0 inventory has been independently confirmed. The future V1.1 candidate must retain those cases and pass additional waitlist tests; no candidate execution is claimed at L7. A third or fourth participant in a future test must be a valid fixture identity registered in the corresponding `DemoState`. Passing an ID absent from that state may produce only INVALID_ACTOR, leaving FIFO untested.
6. The AI intake clearly separates planning contributions, assumptions and future implementation evidence. R-08 correctly remains pending for V1.1 validation. Promotion correctness does not establish timely participant awareness or preparation feasibility, particularly without notifications.

Technical verification, human validation, the justified PR decision, human-only merge and deployment fast-forward, and release approval remain separate future events.

Review material: [CR-01](../changes/CR-01.md), [impact and risks](../changes/CR-01-impact-and-risks.md), [AI Review Intake](../changes/CR-01-ai-review-intake.md), [verification and regression plan](../changes/CR-01-verification-plan.md).
