# Project Requirements Business Rules and Risks

L0 revision 3. Human design decision: ACCEPT_LOOP, 16 November 2026. L1 accepted on 17 November 2026 (Asia/Singapore). L2 identity and permission foundations accepted with ACCEPT_LOOP on 17 November 2026 (Asia/Singapore); the author declared UI/H01-H07 complete. L3: NOT_STARTED. Requirement acceptance targets remain unchanged; L2 implements only the stated subset below. [L2 review](docs/reviews/L2-human-review.md) | [Rules](#business-rules) | [Tests](docs/test-plan.md) | [Sources](docs/demo-reuse.md#references)

## L2 implementation scope

The author's L2 instruction fixes the demonstration identities below. Stable IDs and their roles are retained from L1; display names are updated. No account editor or real login is introduced.

| Fixed ID | Demo name | Role |
|---|---|---|
| organiser-1 | Rui Yan | ORGANISER |
| organiser-2 | Alex | ORGANISER |
| participant-1 | Xingjian | PARTICIPANT |
| participant-2 | Sam | PARTICIPANT |

resolve_actor maps a selected ID to the canonical session DemoUser, or None. check_permission returns INVALID_ACTOR for an absent/unknown actor or inconsistent role claim; FORBIDDEN for a valid actor with the wrong operation role or optional owner; otherwise OK. Both functions leave all input state unchanged. The UI displays an allowed restricted preview only for explicit OK; an absent or unrecognised permission result denies the view without changing business state. Names are display labels, not permission keys.

The role requested by an operation is an application constant, not a user role editor. Future operations must obtain owner_id from the actual looked-up target record; the helper alone does not establish target existence or implement cancellation/roster access. B01/B02 receive L2 identity/preview checks. B10/B12/B13 and complete QR-03 business enforcement remain later work. Switching or clearing the selector never reseeds business state. Selection is freely switchable and does not authenticate a real person.

## Problem and purpose

Outdoor workshops have limited places. Duplicate registrations, incorrect cancellation and unclear timing can undermine allocation. Full sessions need a fair queue and a way to reallocate places released before the booking cutoff.

The application demonstrates correct management of capacity, selected demo identities, registration state and time within one session. Its engineering purpose is to provide requirements, verification, validation, tests, tool findings and human decisions that can be traced through a baseline and a controlled change.

## Users and scope

| Role | Meaningful operations |
|---|---|
| Participant | Browse; book/cancel own confirmed records before C; withdraw own waiting records before S; view own history. |
| Organiser | Create workshops more than 24 hours ahead; inspect owned confirmed rosters and, in V1.1, ordered waitlists. |

Use predefined fictional DemoUser records with stable IDs and fixed roles. Display names are not keys. Business functions reject unknown actors, role mismatch and non-owner actions. Selection does not authenticate a real person and cannot prevent a visitor selecting another demo identity.

Workshop details include title, aware start/end instants, location, capacity and optional preparation notes. Capacity is an integer from 1 to 30. Display Asia/Singapore, the start and the registration cutoff separately.

Workshops, My Bookings and Organiser may be views within app.py. No separate login system is required.

### Boundaries

Included: one provider, one-session state, serial rule operations, two meaningful roles, full dates, stable records, cancelled history and the selected C/S policy.

Excluded: real authentication/passwords, shared or durable storage, multi-user concurrency guarantees, payments, weather/map integrations, email/push, self-registration, whole-workshop cancellation, cross-workshop conflict checks, editing created workshop details/capacity and confirmed-roster overrides.

Organisers make weather and on-site safety decisions outside the application. Explain meeting/preparation information and the limits of a demonstration reservation.

## Release boundaries

| Release | Requirements |
|---|---|
| V1.0 | FR-01 through FR-07, applicable baseline BRs and QR-01 through QR-04. Includes strict creation lead, confirmed-roster closure and temporary session state. No waitlist implementation. |
| V1.1 | CR-01 adds FR-08 through FR-11 and extends cancellation/display. Preserve V1.0 actor, time, full-booking rejection, capacity, history and repeated-request contracts. |

V1.1 does not change C or reopen confirmed cancellation. Withdrawal until S applies to the newly introduced waitlist. Baseline tests with no waiters keep their original preconditions.

## Functional requirements

| ID | Release | Acceptance target |
|---|---|---|
| **FR-01** | V1.0 | A valid selected fictional actor resolves to its fixed ID/role. Unknown or inconsistent selection performs no restricted action. Switching/clearing selection preserves session business state. State explicitly that selection is not secure login. |
| **FR-02** | V1.0 | Show start, end, C, time zone, location, preparation, capacity and confirmed/remaining counts. Distinguish confirmed-roster closure from permitted waiting withdrawal and workshop start. Spare capacity does not reopen closed booking. |
| **FR-03** | V1.0 | Before C, a valid participant with no active registration can book an available place, receiving one CONFIRMED record/ID. Rejection leaves the entire input state unchanged. |
| **FR-04** | V1.0; extended V1.1 | An owner cancels a CONFIRMED record only before C, retaining history. Repetition allocates nothing further. V1.1 cancellation/promotion produces one complete state change. |
| **FR-05** | V1.0; extended V1.1 | Filter records/history by selected actor ID. Switching actors does not reset data. Filtering is not a real confidentiality boundary against identity selection. |
| **FR-06** | V1.0 | Organisers create valid workshops with S-t>24h, end>S and integer capacity 1-30. Assign IDs/ownership in the application. Invalid creation produces no record or counter advance. |
| **FR-07** | V1.0; extended V1.1 | Selected organisers read only owned rosters/counts. V1.1 adds ordered waiting records and operation-specific closure information. |
| **FR-08** | V1.1 | Explicitly join only when full, before C and without active duplication. Assign an increasing workshop-specific sequence; consume no confirmed place. |
| **FR-09** | V1.1 | Owner withdrawal is allowed while t<S, including C<=t<S. Change only that waiting registration; confirmed IDs/states/counts remain unchanged, and no promotion occurs. At/after S reject effective withdrawal. |
| **FR-10** | V1.1 | One effective confirmed cancellation before C promotes at most the earliest active waiter. Cancellation and promotion return together; no partial input mutation. No promotion at/after C. |
| **FR-11** | V1.1 | In-app refresh shows own state and current position. During C<=t<S explain that joining/promotion are closed but withdrawal remains allowed; after S show historical outcomes. Browser reload is not a state-preserving refresh. |

## Quality requirements

Every applicable critical scenario must be executed and pass before the relevant release. Planned scenarios and skipped checks are not passing evidence.

| ID | Measurable acceptance target | Planned evidence |
|---|---|---|
| **QR-01** | Selected valid, invalid, boundary and repeated serial actions preserve capacity, active uniqueness and the C/S matrix; V1.1 also preserves FIFO. Record zero invariant violations in those executed cases, without claiming shared-concurrency correctness. | B03-B09, B15; W03-W12; I01-I04, I10 |
| **QR-02** | Successful mutating functions return a complete new state without changing input. Rejection, no-op and injected failure preserve all original records and ID/queue counters. Repeats create no extra place allocation. | B16; W10/W16; I04/I05 |
| **QR-03** | Selected valid-actor role/owner violations are denied without mutation or mixed-record display. Use fictional data and disclose identity-selection limits; do not claim authentication or impersonation resistance. | B01/B02/B10/B12-B14; W13/W14; I08 |
| **QR-04** | Ordinary reruns and actor changes preserve the same-session state. Independent initialisations share no mutable collections. Explain browser reload/new-session/restart reset and verify that lifecycle rather than promising recovery. | I06/I07/I09; VAL-01/VAL-02/VAL-03 |

Coverage is diagnostic evidence, not an arbitrary HD threshold or proof of untested behaviour.

## Simple architecture

    app.py -> booking.py -> dataclasses and in-memory lists
                 |
          test_booking.py -> pytest and GitHub Actions

app.py handles views, demo actor selection and st.session_state. booking.py has no Streamlit dependency. Rule operations receive current state, selected actor and fresh trusted time and return an explicit outcome with candidate state. The UI assigns complete successful results only; it never adopts a partial failure.

Keep the core files simple. A small result record or constants can represent observable outcomes without introducing a framework, repository layer or external service.

| Data | Purpose |
|---|---|
| DemoUser | Predefined stable user_id, display_name and fixed role; not an authenticated account. |
| Workshop | ID, owner, title, aware start/end, location, capacity and notes. Derive C from S. |
| Registration | ID, workshop/user IDs, state and timestamps. Preserve cancelled history; rebooking uses a new ID. V1.1 adds queue_seq. |
| Demo state | Workshop/registration lists and necessary ID/queue counters, authoritative only within the current session. |

Switch fictional actors within one preserved browser session to demonstrate the workflow. Do not use mutable global booking state shared across independent sessions.

### Fixture and demonstration readiness

Use a controlled clock for automated tests. The dated examples in the rules are test examples, not a permanent live schedule.

At first demo-session initialisation, create bookable example workshops relative to current time with enough margin, such as at least 48 hours ahead. If closed/start-boundary examples are seeded, represent legitimate historical creation and registrations before C rather than allowing illegal late creation. Initialise once per session; do not regenerate timestamps on every rerun.

I07 checks representative baseline fixtures under V1.1 rules. It does not promise live-session upgrade, serialization or durable migration.

Target Python 3.12, Streamlit and pytest. Lock actual application and quality-tool versions in L1, aligned with deployment.

## Business rules

### Time and operation matrix

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

### Rules

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

#### Queue sequence and displayed position

queue_seq is stable historical ordering, not the displayed position. A waiting entry's current position is one plus the number of current WAITLISTED entries in the same workshop with smaller queue_seq.

Sequence gaps are not display gaps. With active sequences 3 and 8, positions are 1 and 2. Withdrawal can reduce positions during the final 24 hours without changing the confirmed roster or enabling promotion. After S, label any displayed queue as historical and closed.

#### Observable results

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

### Boundary examples

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

### State transitions

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

## Risk controls

The following is the accepted risk-control plan. Full business-control execution remains pending; foundation evidence and the current human decision are recorded in the [L2 review](docs/reviews/L2-human-review.md). The project author owns the risks. Initial ratings are qualitative planning judgements; R-08 remains VALIDATION_PENDING.

### Controls and planned acceptance

| ID / version | Risk and control | Acceptance evidence |
|---|---|---|
| **R-01** / Both | Overbooking, duplicate active records or stale replacement. Use current same-session state, validate capacity/uniqueness and serially adopt returned results. Verify last-place/repeated actions without claiming shared-concurrency correctness. | B04, B07-B09; W03/W04; I01/I02 |
| **R-02** / V1.1 | Unfair FIFO or incorrect transitions. Use stable sequences, earliest current WAITLISTED, tail rejoining and a complete cancellation/promotion result. Exclude withdrawn entries; never promote twice for one cancellation. | W05-W11/W15/W16; I03-I05 |
| **R-03** / Both | Missing selected-role/owner checks or overstated security. Enforce rules in booking.py, filter by selected ID and disclose freely switchable fictional identities. Use no real private data. These controls do not prevent identity impersonation. | B01/B02/B10/B12-B14; W13/W14; I08; scope acceptance |
| **R-04** / Both | Accidental rerun reset, aliased lists or misunderstood memory loss. Initialise once per session, preserve state on actor change and use independent state factories. Test actual lifecycle; new-session/restart reset remains a disclosed limitation. | I05-I09; VAL-01/VAL-02 |
| **R-05** / Both | Wrong timing, particularly blocking withdrawal at C or allowing it after S. Use fresh trusted time and operation-specific deadlines. Isolate C/S boundaries with fresh active records and test late form submission. | B03/B05/B06/B15/B16; W08/W12/W16; I10 |
| **R-06** / AI-assisted work | Unchecked AI assumptions, changed policy or unrelated complexity. Bound intent/files, preserve contracts, inspect oracles/dependencies and record human corrections and decisions. | AI-use, loop review, CR-01, PR and findings records |
| **R-07** / Both | Weak tests, false-positive denials or baseline regressions. Derive oracles from requirements; isolate each rejection cause, retain baseline tests and inspect collected/skipped/mocked scope. Protect full rejection, empty-queue cancellation and no-op safety. | B01-B17, W01-W16 and applicable I checks; especially B08/B11/B12/B15/B16, W06/W07/W10/W12 and I05 |
| **R-08** / Both | Misunderstood states, delayed confirmation awareness, cutoff restrictions or temporary data. Explain S/C, no notification, permitted waiting withdrawal, closed confirmed cancellation and session limits; validate actual tasks and feasibility. | VAL-01/VAL-02/VAL-03A-VAL-03E |

Acceptance requires the specified outcomes and state assertions in the linked scenarios, not merely a green report or a helper function's presence.

### Initial likelihood and impact

M means Medium; H means High. Unknown means evidence is still required.

| Risk | Likelihood / impact | Rationale |
|---|---|---|
| R-01 | M / H | Capacity is central and successive actions can use stale state. |
| R-02 | M / H | One state change can allocate a place to another participant. |
| R-03 | M / M for rule defects | Fictional-role checks matter; free identity selection is an intentional limitation, not solved authentication. |
| R-04 | M / H for accidental loss | Unexpected same-session loss breaks the demonstration; new-session reset is expected scope. |
| R-05 | M / H | C and S deliberately permit different actions. |
| R-06 | M / H | Generated work can retain superseded assumptions or change tests to fit code. |
| R-07 | M / H | An error can pass through weak assertions or a denial caused by the wrong precondition. |
| R-08 | Unknown / H | Preparation, arrival and restriction acceptability have not been observed. |

### Monitoring and human decisions

After each control is implemented, record owner, environment/SHA, expected and observed results, evidence, residual risk and decision using the [loop recording format](README.md#record-for-each-loop).

Progress from PLANNED to IMPLEMENTED_NOT_VERIFIED and then VERIFIED_FOR_STATED_SCOPE. Record residual acceptance separately; verification never means all possible failures are eliminated.

Capacity errors, selected-role/owner bypass, wrong C/S behaviour, partial mutation and material FIFO defects block the relevant release. Freely selectable actors and temporary unshared state are scope limitations only after clear disclosure and genuine author acceptance. They are not technically eliminated risks.

Use VAL-01/02 for baseline suitability and VAL-03 before V1.1 merge. Unresolved critical user needs prevent the relevant release. Return policy uncertainty to the human owner rather than adding authentication, notifications or overrides without an agreed change.

### Change-review depth

The planned CR-01 changes core user-visible business state. Start with Medium review depth and justify the actual classification at intake. Reclassify/escalate if the patch changes role boundaries, validation contracts, dependencies or broader data handling. The absence of a database removes migration concerns, not correctness responsibilities.

Track open blockers, missing evidence, test failures/skips, findings dispositions and outstanding human decisions. Do not substitute prompt counts or generated lines of code for quality measures.
