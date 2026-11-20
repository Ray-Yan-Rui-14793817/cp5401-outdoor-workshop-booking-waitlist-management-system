# L9 V1.1 integration and author review

| Item | State |
|---|---|
| Accepted L8 reference | [2531b0d](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2531b0db583564695d3665880df30fda04b102e9), which records the author's L8 ACCEPT_LOOP for a1e0d3a. |
| L9 review candidate | `codex/l9-v11-integration`. See the [candidate Actions](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions?query=branch%3Acodex%2Fl9-v11-integration) and the local L9 technical evidence for the exact tested commit. |
| L9 decision | `HUMAN_ACCEPTANCE_PENDING` |
| Risk R-08 | `PENDING_VAL_03`. The project author assesses discovery and preparation after personally performing the scenarios. |
| L10 and V1.1 release | L10 `NOT_STARTED`. V1.1 `NOT_RELEASED`. |
| Preview | [L9 policy-order revision](http://127.0.0.1:8530/) for VAL-03. The running preview uses application code from `fab46fa`. The VAL-03A and risk-record follow-up changes documentation only. The 88f7dbf and earlier L9 previews remain on ports 8529 and 8528. |

## Integration verification

The new AppTest fixes the local test clock to the canonical Asia/Singapore schedule. A normal Streamlit cancellation at C minus one minute changes the confirmed booking and promotes the head waiter with the original ID. At C plus five minutes the same session shows the promotion and a closed confirmation cancellation. The remaining waiter may still withdraw, with the confirmed seat and the other registrations preserved. The test checks full state changes, the rendered update timestamp, and the no-notification guidance. The L9 test now also submits a previously enabled Cancel control at exact C with two active waiters in a separate session. The attempt returns REGISTRATION_CLOSED and preserves the entire queued state. It verifies that successful promotion and withdrawal leave the previous state objects intact. Existing cases also cover the S boundary, D-01, owner scope, FIFO variants and fault injection.

This is integrated technical evidence for the app's behaviour. The VAL-03 scenarios below measure whether someone understands and can act on that behaviour.

## Deep review findings

| Finding | Disposition |
|---|---|
| L9-F01. Exact-C coverage used a domain test with an active queue and an older stale-control UI test with an empty queue. | The L9 integration test combines a stale Cancel submission with an active queue at exact C. It keeps the existing case identity and strengthens transition checks on retained state objects. |
| L9-F02. A scheduled check at C plus five minutes demonstrated the expected page and controls, while giving the participant a prompt to discover promotion. | Retain that replay for boundary verification. The author records ordinary checking behaviour before reviewing timed instructions, then assesses discovery and a realistic preparation plan separately. Personal evidence remains pending. |
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

The UI uses the existing selected-identity scope, statuses and C/S comparison. [Test adaptations](../changes/CR-01-test-adaptations.md#l9-f05-reminder-and-booking-count-assertions) record the visible assertion changes and unchanged behavior checks. R-08 remains PENDING_VAL_03 because guidance reduces confusion but participants still have to check for themselves and assess available preparation and travel time.

### Policy placement follow-up to 88f7dbf

The public Registration policy appeared below the work area. Move the existing text immediately above the participant reminder, outside the selected-identity container. Guest and organiser views still show the public policy. Only participants see the reminder, on Workshops and My Bookings.

The existing read-only UI test now requires one policy title and paragraph in each role and requires both to precede the reminder on both participant views. It retains organiser tabs, owned roster choices, both saved drafts and whole-state assertions. The five time cases and retained booking-count and permission assertions still verify the same outcomes. For the revision's exact CI and browser evidence, see the candidate Actions and the local policy review report.

### Author review follow-up

The author noted that the public policy is always visible and the reminder starts collapsed. The VAL-03A worksheet now captures the same comprehension questions in both states. The author also identified stale descriptions of the current demo identities and Demo Guide in the [risk record](../changes/CR-01-impact-and-risks.md#l9-documentation-follow-up). This is a low-risk documentation finding. The High CR-01 review classification and the R-08 decision gate remain in place.

## Assessment 3 and lecture cross-check

| Criterion and source | Evidence and remaining gate |
|---|---|
| Requirements, risk and traceability, Assessment 3 pp. 3-5 and 10 | [CR-01](../changes/CR-01.md) AC-02 to AC-05 and AC-07 link to FR-09 to FR-11, BR-06/09/10/11/13/15/16, QR-02/03 and R-08. Follow the [test map](../test-plan.md#l9-v11-integration-verification) and the L9 finding dispositions. |
| Verification, validation and failure coverage, pp. 10-11 | The two independently prepared UI states check a valid cancellation before C and a stale submit exactly at C. D-01 checks prove owner/status precedence at C plus five minutes. Retained cases cover S, time-zone comparison, separate scope and failed promotion atomicity. The oracle uses the approved outcomes, exact IDs and expected snapshot changes. The author still needs to demonstrate suitability through VAL-03. |
| Controlled change and CI, pp. 4-5 and 12 | The separate branch descends from accepted L8. All 377 L8 cases remain. The exact-candidate single-job evidence and L9 finding dispositions support traceability. The completed-assessment chain also requires a PR with the Actions result, a justified author merge decision, approved integration and a deployed V1.1 release. Those stages remain pending. |
| Deployment and defence, pp. 8, 10 and 13 | Published V1.0 and the local candidate have separate evidence. The author should explain why time-of-promotion is different from time-of-discovery and why owner checks precede status. The AI record and review intake identify the scoped changes, assumptions, checks and author decision points. |
| 16 November lectures, 10:45 transcript pp. 2 and 8-10, 10:46 transcript pp. 3-7 | Keep the three-file app structure, a bounded change, named checks and an audit trail. Week 7 slides 24-25 inform object-scope checks, Week 8 slides 14-16 inform focused review and gates, and Week 9 slides 10 and 12 inform escalation and author ownership. |

## VAL-03 author worksheet

Use fictional identities and workshop details. Record the candidate commit, session type, timezone and tester role. Use Asia/Singapore (UTC+08:00) when recording C, S and observations. Use the revised Booking & Waitlist Reminder preview on port 8530 for VAL-03A-E. Preserve the browser session through each live sequence. Switch identities through the sidebar and use **Refresh view**. Prepare a separate fresh session for the normal-promotion exercise so the waitlist starts clean. Write down what you understood and would do before consulting the technical evidence. Before reading the scenario rows or timed instructions, prewrite when and where you would normally check without any app alert, including your reason and any user-set reminder. Use that plan in the practical assessment below.

| Scenario | Author task | What to record |
|---|---|---|
| VAL-03A | In a fresh session, join the full Outdoor Photography Walk as Leo and find your entry in My Bookings. Use the two-pass worksheet below. | Record the same answers before and after opening the reminder. Capture the registration ID once, and record cues, corrections and remaining uncertainty for each pass. |
| VAL-03B | In a fresh session, join the full Outdoor Photography Walk as Leo, then join it as Willy. Verify both positions before switching to Sam and cancelling before C. Switch back to Leo and use Refresh view. Identify the status and practical next step. | Time of cancellation and first check, retained registration ID, location of the current status, and what you would do next. |
| VAL-03C | Use the timed exercise below to promote Leo close to C. First observe the outcome before C in a dedicated repeat or role-play the canonical 08:59 timeline. Assess whether the remaining lead is enough to prepare and travel. | Actual or simulated promotion and discovery times, lead until S, essential preparation, travel, check-in and buffer, and your latest useful confirmation time. |
| VAL-03D | Repeat the timed setup in a new session. After Sam cancels close to C, leave Leo's view unopened until after C. Return to Leo and check manually. Contrast his confirmed booking with Willy's still-waiting entry. | Discovery lag, confirmation and action availability, where you looked for a notice, whether you would realistically check in time, and what you would do if preparation or travel were no longer feasible. |
| VAL-03E | Before S, record Alex's confirmed roster from D. Switch to still-waiting Willy, withdraw, then compare Alex's roster and Willy's history. For the at-S check, use a separate still-active WAITLISTED entry or a clearly labelled policy walkthrough. | Preserved entry ID, historical status, and the before and after roster. At S, distinguish the closed active entry from Willy's already cancelled record, which follows the repeat rule. Label a walkthrough separately from a live observation. |

### VAL-03A comprehension with the reminder closed and open

Use a fresh browser session so the reminder is collapsed by default. Keep it closed while you record the first pass. Read the normal interface as you would during ordinary use. The public Registration policy may be one of the cues you notice. Keep the first answers as written. Open the reminder, read it and answer the same questions again before consulting the technical evidence.

For each pass, explain in your own words what your current status means for attending, which actions close at C and at S, whether you expect an automatic notification, and where, how and when you would check for a promotion.

| Pass | Answers and cues | Comprehension finding |
|---|---|---|
| Reminder still collapsed | Pending. Record your answers, where you looked and the cues you actually used. | Pending. Record any unclear or incorrect point. |
| After reading the reminder | Pending. Answer the same questions again and record what the reminder clarified, confirmed or left unresolved. | Pending. Assess these answers separately and compare with the first pass. |

If both passes are correct, record that the default view supported understanding in this exercise and note what the reminder added. If understanding improves only after opening it, record which information depended on discoverability. Keep any remaining confusion visible. This evidence addresses comprehension. The later scenarios cover discovery and real preparation feasibility.

#### Author-submitted VAL-03A responses

Source: The project author submitted both passes in Chinese on 20 November 2026 (Asia/Shanghai). The answers below are English translations of the author's responses. They refer to the `21d523f` worksheet. The exact observed build, live or role-play method, registration ID, exercise timestamps and specific on-screen cues were not supplied.

| Question | Pass 1: Reminder still collapsed | Pass 2: After reading the reminder |
|---|---|---|
| Q1. Does WAITLISTED mean I have a reserved place? | No. WAITLISTED means I am still on the waiting list. I do not currently have a confirmed place. | No. WAITLISTED only means I am in the queue. Only a change to CONFIRMED means I have a reserved place. |
| Q2. Which operations close at registration cutoff (C)? | I understand that new bookings and cancellation of confirmed bookings close at C. I am unsure whether all waitlist operations close then as well. | At C, new bookings, joining the waitlist, confirmed booking cancellation and automatic FIFO promotion close. C is 24 hours before the workshop starts. |
| Q3. If I am still WAITLISTED at C, what can I do before S? | I should still be able to see my waiting status. If I no longer want to wait, I may be able to leave the waitlist before the workshop starts. | I can withdraw my waitlist entry before S and see the retained record in Booking History. Waiting withdrawal closes at S. |
| Q4. Will the system notify me automatically if I am promoted? | I am unsure whether the system will notify me automatically. I may need to open it and check the status myself. | No. The system sends no automatic notifications. I have to check My Bookings myself to discover whether WAITLISTED has become CONFIRMED. |
| Q5. Where, how and when should I check for a change? | I would check my booking status in My Bookings and check again before the workshop starts. I am unsure how often I should refresh. | I would open My Bookings and click Refresh view. I would check regularly before C, again near C, and after C to confirm the final allocation status. I could also set my own phone reminder to avoid missing the promotion. |

**Technical comparison of the author responses.** The first pass correctly identifies an unconfirmed waitlist place, the two confirmed booking operations that close at C, and My Bookings as the place to look. It leaves the Join and promotion cutoff, the withdrawal deadline, automatic notifications and how often to refresh unresolved. The second pass addresses all five questions consistently with the candidate. The only direct evidence is the author's reported comprehension and intended checking plan. Whether a real check happened on time and whether the resulting lead time was enough for preparations and travel remain separate VAL-03C/D questions.

### Timed exercise for C and D

1. In the L9 preview, select Alex and create a capacity-one workshop with a unique name such as **VAL-03 Ridge Walk**. Choose C at least 10 to 15 minutes in the future and set S exactly 24 hours after it in Asia/Singapore. Allow for a date change around midnight. Make the end later than S. Add a fictional meeting point and preparation notes covering water, footwear and a check-in time. If the chosen C passes before setup is complete, start a fresh scenario with a later S.
2. In the same session, book the seat as Sam. Join the queue as Leo, then as Willy. Record the IDs and read C and S on the workshop card. Return to Sam's My Bookings.
3. Use the time shown on the card and a separate clock. Cancel at about one minute before C. For C, observe Leo's result before C and note the actual time. For D, leave Leo's view unopened until about five minutes after C. Use the sidebar and Refresh view while preserving that session. Record the actual times if they differ. Setting S in the organiser form uses the application's real clock and existing creation rules.
4. The controlled reference uses S = 10 December 2026 09:00, C = 9 December 2026 09:00, promotion = 9 December 08:59, and discovery in D = 9 December 09:05, all in Asia/Singapore. This gives 24 h 1 min from promotion to S and 23 h 55 min from discovery to S. The 08:59 event is on the day before the workshop. Use this as a labelled role-play if a live timed run is impractical. Record which method you used.

### Check discovery and preparation separately

Before the timed setup, write down when you would next look at the waitlist in ordinary use and why. Record whether you would set your own reminder, which device or preserved session you would check, and any period when you could not access it. Base the plan on your normal commitments. Record it before reading the reference timestamps or learning when Sam cancels.

Use the C-plus-five-minute check as a **guided boundary replay**. Record it as prompted. For the practical assessment, use the prewritten checking plan and record the first check you actually made, the later check you would make under the plan, or a missed check. A second person may operate Sam in the same fictional session without telling the participant when the change occurs, while you personally do the participant check. For a solo run with a known promotion time, label the practical estimate as a role-play. Record whether the time was observed, prompted or estimated and how the person learned of the confirmation.

Build a short worked plan for the outdoor workshop. Use credible times for obtaining gear, reading safety information, reaching the meeting point, and arriving by check-in. Include fixed constraints such as opening hours, transport departures and prior commitments. Record the latest time you could discover confirmation and still complete that plan. Compare that deadline with your first check or planned check. If a check would be missed or late, record which step becomes infeasible and what action you would take with confirmed cancellation already closed.

| Evidence for C and D | Author entry |
|---|---|
| Planned check time or frequency, reason, user-set reminder and session access | Pending |
| Promotion time, first observed or estimated discovery time, and prompt source | Pending |
| Gear, safety, travel and check-in steps, durations and fixed deadlines | Pending |
| Latest useful discovery time, comparison with the first check, and intended action | Pending |
| Confidence and limitations of the evidence | Pending |

Mark discovery and preparation outcomes separately. A guided replay establishes how to check and what the controls do at that time. Use the practical observations and a grounded plan to judge feasibility within the intended scope. Choose `UNRESOLVED` if discovery or feasibility remains unsubstantiated.

### Author observation record

- Reviewed commit: __________
- Tester and role: __________
- Date and timezone: __________
- Environment and method (live UI or labelled role-play): __________

| Scenario | Observed actions, IDs and timestamps | Comprehension | Preparation and travel feasibility | Feedback and disposition |
|---|---|---|---|---|
| VAL-03A | [Two sets of author answers received](#author-submitted-val-03a-responses). Build, method, record ID and exercise timestamps remain unreported. | Partial with the reminder closed. All five answers align with the policy after reading it. | Assess discovery and preparation feasibility in VAL-03C and D. | Comprehension evidence recorded. The author's final disposition remains pending. |
| VAL-03B | Pending | Pending | Pending | Pending |
| VAL-03C | Pending | Pending | Pending | Pending |
| VAL-03D | Pending | Pending | Pending | Pending |
| VAL-03E | Pending | Pending | Pending | Pending |

Use `ACCEPTABLE_WITHIN_SCOPE`, `CHANGES_REQUIRED` or `UNRESOLVED` with the observed reason. The author records an R-08 disposition only after reviewing the VAL-03 evidence.

## Author acceptance checklist

- [ ] **L9-H01** Confirm the exact candidate, ancestry from accepted L8, single-job CI and the 378 retained case identities plus the five reminder boundary cases. Verify that the public policy appears before the reminder on both participant views and that guest and organiser views show the policy without the reminder.
- [ ] **L9-H02** Personally perform VAL-03A and B. Record the same answers with the reminder closed and after reading it, the cues and any change in understanding, how you discover a promotion and the registration ID.
- [ ] **L9-H03** Perform VAL-03C. Record C, S, the near-C promotion and preparation and travel feasibility.
- [ ] **L9-H04** Perform VAL-03D. Record the guided post-C result separately from your prewritten checking plan. Compare observed or estimated discovery against the latest useful time and record preparation feasibility without an alert.
- [ ] **L9-H05** Perform VAL-03E. Check withdrawal, history and confirmed-roster stability and explain the boundary at S.
- [ ] **L9-H06** Review the AI and technical evidence, then assess R-08 from the author observations. Record the reasoning, evidence limitations and any required changes.
- [ ] **L9-H07** Supply the exact reviewed commit and author decision. L9 acceptance, L10 authorisation, integration to main and publication have separate gates.

| Decision field | Author entry |
|---|---|
| UI and VAL-03 outcomes | Pending |
| R-08 judgement and rationale | Pending |
| L9 decision | Pending |
| Later PR decision and authority | Pending separate author review. |
