# Test and Validation Plan

L0 revision 3. All scenarios are PLANNED / NOT_EXECUTED. IDs represent scenarios and parameter groups, not passing-test counts.

[Rules](business-rules.md) | [Risks](risks.md) | [Traceability](traceability.md) | [Loop evidence format](development-workflow.md#record-for-each-loop)

## Test design and independent oracles

pytest calls actual booking.py functions without importing Streamlit UI execution. Serially feed each successful returned state into the next action. Independent copies are not a shared-concurrency test.

For every negative or boundary parameter:

1. Use a fresh fixture with valid actor, role, target, ownership and time unless that is the condition under test.
2. Isolate the intended rejection. B12 must use a valid non-owner, active target and open workshop; B09 must leave spare capacity when proving duplication; B15 must leave capacity and avoid duplicates.
3. Use a fresh active WAITLISTED record at each W12/I10 time. A previously withdrawn CANCELLED record proves no-op safety, not start-time rejection.
4. Derive expected outcome and state from FR/BR before comparing implementation. Assert reason plus records, IDs, counters, counts and absence of side effects.
5. For failures, compare the entire original state with its snapshot. For successful mutations also confirm the original snapshot was not changed.
6. Record missing cases, skips and mock limitations. An injected helper failure proves only the selected failure path; it does not prove all exceptional behaviour.

Use a controlled aware clock; do not sleep through actual deadlines. app.py must obtain trusted time when processing submission rather than reusing render-time state. Test UI wiring separately.

Lecture examples of automatic full-session waitlisting or overlap rejection are not this project's oracle. Apply the declared FULL/separate-Join contract and per-workshop scope instead.

## Baseline scenarios

Implement B01-B17 in V1.0 and retain them in V1.1. Preserve no-waiter fixture preconditions rather than changing old assertions to waitlist outcomes.

| ID | Scenario and expected result |
|---|---|
| **B01** | Valid fictional selection resolves fixed ID/role. Switching/clearing selection preserves business state in the same session. |
| **B02** | Unknown ID or inconsistent role produces INVALID_ACTOR without restricted action or state change; this is not credential authentication. |
| **B03** | Valid capacity 1/30 and lead 24h+1 second create correct ID/owner. Use separate valid fixtures for each boundary. |
| **B04** | Reject zero, negative, 31, fraction, True and missing capacity as INVALID_INPUT; no record/counter advance. |
| **B05** | Independently reject blank fields, end<=S, past start and S-t<=24h, including exactly 24h. Input remains unchanged. |
| **B06** | Display correct S/C, zone, location and CONFIRMED-only counts. Spare capacity does not permit booking at/after C. |
| **B07** | Normal and last-place booking before C yield one CONFIRMED ID and correct counts. Original input remains unchanged. |
| **B08** | New eligible actor books an open but full workshop: FULL, no new record and no automatic waiting in either release. |
| **B09** | With spare capacity, an active same-user/workshop duplicate yields DUPLICATE_ACTIVE and preserves the original ID. A distinct workshop remains independent without overlap rejection. |
| **B10** | Own-record functions filter by selected ID. Any targeted non-owner read is denied; changing the demo selector is not prevented or called authentication. |
| **B11** | Own confirmed cancellation before C without waiters retains CANCELLED history and releases exactly one place. |
| **B12** | Valid selected A cancels B's active ID in an otherwise valid open scenario: FORBIDDEN; original records/counts unchanged. |
| **B13** | Valid participants cannot create/read organiser rosters; a valid non-owner organiser cannot read another roster. Isolate these role/owner failures from timing errors. |
| **B14** | Well-formed unknown workshop/registration targets return the corresponding UNKNOWN outcome without mutation or false success. |
| **B15** | Use fresh otherwise-valid fixtures at C-1, C and C+1 second. Book/confirmed cancellation work before C and return REGISTRATION_CLOSED at/after C, including stale forms. |
| **B16** | Repeat owned CANCELLED IDs before/after C and S: ALREADY_CANCELLED, no additional release, ID advance or promotion. |
| **B17** | Before C, rebooking uses a new ID with old history retained; after C reject with no record/counter changes. |

## Waitlist scenarios

W01-W16 apply only to V1.1. Allocation uses C; withdrawal uses S.

| ID | Scenario and expected result |
|---|---|
| **W01** | Explicit pre-C full joining creates one WAITLISTED ID/sequence without consuming confirmed capacity. |
| **W02** | An otherwise-valid Join with spare capacity returns USE_BOOKING without registration. |
| **W03** | A confirmed actor joining the same queue returns DUPLICATE_ACTIVE, with no second active record. |
| **W04** | Repeated Join by a waiter returns DUPLICATE_ACTIVE; preserve original ID/sequence and the next-sequence counter. |
| **W05** | Equal displayed timestamps still produce distinct sequence FIFO, independent of names/browser times. |
| **W06** | Participant A is confirmed; B then D are waiting. Cancel A before the cutoff: only B confirms, D becomes position 1 and confirmed count is unchanged. |
| **W07** | Pre-C confirmed cancellation without waiters releases one place and promotes nobody. |
| **W08** | In independent pre-C and final-24h cases, head/tail withdrawal preserves every confirmed ID/state/count and others' relative order. A later pre-C cancellation excludes the withdrawn head; a post-C withdrawal promotes nobody. |
| **W09** | Pre-C withdrawal/rejoin creates a new ID/tail sequence and retains history. During C<=t<S allow withdrawal but reject rejoining. |
| **W10** | Repeat cancellation that already promoted a waiter: ALREADY_CANCELLED with no second promotion. |
| **W11** | Two workshop queues remain isolated when one is changed. |
| **W12** | Fresh active fixtures at C-1/C/C+1 and S-1/S/S+1. Reject allocation/confirmed cancellation/Join at C, allow owner waiting withdrawal until S, then reject active withdrawal as WORKSHOP_STARTED. No-op cases are separate. |
| **W13** | In-app refresh shows own outcome and contiguous positions, including non-contiguous active sequences such as 3/8. Withdrawal during final 24h updates remaining positions; joining/promotion stay closed. After S show history. |
| **W14** | Only the selected owner organiser reads ordered rosters. After C the queue may shrink but confirmed records remain identical. |
| **W15** | An intentionally inconsistent open spare-place/queue fixture returns INTEGRITY_ERROR without direct bypass or state changes. |
| **W16** | Repeat an owned cancelled waiting record, including after S: ALREADY_CANCELLED without changes. Equal display names with distinct IDs remain independent. |

## In-memory integration and system scenarios

| ID | Version and method | Planned acceptance |
|---|---|---|
| **I01** | Both; automated serial actions | Feed A's successful last-place result into B. Exactly one confirms and B is FULL; do not call independent state copies a concurrent race. |
| **I02** | Both; automated serial actions | Repeated actor requests produce one active registration/counter allocation. |
| **I03** | V1.1; automated serial actions | Check Join-then-Cancel and Cancel-then-Join ordering. Existing waiters have priority and new arrivals cannot bypass. |
| **I04** | V1.1; automated repeats | One confirmed ID cancelled repeatedly causes one effective cancellation/promotion, including a later post-C no-op. |
| **I05** | Both; automated snapshot/failure | Success returns a complete candidate without changing input. Rejection or injected promotion-helper failure leaves all original records and counters unchanged; UI retains its prior state on failure. |
| **I06** | Both; manual UI plus rule checks | Ordinary reruns, in-app Refresh and fictional actor changes preserve one session; do not reseed on selector changes. Distinguish browser reload. |
| **I07** | V1.1; automated baseline fixtures | Representative V1.0 CONFIRMED/CANCELLED fixtures retain IDs, owners, history and time contracts under V1.1 defaults. This is not live migration. |
| **I08** | Both; separate automated/manual parts | Check selected-role/owner wiring, safe failure and no false success. UI clearly labels demo identities, temporary/unshared data and in-app versus browser refresh. |
| **I09** | Both; automated factory isolation plus manual lifecycle | Independent initialisations share no mutable collections; changing A through operations does not affect B. Ordinary reruns preserve data while new sessions/browser reload/restart follow reset limits. No backup/recovery claim. |
| **I10** | Both; automated clock scenarios plus manual UI wiring | A form rendered before C submits at/after C with fresh trusted time: reject Book/confirmed cancellation/Join/promotion. In a fresh active waiting fixture, withdrawal at C<=t<S succeeds. A separate fresh pre-S form submitted at/after S returns WORKSHOP_STARTED. |

I09/I10 were re-scoped during unaccepted L0 revision 2. There are no previous executed application results to relabel. Once a working baseline exists, preserve its genuine history.

## Verification and validation

Verification compares a work product or behaviour with its specification. Examples are this requirements review and later boundary/state tests.

Validation examines whether the intended users can complete useful tasks and accept the declared policy/limits. Passing pytest cannot close R-08.

| ID | User task and evidence |
|---|---|
| **VAL-01** | Find a suitable workshop, identify S/C and complete pre-C booking/cancellation. Explain post-C restrictions and the single-session, non-authenticated demonstration. |
| **VAL-02** | Create a >24h workshop and inspect owned rosters. Assess whether the 24h freeze supports preparation and whether the prototype demonstrates the organising task coherently. |
| **VAL-03** | Complete waiting, withdrawal and promotion; explain C/S differences and assess preparation, awareness and participation feasibility. |

| Scenario | Task and acceptance question |
|---|---|
| **VAL-03A** | After Join, explain that WAITLISTED is unconfirmed and identify C, refresh requirements and lack of notifications. |
| **VAL-03B** | Locate confirmation after ordinary pre-C promotion and explain the next action. |
| **VAL-03C** | S=10 December 09:00, C=9 December 09:00, promotion=9 December 08:59. Separately assess comprehension, preparation/arrival feasibility and latest useful confirmation with reasons. |
| **VAL-03D** | In one preserved demo session simulate pre-C promotion discovered after C. Explain closed confirmed cancellation versus permitted waiting withdrawal. A recreated session follows reset limits, not recovered prior data. |
| **VAL-03E** | Withdraw during C<=t<S without changing confirmed records or promoting another waiter; explain closure at S and assess whether this is understandable/useful. |

### Validation recording and decisions

Record actual tester/role label, version, task, intended need, observations, feedback, issue, owner and decision. Distinguish external testers from author role-play; do not invent participants or claim real multi-user operation.

Task comprehension is acceptable when the tester correctly identifies state, applicable deadline and next permitted action without unresolved critical confusion. Product suitability is a separate human judgement supported by feedback and preparation/arrival constraints.

Use ACCEPTABLE_WITHIN_SCOPE, CHANGES_REQUIRED or UNRESOLVED, with rationale. A critical unmet need prevents the relevant release. R-08 remains pending until these activities actually occur.

The old same-day 08:59 promotion for a 09:00 start is prohibited under W12/I10. Promotion shortly before C is the valid scenario. Allocation time does not guarantee awareness time.
