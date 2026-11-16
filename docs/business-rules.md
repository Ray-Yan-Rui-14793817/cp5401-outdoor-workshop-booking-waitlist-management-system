# Business Rules

L0 revision 3. [Requirements](../requirements.md) | [Tests](test-plan.md) | [Sources](sources.md)

## Time and operation matrix

S is an aware workshop start; C = S - 24 elapsed hours; t is trusted server decision time. The duration is not midnight on the previous calendar day.

Creation requires S-t>24h. At C, freeze confirmed additions/cancellation and close waitlist joining/promotion. Owner waiting withdrawal remains available until S. At S all effective registration mutations close.

| Operation | t < C | C <= t < S | t >= S |
|---|---|---|---|
| Create proposed workshop | Allow if valid | Reject | Reject |
| Book | Apply rules | Reject | Reject |
| Cancel CONFIRMED | Owner may cancel | Reject | Reject |
| Join waitlist | Apply V1.1 rules | Reject | Reject |
| Withdraw WAITLISTED | Owner may withdraw | Owner may withdraw | Reject effective withdrawal |
| Promote | With effective cancellation | Prohibited | Prohibited |
| Read / repeat owned CANCELLED | Role/ownership rules | Same | Same |

One universal read-only flag must not block final-24h withdrawal. Use operation-specific conditions. Check time when the submitted action is processed, not when the page was rendered. Cancellation and its promotion use one decision time and return together.

## Rules

| ID | Rule |
|---|---|
| **BR-01** | Selected actors must exist with their fixed role. Enforce operation role and ownership in booking.py, not only through buttons. These checks do not authenticate a person. |
| **BR-02** | Trimmed title/location are non-empty. Capacity is an integer 1-30; reject booleans, fractions, missing and out-of-range values. |
| **BR-03** | Use complete timezone-aware instants with end>S. Obtain fresh trusted server time for each action; do not use caller-controlled dates as current time. Tests may inject a clock, unavailable as a deployed user control. |
| **BR-04** | Confirmed count is at most capacity; remaining = capacity-confirmed. WAITLISTED/CANCELLED records consume no confirmed place. |
| **BR-05** | At most one active registration per participant/workshop: CONFIRMED in V1.0; CONFIRMED or WAITLISTED in V1.1. IDs, not display names, identify users. |
| **BR-06** | Cancel by registration ID with selected-actor ownership checks. Repeating an owned CANCELLED record returns ALREADY_CANCELLED without any mutation/allocation, including after C/S. |
| **BR-07** | Rebooking before C creates a new ID and retains history. Unknown or unauthorised targets cause no mutation. |
| **BR-08** | Join is explicit, full-only, before C and without an active duplicate. Spare capacity returns USE_BOOKING without registering. |
| **BR-09** | Use unique increasing workshop queue_seq for strict FIFO among current WAITLISTED records. Allocate new sequences only for successful joins. Only pre-C cancellation can promote. |
| **BR-10** | One effective confirmed cancellation promotes at most the earliest waiter by changing that same registration to CONFIRMED. Confirmed count stays unchanged with a waiter, otherwise decreases by one. |
| **BR-11** | Owner WAITLISTED withdrawal is allowed while t<S, including C<=t<S. Change no confirmed records/counts and trigger no promotion. Preserve others' relative order; rejoin only before C with a new ID/tail sequence. |
| **BR-12** | Before C a direct booking cannot bypass an active queue. Unexpected spare capacity alongside a queue blocks mutation as INTEGRITY_ERROR. At/after C allocate no new place, including after withdrawal. |
| **BR-13** | Validate and construct complete new state before UI replacement. Success does not mutate the input snapshot; rejection, no-op or exception preserves all input records/counters. Serial same-session processing is assumed, not concurrent storage transactions. |
| **BR-14** | No created-detail/capacity editing, account management, cross-workshop overlap restriction or confirmed-cutoff override. Use fictional session data without authentication/durability claims. |
| **BR-15** | Creation requires S-t>24h. Reject exactly 24h or less with no workshop or ID-counter advance. |
| **BR-16** | At t>=C stop Book, effective CONFIRMED cancellation, Join and Promotion. Permit owner WAITLISTED withdrawal only while t<S. At t>=S stop all effective registration mutations; retain reads/no-op repeats. |

