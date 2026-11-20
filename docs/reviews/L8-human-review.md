# L8 CR-01 candidate human review

Status: **HUMAN_ACCEPTANCE_PENDING**. Scope: **P1**. P2: **NOT_STARTED**. Human decision: **PENDING**. R-08: **PENDING_VAL_03**. V1.1 release: **NOT_RELEASED**.

The candidate starts from published V1.0 commit `36e7bff3c1d3f74bb29c1900373726ecffdd176b`. The author's [L7 decision](L7-human-review.md#human-decision-record) approved D-01 and High review depth. The [change contract](../changes/CR-01.md) governs the candidate. The existing V1.0 deployment remains on its released baseline.

## P1 UI verification

P1 refines presentation and interaction feedback on the L8 candidate based on `fbbc86c2de7dcc9960097a0b6f6caf0dc1823606`. The source delta covers `app.py`, `test_booking.py`, this review, `docs/ai-use.md`, `docs/test-plan.md` and a P1 pointer in `docs/changes/CR-01-verification-plan.md`. The business module, dependencies, workflow, published deployment and accepted L7 evidence remain intact.

| Requirement | Before P1 | P1 result and review evidence |
|---|---|---|
| P1-01 / P1-02 | Cards presented details in one column and open full workshops used generic registration-window copy. | Give each card a title, availability badge, schedule, counts and meeting point, with notes and identity preserved. Verify C/S against fixed clocks and full versus available fixtures. Keep Book and explicit Join adjacent, with FULL advice on its own line. |
| P1-03 | History preceded waiting entries, and Cancel controls had a separate section. | Place Upcoming Confirmed Bookings, My Waitlist and Booking History in order. Include the workshop and registration ID in the matching active action. Put current position in the waiting table ahead of dates. Started and cancelled records appear in history with their stored status. |
| P1-04 | Action feedback used different explanations for similar outcomes. A stale Cancel could disappear before showing repeat feedback after the record became cancelled. | Share refusal guidance. Cancel runs the original operation against current actor, state and trusted time before rendering. An isolated test on the intake reproduced the missing repeat message. P1 tests preserve no-op outcomes at S and after cancellation. A successful cancellation reports a promotion only when a waiting registration became confirmed. |
| P1-05 | The current identity was repeated in the sidebar and absent from main content. | Show the fictional identity and role next to the heading, retain selection and scoped menus, and display the authentication limit. AppTest and Chrome exercise switching and deselection. |
| P1-06 | C/S and notification guidance was spread across different views. | Label both times beside workshop details, explain the cutoff near Cancel, and place unconfirmed status and no-notification guidance next to Join or Withdraw. Explain withdrawal through the final 24 hours. R-08 remains PENDING_VAL_03. |

The focused local run passed 113 cases, including 12 new P1 cases and the selected regression cases. The complete local run passed 363 cases under Python 3.12.14 and PyArrow 24.0.0, retaining all 351 intake identities. Ruff, formatting, Bandit and pip check passed locally. Exact GitHub CI and delivery evidence are recorded in the local receipt and on the [candidate Actions page](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions?query=branch%3Acodex%2Fcr-01-waitlist). The older CR-01 execution evidence below retains its original scope.

