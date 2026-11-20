# L9 V1.1 integration and author review

| Item | State |
|---|---|
| Accepted L8 reference | [2531b0d](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2531b0db583564695d3665880df30fda04b102e9), which records the author's L8 ACCEPT_LOOP for a1e0d3a. |
| L9 review candidate | `codex/l9-v11-integration`. See the [candidate Actions](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions?query=branch%3Acodex%2Fl9-v11-integration) and the local L9 technical evidence for the exact tested commit. |
| L9 decision | `ACCEPT_LOOP` by the project author on 20 November 2026 (Asia/Shanghai). See the [author's L9 decision](#l9-acceptance-and-residual-risk-decision). |
| Risk R-08 | `ACCEPTABLE_WITHIN_SCOPE` as a residual risk for the fictional classroom booking and waitlist prototype. |
| L10 and V1.1 release | L10 `NOT_STARTED`. V1.1 `NOT_RELEASED`. |
| Preview | [L9 policy-order revision](http://127.0.0.1:8530/) for VAL-03. The running preview uses application code from `fab46fa`. The VAL-03A and risk-record follow-up changes documentation only. The 88f7dbf and earlier L9 previews remain on ports 8529 and 8528. |

## Integration verification

The new AppTest fixes the local test clock to the canonical Asia/Singapore schedule. A normal Streamlit cancellation at C minus one minute changes the confirmed booking and promotes the head waiter with the original ID. At C plus five minutes the same session shows the promotion and a closed confirmation cancellation. The remaining waiter may still withdraw, with the confirmed seat and the other registrations preserved. The test checks full state changes, the rendered update timestamp, and the no-notification guidance. The L9 test now also submits a previously enabled Cancel control at exact C with two active waiters in a separate session. The attempt returns REGISTRATION_CLOSED and preserves the entire queued state. It verifies that successful promotion and withdrawal leave the previous state objects intact. Existing cases also cover the S boundary, D-01, owner scope, FIFO variants and fault injection.

This is integrated technical evidence for the app's behaviour. The VAL-03 scenarios below measure whether someone understands and can act on that behaviour.

## Deep review findings

| Finding | Disposition |
|---|---|
| L9-F01. Exact-C coverage used a domain test with an active queue and an older stale-control UI test with an empty queue. | The L9 integration test combines a stale Cancel submission with an active queue at exact C. It keeps the existing case identity and strengthens transition checks on retained state objects. |
| L9-F02. A scheduled check at C plus five minutes demonstrated the expected page and controls, while giving the participant a prompt to discover promotion. | Retain that replay for boundary verification. The author records ordinary checking behaviour before reviewing timed instructions, then compares the first ordinary check and the latest useful time for a booking decision. Preparation constraints supply context for that time. At this technical checkpoint, personal evidence was pending. See the final author decision below. |
| L9-F03. The L9 test delegated the confirmed roster count to production code and lacked a post-discovery stale-withdrawal check against both the owner and another participant. | Require the exact confirmed registration ID from the state. Check a stale owner's Withdraw control against the latest promoted state for STATUS_CHANGED. A separate domain check requires FORBIDDEN for Willy targeting Leo's entry at the same instant. Both refusals must keep the complete state and object identity. |
| L9-F04. The manual B setup assumed both waiters had joined. The E steps could use a withdrawn record as the at-S test subject. | Make both joins and the pre-withdrawal roster snapshot explicit. Check S in a separate still-active waiting case because a cancelled entry takes the idempotent repeat path. |

## L9-F05 Booking & Waitlist Reminder

The author requested participant-focused support for booking awareness under R-08. The accepted CR-01 policy governs the same actions and data. The classroom FIFO walkthrough is recorded in the README.

| Area | Before | Revised UI |
|---|---|---|
| Entry point | Demo Guide describes the fictional FIFO demonstration. | A compact participant-only booking and waitlist reminder explains manual checking, C/S and the absence of automatic alerts. |
| Before C | Generic advice and a notice near Join. | The waiting notice explains FIFO and checking regularly before C. The confirmed notice points to meeting point and preparation notes and explains the cancellation deadline. |
| From C to S | A waiting row still shows its position and a confirmed cancellation is disabled. | A waiting row explains that promotion has closed and withdrawal remains possible before S. A confirmed row explains the closed cancellation deadline. |
| At and after S | The history table holds recorded statuses. | Guidance points to Booking History and explains action closure. Stored WAITLISTED records remain historical. |
| Counts | Confirmed participants and generic confirmation labels. | Confirmed bookings and remaining places refer to allocated registrations, with a booking-count explanation. |

The UI uses the existing selected-identity scope, statuses and C/S comparison. [Test adaptations](../changes/CR-01-test-adaptations.md#l9-f05-reminder-and-booking-count-assertions) record the visible assertion changes and unchanged behavior checks. Participants still rely on manual checking. The final author decision accepts this residual risk within classroom scope.

### Policy placement follow-up to 88f7dbf

The public Registration policy appeared below the work area. Move the existing text immediately above the participant reminder, outside the selected-identity container. Guest and organiser views still show the public policy. Only participants see the reminder, on Workshops and My Bookings.

The existing read-only UI test now requires one policy title and paragraph in each role and requires both to precede the reminder on both participant views. It retains organiser tabs, owned roster choices, both saved drafts and whole-state assertions. The five time cases and retained booking-count and permission assertions still verify the same outcomes. For the revision's exact CI and browser evidence, see the candidate Actions and the local policy review report.

### Author review follow-up

The author noted that the public policy is always visible and the reminder starts collapsed. The VAL-03A worksheet now captures the same comprehension questions in both states. The author also identified stale descriptions of the current demo identities and Demo Guide in the [risk record](../changes/CR-01-impact-and-risks.md#l9-documentation-follow-up). This is a low-risk documentation finding. The High CR-01 review classification and the R-08 decision gate remain in place.

## Assessment 3 and lecture cross-check

| Criterion and source | Evidence and remaining gate |
|---|---|
| Requirements, risk and traceability, Assessment 3 pp. 3-5 and 10 | [CR-01](../changes/CR-01.md) AC-02 to AC-05 and AC-07 link to FR-09 to FR-11, BR-06/09/10/11/13/15/16, QR-02/03 and R-08. Follow the [test map](../test-plan.md#l9-v11-integration-verification) and the L9 finding dispositions. |
| Verification, validation and failure coverage, pp. 10-11 | The two independently prepared UI states check a valid cancellation before C and a stale submit exactly at C. D-01 checks prove owner/status precedence at C plus five minutes. Retained cases cover S, time-zone comparison, separate scope and failed promotion atomicity. The oracle uses the approved outcomes, exact IDs and expected snapshot changes. The final author decision records VAL-03 suitability within the classroom booking scope. |
| Controlled change and CI, pp. 4-5 and 12 | The separate branch descends from accepted L8. All 377 L8 cases remain. The exact-candidate single-job evidence and L9 finding dispositions support traceability. The completed-assessment chain also requires a PR with the Actions result, a justified author merge decision, approved integration and a deployed V1.1 release. Those stages remain pending. |
| Deployment and defence, pp. 8, 10 and 13 | Published V1.0 and the local candidate have separate evidence. The author should explain why time-of-promotion is different from time-of-discovery and why owner checks precede status. The AI record and review intake identify the scoped changes, assumptions, checks and author decision points. |
| 16 November lectures, 10:45 transcript pp. 2 and 8-10, 10:46 transcript pp. 3-7 | Keep the three-file app structure, a bounded change, named checks and an audit trail. Week 7 slides 24-25 inform object-scope checks, Week 8 slides 14-16 inform focused review and gates, and Week 9 slides 10 and 12 inform escalation and author ownership. |

## L9 author feedback and scope decision

On 20 November 2026 (Asia/Shanghai), the author supplied the following review feedback and clarified that this project manages booking and waiting records. This is a summary of the author's review. This feedback preceded the separate acceptance declaration below.

| Review item | Author feedback and evidence type |
|---|---|
| H01 | Technical review supports the L8 ancestry, exact-SHA single job and 383 cases, including 378 retained cases. The public policy precedes the default-collapsed participant reminder. Business policies remain consistent. |
| H02 | The two-pass VAL-03A answers were a simulation. They suggest where the reminder could help. VAL-03B describes expected same-ID FIFO promotion and the position change from two to one. A guided refresh illustrates the path. At this feedback checkpoint, the simulated responses and guided steps were separate from actual human validation. |
| H03 | The controlled test shows successful promotion one minute before C with the same ID. The 24 hours and one minute before S describes the technical schedule. |
| H04 | The controlled replay shows Leo confirmed after C, with cancellation closed, and Willy still able to withdraw before S. A prewritten check plan and a guided check answer different questions. The role-play discovery time is an estimate. |
| H05 | Retained tests cover withdrawal, history, unchanged roster and no promotion. An active request at S returns WORKSHOP_STARTED. The repeat of an already cancelled record returns ALREADY_CANCELLED. Use a labelled technical reference or walkthrough if the live S boundary is impractical. |
| H06 | The author reviewed the integration and AI records and identified the remaining risk of delayed discovery without alerts. The final author disposition is recorded below. |

## VAL-03 author worksheet

### Scope and acceptance basis

The task is to understand and manage a booking or waiting status. Check whether the participant can locate and interpret their latest record, recognise the applicable C/S rules and discover a promotion in time for a stated booking decision. Record outdoor preparation, safety information or travel constraints only when they explain why a booking decision is time-sensitive. A confirmed place is a reservation. Actual attendance, completed preparations, travel performance, check-in and no-show handling are outside the assessment.

Use fictional identities and workshop details. Record the candidate commit, session type, timezone and tester role. Use Asia/Singapore (UTC+08:00) when recording C, S and observations. Use the revised Booking & Waitlist Reminder preview on port 8530 for VAL-03A-E. Preserve the browser session through each live sequence. Switch identities through the sidebar and use **Refresh view**. Prepare a separate fresh session for the normal-promotion exercise so the waitlist starts clean. Write down what you understood and would do before consulting the technical evidence. Before reading the scenario rows or timed instructions, prewrite when and where you would normally check without any app alert, including your reason and any user-set reminder. Use that plan to assess the timing of the booking decision below.

| Scenario | Author task | What to record |
|---|---|---|
| VAL-03A | In a fresh session, join the full Outdoor Photography Walk as Leo and find your entry in My Bookings. Use the two-pass worksheet below. | Record the same answers before and after opening the reminder. Capture the registration ID once, and record cues, corrections and remaining uncertainty for each pass. |
| VAL-03B | In a fresh session, join the full Outdoor Photography Walk as Leo, then join it as Willy. Verify both positions before switching to Sam and cancelling before C. Switch back to Leo and use Refresh view. Identify the status and practical next step. | Time of cancellation and first check, retained registration ID, location of the current status, and what you would do next. |
| VAL-03C | In the timed exercise, find a near-C promotion in My Bookings and explain its meaning, ID and remaining actions. State the latest useful time for learning this status for the booking decision being tested. | Promotion and first-check times or labelled estimates, the preserved ID, the decision, the latest useful time and its reason. |
| VAL-03D | After a near-C promotion, first check the same session after C. Compare Leo's confirmation and closed cancellation with Willy's waiting entry and open withdrawal before S. Compare a guided refresh with the prewritten checking plan. | Whether discovery was prompted, unprompted or estimated. Record the discovery lag, action availability and whether the first ordinary check meets the stated booking-decision time. |
| VAL-03E | Before S, record Alex's confirmed roster from D. Switch to still-waiting Willy, withdraw, then compare Alex's roster and Willy's history. For the at-S check, use a separate still-active WAITLISTED entry or a clearly labelled policy walkthrough. | Preserved entry ID, historical status, and the before and after roster. At S, distinguish the closed active entry from Willy's already cancelled record, which follows the repeat rule. Label a walkthrough separately from a live observation. |

### VAL-03A comprehension with the reminder closed and open

Use a fresh browser session so the reminder is collapsed by default. Keep it closed while you record the first pass. Read the normal interface as you would during ordinary use. The public Registration policy may be one of the cues you notice. Keep the first answers as written. Open the reminder, read it and answer the same questions again before consulting the technical evidence.

For each pass, explain in your own words what your current status means for attending, which actions close at C and at S, whether you expect an automatic notification, and where, how and when you would check for a promotion.

| Pass | Answers and cues | Comprehension finding |
|---|---|---|
| Reminder still collapsed | Pending. Record your answers, where you looked and the cues you actually used. | Pending. Record any unclear or incorrect point. |
| After reading the reminder | Pending. Answer the same questions again and record what the reminder clarified, confirmed or left unresolved. | Pending. Assess these answers separately and compare with the first pass. |

If both passes are correct, record that the default view supported understanding in this exercise and note what the reminder added. If understanding improves only after opening it, record which information depended on discoverability. Keep any remaining confusion visible. This evidence addresses comprehension. The later scenarios assess discovery in time for the stated booking decision.

#### Author-submitted VAL-03A responses

Source: The project author submitted both passes in Chinese on 20 November 2026 (Asia/Shanghai). The answers below are English translations of the author's responses. They refer to the `21d523f` worksheet. The author later identified these answers as simulated. They are retained as author-supplied role-play. No live observation, exercise timestamps or observed registration ID were supplied.

| Question | Pass 1: Reminder still collapsed | Pass 2: After reading the reminder |
|---|---|---|
| Q1. Does WAITLISTED mean I have a reserved place? | No. WAITLISTED means I am still on the waiting list. I do not currently have a confirmed place. | No. WAITLISTED only means I am in the queue. Only a change to CONFIRMED means I have a reserved place. |
| Q2. Which operations close at registration cutoff (C)? | I understand that new bookings and cancellation of confirmed bookings close at C. I am unsure whether all waitlist operations close then as well. | At C, new bookings, joining the waitlist, confirmed booking cancellation and automatic FIFO promotion close. C is 24 hours before the workshop starts. |
| Q3. If I am still WAITLISTED at C, what can I do before S? | I should still be able to see my waiting status. If I no longer want to wait, I may be able to leave the waitlist before the workshop starts. | I can withdraw my waitlist entry before S and see the retained record in Booking History. Waiting withdrawal closes at S. |
| Q4. Will the system notify me automatically if I am promoted? | I am unsure whether the system will notify me automatically. I may need to open it and check the status myself. | No. The system sends no automatic notifications. I have to check My Bookings myself to discover whether WAITLISTED has become CONFIRMED. |
| Q5. Where, how and when should I check for a change? | I would check my booking status in My Bookings and check again before the workshop starts. I am unsure how often I should refresh. | I would open My Bookings and click Refresh view. I would check regularly before C, again near C, and after C to confirm the final allocation status. I could also set my own phone reminder to avoid missing the promotion. |

**Technical comparison of the author responses.** The first pass correctly identifies an unconfirmed waitlist place, the two confirmed booking operations that close at C, and My Bookings as the place to look. It leaves the Join and promotion cutoff, the withdrawal deadline, automatic notifications and how often to refresh unresolved. The second pass addresses all five questions consistently with the candidate. This comparison describes the simulated answers. These simulated answers remain separate from the subsequent author-declared validation outcome. VAL-03C/D examine the timing of discovery and available booking actions separately.

### Timed exercise for C and D

1. In the L9 preview, select Alex and create a capacity-one workshop with a unique name such as **VAL-03 Ridge Walk**. Choose C at least 10 to 15 minutes in the future and set S exactly 24 hours after it in Asia/Singapore. Allow for a date change around midnight. Make the end later than S. Add a fictional meeting point and preparation notes covering water, footwear and a check-in time. If the chosen C passes before setup is complete, start a fresh scenario with a later S.
2. In the same session, book the seat as Sam. Join the queue as Leo, then as Willy. Record the IDs and read C and S on the workshop card. Return to Sam's My Bookings.
3. Use the time shown on the card and a separate clock. Cancel at about one minute before C. For C, observe Leo's result before C and note the actual time. For D, leave Leo's view unopened until about five minutes after C. Use the sidebar and Refresh view while preserving that session. Record the actual times if they differ. Setting S in the organiser form uses the application's real clock and existing creation rules.
4. The controlled reference uses S = 10 December 2026 09:00, C = 9 December 2026 09:00, promotion = 9 December 08:59, and discovery in D = 9 December 09:05, all in Asia/Singapore. This gives 24 h 1 min from promotion to S and 23 h 55 min from discovery to S. The 08:59 event is on the day before the workshop. Use this as a labelled role-play if a live timed run is impractical. Record which method you used.

### Check discovery against the booking decision

Assess timing against a booking decision. Before learning when Sam cancels, write down when and how you would normally check, which preserved session you can access, and whether you would set your own reminder. State your latest useful time and why. For example, if you need the option to cancel a confirmation, that decision must occur before C. A post-C check may still establish your final allocation, with confirmed cancellation already closed. Gear or transport lead time may explain why a status check matters to you.

The C-plus-five-minute replay is a guided check of the displayed result and available actions. Separately record your first actual unprompted check, a missed check, or the check you estimate from your prewritten plan. A second person can operate Sam in the same demo session without disclosing the cancellation time. A solo exercise with a known cancellation time yields a role-play estimate of ordinary discovery. Record the evidence type and determine whether the check meets your stated booking decision time.

| Optional detailed record for C and D | Supporting detail supplied |
|---|---|
| Planned check time, access to the session and personal reminder if used | Not supplied with the final declaration |
| Promotion time, first discovery time, and whether prompted, unprompted or estimated | Not supplied with the final declaration |
| Status seen, applicable deadline, desired booking decision and latest useful time | Not supplied with the final declaration |
| Whether discovery came in time for that decision and the intended next action | Not supplied with the final declaration |
| Optional outdoor context explaining the desired lead time | Not supplied with the final declaration |

Record comprehension, discovery and available action separately. Where a participant needed to retain the option to cancel, a first check at or after C misses that decision window. The assessment does not require carrying out travel, preparation or attendance.

### VAL-03 outcomes reported by the author

The author confirmed completion of human validation and supplied the following outcome summary on 20 November 2026 (Asia/Shanghai). The summary covers the booking and waitlist tasks. The author did not supply individual run timestamps, registration IDs, a session log or a separate unprompted discovery time. The canonical times above remain controlled examples. The earlier simulated A responses remain a distinct record.

| Scenario | Author-reported validation outcome |
|---|---|
| VAL-03A | The participant can read WAITLISTED and CONFIRMED, see the C/S policy and open the participant reminder. The earlier before-and-after answers are recorded as a simulation. |
| VAL-03B | Normal FIFO promotion retains the original registration ID. The participant can find the updated state manually. |
| VAL-03C | The system supports promotion before C and presents the confirmed booking and workshop details. |
| VAL-03D | The confirmed state is available by manual check after C. Confirmed cancellation is closed and the absence of automatic notifications is disclosed. A guided check and any role-play estimate remain separate from an unprompted observation. |
| VAL-03E | Waiting withdrawal, retained history, confirmed roster stability and the S boundary behave as expected. The author did not specify a separate live at-S observation. |

## L9 acceptance and residual risk decision

The project author declared `ACCEPT_LOOP` and accepted R-08 within the fictional classroom prototype on 20 November 2026 (Asia/Shanghai). The L9 technical references are the executable preview at `fab46fa` and the scope clarification at `fc7fa3e`. The documentation commits record findings and author decisions.

> The VAL-03 assessment supports the suitability of the system within its defined Booking and Waitlist Management scope. The application provides clear registration statuses, stable booking IDs, manual refresh guidance, correct FIFO promotion and appropriate C/S controls.
>
> The system does not manage actual attendance, travel or equipment preparation. These activities are outside the approved functional scope.
>
> R-08 remains a residual risk because automatic notifications are not provided. However, the system clearly discloses this limitation and supports manual status checking.
>
> Based on the documented human validation results, the residual risk is considered acceptable within the scope of the fictional classroom prototype.

The author's decision accepts reliance on manual checks within that scope. Participants can still discover a promotion after C and have missed the cancellation window. The UI and technical evidence verify the available checking path and deadline enforcement. The declaration establishes the human suitability decision. Individual discovery times and wider user performance remain unmeasured in the submitted record.

| Gate | Outcome |
|---|---|
| L9-H01 | Author reviewed candidate ancestry, single-job CI, retained cases, policy placement and business-rule stability. |
| L9-H02 through H05 | Author declared validation complete and supplied the VAL-03A-E outcome summary above. Earlier simulated answers, guided checks and automated evidence keep their original classifications. |
| L9-H06 | Author reviewed the AI and technical evidence and recorded R-08 as `ACCEPTABLE_WITHIN_SCOPE` with delayed manual discovery as a residual risk. |
| L9-H07 | `ACCEPT_LOOP` by the project author. |
| L10, merge and release | L10 `NOT_STARTED`. V1.1 `NOT_RELEASED`. Integration and release require separate author authority. |