### Queue sequence and displayed position

queue_seq is stable historical ordering, not the displayed position. A waiting entry's current position is one plus the number of current WAITLISTED entries in the same workshop with smaller queue_seq.

Sequence gaps are not display gaps. With active sequences 3 and 8, positions are 1 and 2. Withdrawal can reduce positions during the final 24 hours without changing the confirmed roster or enabling promotion. After S, label any displayed queue as historical and closed.

### Observable results

Return an outcome that identifies success or the specific reason for refusal. Tests assert this outcome and state invariants independently of presentation wording. The exact Python return type remains a small L1 implementation choice.

| Outcome | Meaning |
|---|---|
| OK | The requested valid operation produced its complete result. |
| INVALID_ACTOR | Unknown actor or a role inconsistent with the predefined identity. |
| FORBIDDEN | A valid selected actor lacks the operation role or record ownership. |
| INVALID_INPUT | Invalid creation fields, types or insufficient creation lead time. |
| UNKNOWN_WORKSHOP / UNKNOWN_REGISTRATION | A well-formed target ID is not present. |
| REGISTRATION_CLOSED | Effective Book, confirmed cancellation or Join is attempted at/after C. |
| WORKSHOP_STARTED | Effective waiting withdrawal is attempted at/after S. |
| DUPLICATE_ACTIVE | The selected participant already holds an active record for that workshop. |
| FULL | A direct Book request has no confirmed capacity. |
| USE_BOOKING | A Join request has spare capacity and creates no record. |
| ALREADY_CANCELLED | An owned cancelled record is unchanged; this is a no-op, not late effective cancellation. |
| INTEGRITY_ERROR | An inconsistent open spare-place/queue state prevents bypass. |

For registration operations, first resolve a valid actor and operation role, then target and ownership. Recognise an owned CANCELLED repeat before rejecting active mutations on time. For new Book/Join, check the applicable time window, then duplicate-active status before full/available conditions. Creation validates input types before time arithmetic.

Negative tests must still isolate their intended cause rather than relying on this order to hide other failures.

## Boundary examples

S = 2026-12-10 09:00 Asia/Singapore; C = 2026-12-09 09:00. Freeze the test clock for these examples.

| Time / target | Expected result | Planned checks |
|---|---|---|
| Creation at C-1 second | Valid creation may succeed; lead is greater than 24h. | B03 |
| Creation at C or later | INVALID_INPUT; no workshop/counter change. | B05 |
| Valid active Book/cancellation at C-1 second | Apply ordinary rules. | B15 |
| Active Book/cancellation at C or later | REGISTRATION_CLOSED; unchanged state. | B15/I10 |
| Owned active waiter at C or S-1 second | Withdrawal succeeds; confirmed roster unchanged. | W08/W12/I10 |
| Fresh owned active waiter at S or later | WORKSHOP_STARTED; unchanged state. | W12/I10 |
| Owned CANCELLED record after S | ALREADY_CANCELLED; unchanged state. | B16/W16 |

Use a fresh valid active fixture for each boundary parameter. Do not withdraw at C and then reuse that CANCELLED record to claim that a later no-op proves start-time rejection.

## State transitions

| Event | Transition | Condition |
|---|---|---|
| Book | none -> CONFIRMED | Valid participant, capacity, no active duplicate, t<C |
| Cancel confirmed | CONFIRMED -> CANCELLED | Owner and t<C; V1.1 may promote |
| Join | none -> WAITLISTED | Full, no active duplicate, t<C |
| Withdraw | WAITLISTED -> CANCELLED | Owner and t<S, including after C |
| Promote | WAITLISTED -> CONFIRMED | Earliest waiter within effective pre-C cancellation |
| Repeat | CANCELLED -> CANCELLED | Owner, no change |
| Time phase | Derived display | Preserve history; the final-24h queue may shrink |

Selection is not identity security. Early allocation without notification does not guarantee early awareness. Validate these scope/timing limits through R-08 rather than silently adding real authentication, shared storage or overrides.
