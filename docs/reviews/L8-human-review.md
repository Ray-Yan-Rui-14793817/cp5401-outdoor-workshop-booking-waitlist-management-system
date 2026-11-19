# L8 CR-01 candidate human review

Status: **HUMAN_ACCEPTANCE_PENDING**. Human decision: **PENDING**. R-08: **PENDING_VAL_03**. V1.1 release: **NOT_RELEASED**.

The candidate starts from published V1.0 commit `36e7bff3c1d3f74bb29c1900373726ecffdd176b`. The author's [L7 decision](L7-human-review.md#human-decision-record) approved D-01 and High review depth. The [change contract](../changes/CR-01.md) governs the candidate. The existing V1.0 deployment remains on its released baseline.

## Technical evidence

The [test map](../test-plan.md#l8-cr-01-verification) maps the candidate's 31 new cases and 317 exact retained JUnit identities. The local run under Python 3.12.14 and PyArrow 24.0.0 passed all 348 cases and reported 98% combined line and branch coverage for `booking.py`. The [candidate branch Actions](https://github.com/Ray-Yan-Rui-14793817/cp5401-outdoor-workshop-booking-waitlist-management-system/actions?query=branch%3Acodex%2Fcr-01-waitlist) expose the tested SHA, job and downloadable reports. Review the tested commit, all quality steps and result before accepting. The tests exercise serial in-session behaviour and simulated trusted clocks. Human acceptance and VAL-03 need separate author evidence.

## Author checklist

- [ ] **L8-H01 - Check the baseline and delivery.** Confirm the candidate branches from published M and only CR-01 code, tests and records changed. Check the single-job Actions report against the candidate SHA and verify the 317 retained case identities plus new results.
- [ ] **L8-H02 - Check explicit Join and ownership.** In a fresh local demo session, select Xingjian and open Outdoor Photography Walk, which starts full. Book should report FULL. Join should create a WAITLISTED record. Verify position 1, the original confirmed count and the absence of another participant's private entries in My Bookings.
- [ ] **L8-H03 - Check withdrawal and history.** Withdraw Xingjian's waiting record and verify retained CANCELLED history and unchanged roster. Rejoin before cutoff and verify the new ID. Review the Leo/Willy test evidence for FIFO, sequence gaps and multi-waiter ordering.
- [ ] **L8-H04 - Check promotion.** With Xingjian queued, switch to Sam in the same session and cancel Sam's confirmed Outdoor Photography Walk booking. Return to Xingjian and use Refresh view. Verify the same queued ID is CONFIRMED. Check Alex's owned roster and queue, and check Rui Yan's workshop selector for owner scope.
- [ ] **L8-H05 - Review C/S and D-01.** Inspect the independent boundary and stale-action tests for C and S. Confirm a stale Withdraw targeting a promoted row reports STATUS_CHANGED, preserves the confirmation and follows actor/owner checks. Check the fault-injection assertions for no partial state.
- [ ] **L8-H06 - Review AI use, risk and disclosure.** Check the [AI record](../ai-use.md#l8-cr-01-ai-use), ensure extra participants appear only in fixtures and review the temporary session and no-notification copy. Keep R-08 pending human VAL-03 awareness and feasibility evidence.
- [ ] **L8-H07 - Record the decision.** Record the exact reviewed SHA, observations, issues and ACCEPT_LOOP or CHANGES_REQUIRED. Subsequent integration and release decisions are separate. All actual merges and deployment fast-forwards are author-only.

## Author decision record

| Field | Value |
|---|---|
| Reviewer, date and time zone | Pending |
| Reviewed SHA and environment | Pending |
| Checks and observations | Pending |
| Findings and follow-up | Pending |
| Decision | Pending |