The original P1 browser verification exercised the four badges, FULL and Join, withdrawal and rejoin, promotion of the same ID, section order and role switching. A fresh 390px browser checked the public card layout. See the [P1 test map](../test-plan.md#l8-p1-presentation-verification). Technical checks provide no author acceptance or human VAL-03 observations.

### P1 deep review

Review intake: `46eba1d20df09b9ae849f1808549a5b2e866dcb3`. Its 363-case single-job [Actions run](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions/runs/44546334817) remains evidence for that exact SHA. The revised [local review preview](http://127.0.0.1:8523/) uses a separate port so the original 8522 session stays available.

| Requirement | Deep-review result |
|---|---|
| P1-01 | Card title, schedule, ID, meeting point, notes and counts remain visible. Desktop and 390px public-card checks passed. |
| P1-02 | AppTest checks full and available cards at C-1s, C, C+1s, S-1s, S and S+1s, including disabled controls and unchanged state. |
| P1-03 | Confirmed, waiting and historical sections render in order. Live position appears only while waiting before S. Withdrawal and promotion preserve history and the expected IDs. |
| P1-04 | A stale Book click submitted alongside an identity switch could book for the newly selected participant or lose feedback after a switch to organiser. Both AppTest variants failed on intake. The callback now binds the rendered identity, rejects the mismatch with INVALID_ACTOR and preserves state. The existing stale cutoff test captures an enabled control before advancing its clock. Cancel and Withdraw retain the established no-op and status-change outcomes. |
| P1-05 | AppTest and Chrome verified participant, organiser and guest transitions. The main badge and the role-specific views follow the selected identity, and the authentication limit remains visible. |
| P1-06 | C/S and no-notification guidance remain next to the relevant actions. Waiting withdrawal stays available at C and is refused at S. Human awareness and preparation feasibility remain pending under VAL-03. |

L8-F01, L8-F02 and L8-F03 remain covered by the original stale Join capacity, stale Join identity and organiser closed-queue cases. The review preserves the published 317 V1.0 cases and all 363 intake JUnit identities, with two additional P1 review cases. The sole existing test-body adaptation preserves the stale Book cutoff outcome and full-state check under the new callback order. Business rules in `booking.py`, dependency locks and CI configuration remain byte-identical. Exact-commit CI and packaging evidence are in the local delivery receipt.

### P1 acceptance feedback correction

The author reported that a participant with a booking could still see an enabled Join control when the same workshop became full, and that joining a different full workshop or clicking Join could appear to produce no feedback. Reproduction showed that Join was gated by capacity and time alone. Its feedback rendered at the top of Workshops, outside the selected card.

| Author observation | Correction and evidence |
|---|---|
| A participant books one workshop, then Book on another full workshop returns FULL. Join appears silent. | The separate Join action remains eligible for the other workshop. Its result now appears inside that workshop's card. Chrome verified FULL followed by WAITLISTED and a registration ID. |
| Booking the last seat leaves Join enabled for the same participant. | A confirmed or waiting registration owned by the selected participant disables Join for that workshop, with a reason on the card. Chrome verified that another eligible participant can still join. |
| Join feedback is missing near the button. | Success shows the created ID and directs the user to My Bookings. Refusals appear on the same card. A delayed duplicate is still refused by the business layer with no state or counter change. |

Both focused reproduction cases failed on intake and passed after correction. The revised [preview](http://127.0.0.1:8524/) keeps earlier preview sessions available. The original 365 test identities are retained and two acceptance-feedback cases extend them. This is a P1 technical correction. The author still owns acceptance and VAL-03.

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

- [ ] **L8-H01 - Check the baseline and delivery.** Confirm candidate ancestry from published M and review the scoped P1 delta. Check the single-job Actions report against the revised P1 SHA and verify the 317 baseline cases, 34 earlier L8 cases, 12 initial P1 cases and two review additions.
- [ ] **L8-H02 - Check explicit Join and ownership.** In a fresh local demo session, select Xingjian, who already has a different booking, then open the full Outdoor Photography Walk. Book should report FULL on its card. Join should show WAITLISTED and the registration ID on the same card, then become disabled with a reason. In a separate session, cancel Sam's seed booking and book that last seat again. Verify Join is disabled for Sam with the confirmed-booking explanation and is available to eligible Xingjian.
- [ ] **L8-H03 - Check withdrawal and history.** Withdraw Xingjian's waiting record and verify retained CANCELLED history and unchanged roster. Rejoin before cutoff and verify the new ID. Review the Leo/Willy test evidence for FIFO, sequence gaps and multi-waiter ordering.
- [ ] **L8-H04 - Check promotion.** With Xingjian queued, switch to Sam in the same session and cancel Sam's confirmed Outdoor Photography Walk booking. Return to Xingjian and use Refresh view. Verify the same queued ID is CONFIRMED. Check Alex's owned roster and queue, and check Rui Yan's workshop selector for owner scope.
- [ ] **L8-H05 - Review C/S and D-01.** Inspect the independent boundary and stale-action tests for C and S. Review both stale Book identity-switch cases and the retained stale Join cases. Confirm a stale Withdraw targeting a promoted row reports STATUS_CHANGED, preserves the confirmation and follows actor/owner checks. Check the fault-injection assertions for no partial state.
- [ ] **L8-H06 - Review AI use, risk and disclosure.** Check the [AI record](../ai-use.md#p1-ui-contribution-and-review-boundary), fixture-only identities and L8-F01-F03 dispositions. Confirm the C/S guidance, section order and visible no-notification explanation. Keep R-08 pending human VAL-03 awareness and feasibility evidence.
- [ ] **L8-H07 - Record the decision.** Record the exact reviewed SHA, observations, issues and ACCEPT_LOOP or CHANGES_REQUIRED. Subsequent integration and release decisions are separate. All actual merges and deployment fast-forwards are author-only.

## Author decision record

| Field | Value |
|---|---|
| Reviewer, date and time zone | Pending |
| Reviewed SHA and environment | Pending |
| Checks and observations | Pending |
| Findings and follow-up | Pending |
| Decision | Pending |
