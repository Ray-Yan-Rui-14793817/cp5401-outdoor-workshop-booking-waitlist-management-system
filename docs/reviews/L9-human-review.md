# L9 V1.1 integration and author review

| Item | State |
|---|---|
| Accepted L8 reference | [2531b0d](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/commit/2531b0db583564695d3665880df30fda04b102e9), which records the author's L8 ACCEPT_LOOP for a1e0d3a. |
| L9 review candidate | `codex/l9-v11-integration`. See the [candidate Actions](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions?query=branch%3Acodex%2Fl9-v11-integration) and the local L9 technical evidence for the exact tested commit. |
| L9 decision | `HUMAN_ACCEPTANCE_PENDING` |
| Risk R-08 | `PENDING_VAL_03`. The project author assesses discovery and preparation after personally performing the scenarios. |
| L10 and V1.1 release | L10 `NOT_STARTED`. V1.1 `NOT_RELEASED`. |
| Preview | [L9 local preview](http://127.0.0.1:8528/) for the existing fictional Streamlit app. |

## Integration verification

The new AppTest fixes the local test clock to the canonical Asia/Singapore schedule. A normal Streamlit cancellation at C minus one minute changes the confirmed booking and promotes the head waiter with the original ID. At C plus five minutes the same session shows the promotion and a closed confirmation cancellation. The remaining waiter may still withdraw, with the confirmed seat and the other registrations preserved. The test checks full state changes, the rendered update timestamp, and the no-notification guidance. Existing cases cover the exact C and S boundaries, D-01, owner scope, FIFO variants, and fault injection.

This is integrated technical evidence for the app's behaviour. The VAL-03 scenarios below measure whether someone understands and can act on that behaviour.

## VAL-03 author worksheet

Use fictional identities and workshop details. Record the candidate commit, session type, timezone and tester role. Use Asia/Singapore (UTC+08:00) when recording C, S and observations. In the live preview, preserve the browser session through the sequence. Switch identities through the sidebar and use **Refresh view**. Prepare a separate fresh session for the normal-promotion exercise so the waitlist starts clean. Write down what you understood and would do before consulting the technical evidence.

| Scenario | Author task | What to record |
|---|---|---|
| VAL-03A | As Leo, open the full Outdoor Photography Walk, join the waitlist and find your entry in My Bookings. Explain the meaning of the current status, the difference between C and S, and how you would learn about a promotion. | First interpretation, where you found C and S, the entry ID, and how and when you would check again. |
| VAL-03B | With Leo first and Willy second on the normal waitlist, switch to Sam and cancel before C. Switch back to Leo and use Refresh view. Identify the status and practical next step. | Time of cancellation and first check, retained registration ID, location of the current status, and what you would do next. |
| VAL-03C | Use the timed exercise below to promote Leo close to C. First observe the outcome before C in a dedicated repeat or role-play the canonical 08:59 timeline. Assess whether the remaining lead is enough to prepare and travel. | Actual or simulated promotion and discovery times, lead until S, essential preparation, travel, check-in and buffer, and your latest useful confirmation time. |
| VAL-03D | Repeat the timed setup in a new session. After Sam cancels close to C, leave Leo's view unopened until after C. Return to Leo and check manually. Contrast his confirmed booking with Willy's still-waiting entry. | Discovery lag, confirmation and action availability, where you looked for a notice, whether you would realistically check in time, and what you would do if preparation or travel were no longer feasible. |
| VAL-03E | Before S, while Willy is still waiting in D, withdraw his entry. Check his history and Alex's confirmed roster. Describe the expected action at S. | Preserved entry ID, historical status, whether the confirmed roster or allocation changed, and the at-S expectation. Label the at-S check as a policy walkthrough if you use the controlled test evidence. |

### Timed exercise for C and D

1. In the L9 preview, select Alex and create a capacity-one workshop with a unique name such as **VAL-03 Ridge Walk**. Choose C at least 10 to 15 minutes in the future and set S exactly 24 hours after it in Asia/Singapore. Allow for a date change around midnight. Make the end later than S. Add a fictional meeting point and preparation notes covering water, footwear and a check-in time. If the chosen C passes before setup is complete, start a fresh scenario with a later S.
2. In the same session, book the seat as Sam. Join the queue as Leo, then as Willy. Record the IDs and read C and S on the workshop card. Return to Sam's My Bookings.
3. Use the time shown on the card and a separate clock. Cancel at about one minute before C. For C, observe Leo's result before C and note the actual time. For D, leave Leo's view unopened until about five minutes after C. Use the sidebar and Refresh view while preserving that session. Record the actual times if they differ. Setting S in the organiser form uses the application's real clock and existing creation rules.
4. The controlled reference uses S = 10 December 2026 09:00, C = 9 December 2026 09:00, promotion = 9 December 08:59, and discovery in D = 9 December 09:05, all in Asia/Singapore. This gives 24 h 1 min from promotion to S and 23 h 55 min from discovery to S. The 08:59 event is on the day before the workshop. Use this as a labelled role-play if a live timed run is impractical. Record which method you used.

For each timed scenario, estimate how long your actual plan would take, allowing for steps that overlap and steps that must be done in order. Compare your latest useful confirmation time with discovery time. Record whether a manual refresh was realistic without an alert, whether you could meet the preparation and arrival requirements, and what you would do if you could not. Record uncertainty or missed observations explicitly.

### Author observation record

- Reviewed commit: __________
- Tester and role: __________
- Date and timezone: __________
- Environment and method (live UI or labelled role-play): __________

| Scenario | Observed actions, IDs and timestamps | Comprehension | Preparation and travel feasibility | Feedback and disposition |
|---|---|---|---|---|
| VAL-03A | Pending | Pending | Pending | Pending |
| VAL-03B | Pending | Pending | Pending | Pending |
| VAL-03C | Pending | Pending | Pending | Pending |
| VAL-03D | Pending | Pending | Pending | Pending |
| VAL-03E | Pending | Pending | Pending | Pending |

Use `ACCEPTABLE_WITHIN_SCOPE`, `CHANGES_REQUIRED` or `UNRESOLVED` with the observed reason. The author records an R-08 disposition only after reviewing the VAL-03 evidence.

## Author acceptance checklist

- [ ] **L9-H01** Confirm the exact candidate, ancestry from accepted L8, single-job CI and full inventory of all 377 retained tests plus the L9 integration case.
- [ ] **L9-H02** Personally perform VAL-03A and B. Record the initial status interpretation, how you discover a promotion and the registration ID.
- [ ] **L9-H03** Perform VAL-03C. Record C, S, the near-C promotion and preparation and travel feasibility.
- [ ] **L9-H04** Perform VAL-03D. Record when you discover promotion after C, availability of actions and your expected behaviour without alerts.
- [ ] **L9-H05** Perform VAL-03E. Check withdrawal, history and confirmed-roster stability and explain the boundary at S.
- [ ] **L9-H06** Review the AI and technical evidence, then assess R-08 from the author observations. Record the reasoning and any required changes.
- [ ] **L9-H07** Supply the exact reviewed commit and author decision. L9 acceptance, L10 authorisation, integration to main and publication have separate gates.

| Decision field | Author entry |
|---|---|
| UI and VAL-03 outcomes | Pending |
| R-08 judgement and rationale | Pending |
| L9 decision | Pending |
