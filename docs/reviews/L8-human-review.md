# L8 CR-01 candidate human review

Status: **HUMAN_ACCEPTANCE_PENDING**. Human decision: **PENDING**. R-08: **PENDING_VAL_03**. V1.1 release: **NOT_RELEASED**.

The candidate starts from published V1.0 commit `36e7bff3c1d3f74bb29c1900373726ecffdd176b`. The author's [L7 decision](L7-human-review.md#human-decision-record) approved D-01 and High review depth. The [change contract](../changes/CR-01.md) governs the candidate. The existing V1.0 deployment remains on its released baseline.

## Technical evidence

The [test map](../test-plan.md#l8-cr-01-verification) covers 317 exact V1.0 JUnit identities, 31 first-candidate L8 identities and three review additions. The original [L8 push run 44536979502](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44536979502) passed 348 cases at `a0f3121453b3a99280ecd18400252971c31889ab`. Use the [candidate branch Actions](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions?query=branch%3Acodex%2Fcr-01-waitlist) and the separately saved local review evidence for the revised candidate's exact SHA, job and reports. The tests exercise serial in-session behaviour and controlled time. Human acceptance and VAL-03 need separate author evidence.

## Deep review findings and dispositions

| ID | Finding and risk | Disposition and verification |
|---|---|---|
| L8-F01 | **Medium.** A submitted Join control could disappear before the UI handled it if a cancellation made a place available. The first candidate omitted the USE_BOOKING guidance and the user had no decision feedback. | Corrected. Run the callback before rendering controls. Use the current state, trusted time and the existing business result. A before-and-after AppTest reproduces the missing feedback and verifies the repaired response, unchanged state and no extra allocation. |
| L8-F02 | **High review depth.** A callback resolved against a newly selected identity alone could enrol the wrong participant when a stale click and identity change were submitted together. | Corrected in the callback. Bind Join to the rendered selected ID and compare it with the current selection before resolving the actor. The AppTest switches between two eligible fixture participants on a full workshop and verifies rejection and exact state preservation. This is a classroom-demo action guard. |
| L8-F03 | **Medium.** Join's no-notification guidance depended on a help popover and distant policy text. At S the organiser table still used a live Position heading. | Corrected. Show essential waitlist information next to an open Join button. Show Queue order at close in the organiser's historical view. Verify the closed view preserves stored WAITLISTED rows and the confirmed roster. R-08 remains PENDING_VAL_03. |

The business module remains byte-identical to the first L8 candidate. Reviewed FIFO workshop scoping and sequence high-water marks, fresh C/S clock boundaries, the approved D-01 precedence, Leo/Willy membership, owner permissions, and complete candidate adoption. Independent tests use list, name and timestamp orders that disagree with sequence order. Boundary and repeat tests use distinct active and already-cancelled records.

## Assessment and lecture cross-check

Assessment 3 pp. 4-5 and 8 require the change request, impact, retained and new tests, review intake and findings, a justified decision, and release links. The HD criteria on p. 12 cover lifecycle evidence and CI. This L8 candidate supplies the scoped delta and technical evidence. The author review, justified PR decision and separate V1.1 publication evidence remain future stages.

The 16 November 10:45 transcript pp. 2 and 8-10 supports the three-file adaptation and narrow behavioural changes. The 10:46 transcript pp. 3-7 supports precise AI disclosure, risk-specific review, traceable proof and author judgement. Week 6 slides 11/17 inform the intake and High classification. Week 7 slide 25 informs independent oracles and object ownership. Week 8 slides 14-16 and Week 9 slides 1/5/10/12 inform finding dispositions, escalation and the author-led decision. See the [accepted intake](../changes/CR-01-ai-review-intake.md) and [actual AI contribution](../ai-use.md#l8-cr-01-ai-use).

## Author checklist

- [ ] **L8-H01 - Check the baseline and delivery.** Confirm candidate ancestry from published M and review the scoped correction. Check the single-job Actions report against the revised SHA and verify the 317 baseline cases, the original 31 L8 identities and the three review additions.
- [ ] **L8-H02 - Check explicit Join and ownership.** In a fresh local demo session, select Xingjian and open Outdoor Photography Walk, which starts full. Book should report FULL. Join should create a WAITLISTED record. Verify position 1, the original confirmed count and the absence of another participant's private entries in My Bookings.
- [ ] **L8-H03 - Check withdrawal and history.** Withdraw Xingjian's waiting record and verify retained CANCELLED history and unchanged roster. Rejoin before cutoff and verify the new ID. Review the Leo/Willy test evidence for FIFO, sequence gaps and multi-waiter ordering.
- [ ] **L8-H04 - Check promotion.** With Xingjian queued, switch to Sam in the same session and cancel Sam's confirmed Outdoor Photography Walk booking. Return to Xingjian and use Refresh view. Verify the same queued ID is CONFIRMED. Check Alex's owned roster and queue, and check Rui Yan's workshop selector for owner scope.
- [ ] **L8-H05 - Review C/S and D-01.** Inspect the independent boundary and stale-action tests for C and S. Confirm a stale Withdraw targeting a promoted row reports STATUS_CHANGED, preserves the confirmation and follows actor/owner checks. Check the fault-injection assertions for no partial state.
- [ ] **L8-H06 - Review AI use, risk and disclosure.** Check the [AI record](../ai-use.md#l8-cr-01-ai-use), fixture-only identities and L8-F01-F03 dispositions. Confirm the no-notification explanation is visible before using Join. Keep R-08 pending human VAL-03 awareness and feasibility evidence.
- [ ] **L8-H07 - Record the decision.** Record the exact reviewed SHA, observations, issues and ACCEPT_LOOP or CHANGES_REQUIRED. Subsequent integration and release decisions are separate. All actual merges and deployment fast-forwards are author-only.

## Author decision record

| Field | Value |
|---|---|
| Reviewer, date and time zone | Pending |
| Reviewed SHA and environment | Pending |
| Checks and observations | Pending |
| Findings and follow-up | Pending |
| Decision | Pending |
